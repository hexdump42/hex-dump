Moonlight - Shiny, Pretty Things with XML?
==========================================

Author: Mark Rees

Introduction
------------

When Microsoft released Silverlight [silverlight]_, a cross platform, cross browser programming model for developing and distributing rich Internet applications (RIA) that use graphics, animations or video, they forgot Linux. But the Mono [mono]_ team corrected the oversight and created Moonlight [moonlight]_, the open source implementation. This paper will review the status of the implementation and provide an introduction on how to use Moonlight. It will also discuss how you can use Moonlight in a non Mono context.

What is Moonlight
-----------------

Moonlight is an open source implementation of Microsoft's Silverlight Web development technology. At the time of the writing of this paper, Moonlight is a work in progress implementation of both versions of Silverlight. 

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

To identify elements within a Moonlight application, naming of an element instance can be done using the X:Name property. Naming elements allows CLI language to easily access the element and is also required to animate elements.

::

 <Canvas
     xmlns="http://schemas.microsoft.com/client/2007"
     xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
     Height="600" Width="600"
     Background="Gray">
   <Rectangle 
       x:Name="MyRectangleOne"
       Canvas.Left="20" Canvas.Top="40" 
       Height="200" Width="200"
       Stroke="Black" StrokeThickness="10" Fill="Green" />
 </Canvas>

Simple animation

::

 <Canvas
     xmlns="http://schemas.microsoft.com/client/2007"
     xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
   <Canvas.Triggers>
        <EventTrigger RoutedEvent="Canvas.Loaded">
            <EventTrigger.Actions>
                <BeginStoryboard>
                    <Storyboard>
                        <ColorAnimation Storyboard.TargetName="MyRectangleOnesBrush"
                                           Storyboard.TargetProperty="Color"
                                           From="Green" To="Blue"
                                           Duration="0:0:5" />
                    </Storyboard>
                </BeginStoryboard>
            </EventTrigger.Actions>
        </EventTrigger>
   </Canvas.Triggers>

   <Rectangle
       x:Name="MyRectangleOne"
       Canvas.Left="20" Canvas.Top="40"
       Height="200" Width="200"
       Stroke="Black" StrokeThickness="10" >
        <Rectangle.Fill>
            <SolidColorBrush x:Name="MyRectangleOnesBrush" Color="Green" />
        </Rectangle.Fill>
   </Rectangle>
 </Canvas>

XAML is used to define the presentation layer for a Moonlight application, and relies on the application logic to be provided by either the browser javascript or a compiled assembly. The x:Class property allows the creation of a custom class in a CLI language that extends Canvas. The following example extends Canvas and prints the CPU load within the Rectangle.

xaml101-4.xaml - XAML to display rectangle with text block::

 <Canvas
     xmlns="http://schemas.microsoft.com/client/2007"
     xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="CPULoad.CpuMonitorPanel;assembly=monitor.dll"
        Loaded="PageLoaded" Width="300" Height="300">

        <Canvas.Resources>
            <Storyboard x:Name="run">
            </Storyboard>
            <Storyboard x:Name="color_sb">
                        <ColorAnimation x:Name="color_anim"
                                Storyboard.TargetName="CPULoadRectangleBrush"
                                Storyboard.TargetProperty="Color"
                                From="Green" To="Green" Duration="0:0:1" />
            </Storyboard>
    </Canvas.Resources>

   <Rectangle
       x:Name="CPULoadRectangle"
       Canvas.Left="20" Canvas.Top="40"
       Height="200" Width="200"
       Stroke="Black" StrokeThickness="10" >
        <Rectangle.Fill>
            <SolidColorBrush x:Name="CPULoadRectangleBrush" Color="White" />
        </Rectangle.Fill>
   </Rectangle>
   <TextBlock
       x:Name="Load"
       Text="100%"
       FontSize="36"
       FontWeight="Bold"
       Foreground="White"
       Canvas.Left="40"
       Canvas.Top="60" />
 </Canvas>

monitor.cs::

 using System;
 using System.IO;
 using System.Globalization;
 
 using System.Windows;
 using System.Windows.Input;
 using System.Windows.Controls;
 using System.Windows.Media;
 using System.Windows.Media.Animation;
 using System.Windows.Shapes;
 
 namespace CPULoad
 {
 	public struct CpuCounter {
		long user;
		long nice;
		long system;
		long idle;
		long iowait;
		long irq;
		long softirq;
		long steal;
		long total;
		
		public void Read (String line) {
			String[] parts = line.Split (new char[] {' '}, StringSplitOptions.RemoveEmptyEntries);
			total += (user = long.Parse (parts [1]));
			total += (nice = long.Parse (parts [2]));
			total += (system = long.Parse (parts [3]));
			total += (idle = long.Parse (parts [4]));
			total += (iowait = long.Parse (parts [5]));
			total += (irq = long.Parse (parts [6]));
			total += (softirq = long.Parse (parts [7]));
			total += (steal = long.Parse (parts [8]));
		}

		public CpuCounter Sub (ref CpuCounter other) {
			CpuCounter res = this;
			res.user -= other.user;
			res.nice -= other.nice;
			res.system -= other.system;
			res.idle -= other.idle;
			res.iowait -= other.iowait;
			res.irq -= other.irq;
			res.softirq -= other.softirq;
			res.steal -= other.steal;
			res.total -= other.total;
			return res;
		}

		public void FetchGlobalCounters() {
			using ( StreamReader sr = new StreamReader ("/proc/stat")) {
				String line = sr.ReadLine ();
				Read (line);
			}
		}
		
		public double CpuLoad () {
			return 100d * ((double)(total - idle) / total);
		}
	}

	public class CpuMonitorPanel : Canvas 
	{
		Shape cpurect;
		TextBlock load;
		CpuCounter last;
		ColorAnimation colorAnim;
		Storyboard colorSb;

		public void DrawLoad ()
		{
			CpuCounter cur = new CpuCounter ();
			cur.FetchGlobalCounters ();
			CpuCounter delta = cur.Sub (ref last);
			last = cur;
    		
			double num = Math.Round (delta.CpuLoad ());
			load.Text = ((int)num).ToString ();
			Color current = (cpurect.Fill as SolidColorBrush).Color;
			Color color = new Color ();

			if (num <= 50) {
				//interpolate (0,50) between green (0,255,0) and yellow (255,255,0)
				double red = num / (50d / 255);
				color = Color.FromRgb ((byte)red, 255, 0);
			} else {
				//interpolate (50,100) between yellow (255,255,0) and red (255,0,0)
				double green = (100d - num) / (50d / 255);
				color = Color.FromRgb (255, (byte)green, 0);
			}

			colorAnim.From = current;
			colorAnim.To = color;
			colorSb.Begin ();
		}

		public void PageLoaded (object o, EventArgs e) 
		{
			cpurect = FindName ("CPULoadRectangle") as Shape;
			load = FindName ("Load") as TextBlock;
			colorSb = FindName ("color_sb") as Storyboard;
			colorAnim = FindName ("color_anim") as  ColorAnimation;
			last = new CpuCounter ();

			Storyboard sb = FindName ("run") as Storyboard;
			DoubleAnimation timer = new DoubleAnimation ();
			((TimelineCollection)sb.GetValue(TimelineGroup.ChildrenProperty)).Add(timer);
			timer.Duration = new Duration (TimeSpan.FromMilliseconds (100));

			sb.Completed += delegate {
				DrawLoad ();
				sb.Begin ();
			};
			sb.Begin ();
			DrawLoad ();
		}
	}
 }

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
