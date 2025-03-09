# Import app
from flask_app import app
#Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt
#

# Import models class
from flask_app.models import user

# Create the routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    """Register new user"""
    # Call staticmethod to validate form
    if not user.User.validate_registration(request.form):
        # Redirect back to registration page
        return redirect('/')
    # Create data dict based on request form
    # the keys must match exactly to the var in the query set
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    # Pass the data dict to create_user method in class
    # After insert the db returns the user_id; save it
    user_id = user.User.create_user(data)
    # Check we have a user_id; is yes save into session
    if user_id:
        session['id'] = user_id
    # Redirect to the dashboard page
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """Welcome page"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data set to query user based on id to get name to display
    data = {
        'id': session['id']
    }
    # Pass the data dict to create_user method in class
    one_user = user.User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name
    return render_template('dashboard.html', one_user=one_user)

@app.route('/login', methods=['POST'])
def login():
    """Login in the user"""
    # See if the username/email provide is in db
    data = { 'email': request.form['email'] }
    user_in_db = user.User.get_user_by_email(data)
    # if user_in_db returns None
    if not user_in_db:
        flash("Invalid Email or Need to register", "danger")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # If returns False, flash message
        flash("The password must be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
        return redirect('/')
    # If password match, we set the user_id into session
    session['id'] = user_in_db.id
    # Never render on a POST
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    """Logged the user out of seesion and redirect to login"""
    session.clear()
    return redirect('/')