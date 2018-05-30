#
# Introducing the MySQL 8 Document Store - Version 2
#
# This file contains classes that implement a hybrid relational database model
# for the MyLibrary application. Included are the basic create, read,
# update, and delete methods for books and publishers. 
#
# Additional functions are provided for connecting to and disconnecting
# from the MySQL server.
#
# Database name = library_v2
#
# Dr. Charles Bell, 2017
#
import mysqlx

#
# String constants
#
ALL_BOOKS = """
    SELECT DISTINCT book.ISBN, book.ISBN, Title, PublisherId, Year,
                    library_v2.get_author_names(book.ISBN) as Authors
    FROM library_v2.books As book
    ORDER BY book.ISBN DESC
"""

GET_PUBLISHER_NAME = """
    SELECT Name
    FROM library_v2.publishers
    WHERE PublisherId = {0}
"""

GET_LASTID = "SELECT @@last_insert_id"

#
# Publisher SQL Statements
#
INSERT_PUBLISHER = """
    INSERT INTO library_v2.publishers (Name, City, URL) VALUES ('{0}','{1}','{2}')
"""

GET_PUBLISHERS = "SELECT * FROM library_v2.publishers {0}"
UPDATE_PUBLISHER = "UPDATE library_v2.publishers SET Name = '{0}'"
DELETE_PUBLISHER = "DELETE FROM library_v2.publishers WHERE PublisherId = {0}"

#
# Book SQL Statements
#
INSERT_BOOK = """
    INSERT INTO library_v2.books (ISBN, Title, Year, PublisherId, Edition,
    Language, Authors) VALUES ('{0}','{1}','{2}','{3}',{4},'{5}','{6}')
"""

INSERT_NOTE = "INSERT INTO library_v2.notes (ISBN, Note) VALUES ('{0}','{1}')"
GET_BOOKS = "SELECT * FROM library_v2.books {0}"
GET_NOTES = "SELECT * FROM library_v2.notes WHERE ISBN = '{0}'"
GET_AUTHOR_NAMES = "SELECT library_v2.get_author_names('{0}')"
UPDATE_BOOK = "UPDATE library_v2.books SET ISBN = '{0}'"
DELETE_NOTES = "DELETE FROM library_v2.notes WHERE ISBN = '{0}'"
DELETE_BOOK = "DELETE FROM library_v2.books WHERE ISBN = '{0}'"

#
# Publishers table simple abstraction (relational database)
#
class Publisher(object):
    """Publisher class
    
    This class encapsulates the publishers table permitting CRUD operations
    on the data.
    """
    def __init__(self, library):
        self.library = library

    def create(self, Name, City=None, URL=None):
        assert Name, "You must supply a Name for a new publisher."
        query_str = INSERT_PUBLISHER
        last_id = None
        try:
            self.library.sql(query_str.format(Name, City, URL)).execute()
            last_id = self.library.make_rows(
                self.library.sql(GET_LASTID).execute())[0][0]
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot add publisher: {0}".format(err))
        return last_id
    
    def read(self, PublisherId=None):
        query_str = GET_PUBLISHERS
        if not PublisherId:
            # return all authors
            query_str = query_str.format("")
        else:
            # return specific author
            query_str = query_str.format(
                "WHERE PublisherId = '{0}'".format(PublisherId))
        sql_stmt = self.library.sql(query_str)
        return self.library.make_rows(sql_stmt.execute())           
        
    def update(self, PublisherId, Name, City=None, URL=None):
        assert PublisherId, "You must supply a publisher to update the author."
        query_str = UPDATE_PUBLISHER.format(Name)
        if City:
            query_str = query_str + ", City = '{0}'".format(City)
        if URL:
            query_str = query_str + ", URL = '{0}'".format(URL)
        query_str = query_str + " WHERE PublisherId = {0}".format(PublisherId)
        try:
            self.library.sql(query_str).execute()
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot update publisher: {0}".format(err))
    
    def delete(self, PublisherId):
        assert PublisherId, "You must supply a publisher to delete the publisher."
        query_str = DELETE_PUBLISHER.format(PublisherId)
        try:
            self.library.sql(query_str).execute()
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot delete publisher: {0}".format(err))
    

#
# Books table simple abstraction (relational database)
#
class Book(object):
    """Book class
    
    This class encapsulates the books table permitting CRUD operations
    on the data.
    """
    def __init__(self, library):
        self.library = library
        
    def make_authors_json(self, author_list=None):
        from json import JSONEncoder
        
        if not author_list:
            return None
        author_dict = {"authors":[]}
        authors = author_list.split(",")
        for author in authors:
            try:
                last, first = author.strip(' ').split(' ')
            except Exception as err:
                last = author.strip(' ')
                first = ''
            author_dict["authors"].append({"LastName":last,"FirstName":first})
        author_json = JSONEncoder().encode(author_dict)
        return author_json

    def create(self, ISBN, Title, Year, PublisherId, Authors=[], Edition=1,
               Language='English'):
        assert ISBN, "You must supply an ISBN for a new book."
        assert Title, "You must supply Title for a new book."
        assert Year, "You must supply a Year for a new book."
        assert PublisherId, "You must supply a publisher for a new book."
        assert Authors, "You must supply at least one Author for a new book."
        query_str = INSERT_BOOK
        last_id = ISBN
        try:
            author_json = self.make_authors_json(Authors)
            self.library.sql(query_str.format(ISBN, Title, Year, PublisherId,
                                              Edition, Language,
                                              author_json)).execute()
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot add book: {0}".format(err))
            self.library.sql("ROLLBACK").execute()
        return last_id
    
    def read(self, ISBN=None):
        query_str = GET_BOOKS
        if not ISBN:
            # return all authors
            query_str = query_str.format("")
        else:
            # return specific author
            query_str = query_str.format("WHERE ISBN = '{0}'".format(ISBN))
        sql_stmt = self.library.sql(query_str)
        return self.library.make_rows(sql_stmt.execute())           
    
    #
    # Get the notes for this book
    #
    def read_notes(self, ISBN):
        assert ISBN, "You must supply an ISBN to get the notes."
        query_str = GET_NOTES.format(ISBN)
        sql_stmt = self.library.sql(query_str)
        return self.library.make_rows(sql_stmt.execute())           
    
    #
    # Get the authors for this book
    #
    def read_authors(self, ISBN):
        assert ISBN, "You must supply an ISBN to get the list of author ids."
        query_str = GET_AUTHOR_NAMES.format(ISBN)
        sql_stmt = self.library.sql(query_str)
        return self.library.make_rows(sql_stmt.execute())           

    def update(self, old_isbn, ISBN, Title=None, Year=None, PublisherId=None,
               Authors=None, Edition=None, Language=None, Note=None):
        assert ISBN, "You must supply an ISBN to update the book."
        last_id = None
        #
        # Build the book update query
        #
        book_query_str = UPDATE_BOOK.format(ISBN)
        if Title:
            book_query_str += ", Title = '{0}'".format(Title)
        if Year:
            book_query_str += ", Year = {0}".format(Year)
        if PublisherId:
            book_query_str += ", PublisherId = {0}".format(PublisherId)
        if Edition:
            book_query_str += ", Edition = {0}".format(Edition)
        if Authors:
            author_json = self.make_authors_json(Authors)
            book_query_str += ", Authors = '{0}'".format(author_json) 
        book_query_str += " WHERE ISBN = '{0}'".format(old_isbn)
        #
        # We must do this as a transaction to ensure all tables are updated.
        #
        try:
            self.library.sql("START TRANSACTION").execute()
            self.library.sql(book_query_str).execute()
            if Note:
                self.add_note(ISBN, Note)
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot update book: {0}".format(err))
            self.library.sql("ROLLBACK").execute()
        return last_id

    def delete(self, ISBN):
        assert ISBN, "You must supply a ISBN to delete the book."
        #
        # Here, we must cascade delete the notes when we delete a book.
        # We must do this as a transaction to ensure all tables are updated.
        #
        try:
            self.library.sql("START TRANSACTION").execute()
            query_str = DELETE_NOTES.format(ISBN)
            self.library.sql(query_str).execute()
            query_str = DELETE_BOOK.format(ISBN)
            self.library.sql(query_str).execute()
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot delete book: {0}".format(err))
            self.library.sql("ROLLBACK").execute()

    #
    # Add a note for this book
    #
    def add_note(self, ISBN, Note):
        assert ISBN, "You must supply a ISBN to add a note for the book."
        assert Note, "You must supply text (Note) to add a note for the book."
        query_str = INSERT_NOTE.format(ISBN, Note)
        try:
            self.library.sql(query_str).execute()
            self.library.sql("COMMIT").execute()
        except Exception as err:
            print("ERROR: Cannot add note: {0}".format(err))

    
#
# Library database simple abstraction (relational database)
#
class Library(object):
    """Library master class
    
    Use this class to interface with the library database. It includes
    utility functions for connections to the server and returning a
    SQLStatement object.
    """
    def __init__(self):
        self.session = None
    
    #
    # Connect to a MySQL server at host, port
    #
    # Attempts to connect to the server as specified by the connection
    # parameters.
    # 
    def connect(self, username, passwd, host, port):
        config = {
            'user': username,
            'password': passwd,
            'host': host,
            'port': port,
        }
        try:
            self.session = mysqlx.get_session(**config)
        except Exception as err:
            print("CONNECTION ERROR:", err)
            self.session = None
            raise
            
    #
    # Return the session for use in other classes
    #
    def get_session(self):
        return self.session
    
    #
    # Check to see if connected to the server
    #
    def is_connected(self):
        return (self.session and (self.session.is_open()))
    
    #
    # Disconnect from the server
    #
    def disconnect(self):
        try:
            self.session.close()
        except:
            pass
        
    #
    # Get an SQLStatement object
    #
    def sql(self, query_str):
        return self.session.sql(query_str)
        
    #
    #  Build row array
    #
    #  Here, we cheat a bit and give an option to substitute the publisher name
    #  for publisher Id column.
    #
    def make_rows(self, sql_res, get_publisher=False):
        cols = []
        for col in sql_res.columns:
            cols.append(col.get_column_name())
        rows = []
        for row in sql_res.fetch_all():
            row_item = []
            for col in cols:
                if get_publisher and (col == 'PublisherId'):
                    query_str = GET_PUBLISHER_NAME.format(row.get_string(col))
                    name = self.session.sql(query_str).execute().fetch_one()[0]
                    row_item.append("{0}".format(name))
                else:                    
                    row_item.append("{0}".format(row.get_string(col)))
            rows.append(row_item)
        return rows
    
    #
    # Get list of books
    #
    def get_books(self):
        try:
            sql_stmt = self.sql(ALL_BOOKS)
            results = self.make_rows(sql_stmt.execute(), True) 
        except Exception as err:
            print("ERROR: {0}".format(err))
            raise
        return results
    