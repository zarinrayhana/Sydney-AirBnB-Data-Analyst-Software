import wx

class bucky (wx.Frame) :

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'System Analysis and Visualisation Tool', size=(1200, 1200))
        panel = wx.Panel(self)

        customtitle=wx.StaticText(panel, -1, "System Analysis and Visualisation Tool",(10,20), (260,10), wx.ALIGN_CENTER)
        customtitle.SetForegroundColour('white')
        customtitle.SetSize(1200,20)
        customtitle.SetBackgroundColour('light blue')

        getname = wx.TextEntryDialog(None,"What's you Name", "Title", 'Enter Name')
        if getname.ShowModal()==wx.ID_OK:
            gottenname = getname.GetValue()



        customise = wx.StaticText(panel, -1, gottenname, (10,50), (260,50), wx.ALIGN_CENTER)
        customise.SetSize(1200,20)
        customise.SetForegroundColour('white')
        customise.SetBackgroundColour('light blue')

        wx.CheckBox(panel, -1, "Price Distribution Chart",(10,210), (160,-1))

if __name__ == '__main__':
     app = wx.PySimpleApp()
     frame = bucky(parent=None, id=1)
     frame.Show()
     app.MainLoop()