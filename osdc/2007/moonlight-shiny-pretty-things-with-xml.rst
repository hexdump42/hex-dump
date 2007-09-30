Moonlight - Shiny, Pretty Things with XML?
==========================================

Author: Mark Rees

Introduction
------------

When Microsoft released Silverlight [silverlight]_, a cross platform, cross browser programming model for developing and distributing rich Internet applications (RIA) that use graphics, animations or video, they forgot Linux. But the Mono [mono]_ team corrected the oversight and created Moonlight [moonlight]_, the open source implementation. This paper will review the status of the implementation and provide an introduction on how to use Moonlight. It will also discuss how you can use Moonlight in a non Mono context.

What is Moonlight
-----------------

Moonlight is an open source implementation of Microsoft's Silverlight Web development technology. At the time of the writing of this paper, Moonlight implements both versions of Silverlight. 

Version 1.0 consists of a presentation framework responsible for UI, graphics, animation, and media playback. A Moonlight application is started when the Moonlight browser plugin is invoked within an HTML page. The plugin loads a XAML [xaml]_ file which contains a Canvas object. This Canvas object is the root element for all other elements used for the UI. These elements include basic graphic primitives and complex elements like images, and media. Moonlight can be manipulated by browser scripting languages thru modification of the DOM API it exposes. 

Version 1.1 improves the Canvas object whereby the XAML file can be augmented with code-behind code. It also supports an EMCA CLI [cli]_ runtime so it can execute compiled Mono code in a restricted environment with limited local file access.

Similar to Silverlight, Moonlight is implemented as a combination of managed and unmanaged code. The majority of the rendering pipeline is coded in C/C++ and currently uses Cairo [cairo]_, the 2D vector graphics library. Media decoding is done using FFmpeg [ffmpeg]_. This code is in the moon module [moon]_. The code for XAML, base scripting and Linq support is in the olive module [olive]_.

XAML 101
--------

Moonlight XAML is a subset of the Windows Presentation Framework [wpf]_ with a limited set of UI controls. In the context of Moonlight, XAML is a declarative XML-based language that defines graphical or UI elements and their properties in XML. 

Every Moonlight XAML contains a root Canvas element with Silverlight and XAML namespace declarations.

::

 <Canvas 
    xmlns="http://schemas.microsoft.com/client/2007"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
 </Canvas>

The Canvas element is used to contain and position other graphical primitive shapes, UI controls and additional Canvas elements. To add a shape to a Canvas, simply insert the shape element declaration between the <Canvas> tags. An element is positioned via the Canvas.Left and Canvas.Top properties. In the following example, a green filled Rectangle with a black border is added and positioned 20 pixels from the left and 40 pixels from the top of the Canvas. The Canvas element also has optional Height, Width and Background properties. 

::
 
 <Canvas
     xmlns="http://schemas.microsoft.com/client/2007"
     xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
     Height="600" Width="600"
     Background="Gray">
   <Rectangle 
       Canvas.Left="20" Canvas.Top="40" 
       Height="200" Width="200"
       Stroke="Black" StrokeThickness="10" Fill="Green" />
 </Canvas>

To view the above example in a Moonlight enabled web browser, the XAML could be saved to a file called xaml101-1.xaml, and a HTML page created that embeds the Moonlight plugin and references the example xaml file. An example of a HTML page follows. 

::

 <html>
 <head>
     <title>View Moonlight Example</title>
 </head>
 <body bgcolor="white">
    <p align="center">
        <object id="moonControl" width="600" height="600" type="application/x-silverlight">
            <param name="background" value="#ffebcd" />
            <param name="enableHtmlAccess" value="true" />
            <param name="source" value="xaml101-1.xaml" />
            <param name="windowless" value="false" />
         </object>
     </p>
  </body>
  </html>

Even though Silverlight was intended to be used within a web browser, the Moonlight team saw a use for the technology in developing Linux desktop widgets. To allow launching of Moonlight XAML files outside of a browser, there is now a command called mopen. It can also be used to launch Mono applications or directory packages of Mono/Moonlight executables and resources. So by entering the following command, it is possible to view the example without a web browser. 

::

 mopen xaml101-1.xaml

Conclusion
----------

Moonlight may be only alpha quality software (as Silverlight 1.1 is), but what the Moonlight team have achieved to-date makes me feel confident that the Linux community will not be left out of a Silverlight Rich Internet Applications world. Certainly Microsoft feels the same after announcing [silverlight4linux]_ a formal parnership with Novell to deliver Silverlight support for Linux with Moonlight.

References
----------

.. [silverlight] Silverlight Home Page
    (http://www.silverlight.net/)

.. [mono] Mono Home Page
    (http://www.mono-project.com/)

.. [moonlight] Moonlight Project Page
    (http://www.mono-project.com/Moonlight)

.. [xaml] Extensible Application Markup Language
    (http://xaml.net/)

.. [cairo] Cairo 2D Graphics Library Home Page
    (http://cairographics.org)

.. [ffmpeg] FFmpeg Project Home Page
    (http://ffmpeg.mplayerhq.hu/index.html)

.. [moon] Moonlight Rendering Pipeline
    (http://anonsvn.mono-project.com/viewcvs/trunk/moon/)

.. [olive] dotNet 3.x add-on libraries for Mono core
    (http://anonsvn.mono-project.com/viewcvs/trunk/olive/)

.. [cli] The Common Language Infrastructure (CLI) is an open specification developed by Microsoft that describes the executable code and runtime environment that form the core of the Microsoft .NET Framework.  

.. [wpf] Windows Presentation Foundation
     (http://msdn2.microsoft.com/en-us/library/ms754130.aspx)

.. [silverlight4linux] Microsoft announcement of Silverlight for Linux Support
    (http://weblogs.asp.net/scottgu/archive/2007/09/04/silverlight-1-0-released-and-silverlight-for-linux-announced.aspx)

Links to paper and code
-----------------------

.. [paper] Latest version of this paper
    (http://hex-dump.googlecode.com/svn/trunk/osdc/2007/moonlight-shiny-pretty-things-with-xml.html)

.. [code] Source code for all examples
    (http://hex-dump.googlecode.com/svn/trunk/osdc/2007/code)
