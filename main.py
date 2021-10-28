import itertools as iter
import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import re, datetime

# FUNCTIONS=========================================================================================================

# open file function
def callCleanRev():
    x1 = " "
    file = askopenfile(parent=root, mode='r', title="choose a file")
    x1 = file.name  # This is getting the exact file address
    completeLabel = tk.Label(root, text=file.name + "has been processed", fg="Blue")
    completeLabel.place_forget()
    eStr1 = e1.get()   # These are getting the inputs from Entry boxes 1-3
    eStr2 = e2.get()
    eStr3 = e3.get()
    intCheck()
    if intCheck() == True:
        if x1.endswith(".csv"):
            completeLabel.place_forget()
            eStr3= int(eStr3)
            clean_rev(x1, eStr1, eStr2, eStr3)
            completeLabel.place(x=60,y=300)
        else:
            newWindow = tk.Toplevel(root)
            newWindow.geometry("350x50")
            completeLabel2 = tk.Label(newWindow, text="WRONG FILE TYPE: please select a CSV file (.csv)", fg="red", font="bold")
            completeLabel2.pack()
    else:
        print("Entry Error")
        completeLabel.place_forget()
        newWindow = tk.Toplevel(root)
        newWindow.geometry("350x50")
        completeLabel2 = tk.Label(newWindow, text="Entry Error: Please enter numeric values ONLY", fg="red", font="bold")
        completeLabel2.pack()
    browse_text.set("Run")


def clean_rev(x, m1, m2, y):
    # This loads the CSV file into the console
    df1 = pd.read_csv(x)
    df1.columns = [
        'Posted_Dt',
        'Doc_Dt',
        'Doc',
        'Memo / Description',
        'Department',
        'Location',
        'Contract',
        'Customer Name',
        'JNL',
        'Curr',
        'Txn Amt',
        'Debit',
        'Credit',
        'Balance (USD)'
    ]
    df1 = df1.fillna(0)
    df1["Total Billed"] = df1.Credit - df1.Debit
    df1.drop(df1[df1['Memo / Description'] == 0].index, inplace=True)
    df1['Posted_Dt'] = pd.DatetimeIndex(df1['Posted_Dt']).month
    pivot1 = pd.pivot_table(df1, index=['Contract', 'Customer Name'],columns='Posted_Dt',values='Total Billed',aggfunc='sum')
    df2 = pd.DataFrame(pivot1.to_records())
    df2 = df2.fillna(0)
    df2["Variance"] = df2[m1] - df2[m2]
    df_final = df2[(df2.Variance >= y) | (df2.Variance <= -y)]
    df_final.to_csv(x)

def callPaymatch():
    file = askopenfile(parent=root, mode='r', title="choose a file")
    x1 = file.name  # This is getting the exact file address
    instructions2 = tk.Label(frame2, text=x1, font="helvetica 12 bold", bg="#F0F0F0")
    instructions2.place(x=180, y=120)
    if x1.endswith(".csv"):
        data = pd.read_csv(x1)
        df1 = data[['Invoice number', 'Total transaction amount due']]
        df1['Total transaction amount due'] = df1['Total transaction amount due'].replace('[$,)]', '', regex=True)
        df1['Total transaction amount due'] = df1['Total transaction amount due'].replace('[(]', '-', regex=True)
        df1['Total transaction amount due'] = df1['Total transaction amount due'].astype(float)
        df2 = df1[(df1['Total transaction amount due'] != 0)]
        df2 = df2.set_index('Invoice number')
        dic = df2.T.to_dict('list')
        for x in dic:
            dic[x] = str(dic[x]).replace("[", '').replace("]", '')
            dic[x] = float(dic[x])
        eStr4 = e4.get()
        eStr4 = float(eStr4)
        paymatch(dic, eStr4)
    else:
        newWindow = tk.Toplevel(root)
        newWindow.geometry("350x50")
        completeLabel2 = tk.Label(newWindow, text="WRONG FILE TYPE: please select a CSV file (.csv)", fg="red", font="bold")
        completeLabel2.pack()

def paymatch (dictionary_pandas, target_value):
    result_window = tk.Toplevel(root,padx="50")


    x = 0
    for i in range(2,len(dictionary_pandas)+1):
        combination_objt = iter.combinations(dictionary_pandas, i)
        combinations_list= list(combination_objt)
        for j in combinations_list:
            count1 = i - 1
            checker1 = 0
            invoices = []
            while count1 >-1:
                checker1 = checker1 + dictionary_pandas[j[count1]]
                invoices.append(j[count1])
                count1 = count1 - 1
            if checker1 == target_value:
                print(invoices)
                invoices += "<---"
                x=1
                completeLabel3 = tk.Label(result_window, text= invoices, fg="black", font="bold")
                completeLabel3.pack()
                fillerLabel = tk.Label(result_window)
                fillerLabel.pack()

    if x == 0:
        completeLabel2 = tk.Label(result_window, text="ENTRY ERROR: No result found", fg="red", font="bold", pady= 10)
        completeLabel2.pack()

def callrevRaquel():
    x1 = " "
    file = askopenfile(parent=root, mode='r', title="choose a file")
    x1 = file.name  # This is getting the exact file address
    if x1.endswith(".xlsx"):
        revRaquel(x1)
        completeLabel = tk.Label(root, text=file.name + "has been processed", fg="Blue")
        completeLabel.place_forget()
        completeLabel.place(x=20,y=300)
    else:
        print("Entry Error")

        newWindow = tk.Toplevel(root)
        newWindow.geometry("350x50")
        completeLabel2 = tk.Label(newWindow, text="WRONG FILE TYPE: please select an Excel file (.xlsx)", fg="red", font="bold")
        completeLabel2.pack()

def revRaquel(x):
    # Import the excel file that needs to have dates adjusted
    data1 = pd.read_excel(x)
    # Drop 1st column since it doesn't have useful information
    data1.pop(data1.columns[0])
    # Create new column which will store the "cleaned dates"
    data1['Date (clean)'] = None
    # To have easy access to the taget columns
    index_description = data1.columns.get_loc('Computation memo')
    index_date = data1.columns.get_loc('Date (clean)')
    # This for-loop looks for the first date on each box under Computation Memo column and send the new value to Date (clean)
    for row in range(0, len(data1)):
        date = re.search(r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})', data1.iat[row, index_description]).group()
        data1.iat[row, index_date] = date
    data1.to_excel(x)

# function to check value of radio button selected
def clicked(value):
    if value == 2:
        Funct2()
    if value == 1:
        Funct1()
    if value == 3:
        Funct3()

# functions to be called by radio buttons to show menu frames
def Funct1():
    frame3.place_forget()
    frame2.place_forget()
    frame1.place(width=600, height=280)


def Funct2():
    frame1.place_forget()
    frame3.place_forget()
    frame2.place(width=600, height=280)

def Funct3():
    frame1.place_forget()
    frame2.place_forget()
    frame3.place(width=600, height=280)

# checks for integer values in entry boxes, will return error
def intCheck():
    try:
        int(e1.get())
        int(e2.get())
        int(e3.get())
        return True
    except ValueError:
        return False


# MAIN GUI CODE=========================================================================================================

# root canvas and frames set up along with icon and title of window
root = tk.Tk()
root.title('I-Land Python app')
#root.iconbitmap('ilandicon.ico')


canvas = tk.Canvas(root)
root.geometry("600x400")
root.resizable(False, False)
# frames will not cover radio buttons in root
frame1 = tk.Frame(root, bg="#F0F0F0", width=290, height=200)
frame2 = tk.Frame(root, bg="#F0F0F0", width=290, height=200)
frame3 = tk.Frame(root, bg="#F0F0F0", width=290, height=200)


# logos for both frames
#logo = Image.open('iland.png')
#logo = ImageTk.PhotoImage(logo)
#logo_label = tk.Label(frame1, image=logo)
#logo_label.image = logo
#logo_label.place(x=200, y=25)
ilandACSIIlogo = r"""
 /$$$$$$         /$$                                 /$$
|_  $$_/        | $$                                | $$
   | $$          | $$        /$$$$$$  /$$$$$$$   /$$$$$$$
   | $$   /$$$$$$| $$       |____  $$| $$__  $$ /$$__  $$
   | $$  |______/| $$        /$$$$$$$| $$  \ $$| $$  | $$
   | $$          | $$       /$$__  $$| $$  | $$| $$  | $$
 /$$$$$$        | $$$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$
|______/        |________/ \_______/|__/  |__/ \_______/
"""
logoLabel = tk.Label(frame1, text="i-Land", font="helvetica 68 bold", fg="blue")
logoLabel.place(x=180, y=25)
logoLabel = tk.Label(frame2, text="i-Land", font="helvetica 68 bold", fg="blue")
logoLabel.place(x=180, y=25)
logoLabel = tk.Label(frame3, text="i-Land", font="helvetica 68 bold", fg="blue")
logoLabel.place(x=180, y=25)
#logo2 = Image.open('iland.png')
#logo2 = ImageTk.PhotoImage(logo2)
#logo2_label = tk.Label(frame2, image=logo2)
#logo2_label.image = logo2
#logo2_label.place(x=200, y=25)
#
#logo3 = Image.open('iland.png')
#logo3 = ImageTk.PhotoImage(logo3)
#logo3_label = tk.Label(frame3, image=logo3)
#logo3_label.image = logo3
#logo3_label.place(x=200, y=25)


# radio buttons for main root bottom menu
r = tk.IntVar()
r.set("1")

radB=tk.Radiobutton(root, text="Revenue Clean-up", variable=r, value=1, command=lambda: clicked(r.get()))
radB.place(x=80,y=350)
radB=tk.Radiobutton(root, text="Pay Match", variable=r, value=2, command=lambda: clicked(r.get()))
radB.place(x=250,y=350)
radB=tk.Radiobutton(root, text="Raquel Rev Report", variable=r, value=3, command=lambda: clicked(r.get()))
radB.place(x=375,y=350)


# instructions for both frames
instructions = tk.Label(frame1, text="Select a file to process", font="helvetica 12 bold", bg="#F0F0F0")
instructions.place(x=380, y=140)

instructions3 = tk.Label(frame3, text="Select a file to process", font="helvetica 12 bold", bg="#F0F0F0")
instructions3.place(x=230, y=180)


# input boxes and labels for both frames
tk.Label(frame1, text="Month 1").place(x=80, y=140)
tk.Label(frame1, text="Month 2").place(x=80, y=190)
tk.Label(frame1, text="Variance scope").place(x=80, y=240)

e1 = tk.Entry(frame1)
e2 = tk.Entry(frame1)
e3 = tk.Entry(frame1)
e1.place(x=180, y=140)
e2.place(x=180, y=190)
e3.place(x=180, y=240)

tk.Label(frame2, text = "Target Value").place(x=130, y=150)
e4 = tk.Entry(frame2)
e4.place(x=220, y=150)


# RUN button set up for both frames
browse_text = tk.StringVar()                                                         # changed font, color, and bg of button
browsebtn = tk.Button(frame1, textvariable=browse_text, command=callCleanRev, font="helvetica 12 bold", bg="sky blue", fg="black", height=1, width=15)
browse_text.set("Select a file")
browsebtn.place(x=380, y=180)

browsebtn2 = tk.Button(frame2, textvariable=browse_text, command=callPaymatch,  font="helvetica 12 bold", bg="sky blue", fg="black", height=1, width=15)
browse_text.set("Select a file")
browsebtn2.place(x=220, y=240)

browsebtn3 = tk.Button(frame3, textvariable=browse_text, command=callrevRaquel,  font="helvetica 12 bold", bg="sky blue", fg="black", height=1, width=15)
browse_text.set("Select a file")
browsebtn3.place(x=220, y=240)


#  starts off program on  frame 1
Funct1()

root.mainloop()
