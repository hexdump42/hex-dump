import clr
import System
clr.AddReference("System.Data")
clr.AddReference("Mono.Data.SqliteClient")
from Mono.Data.SqliteClient import SqliteConnection, SqliteCommand

dbcon = SqliteConnection()
connectionString = 'URI=file:/home/mark/.gnome2/f-spot/photos.db,version=3'
dbcon.ConnectionString = connectionString
dbcon.Open()
dbcmd = SqliteCommand()
dbcmd.Connection = dbcon
dbcmd.CommandText = """select * from photos, photo_tags, tags 
where photos.id = photo_tags.photo_id 
and photo_tags.tag_id = tags.id 
and tags.name = 'Publish To Web'"""
reader = dbcmd.ExecuteReader()
while reader.Read():
    print reader[2].ToString() + "/" + reader[3].ToString()
dbcon.Close()
