# This method checks the result for warnings and prints them
# if any exist.
#
# result[in]     result object
def process_warnings(result):
    if result.get_warnings_count():
        for warning in result.get_warnings():
            print("WARNING: Type {0} (Code {1}): {2}".format(*warning))
    else:
        print "No warnings were returned."

# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Get the animals schema.
schema = mysqlx_session.get_schema("animals")
# Try to create the table using a SQL string. It should throw a warning.
res = mysqlx_session.sql("CREATE TABLE IF NOT EXISTS animals.pets_sql ("
                         "`id` int auto_increment primary key, "
                         "`name` char(20), "
                         "`age` int, "
                         "`breed` char(20), "
                         "`type` char(12))").execute()
process_warnings(res)
# Close the connection
mysqlx_session.close()
