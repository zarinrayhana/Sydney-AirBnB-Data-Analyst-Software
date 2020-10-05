
import wx
import wx.grid




class bucky (wx.Frame) :

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'System Analysis and Visualisation Tool', size=(1200, 1200))
        panel = wx.Panel(self)

        getname = wx.TextEntryDialog(None,"What's you Name", "Title", 'Enter Name')
        if getname.ShowModal()==wx.ID_OK:
            gottenname = getname.GetValue()



        customise = wx.StaticText(panel, -1, gottenname, (10,50), (260,50), wx.ALIGN_CENTER)
        customise.SetSize(1200,20)
        customise.SetForegroundColour('white')
        customise.SetBackgroundColour('light blue')

        enter_Suburb =  wx.Button(panel, -1, "Enter Suburb",(10,130), (140,-1))
        self.Bind(wx.EVT_BUTTON, self.entersuburbbutton, enter_Suburb)

        enter_keyword = wx.Button(panel, -1, "Enter Keyword", (10, 190), (140, -1))
        self.Bind(wx.EVT_BUTTON, self.enterkeywordbutton, enter_keyword)

        search_startperiod = wx.Button(panel, -1, "Select Start Period", (550, 130), (140, -1))
        self.Bind(wx.EVT_BUTTON, self.startperiodbutton, search_startperiod)

        search_endperiod = wx.Button(panel, -1, "Select End Period", (850, 130), (140, -1))
        self.Bind(wx.EVT_BUTTON, self.endperiodbutton, search_endperiod)

        search_again = wx.Button(panel,-1, "Search Again", (300, 520), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.endperiodbutton, search_endperiod)

        search_again = wx.Button(panel, -1, "Show Price Distribution", (300, 550), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.endperiodbutton, search_endperiod)

        search_again = wx.Button(panel, -1, "Show Popular Properties", (300, 580), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.endperiodbutton, search_endperiod)


    def entersuburbbutton(self,event):
        enter = wx.TextEntryDialog(None, "Enter Suburb", "Title", "Ashgrove")
        if enter.ShowModal()==wx.ID_OK:
            self.answer =enter.GetValue()

    def enterkeywordbutton(self, event):
        enterkey = wx.TextEntryDialog(None, "Enter Keyword", "Title", "Pool")
        if enterkey.ShowModal() == wx.ID_OK:
            answerkey = enterkey.GetValue()

    def startperiodbutton(self, event):
        search_startperiod = wx.TextEntryDialog(None, "Select First Period", "Title", "1/09/2018")
        if search_startperiod.ShowModal() == wx.ID_OK:
            self.answerstartperiod = search_startperiod.GetValue()

    def endperiodbutton(self, event):
        search_endperiod = wx.TextEntryDialog(None, "Select First Period", "Title", "1/09/2018")
        if search_endperiod.ShowModal() == wx.ID_OK:
            answerendperiod = search_endperiod.GetValue()





if __name__ == '__main__':
     app = wx.PySimpleApp()
     frame = bucky(parent=None, id=1)
     frame.Show()
     app.MainLoop()