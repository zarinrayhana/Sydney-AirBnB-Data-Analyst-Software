try:
    import wx
    import wx.grid
except ImportError:
    raise ImportError
    
class myGui(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        panel= wx.Panel(self)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        grid = wx.grid.Grid(self, -1)
        grid.SetRowLabelSize(0)
        grid.SetColLabelSize(0)
        grid.CreateGrid(4, 4)
        
        #sets the size in pixels
        grid.SetColSize(0, 100)
        # grid.SetRowSize(row, height)
        
        #automatically sizes the rows and columns based on the content
        # grid.AutoSizeColumns(setAsMin=True)
        grid.AutoSizeRows(setAsMin=True)
        
        #rows and columns index start from 0
        # grid.SetCellValue(3, 3, 'green on grey')
        
        #adding values from ext file to the grid
        with open('data.txt') as dataFile:
            rowNum = 0
            colNum = 1
            for line in dataFile:
                lineSplit = line.split()
                
                rowTitle = ''.join(lineSplit[:-3])
                
                grid.SetCellValue(rowNum, 0, rowTitle)
                grid.SetCellValue(rowNum, colNum, lineSplit[-3])
                grid.SetCellValue(rowNum, colNum+1, lineSplit[-2])
                grid.SetCellValue(rowNum, colNum+2, lineSplit[-1])
                rowNum += 1
        
        self.sizer.Add(grid)
        panel.SetSizerAndFit(self.sizer)
        
        
        menu = wx.Menu()
        exit = menu.Append(wx.ID_EXIT)
        menuBar = wx.MenuBar()
        menuBar.Append(menu, 'File')
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onExit, exit)
        
        self.Show(True)
        
        
    def onExit(self, event):
        wx.MessageBox('You\'re leaving?')
        self.Close(True)
                
if __name__ == '__main__':
    app = wx.App()
    frame = myGui(None, wx.ID_ANY, title='My first GUI')
    app.MainLoop()