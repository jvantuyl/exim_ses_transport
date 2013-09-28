"""
AWS / DKIM / SES Transport Policy Data
"""

# Copyright 2013, Jayson Vantuyl <jvantuyl@gmail.com>
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

# Exit Codes
EXIT_CODES={
	1: 'Unspecified fatal error',
	2: 'Missing Sender / Recipients',
	3: 'Missing AWS Credentials',
	4: 'Failed to establish connection',
	5: 'Failed to process message text',
	6: 'Bad AWS Credentials',
	7: 'Error actually delivering message',
	8: 'Bad or missing DKIM credentials',
	9: 'Over quota',
}

# All recommended headers except for Date, Message-ID which Amazon may alter.
DKIM_INCLUDE_HEADERS = (
	"Cc",
	"Content-Description",
	"Content-ID",
	"Content-Transfer-Encoding",
	"Content-Type",
	"From",
	"In-Reply-To",
	"List-Archive"
	"List-Help",
	"List-Id",
	"List-Owner",
	"List-Post",
	"List-Subscribe",
	"List-Unsubscribe",
	"MIME-Version",
	"References",
	"Reply-To",
	"Resent-Cc",
	"Resent-Date",
	"Resent-From",
	"Resent-Message-ID",
	"Resent-Sender",
	"Resent-To",
	"Sender",
	"Subject",
	"To",
)

# All headers allowed by AWS (as of 2013-09-28), see http://docs.aws.amazon.com/ses/latest/DeveloperGuide/header-fields.html
AWS_ALLOWED_HEADERS = (
	"Accept-Language",
	"acceptLanguage",
	"Archived-At",
	"Authentication-Results",
	"Auto-Submitted",
	"Bcc",
	"Bounces-To",
	"Cc",
	"Comments",
	"Content-Alternative",
	"Content-Class",
	"Content-Description",
	"Content-Disposition",
	"Content-Features",
	"Content-ID",
	"Content-Language",
	"Content-Length",
	"Content-Location",
	"Content-MD5",
	"Content-Transfer-Encoding",
	"Content-Type",
	"Date",
	"DKIM-Signature",
	"DomainKey-Signature",
	"Errors-To",
	"From",
	"Importance",
	"In-Reply-To",
	"Keywords",
	"List-Archive",
	"List-Help",
	"List-Id",
	"List-Owner",
	"List-Post",
	"List-Subscribe",
	"List-Unsubscribe",
	"Message-Context",
	"Message-ID",
	"MIME-Version",
	"Organization",
	"Original-From",
	"Original-Message-ID",
	"Original-Recipient",
	"Original-Subject",
	"PICS-Label",
	"Precedence",
	"Priority",
	"Received",
	"Received-SPF",
	"References",
	"Reply-To",
	"Return-Path",
	"Return-Receipt-To",
	"Sender",
	"Sensitivity",
	"Subject",
	"Thread-Index",
	"Thread-Topic",
	"To",
	"User-Agent",
	"VBR-Info",
)
