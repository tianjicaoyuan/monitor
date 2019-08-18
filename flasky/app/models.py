# coding=utf-8
# define SQL table
from flask_login import UserMixin
from datetime import datetime
from .import login_manager
from .import db
from werkzeug.security import generate_password_hash, check_password_hash


# define APP register User
class Uxser(db.Model, UserMixin):
    __tablename__ = 'userss'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    face_path = db.Column(db.String(64), index=True)
    face_name = db.Column(db.String(64), index=True)
    # 一个用户密码为12345678.

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_username(self):
        return self.username


# define history video
class Video(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True)
    cameraName = db.Column(db.String(4), index=True)
    dateTime = db.Column(db.DateTime, index=True, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    VideoPath = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    video_info = db.Column(db.String(128), index=True)


# define Camera table
class Camera(db.Model):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    cameraName = db.Column(db.String(4), index=True, unique=True)
    cameraIpAddress = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    FaceRecognition = db.Column(db.String(4), index=True)
    Describle = db.Column(db.String(128), index=True)
    video_way = db.Column(db.String(4), index=True, default="False")


# user login recall
@login_manager.user_loader
def load_user(user_id):
    return Uxser.query.get(int(user_id))

