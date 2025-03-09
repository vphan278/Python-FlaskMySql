from flask import render_template, request, redirect
from flask_app import app
# from datetime import datetime
from flask_app.models import course

# @app.route('/')
# def index():
#     return redirect('/dashboard')

@app.route('/dashboard')
def all_divers():
    courses = course.Courses.get_all_courses()
    return render_template("dashboard.html",courses=courses)

@app.route('/course/new')
def add_new_course():
    return render_template('new_course.html')

@app.route('/course/insert', methods=['POST'])
def insert_course():
    course.Courses.insert_courses(request.form)
    return redirect('/dashboard')

@app.route('/course/<int:id>')
def course_by_id(id):
    all_divers = course.Courses.get_one_with_divers(id)
    return render_template('courses.html', divers=all_divers)