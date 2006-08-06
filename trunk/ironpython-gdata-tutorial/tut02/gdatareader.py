__doc__ = '''

gdatareader.py - A quick and dirty GDATA reader with Windows Forms GUI

Version created for tutorial 2 of IronPython and GDATA series.

(C) 2006 Mark Rees http://hex-dump.blogspot.com

License: MIT

'''
import sys
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
import System
import System.Drawing
import System.Windows.Forms
from System.Windows.Forms import AnchorStyles
clr.AddReference("gdata.dll")
import Google.GData.Client as GDClient

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
    Return list of entries.
    '''
    if feeduri == "":
        return []
    try:
        feed = parse(feeduri)
        entries = []
        for entry in feed.Entries:
            entries.append("%s\n%s\n" % (entry.Title.Text, entry.Summary.Text))
        return entries
    except Exception, e:
        raise e

class GDataReaderForm(System.Windows.Forms.Form):
    def __init__(self, feeduri=None):
        self._initgui()
        self.feeduri = feeduri
        if self.feeduri is not None:
            self.gdataUriTextBox.Text = self.feeduri
            self.gdataLoadFeed(None, None)

    def _initgui(self):
        '''
        Create GUI.
        '''
        self.toolBar = System.Windows.Forms.ToolBar()
        self.gdataRefreshButton = System.Windows.Forms.Button()
        self.gdataUriTextBox = System.Windows.Forms.TextBox()
        self.gdataEntriesTextBox = System.Windows.Forms.TextBox()
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
        self.gdataRefreshButton.Click += self.gdataLoadFeed
        # gdataUriTextBox
        self.gdataUriTextBox.Location = System.Drawing.Point(56, 18)
        self.gdataUriTextBox.Name = "gdataUriTextBox"
        self.gdataUriTextBox.Size = System.Drawing.Size(608, 20)
        self.gdataUriTextBox.Anchor = (AnchorStyles.Left | AnchorStyles.Right |
                                AnchorStyles.Bottom | AnchorStyles.Top)
        self.gdataUriTextBox.TabIndex = 2
        self.gdataUriTextBox.Text = ""
        self.gdataUriTextBox.Leave += self.gdataLoadFeed
        # gdataEntriesTextBox
        self.gdataEntriesTextBox.Location = System.Drawing.Point(8, 56)
        self.gdataEntriesTextBox.Multiline = True
        self.gdataEntriesTextBox.Name = "gdataEntriesTextBox"
        self.gdataEntriesTextBox.ReadOnly = True
        self.gdataEntriesTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Both
        self.gdataEntriesTextBox.Size = System.Drawing.Size(728, 232)
        self.gdataEntriesTextBox.Anchor = (AnchorStyles.Left | AnchorStyles.Right |
                                AnchorStyles.Bottom | AnchorStyles.Top)
        self.gdataEntriesTextBox.TabIndex = 3
        self.gdataEntriesTextBox.Text = ""
        # statusBar
        self.statusBar.Location = System.Drawing.Point(0, 303)
        self.statusBar.Name = "statusBar"
        #self.statusBar.Panels.AddRange(System.Windows.Forms.StatusBarPanel[] { self.statusBarPanelMsg})
        self.statusBar.Size = System.Drawing.Size(744, 22)
        self.statusBar.TabIndex = 4
        # label1
        self.label1.Location = System.Drawing.Point(8, 16)
        self.label1.Name = "label1"
        self.label1.Size = System.Drawing.Size(48, 24)
        self.label1.TabIndex = 5
        self.label1.Text = "Address"
        self.label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        # gdataReaderForm
        self.AutoScaleBaseSize = System.Drawing.Size(5, 13)
        self.ClientSize = System.Drawing.Size(744, 325)
        self.Controls.Add(self.label1)
        self.Controls.Add(self.statusBar)
        self.Controls.Add(self.gdataEntriesTextBox)
        self.Controls.Add(self.gdataUriTextBox)
        self.Controls.Add(self.gdataRefreshButton)
        self.Controls.Add(self.toolBar)
        self.Name = "gdataReaderForm"
        self.Text = "GDATA Reader"
        System.ComponentModel.ISupportInitialize.EndInit(self.statusBarPanelMsg)
        self.ResumeLayout(False)

    def gdataLoadFeed(self, sender, args):
        try:
            entries = load_feed(self.gdataUriTextBox.Text)
            self.gdataEntriesTextBox.Text = "\n".join(entries)
        except Exception, e:
            self.displayError(e)

    def displayError(self, e):
        self.gdataEntriesTextBox.Text = "Unable to display feed due to following error:\n%s" % str(e)

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

