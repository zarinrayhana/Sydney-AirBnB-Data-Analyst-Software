import wx
import wx.grid
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

# IMPORT THE MODULES USED FOR THE FUNCTIONS AND CSV FILES
from visualization import getListings, findKeyword, showListings, showPopularListings, showPriceDist, showCleanComments


class plotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(600, 600))
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

    def priceDistribution(self, startDate, endDate):
        startDateSplitted = startDate.split('/')
        endDateSplitted = endDate.split('/')
        startYear = int(startDateSplitted[-1])
        endYear = int(endDateSplitted[-1])

        pricesList = showPriceDist(startDate, endDate)

        for priceList in pricesList:
            self.axes.hist(priceList, range=(0, 3000), bins=150, alpha=0.5, density=True)

        plt.title('Price distribution between {0} and {1}'.format(startYear, endYear))
        plt.legend([year for year in range(startYear, endYear)])
        plt.show()


class gui(wx.Frame) :
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Sydney AirBnB Analysis and Visualisation Tool', size=(1200, 650))
        self.panel = wx.Panel(self)
        
        getname = wx.TextEntryDialog(None,"What's your name", "Title", 'Enter Name')
        if getname.ShowModal()==wx.ID_OK:
            gottenname = getname.GetValue()
        username = wx.StaticText(self.panel, -1, label=gottenname, pos=(450, 10), style=wx.ALIGN_CENTER)

        # DICTIONARY TO KEEP USER INPUTS
        self.userInput = {}        

        # INPUT BOXES
        suburbInfoText = wx.StaticText(self.panel, -1, label='Enter a suburb name - e.g. Sydney, Potts Points, etc.', pos=(10, 50), style=wx.ALIGN_CENTER)
        self.enter_suburb =  wx.TextCtrl(self.panel, -1, pos=(10, 80), size=(180, 30))
        self.Bind(wx.EVT_TEXT, self.suburbOnChange, self.enter_suburb)

        keywordInfoText = wx.StaticText(self.panel, -1, label='Enter a keyword - e.g. pool, internet, tv, etc.', pos=(10, 150), style=wx.ALIGN_CENTER)
        self.enter_keyword = wx.TextCtrl(self.panel, -1, pos=(10, 180), size=(180, 30))
        self.Bind(wx.EVT_TEXT, self.keywordOnChange, self.enter_keyword)

        startDateInfoText = wx.StaticText(self.panel, -1, label='Enter a start date to search in - e.g. 1/1/2009', pos=(550, 50), style=wx.ALIGN_CENTER)
        self.startperiod = wx.TextCtrl(self.panel, -1, pos=(550, 80), size=(180, 30))
        self.Bind(wx.EVT_TEXT, self.startPeriodOnChange, self.startperiod)

        endDateInfoText = wx.StaticText(self.panel, -1, label='Enter an end date to search in - e.g. 1/12/2009', pos=(850, 50), style=wx.ALIGN_CENTER)
        self.endperiod = wx.TextCtrl(self.panel, -1, pos=(850, 80), size=(180, 30))
        self.Bind(wx.EVT_TEXT, self.endPeriodOnChange, self.endperiod)

        #BUTTONS
        searchButton = wx.Button(self.panel,-1, "Search", (300, 430), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.search, searchButton)

        searchAgainButton = wx.Button(self.panel, -1, "Search Again", (300, 460), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.searchAgain, searchAgainButton)

        showPriceButton = wx.Button(self.panel, -1, "Show Price Distribution", (300, 490), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.showPriceDist, showPriceButton)

        popularPropertiesButton = wx.Button(self.panel, -1, "Show Popular Properties", (300, 520), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.showPopularListings, popularPropertiesButton)

        cleanlinessButton = wx.Button(self.panel, -1, "Analyze Comments About Cleanliness", (300, 550), (500, -1))
        self.Bind(wx.EVT_BUTTON, self.cleanlinessComments, cleanlinessButton)

        # AREA DISPLAYING THE SEARCH RESULT
        self.resultDisplay = wx.Panel(self.panel, -1, size=(500, 425), pos=(300, 200), style=wx.SIMPLE_BORDER)


    # METHODS
    def suburbOnChange(self,event):
        suburbName = self.enter_suburb.GetValue()
        self.userInput['suburbName'] = suburbName

    def keywordOnChange(self, event):
        keyword = self.enter_keyword.GetValue()
        self.userInput['keywords'] = keyword

    def startPeriodOnChange(self, event):
        startDate = self.startperiod.GetValue()
        self.userInput['startDate'] = startDate

    def endPeriodOnChange(self, event):
        endDate = self.startperiod.GetValue()
        self.userInput['endDate'] = endDate

    def search(self, event):
        getListings(self.userInput['startDate'], self.userInput['endDate'], self.userInput['suburbName'], self.userInput['keywords'])

        # DISPLAY THE GRID TABLE OF LISTINGS
        with open('listings.json') as jsonListings:
            listings = json.load(jsonListings)

        df = pd.read_json(listings, orient='index')

        dfToDisplay = df[['id', 'name', 'host_name', 'street', 'amenities', 'price', 'review_scores_rating']]

        self.result = wx.StaticText(self.resultDisplay, -1, label=str(dfToDisplay), pos=(300, 200), style=wx.ALIGN_CENTER)
        resultSizer = wx.BoxSizer(wx.VERTICAL)
        resultSizer.Add(self.result)
        self.resultDisplay.SetSizerAndFit(resultSizer)

    def searchAgain(self, event):
        self.userInput.clear()
        self.enter_suburb.Clear()
        self.enter_keyword.Clear()
        self.startperiod.Clear()
        self.endperiod.Clear()

    def showPriceDist(self, event):
        self.myMatplotlib = plotPanel(self)
        self.myMatplotlib.priceDistribution(self.userInput['startDate'], self.userInput['endDate'])
        # INITIALIZE THE MATPLOTLIB CLASS
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.myMatplotlib, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)



    def showPopularListings(self, event):
        pass

    def cleanlinessComments(self, event):
        pass




if __name__ == '__main__':
     app = wx.App()
     frame = gui(parent=None, id=1)
     frame.Show()
     app.MainLoop()
