from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user

from app.models import RoleEnum, Admin, Staff, Teacher, Student

selected_role = ""

@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def common_response():
    return {
        'RoleEnum': RoleEnum
    }


@app.route('/signinandsignup')
def signinandsignup():
    return render_template('signinandsignup.html')


@login.user_loader
def load_user(user_id):
    if selected_role == "Admin":
        return Admin.query.get(user_id)
    elif selected_role == "Staff":
        return Staff.query.get(user_id)
    elif selected_role == "Teacher":
        return Teacher.query.get(user_id)
    else:
        return Student.query.get(user_id)


@app.route("/login", methods=['get', 'post'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get('role')
        global selected_role
        selected_role = role
        user = dao.authenicate_user(username, password, role)
        if user:
            login_user(user=user)
            if user.role == RoleEnum.Student:
                return redirect('/')
            else:
                return redirect('/admin')
    return redirect("/signinandsignup")


@app.route("/signupandsignin", methods=['get', 'post'])
def signupandsignin():
    return render_template('/signupandsignin')


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
