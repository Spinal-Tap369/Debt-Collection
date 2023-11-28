
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use your preferred database connection string
db = SQLAlchemy(app)

# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_number = db.Column(db.String(20), unique=True, nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    amount_owed = db.Column(db.Float, nullable=False)
    borrower_address = db.Column(db.String(200), nullable=False)
    borrower_contact_number = db.Column(db.String(15), nullable=False)


# Run these on Terminal to create DB, after importing app and db from models.py
# app.app_context().push()
# db.create_all()