Development of Mono Applications with Agile Languages
=====================================================

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

A note on the examples

Most of the examples in this paper use or enhance an existing Mono application F-Spot [fspot]_. F-Spot is a full-featured personal photo management application written in C# for the GNOME desktop.


1. Agile Investigation
----------------------

2. Script Your Objects
----------------------

3. Simplify Your Unit Tests
---------------------------

Since we can script other CLI objects, it is easy to create simple unit tests.

4. Mine Your Data
-----------------

F-Spot uses SQLite 3 as it's relational data store. Since a SQLite ADO.NET provider comes with Mono, it is very easy with either Boo or IronPython to access the data store. In the examples we find all photos that have been tagged with "Publish To Web".

::

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

5. Throw Together A Web Interface
---------------------------------

6. Implement Objects
--------------------

7. Write A Complete Application
-------------------------------

While this paper has focused on how these agile languages can assist in development of an appliaction created with C#, both Boo and IronPython can create Windows Forms or GTK# applications, so there is no reason why capable...

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
