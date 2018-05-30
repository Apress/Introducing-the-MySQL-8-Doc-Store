#
# Introducing the MySQL 8 Document Store - Base
#
# This file contains the sample Python + Flask application for demonstrating
# how to build a simple relational database application. Thus, it relies on
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
# Utility functions
#
def flash_errors(form):
    for error in form.errors:
        flash("{0} : {1}".format(error, ",".join(form.errors[error])))
        
#
# Customized fields for skipping prevalidation
#
class NewSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

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

class AuthorForm(FlaskForm):
    authorid = HiddenField('AuthorId')
    firstname = TextField('First name', validators=[
            Required(message=REQUIRED.format("Firstname")),
            Length(min=1, max=64, message=RANGE.format("Firstname", 1, 64))
        ])
    lastname = TextField( 'Last name', validators=[
            Required(message=REQUIRED.format("Lastname")),
            Length(min=1, max=64, message=RANGE.format("Lastname", 1, 64))
        ])
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')

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
    authors = NewSelectMultipleField('Authors ',
                    validators=[Required(message=REQUIRED.format("Author"))])
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    new_note = TextAreaField('Add Note')

#
# Routing functions - the following defines the routing functions for the
# menu including the index or "home", book, author, and publisher.
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
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'author':
        if request.method == 'POST':
            return redirect('author')
        # Just list the authors
        columns = (
            '<td style="width:100px">Lastname</td>',
            '<td style="width:200px">Firstname</td>',
        )
        kind = 'author'
        # Here, we get all authors in the database
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
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    else:
        flash("Something is wrong!")
        return

#
# Author
#
# This page allows creating and editing author records.
#
@app.route('/author', methods=['GET', 'POST'])
@app.route('/author/<int:author_id>', methods=['GET', 'POST'])
def author(author_id=None):
    form = AuthorForm()
    if request.method == 'POST':
        pass
    return render_template("author.html", form=form)

#
# Publisher
#
# This page allows creating and editing publisher records.
#
@app.route('/publisher', methods=['GET', 'POST'])
@app.route('/publisher/<int:publisher_id>', methods=['GET', 'POST'])
def publisher(publisher_id=None):
    form = PublisherForm()
    if request.method == 'POST':
            pass
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
    form = BookForm()
    form.publisher.choices = []
    form.authors.choices = []
    new_note = ""
    if request.method == 'POST':
        pass
    return render_template("book.html", form=form, notes=notes)

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
