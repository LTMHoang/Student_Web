from datetime import datetime, date

from pymysql import Date
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship, declarative_base
from app import db, app
from flask_login import UserMixin
import enum


class SemesterEnum(enum.Enum):
    I = "Học Kỳ I"
    II = "Học Kỳ II"


class RoleEnum(enum.Enum):
    Admin = "admin",
    Staff = "staff",
    Teacher = "teacher",
    Student = "student",


class Role(db.Model):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(RoleEnum), primary_key=True)

    def __str__(self):
        return self.name.value


class User(db.Model, UserMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    dateofbirth = Column(DateTime)
    address = Column(String(255))
    sex = Column(Boolean, nullable=False)
    phone = Column(String(10))
    email = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), default='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
    # user_role = Column(Enum(UserRoleEnum), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)

    def __init__(self, name, dateofbirth, address, sex, phone, email, username, password, avatar, role,
                 role_id):
        self.name = name
        self.dateofbirth = dateofbirth
        self.address = address
        self.sex = sex
        self.phone = phone
        self.email = email
        self.username = username
        self.password = password
        self.avatar = avatar
        self.role = role
        self.role_id = role_id

    def __str__(self):
        return self.name


class Teacher(User):
    __tablename__ = 'teacher'
    teachingdetails = relationship('TeachingDetails', back_populates='teacher')

    def __str__(self):
        return self.name

    # def __init__(self, name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #              user_role, role, role_id):
    #     super(Teacher, self).__init__(name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #                                   user_role, role, role_id)


class Admin(User):
    __tablename__ = 'admin'

    def __str__(self):
        return self.name

    # def __init__(self, name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #              user_role, role, role_id):
    #     super(Teacher, self).__init__(name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #                                   user_role, role, role_id)


class Staff(User):
    __tablename__ = 'staff'

    def __str__(self):
        return self.name

    # def __init__(self, name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #              user_role, role, role_id):
    #     super(Teacher, self).__init__(name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #                                   user_role, role, role_id)


class Year(db.Model):
    __tablename__ = 'year'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(11), nullable=False)
    classrooms = relationship('ClassRoom', backref='year', lazy=True)
    semesters = relationship('Semester', back_populates='year', lazy=True)

    def __str__(self):
        return self.name


class Grade(db.Model):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer, nullable=False)
    classrooms = relationship('ClassRoom', backref='grade', lazy=True)

    def __str__(self):
        return self.name


class ClassRoom(db.Model):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    grade_name = Column(Integer, ForeignKey(Grade.id), nullable=False)
    year_name = Column(Integer, ForeignKey(Year.id), nullable=False)
    teachingdetails = relationship('TeachingDetails', back_populates='classroom')
    students = relationship('Student', backref='classroom', lazy=True)

    def __str__(self):
        return self.name


class Student(User):
    __tablename__ = 'student'
    subjectdetails = relationship('SubjectDetails', back_populates='student')
    id_classroom = Column(Integer, ForeignKey(ClassRoom.id), nullable=False)

    # def __init__(self, id_classroom, name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #              user_role,role,role_id):
    #     self.id_classroom = id_classroom
    #     super(Student, self).__init__(name, dateofbirth, address, sex, phone, email, username, password, avatar,
    #                                   user_role, role, role_id)


class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teachingdetails = relationship('TeachingDetails', back_populates='subject')
    subjectdetails = relationship('SubjectDetails', back_populates='subject')

    def __str__(self):
        return self.name


class Semester(db.Model):
    __tablename__ = 'semester'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(SemesterEnum), nullable=False)
    year_id = Column(Integer, ForeignKey(Year.id), nullable=False)
    subjectdetails = relationship('SubjectDetails', back_populates='semester')
    year = relationship('Year', back_populates='semesters', lazy=True)

    def __str__(self):
        return self.name


class TeachingDetails(db.Model):
    __tablename__ = 'teachingdetails'
    id = Column(Integer, primary_key=True)
    id_teacher = Column(Integer, ForeignKey(Teacher.id))
    subject_name = Column(Integer, ForeignKey(Subject.id))
    classroom_name = Column(Integer, ForeignKey(ClassRoom.id))
    schedule = Column(DateTime, nullable=False)
    teacher = relationship('Teacher', back_populates='teachingdetails')
    subject = relationship('Subject', back_populates='teachingdetails')
    classroom = relationship('ClassRoom', back_populates='teachingdetails')


class SubjectDetails(db.Model):
    __tablename__ = 'subjectdetails'
    id = Column(Integer, primary_key=True)
    marktype = Column(String(50), nullable=False)
    mark = Column(Float, nullable=False)
    subject_name = Column(Integer, ForeignKey(Subject.id), nullable=True)
    id_student = Column(Integer, ForeignKey(Student.id), nullable=False)
    semester_name = Column(Integer, ForeignKey(Semester.id), nullable=False)
    student = relationship('Student', back_populates='subjectdetails')
    semester = relationship('Semester', back_populates='subjectdetails')
    subject = relationship('Subject', back_populates='subjectdetails')


if __name__ == '__main__':
    with app.app_context():
        # Xóa các bảng đã có sẵn
        db.drop_all()

        # Tạo các bảng
        db.create_all()

        # Tạo các role
        r1 = Role(name=RoleEnum.Admin)
        r2 = Role(name=RoleEnum.Staff)
        r3 = Role(name=RoleEnum.Teacher)
        r4 = Role(name=RoleEnum.Student)
        db.session.add_all([r1, r2, r3, r4])
        db.session.commit()

        # Tạo các user
        import hashlib

        u1 = Admin(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                   role=RoleEnum.Admin, role_id=1, sex=True,
                   dateofbirth=datetime.now(),
                   address='text', phone='text',
                   email='test'
                   , avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
        u2 = Staff(name='Staff', username='staff', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                   role=RoleEnum.Staff, role_id=2, sex=True,
                   dateofbirth=datetime.now(),
                   address='text', phone='text',
                   email='test'
                   , avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
        y1 = Year(name='2020 - 2021')
        y2 = Year(name='2021 - 2022')
        y3 = Year(name='2022 - 2023')
        y4 = Year(name='2023 - 2024')
        db.session.add_all([y1, y2, y3, y4])
        db.session.add_all([u1, u2])

        db.session.commit()
