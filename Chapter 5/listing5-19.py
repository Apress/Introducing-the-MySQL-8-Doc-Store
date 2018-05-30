# Import the MySQL X module
import mysqlx
import getpass
# Get a session with a URI
mysqlx_session = None
try: 
    mysqlx_session = mysqlx.get_session("root:wrongpassworddude!@localhost:33060")
except mysqlx.errors.InterfaceError as ex:
    print("ERROR: {0} : {1}".format(*ex))
    passwd = getpass.getpass("Wrong password, try again: ")    
finally:
    mysqlx_session = mysqlx.get_session("root:{0}@localhost:33060".format(passwd))
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Demostrate error from get_schema()
schema = mysqlx_session.get_schema("animal")
if (not schema.exists_in_database()):
    print("Schema 'animal' doesn't exist.")
# Get the animals schema.
schema = mysqlx_session.get_schema("animals")
try:
    # Try to create the table using a SQL string. It should throw an
    # error that it already exists.
    res = mysqlx_session.sql("CREATE TABLE animals.pets_sql ("
                      "`id` int auto_increment primary key, "
                      "`name` char(20), "
                      "`age` int, "
                      "`breed` char(20), "
                      "`type` char(12))").execute()
except mysqlx.errors.OperationalError as ex:
    print("ERROR: {0} : {1}".format(*ex))
# Close the connection
if mysqlx_session:
    mysqlx_session.close()