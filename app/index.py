from flask import render_template, request, redirect
from flask_login import login_user
from app import login, admin, dao
from app.models import *



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/login', methods=['post'])
def admin_login():
    request.form.get('username')
    request.form.get('password')


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login-admin", methods=['get', 'post'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.authenicate_user(username, password)
        if user:
            login_user(user=user)
    return redirect("/admin")

if __name__ == '__main__':
    app.run(debug=True)
