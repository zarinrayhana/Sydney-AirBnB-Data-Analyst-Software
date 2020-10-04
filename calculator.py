# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 22:46:09 2020

@author: Sisilia
"""

try:
    import wx
except ImportError:
    raise ImportError
    
class Calculator(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        panel = wx.Panel(self)
        
        #draw the text fields
        num1Text = wx.StaticText(panel, label='Enter first number here', pos=(10, 10))
        num1 = wx.TextCtrl(panel, wx.ID_ANY, value='', style=wx.TE_CENTRE, pos=(10, 30))
        num1.Bind(wx.EVT_TEXT, self.checkVal, num1)

        num2Text = wx.StaticText(panel, label='Enter second number here')
        num2 = wx.TextCtrl(panel, wx.ID_ANY, value='', style=wx.TE_CENTRE)
        num2.Bind(wx.EVT_TEXT, self.checkVal, num2)

        #result area
        resultTitleText = wx.StaticText(panel, label='Result', pos=(20, 80))
        font = resultTitleText.GetFont()
        font.PointSize += 10
        font = font.Bold()
        resultTitleText.SetFont(font)
        
        self.result = wx.TextCtrl(panel, wx.ID_ANY, value='', style=wx.TE_READONLY, pos=(20, 85))
        
        #draw the buttons
        addbutton = wx.Button(panel, wx.ID_ANY, label='+', pos=(20, 200))
        subsbutton = wx.Button(panel, wx.ID_ANY, label='-', pos=(20, 250))
        multbutton = wx.Button(panel, wx.ID_ANY, label='*', pos=(20, 300))
        divbutton = wx.Button(panel, wx.ID_ANY, label='/', pos=(20, 350))
        clearbutton = wx.Button(panel, wx.ID_ANY, label='Clear', pos=(20, 400))
        
        #main sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        #sizer for buttons
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        
        #add the buttons into the btnSizer
        #proportion value is 1 so the content auto adjust with window size
        btnSizer.Add(addbutton, 1, wx.EXPAND | wx.ALL, border=5)
        btnSizer.Add(subsbutton, 1, wx.EXPAND | wx.ALL, border=5)
        btnSizer.Add(multbutton, 1, wx.EXPAND | wx.ALL, border=5)
        btnSizer.Add(divbutton, 1, wx.EXPAND | wx.ALL, border=5)
        btnSizer.Add(clearbutton, 1, wx.EXPAND | wx.ALL, border=5)
        
        #add the content in the window to the mainSizer in order top-down
        mainSizer.Add(num1Text, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(num1, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(num2Text, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(num2, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(resultTitleText, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.result, 1, wx.EXPAND | wx.ALL, 5)
        
        mainSizer.Add(btnSizer, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizerAndFit(mainSizer)
        
        #bind events to the buttons
        self.value1 = (num1.GetValue())
        self.value2 = (num2.GetValue())
        
        self.Bind(wx.EVT_BUTTON, self.onAdd, addbutton)
        self.Bind(wx.EVT_BUTTON, self.onSubs, subsbutton)
        self.Bind(wx.EVT_BUTTON, self.onMult, multbutton)
        self.Bind(wx.EVT_BUTTON, self.onDiv, divbutton)
        self.Bind(wx.EVT_BUTTON, self.onClear, clearbutton)

        self.Show(True)
        
    def checkVal(self, event):
        # opTypes = ['+', '-', '*', '/']
        # buttonPressed = event.GetEventObject()
        # buttonLabel = buttonPressed.GetLabel()
        
        #check if numbers provided
        if self.value1 and self.value2:
            self.value1 = int(self.value1)
            self.value2 = int(self.value2)
            return True
        
    def onAdd(self, event):
        valsProvided = self.checkVal(event)
        if valsProvided:
            self.result.SetValue(str(float(self.value1) + float(self.value2)))
            # self.value1.SetValue('')
            # self.value2.SetValue('')
    
    def onSubs(self, event):
        valsProvided = self.checkVal(event)
        if valsProvided:
            self.result.SetValue(str(float(self.value1) - float(self.value2)))
            # self.value1.SetValue('')
            # self.value2.SetValue('')

    def onMult(self, event):
        valsProvided = self.checkVal(event)
        if valsProvided:
            self.result.SetValue(str(float(self.value1) * float(self.value2)))
            # self.value1.SetValue('')
            # self.value2.SetValue('')

    def onDiv(self, event):
        valsProvided = self.checkVal(event)
        if valsProvided:
            self.result.SetValue(str(float(self.value1) / float(self.value2)))
            # self.value1.SetValue('')
            # self.value2.SetValue('')

    def onClear(self, event):
        self.num1 = ''
        self.num2 = ''
        
        
#Runs the program
if __name__ == '__main__':
    app = wx.App()
    frame = Calculator(None, wx.ID_ANY, title='Calculator')
    app.MainLoop()