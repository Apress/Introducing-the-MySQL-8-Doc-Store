#
# Introducing the MySQL 8 Document Store - xclient_sql
#
# This file contains and example of how to read a database (SQL) from a MySQL
# server using the X Protocol via a Session object
#
# Dr. Charles Bell, 2017
#
import getpass
import mysqlx

# Get user information
print("Please enter the connection information.")
user = raw_input("Username: ")
passwd = getpass.getpass("Password: ")
host =  raw_input("Hostname [localhost]: ") or 'localhost'
port = raw_input("Port [33060]: ") or '33060'

# Get a session object since we want to execute SQL statements
mysqlx_session = mysqlx.get_session({'host': host, 'port': port, 'user': user, 'password': passwd})

# Check to see that the session is open. If not, quit.
if not mysqlx_session.is_open():
    exit(1)

# Get an SqlStatements object
sql_stmt = mysqlx_session.sql("SHOW VARIABLES LIKE 'mysqlx_%'")

# Execute and get a SqlResult object
sql_result = sql_stmt.execute()

print("\nVariables for the X Plugin:")
# Print the column labels (names)
for col in sql_result.columns:
    print("{0}\t".format(col.get_column_name())),
print("\n-------------------------------------------")

# Print the rows
for row in sql_result.fetch_all():
    for col in row:
        print("{0}\t".format(col)),
    print("")

# Close the session
mysqlx_session.close()
