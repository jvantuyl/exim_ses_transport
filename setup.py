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

from setuptools import setup

setup(
	name = "EximSesTransport",
	version = "0.4pre",

	description = 'An Amazon SES transport for the Exim MTA.',
	platforms = [ 'any' ],
	author = "Jayson Vantuyl",
	author_email = "jvantuyl@gmail.com",
	long_description = """Amazon's cloud includes a service to send e-mail through their infrastructure.
While this is useful, sometimes there's just no substitute for an MTA.  This
transport allows you to selectively integrate Amazon's SES with one of the
Internet's most powerful MTAs, Exim.
""",
	url = 'https://github.com/jvantuyl/exim_ses_transport',
	license = "http://www.gnu.org/copyleft/lesser.html",
	classifiers = [
		'Topic :: Communications :: Email :: Filters',
		'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)'
	],

	packages = ['exim_ses_transport'],
	install_requires = ['boto>=2.0', 'dkimpy>=0.5'],
	dependency_links = ['https://launchpad.net/dkimpy/trunk/0.5.4/+download/dkimpy-0.5.4.tar.gz#egg=dkimpy-0.5.4'],
	entry_points = { 'console_scripts': [ 'exim_ses_transport=exim_ses_transport.run:main' ] }
)
