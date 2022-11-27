import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# import pybind11
# import file_management

# initialising constants
bgColor = "orange"
fontBig = ("Arial", 26)  # font type and font size
fontMedium = ("Arial", 18)  # font type and font size

# initialising the main window and the options
windowMain = Tk()
windowMain.title("BE")
windowMain.minsize(height=650, width=550)
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
# functions - pack_forget() function "erases" the frame from the screen, while keeping it in memory


def showMain():
    """ Shows the main frame and forgets the other frames """
    frameSearch.pack_forget()
    frameAdd.pack_forget()
    frameMain.pack()


def showSearch():
    """ Shows the search frame and forgets the other frames """
    frameMain.pack_forget()
    frameAdd.pack_forget()
    frameSearch.pack()


def showAdd():
    """ Shows the add property frame and forgets the other frames """
    frameMain.pack_forget()
    frameSearch.pack_forget()
    frameAdd.pack()


def fileDialog():
    """ Will ask for what file you want to import and then store it in another "internal" file which remembers settings
    and all that """
    file = tk.filedialog.askopenfile(mode="r", filetypes=[("Text files", ".txt")])
    # copy the file


# buttons
# main frame stuff
nameLabelMain = ttk.Label(master=frameMain, text="BE", font=fontBig, padding=40, background=bgColor)
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
searchLabel = ttk.Label(master=frameSearch, text="Search name:", font=fontBig, padding=50, background=bgColor)
searchLabel.grid(column=0, row=0)

searchEntry = ttk.Entry(master=frameSearch, width=25)
searchEntry.grid(column=0, row=1)
searchSubmit = ttk.Button(master=frameSearch, text="Search")  # PUT COMMAND
searchSubmit.grid(column=1, row=1)

backButtonSearch = ttk.Button(master=frameSearch, text="Back", command=lambda: showMain())
backButtonSearch.grid(column=0, row=2, pady=50)

# add property frame stuff
addLabel = ttk.Label(master=frameAdd, text="Add property:", font=fontBig, background=bgColor)
addLabel.grid(column=1, row=0, pady=40)

nameLabelAdd = ttk.Label(master=frameAdd, text="Name:", font=fontMedium, background=bgColor)
nameLabelAdd.grid(column=0, row=1)
nameEntry = ttk.Entry(master=frameAdd, width=35)
nameEntry.grid(column=1, row=1)

priceLabel = ttk.Label(master=frameAdd, text="Price:", font=fontMedium, background=bgColor)
priceLabel.grid(column=0, row=2)
priceEntry = ttk.Entry(master=frameAdd, width=35)
priceEntry.grid(column=1, row=2)
selectListCurrency = ["Select Option", "EURO", "RON"]  # the first value won't appear after selection
selectCurrency = tk.StringVar(windowMain)
selectCurrency.set("Select Option")
priceCurrency = ttk.OptionMenu(frameAdd, selectCurrency, *selectListCurrency)
priceCurrency.grid(column=2, row=2)

cityLabel = ttk.Label(master=frameAdd, text="City:", font=fontMedium, background=bgColor)
cityLabel.grid(column=0, row=3)
cityEntry = ttk.Entry(master=frameAdd, width=35)
cityEntry.grid(column=1, row=3)

priceTypeLabel = ttk.Label(master=frameAdd, text="Price for:", font=fontMedium, background=bgColor)
priceTypeLabel.grid(column=0, row=4)
selectList = ["Select Option", "Renting", "Selling"]  # the first value won't appear after selection
selectOption = tk.StringVar(windowMain)
selectOption.set("Select Option")
priceTypeOption = ttk.OptionMenu(frameAdd, selectOption, *selectList)
priceTypeOption.grid(column=1, row=4)

descriptionLabel = ttk.Label(master=frameAdd, text="Description:", font=fontMedium, background=bgColor)
descriptionLabel.grid(column=0, row=5)
descriptionText = tk.Text(master=frameAdd, height=5, width=35)
descriptionText.grid(column=1, row=5)

addSubmit = ttk.Button(master=frameAdd, text="Add")  # PUT COMMAND
addSubmit.grid(column=1, row=6, pady=30)

backButtonAdd = ttk.Button(master=frameAdd, text="Back", command=lambda: showMain())
backButtonAdd.grid(column=1, row=7)


windowMain.mainloop()
