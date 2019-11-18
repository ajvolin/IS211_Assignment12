#!/usr/bin/python
# -*- coding: utf-8 -*-

"""app.py: IS 211 Assignment 12."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

import os
from flask import Flask, current_app, render_template, request, session, redirect, g

app = Flask(__name__)
# Set a secret key for Flask to use to encrypt the session,
# best practice is to store this in an environment file
# but for simplicity will be stored here
app.secret_key = "5c8fce510fa3c5f9bb251cd1b13fd6eb"

students = [{ "id": "10000001", "first_name": "John", "last_name": "Smith" }]
quizzes = [{ "id": "1", "quiz_subject": "Python Basics", "question_count": 5, "quiz_date": "2015-02-05" }]

def check_auth():
    if "auth" in session:
        return True
    return False

# Index route
@app.route('/')
def index():
    return redirect("/login")

@app.route('/login')
def get_login():
    if not check_auth():
        return render_template("auth/login.html",
                           errors=session.pop("errors", None),
                           alert=session.pop("alert", None)
                           )
    else:
        return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def post_login():
    """Function to authenticate a user."""
    def authenticate():
        if request.form["username"] != "admin" or request.form["password"] != "password":
            return False
        else:
            return True

    if authenticate():
        session['auth'] = { "username": request.form["username"] }
        session["alert"] = {
            "level": "success",
            "message": "Successfully logged in!"
        }
        return redirect("/dashboard")
    else:
        session["alert"] = {
            "level": "danger",
            "message": "Could not validate the provided credentials. Please try again!"
        }
        return redirect("/login")

@app.route('/logout')
def logout():
    if check_auth():
        session.pop("auth", None)
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    if not check_auth():
        return redirect("/")
    
    breadcrumbs = [ { "title": "Dashboard", "url": "/" } ]
    return render_template("teacher/dashboard.html",
                           breadcrumbs=breadcrumbs,
                           students=students,
                           quizzes=quizzes,
                           errors=session.pop("errors", None),
                           alert=session.pop("alert", None)
                           )

@app.route('/student/add')
def get_add_student():
    """
    Function to render the add_student template and pass errors and alerts.
    """
    breadcrumbs = [
                    {"title": "Dashboard", "url": "/dashboard"},
                    {"title": "Add Student", "url": "/student/add"}
                  ]
    return render_template("teacher/add_student.html",
                           breadcrumbs=breadcrumbs,
                           errors=session.pop("errors", None),
                           alert=session.pop("alert", None)
                           )

@app.route('/student/add', methods=['POST'])
def post_add_student():
    pass

@app.route('/student/<id>')
def get_student(id):
    breadcrumbs = [
                    {"title": "Dashboard", "url": "/dashboard"},
                    {"title": "Student", "url": "/student/"+id }
                  ]
    return render_template("teacher/view_student.html",
                           breadcrumbs=breadcrumbs,
                           student=students[0],
                           errors=session.pop("errors", None),
                           alert=session.pop("alert", None)
                           )

@app.route('/student/<id>/delete', methods=['POST'])
def post_delete_student(id):
    pass

@app.route('/quiz/add')
def get_add_quiz():
    """
    Function to render the add_quiz template and pass errors and alerts.
    """
    breadcrumbs = [
                    {"title": "Dashboard", "url": "/dashboard"},
                    {"title": "Add Quiz", "url": "/quiz/add"}
                  ]
    return render_template("teacher/add_quiz.html",
                           breadcrumbs=breadcrumbs,
                           errors=session.pop("errors", None),
                           alert=session.pop("alert", None)
                           )

@app.route('/quiz/add', methods=['POST'])
def post_add_quiz():
    pass

@app.route('/quiz/<id>/results')
def get_quiz_results(id):
    pass

@app.route('/quiz/<quiz_id>/results/<student_id>/delete')
def get_delete_quiz_result(quiz_id, student_id):
    return redirect('/dashboard')


@app.route('/results/add')
def get_add_result():
    """
    Function to render the add_quiz template and pass errors and alerts.
    """
    breadcrumbs = [
                    {"title": "Dashboard", "url": "/dashboard"},
                    {"title": "Add Quiz Result", "url": "/results/add"}
                  ]
    return render_template("teacher/add_result.html",
                           breadcrumbs=breadcrumbs,
                           students=students,
                           quizzes=quizzes,
                           errors=session.pop("errors", None),
                           alert=session.pop("alert", None)
                           )


if __name__ == '__main__':
    app.run()
