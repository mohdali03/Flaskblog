from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20),  nullable=False, default="default.jpg")
    password = db.Column(db.String(20),  nullable=False)
    posts = db.relationship("Post", backref='author', lazy=True)
    
    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password
            
     
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}' )"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}' )"

