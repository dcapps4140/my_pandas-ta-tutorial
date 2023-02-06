import pyodbc

#Define your database connection string parameters
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database1 = 'Project_Loaded_Cost_Data'
database2 = 'SmallSites'
table_name = 'Sheet_1'
table_name_2 = ''
table_name_3 = ''
column_name = 'Symbol'
username = 'vscode'
password = 'development'

# Connect to the database Project_Loaded_Cost_Data and SmallSite
connS = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=' + server + ';'
                    'DATABASE=' + database1 + ';'
                    'UID=' + username + ';'
                    'PWD=' + password)

# Connect to the destination database
connD = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=' + server + ';'
                    'DATABASE=' + database2 + ';'
                    'UID=' + username + ';'
                    'PWD=' + password)

# Execute a query to select data from the source table
#cursor.execute("SELECT * FROM SourceDB.dbo.SourceTable")
srcTable = ('['+database1 +']' + '.[dbo].' + '[' + table_name +']')
cursor = connS.cursor()
cursor.execute("SELECT * FROM [Project_Loaded_Cost_Data].[dbo].[Sheet1]")
rows = cursor.fetchall()

# Insert data into the destination table
sql_insert_string_s = ("INSERT INTO [SmallSites].[dbo].[Sheet1] VALUES (?,?,?,?,?)")
dest_cursor = connD.cursor()
dest_cursor.fast_executemany = False
dest_cursor.executemany(sql_insert_string_s, rows)

# Commit the changes
connD.commit()

# Close the connections
cursor.close()
dest_cursor.close()
dest_cursor.close()
connD.close()
