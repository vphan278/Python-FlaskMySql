from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route("/")
def all_dojos():
    dojo_list = Dojo.get_all()                  #returns a list
    return render_template("dojos.html", dojos = dojo_list)


@app.route("/dojos/<int:id>")              # want to show all the ninjas for this specific dojo as well so id need to unite them in the query
def show_one_dojo_with_all_ninjas(id):
    one_dojo_with_ninjas = Dojo.one_dojo_with_ninjas(id)
    return render_template("one_dojo.html", dojo_info = one_dojo_with_ninjas)

@app.route('/new_dojo', methods=['POST'])       #create dojo post route
def save_new_dojo():
    new_dojo = Dojo.save_dojo(request.form)
    return redirect('/')
################################################################
