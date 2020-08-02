from application import db, login_manager


#Name of database: stocklistdb

# User table
class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(id):
    return users.query.get(int(id))   

    # def __repr__(self):
    #     return ''.join([
    #         'User ID: ', str(self.id), '\r\n',
    #         'Email: ', self.email, '\r\n',
    #         'Name: ', self.first_name, ' ', self.last_name
    #     ])

#stock table
class product(db.Model):

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)



#bar table
class bar(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String, db.ForeignKey('product.brand_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    stock_amount = db.Column(db.Integer, nullable=False)

#posts= db.realtionship('Posts', backref='author', lazy=True)

#user_id = db.Columns(db.Integer, db.Foreigney('users.id'), nullable=False)