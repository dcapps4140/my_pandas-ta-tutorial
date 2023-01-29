'''
This code connects to the database using Pyodbc, creates a cursor object, and executes a DELETE query to delete 
records from the table_name where the column_name is either NULL or an empty string. Finally, the changes are 
committed to the database and the connection is closed.
'''
import pyodbc

#Define your database connection string parameters
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database = 'stocks'
table_name = 'StockSymbols'
column_name = 'Symbol'
username = 'vscode'
password = 'development'

# Connect to the database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=' + server + ';'
                    'DATABASE=' + database + ';'
                    'UID=' + username + ';'
                    'PWD=' + password)
cursor = conn.cursor()

# Create the SQL query to delete blank or null records
delete_sql = "DELETE FROM {} WHERE {} IS NULL OR {} = ''".format(table_name, column_name, column_name)

# Execute the query
cursor.execute(delete_sql)

# Commit the changes
conn.commit()

# Close the connection
conn.close()