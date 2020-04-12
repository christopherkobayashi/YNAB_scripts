#! /usr/bin/env python2.7

#	prestia.py
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

import csv
import os
import unicodedata
import sys
import re
import time
import codecs
from datetime import date
from datetime import datetime

if len(sys.argv) is not 2:
	print ("prestia.py: must specify an input file.")
	exit (1)

print ('!Type:Bank')

with open( sys.argv[1], 'rb') as csvfile:
	rows = csv.reader(csvfile, delimiter=',')

	next(rows)
	for row in rows:
		if not row:
			break
		year, month, day = row[0].split('/')
		trans_date = date(int(year), int(month), int(day))
		payee = row[1].decode('shift-jis').encode('utf-8')
		payee = unicodedata.normalize('NFKC', payee.decode('utf8'))
		payee = re.sub("\s\s+", " ", payee)
		if row[2] != "":
			amount = '-'+str(int(row[2]))
		elif row[3] != "":
			amount = int(row[3])
			
		print ('D' + trans_date.strftime('%Y/%m/%d'))
		print ('T' + str(amount))
		print ('Cc')
		print ('P' + payee.encode('UTF-8'))
		print ('^')
