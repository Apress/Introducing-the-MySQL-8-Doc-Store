#
# Introducing the MySQL 8 Document Store - Version 1
#
# This file contains classes that implement a relational database model
# for the MyLibrary application. Included are the basic create, read,
# update, and delete methods for books, authors, and publishers. 
#
# Additional functions are provided for connecting to and disconnecting
# from the MySQL server.
#
# Database name = library_v1
#
# Dr. Charles Bell, 2017
#
import mysql.connector

#
# String constants
#
ALL_BOOKS = """
    SELECT DISTINCT book.ISBN, book.ISBN, Title, publisher.Name as Publisher,
                    Year, library_v1.get_author_names(book.ISBN) as Authors
    FROM library_v1.books As book
        INNER JOIN library_v1.publishers as publisher ON
                   book.PublisherId=publisher.PublisherId
        INNER JOIN library_v1.books_authors as book_author ON
                   book.ISBN = book_author.ISBN
        INNER JOIN library_v1.authors as a ON book_author.AuthorId = a.AuthorId
    ORDER BY book.ISBN DESC
"""

GET_LASTID = "SELECT @@last_insert_id"

#
# Author SQL Statements
#
INSERT_AUTHOR = """
    INSERT INTO library_v1.authors (LastName, FirstName) VALUES ('{0}','{1}')
"""

GET_AUTHORS = "SELECT * FROM library_v1.authors {0}"
UPDATE_AUTHOR = """
    UPDATE library_v1.authors SET LastName = '{0}', 
    FirstName='{1}' WHERE AuthorId = {2}
"""

DELETE_AUTHOR = """
    DELETE FROM library_v1.authors WHERE AuthorId = {0}
"""

#
# Publisher SQL Statements
# 
INSERT_PUBLISHER = """
    INSERT INTO library_v1.publishers (Name, City, URL) VALUES ('{0}','{1}','{2}')
"""

GET_PUBLISHERS = "SELECT * FROM library_v1.publishers {0}"
UPDATE_PUBLISHER = "UPDATE library_v1.publishers SET Name = '{0}'"
DELETE_PUBLISHER = "DELETE FROM library_v1.publishers WHERE PublisherId = {0}"

#
# Book SQL Statements
#
INSERT_BOOK = """
    INSERT INTO library_v1.books (ISBN, Title, Year, PublisherId, Edition,
    Language) VALUES ('{0}','{1}','{2}','{3}',{4},'{5}')
"""

INSERT_BOOK_AUTHOR = """
    INSERT INTO library_v1.books_authors (ISBN, AuthorId) VALUES ('{0}', {1})
"""

INSERT_NOTE = "INSERT INTO library_v1.notes (ISBN, Note) VALUES ('{0}','{1}')"
GET_BOOKS = "SELECT * FROM library_v1.books {0}"
GET_NOTES = "SELECT * FROM library_v1.notes WHERE ISBN = '{0}'"
GET_AUTHOR_IDS = "SELECT library_v1.get_author_ids('{0}')"
UPDATE_BOOK = "UPDATE library_v1.books SET ISBN = '{0}'"
DELETE_BOOK = "DELETE FROM library_v1.books WHERE ISBN = '{0}'"
DELETE_BOOK_AUTHOR = "DELETE FROM library_v1.books_authors WHERE ISBN = '{0}'"
DELETE_NOTES = "DELETE FROM library_v1.notes WHERE ISBN = '{0}'"


#
# Authors table simple abstraction (relational database)
#
class Author(object):
    """Author class
    
    This class encapsulates the authors table permitting CRUD operations
    on the data.
    """
    def __init__(self, library):
        self.library = library

    def create(self, LastName, FirstName):
        assert LastName, "You must supply a LastName for a new author."
        assert FirstName, "You must supply a FirstName for a new author."
        query_str = INSERT_AUTHOR
        last_id = None
        try:
            self.library.sql(query_str.format(LastName, FirstName))
            last_id = self.library.sql(GET_LASTID)
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot add author: {0}".format(err))
        return last_id
    
    def read(self, AuthorId=None):
        query_str = GET_AUTHORS
        if not AuthorId:
            # return all authors
            query_str = query_str.format("")
        else:
            # return specific author
            query_str = query_str.format("WHERE AuthorId = '{0}'".format(AuthorId))
        return self.library.sql(query_str)            
        
    def update(self, AuthorId, LastName, FirstName):
        assert AuthorId, "You must supply an AuthorId to update the author."
        assert LastName, "You must supply a LastName for the author."
        assert FirstName, "You must supply a FirstName for the author."
        query_str = UPDATE_AUTHOR
        try:
            self.library.sql(query_str.format(LastName, FirstName, AuthorId))
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot update author: {0}".format(err))
    
    def delete(self, AuthorId):
        assert AuthorId, "You must supply an AuthorId to delete the author."
        query_str = DELETE_AUTHOR.format(AuthorId)
        try:
            self.library.sql(query_str)
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot delete author: {0}".format(err))


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
            self.library.sql(query_str.format(Name, City, URL))
            last_id = self.library.sql(GET_LASTID)
            self.library.sql("COMMIT")
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
        return self.library.sql(query_str)            
        
    def update(self, PublisherId, Name, City=None, URL=None):
        assert PublisherId, "You must supply a publisher to update the author."
        query_str = UPDATE_PUBLISHER.format(Name)
        if City:
            query_str = query_str + ", City = '{0}'".format(City)
        if URL:
            query_str = query_str + ", URL = '{0}'".format(URL)
        query_str = query_str + " WHERE PublisherId = {0}".format(PublisherId)
        try:
            self.library.sql(query_str)
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot update publisher: {0}".format(err))
    
    def delete(self, PublisherId):
        assert PublisherId, "You must supply a publisher to delete the publisher."
        query_str = DELETE_PUBLISHER.format(PublisherId)
        try:
            self.library.sql(query_str)
            self.library.sql("COMMIT")
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

    def create(self, ISBN, Title, Year, PublisherId, Authors=[], Edition=1,
               Language='English'):
        assert ISBN, "You must supply an ISBN for a new book."
        assert Title, "You must supply Title for a new book."
        assert Year, "You must supply a Year for a new book."
        assert PublisherId, "You must supply a PublisherId for a new book."
        assert Authors, "You must supply at least one AuthorId for a new book."
        last_id = ISBN
        #
        # We must do this as a transaction to ensure all tables are updated.
        #
        try:
            self.library.sql("START TRANSACTION")
            query_str = INSERT_BOOK.format(ISBN, Title, Year, PublisherId,
                                           Edition, Language)
            self.library.sql(query_str)
            query_str = INSERT_BOOK_AUTHOR
            for AuthorId in Authors.split(","):
                self.library.sql(query_str.format(ISBN, AuthorId))
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot add book: {0}".format(err))
            self.library.sql("ROLLBACK")
        return last_id
    
    def read(self, ISBN=None):
        query_str = GET_BOOKS
        if not ISBN:
            # return all authors
            query_str = query_str.format("")
        else:
            # return specific author
            query_str = query_str.format("WHERE ISBN = '{0}'".format(ISBN))
        return self.library.sql(query_str)
    
    #
    # Get the notes for this book
    #
    def read_notes(self, ISBN):
        assert ISBN, "You must supply an ISBN to get the notes."
        query_str = GET_NOTES.format(ISBN)
        return self.library.sql(query_str)
    
    #
    # Get the author ids for this book
    #
    def read_author_ids(self, ISBN):
        assert ISBN, "You must supply an ISBN to get the list of author ids."
        query_str = GET_AUTHOR_IDS.format(ISBN)
        return self.library.sql(query_str)

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
        book_query_str += " WHERE ISBN = '{0}'".format(old_isbn)
        #
        # We must do this as a transaction to ensure all tables are updated.
        #
        try:
            self.library.sql("START TRANSACTION")
            #
            # If the ISBN changes, we must remove the author ids first to
            # avoid the foreign key constraint error.
            #
            if old_isbn != ISBN:
                self.library.sql(DELETE_BOOK_AUTHOR.format(old_isbn))
            self.library.sql(book_query_str)
            last_id = self.library.sql(GET_LASTID)
            if Authors:
                # First, clear the author list.
                self.library.sql(DELETE_BOOK_AUTHOR.format(ISBN))
                query_str = INSERT_BOOK_AUTHOR
                for AuthorId in Authors:
                    self.library.sql(query_str.format(ISBN,AuthorId))
            if Note:
                self.add_note(ISBN, Note)
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot update book: {0}".format(err))
            self.library.sql("ROLLBACK")
        return last_id

    def delete(self, ISBN):
        assert ISBN, "You must supply a ISBN to delete the book."
        #
        # Here, we must cascade delete the notes when we delete a book.
        # We must do this as a transaction to ensure all tables are updated.
        #
        try:
            self.library.sql("START TRANSACTION")
            query_str = DELETE_NOTES.format(ISBN)
            self.library.sql(query_str)
            query_str = DELETE_BOOK_AUTHOR.format(ISBN)
            self.library.sql(query_str)
            query_str = DELETE_BOOK.format(ISBN)
            self.library.sql(query_str)
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot delete book: {0}".format(err))
            self.library.sql("ROLLBACK")

    #
    # Add a note for this book
    #
    def add_note(self, ISBN, Note):
        assert ISBN, "You must supply a ISBN to add a note for the book."
        assert Note, "You must supply text (Note) to add a note for the book."
        query_str = INSERT_NOTE.format(ISBN, Note)
        try:
            self.library.sql(query_str)
            self.library.sql("COMMIT")
        except Exception as err:
            print("ERROR: Cannot add publisher: {0}".format(err))
    
    
#
# Library database simple abstraction (relational database)
#
class Library(object):
    """Library master class
    
    Use this class to interface with the library database. It includes
    utility functions for connections to the server as well as running
    queries.
    """
    def __init__(self):
        self.db_conn = None
    
    #
    # Utility functions
    # 
        
    #
    # Connect to a MySQL server at host, port
    #
    # Attempts to connect to the server as specified by the connection
    # parameters.
    # 
    def connect(self, username, passwd, host, port, db=None):
        config = {
            'user': username,
            'password': passwd,
            'host': host,
            'port': port,
            'database': db,
        }
        try:
            self.db_conn = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            print("CONNECTION ERROR:", err)
            self.db_conn = None
            raise
            
    #
    # Return the connection for use in other classes
    #
    def get_connection(self):
        return self.db_conn
    
    #
    # Check to see if connected to the server
    #
    def is_connected(self):
        return (self.db_conn and (self.db_conn.is_connected()))
    
    #
    # Disconnect from the server
    #
    def disconnect(self):
        try:
            self.db_conn.disconnect()
        except:
            pass

    #
    # Execute a query and return any results
    #
    # query_str[in]      The query to execute
    # fetch          Execute the fetch as part of the operation and
    #                use a buffered cursor (default is True)
    # buffered       If True, use a buffered raw cursor (default is False)
    #
    # Returns result set or cursor
    # 
    def sql(self, query_str, fetch=True, buffered=False):
        # If we are fetching all, we need to use a buffered
        if fetch:
            cur = self.db_conn.cursor(buffered=True)
        else:
            cur = self.db_conn.cursor(raw=True)

        try:
            cur.execute(query_str)
        except Exception as err:
            cur.close()
            print("Query error. Command: {0}:{1}".format(query_str, err))
            raise

        # Fetch rows (only if available or fetch = True).
        if cur.with_rows:
            if fetch:
                try:
                    results = cur.fetchall()
                except mysql.connector.Error as err:
                    print("Error fetching all query data: {0}".format(err))
                    raise
                finally:
                    cur.close()
                return results
            else:
                # Return cursor to fetch rows elsewhere (fetch = false).
                return cur
        else:
            return cur

    #
    # Get list of books
    #
    def get_books(self):
        try:
            results = self.sql(ALL_BOOKS)
        except Exception as err:
            print("ERROR: {0}".format(err))
            raise
        return results
    