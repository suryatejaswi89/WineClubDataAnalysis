import csv
import sqlite3
import os.path

conn = sqlite3.connect('members.db')
c = conn.cursor()

current_dir_path = os.path.abspath(os.path.dirname(__file__))
membersDataFilePath = os.path.join(current_dir_path, "data/members.csv")
storesDataFilePath = os.path.join(current_dir_path, "data/stores.csv")

f1 = csv.reader(open(membersDataFilePath))
f2 = csv.reader(open(storesDataFilePath))

header1 = f1.next()
header2 = f2.next()

#print(header)

#Create store_table
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
    query1 = "INSERT INTO stores_table('StoreId','StoreName','Location')"+(" VALUES (%s)" % commaSeparatedVals)

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

    #query1 = "INSERT INTO stores_table('StoreId','StoreName','Location')"+(" VALUES (%s)" % commaSeparatedVals)
    query2 = "INSERT INTO members_table ('Member#','LastName','FirstName','StreetAddress','City','State','ZipCode','Phone','FavoriteStore','DateJoined','DuesPaid')" + (" VALUES (%s)" % commaSeparatedVals)



    c.execute(query2)

# Save (commit) the changes





conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()





