'''
Flask Minimal Application - Reference for more advanced code
'''

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Can use this as reference for all projects going forward: https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application