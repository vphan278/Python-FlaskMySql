#from flask import Flask, render_template, request, redirect, session
# import the class from friend.py
#from datetime import datetime
#from user import User

#from flask_app import app
#app = Flask(__name__)

from flask_app import app
from flask_app.controllers import users





if __name__ == "__main__":
    app.run(debug=True)

