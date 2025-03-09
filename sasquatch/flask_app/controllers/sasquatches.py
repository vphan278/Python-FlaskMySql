from flask import render_template, redirect, session, request
from flask_app import app
# from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.sasquatch import Sasquatch
from datetime import datetime


@app.route("/sasquatches/new")
def display_dasboard():
    
    return render_template("sasquatch_new.html")


@app.route('/sasquatches/create', methods=["POST"])
def create():
    if not "user_id" in session:
        return redirect('/')
    if not Sasquatch.validator(request.form):
        return redirect('/sasquatches/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Sasquatch.save(data)

    return redirect('/sasquatches')

@app.route('/sasquatches/edit/<int:id>')
def edit(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    sasquatch = Sasquatch.get_by_id(data)
    return render_template('sasquatch_edit.html', sasquatch=sasquatch)

@app.route('/sasquatches/update/<int:id>', methods=["POST"])
def update(id):
    if not "user_id" in session:
        return redirect('/')
    if not Sasquatch.validator(request.form):
        return redirect(f'/sasquatches/edit/{id}')
    data = {
        **request.form,
        'id': id
    }
    Sasquatch.update(data)
    return redirect('/sasquatches')

@app.route('/sasquatches/delete/<int:id>')
def destroy(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id 
    }
    #optional security features
    to_be_deleted = Sasquatch.get_by_id(data)
    if not session['user_id'] == to_be_deleted.user_id:
        flash("Quit trying to delete other people's sasquatches", "err_destroy")
        return redirect('/')
    Sasquatch.delete(data)
    return redirect('/sasquatches')

@app.route('/sasquatches/<int:id>')
def show_one(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    data2 = {
        'id': session['user_id']
    }
    sasquatch = Sasquatch.get_by_id(data)
    user = User.get_user_by_id(data2)
    return render_template('sasquatch_one.html', sasquatch=sasquatch, user=user)