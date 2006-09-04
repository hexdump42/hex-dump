__doc__ = '''
find_country_dtuple.py - Find country of IP address dtuple example.

Version created for tutorial 1 of IronPython ADO series.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT

Credits:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81252

'''
import sys
import clr
import System
from System import Object, Array
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

# Use dtuple to allow access by column name
# http://www.lyra.org/greg/python/dtuple.py
import dtuple
schema = reader.GetSchemaTable()
descr = dtuple.TupleDescriptor([[n['ColumnName']] for n in schema.Rows])
while reader.Read():
    rowvalues = Array.CreateInstance(Object, reader.FieldCount)
    reader.GetValues(rowvalues)
    row = dtuple.DatabaseTuple(descr,tuple(rowvalues)) 
    print "The location of IP address %s is %s." % (ipaddress, row['countryname'])

reader.Close()
dbcon.Close()

