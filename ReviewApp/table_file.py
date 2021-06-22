# Code by : Vítor Carvalho Marx Lima
# Start Date : 18/08/2020 - Finish Date : Still in Progress



# Importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import psycopg2



# Configurations for the width and height for Table of Kanji
WIDTHToK = 500
HEIGHTToK = 300





class TableOfKanjis:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTHToK}x{HEIGHTToK}")
        self.master.maxsize(WIDTHToK, HEIGHTToK)
        self.master.minsize(WIDTHToK, HEIGHTToK)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習 - List of saved kanjis!")
        self.master.config(bg="pink")



        # Canvas ------------------------------------------------------------------------------------------------------------

        # Adding the table title canvas
        self.TableTitle = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TableTitle.pack()

        # Adding subtitles canvas
        self.TableSubTitle = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TableSubTitle.pack()

        # Adding the table canvas 
        self.TableCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TableCanvas.pack()





        # Labels ------------------------------------------------------------------------------------------------------------

        # Adding the title label
        self.TitleLabel = tk.Label(self.TableTitle, text = "Keyword and 漢字 table")
        self.TitleLabel.config(font = ("Courier", 20, "bold"), fg = "#C71150",bg = "pink")
        self.TitleLabel.pack(pady = 5)


        # Adding the subtitles labels
        self.KeywordSubTitleLabel = tk.Label(self.TableSubTitle, text = "Keywords")
        self.KeywordSubTitleLabel.config(width = 10, font = ("Courier", 15, "bold"), fg = "#C71150",bg = "pink")
        self.KeywordSubTitleLabel.pack(side = "left", pady = 20, padx = 25)

        self.KanjiSubTitleLabel = tk.Label(self.TableSubTitle, text = "Kanjis")
        self.KanjiSubTitleLabel.config(width = 10, font = ("Courier", 15, "bold"), fg = "#C71150",bg = "pink")
        self.KanjiSubTitleLabel.pack(side = "left", pady = 10, padx = 20)


      

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

            self.EmptyTable01 = tk.Label(self.TableCanvas, text = "There's no kanji to be seen...")
            self.EmptyTable01.config(font = ("Courier", 20), fg = "#C71150", bg = "pink")
            self.EmptyTable01.pack(pady = 10)

            self.EmptyTable02 = tk.Label(self.TableCanvas, text = "Add some and come back later!")
            self.EmptyTable02.config(font = ("Courier", 20), fg = "#C71150", bg = "pink")
            self.EmptyTable02.pack(pady = 10)

        # Else, we just print out the list from database
        else:
            # Adding a scrollbar to view the list when it gets bigger than the listbox height size
            self.TableScrollbar = tk.Scrollbar(self.TableCanvas)
            self.TableScrollbar.pack(side = "right", fill = "y")
            # Binding the scrollbar into the function that makes it scroll both of the listboxes
            self.TableScrollbar.config(command = self.masterScroll)

            # Creating a listbox to display as table for keywords
            self.TableKeywordListBox = tk.Listbox(self.TableCanvas, yscrollcommand = self.TableScrollbar.set)
            self.TableKeywordListBox.config(width=20, height = 10, font = ("Courier", 12), highlightthickness=0, highlightbackground = "#C71150", fg = "#C71150", bg = "pink")
            self.TableKeywordListBox.pack(side = "left", padx = 5)


            # Creating a listbox to display as table for kanjis
            self.TableKanjiListBox = tk.Listbox(self.TableCanvas, yscrollcommand = self.TableScrollbar.set)
            self.TableKanjiListBox.config(width=11, height = 10, font = ("Courier", 12), highlightthickness=0, highlightbackground = "#C71150", fg = "#C71150", bg = "pink")
            self.TableKanjiListBox.pack(side = "left", padx = 5)


            
            # Defining the variables that will compose the table display
            total_rows = len(self.list_of_keywords)
            division_string = "____________________"
            blank_space = " "

            # Actually creating the "table" by adding the items for each listbox
            for i in range(total_rows):
                if(i == 0):
                    # Making sure the first item also has a blank space to breathroom 
                    self.TableKeywordListBox.insert("end", blank_space)
                    self.TableKeywordListBox.insert("end", " " + self.list_of_keywords[i])
                    self.TableKeywordListBox.insert("end", division_string)
                    self.TableKeywordListBox.insert("end", blank_space)

                    self.TableKanjiListBox.insert("end", blank_space)
                    self.TableKanjiListBox.insert("end", "     " + self.list_of_kanjis[i])
                    self.TableKanjiListBox.insert("end", division_string)
                    self.TableKanjiListBox.insert("end", blank_space)
                else:
                    # Inserting the rest of the list
                    self.TableKeywordListBox.insert("end", " " + self.list_of_keywords[i])
                    self.TableKeywordListBox.insert("end", division_string)
                    self.TableKeywordListBox.insert("end", blank_space)
                    self.TableKanjiListBox.insert("end", "     " + self.list_of_kanjis[i])
                    self.TableKanjiListBox.insert("end", division_string)
                    self.TableKanjiListBox.insert("end", blank_space)
    




    # Functions ------------------------------------------------------------------------------------------------------------

    # Setting scrollbar to scroll both listboxes
    def masterScroll(self, *args):
        self.TableKeywordListBox.yview(*args)
        self.TableKanjiListBox.yview(*args)

#---------------------------------------------------------------------------------------------------------------------------------