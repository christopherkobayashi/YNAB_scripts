#! /usr/bin/env python2.7

import os
import sys
import csv
import getopt
from dateutil import parser

infile = os.environ['HOME']+'/Downloads/ACCT_xxx.csv'

opts, args = getopt.getopt(sys.argv[1:], "f:", ["file"])
for o, a in opts:
        if o in ("-f", "--file"):
                infile = a

print "Date,Payee,Category,Memo,Outflow,Inflow"

with open (infile, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile, ['Date', 'Payee', 'Amount', 'Account'])
	for line in csvreader:
		Date=parser.parse(line['Date'])
		Datestring=Date.strftime('%Y/%m/%d')
		Payto=line['Payee'][0:20].rstrip(' ')
		Memo_work=line['Payee'][20:].rstrip(' ')
		Memo = ''
		for word in Memo_work.split():
		  Memo=Memo+' '+word
		if len(Memo) > 0:
		  Memo = Memo.strip()
		  Memo = ' '+Memo
		Memo = Memo.replace(',', ' ')
		Account=line['Account'].strip("'")
		
		everything=Datestring+","+Payto+",,"+"("+Account+")"+Memo+',,'+line['Amount']
		print everything

print ",,,,,"
