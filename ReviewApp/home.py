# Code by : Vítor Carvalho Marx Lima
# Start Date : 18/08/2020 - Finish Date : Still in Progress

# Importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import winsound

# Importing the other classes
from add_file import AddKanjiWindow
from remove_file import RemoveKanjiWindow
from table_file import TableOfKanjis
from review_file import ReviewWindow


# Configurations for the width and height for Main Window
WIDTH = 550
HEIGHT = 350

# Connecting to the server to check if the "review" database exists
conn = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "35c4p3fromh3ll",
    port = 5432
)
# Setting isolation level to autocommit
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
create_database = "CREATE DATABASE review"

f = open("check_db_exists.txt", "a+")
f.seek(0)
check_exists = f.read()
f.close()
if check_exists == '':
    # Modifying the file for next compile to not create an existing database
    f = open("check_db_exists.txt", "w")
    f.write("exists")
    f.close()
    #Creating database if it does not exists
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("review")))
else:
    f.close()
    pass

# Closing the connection with server
cur.close()
conn.close()






class MainWindow:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.maxsize(WIDTH, HEIGHT)
        self.master.minsize(WIDTH, HEIGHT)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習")
        self.master.config(bg="pink")





        # Canvas ------------------------------------------------------------------------------------------------------------

        # Adding the canvas for the Title
        self.TitleCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TitleCanvas.pack(expand = True)

        # Adding the canvas for the Image
        self.ImageCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.ImageCanvas.pack(expand = True)

        # Adding the canvas for the Buttons
        self.ButtonsCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.ButtonsCanvas.pack(expand = True, fill = "both")






        # Title and Image ------------------------------------------------------------------------------------------------------------

        # Adding the Title
        self.TitleLabel = tk.Label(self.TitleCanvas, text = "Welcome to 漢字復習!")
        self.TitleLabel.config(font = ("Courier", 20, "bold"), bg = "pink", fg = "#C71150")
        self.TitleLabel.pack()


        # Adding the image to the master
        image = Image.open("Images/umaru.jpg").resize((300,200), Image.ANTIALIAS)
        UmaruPath = ImageTk.PhotoImage(image)
        self.Umarulabel = tk.Label(self.ImageCanvas, image = UmaruPath)
        self.Umarulabel.image = UmaruPath
        self.Umarulabel.pack()





        # Buttons ------------------------------------------------------------------------------------------------------------

        # Creating the Button that opens the Review window
        self.ReviewButton = tk.Button(self.ButtonsCanvas, text = "Start Review", command = lambda: self.OpenNewWindow(ReviewWindow))
        self.ReviewButton.config(height = 2, width = 16, bg = "#F98FB4", fg = "#C71150")
        self.ReviewButton.pack(side = "left", padx = 5)

        # Creating the Button that opens the Kanji List
        self.KanjiListPopButton = tk.Button(self.ButtonsCanvas, text = "Show Kanji List", command = lambda: self.OpenNewWindow(TableOfKanjis))
        self.KanjiListPopButton.config(height = 2, width = 16 , bg = "#F98FB4", fg = "#C71150")
        self.KanjiListPopButton.pack(side = "left", padx = 5)


        # Creating the Button that opens the Add to kanji List window
        self.AddKanjiButton = tk.Button(self.ButtonsCanvas, text = "Add Kanji", command = lambda: self.OpenNewWindow(AddKanjiWindow))
        self.AddKanjiButton.config(height = 2, width = 16, bg = "#F98FB4", fg = "#C71150")
        self.AddKanjiButton.pack(side = "left", padx = 5)


        # Creating the Button that opens the Remove from kanji list window
        self.RemoveKanjiButton = tk.Button(self.ButtonsCanvas, text = "Remove Kanji", command = lambda: self.OpenNewWindow(RemoveKanjiWindow))
        self.RemoveKanjiButton.config(height = 2, width = 16, bg = "#F98FB4", fg = "#C71150")
        self.RemoveKanjiButton.pack(side = "left", padx = 5)





    # Functions ------------------------------------------------------------------------------------------------------------

    # Creating the function that pops new windows
    def OpenNewWindow(self, windowClass):
        self.NewWindow = tk.Toplevel(self.master)
        windowClass(self.NewWindow)



# Running app ------------------------------------------------------------------------------------------------------------

root = tk.Tk()
app = MainWindow(root)
root.mainloop()