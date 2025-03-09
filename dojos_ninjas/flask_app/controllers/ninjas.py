from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja
from datetime import datetime


@app.route("/ninjas")
def create_ninja_page():                    # NEED TO ADD A UNITE JOIN QUERY TO SHOW EVERYTHING WITH CLASSES TO CALL ON FOR DATA
    dojo_list = Dojo.get_all()
    return render_template("ninjas.html", dojos = dojo_list)


@app.route('/new_ninja', methods=['POST'])      #create dojo post route
def save_new_ninja():
    Ninja.save_ninja(request.form)
    one_dojo_id = request.form['dojo_id']
    return redirect(f'/dojos/{ one_dojo_id }')
##############################################################

@app.route("/show")
def show():
    ninjas = Ninja.get_all()
    return render_template("ninjas.html", ninjas = ninjas)

@app.route("/ninjas/<int:ninja_id>/show")
def show_one(ninja_id):
    ninjas = Ninja.get_one(ninja_id)
    return render_template("show.html", ninjas = ninjas)



@app.route('/ninjas/<int:ninja_id>/edit', methods=["GET","POST"])
def edit(ninja_id):
    ninjas = Ninja.get_one(ninja_id)
    if request.method == 'GET':
        return render_template("edit.html", ninja=ninjas, date=datetime.now())
    
    
    print("I'm here")
    Ninja.update(request.form)
    return redirect('/show')


@app.route("/ninja/<ninja_id>/delete")
def delete(ninja_id):
    Ninja.delete(ninja_id)
    return redirect("/show")