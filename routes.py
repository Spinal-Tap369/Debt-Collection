# routes.py

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Loan, db
from forms import LoginForm, AddLoanForm, EditLoanForm, DeleteLoanForm, RegistrationForm, SearchLoanForm, ChangePasswordForm


def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            # Query the user by username
            user = User.query.filter_by(username=form.username.data).first()

            if user:
                # Check the password using the correct hashing method (pbkdf2:sha256)
                if check_password_hash(user.password, form.password.data):
                    # Check if the user is sysadmin
                    if user.username == 'sysadmin':
                        login_user(user)
                        flash(f"Logged in as Sysadmin", 'success')
                        return redirect(url_for('sysadmin'))
                    else:
                        login_user(user)
                        flash(f"Logged in as {user.username}, User ID: {user.id}", 'success')
                        return redirect(url_for('loan_dashboard'))
                else:
                    flash('Invalid username or password', 'danger')
                    print(f"Password Mismatch! Login failed. Form data: {request.form}")
            else:
                flash('Invalid username or password', 'danger')
                print(f"User not found. Login failed. Form data: {request.form}")

        return render_template('login.html', form=form)

    @app.route('/sysadmin', methods=['GET', 'POST'])
    @login_required
    def sysadmin():
        # Check if the current user is authenticated and has the username 'sysadmin'
        if current_user.is_authenticated and current_user.username == 'sysadmin':
            users = User.query.all()
            return render_template('sysadmin.html', users=users)  # Pass 'users' to the template
        else:
            flash('Access denied. You do not have permission to view this page.', 'danger')
            return redirect(url_for('login'))

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

    # ...

    @app.route('/edit_loan', methods=['GET', 'POST'])
    @login_required
    def edit_loan():
        form = EditLoanForm()

        if form.validate_on_submit():
            loan = Loan.query.filter_by(loan_number=form.loan_number.data).first()
            if not loan:
                flash('Loan not found.', 'danger')
            elif request.method == 'POST':
                # Update loan details based on form data
                loan.borrower_name = form.borrower_name.data
                loan.amount_owed = form.amount_owed.data
                loan.borrower_address = form.borrower_address.data
                loan.borrower_contact_number = form.borrower_contact_number.data
                db.session.commit()
                flash('Loan details updated successfully.', 'success')
                return redirect(url_for('loan_dashboard'))

        return render_template('edit_loan.html', form=form)

    @app.route('/delete_loan', methods=['GET', 'POST'])
    @login_required
    def delete_loan():
        form = DeleteLoanForm()

        if form.validate_on_submit():
            loan_number = form.loan_number.data
            loan = Loan.query.filter_by(loan_number=loan_number).first()

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

    @app.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def change_password(user_id):
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('sysadmin'))

        form = ChangePasswordForm()

        if request.method == 'POST' and form.validate_on_submit():
            current_password = form.current_password.data
            new_password = form.new_password.data

            if not user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('change_password', user_id=user.id))

            # Update the password using generate_password_hash with the same method used during registration
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            user.password = hashed_password
            db.session.commit()

            flash('Password changed successfully.', 'success')
            return redirect(url_for('sysadmin'))

        return render_template('change_password.html', form=form, user=user)

    @app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def delete_user(user_id):
        if current_user.is_authenticated and current_user.username == 'sysadmin':
            user = User.query.get(user_id)
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('sysadmin'))

            # Do not allow deletion of sysadmin
            if user.username == 'sysadmin':
                flash('Cannot delete sysadmin.', 'danger')
            else:
                db.session.delete(user)
                db.session.commit()
                flash(f"User {user.username} deleted.", 'success')

            return redirect(url_for('sysadmin'))
        else:
            flash('Access denied. You do not have permission to perform this action.', 'danger')
            return redirect(url_for('login'))