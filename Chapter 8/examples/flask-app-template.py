#
# Introducing the MySQL 8 Document Store - Template
#
# This file contains a template for building Flask applications. No form
# classes, routes, or view functions are defined but placeholders for each
# are defined in the comments.
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
<custom field classes go here>

#
# Form classes - the forms for the application
#
<form classes go here>

#
# Routing functions - the following defines the routing functions for the
# menu including the index or "home", book, author, and publisher.
# 
<routing functions (view functions) go here>

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
