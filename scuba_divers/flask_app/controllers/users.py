from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import user

@app.route('/')
def index():
    return redirect('/user/login')

@app.route('/user/login')
def login():
    return render_template('index.html')

@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not user.User.validate_reg(request.form):
        return redirect('/user/login')
    
    user_id = user.User.save(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/login/process', methods=['POST'])
def login_success():
    user_login = user.User.validate_login(request.form)
    if not user_login:
        return redirect('/user/login')
    print('here')
    session['user_id'] = user_login.id
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
	#We can clear the session here.
    return redirect('/user/login')