from app.models import *
from app import app
import hashlib

selected_role = ""

def get_user_by_id(user_id):
    if selected_role == "Admin":
        return Admin.query.get(user_id)
    elif selected_role == "Staff":
        return Staff.query.get(user_id)
    elif selected_role == "Teacher":
        return Teacher.query.get(user_id)
    else:
        return Student.query.get(user_id)


def authenicate_user(username, password, role):
    global selected_role
    selected_role = role
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    if role == "Admin":
        return Admin.query.filter(Admin.username.__eq__(username.strip()),
                                  Admin.password.__eq__(password.strip())).first()
    elif role == "Staff":
        return Staff.query.filter(Staff.username.__eq__(username.strip()),
                                  Staff.password.__eq__(password.strip())).first()
    elif role == "Teacher":
        return Staff.query.filter(Teacher.username.__eq__(username.strip()),
                                  Teacher.password.__eq__(password.strip())).first()
    else:
        return Student.query.filter(Student.username.__eq__(username.strip()),
                                    Student.password.__eq__(password.strip())).first()
