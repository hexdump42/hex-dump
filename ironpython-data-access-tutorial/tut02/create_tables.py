__doc__ = '''
create_tables.py - Create tables to hold data for ip address location.

Version created for tutorial 2 of IronPython ADO series.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT
'''
import dbapi
try:
    import sqlite as db
    dbapi._load_type(db.assembly,db.typename)
    connectstr = 'URI=file:ip2country.db,version=3'
    ip2country_create_table_ddl = '''
    CREATE TABLE ip2country (
        ipfrom          INTEGER,
        ipto            INTEGER,
        countrycode2    CHAR(2),
        countrycode3    CHAR(3),
        countryname     VARCHAR(50),
        PRIMARY KEY (ipfrom,ipto)
    )
    '''
except:
    import odbc as db
    dbapi._load_type(db.assembly,db.typename)
    connectstr = 'DSN=ip2country'
    ip2country_create_table_ddl = '''
    CREATE TABLE ip2country (
        ipfrom          DOUBLE,
        ipto            DOUBLE,
        countrycode2    CHAR(2),
        countrycode3    CHAR(3),
        countryname     VARCHAR(50),
        CONSTRAINT ip2country_pk PRIMARY KEY (ipfrom,ipto)
    )
    '''

dbcon = db.connect(connectstr)

cursor = dbcon.cursor()

cursor.execute(ip2country_create_table_ddl)

dbcon.commit()

dbcon.close()
