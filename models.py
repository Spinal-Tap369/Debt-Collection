# models.py

from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use your preferred database connection string
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_number = db.Column(db.String(20), unique=True, nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    amount_owed = db.Column(db.Float, nullable=False)
    borrower_address = db.Column(db.String(200), nullable=False)
    borrower_contact_number = db.Column(db.String(15), nullable=False)

