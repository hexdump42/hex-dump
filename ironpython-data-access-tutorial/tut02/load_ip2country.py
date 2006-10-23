__doc__ = '''
load_ip2country.py - Load DB table with contents of ip-to-country.csv

A database must exist with the table structure defined in create_tables.py

Version created for tutorial 2 of IronPython ADO series.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT
'''
import sys
import dbapi
try:
    import sqlite as db
    dbapi._load_type(db.assembly,db.typename)
    connectstr = 'URI=file:ip2country.db,version=3'
except:
    import odbc as db
    dbapi._load_type(db.assembly,db.typename)
    connectstr = 'DSN=ip2country'

dbcon = db.connect(connectstr)

import re
re_csv = re.compile(',(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))')

cursor = dbcon.cursor()
insert_statement=  '''
    INSERT INTO ip2country (
        ipfrom, ipto, countrycode2, countrycode3, countryname
        ) VALUES ( ?,?,?,?,? )
'''

f = open("ip-to-country.csv")
print "Loading..."
for line in f.readlines():
    if line.endswith("\r\n"):
        line = line[:-2] # remove \r\n
    else:
	line = line[:-1] # just remove \n
    print line
    ipf, ipt, cc2, cc3, cn = re_csv.split(line)
    cursor.execute(insert_statement,(ipf[1:-1],ipt[1:-1],cc2[1:-1],cc3[1:-1],cn[1:-1]))
    dbcon.commit()

f.close()
dbcon.close()
