import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import webbrowser

### Window Settings
home = tk.Tk()
home.geometry("750x350")
home.title("Rename Bulk Files")
home.iconbitmap('RBF_icon.ico')

### Define Grid Layout
## Colum Configure
home.columnconfigure(0, weight = 1)
home.columnconfigure(1, weight = 1)
home.columnconfigure(2, weight = 1)
## Row Configure
home.rowconfigure(0, weight = 1)
home.rowconfigure(1, weight=1)
home.rowconfigure(2, weight=1)
home.rowconfigure(3, weight=1)
home.rowconfigure(4, weight=1)
home.rowconfigure(5, weight=1)
home.rowconfigure(6, weight=1)
home.rowconfigure(7, weight=1)
home.rowconfigure(8, weight=1)

### File Directory
def LocateDirectory():
    global FD_Confirmed
    global FD_Location
    FD_Location = filedialog.askdirectory()
    print("File Directory: ", FD_Location)
    FD_Text.config(text = FD_Location)
    if FD_Location == "":
        FD_Confirmed = False
        FD_Button.config(text= "Not Ready", bg= "red3")
        CheckRenameButtonEnabled()
    else:
        FD_Confirmed = True
        FD_Button.config(text= "Ready", bg= "dodger blue")
        CheckRenameButtonEnabled()

FD_Label = tk.Label(home, text= "Folder Directory", font=('Arial', 16))
FD_Text = tk.Label(home, text = "Please Select A Folder", height = 1, width = 55, bg = "light gray")
FD_Button = tk.Button(home,text= "Not Ready",fg= "white", font=('Arial', 16), height = 1, width = 10, bg = "red3", command=LocateDirectory)
FD_Confirmed = False
FD_Location = ""

### File Type
def FT_Valid():
    global FT_Result
    global FT_Confirmed
    FT_Result = FT_Dropdown.get()
    if FT_Confirmed is True:
        FT_Confirmed = False
        FT_Check_Button()
    elif FT_Result.startswith('.'):
        FT_Confirmed = True
        FT_Check_Button()
        print("File Type:", FT_Result)
    else:
        FT_Confirmed = False
        FT_Check_Button()
        print("File Type Must Start With A .")

def FT_Check_Button():
    if FT_Confirmed is True:
        FT_Button.config(text= "Ready", bg= "dodger blue")
        FT_Dropdown.config(state= "disabled")
        CheckRenameButtonEnabled()
    else:
        FT_Button.config(text= "Not Ready", bg= "red3")
        FT_Dropdown.config(state= "normal")
        CheckRenameButtonEnabled()

FT_Label = tk.Label(home, text= "File Type", font=('Arial', 16))
FT_Options = [
    '.png', '.jpeg', '.jpg', '.svg', '.ico', '.gif', '.tiff', '.bmp',
    '.wav', '.mp3', '.flac', '.aac', '.ogg',
    '.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.rtf',
    '.html', '.htm', '.css', '.js', '.json', '.xml', '.csv', '.md',
    '.zip', '.rar', '.tar', '.gz', '.7z',
    '.exe', '.dll', '.bin', '.iso',
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg',
    '.psd', '.ai', '.eps', '.indd', '.raw',
    '.sqlite', '.db', '.dbf', '.mdb', '.accdb',
    '.apk', '.ipa', '.jar', '.bat', '.sh', '.pl', '.py', '.rb', '.php'
]
FT_Dropdown = ttk.Combobox(home, values=FT_Options, height=1, width=30)
FT_Button = tk.Button(home,text= "Not Ready",fg= "white", font=('Arial', 16), height = 1, width = 10, bg = "red3", command=FT_Valid)
FT_Result = ""
FT_Confirmed = False

### Search Word
def Save_SearchWord():
    global SearchWord_Confirmed
    global Search_Word
    Search_Word = SearchWord_Text.get("1.0", "end-1c")
    if Search_Word == "":
        print("Current Word Cannot Be Blank")
    else:
        print("Current Word: ", Search_Word)
        SearchWord_SaveButton.config(text= "Ready", bg='dodger blue')
        SearchWord_Text.config(state='disabled')
        SearchWord_Confirmed = True
        CheckRenameButtonEnabled()

def Check_SearchWord():
    global SearchWord_Confirmed
    if SearchWord_Confirmed is True:
        SearchWord_Text.config(state='normal')
        SearchWord_SaveButton.config(text= "Not Ready", bg="red3")
        SearchWord_Confirmed = False
        CheckRenameButtonEnabled()
    else:
        Save_SearchWord()
        CheckRenameButtonEnabled()

def Check_SearchWord_Blank():
    global Search_Word

SearchWord_Label = tk.Label(home, text="Current Word", font=('Arial', 16))
SearchWord_Text = tk.Text(home, height = 2, width = 50, bg = "light grey", wrap='none')
SearchWord_SaveButton = tk.Button(home,text= "Not Ready",fg= "white", font=('Arial', 16), height = 1, width = 10, bg = "red3",command=Check_SearchWord)
SearchWord_Confirmed = False
Search_Word = ""

### New Word
def Save_NewWord():
    global NewWord_Confirmed
    global New_Word
    New_Word = NewWord_Text.get("1.0", "end-1c")
    print("New Word: ", New_Word)
    NewWord_SaveButton.config(text= "Ready", bg = "dodger blue")
    NewWord_Text.config(state= 'disabled')
    NewWord_Confirmed = True
    CheckRenameButtonEnabled()

def Check_NewWord():
    global NewWord_Confirmed
    if NewWord_Confirmed is True:
        NewWord_Text.config(state='normal')
        NewWord_SaveButton.config(text= "Not Ready", bg="red3")
        NewWord_Confirmed = False
        CheckRenameButtonEnabled()
    else:
        Save_NewWord()
        CheckRenameButtonEnabled()

NewWord_Label = tk.Label(home, text="New Word", font=('Arial', 16))
NewWord_Text = tk.Text(home, height = 2, width = 50, bg = "light grey", wrap='none')
NewWord_SaveButton = tk.Button(home,text= "Not Ready",fg= "white", font=('Arial', 16), height = 1, width = 10, bg = "red3",command=Check_NewWord)
NewWord_Confirmed = False
New_Word = ""

### Apply Rename Button
def ApplyRename():
    global ApplyRenameButton
    if NewWord_Confirmed is True and SearchWord_Confirmed is True and FD_Confirmed is True and FT_Confirmed is True:
        RenameFiles()
    else:
        print("Please Make Sure All Inputs Are Correct And Confirmed With Red/Green Buttons On The Right")

def RenameFiles():
    global ApplyRenameButton
    global FT_Dropdown
    global FT_Button
    global FT_Confirmed
    global SearchWord_SaveButton
    global SearchWord_Text
    global SearchWord_Confirmed
    global NewWord_SaveButton
    global NewWord_Text
    global NewWord_Confirmed
    for filename in os.listdir(FD_Location):
        if filename.endswith(FT_Result) and Search_Word in filename:
            new_filename = filename.replace(Search_Word, New_Word)
            old_file = os.path.join(FD_Location, filename)
            new_file = os.path.join(FD_Location, new_filename)
            os.rename(old_file, new_file)
            print(f'Renamed: {filename} to {new_filename}')
    else:
        print("Rename Complete")
        FT_Dropdown.config(state='normal')
        FT_Button.config(text="Not Ready", bg="red3")
        FT_Confirmed = False
        SearchWord_SaveButton.config(text="Not Ready", bg="red3")
        SearchWord_Text.config(state='normal')
        SearchWord_Confirmed = False
        NewWord_SaveButton.config(text="Not Ready", bg="red3")
        NewWord_Text.config(state='normal')
        NewWord_Confirmed = False
        CheckRenameButtonEnabled()

ApplyRenameButton = tk.Button(home,text= "NOT READY",fg= "white", font= ("Arial", 16), height = 1, width = 12, bg= "red3", command=ApplyRename,state= 'disabled',disabledforeground= "white")

### Check Rename Button Enabled
def CheckRenameButtonEnabled():
    global ApplyRenameButton
    if FD_Confirmed is True and SearchWord_Confirmed is True and NewWord_Confirmed is True and FT_Confirmed is True:
        ApplyRenameButton.config(text= "Apply", bg= "dodger blue", state= 'normal')
    else:
        ApplyRenameButton.config(text= "NOT READY",bg= "Red3",state= 'disabled')

### Open URL
def OpenURL():
    webbrowser.open_new_tab(URL)

URL = "www.lukelz.com"
Credits_Label = tk.Label(home, text="www.lukelz.com", font=('Arial', 10))
Credits_Label.bind("<Button-1>", lambda e:OpenURL())

### Place Widgets
FD_Label.grid(row=1, column=0)
FD_Text.grid(row=1, column=1)
FD_Button.grid(row=1, column=2)

FT_Label.grid(row=2, column=0)
FT_Dropdown.grid(row=2, column=1)
FT_Button.grid(row=2, column=2)

SearchWord_Label.grid(row=3, column = 0)
SearchWord_Text.grid(row=3, column = 1)
SearchWord_SaveButton.grid(row=3, column = 2)

NewWord_Label.grid(row=4, column=0)
NewWord_Text.grid(row=4, column=1)
NewWord_SaveButton.grid(row=4, column=2)

ApplyRenameButton.grid(row=6, column=1)
Credits_Label.grid(row=7, column=2)

home.mainloop()