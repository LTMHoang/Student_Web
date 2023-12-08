from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    TEACHER = "teacher"
    STAFF = "staff"


class Role(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(UserRoleEnum))

    def __str__(self):
        return self.id


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), default='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
    user_role_id = Column(Integer, ForeignKey(Role.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()


        # Tạo các bảng
        db.create_all()

        r1 = Role(name=UserRoleEnum.ADMIN)
        r2 = Role(name=UserRoleEnum.USER)
        r3 = Role(name=UserRoleEnum.TEACHER)
        r4 = Role(name=UserRoleEnum.STAFF)
        db.session.add_all([r1, r2, r3, r4])

        import hashlib
        u1 = User(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role_id=1)
        u2 = User(name='User2', username='user2', password=str(hashlib.md5('654321'.encode('utf-8')).hexdigest()),
                 user_role_id=2)
        db.session.add_all([u1, u2])

        db.session.commit()
