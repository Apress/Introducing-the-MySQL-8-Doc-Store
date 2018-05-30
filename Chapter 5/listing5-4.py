# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Get the schema
schema = mysqlx_session.create_schema("test_schema")
# Create a new collection
pets = schema.create_collection("pets_json")
# Insert some documents
pets.add({'name': 'Violet', 'age': 6, 'breed':'dachshund', 'type':'dog'}).execute()
pets.add({'name': 'JonJon', 'age': 15, 'breed':'poodle', 'type':'dog'}).execute()
pets.add({'name': 'Mister', 'age': 4, 'breed':'siberian khatru', 'type':'cat'}).execute()
pets.add({'name': 'Spot', 'age': 7, 'breed':'koi', 'type':'fish'}).execute()
pets.add({'name': 'Charlie', 'age': 6, 'breed':'dachshund', 'type':'dog'}).execute()
# Fetch collection as Table
pets_tbl = schema.get_collection_as_table('pets_json')
# Now do a find operation to retrieve the inserted document
result = pets_tbl.select(["doc->'$.name'", "doc->'$.age'"]).execute()
record = result.fetch_one()
# Print the first row
print("Name : {0}, Age: {1}".format(record[0], record[1]))
# Drop the collection
schema.drop_collection("pets_json")
# Close the session
mysqlx_session.close()
