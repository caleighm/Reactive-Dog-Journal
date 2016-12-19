# 3 December 2016 - UBC Hack Day
# ReactiveDogJournal.py

''' WISHLIST:
* datetime automatically input - Aislin knows - look into it
* re-sort dogentries every time user saves
* upload dog photo
* load/edit files
* undo/redo
* how to factor into different files for diff classes?
* commit to git?!??
'''

try :
    import wx
    import datetime
except ImportError:
    raise ImportError("The wxPython and datetime modules are required to run this program.")

ID_FILEMENU_NEW = wx.NewId()
ID_EDITMENU_CHANGE = wx.NewId()
ID_FILEMENU_SAVE = wx.NewId()
ID_REPORTMENU_REPORT = wx.NewId()

###########################################################
class Home(wx.Frame) :
    def __init__(self, parent, title) :
        super(Home, self).__init__(parent, title=title, size=(390, 350))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self) :
        # MENU
        menubar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        fileMenu.Append(ID_FILEMENU_NEW, '&Add a new entry')
        smi = wx.MenuItem(fileMenu, ID_FILEMENU_SAVE, '&Save current entry')
        self.Bind(wx.EVT_MENU, self.OnSave, smi)
        fileMenu.AppendItem(smi)
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        fileMenu.AppendItem(qmi)

        editMenu = wx.Menu()
        emi = wx.MenuItem(editMenu, ID_EDITMENU_CHANGE, '&Edit a previous entry')
        self.Bind(wx.EVT_MENU, self.OnEdit, emi)
        editMenu.AppendItem(emi)
        
        reportMenu = wx.Menu()
        reportMenu.Append(ID_REPORTMENU_REPORT, '&Generate report')
        
        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(reportMenu, '&Report')
        
        self.SetMenuBar(menubar)

        # TOOLBAR - doesn't currently work... missing image?
        '''toolbar = self.CreateToolBar()
        qtool = toolbar.AddLabelTool(wx.ID_ANY, 'Quit', wx.Bitmap('texit.png'))
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)'''

        # LAYOUT
        panel = wx.Panel(self)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(8, 2, 9, 25)
        
        # static text labels
        welcome = wx.StaticText(panel, label="Welcome to your Reactive Dog Journal.")
        date = wx.StaticText(panel, label="Date (YYYYMMDD): ")
        dogReactions = wx.StaticText(panel, label="Number of reactions to dogs:")
        pplReactions = wx.StaticText(panel, label="Number of reactions to people:")
        otherReactions = wx.StaticText(panel, label="Number of other reactions:")
        notes = wx.StaticText(panel, label="Notes:")

        # text entry fields
        self.tc0 = wx.TextCtrl(panel)
        self.tc1 = wx.TextCtrl(panel)
        self.tc2 = wx.TextCtrl(panel)
        self.tc3 = wx.TextCtrl(panel)
        self.tc4 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        # buttons (save/report/close)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Save', size=(70, 30))
        btn2 = wx.Button(panel, label='Report', size=(70, 30))
        btn3 = wx.Button(panel, label='Close', size=(70, 30))
        
        btn1.Bind(wx.EVT_BUTTON, self.OnSave)
        btn1.Bind(wx.EVT_TEXT_ENTER, self.OnSave)
        btn2.Bind(wx.EVT_BUTTON, self.OnReport)
        btn2.Bind(wx.EVT_TEXT_ENTER, self.OnReport)
        btn3.Bind(wx.EVT_BUTTON, self.OnQuit)
        btn3.Bind(wx.EVT_TEXT_ENTER, self.OnQuit)
        
        hbox2.Add(btn1, flag=wx.ALIGN_RIGHT)
        hbox2.Add(btn2, flag=wx.ALIGN_RIGHT)
        hbox2.Add(btn3, flag=wx.ALIGN_RIGHT)

        # add all to flex grid
        fgs.AddMany([(welcome), (wx.StaticText(panel, label='')), (date), (self.tc0, 1, wx.EXPAND), (dogReactions), 
            (self.tc1, 1, wx.EXPAND), (pplReactions), (self.tc2, 1, wx.EXPAND),
                (otherReactions), (self.tc3, 1, wx.EXPAND), (notes, 1, wx.EXPAND),
                     (self.tc4, 1, wx.EXPAND), (wx.StaticText(panel, label='')), (hbox2)])
        fgs.AddGrowableRow(5, 1)
        fgs.AddGrowableCol(1, 1)

        hbox1.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox1)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        
        self.SetSize((500, 500))
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e) :
        dial = wx.MessageDialog(None, 'Are you sure you want to quit?', 'Just checking!',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            
        ret = dial.ShowModal()
        
        if ret == wx.ID_YES :
            self.Destroy()
        else:
            e.Veto()

    # check input validity after clicking 'save'
    def OnSave(self, e) :
        try :           
            date = int(self.tc0.GetValue())
            dogNum = int(self.tc1.GetValue())
            pplNum = int(self.tc2.GetValue())
            otherNum = int(self.tc3.GetValue())
            notes = self.tc4.GetValue()

            if (len(str(date)) != 8) :
                message = "Please ensure your date is in YYYYMMDD format."
                wx.MessageBox(message, 'Error - Incorrect Input Type', wx.OK | wx.ICON_INFORMATION)
                return
            else :
                date = str(date)
                formattedDate = date[0:4] + '/' + date[4:6] + '/' + date[6:8]

            self.SaveEntry(formattedDate, str(dogNum), str(pplNum), str(otherNum), notes)

        except ValueError :
            message = "Please ensure that you entered only integers in each text field (except for the Notes section)."
            wx.MessageBox(message, 'Error - Incorrect Input Type', wx.OK | wx.ICON_INFORMATION)

    # write new entry to file
    def SaveEntry(self, date, dogNum, pplNum, otherNum, notes) :
        f = open('dogentries', 'a')
        f.write(date + '\t' + dogNum + '\t' + pplNum  + '\t' + otherNum + '\t' + notes + '\n')

        message = "Your entry has been saved."
        wx.MessageBox(message, 'Successful Save', wx.OK | wx.ICON_INFORMATION)

        # clear values in text fields
        self.tc0.SetValue("")
        self.tc1.SetValue("")
        self.tc2.SetValue("")
        self.tc3.SetValue("")
        self.tc4.SetValue("")

    # right click for popup
    def OnRightDown(self, e) :
        self.PopupMenu(PopUp(self), e.GetPosition())

    def OnEdit(self, e) :
        frame = EditFrame()
        frame.Show()

    def OnReport() :
        pass
    
###########################################################
class EditFrame(wx.Frame) :
    def __init__(self) :
        wx.Frame.__init__(self, None, title='Edit previous entries')
        panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox1 = wx.BoxSizer(wx.VERTICAL)

        entryList = []
        f = open('dogentries', "r")
        for line in f :
            line = line[0:10]
            entryList.append(line)
        f.close()

        txt = wx.StaticText(panel, label = "Choose the entry below that you would like to edit.")
        chooseEntry = wx.ComboBox(panel, -1, size=(100,20), choices=entryList)

        vbox1.Add(txt, flag=wx.ALIGN_LEFT, border=91111)
        vbox1.Add(chooseEntry, flag=wx.ALIGN_LEFT, border=9)

        fgs = wx.FlexGridSizer(5, 2, 9, 25)
        
        # static text labels
        date = wx.StaticText(panel, label="Date (YYYYMMDD): ")
        dogReactions = wx.StaticText(panel, label="Number of reactions to dogs:")
        pplReactions = wx.StaticText(panel, label="Number of reactions to people:")
        otherReactions = wx.StaticText(panel, label="Number of other reactions:")
        notes = wx.StaticText(panel, label="Notes:")

        # text entry fields
        self.tc0 = wx.TextCtrl(panel)
        self.tc1 = wx.TextCtrl(panel)
        self.tc2 = wx.TextCtrl(panel)
        self.tc3 = wx.TextCtrl(panel)
        self.tc4 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        # add all to flex grid
        fgs.AddMany([(date), (self.tc0, 1, wx.EXPAND), (dogReactions), 
            (self.tc1, 1, wx.EXPAND), (pplReactions), (self.tc2, 1, wx.EXPAND),
                (otherReactions), (self.tc3, 1, wx.EXPAND), (notes, 1, wx.EXPAND),
                     (self.tc4, 1, wx.EXPAND)])
        fgs.AddGrowableRow(4, 1)
        fgs.AddGrowableCol(1, 1)

        vbox1.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Select', size=(70, 30))
        btn2 = wx.Button(panel, label='Cancel', size=(70, 30))
        
        btn1.Bind(wx.EVT_BUTTON, self.OnSelect)
        btn1.Bind(wx.EVT_TEXT_ENTER, self.OnSelect)
        btn2.Bind(wx.EVT_BUTTON, self.OnClose)
        btn2.Bind(wx.EVT_TEXT_ENTER, self.OnClose)

        hbox1.Add(btn1, flag=wx.ALIGN_CENTRE, border=9)
        hbox1.Add(btn2, flag=wx.ALIGN_CENTRE, border=9)

        vbox1.Add(hbox1)

        panel.SetSizer(vbox1)
        
        self.SetSize((600,400))
        self.Centre()
        self.Show(True)

    def OnSelect(self, e) :
        pass

    def OnClose(self, e) :
        self.Close()

    
###########################################################
class PopUp(wx.Menu) :
    def __init__(self, parent) :
        super(PopUp, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.parent.OnQuit, cmi)

    def OnMinimize(self, e) :
        self.parent.Iconize()

def main() :
    ex = wx.App()
    Home(None, title="Reactive Dog Journal")
    ex.MainLoop()    

if __name__ == '__main__' :
    main()
