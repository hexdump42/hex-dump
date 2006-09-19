namespace HexDump.Examples.Boo.Web.FSpotPhotos

import System
import System.Web
import System.Web.UI
import System.Web.UI.HtmlControls
import System.Data from System.Data
import Mono.Data.SqliteClient

class Photos(Page):

    _photos as HtmlGenericControl

    def Page_Load(sender, args as EventArgs):
        table = "<table><tr><th>Image Name</th><th>Location</th></tr>"
        for row as Boo.Lang.Hash in self.GetPhotosByTag('Publish To Web'):
            tabrow = "<tr><td>${row['name']}</td><td>${row['directory_path']}</td></tr>"
            table += tabrow
        table += "</table>"
        _photos.InnerHtml = table

    def GetPhotosByTag(tag):
        dbcon as SqliteConnection = SqliteConnection()
        connectionString as string = 'URI=file:/home/mark/.gnome2/f-spot/photos.db,version=3'
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
            row = {}
            row['directory_path'] = reader[2].ToString()
            row['name'] = reader[3].ToString()
            row['description'] = reader[4].ToString()
            yield row
        dbcon.Close()

