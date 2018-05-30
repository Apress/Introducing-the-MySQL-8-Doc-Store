# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Get the collection.
pets_json = mysqlx_session.get_schema("animals").get_collection("pets_json")
# Get the table.
pets_sql = mysqlx_session.get_schema("animals").get_table("pets_sql")
res = pets_sql.select().where("type = 'dog'").limit(1).execute();
print("SQL result ="),
for row in res.fetch_all():
    for i in range(0,len(res.columns)):
       print("{0}".format(row[i])), 
print("")
mydoc = pets_json.find("type = 'fish'").execute();
print("JSON result = {0}".format(mydoc.fetch_one()))
# Close the connection
mysqlx_session.close()
