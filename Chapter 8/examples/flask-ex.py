from flask import Flask      # import the Flask framework
app = Flask(__name__)        # initialize the application
if __name__ == "__main__":   # guard for running the code
    app.run()                # launch the application
