# Import app
from flask_app import app
#Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt
# Import models class
from flask_app.models import user

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods= ["POST"])
def register():
    print(request.form)
    if not user.User.validate_registration(request.form):
        return redirect("/")

    
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }

    user_id = user.User.create_user(data)
    if user_id:
        session["id"] = user_id
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    """Welcome Page"""
    if "id" not in session:
        flash("Please register or login to continue", "danger")
        return redirect("/")

    data = {
        "id": session["id"]
    }

    one_user = user.User.get_user_by_id(data)
    if one_user:
        session["first_name"] = one_user.first_name
        session["last_name"] = one_user.last_name
        session["email"] = one_user.email
    return render_template("dashboard.html", one_user=one_user)


@app.route("/login", methods=["POST"])
def login():

    data = { "email": request.form["email"]}
    

    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email or Need to register", "danger")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("The password must be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
        return redirect("/")

    session["id"] = user_in_db.id
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
