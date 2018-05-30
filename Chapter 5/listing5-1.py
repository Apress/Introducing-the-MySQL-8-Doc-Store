# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Get an unknown schema
schema1 = mysqlx_session.get_schema("not_there!")
# Does it exist?
print("Does not_there! exist? {0}".format(schema1.exists_in_database()))
# Create the schema
schema = mysqlx_session.create_schema("test_schema")
# Does it exist?
print("Does test_schema exist? {0}".format(schema.exists_in_database()))
mysqlx_session.close()
