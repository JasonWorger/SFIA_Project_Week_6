from application import db
from application.models import Users, Stock, Product

db.drop_all()
db.create_all()