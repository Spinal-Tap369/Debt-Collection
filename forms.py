from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, SubmitField
from wtforms.validators import DataRequired, EqualTo

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

class SearchLoanForm(FlaskForm):
    loan_number = StringField('Loan Number', validators=[DataRequired()])
    submit = SubmitField('Search')