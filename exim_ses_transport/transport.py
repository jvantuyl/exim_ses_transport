"""
Exim Transport for Amazon SES
"""

# Copyright 2011, Jayson Vantuyl <jvantuyl@gmail.com>
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
from os import environ, getpid
from sys import stdin, argv, stderr, exit, exc_info
from traceback import format_exc

# Exit Codes
# 1 Unspecified Fatal Badness
# 2 Missing Sender / Recipients
# 3 Missing AWS Credentials
# 4 Failed to establish connection
# 5 Failed to process message text
# 6 Bad AWS Credentials
# 7 Error actually delivering message

class SesSender(object):
	logger = None

	def run(self):
		self.init_log()
		try:
			self.log("Args: %r" % argv)
			self.log("Env: %r" % dict(environ))
			self.get_parties()
			self.get_credentials()
			self.make_connection()
			self.process_message()
		except Exception:
			self.abort('Unspecified error',1)

	def get_parties(self):
		try:
			self.sender = argv[1]
			self.recipients = argv[2:]
		except Exception:
			self.abort('Missing Sender / Recipients',2)

	def get_credentials(self):
		try:
			self.aws_id = environ['AWS_ACCESS_KEY_ID']
			self.aws_key = environ['AWS_SECRET_KEY']
			assert self.aws_id is not None
			assert self.aws_key is not None
		except Exception:
			self.abort('Missing AWS Credentials',3)

	def make_connection(self):
		try:
			self.conn = SESConnection(self.aws_id,self.aws_key)
		except Exception:
			self.abort('Failed to establish connection',4)

	def process_message(self):
		try:
			msg = stdin.read()
			assert msg[:4] == 'From'
			envelope,msg = msg.split('\n',1)
			self.log('Sender: %r' % self.sender)
			self.log('Recipients: %r' % self.recipients)
			self.log('Message:\n' + msg)
		except Exception:
			self.abort('Failed to process message text',5)
		try:
			self.conn.send_raw_email(
				source=self.sender,
				raw_message=msg,
				destinations=self.recipients
			)
		except BotoServerError, bse:
			if 'InvalidTokenId' in bse.body:
				self.abort('Bad AWS Credentials (token)',6)
			if 'SignatureDoesNotMatch' in bse.body:
				self.abort('Bad AWS Credentials (signature)',6)
			self.abort('Failed to actually deliver message',7)
		except Exception:
			self.abort('Failed to actually deliver message',7)
		self.log("Delivered!")

	def abort(self,msg,code,exc=True):
		self.log("FATAL ERROR: " + msg)
		if exc:
			self.log('Exception:\n' + format_exc())
			etype, evalue, etb = exc_info()
			print repr(evalue) # for logging
		exit(code)

	def init_log(self):
		if 'DEBUG' in environ:
			self.logger = file('/tmp/exim_ses_delivery_%s' % getpid(),'w')

	def log(self,msg,exc=True):
		if self.logger:
			print >>self.logger, msg

def run():
	SesSender().run()

