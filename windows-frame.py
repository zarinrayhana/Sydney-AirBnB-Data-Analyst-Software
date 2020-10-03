from tkinter import Tk, Frame, BOTH

class soft_frame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   

        self.parent = parent        
        self.parent.title('Sydney AirBnB Data Analysis & Visualisation Software')
        self.pack(fill=BOTH, expand=1)

def main():

    root = Tk()
    root.geometry("850x500+500+500")
    root.resizable(width=True, height=True)
    app = soft_frame(root)
    root.mainloop()  

if __name__ == '__main__':
    main()
    
