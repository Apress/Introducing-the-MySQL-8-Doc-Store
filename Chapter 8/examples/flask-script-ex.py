from flask import Flask          # import the Flask framework
from flask_script import Manager # import the flask script manager class

app = Flask(__name__)            # initialize the application
manager = Manager(app)           # initialize the script manager class 

# Sample method linked as a command-line option
@manager.command
def hello_world():
    """Print 'Hello, world!'"""
    print("Hello, world!")

if __name__ == "__main__":       # guard for running the code
    manager.run()                # launch the application via manager class
