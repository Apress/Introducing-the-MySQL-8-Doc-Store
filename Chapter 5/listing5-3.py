# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Get the schema
schema = mysqlx_session.create_schema("test_schema")
# Create a new collection
testCol = schema.create_collection('test_collection1', True)
# Create a new collection
testCol = schema.create_collection('test_collection2', True)
# Show the collections.
collections = schema.get_collections()
for col in collections:
    print(col.name)
mysqlx_session.close()
