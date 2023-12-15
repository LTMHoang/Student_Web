

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, Table, DateTime
from sqlalchemy.orm import relationship, Relationship
from app import db, app
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    TEACHER = "teacher"
    STAFF = "staff"


class SemesterEnum(enum.Enum):
    FIRSTSEMESTER = "firstsemester"
    MID_TERMONE = "mid_termone"
    SECONDSEMESTER = "secondsemester"
    MIDTERMSECONDSEMESTER = "Midtermsecondsemester"


class Role(db.Model):
    __tablename = 'role'
    # id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(Enum(UserRoleEnum), primary_key=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
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
    user_role = Column(Enum(UserRoleEnum), ForeignKey(Role.name), nullable=False)

    def __str__(self):
        return self.name

class Teacher(User):
    __tablename__ = 'teacher'
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    teachingdetails = Relationship('TeachingDetails', back_populates='teacher')



class Year(db.Model):
    __tablename__ = 'year'
    name = Column(String(11), primary_key=True)
    classrooms = Relationship('ClassRoom', backref='year', lazy=True)

    def __str__(self):
        return self.name


class Grade(db.Model):
    __tablename__ = 'grade'
    name = Column(Integer, primary_key=True)
    classrooms = Relationship('ClassRoom', backref='grade', lazy=True)
    year_name = Column(String(11), ForeignKey(Year.name))

    def __str__(self):
        return self.name


class ClassRoom(db.Model):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key=True)
    name = Column(String(5), nullable=False)
    quantity = Column(Integer, nullable=False)
    grade_name = Column(Integer, ForeignKey(Grade.name), nullable=False)
    year_name = Column(String(11), ForeignKey(Year.name), nullable=False)
    teachingdetails = Relationship('TeachingDetails', back_populates='classroom')
    students = relationship('Student', backref='classroom', lazy=True)
    def __str__(self):
        return self.name

class Student(User):
    __tablename__ = 'student'
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    subjectdetails = Relationship('SubjectDetails', back_populates='student')
    id_classroom = Column(Integer, ForeignKey(ClassRoom.id),nullable=False)
class Subject(db.Model):
    __tablename__ = 'subject'
    name = Column(String(100), primary_key=True)
    teachingdetails = Relationship('TeachingDetails', back_populates='subject')
    subject_details = relationship('SubjectDetails', back_populates='subject')

    def __str__(self):
        return self.name


class Semester(db.Model):
    __tablename__ = 'semester'
    name = Column(Enum(SemesterEnum), primary_key=True)
    year = Column(String(11), ForeignKey(Year.name), nullable=False)
    subject_details = relationship('SubjectDetails', back_populates='Semester')

    def __str__(self):
        return self.name

class TeachingDetails(db.Model):
   __tablename__='teachingdetails'
   id = Column(Integer, primary_key=True)
   id_giaovien = Column(Enum(UserRoleEnum),ForeignKey(User.id))
   subject_name = Column(String(100),ForeignKey(Subject.name))
   classroom_name=Column(String(5),ForeignKey(ClassRoom.name))
   schedule=Column(DateTime, nullable=False)
   teacher = Relationship('Teahcher',back_populates='teachingdetails')
   subject = Relationship('Subject', back_populates='teachingdetails')
   teacher = Relationship('ClassRoom', back_populates='teachingdetails')


class SubjectDetails(db.Model):
    __tablename__='subjectdetails'
    id = Column(Integer,primary_key=True)
    marktype = Column(String(50), nullable=False)
    mark = Column(Float,nullable=False),
    subject_name = Column(String(100),ForeignKey(Subject.name),nullable=True)
    id_student = Column(Integer, ForeignKey(Student.id),nullable=False)
    semester_name = Column(Enum(SemesterEnum), ForeignKey(Semester.name), nullable=False)
    student = Relationship('Student', back_populates='subjectdetails')
    semester = Relationship('Semester', back_populates='subjectdetails')
    subject = Relationship('Subject', back_populates='subjectdetails')

if __name__ == '__main__':
    with app.app_context():
        # Xóa các bảng đã có sẵn
        db.drop_all()

        # Tạo các bảng
        db.create_all()

        # Tạo các role
        r1 = Role(name=UserRoleEnum.ADMIN)
        r2 = Role(name=UserRoleEnum.USER)
        r3 = Role(name=UserRoleEnum.TEACHER)
        r4 = Role(name=UserRoleEnum.STAFF)
        db.session.add_all([r1, r2, r3, r4])

        # Tạo các user
        import hashlib

        u1 = User(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.ADMIN)
        u2 = User(name='User2', username='user2', password=str(hashlib.md5('654321'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.USER)
        db.session.add_all([u1, u2])

        db.session.commit()
