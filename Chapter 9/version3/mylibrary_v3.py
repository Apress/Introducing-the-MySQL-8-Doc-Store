#
# Introducing the MySQL 8 Document Store - Version 3
#
# This file contains the sample Python + Flask application for demonstrating
# how to build a document store application. Thus, it relies on a document
# class that encapsulates the CRUD operations for a MySQL collection.
#
# Dr. Charles Bell, 2017
#
from flask import Flask, render_template, request, redirect, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (HiddenField, TextField, TextAreaField,
                     IntegerField, SubmitField)
from wtforms.validators import Required, Length
from database.library_v3 import Books

#
# Strings
#
REQUIRED = "{0} field is required."
RANGE = "{0} range is {1} to {2} characters."

#
# Setup Flask, Bootstrap, and security.
#
app = Flask(__name__)
app.config['SECRET_KEY'] = "He says, he's already got one!"
manager = Manager(app)
bootstrap = Bootstrap(app)

#
# Setup the books document store class
#
books = Books()
# Provide your user credentials here
books.connect('root','root', 'localhost', 33060)

#
# Utility functions
#
def flash_errors(form):
    for error in form.errors:
        flash("{0} : {1}".format(error, ",".join(form.errors[error])))

#
# Form classes - the forms for the application
#
class ListForm(FlaskForm):
    submit = SubmitField('New')

class BookForm(FlaskForm):
    isbn = TextField('ISBN ', validators=[
            Required(message=REQUIRED.format("ISBN")),
            Length(min=1, max=32, message=RANGE.format("ISBN", 1, 32))
        ])
    title = TextField('Title ',
                      validators=[Required(message=REQUIRED.format("Title"))])
    year = IntegerField('Year ',
                        validators=[Required(message=REQUIRED.format("Year"))])
    edition = IntegerField('Edition ')
    language = TextField('Language ', validators=[
            Required(message=REQUIRED.format("Language")),
            Length(min=1, max=24, message=RANGE.format("Language", 1, 24))
        ])
    pub_name = TextField('Publisher Name', validators=[
            Required(message=REQUIRED.format("Name")),
            Length(min=1, max=128, message=RANGE.format("Name", 1, 128))
        ])
    pub_city = TextField('Publisher City', validators=[
            Required(message=REQUIRED.format("City")),
            Length(min=1, max=32, message=RANGE.format("City", 1, 32))
        ])
    pub_url = TextField('Publisher URL/Website')
    authors = TextField('Authors (comma separated by LastName FirstName)',
                        validators=[Required(message=REQUIRED.format("Author"))])
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    new_note = TextAreaField('Add Note')
    # Here, we book id for faster updates
    book_id = HiddenField("BookId")
    # Here, we store the book data structure (document)
    book_dict = HiddenField("BookData")

#
# Routing functions - the following defines the routing functions for the menu.
#

#
# Simple List
#
# This is the default page for "home" and listing objects. It reuses a single
# template "list.html" to show a list of rows from the database. Built into
# each row is a special edit link for editing any of the rows, which redirects
# to the appropriate route (form).
#
@app.route('/', methods=['GET', 'POST'])
@app.route('/list/<kind>', methods=['GET', 'POST'])
def simple_list(kind=None):
    rows = []
    columns = []
    form = ListForm()
    if kind == 'book' or not kind:
        if request.method == 'POST':
            return redirect('book')
        columns = ('ISBN','Title','Publisher','Year','Authors')
        columns = (
            '<td style="width:200px">ISBN</td>',
            '<td style="width:400px">Title</td>',
            '<td style="width:200px">Publisher</td>',
            '<td style="width:80px">Year</td>',
            '<td style="width:300px">Authors</td>',
        )
        kind = 'book'
        # Here, we get all books in the database
        rows = books.get_books()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    else:
        flash("Something is wrong!")
        return

#
# Book
#
# This page allows creating and editing book documents.
#
@app.route('/book', methods=['GET', 'POST'])
@app.route('/book/<string:id_selected>', methods=['GET', 'POST'])
def book(id_selected=None):
    notes = []
    form = BookForm()
    # Get data from the form if present
    bookid = form.book_id.data
    isbn = form.isbn.data
    title = form.title.data
    year = form.year.data
    author_list = form.authors.data
    pub_name = form.pub_name.data
    pub_city = form.pub_city.data
    pub_url = form.pub_url.data
    edition = form.edition.data
    language = form.language.data
    new_note = form.new_note.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if id_selected:
        # Here, we get the data and populate the form
        data = books.read(id_selected)
        if data == []:
            flash("Book not found!")

        #
        # Here, we populate the data
        #
        form.book_dict.data = data;
        form.book_id.data = data["_id"]
        form.isbn.data = data["ISBN"]
        form.title.data = data["Title"]
        form.year.data = data["Pub_Year"]
        #
        # Since edition is optional, we must check for it first.
        #
        if "Edition" in data.keys():
            form.edition.data = data["Edition"]
        else:
            form.edition.data = '1'
        form.pub_name.data = data["Publisher"]["Name"]
        #
        # Since publisher city is optional, we must check for it first.
        #
        if "City" in data["Publisher"].keys():
            form.pub_city.data = data["Publisher"]["City"]
        else:
            form.pub_city = ""
        #
        # Since publisher URL is optional, we must check for it first.
        #
        if "URL" in data["Publisher"].keys():
            form.pub_url.data = data["Publisher"]["URL"]
        else:
            form.pub_url.data = ""
        #
        # Since language is optional, we must check for it first.
        #
        if "Language" in data.keys():
            form.language.data = data["Language"]
        else:
            form.language.data = "English"
        form.authors.data = books.make_authors_str(data["Authors"])

        # We also must retrieve the notes for the book.
        if "Notes" in data.keys():
            all_notes = data["Notes"]
        else:
            all_notes = []
        notes = []
        for note in all_notes:
            notes.append(note["Text"])
        form.create_button.label.text = "Update"
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    books.create(ISBN=isbn, Title=title, Pub_Year=year,
                                 Pub_Name=pub_name, Pub_City=pub_city,
                                 Pub_URL=pub_url, Authors=author_list,
                                 Notes=notes, Edition=edition,
                                 Language=language)
                    flash("Added.")
                    return redirect('/list/book')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    books.update(id_selected, form.book_dict.data, ISBN=isbn,
                                 Title=title, Pub_Year=year, Pub_Name=pub_name,
                                 Pub_City=pub_city, Pub_URL=pub_url,
                                 Authors=author_list, Edition=edition,
                                 Language=language, New_Note=new_note)
                    flash("Updated.")
                    return redirect('/list/book')
                except Exception as err:
                    flash(err)
            else:
                try:
                    books.delete(form.book_id.data)
                    flash("Deleted.")
                    return redirect('/list/book')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("book.html", form=form, notes=notes,
                           authors=author_list)

#
# Error handling routes
#
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#
# Main entry
#
if __name__ == '__main__':
    manager.run()
