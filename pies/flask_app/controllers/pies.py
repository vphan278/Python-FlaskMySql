from flask import render_template, redirect, session, request
from flask_app import app
# from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.pie import Pie
from datetime import datetime


@app.route("/pies/new")
def display_dasboard():
    
    return render_template("pie_new.html")


@app.route('/pies/create', methods=["POST"])
def create():
    if not "user_id" in session:
        return redirect('/')
    if not Pie.validator(request.form):
        return redirect('/pies/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Pie.save(data)

    return redirect('/pies')

@app.route('/pies/edit/<int:id>')
def edit(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    pie = Pie.get_by_id(data)
    return render_template('pie_edit.html', pie=pie)

@app.route('/pies/update/<int:id>', methods=["POST"])
def update(id):
    if not "user_id" in session:
        return redirect('/')
    if not Pie.validator(request.form):
        return redirect(f'/pies/edit/{id}')
    data = {
        **request.form,
        'id': id
    }
    Pie.update(data)
    return redirect('/pies')

@app.route('/pies/delete/<int:id>')
def destroy(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id 
    }
    #optional security features
    to_be_deleted = Pie.get_by_id(data)
    if not session['user_id'] == to_be_deleted.user_id:
        flash("Quit trying to delete other people's pies", "err_destroy")
        return redirect('/')
    Pie.delete(data)
    return redirect('/pies')

@app.route('/pies/<int:id>')
def show_one(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    data2 = {
        'id': session['user_id']
    }
    pie = Pie.get_by_id(data)
    user = User.get_user_by_id(data2)
    return render_template('pie_one.html', pie=pie, user=user)