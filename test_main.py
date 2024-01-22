import pytest
from datetime import datetime
from flask import url_for
from models import app, db, User, Loan


# Fixture to register a new user
@pytest.fixture
def register_user(client):
    def _register_user(username, password, date_of_birth):
        with app.app_context():
            db.create_all()
            user = User(username=username, password=password, date_of_birth=date_of_birth)
            db.session.add(user)
            db.session.commit()

    return _register_user


# Fixture to log in a user
@pytest.fixture
def login_user(client):
    def _login_user(username, password):
        return client.post('/login', data={'username': username, 'password': password})

    return _login_user


# Fixture to add a loan
@pytest.fixture
def add_loan(client):
    def _add_loan(loan_number, borrower_name, amount_owed, borrower_address, contact_number):
        return client.post('/add_loan', data={
            'loan_number': loan_number,
            'borrower_name': borrower_name,
            'amount_owed': amount_owed,
            'borrower_address': borrower_address,
            'contact_number': contact_number
        })

    return _add_loan


# Fixture to search for a loan
@pytest.fixture
def search_loan(client):
    def _search_loan(loan_number):
        return client.get(url_for('search_loan', loan_number=loan_number))

    return _search_loan


# Fixture to delete a loan
@pytest.fixture
def delete_loan(client):
    def _delete_loan(loan_number):
        return client.post(url_for('delete_loan', loan_number=loan_number))

    return _delete_loan


# Fixture to change user password
@pytest.fixture
def change_password(client):
    def _change_password(username, new_password):
        return client.post(url_for('change_password', username=username), data={'new_password': new_password})

    return _change_password


# Fixture to delete a user
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def delete_user(client):
    def _delete_user(username):
        return client.post(url_for('delete_user', username=username))

    return _delete_user


# Test the entire scenario
def test_complete_scenario(register_user, login_user, add_loan, search_loan, delete_loan, delete_user, change_password,
                           client):
    # Register new user
    register_user('tim123', 'tim123', '12/9/2012')

    # Login using tim123
    login_response = login_user('tim123', 'tim123')
    assert login_response.status_code == 200

    # Add a loan
    add_loan_response = add_loan(99999, 'Sanjay', 1000, 'Mumbai', 100)
    assert add_loan_response.status_code == 200

    # Search for the loan
    search_response = search_loan(99999)
    assert search_response.status_code == 200

    # Delete the loan
    delete_response = delete_loan(99999)
    assert delete_response.status_code == 200

    # Logout the user
    logout_response = client.get('/logout')
    assert logout_response.status_code == 200

    # Login as SysAdmin
    login_response_sysadmin = login_user('sysadmin', 'root69')
    assert login_response_sysadmin.status_code == 200

    # Change password of user tim123 to 1234root
    change_password_response = change_password('tim123', '1234root')
    assert change_password_response.status_code == 200

    # Delete the user tim123
    delete_user_response = delete_user('tim123')
    assert delete_user_response.status_code == 200

    # Logout of SysAdmin
    logout_sysadmin_response = client.get('/logout')
    assert logout_sysadmin_response.status_code == 200
