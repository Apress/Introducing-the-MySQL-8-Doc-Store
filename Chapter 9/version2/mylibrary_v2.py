#
# Introducing the MySQL 8 Document Store - Version 2
#
# This file contains the sample Python + Flask application for demonstrating
# how to build a hybrid relational database application. Thus, it relies on
# a database class that encapsulates the CRUD operations for a MySQL database
# of relational tables.
#
# Dr. Charles Bell, 2017
#
from flask import Flask, render_template, request, redirect, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (HiddenField, TextField, TextAreaField, SelectField,
                     SelectMultipleField, IntegerField, SubmitField)
from wtforms.validators import Required, Length
from database.library_v2 import Library, Publisher, Book

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
# Setup the library database class
#
library = Library()
# Provide your user credentials here
library.connect(<user>, <password>, 'localhost', 33060)

#
# Utility functions
#
def flash_errors(form):
    for error in form.errors:
        flash("{0} : {1}".format(error, ",".join(form.errors[error])))

#
# Customized fields for skipping prevalidation
#
class NewSelectField(SelectField):
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

#
# Form classes - the forms for the application
#
class ListForm(FlaskForm):
    submit = SubmitField('New')

class PublisherForm(FlaskForm):
    publisherid = HiddenField('PublisherId')
    name = TextField('Name', validators=[
            Required(message=REQUIRED.format("Name")),
            Length(min=1, max=128, message=RANGE.format("Name", 1, 128))
        ])
    city = TextField('City', validators=[
            Required(message=REQUIRED.format("City")),
            Length(min=1, max=32, message=RANGE.format("City", 1, 32))
        ])
    url = TextField('URL/Website')
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')

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
    publisher = NewSelectField('Publisher ',
                    validators=[Required(message=REQUIRED.format("Publisher"))])
    authors = TextField('Authors (comma separated by LastName FirstName)',
                    validators=[Required(message=REQUIRED.format("Author"))])
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    new_note = TextAreaField('Add Note')

#
# Routing functions - the following defines the routing functions for the
# menu including the index or "home", book and publisher.
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
        rows = library.get_books()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'publisher':
        if request.method == 'POST':
            return redirect('publisher')
        columns = (
            '<td style="width:300px">Name</td>',
            '<td style="width:100px">City</td>',
            '<td style="width:300px">URL/Website</td>',
        )
        kind = 'publisher'
        # Here, we get all publishers in the database
        publisher = Publisher(library)
        rows = publisher.read()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    else:
        flash("Something is wrong!")
        return

#
# Publisher
#
# This page allows creating and editing publisher records.
#
@app.route('/publisher', methods=['GET', 'POST'])
@app.route('/publisher/<int:publisher_id>', methods=['GET', 'POST'])
def publisher(publisher_id=None):
    publisher = Publisher(library)
    form = PublisherForm()
    # Get data from the form if present
    form_publisherid = form.publisherid.data
    name = form.name.data
    city = form.city.data
    url = form.url.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if publisher_id:
        # Here, we get the data and populate the form
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = publisher.read(publisher_id)
        if data == []:
            flash("Publisher not found!")
        form.publisherid.data = data[0][0]
        form.name.data = data[0][1]
        form.city.data = data[0][2]
        form.url.data = data[0][3]
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
                    publisher.create(Name=name, City=city, URL=url)
                    flash("Added.")
                    return redirect('/list/publisher')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    publisher.update(PublisherId=form_publisherid, Name=name,
                                     City=city, URL=url)
                    flash("Updated.")
                    return redirect('/list/publisher')
                except Exception as err:
                    flash(err)
            else:
                try:
                    publisher.delete(form_publisherid)
                    flash("Deleted.")
                    return redirect('/list/publisher')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("publisher.html", form=form)

#
# Book
#
# This page allows creating and editing book records.
#
@app.route('/book', methods=['GET', 'POST'])
@app.route('/book/<string:isbn_selected>', methods=['GET', 'POST'])
def book(isbn_selected=None):
    notes = None
    book = Book(library)
    form = BookForm()
    # Get data from the form if present
    isbn = form.isbn.data
    title = form.title.data
    year = form.year.data
    author_list = form.authors.data
    publisherid = form.publisher.data
    edition = form.edition.data
    language = form.language.data
    #
    # Here, we get the choices for the select lists
    #
    publisher = Publisher(library)
    publishers = publisher.read()
    publisher_list = []
    for pub in publishers:
        publisher_list.append((pub[0], '{0}'.format(pub[1])))
    form.publisher.choices = publisher_list
    new_note = form.new_note.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if isbn_selected:
        # Here, we get the data and populate the form
        data = book.read(isbn_selected)
        if data == []:
            flash("Book not found!")

        #
        # Here, we populate the data
        #
        form.isbn.data = data[0][0]
        form.title.data = data[0][1]
        form.year.data = data[0][2]
        form.edition.data = data[0][3]
        form.publisher.process_data(data[0][4])
        form.language.data = data[0][5]
        form.authors.data = book.read_authors(isbn_selected)[0][0]

        # We also must retrieve the notes for the book.
        all_notes = book.read_notes(isbn_selected)
        notes = []
        for note in all_notes:
            notes.append(note[2])
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
                    book.create(ISBN=isbn, Title=title, Year=year,
                                PublisherId=publisherid, Authors=author_list,
                                Edition=edition, Language=language)
                    flash("Added.")
                    return redirect('/list/book')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    book.update(isbn_selected, isbn, Title=title, Year=year,
                                PublisherId=publisherid, Authors=author_list,
                                Edition=edition, Language=language,
                                Note=new_note)
                    flash("Updated.")
                    return redirect('/list/book')
                except Exception as err:
                    flash(err)
            else:
                try:
                    book.delete(isbn)
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
