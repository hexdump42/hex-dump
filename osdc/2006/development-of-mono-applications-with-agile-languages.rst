Development of Mono Applications with Agile Languages
=====================================================

Author: Mark Rees

Introduction
------------

The Mono [mono]_ implementation of the Common Language Infrastructure provides an opportunity to develop software components and applications that are cross language and platform. With agile languages like IronPython, and Boo now working on Mono, development of these applications can be quicker and easier. The paper will introduce both IronPython and Boo. It will also show a number of examples of how programmers can use these languages to aid their Mono application development.

The style and structure of this paper is influenced by Alan Greens "Six Things Groovy Can Do For You" [ag]_ from last years OSDC.

Boo
---

Boo [boo]_ is an object oriented statically typed programming language for the CLI with a Python inspired syntax.

The standard distribution includes the Boo libraries as well as a compiler, interpreter and interactive shell. The boo compiler and the programs it produces are 100% CIL [cil]_ and can be run on any compliant CLI virtual machine. 

Boo is the brainchild of Rodrigo Barreto de Oliveira's created in response to his frustation [manifesto]_ with the existing programming languages for the CLI.

Boo is licensed under a MIT/BSD style license.

This paper uses Boo 0.7.6 released in April 2006.

IronPython
----------

IronPython [fepy]_ aspires to be a strict Python implementation written in C#, that also allows full access to the CLI and base class libraries. 

The standard distribution is very close to a full implementation of core Python 2.4 with support for some of the new Python 2.5 additions. As well as being able to run as an interpreter or interactive shell, it is also possible to compile python code to CIL executables and assemblies. Only a subset of the standard Python libraries are provided in the IronPython assemblies. To access other non C code dependant standard library modules, the modules from the CPython 2.4 distribution must be installed.

IronPython was originally created by Jim Hugunin to investigate if the CLI was a terrible platform for dynamic languages as reports at the time were suggesting. When Jim joined the Microsoft CLR team in 2005, the Dynamic Languages team at Microsoft took over the development of IronPython.

IronPython is licensed under a Microsoft Shared Source license.

This paper uses IronPython 1.0 released in September 2006.

*A note on the examples*

Most of the examples in this paper use or enhance an existing Mono application F-Spot [fspot]_. F-Spot is a full-featured personal photo management application written in C# for the GNOME desktop. The full source code for the examples can be found in my online subversion repository [code]_.


1. Agile Investigation
----------------------

With both Boo and IronPython having interactive consoles that expose the full functionality of the language, and these provide an excellent environment for investigation and experimentation.

As an example of how easy it is to use, we will investigate and experiment with the F-Spot LibGPhoto2-Sharp assembly which is a C# wrapper for the gphoto2 [gphoto2]_ C library. This library allows UNIX-like operating systems to communicate with over 700 digital camera models.

Boo Shell - booish::

 >>> import LibGPhoto2 from "libgphoto2-sharp.dll"
 >>> dir(Camera)
 (Void .ctor(), Void SetAbilities(CameraAbilities),
 Void Init(LibGPhoto2.Context),...)
 >>> mycamera = Camera()
 LibGPhoto2.Camera
 >>> cx = Context()
 LibGPhoto2.Context

IronPython Console - mono ipy.exe::

 >>>

2. Script Your Objects
----------------------

3. Simplify Your Unit Tests
---------------------------

Since we can script other CLI objects, it is easy to create simple unit tests.

4. Mine Your Data
-----------------

F-Spot uses SQLite 3 as it's relational data store. Since a SQLite ADO.NET provider comes with Mono, it is very easy with either Boo or IronPython to access the data store. In the examples we find all photos that have been tagged with "Publish To Web".

datamine.boo::

 import System
 import System.Data from System.Data
 import Mono.Data.SqliteClient
 
 dbcon as SqliteConnection = SqliteConnection()
 connectionString as string = 'URI=file:photos.db,version=3'
 dbcon.ConnectionString = connectionString
 dbcon.Open()
 dbcmd as SqliteCommand = SqliteCommand()
 dbcmd.Connection = dbcon
 dbcmd.CommandText = "select * from photos, photo_tags,tags    
 where photos.id = photo_tags.photo_id 
 and photo_tags.tag_id = tags.id 
 and tags.name = 'Publish To Web'"
 reader as SqliteDataReader = dbcmd.ExecuteReader()
 while reader.Read():
     print reader[0].ToString()
 dbcon.Close()

datamine.py::

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

5. Throw Together A Web Interface
---------------------------------

Photos.aspx::

 <%@Page Inherits="HexDump.Examples.Boo.Web.FSpotPhotos.Photos" %>
 <html>
 <body>
 <form runat="server">
 <center>
 <div id="_photos" runat="server" >
 </div>
 </center>
 </form>
 </body>
 </html>

Snippet from Photos.aspx.boo::

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

6. Implement Objects
--------------------

7. Write A Complete Application
-------------------------------

While this paper has focused on how these agile languages can assist in development of an application created with C#, Boo and IronPython are capable of creating standalone Windows Forms, GTK# or Web applications. 

Conclusion
----------

Boo has better support for NUnit and can create CLI components that can be used by any other CLI language.

.. [mono] Mono Home Page
    (http://go-mono.org/)

.. [ag] Alan Green, Six Things Groovy Can Do For You
    (http://osdcpapers.cgpublisher.com/product/pub.84/prod.14)

.. [boo] Boo Home Page
    (http://boo.codehaus.org/)

.. [cil] Common Intermediate Language. Compiler and machine independent intermediate code that is run by an implementation of the Common Language Infrastructure.

.. [manifesto] Rodrigo Barreto de Oliveira, Boo Manifesto
    (http://boo.codehaus.org/BooManifesto.pdf)

.. [fepy] IronPython Home Page 
    (http://www.codeplex.com/IronPython)

.. [fspot] F-Spot Home Page
    (http://f-spot.org/)

.. [code] Source code for examples
    (http://hex-dump.googlecode.com/svn/trunk/osdc/2006/code

.. [gphoto2] gPhoto2 Digital Camera Software
    (http://www.gphoto.org/)
