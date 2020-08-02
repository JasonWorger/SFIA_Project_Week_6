from application import db
from application.models import Users, Bar, Product

db.drop_all()
db.create_all()