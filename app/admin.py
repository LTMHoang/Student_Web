from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import *
from flask_login import current_user, logout_user
from flask import redirect


class AuthenticatedAdminMV(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role_id == 1


class AuthenticatedAdminBV(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role_id == 1


class UserView(ModelView):
    pass


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='QUẢN TRỊ', template_mode='bootstrap4')
admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(UserView(User, db.session))