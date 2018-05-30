# Import the MySQL X module
import mysqlx
# Get a session with a URI
mysqlx_session = mysqlx.get_session("root:secret@localhost:33060")
# Check the connection
if not mysqlx_session.is_open():
    print("Connection failed!")
    exit(1)
# Create a schema.
schema = mysqlx_session.create_schema("animals")
# Create a new table
mysqlx_session.sql("CREATE TABLE animals.pets_sql ("
            "`id` int auto_increment primary key, "
            "`name` char(20), "
            "`age` int, "
            "`breed` char(20), "
            "`type` char(12))").execute()
pets = schema.get_table("pets_sql", True)
# Insert some documents
pets.insert().values([None, 'Violet', 6, 'dachshund', 'dog']).execute()
pets.insert().values([None, 'JonJon', 15,'poodle', 'dog']).execute()
pets.insert().values([None, 'Mister', 4,'siberian khatru', 'cat']).execute()
pets.insert().values([None, 'Spot', 7,'koi', 'fish']).execute()
pets.insert().values([None, 'Charlie', 6,'dachshund', 'dog']).execute()
# Do a select (find) on the table - find el gato
mydoc = pets.select().where("type = 'cat'").execute();
print(", ".join("{0}".format(c.get_column_name()) for c in mydoc.columns))
print(", ".join("{0}".format(r) for r in mydoc.fetch_one()))
# Drop the collection 
mysqlx_session.drop_schema("animals")
# Close the connection
mysqlx_session.close()