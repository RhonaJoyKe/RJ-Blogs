from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager
# modifies the load_userfunction by passing in a user_id to the function that queries the database and gets a User with that ID.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# user table
class User(UserMixin, db.Model):  
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
     # save user
    def save_user(self):
        db.session.add(self)
        db.session.commit()
        # generate password hash
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    # check password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    # login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    def __repr__(self):
        return f'User {self.username}'

class Blogs(db.Model):  
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='blog', lazy = 'dynamic')
    def save_blogs(self):
        db.session.add(self)
        db.session.commit()
    def repr(self):
        return f'Post {self.title}'

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    date_created=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Comment {self.name}'

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

class Quotes:
    """
     '''
    Quotes class to define Quotes Objects
    '''
    """
    def __init__(self,author,quote,url):
        
        self.author = author
        self.quote = quote
        self.url = url
       
        