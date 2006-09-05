__doc__ = '''
load_ip2country.py - Load DB table with contents of ip-to-country.csv

A database must exist with the table structure defined in create_tables.py

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
    from Mono.Data.SqliteClient import SqliteParameter as dbparam
    connectstr = 'URI=file:ip2country.db,version=3'
except:
    from System.Data.Odbc import OdbcConnection as dbconnection
    from System.Data.Odbc import OdbcParameter as dbparam
    connectstr = 'DSN=ip2country'

dbcon = dbconnection(connectstr)

dbcon.Open()

import re
re_csv = re.compile(',(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))')

dbcmd = dbcon.CreateCommand()
insert_statement=  '''
    INSERT INTO ip2country (
        ipfrom, ipto, countrycode2, countrycode3, countryname
        ) VALUES ( ?,?,?,?,? )
'''
# Create empty parameters for insert and attach to db command
p1 = dbparam()
dbcmd.Parameters.Add(p1)
p2 = dbparam()
dbcmd.Parameters.Add(p2)
p3 = dbparam()
dbcmd.Parameters.Add(p3)
p4 = dbparam()
dbcmd.Parameters.Add(p4)
p5 = dbparam()
dbcmd.Parameters.Add(p5)

dbcmd.CommandText = insert_statement

f = open("ip-to-country.csv")
print "Loading..."
for line in f.readlines():
    if line.endswith("\r\n"):
        line = line[:-2] # remove \r\n
    else:
	line = line[:-1] # just remove \n
    print line
    ipf, ipt, cc2, cc3, cn = re_csv.split(line)
    p1.Value = ipf[1:-1]
    p2.Value = ipt[1:-1]
    p3.Value = cc2[1:-1]
    p4.Value = cc3[1:-1]
    p5.Value = cn[1:-1]
    dbcmd.ExecuteNonQuery()

f.close()
dbcon.Close()
