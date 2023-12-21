from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from flask_login import logout_user, current_user
from flask import redirect

from app.models import RoleEnum, Year, Semester, Subject, Grade

admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.Admin


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedUser):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class YearView(AuthenticatedAdmin):
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


class SemesterView(AuthenticatedAdmin):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name', 'year.name']
    column_labels = {
        'id': 'STT',
        'name': 'Học Kỳ',
        'year.name': 'Năm Học'
    }
    column_exclude_list = ['SubjectDetails']


class SubjectView(AuthenticatedAdmin):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name']
    column_labels = {
        'id': 'STT',
        'name': 'Tên Môn Học',
    }


class GradeView(AuthenticatedAdmin):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name']
    column_labels = {
        'id': 'STT',
        'name': 'Tên Khối',
    }


class UserView(AuthenticatedAdmin):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name', 'dateofbirth', 'address', 'sex', 'phone', 'email', 'username', 'password', 'avatar',
                   'user_role', 'role']
    column_labels = {
        'id': 'STT',
        'name': 'Họ Và Tên',
        'dateofbirth': 'Ngày Sinh',
        'address': 'Địa Chỉ',
        'sex': 'Giới Tính',
        'phone': 'Số Điện Thoại',
        'email': 'Email',
        'username': 'Tên Tài Khoản',
        'password': 'Mật Khẩu',
        'avatar': 'Ảnh Đại Diện',
        'user_role': 'Vai Trò',
        'role': 'Chức Vụ'
    }


class HomePageView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(StatsView(name="Thống Kê Kết Quả Học Tập"))
admin.add_view(YearView(Year, db.session, name='Quản Lý Năm Học'))
admin.add_view(SemesterView(Semester, db.session, name='Quản Lý Học Kỳ'))
admin.add_view(SubjectView(Subject, db.session, name='Quản Lý Môn Học'))
admin.add_view(GradeView(Grade, db.session, name='Quản Lý Khối Lớp'))
admin.add_view(HomePageView(name='Trang Chủ'))
