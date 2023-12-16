from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import *
from flask_login import current_user, logout_user
from flask import redirect


class AuthenticatedAdminMV(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedAdminBV(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.USER


class UserView(ModelView):
    pass


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class YearView(AuthenticatedAdminMV):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name']
    column_labels = {
        'name': 'Năm Học',
        'id': 'STT'
    }
    can_create = True


class SemesterView(AuthenticatedAdminMV):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name', 'year_id']
    column_labels = {
        'id': 'STT',
        'name': 'Học Kỳ',
        'year_id': 'Năm Học'
    }


admin = Admin(app=app, name='QUẢN TRỊ', template_mode='bootstrap4')
admin.add_view(UserView(User, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(YearView(Year, db.session, name='Quản Lý Năm Học'))
admin.add_view(SemesterView(Semester, db.session, name='Quản Lý Học Kỳ'))
