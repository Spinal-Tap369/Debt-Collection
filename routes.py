from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Loan, db
from forms import LoginForm, AddLoanForm, EditLoanForm, DeleteLoanForm, RegistrationForm, SearchLoanForm, ChangePasswordForm

def login_user_redirect(user, role, page):
    login_user(user)
    flash(f"Logged in as {role}, User ID: {user.id}", 'success')
    return redirect(url_for(page))

def handle_invalid_login():
    flash('Invalid username or password', 'danger')
    print(f"Login failed. Form data: {request.form}")

def handle_existing_loan():
    flash('Loan number already exists. Please choose a different one.', 'danger')

def handle_loan_not_found():
    flash('Loan not found.', 'danger')

def handle_password_mismatch():
    flash('Incorrect password.', 'danger')

def handle_user_not_found():
    flash('User not found.', 'danger')

def handle_access_denied():
    flash('Access denied. You do not have permission to perform this action.', 'danger')

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if not form.validate_on_submit():
            handle_invalid_login()
            return render_template('login.html', form=form)

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            handle_invalid_login()
            return render_template('login.html', form=form)

        role = 'Sysadmin' if user.username == 'sysadmin' else user.username
        page = 'sysadmin' if user.username == 'sysadmin' else 'loan_dashboard'
        return login_user_redirect(user, role, page)

    @app.route('/sysadmin', methods=['GET', 'POST'])
    @login_required
    def sysadmin():
        if not (current_user.is_authenticated and current_user.username == 'sysadmin'):
            handle_access_denied()
            return redirect(url_for('login'))

        users = User.query.all()
        return render_template('sysadmin.html', users=users)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()

        if not form.validate_on_submit():
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, date_of_birth=form.date_of_birth.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

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
            existing_loan = Loan.query.filter_by(loan_number=form.loan_number.data).first()
            if existing_loan:
                handle_existing_loan()
            else:
                add_loan_to_database(form)
                return redirect(url_for('loan_dashboard'))
        return render_template('add_loan.html', form=form)

    @app.route('/edit_loan', methods=['GET', 'POST'])
    @login_required
    def edit_loan():
        form = EditLoanForm()

        if form.validate_on_submit():
            loan = Loan.query.filter_by(loan_number=form.loan_number.data).first()
            if not loan:
                handle_loan_not_found()
            elif request.method == 'POST':
                update_loan_details(loan, form)
                return redirect(url_for('loan_dashboard'))

        return render_template('edit_loan.html', form=form)

    @app.route('/delete_loan', methods=['GET', 'POST'])
    @login_required
    def delete_loan():
        form = DeleteLoanForm()

        if form.validate_on_submit():
            handle_loan_deletion(form)

        return render_template('delete_loan.html', form=form)

    @app.route('/get_loan_details', methods=['GET'])
    @login_required
    def get_loan_details():
        loan_number = request.args.get('loan_number')
        loan = Loan.query.filter_by(loan_number=loan_number).first()

        if loan:
            return jsonify(create_loan_details_dict(loan))
        return jsonify({'error': 'Loan not found'}), 404

    @app.route('/search_loan', methods=['GET', 'POST'])
    @login_required
    def search_loan():
        form = SearchLoanForm()

        if form.validate_on_submit():
            loan = search_loan_by_number(form.loan_number.data)
            if loan:
                return render_template('search_loan.html', loan_details=create_loan_details_dict(loan))
            handle_loan_not_found()

        return render_template('search_loan.html', form=form)

    @app.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def change_password(user_id):
        user = User.query.get(user_id)
        if not user:
            handle_user_not_found()
            return redirect(url_for('sysadmin'))

        form = ChangePasswordForm()

        if request.method == 'POST' and form.validate_on_submit():
            change_user_password(user, form.new_password.data)
            return redirect(url_for('sysadmin'))

        return render_template('change_password.html', form=form, user=user)

    @app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def delete_user(user_id):
        if current_user.is_authenticated and current_user.username == 'sysadmin':
            handle_user_deletion(user_id)
            return redirect(url_for('sysadmin'))
        handle_access_denied()
        return redirect(url_for('login'))

# Helper functions

def add_loan_to_database(form):
    loan = Loan(
        loan_number=form.loan_number.data,
        borrower_name=form.borrower_name.data,
        amount_owed=form.amount_owed.data,
        borrower_address=form.borrower_address.data,
        borrower_contact_number=form.borrower_contact_number.data
    )
    db.session.add(loan)
    db.session.commit()
    flash('Loan added successfully.', 'success')

def update_loan_details(loan, form):
    loan.borrower_name = form.borrower_name.data
    loan.amount_owed = form.amount_owed.data
    loan.borrower_address = form.borrower_address.data
    loan.borrower_contact_number = form.borrower_contact_number.data
    db.session.commit()
    flash('Loan details updated successfully.', 'success')

def handle_loan_deletion(form):
    loan_number = form.loan_number.data
    loan = Loan.query.filter_by(loan_number=loan_number).first()

    if loan:
        if check_password_hash(current_user.password, form.password.data):
            db.session.delete(loan)
            db.session.commit()
            flash('Loan deleted successfully.', 'success')
            return redirect(url_for('loan_dashboard'))
        else:
            handle_password_mismatch()
    else:
        handle_loan_not_found()

def create_loan_details_dict(loan):
    return {
        'loan_number': loan.loan_number,
        'borrower_name': loan.borrower_name,
        'amount_owed': loan.amount_owed,
        'borrower_address': loan.borrower_address,
        'borrower_contact_number': loan.borrower_contact_number
    }

def search_loan_by_number(loan_number):
    return Loan.query.filter_by(loan_number=loan_number).first()

def change_user_password(user, new_password):
    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
    user.password = hashed_password
    db.session.commit()
    flash('Password changed successfully.', 'success')

def handle_user_deletion(user_id):
    user = User.query.get(user_id)
    if not user:
        handle_user_not_found()
        return

    if user.username == 'sysadmin':
        flash('Cannot delete sysadmin.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} deleted.", 'success')