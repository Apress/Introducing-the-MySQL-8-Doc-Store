#
# Introducing the MySQL 8 Document Store - xclient_json
#
# This file contains and example of how to read a collection from a MySQL
# server using the X Protocol via a Session object
#
# Dr. Charles Bell, 2017
#
import getpass
import mysqlx

# Declarations
TEST_SCHEMA = "rolodex"
TEST_COL = "contacts"

# Get user information
print("Please enter the connection information.")
user = raw_input("Username: ")
passwd = getpass.getpass("Password: ")
host = raw_input("Hostname [localhost]: ") or 'localhost'
port = raw_input("Port [33060]: ") or '33060'

# Get a session object using a dictionary of terms
mysqlx_session = mysqlx.get_session({'host': host, 'port': port, 'user': user, 'password': passwd})

# Check to see that the session is open. If not, quit.
if not mysqlx_session.is_open():
    exit(1)

# Get the schema and create it if it doesn't exist
schema = mysqlx_session.get_schema(TEST_SCHEMA)
if not schema.exists_in_database():
    schema = mysqlx_session.create_schema(TEST_SCHEMA)

# Create a collection or use it if it already exists
contacts = schema.create_collection(TEST_COL)

# Empty the collection
contacts.remove()

# Insert data with inline JSON
contacts.add({"name": {"first": "Allen"},
              "phones": [{"work": "212-555-1212"}]}).execute()
contacts.add({"name": {"first": "Joe", "last": "Wheelerton"},
              "phones": [{"work": "212-555-1213"}, {"home": "212-555-1253"}],
              "address": {"street": "123 main", "city": "oxnard", "state": "ca", "zip": "90125"},
              "notes": "Excellent car detailer. Referrals get $20 off next detail!"}).execute()

# Get all of the data
doc_results = contacts.find().execute()

# Show the results
print("\nList of Phone Numbers")
document = doc_results.fetch_one()
while document:
    print("{0}:\t".format(document.name['first'])),
    for phone in document.phones:
        for key, value in phone.iteritems():
            print("({0}) {1}".format(key, value)),
    print("")
    document = doc_results.fetch_one()

# Drop the collection
schema.drop_collection(TEST_COL)

# Drop the schema
mysqlx_session.drop_schema(TEST_SCHEMA)

# Close the session
mysqlx_session.close()
