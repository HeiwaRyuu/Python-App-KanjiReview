# Code by : Vítor Carvalho Marx Lima
# Start Date : 18/08/2020 - Finish Date : Still in Progress



# Importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import psycopg2



# Configurations for the width and height for Remove Kanji
WIDTHRem = 350
HEIGHTRem = 200





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