__doc__ = '''

gdatareader.py - A quick and dirty GDATA reader with Windows Forms GUI

Version created for tutorial 2 of IronPython and GDATA series. This reader
uses a RichTextBox for the entries view.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT

'''
__version__ = "$Revision$"[11:-1]
import sys
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
import System
import System.Drawing
import System.Windows.Forms
from System.Windows.Forms import AnchorStyles
clr.AddReference("Google.GData.Client.dll")
import Google.GData.Client as GDClient

# Normally we can get the text file line separator from os.linesep
# but since I want this tutorial to work without the standard CPython
# libraries we need to do the following:
try:
    import nt as os
    os.linesep = "\r\n"
except:
    import posix as os
    os.linesep = "\n"
    
def parse(uri, nc=None):
    '''
    Create a query and service object
    '''
    try:
        query = GDClient.FeedQuery()
        service = GDClient.Service("cl","hexdump-gdatareader-0.1")
        query.Uri = System.Uri(uri)
        return service.Query(query)
    except Exception, e:
        raise e

def load_feed(feeduri):
    '''
    Attempt to load a GDATA feed passed as argument feeduri.
    Return list of entry objects.
    '''
    if feeduri == "":
        return []
    try:
        feed = parse(feeduri)
        entries = []
        for entry in feed.Entries:
            entries.append(entry)
        return entries
    except Exception, e:
        raise e

class GDataReaderForm(System.Windows.Forms.Form):
    def __init__(self, feeduri=None):
        self._initgui()
        self.feeduri = feeduri
        if self.feeduri is not None:
            self.gdataUriTextBox.Text = self.feeduri
            self.GdataLoadFeed(None, None)

    def _initgui(self):
        '''
        Create GUI.
        '''
        self.toolBar = System.Windows.Forms.ToolBar()
        self.gdataRefreshButton = System.Windows.Forms.Button()
        self.gdataUriTextBox = System.Windows.Forms.TextBox()
        self.gdataEntriesRichTextBox = System.Windows.Forms.RichTextBox()
        self.statusBar = System.Windows.Forms.StatusBar()
        self.statusBarPanelMsg = System.Windows.Forms.StatusBarPanel()
        self.label1 = System.Windows.Forms.Label()
        System.ComponentModel.ISupportInitialize.BeginInit(self.statusBarPanelMsg)
        self.SuspendLayout()
        # toolBar
        self.toolBar.DropDownArrows = True
        self.toolBar.Location = System.Drawing.Point(0, 0)
        self.toolBar.Name = "toolBar"
        self.toolBar.ShowToolTips = True
        self.toolBar.Size = System.Drawing.Size(744, 42)
        self.toolBar.TabIndex = 0
        # gdataRefreshButton
        self.gdataRefreshButton.Location = System.Drawing.Point(672, 16)
        self.gdataRefreshButton.Name = "gdataRefreshButton"
        self.gdataRefreshButton.Size = System.Drawing.Size(56, 24)
        self.gdataRefreshButton.Anchor = (AnchorStyles.Top | AnchorStyles.Right)
        self.gdataRefreshButton.TabIndex = 1
        self.gdataRefreshButton.Text = "Refresh"
        self.gdataRefreshButton.Click += self.GdataLoadFeed
        # gdataUriTextBox
        self.gdataUriTextBox.Location = System.Drawing.Point(56, 18)
        self.gdataUriTextBox.Name = "gdataUriTextBox"
        self.gdataUriTextBox.Size = System.Drawing.Size(608, 20)
        self.gdataUriTextBox.Anchor = (AnchorStyles.Left | AnchorStyles.Right |
                                AnchorStyles.Bottom | AnchorStyles.Top)
        self.gdataUriTextBox.TabIndex = 2
        self.gdataUriTextBox.Text = ""
        self.gdataUriTextBox.AcceptsReturn = False
        self.gdataUriTextBox.Leave += self.GdataLoadFeed
        # gdataEntriesRichTextBox
        self.gdataEntriesRichTextBox.Location = System.Drawing.Point(8, 56)
        self.gdataEntriesRichTextBox.Multiline = True
        self.gdataEntriesRichTextBox.Name = "gdataEntriesRichTextBox"
        self.gdataEntriesRichTextBox.ReadOnly = True
        self.gdataEntriesRichTextBox.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.Both
        self.gdataEntriesRichTextBox.Size = System.Drawing.Size(728, 232)
        self.gdataEntriesRichTextBox.Anchor = (AnchorStyles.Left | AnchorStyles.Right |
                                AnchorStyles.Bottom | AnchorStyles.Top)
        self.gdataEntriesRichTextBox.TabIndex = 3
        self.gdataEntriesRichTextBox.TabStop = False
        self.gdataEntriesRichTextBox.Text = ""
        self.gdataEntriesRichTextBox.LinkClicked += self.LinkClicked
        # statusBar
        self.statusBar.Location = System.Drawing.Point(0, 303)
        self.statusBar.Name = "statusBar"
        self.statusBarPanelMsg = System.Windows.Forms.StatusBarPanel()
        self.statusBar.Panels.Add(self.statusBarPanelMsg)
	self.statusBarPanelMsg.AutoSize = System.Windows.Forms.StatusBarPanelAutoSize.Spring
        self.statusBar.Size = System.Drawing.Size(744, 22)
        self.statusBar.ShowPanels = True
        # label1
        self.label1.Location = System.Drawing.Point(8, 16)
        self.label1.Name = "label1"
        self.label1.Size = System.Drawing.Size(48, 24)
        self.label1.Text = "Address"
        self.label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        # gdataReaderForm
        self.AutoScaleBaseSize = System.Drawing.Size(5, 13)
        self.ClientSize = System.Drawing.Size(744, 325)
        self.Controls.Add(self.label1)
        self.Controls.Add(self.statusBar)
        self.Controls.Add(self.gdataEntriesRichTextBox)
        self.Controls.Add(self.gdataUriTextBox)
        self.Controls.Add(self.gdataRefreshButton)
        self.Controls.Add(self.toolBar)
	self.AcceptButton = self.gdataRefreshButton
        self.Name = "gdataReaderForm"
        self.Text = "GDATA Reader"
        System.ComponentModel.ISupportInitialize.EndInit(self.statusBarPanelMsg)
        self.ResumeLayout(False)

    def GdataLoadFeed(self, sender, args):
        '''
        Load the GDATA feed using uri in gdataUriTextBox, and display RTF
        rendering in gdataEntriesRichTextBox.
        '''
	self.statusBarPanelMsg.Text = "Get %s" % self.gdataUriTextBox.Text
        try:
            entries = []
            entries = load_feed(self.gdataUriTextBox.Text)
            self.gdataEntriesRichTextBox.Rtf = self.FormatAsRtf(entries)
        except Exception, e:
            self.DisplayError(e)
	self.statusBarPanelMsg.Text = "Done"

    def DisplayError(self, e):
        '''
        Display exception e string representation in gdataEntriesRichTextBox.
        '''
        self.gdataEntriesRichTextBox.Text = "Unable to display feed due to following error:%s%s" % (os.linesep, str(e))

    def LinkClicked(self, sender, args):
	'''
	Get OS to launch the link using associated application
	'''
        System.Diagnostics.Process.Start(args.LinkText)

    def FormatAsRtf(self, entries):
        '''
        Return entry formatted as RTF.
        '''
        rtf = []
        rtf.append(r"{\rtf1\ansi\ansicpg1252\deff0\deflang1033{\fonttbl{\f0\fswiss\fcharset0 Arial;}}")
        rtf.append(r"\viewkind4\uc1\pard")
        for entry in entries:
            rtf.append(r"\b\f0\fs20 %s\b0\par%s" % (entry.Title.Text,"\r"))
            if entry.Summary.Text is not None:
                rtf.append(r"%s\par%s" % (entry.Summary.Text,"\r"))
            alternate_link = self.GetRelatedUri(entry)
            if alternate_link is not None:
                rtf.append(r"%s\par" % alternate_link)
            rtf.append(r"\par") 
        rtf.append("}")
        return "".join(rtf)

    def GetRelatedUri(self, entry, reltype="alternate"):
        '''
        Get the related uri of reltype from the GDATA entry Links collection.
        Returns Uri or None if ne not found.
        '''
        uri = None
        for link in entry.Links:
            if hasattr(link, "Rel"):
                if link.Rel == reltype:
                    uri = link.HRef.Content
            else:
                if reltype == "alternate":
                    # No Rel attribute means it's alternate
                    uri = link.HRef.Content
            return uri
            
def main(argv=sys.argv):
    System.Windows.Forms.Application.EnableVisualStyles()
    if len(argv) == 2:
        feeduri = argv[1]
    else:
        feeduri=None
    form = GDataReaderForm(feeduri)
    System.Windows.Forms.Application.Run(form)

if __name__ == "__main__":
    sys.exit(main())

