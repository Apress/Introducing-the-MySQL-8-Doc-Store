# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysql_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysql_session.is_open():
    print("Connection failed!")
    exit(1)
# Create a schema.
schema = mysql_session.get_schema("animals")
# Create a new collection
pets = schema.get_collection("pets_json")
# Prepare a CRUD statement.
find_pet = pets.find("name = :param")
# Now execute the CRUD statement different ways.
mydoc = find_pet.bind('param', 'JonJon').execute()
print(mydoc.fetch_one())
mydoc = find_pet.bind('param', 'Charlie').execute()
print(mydoc.fetch_one())
mydoc = find_pet.bind('param', 'Spot').execute()
print(mydoc.fetch_one())
# Close the connection
mysql_session.close()
