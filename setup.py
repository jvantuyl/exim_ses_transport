"""
setuptools installer for exim_ses_transport
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

from setuptools import setup, find_packages

setup(
	name = "EximSesTransport",
	version = "0.1",
	packages = find_packages(),
	install_requires = ['boto'],

	author = "Jayson Vantuyl",
	author_email = "jvantuyl@gmail.com",
	description = "provides a 'pipe' transport for Exim to deliver mail via Amazon SES",
	license = "LGPL",

	entry_points = { 'console_scripts': [ 'exim_ses_transport=exim_ses_transport.transport:run' ] }
)
