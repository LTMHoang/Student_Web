from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum


class SemesterEnum(enum.Enum):
    I = 1
    II = 2


class GradeEnum(enum.Enum):
    Grade_10 = 10,
    Grade_11 = 11,
    Grade_12 = 12,


#
# class YearEnum(enum.Enum):
#     Year_2020_2021 = 2020,
#     Year_2021_2022 = 2021,
#     Year_2022_2023 = 2022,
#     Year_2023_2024 = 2023,
#     Year_2024_2025 = 2024,


class RoleEnum(enum.Enum):
    Admin = 1,
    Staff = 2,
    Teacher = 3,
    Student = 4


class SubjectEnum(enum.Enum):
    Mathematics = 1,
    Literature = 2,
    English = 3,
    Physics = 4,
    Chemistry = 5,
    Biology = 6,
    History = 7,
    Geography = 8,
    Civics = 9,
    ComputerScience = 10,
    Technology_Education = 11,
    Physical_Education = 12,
    NationalDefense_SecurityEducation = 13,


class Role(db.Model):
    __tablename__ = 'role'
    name = Column(Enum(RoleEnum), primary_key=True)

    def __str__(self):
        return self.name.value


class User(db.Model, UserMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    dob = Column(DateTime)
    address = Column(String(255))
    sex = Column(Boolean, nullable=False)
    phone = Column(String(11))
    email = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), default='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
    role = Column(Enum(RoleEnum), ForeignKey(Role.name), nullable=False)

    def __str__(self):
        return self.name


class Teacher(User):
    __tablename__ = 'teacher'
    teachingdetails = relationship('TeachingDetails', back_populates='teacher')

    def __str__(self):
        return self.name


class Admin(User):
    __tablename__ = 'admin'

    def __str__(self):
        return self.name


class Staff(User):
    __tablename__ = 'staff'

    def __str__(self):
        return self.name


# class Year(db.Model):
#     __tablename__ = 'year'
#     id = Column(Integer, primary_key=True)
#     name = Column(Enum(YearEnum), nullable=False)
#     classrooms = relationship('ClassRoom', backref='year', lazy=True)
#     semesters = relationship('Semester', back_populates='year', lazy=True)
#
#     def __str__(self):
#         return self.name
#

class Grade(db.Model):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(GradeEnum), nullable=False)
    classrooms = relationship('ClassRoom', backref='grade', lazy=True)

    def __str__(self):
        return self.name


class ClassRoom(db.Model):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    grade_name = Column(Integer, ForeignKey(Grade.id), nullable=False)
    # year_name = Column(Integer, ForeignKey(Year.id), nullable=False)
    year_name = Column(Integer, nullable=False)
    teachingdetails = relationship('TeachingDetails', back_populates='classroom')
    students = relationship('Student', backref='classroom', lazy=True)

    def __str__(self):
        return self.name


class Student(User):
    __tablename__ = 'student'
    subjectdetails = relationship('SubjectDetails', back_populates='student')
    classroom_id = Column(Integer, ForeignKey(ClassRoom.id), nullable=False)


class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(Enum(SubjectEnum), nullable=False)
    teachingdetails = relationship('TeachingDetails', back_populates='subject')
    subjectdetails = relationship('SubjectDetails', back_populates='subject')

    def __str__(self):
        return self.name


class Semester(db.Model):
    __tablename__ = 'semester'
    id = Column(Integer, primary_key=True)
    name = Column(Enum(SemesterEnum), nullable=False)
    # year_id = Column(Integer, ForeignKey(Year.id), nullable=False)
    year_name = Column(Integer, nullable=False)
    subjectdetails = relationship('SubjectDetails', back_populates='semester')

    # year = relationship('Year', back_populates='semesters', lazy=True)

    def __str__(self):
        return self.name


class TeachingDetails(db.Model):
    __tablename__ = 'teachingdetails'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(Teacher.id))
    subject_id = Column(Integer, ForeignKey(Subject.id))
    classroom_id = Column(Integer, ForeignKey(ClassRoom.id))
    schedule = Column(DateTime, nullable=False)
    teacher = relationship('Teacher', back_populates='teachingdetails')
    subject = relationship('Subject', back_populates='teachingdetails')
    classroom = relationship('ClassRoom', back_populates='teachingdetails')


class SubjectDetails(db.Model):
    __tablename__ = 'subjectdetails'
    id = Column(Integer, primary_key=True)
    marktype = Column(String(50), nullable=False)
    mark = Column(Float, nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    student = relationship('Student', back_populates='subjectdetails')
    semester = relationship('Semester', back_populates='subjectdetails')
    subject = relationship('Subject', back_populates='subjectdetails')


if __name__ == '__main__':
    with app.app_context():
        # Xóa các bảng đã có sẵn
        db.drop_all()

        # Tạo các bảng
        db.create_all()

        # Tạo các Role
        r1 = Role(name=RoleEnum.Admin)
        r2 = Role(name=RoleEnum.Staff)
        r3 = Role(name=RoleEnum.Teacher)
        r4 = Role(name=RoleEnum.Student)
        db.session.add_all([r1, r2, r3, r4])
        db.session.commit()
        #
        # # Tạo Year
        # y1 = Year(id = YearEnum.Year_2020_2021.value,name=YearEnum.Year_2020_2021)
        # y2 = Year(id = YearEnum.Year_2021_2022.value,name=YearEnum.Year_2021_2022)
        # y3 = Year(id = YearEnum.Year_2022_2023.value,name=YearEnum.Year_2022_2023)
        # y4 = Year(id = YearEnum.Year_2023_2024.value,name=YearEnum.Year_2023_2024)
        # y5 = Year(id = YearEnum.Year_2024_2025.value,name=YearEnum.Year_2024_2025)

        # Tạo Grade
        g1 = Grade(id=GradeEnum.Grade_10.value, name=GradeEnum.Grade_10)
        g2 = Grade(id=GradeEnum.Grade_11.value, name=GradeEnum.Grade_11)
        g3 = Grade(id=GradeEnum.Grade_12.value, name=GradeEnum.Grade_12)

        # db.session.add_all([g1, g2, g3, y1, y2, y3, y4])
        # db.session.commit()

        db.session.add_all([g1, g2, g3])
        db.session.commit()

        # Tạo ClassRoom
        # cr1 = ClassRoom(name="10A1", quantity=50, grade_name=GradeEnum.Grade_10.value,
        #                 year_name=22)
        # cr2 = ClassRoom(name="11B1", quantity=60, grade_name=GradeEnum.Grade_11.value,
        #                 year_name=YearEnum.Year_2022_2023.value)
        # cr3 = ClassRoom(name="12C1", quantity=45, grade_name=GradeEnum.Grade_12.value,
        #                 year_name=YearEnum.Year_2022_2023.value)
        #
        # db.session.add_all([cr1, cr2, cr3])
        # db.session.commit()

        cr1 = ClassRoom(name="10A1", quantity=50, grade_name=GradeEnum.Grade_10.value,
                        year_name=2022)
        cr2 = ClassRoom(name="11B1", quantity=60, grade_name=GradeEnum.Grade_11.value,
                        year_name=2022)
        cr3 = ClassRoom(name="12C1", quantity=45, grade_name=GradeEnum.Grade_12.value,
                        year_name=2022)

        db.session.add_all([cr1, cr2, cr3])
        db.session.commit()

        # Tạo Semester
        # st1 = Semester(name=SemesterEnum.I, year_id=YearEnum.Year_2022_2023.value, year=y3)
        # st2 = Semester(name=SemesterEnum.II, year_id=YearEnum.Year_2022_2023.value, year=y3)
        #
        # db.session.add_all([st1, st2])
        # db.session.commit()

        # Tạo Semester
        st1 = Semester(id=SemesterEnum.I.value, name=SemesterEnum.I, year_name=2022)
        st2 = Semester(id=SemesterEnum.II.value, name=SemesterEnum.II, year_name=2022)

        db.session.add_all([st1, st2])
        db.session.commit()

        # Tạo User
        import hashlib

        u1 = Admin(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                   role=RoleEnum.Admin, sex=True,
                   dob=datetime.now(),
                   address='text', phone='text',
                   email='test'
                   , avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
        u2 = Staff(name='Staff', username='staff', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                   role=RoleEnum.Staff, sex=True,
                   dob=datetime.now(),
                   address='text', phone='text',
                   email='test'
                   , avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
        u3 = Student(name='Student', username='student',
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                     role=RoleEnum.Student, classroom_id=1, sex=True,
                     dob=datetime.now(),
                     address='text', phone='text',
                     email='test'
                     , avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
        u4 = Teacher(name='Teacher', username='teacher',
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                     role=RoleEnum.Staff, sex=True,
                     dob=datetime.now(),
                     address='text', phone='text',
                     email='test'
                     , avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')

        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

        # Tạo Subject
        sj1 = Subject(id=SubjectEnum.Mathematics.value, name=SubjectEnum.Mathematics)
        sj2 = Subject(id=SubjectEnum.Literature.value, name=SubjectEnum.Literature)
        sj3 = Subject(id=SubjectEnum.English.value, name=SubjectEnum.English)
        sj4 = Subject(id=SubjectEnum.Physics.value, name=SubjectEnum.Physics)
        sj5 = Subject(id=SubjectEnum.Chemistry.value, name=SubjectEnum.Chemistry)
        sj6 = Subject(id=SubjectEnum.Biology.value, name=SubjectEnum.Biology)
        sj7 = Subject(id=SubjectEnum.History.value, name=SubjectEnum.History)
        sj8 = Subject(id=SubjectEnum.Geography.value, name=SubjectEnum.Geography)
        sj9 = Subject(id=SubjectEnum.Civics.value, name=SubjectEnum.Civics)
        sj10 = Subject(id=SubjectEnum.ComputerScience.value, name=SubjectEnum.ComputerScience)
        sj11 = Subject(id=SubjectEnum.Technology_Education.value, name=SubjectEnum.Technology_Education)
        sj12 = Subject(id=SubjectEnum.Physical_Education.value, name=SubjectEnum.Physical_Education)
        sj13 = Subject(id=SubjectEnum.NationalDefense_SecurityEducation.value,
                       name=SubjectEnum.NationalDefense_SecurityEducation)

        db.session.add_all([sj1, sj2, sj3, sj4, sj5, sj6, sj7, sj8, sj9, sj10, sj11, sj12, sj13])
        db.session.commit()
