from . import db
from flask_login import UserMixin

# Define the TXTRecords model 
class TXTRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text =  db.Column(db.String(50))
    now = db.Column(db.String(50))

# Define the User model for storing user information
class User(db.Model, UserMixin):
    # Define table columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    txt_records = db.relationship('TXTRecords')  