__doc__ = '''
find_country.py - Find country of IP address.

Version created for tutorial 1 of IronPython ADO series.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT
'''
import sys
import clr
import System
clr.AddReference("System.Data")
import System.Data
try:
    clr.AddReference("Mono.Data.SqliteClient")
    from Mono.Data.SqliteClient import SqliteConnection as dbconnection
    connectstr = 'URI=file:ip2country.db,version=3'
except:
    clr.AddReference("System.Data.ODBCClient")
    from System.Data.Odbc import OdbcConnection as dbconnection
    connectstr = 'DSN=ip2country'

def ip2number(ipaddress):
    '''
    Convert dotted IP address to number
    '''
    A,B,C,D = ipaddress.split(".")
    return (int(A) * 16777216) + (int(B) * 65536) + (int(C) * 256) + int(D)

dbcon = dbconnection(connectstr)

dbcon.Open()

dbcmd = dbcon.CreateCommand()

try:
    ipaddress = sys.argv[1]
    # Convert dotted ip address to number
    ipnumber = ip2number(ipaddress)
except:
    print "Error - An IP Address is required"
    sys.exit(1)


dbcmd.CommandText = '''
    SELECT * FROM ip2country 
    WHERE ipfrom <= %s
    AND ipto >= %s
''' % (ipnumber, ipnumber)


reader = dbcmd.ExecuteReader()

while reader.Read():
    print "The location of IP address %s is %s." % (ipaddress, reader[4])

reader.Close()
dbcon.Close()

