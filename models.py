from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime
import base64
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet


def encrypt(data, postkey):
    return Fernet(postkey).encrypt(bytes(data, 'utf-8'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # crypto key for user's posts
    postkey = db.Column(db.BLOB)

    blogs = db.relationship('Post')

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.postkey = base64.urlsafe_b64encode(scrypt(password, str(get_random_bytes(32)), 32, N=2 ** 14, r=8, p=1))


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False, default=False)
    body = db.Column(db.Text, nullable=False, default=False)

    def __init__(self, username, title, body, postkey):
        self.username = username
        self.created = datetime.now()
        self.title = encrypt(title, postkey)
        self.body = encrypt(body, postkey)

    def update_post(self, title, body, postkey):
        self.title = encrypt(title, postkey)
        self.body = encrypt(body, postkey)
        db.session.commit()


def init_db():
    db.drop_all()
    db.create_all()
    new_user = User(username='user1@test.com', password='mysecretpassword')
    newuser2 = User(username='ac@abc.com', password='user2passwordwoop')
    db.session.add(new_user)
    db.session.add(newuser2)
    db.session.commit()
