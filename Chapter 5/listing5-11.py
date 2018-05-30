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
# Do a find on the collection - find the fish
find = pets.find("type = 'dog'").execute()
res = find.fetch_one()
while (res):
    print("Get the data item as a string: {0}".format(res))
    print("Get the data elements: {0}, {1}, {2}".format(res.name, res.age, res['breed']))
    res = find.fetch_one()
# Close the connection
mysqlx_session.close()
