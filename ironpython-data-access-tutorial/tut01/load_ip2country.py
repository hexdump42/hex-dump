__doc__ = '''
load_ip2country.py - Load DB table with contents of ip-to-country.csv

A database must exist with the table structure defined in create_tables.py

Version created for tutorial 1 of IronPython ADO series.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT
'''
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

dbcon = dbconnection(connectstr)

dbcon.Open()

import re
re_csv = re.compile(',(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))')

dbcmd = dbcon.CreateCommand()
insert_statement=  '''
    INSERT INTO ip2country (
        ipfrom, ipto, countrycode2, countrycode3, countryname
        ) VALUES ( %s,%s,%s,%s,%s)
'''

f = open("ip-to-country.csv")
for line in f.readlines():
    line = line[:-2] # remove \r\n
    ipf, ipt, cc2, cc3, cn = re_csv.split(line)
    sqlcmd = insert_statement % (ipf, ipt, cc2, cc3, cn)
    print sqlcmd
    dbcmd.CommandText = sqlcmd
    dbcmd.ExecuteNonQuery()

f.close()
dbcon.Close()
