__doc__ = '''

gdatareader.py - A quick and dirty GDATA reader

Version created for tutorial:

 http://hex-dump.blogspot.com/2006/08/agile-investigation-of-gdata-client.html

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT

'''
import clr
import System
clr.AddReference("gdata.dll")
import Google.GData.Client as GDClient

def parse(uri, nc=None):
  # Create a query and service object
  query = GDClient.FeedQuery()
  service = GDClient.Service("cl","hexdump-gdatareader-0.1")
  query.Uri = System.Uri(uri)
  return service.Query(query)

if __name__ == "__main__":
 feed = parse("http://feedparser.org/docs/examples/atom10.xml")
 for entry in feed.Entries:
     print entry.Title.Text,":",entry.Summary.Text
