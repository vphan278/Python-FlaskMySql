from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja


@app.route("/ninjas")
def create_ninja_page():                    # NEED TO ADD A UNITE JOIN QUERY TO SHOW EVERYTHING WITH CLASSES TO CALL ON FOR DATA
    dojo_list = Dojo.get_all()
    return render_template("ninjas.html", dojos = dojo_list)


@app.route('/new_ninja', methods=['POST'])      #create dojo post route
def save_new_ninja():
    Ninja.save_ninja(request.form)
    one_dojo_id = request.form['dojo_id']
    return redirect(f'/dojos/{ one_dojo_id }')