"""
Exim Transport for Amazon SES
"""

# Copyright 2011-2013, Jayson Vantuyl <jvantuyl@gmail.com>
# Copyright 2011, Toby White <tow@eaddrinu.se>
#
# This file is part of exim_ses_transport.
#
# exim_ses_transport is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# exim_ses_transport is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with exim_ses_transport.  If not, see <http://www.gnu.org/licenses/>.

from boto.ses import SESConnection
from boto.exception import BotoServerError
from dkim import DKIM
from email.parser import Parser
from os import environ, getpid
from sys import stdin, argv, stderr, exit, exc_info
from traceback import format_exc
from policy import EXIT_CODES, DKIM_INCLUDE_HEADERS, AWS_ALLOWED_HEADERS


class SesSender(object):
	logger = None

	def run(self):
		self.init_log()
		self.init_signer()
		try:
			self.log("Args: %r" % argv)
			self.log("Env: %r" % dict(environ))
			self.get_parties()
			self.get_credentials()
			self.make_connection()
			self.process_message()
			self.send_message()
		except Exception:
			self.abort('Unspecified error',1)

	def get_parties(self):
		try:
			self.sender = argv[1]
			self.recipients = argv[2:]
			self.log("sending from %s to %r" % (self.sender, self.recipients,))
		except Exception:
			self.abort('Missing Sender / Recipients',2,False)

	def get_credentials(self):
		try:
			self.aws_id = environ['AWS_ACCESS_KEY_ID']
			self.aws_key = environ['AWS_SECRET_KEY']
			self.log("configured to access AWS as %s" % self.aws_id)
		except Exception, e:
			self.abort('Missing AWS Credentials (%s)' % e.args[0],3, False)

	def make_connection(self):
		try:
			self.log("connecting to SES")
			self.conn = SESConnection(self.aws_id,self.aws_key)
		except Exception:
			self.abort('Failed to establish connection',4)

	def process_message(self):
		try:
			self.log("reading message")
			msg = stdin.read()
			if msg[:4] != 'From':
				self.abort('Message missing From header',5, False)
				return
			msg = self.sanitize_headers(msg)
			envelope,msg = msg.split('\n',1)
			self.msg = self.sign_message(msg)
			self.log('Sender: %r' % self.sender)
			self.log('Recipients: %r' % self.recipients)
			self.log('Message:\n' + msg)
		except Exception:
			self.abort('Failed to process message text',5)

	def sanitize_headers(self, msg):
		self.log("parsing message")
		msg_obj = Parser().parsestr(msg)
		for hdr in msg_obj.keys():
			if hdr not in AWS_ALLOWED_HEADERS and not hdr.startswith('X-'):
				self.log("sanitizing SES disallowed header: %s" % hdr)
				msg_obj['X-EximSESTransport-Sanitized-' + hdr] = msg_obj.pop(hdr)
		return str(msg_obj)

	def sign_message(self, msg):
		if self.dkim:
			self.log("generating DKIM signature")
			return DKIM(msg).sign(self.dkim_selector,
				self.dkim_domain, self.dkim_private_key,
				canonicalize=('relaxed', 'simple'),
				include_headers=DKIM_INCLUDE_HEADERS) + msg
		else:
			return msg

	def send_message(self):
		try:
			self.log("sending message")
			self.conn.send_raw_email(
				source=self.sender,
				raw_message=self.msg,
				destinations=self.recipients
			)
		except BotoServerError, bse:
			if 'InvalidTokenId' in bse.body:
				self.abort('Bad AWS Credentials (token)',6, False)
			if 'SignatureDoesNotMatch' in bse.body:
				self.abort('Bad AWS Credentials (signature)',6, False)
			if bse.error_code == 'Throttling':
				self.abort('Failed to actually deliver message: quota exceeded',9, False)
			self.abort('Failed to actually deliver message',7)
		except Exception:
			self.abort('Failed to actually deliver message',7)
		self.log("Delivered!")

	def abort(self,msg,code,exc=True):
		self.log("FATAL ERROR: " + msg)
		code_desc = EXIT_CODES.get(code, 'Unrecognized error code')
		etype, evalue, etb = exc_info()
		if evalue is None or not exc:
			print '%s (%r): %s' % (code_desc, code, msg)
		else:
			print '%s (%r): %s, %r' % (code_desc, code, msg, evalue) # for logging
			self.log(code_desc + '\n\nException:\n' + format_exc())
		exit(code)

	def init_log(self):
		if environ.get('DEBUG', '').lower() in ('1', 'true'):
			self.logger = file('/tmp/exim_ses_delivery_%s' % getpid(),'w')
		self.log('logging initialized')

	def init_signer(self):
		if environ.get('DKIM', '').lower() in ('1', 'true'):
			try:
				self.dkim_domain = environ['DKIM_DOMAIN']
				self.dkim_selector = environ['DKIM_SELECTOR']
				self.dkim_private_key = open(environ['DKIM_KEYFILE']).read()
				self.log("DKIM Configured: %s / %s" % (self.dkim_domain, self.dkim_selector,))
			except KeyError, e:
				self.abort('DKIM setup failed: %s not specified' % e.args[0], 8, False)
			except IOError:
				self.abort('DKIM setup failed: keyfile not found', 8, False)
			self.dkim = True
		else:
			self.dkim = False

	def log(self,msg,exc=True):
		if self.logger:
			print >>self.logger, msg
