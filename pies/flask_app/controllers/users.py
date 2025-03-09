from flask import render_template, request, redirect, session, flash
# Import app
from flask_app import app
#Import modules from flask
# Import models class
from flask_app.models import user, pie

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods= ["POST"])
def register():
    
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
        session["user_id"] = user_id
    return redirect("/")

@app.route("/pies")
def dashboard():
    """Welcome Page"""
    if "user_id" not in session:
        flash("Please register or login to continue", "danger")
        return redirect("/")

    current_user = user.User.get_user_by_id({"id": session["user_id"]})
    all_pies = pie.Pie.get_all()
    
    return render_template("pies.html", user_pies = all_pies, current_user = current_user)


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

    session["user_id"] = user_in_db.id
    return redirect("/pies")



@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/")


