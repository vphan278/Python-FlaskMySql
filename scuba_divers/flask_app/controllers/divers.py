from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_app.models.diver import Diver


app=Flask(__name__)

@app.route('/')
def index():
    return redirect('/divers')

@app.route('/divers')
def all_divers():
    return render_template("index.html",divers=Diver.get_all_divers())



@app.route('/diver/new')
def add_new_diver():
    return render_template('new_diver.html')

@app.route('/diver/save', methods=['POST'])
def save_diver():
    Diver.save_diver(request.form)
    return redirect('/')

# @app.route('/diver/update')
# def update_diver():
#     return render_template('update_diver.html')


@app.route("/diver/<int:id>/delete")
def delete_diver(id):
    Diver.delete_diver(id)
    return redirect('/')

@app.route('/diver/<int:id>/edit', methods=["GET","POST"])
def edit_diver(id):
    diver = Diver.get_diver_by_id(id)
    if request.method == 'GET':
        return render_template("edit_diver.html", diver=diver, date=datetime.now())

    Diver.update_diver(request.form)
    return redirect('/')


