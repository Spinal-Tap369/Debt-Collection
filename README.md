# About Debt-Collection
A simple Debt Collection (Vasooli) manager created using the Flask framework.
An employee of a debt collection agency(user) will login to this application and will manually create new records of people given debts by loan sharks.
They will update the records daily in case a payment is made by the borrower. 
After a debt has been paid in full, the record will be deleted!


# Languages used
1. Python - Uses the Flask Framework
2. HTML, CSS and Bootstrap 


# Requirements Engineering
* The Various features to be added to the Debt-Collection manager has been planned out on Jira : https://spinal-tap369.atlassian.net/jira/software/projects/SCRUM/boards/1
## Functional Requirements
1. ### User Authentication:
* Users are working for the Debt Collection firm and must be able to register for an account for the Debt-Collection manager.
* User sessions should be managed to ensure secure access to the system.
2. ### Loan Management:
* Users should be able to add a new loan record, providing necessary details such as loan number, borrower name, amount owed, borrower address, and contact number.
* Users can view a dashboard displaying a list of all loans.
* The system must support the searching, editing, and deletion of loans.
3. ### Loan Details:
* Users can view detailed information about a specific loan, including borrower details and the amount owed.
4. ### Search Functionality:
* Users should be able to search for a specific loan by its loan number.
5. ### Security:
* Passwords must be securely hashed and stored.
* User sessions must be secure and protected against common web vulnerabilities.
## Non-Functional Requirements
1. ### Performance: 
* The system should handle a reasonable number of concurrent users without significant performance degradation.
2. ### Usability:
* The user interface should be intuitive and easy to navigate.
3. ### Scalability: 
* The architecture should allow for easy scalability to accommodate potential future growth.


# Installation
## Pre-requisites:
1. ### The latest Python or a Python IDE such as PyCharm Community Edition
2. ### The following Python libraries :
* Flask
* Flask-SQLAlchemy
* Flask-WTF
* Flask-login
* werkzeug (For hashing passwords)
## Getting it to run:
* After you have setup your project on your IDE and have installed the above-mentioned packages, Clone this git.
* After cloning, you will need to create a Database using the below-mentioned steps
1. open python console
2. type - from models import app, db
3. type - app.app_context().push()
4. type - db.create_all()
* This will create the Database.
* After Database if created, open the Terminal and run the command - python main.py
* This will run the website on port 5000 on your local machine. /127.0.0.1:5000





