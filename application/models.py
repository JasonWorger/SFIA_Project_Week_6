from application import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))  


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    Bar= db.relationship('Bar', backref='usersid', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Email: ', self.email, '\r\n',
            'Name: ', self.first_name, ' ', self.last_name
        ])

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    size = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    Bar= db.relationship('Bar', backref='supplier', lazy=True)


class Bar(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(30), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    stock_amount = db.Column(db.Integer, nullable=False)

