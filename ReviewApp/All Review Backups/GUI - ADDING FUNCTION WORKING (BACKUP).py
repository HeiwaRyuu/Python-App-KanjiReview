import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import psycopg2

WIDTH = 550
HEIGHT = 350

WIDTHAdd = 350
HEIGHTAdd = 200

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
        self.TitleCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TitleCanvas.pack(expand = True)

        # Adding the canvas for the Image
        self.ImageCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.ImageCanvas.pack(expand = True)

        # Adding the canvas for the Buttons
        self.ButtonsCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
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

        





        # Buttons ------------------------------------------------------------------------------------------------------------

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




    # Functions ------------------------------------------------------------------------------------------------------------

    # Creating the function that pops new windows
    def OpenNewWindow(self, windowClass):
        self.NewWindow = tk.Toplevel(self.master)
        windowClass(self.NewWindow)






































class WindowOne:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTHAdd}x{HEIGHTAdd}")
        self.master.maxsize(WIDTHAdd, HEIGHTAdd)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習 - Adding new Kanji!")
        self.master.config(bg="pink")





        # Canvas ------------------------------------------------------------------------------------------------------------

        # Adding the canvas for Keyword
        self.KeywordCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.KeywordCanvas.pack(expand = True)

        # Adding the canvas for Kanji
        self.KanjiCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.KanjiCanvas.pack(expand = True)

        # Adding the canvas for Buttons
        self.ButtonsCanvas = tk.Canvas(self.master, height = 20, bg = "pink", highlightthickness=0)
        self.ButtonsCanvas.pack(expand = True, fill = "y")        





        # Labels ------------------------------------------------------------------------------------------------------------

        # Adding the Label for Keyword
        self.KeywordLabel = tk.Label(self.KeywordCanvas, text = "Type here your Keyword:", bg = "pink", width = 25)
        self.KeywordLabel.pack(side = "left")

        # Adding the Label for Kanji
        self.KanjiLabel = tk.Label(self.KanjiCanvas, text = "Enter here the respective kanji:", bg = "pink", width = 25)
        self.KanjiLabel.pack(side = "left")




        # Entries ------------------------------------------------------------------------------------------------------------

        # Defining textvariables dor entry
        self.Keywordcontent = tk.StringVar()
        self.Kanjicontent = tk.StringVar()

        # Adding the Entry for Keyword
        self.KeywordEntry = tk.Entry(self.KeywordCanvas, width = 25, fg = "#C71150", textvariable = self.Keywordcontent)
        self.KeywordEntry.pack(side = "left")

        # Adding the Entry for Kanji
        self.KanjiEntry = tk.Entry(self.KanjiCanvas, width = 25, fg = "#C71150", textvariable = self.Kanjicontent)
        self.KanjiEntry.pack(side = "left")




        # Buttons ------------------------------------------------------------------------------------------------------------

        # Adding button to close window
        self.AddKanjiCloseButton = tk.Button(self.ButtonsCanvas, text = "Go back", width = 20, command = self.master.destroy)
        self.AddKanjiCloseButton.pack(side = "left", padx = 4)

        # Adding the button that effectivelly adds the Kanji
        self.AddButton = tk.Button(self.ButtonsCanvas, text = "Add kanji", width = 20, command = self.addKanji)
        self.AddButton.pack(side = "left", padx = 4)

    



    # Functions ------------------------------------------------------------------------------------------------------------

    # Defining the function that adds the new kanji and keyword to the list
    def addKanji(self):

        # Adressing any mistake befor connecting to the database and making changes
        if len(self.Keywordcontent.get()) == 0:
            self.empty_keyword()
        elif len(self.Kanjicontent.get()) == 0:
            self.empty_kanji()
        else:
        
            # Connecting to the database
            conn = psycopg2.connect(
                host = "localhost",
                database = "review",
                user = "postgres",
                password = "35c4p3fromh3ll",
                port = "5432"
            )   
            
            # Creating the cursor
            cur = conn.cursor()

            # Creating the table if it does not exist
            create_table = "CREATE TABLE IF NOT EXISTS review (id SERIAL PRIMARY KEY, keyword VARCHAR(50) NOT NULL, kanji VARCHAR(30) NOT NULL)"
            cur.execute(create_table)
            # Commiting the table creation
            conn.commit()
            

            # Getting the content from the keyword and kanji Entry input
            keyword_ = self.Keywordcontent.get().upper()
            kanji_ = self.Kanjicontent.get()

            # Creating the error exceptions after the database connection

            # Checking if the keyword or kanji is already in the database
            check_if_keyword_data_exists = "SELECT * FROM review WHERE keyword = '{}'"
            check_if_kanji_data_exists = "SELECT * FROM review WHERE kanji = '{}'"

            cur.execute(check_if_keyword_data_exists.format(keyword_))
            keyword_checker = cur.fetchall()
            cur.execute(check_if_kanji_data_exists.format(kanji_))
            kanji_checker = cur.fetchall()

            if len(keyword_checker) != 0:
                self.existing_keyword()
                cur.close()
                conn.close()
            elif len(kanji_checker) != 0:
                self.existing_kanji()
                cur.close()
                conn.close()
            else:

            
                # Adding the keyword and kanji to the table
                
                inserting_data = "INSERT INTO review (keyword, kanji) VALUES (%s, %s)"
                cur.execute(inserting_data,(keyword_,kanji_))
                print("The kanji and keyword has been added succesfully")
                # Commiting the insertion
                conn.commit()

                cur.close()
                conn.close()




# Errors and Messages ------------------------------------------------------------------------------------------------------------

    # Warning for empty keyword entry
    def empty_keyword(self):
        tk.messagebox.showwarning(title = "Empty Keyword Entry", message = "Please enter a keyword")


    # Warning for empty kanji entry
    def empty_kanji(self):
        tk.messagebox.showwarning(title = "Empty Kanji Entry", message = "Please enter a kanji")
    

    # Warning for already existant keyword in database
    def existing_keyword(self):
        tk.messagebox.showwarning(title = "Existing Keyword", message = "This keyword is already in the database!")

    
    # Warning for empty kanji entry
    def existing_kanji(self):
        tk.messagebox.showwarning(title = "Existing Kanji", message = "This kanji is already in the database!")



        

# Running app ------------------------------------------------------------------------------------------------------------

root = tk.Tk()
app = MainWindow(root)
root.mainloop()