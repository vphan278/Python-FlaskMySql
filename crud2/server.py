from flask import Flask, render_template, request, redirect
# import the class from friend.py
from datetime import datetime
from friend import Friend

app = Flask(__name__)


@app.route("/")
def index():
    # call the get all classmethod to get all friends
    #friends = Friend.get_all()
    #print(friends)
    return render_template("index.html")
            

# relevant code snippet from server.py

@app.route('/create_friend', methods=["POST"])
def create_friend():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    Friend.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/show')

@app.route("/show")
def show():
    friends = Friend.get_all()
    return render_template("friends.html", friends = friends)


@app.route("/friends/<int:friend_id>/show")
def show_one(friend_id):
    friends = Friend.get_one(friend_id)
    return render_template("show.html", friends = friends)


@app.route("/friend/<friend_id>/delete")
def delete(friend_id):
    Friend.delete(friend_id)
    return redirect("/show")



@app.route('/friends/<int:friend_id>/edit', methods=["GET","POST"])
def edit(friend_id):
    Friends = Friend.get_one(friend_id)
    if request.method == 'GET':
        return render_template("edit.html", friend=Friends, date=datetime.now())
    
    

    Friend.update(request.form)
    return redirect('/show')








if __name__ == "__main__":
    app.run(debug=True)

