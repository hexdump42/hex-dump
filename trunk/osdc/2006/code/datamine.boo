import System
import System.Data from System.Data
import Mono.Data.SqliteClient

dbcon as SqliteConnection = SqliteConnection()
connectionString as string = 'URI=file:photos.db,version=3'
dbcon.ConnectionString = connectionString
dbcon.Open()
dbcmd as SqliteCommand = SqliteCommand()
dbcmd.Connection = dbcon
dbcmd.CommandText = """select * from photos, photo_tags, tags 
        where photos.id = photo_tags.photo_id 
        and photo_tags.tag_id = tags.id 
        and tags.name = 'Publish To Web'"""
reader as SqliteDataReader = dbcmd.ExecuteReader()
while reader.Read():
    print reader[2].ToString() + "/" + reader[3].ToString()
dbcon.Close()
