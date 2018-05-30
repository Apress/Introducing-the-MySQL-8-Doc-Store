# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Get the collection.
pets = mysqlx_session.get_schema("animals").get_table("pets_sql")
# Do a select (find) on the table - find the dogs
res = pets.select().where("type = 'dog'").execute();
# Working with column properties
print("Get the data using column names as properties:")
for row in res.fetch_all():
    for col in res.columns:
        print(row.get_string(col.get_column_name())),
    print("")
# Working with column indexes
print("Get the data using column index by integer:")
for row in res.fetch_all():
    for i in range(0,len(res.columns)):
        print(row[i]),
    print("")
# Working with column names
print("Get the data using column index by name:")
for row in res.fetch_all():
    for col in res.columns:
        print(row[col.get_column_name()]),
    print("")
# Close the connection
mysqlx_session.close()
