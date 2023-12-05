# main.py
from flask import  render_template, redirect, url_for, flash, request, jsonify
from models import app, db, User, Loan
from forms import LoginForm, RegistrationForm, AddLoanForm, EditLoanForm, DeleteLoanForm, SearchLoanForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


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


@app.route('/get_loan_details', methods=['GET'])
@login_required
def get_loan_details():
    loan_number = request.args.get('loan_number')
    loan = Loan.query.filter_by(loan_number=loan_number).first()

    if loan:
        loan_details = {
            'loan_number': loan.loan_number,
            'borrower_name': loan.borrower_name,
            'amount_owed': loan.amount_owed,
            'borrower_address': loan.borrower_address,
            'borrower_contact_number': loan.borrower_contact_number
        }
        return jsonify(loan_details)

    return jsonify({'error': 'Loan not found'}), 404


@app.route('/search_loan', methods=['GET', 'POST'])
@login_required
def search_loan():
    form = SearchLoanForm()  # You need to create a WTForms form for this

    if form.validate_on_submit():
        loan_number = form.loan_number.data
        loan = Loan.query.filter_by(loan_number=loan_number).first()

        if loan:
            loan_details = {
                'loan_number': loan.loan_number,
                'borrower_name': loan.borrower_name,
                'amount_owed': loan.amount_owed,
                'borrower_address': loan.borrower_address,
                'borrower_contact_number': loan.borrower_contact_number
            }
            return render_template('search_loan.html', loan_details=loan_details)

        flash('Loan not found.', 'danger')

    return render_template('search_loan.html', form=form)



# Implement other routes for add, edit, delete, and superadmin_dashboard


# Run the application
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)