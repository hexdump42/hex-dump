def get_table_list(cursor):
    tables = []
    cursor.execute("SELECT tabname FROM systables WHERE tabtype = 'T'")
    return [row[0] for row in cursor.fetchall()]

def get_table_description(cursor, table_name):
    return table_name

def get_relations(cursor, table_name):
    raise NotImplementedError

def get_indexes(cursor, table_name):
    raise NotImplementedError

DATA_TYPES_REVERSE = {}
