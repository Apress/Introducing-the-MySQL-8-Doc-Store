# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Get the collection.
pets = mysqlx_session.get_schema("animals").get_collection("pets_json")
# Do a find on the collection - find the fish with an expression string and parameter binding
fish_type = 'fish'
mydoc = pets.find("type = :mytype").bind('mytype', fish_type).execute();
print(mydoc.fetch_one())
# Close the connection
mysqlx_session.close()
