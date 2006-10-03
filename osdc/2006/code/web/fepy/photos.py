import sqlite

def main(environ, start_response):
    connectionString = '/home/mark/.gnome2/f-spot/photos.db,version=3'
    dbcon = sqlite.connect(connectionString)
    cursor = dbcon.cursor()
    commandText = """select * from photos, photo_tags, tags 
        where photos.id = photo_tags.photo_id 
        and photo_tags.tag_id = tags.id 
        and tags.name = 'Publish To Web'"""
    cursor.execute(commandText)
    yield "<table><tr><th>Image Name</th><th>Location</th></tr>"
    for row in cursor.fetchall():
        yield "<tr><td>%s</td><td>%s</td></tr>" % (row[3], row[2])
    cursor.close()
    dbcon.close()
    yield "</table>"
