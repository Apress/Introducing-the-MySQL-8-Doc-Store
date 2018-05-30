# Import the MySQL X module
import mysqlx
try:
    # Get a session with a URI
    mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
    # Check the connection
    if not mysqlx_session.is_open():
        print("Connection failed!")
        exit(1)
    # Get the animals schema.
    schema = mysqlx_session.get_schema("animals")
    # Try to create the table using a SQL string. It should throw an error
    # that it already exists.
    res = mysqlx_session.sql("CREATE TABLE animals.pets_sql ("
                             "`id` int auto_increment primary key, "
                             "`name` char(20), "
                             "`age` int, "
                             "`breed` char(20), "
                             "`type` char(12))").execute()
except Exception as ex:
    print("ERROR: {0}:{1}".format(*ex))
# Close the connection
mysqlx_session.close()