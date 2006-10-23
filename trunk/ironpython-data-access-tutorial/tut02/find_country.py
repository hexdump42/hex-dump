__doc__ = '''
find_country.py - Find country of IP address.

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

def ip2number(ipaddress):
    '''
    Convert dotted IP address to number
    '''
    A,B,C,D = ipaddress.split(".")
    return (int(A) * 16777216) + (int(B) * 65536) + (int(C) * 256) + int(D)

dbcon = db.connect(connectstr)

cursor = dbcon.cursor()

try:
    ipaddress = sys.argv[1]
    # Convert dotted ip address to number
    ipnumber = ip2number(ipaddress)
except:
    print "Error - An IP Address is required"
    sys.exit(1)

select_statement = '''SELECT * FROM ip2country 
    WHERE ipfrom <= %s
    AND ipto >= %s
''' % (ipnumber, ipnumber)

cursor.execute(select_statement)

row = cursor.fetchone()
print "The location of IP address %s is %s." % (ipaddress, row[4])

dbcon.close()

