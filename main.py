import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import sqlite3
import os

# initialising constants
dbName = "BEM.db"
dbFile = None
searchNumber = 0 # put +1 when showing this number to the user
# general colors used
bgColor = "orange"
errorColor = "red"
successColor = "green"
# font type and font size
fontBig = ("Arial", 26)
fontMedium = ("Arial", 18)
fontFeedback = ("Arial bold", 20)

# initialising the main window and the options
windowMain = Tk()
# noinspection SpellCheckingInspection
windowMain.title("Bogdy's Estate Manager")
windowMain.minsize(height=700, width=600)
windowMain.wm_resizable(height=False, width=False)  # main window can't be resized
windowMain.config(bg=bgColor)

# configuring the style for the frames
mainStyle = ttk.Style()
mainStyle.configure("mainStyle.TFrame", background=bgColor)

# making frames
frameMain = ttk.Frame(master=windowMain, style="mainStyle.TFrame", padding=25)
frameMain.pack()

frameSearch = ttk.Frame(master=windowMain, style="mainStyle.TFrame", padding=10)

frameAdd = ttk.Frame(master=windowMain, style="mainStyle.TFrame", padding=10)
# functions - pack_forget() function "erases" the frame from the screen, while keeping it in memory - same thing with grid_forget()


def showMain():
    """ Shows the main frame and forgets the other frames. """
    dbCreatedLabel.grid_forget()
    resultLabel.grid_forget()
    errorLabel.grid_forget()
    successLabel.grid_forget()
    frameSearch.pack_forget()
    frameAdd.pack_forget()
    frameMain.pack()
    return


def showSearch():
    """ Shows the search frame and forgets the other frames. """
    previousButton.grid_forget()
    nextButton.grid_forget()
    frameMain.pack_forget()
    frameAdd.pack_forget()
    frameSearch.pack()
    return


def showAdd():
    """ Shows the add property frame and forgets the other frames. """
    frameMain.pack_forget()
    frameSearch.pack_forget()
    frameAdd.pack()
    return


def fileDialog():
    """ Will ask for what file you want to import and then store it in another "internal" file which remembers settings
    and all that. """
    global dbFile
    path = tk.filedialog.askopenfile(mode="r", filetypes=[("Database files", ".db")])
    if path is None or path == '':
        if os.path.exists(dbName):
            dbFile = dbName
    else:
        path = str(path).split("'")[1]
        if os.path.exists(path):
            dbFile = path # gets the full file path
    return

def addProperty():
    """ Adds a property to the database and shows either an error or a confirmation message. """
    dbCreatedLabel.grid_forget()
    errorLabel.grid_forget()
    successLabel.grid_forget()
    if nameEntry.get().isnumeric() or priceEntry.get().isalpha() or phoneEntry.get().isalpha() or cityEntry.get().isnumeric():
        errorLabel.config(text="Improper inputs.")
        errorLabel.grid(column=1, pady=30)
        return
    if nameEntry.get() == '' or priceEntry.get() == '' or phoneEntry.get() == '' or cityEntry.get() == '' or selectCurrency.get() == "Select Option" or selectOption.get() == "Select Option":
        errorLabel.config(text="Empty inputs.")
        errorLabel.grid(column=1, pady=30)
        return
    # start of database creation stuff
    global dbFile, dbName
    booly = False
    if dbFile is None:
        dbFile = dbName
        booly = True
        # preparing database stuff
        # USE https://inloop.github.io/sqlite-viewer/ TO VIEW DB FILE CONTENTS
        # TODO: add "permanent" db, just copy everything the whole db code except for the deletes when I eventually implement them
        dbConnection = sqlite3.connect(dbFile)  # creating a connection to the main database
        # dbConnectionP = sqlite3.connect("permanentBEM.db") # creating a connection to the permanent database
        dbCursor = dbConnection.cursor()  # creating a cursor through the connection to the main database
        # dbCursorP = dbConnectionP.cursor() # creating a cursor through the connection to the permanent database
        # tables are created only if they don't exist
        dbCursor.execute("""CREATE TABLE IF NOT EXISTS location(
        city VARCHAR(60) PRIMARY KEY,
        country VARCHAR(60) DEFAULT('Romania')
        )""")
        # dbCursor.execute("""INSERT OR IGNORE INTO location VALUES ('Timisoara', 'Romania')""")
        # DO NOT GIVE THE cID A VALUE, IT MANAGES ITSELF AUTOMATICALLY BECAUSE IT'S AN INTEGER PRIMARY KEY (meaning it just renames "rowid")
        dbCursor.execute("""CREATE TABLE IF NOT EXISTS customers(
        cID INTEGER PRIMARY KEY,
        cName VARCHAR(100) NOT NULL,
        phone INT UNIQUE,
        city VARCHAR(60) DEFAULT('Timisoara'),
        country VARCHAR(60) DEFAULT('Romania')
        )""")
        # cID OF THE properties TABLE SHOULD PICK THE CUSTOMER cID
        dbCursor.execute("""CREATE TABLE IF NOT EXISTS properties(
        cName VARCHAR(100) NOT NULL,
        price INT NOT NULL,
        currency VARCHAR(5) NOT NULL,
        priceType VARCHAR(8) NOT NULL,
        country VARCHAR(60) DEFAULT('Romania'),
        city VARCHAR(60) NOT NULL,
        description TEXT
        )""")
        # dbCursorP.execute("""CREATE TABLE """)
        dbConnection.commit()
        dbConnection.close()
    # end of database creation stuff
    dbConnectionF = sqlite3.connect(dbFile)  # creating a connection to the main database
    dbCursorF = dbConnectionF.cursor()  # creating a cursor through the connection to the main database
    dbCursorF.execute("""INSERT OR IGNORE INTO customers (cName, phone, city) VALUES (?, ?, ?)""",
                     (nameEntry.get(), phoneEntry.get(), cityEntry.get()))
    # DON'T GIVE cID A VALUE
    dbCursorF.execute("""INSERT INTO properties (cName, price, currency, priceType, city, description) VALUES (?, ?, ?, ?, ?, ?)""",
        (nameEntry.get(), priceEntry.get(), selectCurrency.get(), selectOption.get(), cityEntry.get(), descriptionText.get("1.0",'end-1c')))
    dbCursorF.execute("""INSERT OR IGNORE INTO location (city) VALUES (?)""", (cityEntry.get(),)) # WITHOUT THE COMMA, IT'S NOT A TUPLE, SO IT CRASHES
    # dbCursorF.execute("""SELECT * FROM location""")
    # print(dbCursorF.fetchall())
    # dbCursorF.close() # close cursor
    dbConnectionF.commit()  # commit changes
    dbConnectionF.close()  # close the connection
    successLabel.grid(column=1, pady=30) # will be added after each Tkinter object before it, so no row must be specified
    if booly == True:
        dbCreatedLabel.grid(column=1, pady=15) # will be added after each Tkinter object before it, so no row must be specified
    return

def searchResult(booly):
    """ Shows the search result. Give None as the parameter if it's the first time the search result is showed in this
    frame, give False as the parameter if you want the previous result, and True if you want the next one. """
    # only grid_forget() resultLabel when switching back to the main frame
    if searchEntry.get() == '':
        resultLabel.config(text="No input.")
        resultLabel.grid(column=0, row=3, columnspan=2)
        return
    global dbFile, searchNumber # declares that these variables are taken from the global scope
    if dbFile is None:
        if os.path.exists(dbName):
            dbFile = dbName
            dbConnectionF = sqlite3.connect(dbFile)  # creating a connection to the main database
        else:
            resultLabel.config(text="No database selected/created.\nTo create a new database, go to the main\npage and click Add Property, and add a\nproperty.")
            resultLabel.grid(column=0, row=3, columnspan=2)
            return
        dbCursorF = dbConnectionF.cursor()  # creating a cursor through the connection to the main database
        dbCursorF.execute("""SELECT price, currency, priceType, city FROM properties WHERE cName == ?""", (searchEntry.get(),)) # WITHOUT THE COMMA, IT'S NOT A TUPLE, SO IT CRASHES
        fullTextR = dbCursorF.fetchall()
        if len(fullTextR) == 0:
            resultLabel.config(text="No properties.")
            resultLabel.grid(column=0, row=3, columnspan=2)
            # no changes to commit so just close the connection
            dbConnectionF.close()
            return
        if booly is None:
            searchNumber = 0
        elif booly:
            searchNumber += 1
            # -1 because searchNumber stores the index and len(fullTextR) gives the size
            if searchNumber > len(fullTextR) - 1:
                searchNumber = len(fullTextR) - 1
        else:
            searchNumber -= 1
            if searchNumber < 0:
                searchNumber = 0
        textR = "Property {} of {}:\n\n{}: {} {} in\n{} city.".format(searchNumber + 1, len(fullTextR), fullTextR[searchNumber][2], fullTextR[searchNumber][0], fullTextR[searchNumber][1], fullTextR[searchNumber][3])
        resultLabel.config(text=textR)
        resultLabel.grid(column=0, row=3, columnspan=2)
        previousButton.grid(column=0, row=4, pady=25, sticky="W")
        nextButton.grid(column=1, row=4, pady=25, sticky="E")
        # no changes to commit so just close the connection
        dbConnectionF.close()
        return
    else:
        dbConnectionF = sqlite3.connect(dbFile)  # creating a connection to the main database
        dbCursorF = dbConnectionF.cursor()  # creating a cursor through the connection to the main database
        dbCursorF.execute("""SELECT price, currency, priceType, city FROM properties WHERE cName == ?""",
                          (searchEntry.get(),))  # WITHOUT THE COMMA, IT'S NOT A TUPLE, SO IT CRASHES
        fullTextR = dbCursorF.fetchall()
        if len(fullTextR) == 0:
            resultLabel.config(text="No properties.")
            resultLabel.grid(column=0, row=3, columnspan=2)
            # no changes to commit so just close the connection
            dbConnectionF.close()
            return
        if booly is None:
            searchNumber = 0
        elif booly:
            searchNumber += 1
            # -1 because searchNumber stores the index and len(fullTextR) gives the size
            if searchNumber > len(fullTextR) - 1:
                searchNumber = len(fullTextR) - 1
        else:
            searchNumber -= 1
            if searchNumber < 0:
                searchNumber = 0
        textR = "Property {} of {}:\n\n{}: {} {} in\n{} city.".format(searchNumber + 1, len(fullTextR),
                                                                      fullTextR[searchNumber][2],
                                                                      fullTextR[searchNumber][0],
                                                                      fullTextR[searchNumber][1],
                                                                      fullTextR[searchNumber][3])
        resultLabel.config(text=textR)
        resultLabel.grid(column=0, row=3, columnspan=2)
        previousButton.grid(column=0, row=4, pady=25, sticky="W")
        nextButton.grid(column=1, row=4, pady=25, sticky="E")
        # no changes to commit so just close the connection
        dbConnectionF.close()
    return

# buttons
# MAIN frame stuff
# noinspection SpellCheckingInspection
nameLabelMain = ttk.Label(master=frameMain, text="Bogdy's\nEstate\nManager", font=fontBig, padding=35, background=bgColor, justify=CENTER)
nameLabelMain.grid(column=0, row=0)

searchButton = ttk.Button(master=frameMain, text="Search", command=lambda: showSearch(), width=20)
searchButton.grid(column=0, row=1, pady=40)

addButton = ttk.Button(master=frameMain, text="Add property", command=lambda: showAdd(), width=20)
addButton.grid(column=0, row=2)

importButton = ttk.Button(master=frameMain, text="Import file", command=lambda: fileDialog(), width=20)
importButton.grid(column=0, row=3, pady=40)

quitButton = ttk.Button(master=frameMain, text="Quit", command=windowMain.destroy, width=20)
quitButton.grid(column=0, row=4)

# search frame stuff
searchLabel = ttk.Label(master=frameSearch, text="Search name:", font=fontBig, padding=50, background=bgColor, justify=CENTER)
searchLabel.grid(column=0, row=0, columnspan=2)

searchEntry = ttk.Entry(master=frameSearch, width=40)
searchEntry.grid(column=0, row=1, sticky="E", padx=25)
searchSubmit = ttk.Button(master=frameSearch, text="Search", command=lambda: searchResult(None))
searchSubmit.grid(column=1, row=1, columnspan=2, sticky="W")

previousButton = ttk.Button(master=frameSearch, text="< Previous", command=lambda: searchResult(False))
nextButton = ttk.Button(master=frameSearch, text="Next >", command=lambda: searchResult(True))

backButtonSearch = ttk.Button(master=frameSearch, text="Back", command=lambda: showMain())
backButtonSearch.grid(column=0, row=2, pady=50, columnspan=2)

resultLabel = ttk.Label(master=frameSearch, text="", font=fontMedium, background=bgColor, justify=CENTER)

# add property frame stuff
addLabel = ttk.Label(master=frameAdd, text="Add property:", font=fontBig, background=bgColor)
addLabel.grid(column=1, row=0, pady=40)

nameLabelAdd = ttk.Label(master=frameAdd, text="Name:", font=fontMedium, background=bgColor)
nameLabelAdd.grid(column=0, row=1)
nameEntry = ttk.Entry(master=frameAdd, width=40)
nameEntry.grid(column=1, row=1)

phoneLabelAdd = ttk.Label(master=frameAdd, text="Phone no.:", font=fontMedium, background=bgColor)
phoneLabelAdd.grid(column=0, row=2)
phoneEntry = ttk.Entry(master=frameAdd, width=40)
phoneEntry.grid(column=1, row=2)

priceLabel = ttk.Label(master=frameAdd, text="Price:", font=fontMedium, background=bgColor)
priceLabel.grid(column=0, row=3)
priceEntry = ttk.Entry(master=frameAdd, width=40)
priceEntry.grid(column=1, row=3)
selectListCurrency = ["Select Option", "EURO", "RON"]  # the first value won't appear after selection
selectCurrency = tk.StringVar(windowMain)
selectCurrency.set("Select Option")
priceCurrency = ttk.OptionMenu(frameAdd, selectCurrency, *selectListCurrency)
priceCurrency.grid(column=2, row=3)

cityLabel = ttk.Label(master=frameAdd, text="City:", font=fontMedium, background=bgColor)
cityLabel.grid(column=0, row=4)
cityEntry = ttk.Entry(master=frameAdd, width=40)
cityEntry.grid(column=1, row=4)

priceTypeLabel = ttk.Label(master=frameAdd, text="Price for:", font=fontMedium, background=bgColor)
priceTypeLabel.grid(column=0, row=5)
selectList = ["Select Option", "Renting", "Selling"]  # the first value won't appear after selection
selectOption = tk.StringVar(windowMain)
selectOption.set("Select Option")
priceTypeOption = ttk.OptionMenu(frameAdd, selectOption, *selectList)
priceTypeOption.grid(column=1, row=5)

descriptionLabel = ttk.Label(master=frameAdd, text="Description:", font=fontMedium, background=bgColor)
descriptionLabel.grid(column=0, row=6)
descriptionText = tk.Text(master=frameAdd, height=5, width=35)
descriptionText.grid(column=1, row=6)

# labels for feedback on submitting
errorLabel = ttk.Label(master=frameAdd, text=".", font=fontFeedback, background=bgColor, foreground=errorColor)
successLabel = ttk.Label(master=frameAdd, text="Added successfully.", font=fontFeedback, background=bgColor, foreground=successColor)
dbCreatedLabel = ttk.Label(master=frameAdd, text="No database had been\nselected, created one.", font=fontFeedback, background=bgColor)

addSubmit = ttk.Button(master=frameAdd, text="Add", command=lambda: addProperty())
addSubmit.grid(column=1, row=8, pady=30)

backButtonAdd = ttk.Button(master=frameAdd, text="Back", command=lambda: showMain())
backButtonAdd.grid(column=1, row=9)


windowMain.mainloop()
