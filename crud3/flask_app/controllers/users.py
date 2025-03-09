from flask import Flask, render_template, request, redirect, session
# import the class from friend.py
from datetime import datetime
from flask_app.models.user import User
#from mysqlconnection import connect_to_mysql
from flask_app import app
#app = Flask(__name__)


@app.route("/")
def index():
    # call the get all classmethod to get all friends
    #friends = Friend.get_all()
    #print(friends)
    return render_template("index.html")
            

# relevant code snippet from server.py

@app.route('/create_user', methods=["POST"])
def create_friend():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/show')

@app.route("/show")
def show():
    users = User.get_all()
    return render_template("users.html", users = users)


@app.route("/users/<int:user_id>/show")
def show_one(user_id):
    users = User.get_one(user_id)
    return render_template("show.html", users = users)


@app.route("/user/<user_id>/delete")
def delete(user_id):
    User.delete(user_id)
    return redirect("/show")



@app.route('/users/<int:user_id>/edit', methods=["GET","POST"])
def edit(user_id):
    Users = User.get_one(user_id)
    if request.method == 'GET':
        return render_template("edit.html", user=Users, date=datetime.now())
    
    

    User.update(request.form)
    return redirect('/show')


