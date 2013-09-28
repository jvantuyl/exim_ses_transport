"""
Exim SES Transport Entry Points
"""

# Copyright 2013, Jayson Vantuyl <jvantuyl@gmail.com>
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

from transport import SesSender

def main():
	SesSender().run()
