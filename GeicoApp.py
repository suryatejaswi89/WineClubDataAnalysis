from Tkinter import *
import csv
import sqlite3

window = Tk()
mainFrame = Frame(window)
mainFrame.grid(row=0, column=0, sticky="nsew")

def initializeFrame(title):
    resultFrame = Frame(window)
    resultFrame.grid(row=0, column=0, sticky="nsew")
    topButton = Button(resultFrame, text="CLOSE", command=lambda: closeResultsFrame(resultFrame))
    topButton.grid(column=0, row=0)
    frame_title = Label(resultFrame, text=title)
    frame_title.grid(column=1, row=0, columnspan=10)
    return resultFrame

def closeResultsFrame(resultFrame):
    resultFrame.destroy()

window.title("Wine Club Data Analysis")
window.geometry("{0}x{1}+0+0".format(
    window.winfo_screenwidth()-3, window.winfo_screenheight()-3))

def loadMembersAndStoreData(members_path, store_path, frame):
    conn = sqlite3.connect('members.db')
    c = conn.cursor()

    f1 = csv.reader(open(members_path))
    f2 = csv.reader(open(store_path))

    header1 = f1.next()
    header2 = f2.next()



    # Create store_table
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS stores_table(
        'StoreId' integer PRIMARY KEY,
        'StoreName' text,
        'Location' text
        )
        '''
    )

    for line in f2:
        # Insert a row of data
        commaSeparatedVals = "";
        for val in line:
            if commaSeparatedVals is "":
                commaSeparatedVals = commaSeparatedVals + "'" + ("%s" % val) + "'"
            else:
                commaSeparatedVals = commaSeparatedVals + ", '" + ("%s" % val) + "'"
        query1 = "INSERT INTO stores_table('StoreId','StoreName','Location')" + (" VALUES (%s)" % commaSeparatedVals)

        c.execute(query1)

    # Create members_table
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS members_table (
         'Member#' text PRIMARY KEY,
         'LastName' text,
         'FirstName' text,
         'StreetAddress' text,
         'City' text,
         'State' text,
         'ZipCode' int,
         'Phone'  text,
         'FavoriteStore'  int,
         'DateJoined' Date,
         'DuesPaid' text,
         FOREIGN KEY(FavoriteStore) REFERENCES stores_table(StoreId)
        );
        ''')

    for line in f1:
        # Insert a row of data
        commaSeparatedVals = "";
        for val in line:
            if commaSeparatedVals is "":
                commaSeparatedVals = commaSeparatedVals + "'" + ("%s" % val) + "'"
            else:
                commaSeparatedVals = commaSeparatedVals + ", '" + ("%s" % val) + "'"

        # query1 = "INSERT INTO stores_table('StoreId','StoreName','Location')"+(" VALUES (%s)" % commaSeparatedVals)
        query2 = "INSERT INTO members_table ('Member#','LastName','FirstName','StreetAddress','City','State','ZipCode','Phone','FavoriteStore','DateJoined','DuesPaid')" + (
                    " VALUES (%s)" % commaSeparatedVals)

        c.execute(query2)

    # Save (commit) the changes

    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    import_complete = Label(frame, text="Success!! click on close for main menu!")
    import_complete.grid(column=1, row=8)

def showQueryButtons():
    query1_button = Button(window, text="Query 1", command=executeQuery1)
    query1_button.grid(column=0, row=0)

def displayResultTable(rows,start_row,resultsFrame):
    resultsFrame.tkraise(mainFrame)
    row_counter=start_row
    col_counter=0
    for row in rows:
        print(row)
        for col in row:
            curr_ele =Label(resultsFrame, text=col)
            curr_ele.grid(column=col_counter, row=row_counter)
            col_counter = col_counter + 1
            col_divider = Label(resultsFrame, text="|")
            col_divider.grid(column=col_counter, row=row_counter)
            col_counter = col_counter + 1
        col_counter = 0
        row_counter = row_counter + 1

def createResultsFrame(header,rows, title):
    resultsFrame = initializeFrame(title)
    displayResultTable(header,4,resultsFrame)
    displayResultTable(rows,5,resultsFrame)

def executeQuery1():

    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    query1 = '''
    SELECT * FROM 'members_table' ORDER BY LastName ASC;
    '''
    headerRow = [['Member#','LastName','FirstName','StreetAddress','City','State','ZipCode','Phone','FavoriteStore','DateJoined','DuesPaid']]
    c.execute(query1)
    rows = c.fetchall()
    queryTitle="List of alphabetized member names with all available data"
    createResultsFrame(headerRow,rows,queryTitle)
    conn.close()

def executeQuery2():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    query1 = '''
    SELECT * FROM 'members_table' 
    WHERE DuesPaid LIKE '_____01%'
    AND ZipCode = "22101";
'''
    headerRow = [['Member#','LastName','FirstName','StreetAddress','City','State','ZipCode','Phone','FavoriteStore','DateJoined','DuesPaid']]
    c.execute(query1)
    rows = c.fetchall()
    queryTitle="List all members with zip code 22101 who have paid dues during January"
    createResultsFrame(headerRow,rows,queryTitle)
    conn.close()

def executeQuery3():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    query1 = '''
    SELECT * FROM 'members_table' 
    WHERE State = "VA"
    AND DateJoined >= "1999-07-01";
'''
    headerRow = [['Member#','LastName','FirstName','StreetAddress','City','State','ZipCode','Phone','FavoriteStore','DateJoined','DuesPaid']]
    c.execute(query1)
    rows = c.fetchall()
    queryTitle="List all members who have joined since 1999-07-01 and live in VA."
    createResultsFrame(headerRow,rows,queryTitle)
    conn.close()


def executeQuery4():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    query1 = '''
    SELECT LastName, FirstName, StoreName, Location
    FROM members_table
    INNER JOIN stores_table
    ON members_table.FavoriteStore = stores_table.StoreID;
'''
    headerRow = [['LastName','FirstName','StoreName','Location']]
    c.execute(query1)
    rows = c.fetchall()
    queryTitle="List the names of all members and the names of their favorite store and its location"
    createResultsFrame(headerRow,rows,queryTitle)
    conn.close()


def executeQuery5():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    query1 = '''
    SELECT LastName, FirstName
    FROM members_table
    WHERE members_table.FavoriteStore =
    (SELECT StoreID 
    FROM stores_table
    WHERE stores_table.StoreName = "Total Wine")
'''
    headerRow = [['LastName','FirstName']]
    c.execute(query1)
    rows = c.fetchall()
    queryTitle="List the names of  all members whose favorite store is Total Wine"
    createResultsFrame(headerRow,rows,queryTitle)
    conn.close()

def importData(frame):
    frame.tkraise(mainFrame)
    members_path_lbl = Label(frame, text = "Member data: ")
    members_path_entry = Entry(frame)
    stores_path_lbl = Label(frame, text = "Store data: ")
    stores_path_entry= Entry(frame)

    members_path_lbl.grid(column =0, row = 4)
    members_path_entry.grid(column = 1, row =4)
    stores_path_lbl.grid(column =0, row =5 )
    stores_path_entry.grid(column =1, row =5)

    submitpath_button = Button(frame, text="Submit", command = lambda: loadMembersAndStoreData(members_path_entry.get(), stores_path_entry.get(), frame))
    submitpath_button.grid(column = 0, row = 8)

def showDataImportForm():
    dataImportFrame = initializeFrame("Please enter absolute paths for Member and Store csv files")
    importData(dataImportFrame)

importData_button = Button(mainFrame, text="Import Data", command = showDataImportForm)
executeQuery1_button = Button(mainFrame, text = "Execute Query1", command=executeQuery1 )
executeQuery2_button = Button(mainFrame, text = "Execute Query2", command=executeQuery2 )
executeQuery3_button = Button(mainFrame, text = "Execute Query3", command=executeQuery3 )
executeQuery4_button = Button(mainFrame, text = "Execute Query4", command=executeQuery4 )
executeQuery5_button = Button(mainFrame, text = "Execute Query5", command=executeQuery5 )


importData_button.grid(column = 0, row =0)
executeQuery1_button.grid(column =0, row=1)
executeQuery2_button.grid(column =0, row=2)
executeQuery3_button.grid(column =0, row=3)
executeQuery4_button.grid(column =0, row=4)
executeQuery5_button.grid(column =0, row=5)

window.mainloop()

