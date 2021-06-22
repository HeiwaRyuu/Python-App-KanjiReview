import tkinter as tk
from PIL import ImageTk, Image

WIDTH = 550
HEIGHT = 350

class MainWindow:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.maxsize(WIDTH, HEIGHT)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習")
        self.master.config(bg="pink")





        # Adding the canvas for the Title
        self.TitleCanvas = tk.Canvas(self.master)
        self.TitleCanvas.pack(expand = True)

        # Adding the canvas for the Image
        self.ImageCanvas = tk.Canvas(self.master)
        self.ImageCanvas.pack(expand = True)

        # Adding the canvas for the Buttons
        self.ButtonsCanvas = tk.Canvas(self.master)
        self.ButtonsCanvas.config(bg = "pink")
        self.ButtonsCanvas.pack(expand = True, fill = "both")






        # Adding the Title
        self.TitleLabel = tk.Label(self.TitleCanvas, text = "Welcome to 漢字復習!")
        self.TitleLabel.config(font = ("Courier", 20, "bold"), bg = "pink")
        self.TitleLabel.pack()


        # Adding the image to the master
        image = Image.open("Images/umaru.jpg").resize((300,200), Image.ANTIALIAS)
        UmaruPath = ImageTk.PhotoImage(image)
        self.Umarulabel = tk.Label(self.ImageCanvas, image = UmaruPath)
        self.Umarulabel.image = UmaruPath
        self.Umarulabel.pack()

        
        # Creating the Button that opens the Kanji List
        self.KanjiListPopButton = tk.Button(self.ButtonsCanvas, text = "Show Kanji List", command = lambda: self.OpenNewWindow(WindowOne))
        self.KanjiListPopButton.config(height = 2, width = 16 , bg = "#F98FB4")
        self.KanjiListPopButton.pack(side = "right", padx = 5)


        # Creating the Button that opens the Add to kanji List window
        self.AddKanjiButton = tk.Button(self.ButtonsCanvas, text = "Add Kanji", command = lambda: self.OpenNewWindow(WindowOne))
        self.AddKanjiButton.config(height = 2, width = 16, bg = "#F98FB4")
        self.AddKanjiButton.pack(side = "right", padx = 5)


        # Creating the Button that opens the Remove from kanji list window
        self.RemoveKanjiButton = tk.Button(self.ButtonsCanvas, text = "Remove Kanji", command = lambda: self.OpenNewWindow(WindowOne))
        self.RemoveKanjiButton.config(height = 2, width = 16, bg = "#F98FB4")
        self.RemoveKanjiButton.pack(side = "right", padx = 5)


        # Creating the Button that opens the Review window
        self.ReviewButton = tk.Button(self.ButtonsCanvas, text = "Start Review", command = lambda: self.OpenNewWindow(WindowOne))
        self.ReviewButton.config(height = 2, width = 16, bg = "#F98FB4")
        self.ReviewButton.pack(side = "right", padx = 5)


    # Creating the function that pops new windows
    def OpenNewWindow(self, windowClass):
        self.NewWindow = tk.Toplevel(self.master)
        windowClass(self.NewWindow)










class WindowOne:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.maxsize(WIDTH, HEIGHT)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習")
        self.master.config(bg="pink")

        
        # Creating the Button that opens Window One
        self.windowOneCloseButton = tk.Button(self.master, text = "Close This Window", command = self.master.destroy)
        self.windowOneCloseButton.pack()

        


root = tk.Tk()
app = MainWindow(root)
root.mainloop()