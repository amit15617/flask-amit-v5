from smartStore import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin



@login_manager.user_loader

def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
db.create_all()

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
db.create_all()

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer ,primary_key = True)
    name = db.Column(db.String,unique = True)
    description = db.Column(db.String)
    price = db.Column(db.String)
    category =  db.Column(db.String)

    def __init__(self,  name, description, price,category):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
db.create_all()


