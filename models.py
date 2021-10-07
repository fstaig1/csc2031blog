from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    blogs = db.relationship('Post')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False, default=False)
    body = db.Column(db.Text, nullable=False, default=False)

    def __init__(self, username, title, body):
        self.username = username
        self.created = datetime.now()
        self.title = title
        self.body = body


def init_db():
    db.drop_all()
    db.create_all()
    new_user = User(username='user1@test.com', password='mysecretpassword')
    db.session.add(new_user)
    db.session.commit()
