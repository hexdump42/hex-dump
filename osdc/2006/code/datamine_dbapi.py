import sqlite3

connectionString = '/home/mark/.gnome2/f-spot/photos.db'
dbcon = sqlite3.connect(connectionString)
cursor = dbcon.cursor()
commandText = """select * from photos, photo_tags, tags 
where photos.id = photo_tags.photo_id 
and photo_tags.tag_id = tags.id 
and tags.name = 'Publish To Web'"""
cursor.execute(commandText)
for row in cursor.fetchall():
    print row[2] + "/" + row[3]
cursor.close()
dbcon.close()
