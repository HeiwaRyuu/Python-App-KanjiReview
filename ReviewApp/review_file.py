# Code by : Vítor Carvalho Marx Lima
# Start Date : 18/08/2020 - Finish Date : Still in Progress



# Importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import psycopg2
import random



# Configurations for the width and height for review window
WIDTHReview = 400
HEIGHTReview = 250





class ReviewWindow:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTHReview}x{HEIGHTReview}")
        self.master.maxsize(WIDTHReview, HEIGHTReview)
        self.master.minsize(WIDTHReview, HEIGHTReview)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習 - Let's review!")
        self.master.config(bg="pink")

        # Canvas ------------------------------------------------------------------------------------------------------------

        # Adding the keyword title canvas
        self.KeywordTitleCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.KeywordTitleCanvas.config(height = 50)
        self.KeywordTitleCanvas.pack(fill = "both", pady = 5)

        # Adding the keyword canvas
        self.KeywordCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.KeywordCanvas.config(height = 50)
        self.KeywordCanvas.pack(fill = "both")


        # Adding the kanji canvas
        self.KanjiTitleCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.KanjiTitleCanvas.config(height = 50)
        self.KanjiTitleCanvas.pack(fill = "both", pady = 5)
        

        # Adding the kanji canvas
        self.KanjiCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.KanjiCanvas.config(height = 50)
        self.KanjiCanvas.pack(fill = "both", pady = 5)

        # Adding the buttons canvas
        self.ButtonsCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.ButtonsCanvas.config(height = 50)
        self.ButtonsCanvas.pack(pady = 15)



        # Labels ------------------------------------------------------------------------------------------------------------

        # Adding the keyword title label
        self.KeywordTitleLabel = tk.Label(self.KeywordTitleCanvas, text = "Keyword")
        self.KeywordTitleLabel.config(font = ("Courier", 20, "bold"), fg = "#C71150",bg = "pink")
        self.KeywordTitleLabel.pack(pady = 5)

        # Adding the keyword label 
        self.KeywordLabel = tk.Label(self.KeywordCanvas)
        self.KeywordLabel.config(font = ("Courier", 15, "bold"), fg = "#C71150",bg = "pink")
        self.KeywordLabel.pack()

        # Displaying the kanji title
        self.KanjiTitleLabel = tk.Label(self.KanjiTitleCanvas)
        self.KanjiTitleLabel.config(font = ("Courier", 20, "bold"), fg = "#C71150",bg = "pink")
        self.KanjiTitleLabel.pack(fill = "both", pady = 5)

        # Displaying the kanji title
        self.KanjiLabel = tk.Label(self.KanjiCanvas)
        self.KanjiLabel.config(font = ("Courier", 20, "bold"), fg = "#C71150", bg = "pink")
        self.KanjiLabel.pack(fill = "both")


        # Buttons ------------------------------------------------------------------------------------------------------------

        # Adding the button to close window
        self.RewviewKanjiCloseButton = tk.Button(self.ButtonsCanvas, text = "Go back", width = 15, command = self.master.destroy)
        self.RewviewKanjiCloseButton.config(bg = "#F98FB4", fg = "#C71150")
        self.RewviewKanjiCloseButton.pack(side = "left", padx = 4)

        # Adding the button to show the kanji for the respective keyword
        self.ShowKanjiButton = tk.Button(self.ButtonsCanvas, text = "Check Kanji", width = 15)
        self.ShowKanjiButton.config(bg = "#F98FB4", fg = "#C71150")
        self.ShowKanjiButton.pack(side = "left", padx = 4)

        # Adding the button to go to the next keyword
        self.NextKeywordButton = tk.Button(self.ButtonsCanvas, text = "Next Keyword", width = 15, command = self.RandomKeyword)
        self.NextKeywordButton.config(bg = "#F98FB4", fg = "#C71150")
        self.NextKeywordButton.pack(side = "left", padx = 4)



        # The keyword label itslef has to be added after the database connection, otherwise we won't have the right keyword to output
        # The connection is made so we can grab all data from database into lists we can further use the data to print on screen
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

        # Getting all the keywords and kanjis into a list
        # OBS: HERE WE HAVE TO TRANSFER TE STRINGS FROM THE TUPLES INTO A REAL STRING LIST, BECAUSE FETCHALL GIVES TUPLES!
        keyword_list_command = "SELECT keyword FROM review"
        cur.execute(keyword_list_command)
        self.list_of_keywords_tuples = cur.fetchall()
        self.list_of_keywords = []
        for tup in range(len(self.list_of_keywords_tuples)):
            self.list_of_keywords.append(self.list_of_keywords_tuples[tup][0])

        
        kanji_list_command = "SELECT kanji FROM review"
        cur.execute(kanji_list_command)
        self.list_of_kanjis_tuples = cur.fetchall()
        self.list_of_kanjis = []
        for tup in range(len(self.list_of_kanjis_tuples)):
            self.list_of_kanjis.append(self.list_of_kanjis_tuples[tup][0])

        # Closing the connection after we get all executes done
        cur.close()
        conn.close()


        # Checking if the database table is empty, if so, we put out a message showing that it is indeed empty
        if(len(self.list_of_keywords) == 0):

            self.EmptyTable01 = tk.Label(self.KeywordTitleCanvas, text = "There's no kanji to be review...")
            self.EmptyTable01.config(font = ("Courier", 15), fg = "#C71150", bg = "pink")
            self.EmptyTable01.pack(pady = 10)

            self.EmptyTable02 = tk.Label(self.KeywordTitleCanvas, text = "Add some and come back later!")
            self.EmptyTable02.config(font = ("Courier", 15), fg = "#C71150", bg = "pink")
            self.EmptyTable02.pack(pady = 10)
        else:  
            # Generating the random keyword and displaying the kanji if the button for check kanji is pressed
            self.RandomKeyword()
            self.ShowKanjiButton.config(command = self.DisplayKanji)
            




    # Functions ------------------------------------------------------------------------------------------------------------

    def RandomKeyword(self):
        # If the list gets empty, it means te user has reviewd everything
        if len(self.list_of_keywords) == 0:
            self.ReviewDone()
            # Poping last element from list of kanjis
            self.list_of_kanjis.pop(0)

            # Reseting the Kanji title label text
            self.KanjiTitleLabel.config(text = "")
            # Reseting the Kanji label text
            self.KanjiLabel.config(text = "")

            # Reseting the keyword title and keyword labels to show to review has finished
            self.KeywordTitleLabel.config(font = ("Courier", 15, "bold"), text = "Great job!")
            self.KeywordLabel.config(font = ("Courier", 10, "bold"), text = "You have reviewd all the kanji in the list!")
        elif len(self.list_of_keywords) == 1:
            # Generating a random index to generate a random keyword for the review, as the purpose of the app is to review in a random order
            n_keyword = (len(self.list_of_keywords) - 1)
            rand_index = random.randint(0, n_keyword)
            keyword = self.list_of_keywords[rand_index]

            # Reseting the Kanji title label text
            self.KanjiTitleLabel.config(text = "")
            # Reseting the Kanji label text
            self.KanjiLabel.config(text = "")
            # Reseting the keyword label text
            self.KeywordLabel.config(text = keyword)

            self.respective_kanji = self.list_of_kanjis[rand_index]

            # Removing the elements that have already been shown
            self.list_of_keywords.pop(rand_index)
        else:
            # Generating a random index to generate a random keyword for the review, as the purpose of the app is to review in a random order
            n_keyword = (len(self.list_of_keywords) - 1)
            rand_index = random.randint(0, n_keyword)
            keyword = self.list_of_keywords[rand_index]

            # Reseting the Kanji title label text
            self.KanjiTitleLabel.config(text = "")
            # Reseting the Kanji label text
            self.KanjiLabel.config(text = "")
            # Reseting the keyword label text
            self.KeywordLabel.config(text = keyword)

            self.respective_kanji = self.list_of_kanjis[rand_index]

            # Removing the elements that have already been shown
            self.list_of_keywords.pop(rand_index)
            self.list_of_kanjis.pop(rand_index)
        

    def DisplayKanji(self):
        # If the list gets empty, it means te user has reviewd everything
        if len(self.list_of_kanjis) == 0:
            self.ReviewDone()
        else:
            # Reseting the Kanji title label text
            self.KanjiTitleLabel.config(text = "Kanji")
            # Reseting the Kanji label text
            self.KanjiLabel.config(text = self.respective_kanji)

    # Errors and Messages ------------------------------------------------------------------------------------------------------------

    # Warning for review done
    def ReviewDone(self):
        tk.messagebox.showwarning(title = "Review Done!", message = "You have finished the review! No kanji to be shown!")
