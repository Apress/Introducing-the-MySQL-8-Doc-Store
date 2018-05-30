# Import the MySQL X module
import mysqlx
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
schema = mysqlx_session.get_schema("world_x")
# Collection.find() function with hardcoded values
myColl = schema.get_collection('countryinfo')
myRes1 = myColl.find("GNP >= 828").execute()
print(myRes1.fetch_one())
# Using the .bind() function to bind parameters
myRes2 = myColl.find('Name = :param1 and GNP = :param2').bind('param1','Aruba').bind('param2', '828').execute()
print(myRes2.fetch_one())
# Using named parameters
myColl.modify('Name = :param').set('GNP', '829').bind('param', 'Aruba').execute()
# Binding works for all CRUD statements except add()
myRes3 = myColl.find('Name LIKE :param').bind('param', 'Ar%').execute()
print(myRes3.fetch_one())
# Ok, now put the candle back...
myColl.modify('Name = :param').set('GNP', '828').bind('param', 'Aruba').execute()
# Close the connection
mysqlx_session.close()