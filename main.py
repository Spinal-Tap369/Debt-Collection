# main.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use your preferred database connection string
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with ID: {user_id}")
    try:
        user = User.query.get(int(user_id))
        print(f"Loaded user: {user}")
        return user
    except Exception as e:
        print(f"Error loading user: {e}")
        return None


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


# app.app_context().push()
# db.create_all()

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class AddLoanForm(FlaskForm):
    loan_number = StringField('Loan Number', validators=[DataRequired()])
    borrower_name = StringField('Borrower\'s Name', validators=[DataRequired()])
    amount_owed = StringField('Amount Owed', validators=[DataRequired()])
    borrower_address = StringField('Borrower\'s Address', validators=[DataRequired()])
    borrower_contact_number = StringField('Borrower\'s Contact Number', validators=[DataRequired()])

class EditLoanForm(FlaskForm):
    loan_number = StringField('Loan Number', validators=[DataRequired()])
    borrower_name = StringField('Borrower\'s Name', validators=[DataRequired()])
    amount_owed = StringField('Amount Owed', validators=[DataRequired()])
    borrower_address = StringField('Borrower\'s Address', validators=[DataRequired()])
    borrower_contact_number = StringField('Borrower\'s Contact Number', validators=[DataRequired()])

class DeleteLoanForm(FlaskForm):
    loan_number = StringField('Loan Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('loan_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, date_of_birth=form.date_of_birth.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/loan_dashboard')
@login_required
def loan_dashboard():
    loans = Loan.query.all()
    return render_template('loan_dashboard.html', loans=loans)

@app.route('/add_loan', methods=['GET', 'POST'])
@login_required
def add_loan():
    form = AddLoanForm()
    if form.validate_on_submit():
        # Check if loan number already exists
        existing_loan = Loan.query.filter_by(loan_number=form.loan_number.data).first()
        if existing_loan:
            flash('Loan number already exists. Please choose a different one.', 'danger')
        else:
            loan = Loan(loan_number=form.loan_number.data,
                        borrower_name=form.borrower_name.data,
                        amount_owed=form.amount_owed.data,
                        borrower_address=form.borrower_address.data,
                        borrower_contact_number=form.borrower_contact_number.data)
            db.session.add(loan)
            db.session.commit()
            flash('Loan added successfully.', 'success')
            return redirect(url_for('loan_dashboard'))
    return render_template('add_loan.html', form=form)

@app.route('/edit_loan', methods=['GET', 'POST'])
@login_required
def edit_loan():
    form = EditLoanForm()
    if form.validate_on_submit():
        loan = Loan.query.filter_by(loan_number=form.loan_number.data).first()
        if loan:
            # Update loan details based on form data
            loan.borrower_name = form.borrower_name.data
            loan.amount_owed = form.amount_owed.data
            loan.borrower_address = form.borrower_address.data
            loan.borrower_contact_number = form.borrower_contact_number.data
            db.session.commit()
            flash('Loan details updated successfully.', 'success')
            return redirect(url_for('loan_dashboard'))
        else:
            flash('Loan not found.', 'danger')
    return render_template('edit_loan.html', form=form)

@app.route('/delete_loan', methods=['GET', 'POST'])
@login_required
def delete_loan():
    form = DeleteLoanForm()
    if form.validate_on_submit():
        loan = Loan.query.filter_by(loan_number=form.loan_number.data).first()
        if loan:
            # Check if the password is correct
            if check_password_hash(current_user.password, form.password.data):
                db.session.delete(loan)
                db.session.commit()
                flash('Loan deleted successfully.', 'success')
                return redirect(url_for('loan_dashboard'))
            else:
                flash('Incorrect password.', 'danger')
        else:
            flash('Loan not found.', 'danger')
    return render_template('delete_loan.html', form=form)


# Implement other routes for add, edit, delete, and superadmin_dashboard


# Run the application
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
