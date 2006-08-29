"""
Informix database backend for Django.

Requires informixdb 2 http://informixdb.sourceforge.net/ and mx.DateTime
"""

from django.db.backends import util
try:
    import informixdb as Database
except ImportError, e:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured, "Error loading informixdb module: %s" % e
import datetime
try:
    import mx.DateTime
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured, "Error loading mx.DateTime module: %s" % e

import re
# RE for datetime of format YYYY-MM-DD HH:MM:SS.FFFFFF
re_datetime_with_fraction6 = re.compile("^\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}\.\d{6}$")
# RE for datetime of format YYYY-MM-DD HH:MM:SS
re_datetime_no_fraction = re.compile("^\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}$")

DatabaseError = Database.DatabaseError

try:
    # Only exists in Python 2.4+
    from threading import local
except ImportError:
    # Import copy of _thread_local.py from Python 2.4
    from django.utils._threading_local import local

class DatabaseWrapper(local):
    def __init__(self):
        self.connection = None
        self.queries = []

    def cursor(self):
        from django.conf import settings
        if self.connection is None:
            if settings.DATABASE_NAME == '':
                from django.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured, "You need to specify at least DATABASE_NAME in your Django settings file."
            conn_string = "%s" % (settings.DATABASE_NAME,)
            self.connection = Database.connect(conn_string)
        cursor = self.connection.cursor()
        if settings.DEBUG:
            return util.CursorDebugWrapper(FixedCursor(cursor), self)
        return FixedCursor(cursor)

    def _commit(self):
        return self.connection.commit()

    def _rollback(self):
        if self.connection:
            return self.connection.rollback()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

class FixedCursor(object):
    """
    Django uses "format" (e.g. '%s') style placeholders, but informixdb 
    uses "?" style.
    This fixes it -- but note that if you want to use a literal "%s" in a query,
    you'll need to use "%%s".
    """
    def __init__(self, cursor):
        self.cursor = cursor
        self.sqlerrd = cursor.sqlerrd
        self.rowcount = cursor.rowcount
	self.last_id = None

    def execute(self, query, params=None):
        if params is None: 
	    params = []
	else:
	    params = self.fix_datetime(params)
        query = self.fix_sql(query)
        query = self.convert_placeholders(query)
        results = self.cursor.execute(query, tuple(params))
	self.last_id = self.cursor.sqlerrd[1]
        return results

    def executemany(self, query, params=None):
        if params is None: 
	    params = []
	else:
	    params = self.fix_datetime(params)
        query = self.fix_sql(query)
        query = self.convert_placeholders(query)
        results = self.cursor.execute(query, tuple(params))
	self.last_id = self.cursor.sqlerrd[1]
        return results

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchmany(self, rows=Database.Cursor.arraysize):
        return self.cursor.fetchmany(rows)

    def convert_placeholders(self, query):
        # replace occurances of "%s" with "?" 
        return query.replace("%s","?")

    def fix_datetime(self, params):
        # convert datetime so informixdb can handle them
	for i in range(0,len(params)):
	    p = str(params[i])
	    if type(params[i]) == type(datetime.datetime.now()):
		params[i] = p[:-1]
	    else:
	        # Check to see if it's a datetime string with fraction 6
	        if re_datetime_with_fraction6.match(p) is not None:
		    params[i] = p[:-1]
		elif re_datetime_no_fraction.match(p) is not None:
		    dt = mx.DateTime.strptime(p, "%Y-%m-%d %H:%M:%S")
		    params[i] = Database.TimestampFromTicks(dt.ticks())
        return params

    def fix_sql(self, query):
        # Remove LIMIT keyword if present
	i = query.find(" LIMIT")
	if i > -1:
	    return query[0:i]
	else:
	    return query

supports_constraints = False

def quote_name(name):
    if name.startswith('[') and name.endswith(']'):
        return name # Quoting once is enough.
    return name

dictfetchone = util.dictfetchone
dictfetchmany = util.dictfetchmany
dictfetchall  = util.dictfetchall

def get_last_insert_id(cursor, table_name, pk_name):
    return cursor.last_id

def get_date_extract_sql(lookup_type, table_name):
    raise NotImplementedError
    # lookup_type is 'year', 'month', 'day'
    return "DATEPART(%s, %s)" % (lookup_type, table_name)

def get_date_trunc_sql(lookup_type, field_name):
    # lookup_type is 'year', 'month', 'day'
    if lookup_type=='year':
        return "EXTEND(%s, YEAR TO YEAR)" % field_name
    if lookup_type=='month':
        return "EXTEND(%s, MONTH TO MONTH)" % field_name
    if lookup_type=='day':
        return "EXTEND(%s, DAY TO DAY)" % field_name

def get_limit_offset_sql(limit, offset=None):
    return " "

def get_random_function_sql():
    raise NotImplementedError

def get_fulltext_search_sql(field_name):
    raise NotImplementedError

def get_drop_foreignkey_sql():
    return "DROP FOREIGN KEY"

def get_pk_default_value():
    return "DEFAULT"

OPERATOR_MAPPING = {
    'exact': '= %s',
    'iexact': 'LIKE %s',
    'contains': 'LIKE %s',
    'icontains': 'LIKE %s',
    'gt': '> %s',
    'gte': '>= %s',
    'lt': '< %s',
    'lte': '<= %s',
    'startswith': 'LIKE %s',
    'endswith': 'LIKE %s',
    'istartswith': 'LIKE %s',
    'iendswith': 'LIKE %s',
}
