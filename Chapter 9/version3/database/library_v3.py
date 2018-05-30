#
# Introducing the MySQL 8 Document Store - Version 3
#
# This file contains classes that implement a document store model
# for the MyLibrary application. Included are the basic create, read,
# update, and delete methods for books.
#
# Additional functions are provided for connecting to and disconnecting
# from the MySQL server.
#
# Database name = library_v3
#
# Dr. Charles Bell, 2017
#
import mysqlx
from json import JSONEncoder as encoder

#
# Books collection simple abstraction (document store)
#
class Books(object):
    """Books class

    This class encapsulates the books collection permitting CRUD operations
    on the data.
    """
    def __init__(self):
        self.session = None
        self.book_schema = None
        self.book_col =  None

    def create(self, ISBN, Title, Pub_Year, Pub_Name, Pub_City, Pub_URL,
               Authors=[], Notes=[], Edition=1, Language='English'):
        assert ISBN, "You must supply an ISBN for a new book."
        assert Title, "You must supply Title for a new book."
        assert Pub_Year, "You must supply a Year for a new book."
        assert Pub_Name, "You must supply a Publisher Name for a new book."
        assert Authors, "You must supply at least one Author Name for a new book."
        last_id = None
        try:
            book_json = self.make_book_json(ISBN, Title, Pub_Year, Pub_Name,
                                            Pub_City, Pub_URL, Authors, Notes,
                                            Edition, Language)
            self.book_col.add(book_json).execute()
            last_id = self.book_col.find(
                "ISBN = '{0}'".format(ISBN)).execute().fetch_all()[0]["_id"]
        except Exception as err:
            print("ERROR: Cannot add book: {0}".format(err))
        return last_id

    def read(self, bookid=None):
        return self.book_col.find("_id = '{0}'".format(bookid)).execute().fetch_one()

    def update(self, book_id, book_data, ISBN, Title, Pub_Year, Pub_Name, Pub_City,
               Pub_URL, Authors=[], New_Note=None, Edition=1, Language='English'):
        assert book_id, "You must supply an book id to update the book."
        try:
            bkid = "_id = '{0}'".format(book_id)
            self.session.start_transaction()
            if ISBN != book_data["ISBN"]:
                self.book_col.modify(bkid).set("ISBN", ISBN).execute()
            if Title != book_data["Title"]:
                self.book_col.modify(bkid).set("Title", Title).execute()
            if Pub_Year != book_data["Pub_Year"]:
                self.book_col.modify(bkid).set("Pub_Year", Pub_Year).execute()
            if Pub_Name != book_data["Publisher"]["Name"]:
                self.book_col.modify(bkid).set("$.Publisher.Name", Pub_Name).execute()
            if Pub_City != book_data["Publisher"]["City"]:
                self.book_col.modify(bkid).set("$.Publisher.City", Pub_City).execute()
            if Pub_URL != book_data["Publisher"]["URL"]:
                self.book_col.modify(bkid).set("$.Publisher.URL", Pub_URL).execute()
            if Edition != book_data["Edition"]:
                self.book_col.modify(bkid).set("Edition", Edition).execute()
            if Language != book_data["Language"]:
                self.book_col.modify(bkid).set("Language", Language).execute()
            if New_Note:
                #
                # If this is the first note, we create the array otherwise,
                # we append to it.
                #
                if not "Notes" in book_data.keys():
                    mod_book = self.book_col.modify(bkid)
                    mod_book.set("Notes", [{"Text":New_Note}]).execute()
                else:
                    mod_book =  self.book_col.modify(bkid)
                    mod_book.array_append("Notes", {"Text":New_Note}).execute()
            if Authors and (Authors != self.make_authors_str(book_data['Authors'])):
                authors_json = self.make_authors_dict_list(Authors)
                self.book_col.modify(bkid).set("Authors", authors_json).execute()
            self.session.commit()
        except Exception as err:
            print("ERROR: Cannot update book: {0}".format(err))
            self.session.rollback()

    def delete(self, book_id):
        assert book_id, "You must supply a book id to delete the book."
        try:
            self.book_col.remove_one(book_id).execute()
        except Exception as err:
            print("ERROR: Cannot delete book: {0}".format(err))
            self.session.rollback()

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
            if self.session.is_open():
                self.book_schema = self.session.get_schema("library_v3")
                self.book_col = self.book_schema.get_collection("books")
        except Exception as err:
            print("CONNECTION ERROR:", err)
            self.session = None
            raise

    def make_authors_str(self, authors):
        author_str = ""
        num = len(authors)
        i = 0
        while (i < num):
            author_str += "{0} {1}".format(authors[i]["LastName"],
                                           authors[i]["FirstName"])
            i += 1
            if (i < num):
                author_str += ", "
        return author_str

    def make_authors_dict_list(self, author_list=None):
        if not author_list:
            return None
        author_dict_list = []
        authors = author_list.split(",")
        for author in authors:
            try:
                last, first = author.strip(' ').split(' ')
            except Exception as err:
                last = author.strip(' ')
                first = ''
            author_dict_list.append({"LastName":last,"FirstName":first})
        return author_dict_list

    def make_book_json(self, ISBN, Title, Pub_Year, Pub_Name, Pub_City, Pub_URL,
                       Authors=[], Notes=[], Edition=1, Language='English'):
        notes_list = []
        for note in Notes:
            notes_list.append({"Text":"{0}".format(note)})
        book_dict = {
            "ISBN": ISBN,
            "Title": Title,
            "Pub_Year": Pub_Year,
            "Edition": Edition,
            "Language": Language,
            "Authors": self.make_authors_dict_list(Authors),
            "Publisher": {
                "Name": Pub_Name,
                "City": Pub_City,
                "URL": Pub_URL,
            },
            "Notes": notes_list,
        }
        return encoder().encode(book_dict)

    #
    #  Build row array
    #
    def make_row_array(self, book_doc_list):
        rows = []
        for book in book_doc_list:
            book_dict = book
            # Now, we build the row for the book list
            row_item = (
                book_dict["_id"],
                book_dict["ISBN"],
                book_dict["Title"],
                book_dict["Publisher"]["Name"],
                book_dict["Pub_Year"],
                self.make_authors_str(book_dict["Authors"]),
            )
            rows.append(row_item)
        return rows

    #
    # Get list of books
    #
    def get_books(self):
        rows = []
        try:
            book_docs = self.book_col.find().sort("ISBN").execute().fetch_all();
            rows = self.make_row_array(book_docs)
        except Exception as err:
            print("ERROR: {0}".format(err))
            raise
        return rows
