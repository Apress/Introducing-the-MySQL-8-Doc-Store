# Import the MySQL X module
import mysqlx
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Get the table
city = mysqlx_session.get_schema("world_x").get_table("city")
# Perform a complex select
res = city.select(['Name', 'District']).where("Name LIKE :param1").order_by(["District", "Name"]).bind('param1', 'X%').limit(1).execute()
# Show results
print("SQL result ="),
for row in res.fetch_all():
    for i in range(0,len(res.columns)):
       print("{0}".format(row[i])), 
print("")
# Close the connection
mysqlx_session.close()


