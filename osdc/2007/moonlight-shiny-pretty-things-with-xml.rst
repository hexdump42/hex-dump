Moonlight - Shiny, Pretty Things with XML?
==========================================

Author: Mark Rees

Introduction
------------

When Microsoft released Silverlight [silverlight]_, a cross platform, cross browser programming model for developing and distributing rich Internet applications (RIA) that use graphics, animations or video, they forgot Linux. But the Mono [mono]_ team corrected the oversight and created Moonlight [moonlight]_, the open source implementation. The paper will review the status of the implementation and provide an introduction on how to use Moonlight. It will also discuss how you can use Moonlight in a non Mono context.

What is Moonlight
-----------------

Moonlight is an open source implementation of Microsoft's Silverlight Web development technology. At the time of the writing of this paper, Moonlight implements both versions of Silverlight. 

Version 1.0 consists of a presentation framework responsible for UI, graphics, animation, and media playback. A Moonlight application is started when the Moonlight browser plugin is invoked within an HTML page. The plugin loads a XAML file which contains a Canvas object. This Canvas object is the root element for all other elements used for the UI. These elements include basic graphic primitives and complex elements like images, and media. Moonlight can be manipulated by browser scripting languages thru modification of the DOM API it exposes. 

Version 1.1 improves the Canvas object whereby the XAML file can be augmented with code-behind code.(canvas + ECMA CLI powered execution engine).

Rendering is currently done using Cairo [cairo]_, the 2D vector graphics library.

Developing Non Web Applications with Moonlight
----------------------------------------------

Even though Silverlight was intended to be used within a web browser, the Moonlight team saw a use for the technology in developing Linux desktop widgets.

References
----------

.. [silverlight] Silverlight Home Page
    (http://www.silverlight.net/)

.. [mono] Mono Home Page
    (http://www.mono-project.com/)

.. [moonlight] Moonlight Project Page
    (http://www.mono-project.com/Moonlight)

.. [cairo] Cairo 2D Graphics Library Home Page
     (http://cairographics.org)
