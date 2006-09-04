__doc__ = '''
create_tables.py - Create tables to hold data for ip address location.

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

dbcmd = dbcon.CreateCommand()
dbcmd.CommandText = '''
    CREATE TABLE ip2country (
        ipfrom          INTEGER,
        ipto            INTEGER,
        countrycode2    CHAR(2),
        countrycode3    CHAR(3),
        countryname     VARCHAR(50),
        PRIMARY KEY (ipfrom,ipto)
    )
'''

dbcmd.ExecuteNonQuery()

dbcmd.CommandText = '''
    CREATE TABLE flags (
        countrycode2    CHAR(2),
        flagimage       BLOB,
        PRIMARY KEY (countrycode2)
    )
'''

dbcmd.ExecuteNonQuery()

dbcon.Close()
