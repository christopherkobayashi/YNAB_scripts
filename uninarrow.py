#! /usr/bin/env python2.7

#	uninarrow.py
#	Copyright (C) 2019 Christopher Kobayashi <software+github@disavowed.jp>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import unicodedata
import fileinput

for line in sys.stdin:
	line = line.rstrip('\n')
	outline = unicodedata.normalize('NFKC', line.decode('utf8'))
	print (outline.encode('UTF-8'))
