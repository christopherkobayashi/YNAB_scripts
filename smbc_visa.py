#! /usr/bin/env python2.7
# -*- coding: utf8 -*-

#    smbc_visa.py
#    Copyright (C) 2019 Christopher Kobayashi <software+github@disavowed.jp>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


# This script takes a CSV file manually downloaded from Sumitomo-Mitsui Bank
# Card web site (https://www.smbc-card.com), converts it to Unicode, and
# rearranges it into QIF format.
# Charges spread out over multiple months ("kai") are handled.
# Charges in foreign currency are noted and the exchange rate is calculated.

import csv
import os
import unicodedata
import sys
import re
import time
from datetime import date
from datetime import datetime

print ('!Type:CCard')

first_line = 0

ymd_field = 0
payee_field = 1

with open( sys.argv[1], 'rb') as csvfile:
	rows = csv.reader(csvfile, delimiter=',')
	for row in rows:

		if not row[0]:
			continue
		if row[0] and row[0][0].isdigit() and not first_line:
			amount_field = 6
			period_field = 2
			period_count = 5
			currency_field = 10
			amount_foreign = 9
			amount_ratio = 11
			comment_field = 4
			type = 1
			first_line = 1
		elif not first_line:
			amount_field = 5
			period_count = 3
			period_field = 4
			comment_field = 6
			type = 2
			first_line = 1
			continue

		year, month, day = row[ymd_field].split('/')
		trans_date = date(int(year), int(month), int(day))
		payee = row[payee_field].decode('shift-jis').encode('utf-8')
		payee = unicodedata.normalize('NFKC', payee.decode('utf8'))
		payee = re.sub("\s\s+", " ", payee)
		amount = row[amount_field]

		if type is 1:
			# if the charge is made by someone other than you, add it)
			if row[period_field] != "ご本人" and row[period_field] != 1:
				comment = row[period_field] + ' '
			comment = 'Period: ' + row[period_count]
			if row[currency_field] and row[currency_field] != "JPY":
				comment = comment + ' ' + row[currency_field] + ' ' + row[amount_ratio] + ' (' + row[amount_foreign] + ')'
			if row[comment_field]:
				comment = comment + ' (' + row[comment_field] + ')'
				newmonth = int(month)+(int(row[comment_field][1])-1)
				if newmonth > 12:
					newmonth = newmonth - 12
					newyear = int(year)+1
					year = str(newyear)
				month = str(newmonth)
				trans_date = date(int(year), int(month), int(day))
		else:
				comment = row[comment_field]

		comment = comment.decode('shift-jis').encode('utf-8')
		comment = unicodedata.normalize('NFKC', comment.decode('utf8'))
		comment = re.sub("\s\s+", " ", comment)

		amount = -int(amount)

		print ('D' + trans_date.strftime('%Y/%m/%d'))
		print ('T' + str(amount))
		print ('P' + payee.encode('UTF-8'))
		print ('M' + comment.encode('UTF-8'))
		print ('^')

