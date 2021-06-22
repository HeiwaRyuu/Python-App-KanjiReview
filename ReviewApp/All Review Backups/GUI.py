# Code by : Vítor Carvalho Marx Lima
# Start Date : 18/08/2020 - Finish Date : Still in Progress

# Importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import psycopg2


# Configurations for the width and height for Main Window
WIDTH = 550
HEIGHT = 350

# Configurations for the width and height for Add Kanji
WIDTHAdd = 350
HEIGHTAdd = 200
# Configuration for text input in Add Kanji
keyword_entry_length = 60
kanji_entry_length = 40
safety_length = 10

# Configurations for the width and height for Remove Kanji
WIDTHRem = 350
HEIGHTRem = 200

# Configurations for the width and height for Table of Kanji
WIDTHToK = 500
HEIGHTToK = 300




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
        self.TitleLabel.config(font = ("Courier", 20, "bold"), bg = "pink", fg = "#C71150")
        self.TitleLabel.pack()


        # Adding the image to the master
        image = Image.open("Images/umaru.jpg").resize((300,200), Image.ANTIALIAS)
        UmaruPath = ImageTk.PhotoImage(image)
        self.Umarulabel = tk.Label(self.ImageCanvas, image = UmaruPath)
        self.Umarulabel.image = UmaruPath
        self.Umarulabel.pack()

        





        # Buttons ------------------------------------------------------------------------------------------------------------

        # Creating the Button that opens the Kanji List
        self.KanjiListPopButton = tk.Button(self.ButtonsCanvas, text = "Show Kanji List", command = lambda: self.OpenNewWindow(TableOfKanjis))
        self.KanjiListPopButton.config(height = 2, width = 16 , bg = "#F98FB4")
        self.KanjiListPopButton.pack(side = "right", padx = 5)


        # Creating the Button that opens the Add to kanji List window
        self.AddKanjiButton = tk.Button(self.ButtonsCanvas, text = "Add Kanji", command = lambda: self.OpenNewWindow(AddKanjiWindow))
        self.AddKanjiButton.config(height = 2, width = 16, bg = "#F98FB4")
        self.AddKanjiButton.pack(side = "right", padx = 5)


        # Creating the Button that opens the Remove from kanji list window
        self.RemoveKanjiButton = tk.Button(self.ButtonsCanvas, text = "Remove Kanji", command = lambda: self.OpenNewWindow(RemoveKanjiWindow))
        self.RemoveKanjiButton.config(height = 2, width = 16, bg = "#F98FB4")
        self.RemoveKanjiButton.pack(side = "right", padx = 5)


        # Creating the Button that opens the Review window
        self.ReviewButton = tk.Button(self.ButtonsCanvas, text = "Start Review", command = lambda: self.OpenNewWindow(AddKanjiWindow))
        self.ReviewButton.config(height = 2, width = 16, bg = "#F98FB4")
        self.ReviewButton.pack(side = "right", padx = 5)




    # Functions ------------------------------------------------------------------------------------------------------------

    # Creating the function that pops new windows
    def OpenNewWindow(self, windowClass):
        self.NewWindow = tk.Toplevel(self.master)
        windowClass(self.NewWindow)











class AddKanjiWindow:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTHAdd}x{HEIGHTAdd}")
        self.master.maxsize(WIDTHAdd, HEIGHTAdd)
        self.master.minsize(WIDTHAdd, HEIGHTAdd)
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
        elif len(self.Keywordcontent.get()) > (keyword_entry_length - safety_length):
            self.too_long_keyword()
        elif len(self.Kanjicontent.get()) > (kanji_entry_length - safety_length):
            self.too_long_kanji()
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
            create_table = "CREATE TABLE IF NOT EXISTS review (id SERIAL PRIMARY KEY, keyword VARCHAR({}) NOT NULL, kanji VARCHAR({}) NOT NULL)"
            cur.execute(create_table.format(keyword_entry_length, kanji_entry_length))
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
                # Confirming the execution and changes in database
                conn.commit()
                # Closing the connection with the database after finishing all changes
                cur.close()
                conn.close()
                # Message showing that the keyword and kanji were successfully added
                self.successfully_added()




# Errors and Messages ------------------------------------------------------------------------------------------------------------



    # Warning for empty keyword entry
    def empty_keyword(self):
        tk.messagebox.showwarning(title = "Empty Keyword Entry", message = "Please enter a keyword")


    # Warning for empty kanji entry
    def empty_kanji(self):
        tk.messagebox.showwarning(title = "Empty Kanji Entry", message = "Please enter a kanji")
    



    # Warning for too many characters into keyword entry
    def too_long_keyword(self):
        tk.messagebox.showwarning(title = "Too long keyword!", message = "Please enter a keyword less than {} characters!".format(keyword_entry_length - safety_length))

    # Warning for too many characters into kanji entry
    def too_long_kanji(self):
        tk.messagebox.showwarning(title = "Too many kanji!", message = "Please enter less than {} characters into the kanji entry!".format(kanji_entry_length - safety_length))




    # Warning for already existant keyword in database
    def existing_keyword(self):
        tk.messagebox.showwarning(title = "Existing Keyword", message = "This keyword is already in the database!")

    
    # Warning for empty kanji entry
    def existing_kanji(self):
        tk.messagebox.showwarning(title = "Existing Kanji", message = "This kanji is already in the database!")


    # Warning for successfully adding the keyword and kanji to the database
    def successfully_added(self):
        tk.messagebox.showwarning(title = "Successfully added!", message = "Keyword and kanji successfully added!")







#---------------------------------------------------------------------------------------------------------------------------------







class RemoveKanjiWindow:

    def __init__(self, master):
        # Defining master configs
        self.master = master
        self.master.geometry(f"{WIDTHRem}x{HEIGHTRem}")
        self.master.maxsize(WIDTHRem, HEIGHTRem)
        self.master.minsize(WIDTHRem, HEIGHTRem)
        self.master.iconbitmap("Images/icon.ico")
        self.master.title("漢字復習 -Removing a kanji!")
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
        self.KeywordLabel = tk.Label(self.KeywordCanvas, text = "Select the desired Keyword:", bg = "pink", width = 25)
        self.KeywordLabel.pack(side = "left")

        # Adding the Label for Kanji
        self.KanjiLabel = tk.Label(self.KanjiCanvas, text = "Check if its the disred kanji:", bg = "pink", width = 25)
        self.KanjiLabel.pack(side = "left")






        # Drop down menu ------------------------------------------------------------------------------------------------------------

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



        # Adding the drop down menu for Keyword
        self.Empty_list = ["Empty"]

        if len(self.list_of_keywords) == 0:
            self.KeywordComboBox = ttk.Combobox(self.KeywordCanvas, value = self.Empty_list[0])
            self.KeywordComboBox.current(0)
            self.KeywordComboBox.pack(side = "left")
        else:
            self.KeywordComboBox = ttk.Combobox(self.KeywordCanvas, value = self.list_of_keywords)
            self.KeywordComboBox.current(0)
            self.KeywordComboBox.bind("<<ComboboxSelected>>", self.update_kanji_dropdown)
            self.KeywordComboBox.pack(side = "left")

        if len(self.list_of_keywords) == 0:
            self.KanjiComboBox = ttk.Combobox(self.KanjiCanvas, value = self.Empty_list[0])
            self.KanjiComboBox.current(0)
            self.KanjiComboBox.pack(side = "left")
        else:
            self.KanjiComboBox = ttk.Combobox(self.KanjiCanvas, value = self.list_of_kanjis)
            self.KanjiComboBox.current(0)
            self.KanjiComboBox.bind("<<ComboboxSelected>>", self.update_keyword_dropdown)
            self.KanjiComboBox.pack(side = "left")




    # Buttons ------------------------------------------------------------------------------------------------------------

        # Adding the button to close window
        self.RemoveKanjiCloseButton = tk.Button(self.ButtonsCanvas, text = "Go back", width = 15, command = self.master.destroy)
        self.RemoveKanjiCloseButton.pack(side = "left", padx = 4)

        # Adding the button that removes all items
        self.DeleteAllButton = tk.Button(self.ButtonsCanvas, text = "Delete All Data", width = 15, command = self.RemAllData)
        self.DeleteAllButton.pack(side = "left", padx = 4)

        # Adding the button that effectivelly removes the Kanji
        self.RemoveButton = tk.Button(self.ButtonsCanvas, text = "Remove kanji", width = 15, command = self.RemKanji)
        self.RemoveButton.pack(side = "left", padx = 4)



    # Functions ------------------------------------------------------------------------------------------------------------

    # Defining the function that updates the kanji dropdown when user changes keyword dropdown value
    def update_kanji_dropdown(self, list):
        try:
            index = self.KeywordComboBox.current()
            self.KanjiComboBox.current(index)
        except:
            self.KeywordComboBox = ttk.Combobox(self.KeywordCanvas, value = self.Empty_list[0])



    # Defining the function that updates the keyword dropdown when user changes keyword dropdown value
    def update_keyword_dropdown(self, list):
        try:
            index = self.KanjiComboBox.current()
            self.KeywordComboBox.current(index)
        except:
            self.KanjiComboBox = ttk.Combobox(self.KeywordCanvas, value = self.Empty_list[0])



    # Defining the function that adds the new kanji and keyword to the list
    def RemKanji(self):
        if(len(self.list_of_keywords) == 0):
            self.empty_list_warning()
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

            # Creating the action of deleting an element from the table itself
            # Here we are grabing the values from the drop down menu
            selected_keyword = self.list_of_keywords[self.KeywordComboBox.current()]
            selected_kanji = self.list_of_kanjis[self.KanjiComboBox.current()]
            if self.confirm_remove(selected_keyword, selected_kanji) == 0:
                pass
            else:
                # Here we are performing the action of removing the elements from the database
                delete_keyword_kanji_command = "DELETE FROM review WHERE keyword = '{}' AND kanji = '{}'"
                cur.execute(delete_keyword_kanji_command.format(selected_keyword, selected_kanji))
                print("The elements have been removed successfully")
                # Confirming the execution and changes in database
                conn.commit()
                # Closing the connection with the database after finishing all changes
                cur.close()
                conn.close()

                # Message showing that the keyword and kanji were successfully removed
                self.successfully_removed()

                # Updating the lists itself to show off on drop down menus
                self.list_of_keywords.remove(selected_keyword)
                self.list_of_kanjis.remove(selected_kanji)
                self.KeywordComboBox.config(values = self.list_of_keywords)
                try:
                    self.KeywordComboBox.current(0)
                except:
                    self.KeywordComboBox.config(value = self.Empty_list[0])
                    self.KeywordComboBox.current(0)

                self.KanjiComboBox.config(values = self.list_of_kanjis)

                try:
                    self.KanjiComboBox.current(0)
                except:
                    self.KanjiComboBox.config(value = self.Empty_list[0])
                    self.KanjiComboBox.current(0)



    # Defining the delete all data function
    def RemAllData(self):
        if(len(self.list_of_keywords) == 0):
            self.empty_list_warning()
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

            # Creating the action of deleting an element from the table itself
            # Here we are grabing the values from the drop down menu
            if self.confirm_delete_all_data() == 0:
                pass
            else:
                # Here we are performing the action of removing the elements from the database
                delete_all_data_command = "TRUNCATE TABLE review"
                cur.execute(delete_all_data_command)
                print("All data has been removed successfully!")
                # Confirming the execution and changes in database
                conn.commit()
                # Closing the connection with the database after finishing all changes
                cur.close()
                conn.close()

                # Message showing that the keyword and kanji were successfully removed
                self.successfully_removed_all()
                self.list_of_keywords.clear()
                self.list_of_kanjis.clear()
                self.KeywordComboBox.config(values = self.list_of_keywords)
                try:
                    self.KeywordComboBox.current(0)
                except:
                    self.KeywordComboBox.config(value = self.Empty_list[0])
                    self.KeywordComboBox.current(0)

                self.KanjiComboBox.config(values = self.list_of_kanjis)

                try:
                    self.KanjiComboBox.current(0)
                except:
                    self.KanjiComboBox.config(value = self.Empty_list[0])
                    self.KanjiComboBox.current(0)






# Errors and Messages ------------------------------------------------------------------------------------------------------------



    # Warning for empty database
    def empty_list_warning(self):
        tk.messagebox.showwarning(title = "No data in database!", message = "The list is empty. No data to erase!")

    # Warning for successfully removing the keyword and kanji to the database
    def successfully_removed(self):
        tk.messagebox.showwarning(title = "Successfully removed!", message = "Keyword and kanji successfully removed!")

    # Warning for successfully removing ALL DATA from database
    def successfully_removed_all(self):
        tk.messagebox.showwarning(title = "Successfully removed!", message = "All data erased successfully!!")

    # Asking for confirmation before removing a keyword and kanji from database
    def confirm_remove(self, keyword, kanji):
        MsgBox = tk.messagebox.askquestion ("Confirm Deleting","Are you sure you want to delete the keyword:'{}' and the kanji:'{}'?".format(keyword, kanji) ,icon = "warning")
        if MsgBox == "yes":
            return 1
        else:
            return 0

    # Asking for confirmation before removing ALL DATA from database
    def confirm_delete_all_data(self):
        MsgBox = tk.messagebox.askquestion ("Confirm Deleting","Are you sure you want to delete ALL DATA?",icon = "warning")
        if MsgBox == "yes":
            return 1
        else:
            return 0








#---------------------------------------------------------------------------------------------------------------------------------








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


        # Adding the table title canvas
        self.TableTitle = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TableTitle.pack()

        # Adding subtitles canvas
        self.TableSubTitle = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TableSubTitle.pack()

        # Adding the table canvas 
        self.TableCanvas = tk.Canvas(self.master, bg = "pink", highlightthickness=0)
        self.TableCanvas.pack()


        # Adding the title label
        self.TitleLabel = tk.Label(self.TableTitle, text = "Keyword and 漢字 table")
        self.TitleLabel.config(font = ("Courier", 20, "bold"), fg = "#C71150",bg = "pink")
        self.TitleLabel.pack()


        # Adding the subtitles labels
        self.KeywordSubTitleLabel = tk.Label(self.TableSubTitle, text = "Keywords")
        self.KeywordSubTitleLabel.config(width = 10, font = ("Courier", 15, "bold"), fg = "#C71150",bg = "pink")
        self.KeywordSubTitleLabel.pack(side = "left", pady = 10)

        self.KanjiSubTitleLabel = tk.Label(self.TableSubTitle, text = "Kanjis")
        self.KanjiSubTitleLabel.config(width = 10, font = ("Courier", 15, "bold"), fg = "#C71150",bg = "pink")
        self.KanjiSubTitleLabel.pack(side = "left", pady = 10, padx = 30)


      

        # Defining the function that adds the new kanji and keyword to the list
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
            self.EmptyTable01.config(font = ("Courier", 15), fg = "#C71150", bg = "pink")
            self.EmptyTable01.pack(pady = 10)

            self.EmptyTable02 = tk.Label(self.TableCanvas, text = "Add some and come back later!")
            self.EmptyTable02.config(font = ("Courier", 15), fg = "#C71150", bg = "pink")
            self.EmptyTable02.pack(pady = 10)

        # Else, we just print out the list from database
        else:
            # Adding a scrollbar to view the list when it gets bigger than the screen size
            self.TableScrollbar = tk.Scrollbar(self.TableCanvas)
            self.TableScrollbar.pack(side = "right", fill = "y")

            # Creating a listbox to display as table
            self.TableKeywordListBox = tk.Listbox(self.TableCanvas, yscrollcommand = self.TableScrollbar.set)
            self.TableKeywordListBox.config(width=15, height = 10, font = ("Courier", 12), highlightthickness=0, highlightbackground = "#C71150", fg = "#C71150", bg = "pink")
            self.TableKeywordListBox.pack(side = "left", padx = 5)


            # Creating a listbox to display as table
            self.TableKanjiListBox = tk.Listbox(self.TableCanvas, yscrollcommand = self.TableScrollbar.set)
            self.TableKanjiListBox.config(width=15, height = 10, font = ("Courier", 12), highlightthickness=0, highlightbackground = "#C71150", fg = "#C71150", bg = "pink")
            self.TableKanjiListBox.pack(side = "left", padx = 5)



            self.TableScrollbar.config(command = self.masterScroll)

            # Defining the variables that will compose the table display
            total_rows = len(self.list_of_keywords)
            division_string = "____________________"
            blank_space = " "
            # Creating the list we use to output the table data into the table
            self.display_list = list(zip(self.list_of_keywords, self.list_of_kanjis))


            #for i in range(total_rows):
            for i in range(total_rows):
                if(i == 0):
                    # Making sure the first item also has a blank space to breathroom 
                    self.TableKeywordListBox.insert("end", blank_space)
                    self.TableKeywordListBox.insert("end", " " + self.list_of_keywords[i])
                    self.TableKeywordListBox.insert("end", division_string)
                    self.TableKeywordListBox.insert("end", blank_space)

                    self.TableKanjiListBox.insert("end", blank_space)
                    self.TableKanjiListBox.insert("end", "       " + self.list_of_kanjis[i])
                    self.TableKanjiListBox.insert("end", division_string)
                    self.TableKanjiListBox.insert("end", blank_space)
                else:
                    # Inserting the rest of the list
                    self.TableKeywordListBox.insert("end", " " + self.list_of_keywords[i])
                    self.TableKeywordListBox.insert("end", division_string)
                    self.TableKeywordListBox.insert("end", blank_space)
                    self.TableKanjiListBox.insert("end", "       " + self.list_of_kanjis[i])
                    self.TableKanjiListBox.insert("end", division_string)
                    self.TableKanjiListBox.insert("end", blank_space)


            # Adding the table with the data output
            #for i in range(total_rows):
                # Creating one separate canvas for each row, because we are not going to use grid
            #    RowCanvas = tk.Canvas(self.TableListBox)
            #    RowCanvas.pack()
            #    for j in range(total_columns):
                # Iserting the entries and inserting the data into each one, firt keyword, and then kanji
            #        Table = tk.Entry(RowCanvas, fg = "#C71150", width = 15)
            #        Table.config(font = ("Courier", 15))
            #        Table.pack(side = "left")
            #        Table.insert("end", self.display_list[i][j])
    

    # Setting scrollbar to scroll both listboxes
    def masterScroll(self, *args):
        self.TableKeywordListBox.yview(*args)
        self.TableKanjiListBox.yview(*args)

#---------------------------------------------------------------------------------------------------------------------------------







# Running app ------------------------------------------------------------------------------------------------------------

root = tk.Tk()
app = MainWindow(root)
root.mainloop()