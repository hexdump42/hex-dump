Development of Mono Applications with Agile Languages
=====================================================

Author: Mark Rees

Introduction
------------

Mono [mono]_, the open source implementation of the Microsoft's Common Language Infrastructure [cli]_ aka .NET, provides an opportunity to develop software components and applications that are cross language and cross platform. With agile languages like Boo, and IronPython now working on Mono, development of these applications can be quicker and easier. The paper will introduce both Boo and IronPython. It will also show a number of examples of how programmers can use these languages to aid their Mono application development. The paper is not intended to be a side by side comparison of Boo and IronPython, but demonstrate that agile languages run well under Mono and are a useful addition to a programmers toolbox.

The style and structure of this paper is influenced by Alan Greens "Six Things Groovy Can Do For You" [ag]_ from last years OSDC.

Boo
---

Boo [boo]_ is an object oriented statically typed programming language for the CLI with a Python inspired syntax.

Boo is the brainchild of Rodrigo Barreto de Oliveira's created in response to his frustration [manifesto]_ with the existing programming languages for the CLI.

The standard distribution includes the Boo libraries as well as a compiler, interpreter and interactive shell. The boo compiler and the programs it produces are 100% Common Intermediate Language (CIL) [cil]_ and can be run on any compliant CLI virtual machine. The language supports automatic variable declaration, type inference, and type casting. It also supports first class functions and generators, and duck typing.

Currently Boo's support for Generics is not fully compliant.

Boo is licensed under a MIT/BSD style license.

IronPython
----------

IronPython [fepy]_ aspires to be a strict Python implementation written in C#, that also allows full access to the CLI and base class libraries. 

IronPython was originally created by Jim Hugunin to investigate if the CLI was a terrible platform for dynamic languages as reports at the time were suggesting. When Jim joined the Microsoft CLR team in 2005, the Dynamic Languages team at Microsoft took over the development of IronPython.

The standard distribution is very close to a full implementation of core Python 2.4 with support for some of the new Python 2.5 additions. As well as being able to run as an interpreter or interactive shell, it is also possible to compile Python code to CIL executables and assemblies. Only a subset of the standard Python libraries are provided in the IronPython assemblies. To access other non C code dependant standard library modules, the modules from the CPython 2.4 distribution must be installed.

IronPython currently cannot create assemblies and CLI types that can easily been used by other CLI languages. It's lack of support for CLI attributes makes it harder to use with some Mono tools and services.

IronPython is licensed under a Microsoft Shared Source license.

*A note on the examples*

Most of the examples in this paper use or enhance an existing Mono application F-Spot [fspot]_. F-Spot is a full-featured personal photo management application written in C# for the GNOME desktop. The full source code for the examples can be found in my on-line subversion repository [code]_. The code examples were developed under Mono 1.1.18.0, Boo 0.7.6 and IronPython Community Edition 1.0r3 [ipce]_.

1. Agile Investigation
----------------------

Both Boo and IronPython having interactive consoles that expose the full functionality of the language, and these provide an excellent environment for investigation and experimentation.

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
 >>> mycamera.Init(cx)
 >>> mycamera.GetAbilities().model
 'Kodak DX6340'

IronPython Console - mono ipy.exe::

 >>> import clr
 >>> clr.AddReference("libgphoto2-sharp.dll")
 >>> import LibGPhoto2
 >>> dir(LibGPhoto2.Camera)
 ['Capture', 'CapturePreview',...] 
 >>> LibGPhoto2.Camera.__doc__
 'Camera()'
 >>> mycamera = LibGPhoto2.Camera()
 >>> cx = LibGPhoto2.Context()
 >>> mycamera.Init(cx)
 >>> mycamera.GetAbilities().model
 'Kodak DX6340'

2. Script Your Objects
----------------------

Now we have played with the LibGPhoto2 Camera object, let's make it do something useful. Using IronPython we will script the object to discover and list all the photos stored on the camera. 

Snippet from script_camera.py::

 camera.Init(cx)
 camera_fs = camera.GetFS()
 
 files = []
 
 def get_filelist(dir):
     filelist = camera_fs.ListFiles(dir,cx)
     i = 0
     while i < filelist.Count():
         files.append((dir,filelist.GetName(i)))
         i += 1
     # process subdirectories
     folderlist = camera_fs.ListFolders(dir, cx)
     i = 0
     while i < folderlist.Count():
         get_filelist(dir + folderlist.GetName(i) + "/")
         i += 1
 
 get_filelist("/")
 print files
 
As well as accessing the objects using simple external scripts, both Boo and IronPython provide api's that allow them to be embedded within Mono applications as dedicated scripting engines. 

3. Simplify Your Unit Tests
---------------------------

Since we can script other CLI objects, it is easy to create simple unit tests. As Boo can create library assemblies and supports CLI attributes, it can be used to create NUnit [nunit]_ test fixtures as the following example shows:

fspot_unittest.boo::

 import NUnit.Framework from "nunit.framework"
 import LibGPhoto2 from "libgphoto2-sharp.dll"
 
 [TestFixture]
 class LibGPhoto2Fixture:
     [Test]
     def TestCamera():
         assert Camera()
 
     [Test]
     def Testcontext():
         assert Context()

IronPython's inability to create fixtures for NUnit doesn't prevent it being used to unit-test CLI code. IronPython can use the Python standard library unittest to achieve the same results.

fspot_unittest.py::

 import unittest
 import clr
 clr.AddReference("libgphoto2-sharp.dll")
 import LibGPhoto2
 
 class TestLibGPhoto2(unittest.TestCase):
     """
     A simple test case for the FSpot LibGPhoto2 wrapper
     """
 
     def setUp(self):
         pass
 
     def tearDown(self):
         pass
 
     def test_Camera(self):
         self.assert_(LibGPhoto2.Camera(),"Creation of Camera object failed.")
 
     def test_Context(self):
         self.assert_(LibGPhoto2.Context(),"Creation of Context object failed.")
 
 def suite():
     suite = unittest.TestSuite()
     suite.addTest(unittest.makeSuite(TestLibGPhoto2))
     return suite
 
 if __name__ == "__main__":
     unittest.TextTestRunner(verbosity=2).run(suite())

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
     print reader[2].ToString()
 dbcon.Close()

While IronPython could directly use the SQLite ADO.NET provider, an IronPython implementation [ipce]_ of the Python DB-API is available. An example using the DB-API is shown below:

datamine_dbapi.py::

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

5. Throw Together A Web Interface
---------------------------------

Under Mono, the normal method of publishing a website is via the Mono implementation of ASP.NET. ASP.NET uses a technology called the Code Document Object Model (CodeDOM) which allows CLI languages to provide the presentation and business logic. Boo and IronPython can be used in this context, but IronPythons ASP.NET CodeDOM support is only a proof of concept and will be removed in a future release. The following code snippets show how Boo can used to publish a table of f-spot images. [boo-web]_

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

As stated previously, IronPython CodeDOM support will be removed in a future release, and ASP.NET support for dynamic languages will be provided using a new model [aspnet_dlem]_. To allow the use of IronPython for ASP.NET development today, Seo Sanghyeon, Christoper Baus and the author have been working on an ASP.NET handler [wsgihdlr]_ which implements a WSGI [wsgi]_ gateway. This handler allows IronPython code that implements the simple WSGI application model to be hosted by ASP.NET. The following code snippet [fepy-web]_ uses the gateway to publish a table of f-spot images.

Code snippet from photos.py::

 import sqlite3
 
 def main(environ, start_response):
     connectionString = '/home/mark/.gnome2/f-spot/photos.db'
     dbcon = sqlite3.connect(connectionString)
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

Conclusion
----------

While this paper has focused on how these agile languages can assist in development of an application created with C#, Boo and IronPython are very capable of creating standalone Windows Forms [wfex]_, GTK# or Web applications. 

Both languages have features that differentiate them. Boo's ability to create CLI components that can be used by any other CLI language. Also being able to work seamlessly with NUnit and NAnt. IronPython's access to the Python standard library and other Python code at runtime.

But both languages offer a number of advantages over core CLI languages like C#.

 * An interactive environment to develop and test code.

 * Clean and wrist-friendly syntax.

 * Automatic type inference and casting.

Hopefully I have been able to give you the incentive to investigate using agile languages as part of your Mono development toolbox.

References
----------

.. [mono] Mono Home Page
    (http://go-mono.org/)

.. [cli] Common Language Infrastructure, an open specification developed by Microsoft that describes the executable code and runtime environment that forms the core of the Microsoft .NET Framework.
     (http://www.ecma-international.org/publications/standards/Ecma-335.htm)

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

.. [ipce] IronPython Community Edition 1.0 download. This version has number of patches that fix issues when running under Mono, and a subset of the CPython standard library that is known to run under IronPython.
    (http://sourceforge.net/project/showfiles.php?group_id=178069)

.. [gphoto2] gPhoto2 Digital Camera Software
    (http://www.gphoto.org/)

.. [nunit] Unit testing framework for CLI languages.
    (http://www.nunit.org/)

.. [aspnet_dlem] The New Dynamic Language Extensibility Model for ASP.NET Whitepaper
    (http://www.asp.net/ironpython/WhitePaper.aspx?tabid=62)

.. [wsgihdlr] ASP.NET WSGI Handler
    (https://svn.sourceforge.net/svnroot/fepy/trunk/src/)
    (https://svn.sourceforge.net/svnroot/fepy/trunk/lib/wsgi.py)

.. [wsgi] Web Services Gateway Interface PEP.
    (http://www.python.org/dev/peps/pep-0333/)

.. [wfex] A Windows.Forms GUI for GDATA Reader Example
    (http://hex-dump.blogspot.com/2006/08/windowsforms-gui-for-gdata-reader_12.html)

Links to code examples
----------------------

.. [code] Source code repository for all examples
    (http://hex-dump.googlecode.com/svn/trunk/osdc/2006/code/)

.. [boo-web] directory containing boo code, aspx page, web.config and nant build file for Boo ASP.NET example.
    (http://hex-dump.googlecode.com/svn/trunk/osdc/2006/code/web/boo/)

.. [fepy-web] directory containing IronPython code for IronPython ASP.NET example.
    (http://hex-dump.googlecode.com/svn/trunk/osdc/2006/code/web/fepy/)
