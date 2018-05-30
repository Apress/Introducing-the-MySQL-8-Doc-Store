# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Create a schema.
schema = mysqlx_session.create_schema("animals")
# Create a new collection
pets = schema.create_collection("pets_json", True)
# Insert some documents
pets.add({'name': 'Violet', 'age': 6, 'breed':'dachshund', 'type':'dog'}).execute()
pets.add({'name': 'JonJon', 'age': 15, 'breed':'poodle', 'type':'dog'}).execute()
pets.add({'name': 'Mister', 'age': 4, 'breed':'siberian khatru', 'type':'cat'}).execute()
pets.add({'name': 'Spot', 'age': 7, 'breed':'koi', 'type':'fish'}).execute()
pets.add({'name': 'Charlie', 'age': 6, 'breed':'dachshund', 'type':'dog'}).execute()
# Do a find on the collection - find the fish
find = pets.find("type = 'fish'")
filterable = find.fields(['name','type'])
mydoc = filterable.execute();
print(mydoc.fetch_one())
# Drop the collection
mysqlx_session.drop_schema("animals")
# Close the connection
mysqlx_session.close()