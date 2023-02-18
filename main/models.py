
from main import db, login_manager
from main import bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    about = db.Column(db.String(length=250), nullable=False)


    @property
    def password(self):
        return self.password 
    
    @password.setter
    def password(self, plain_text):
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Activity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    author = db.Column(db.String(length=50), nullable=False)
    desc = db.Column(db.String(length=250), nullable=False)



class Blog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    blogname = db.Column(db.String(length=50), nullable=False, unique=True)
    author = db.Column(db.String(length=50), nullable=False)
    content = db.Column(db.String(length=250), nullable=False)

    