# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
res = mysqlx_session.sql("SELECT name as pet_name, age as years_young FROM animals.pets_sql").execute()
cols = res.columns
for col in cols:
    print "name =", col.get_column_name(), "label =", col.get_column_label()
mysqlx_session.close()
