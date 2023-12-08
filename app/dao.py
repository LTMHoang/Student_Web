from app.models import *
from app import app


def get_user_by_id(user_id):
    return User.query.get(user_id)