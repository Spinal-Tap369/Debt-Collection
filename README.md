# About Debt-Collection
A simple Debt Collection (Vasooli) manager created using the Flask framework.
An employee of a debt collection agency(user) will login to this application and will manually create new records of people given debts by loan sharks.
They will update the records daily in case a payment is made by the borrower. 
After a debt has been paid in full, the record will be deleted!

___

# Languages used
1. Python - Uses the Flask Framework
2. HTML, CSS and Bootstrap 

___

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

___


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


___


# UML Diagrams :
* UML or Unified Modeling Language Diagrams are ways to represent the design, architecture and working of an application.
1. ### Use case diagram:
* As of now, there is only one user model defined who can login, register, logout, View the loan dashboard, perform actions on Loans like Add, delete, edit and search loan and View loan records.
Use case diagram : https://github.com/Spinal-Tap369/Debt-Collection/blob/main/uml/use_case_diagram.png
2. ### Class Diagram:
* There are two main classes, Loan and User. The remaining classes are forms which are used for the various operations such as login, register, add loan, search loan, delete loan and edit loan etc.
Class diagram : https://github.com/Spinal-Tap369/Debt-Collection/blob/main/uml/class_diagram.png
3. ### Activity Diagram:
* The activity diagram describes the workflow of the Debt Collection Manager.
Activity Diagram : https://github.com/Spinal-Tap369/Debt-Collection/blob/main/uml/activity_diagram.png
___
# DDD
In order to make good use of the 100,000,000 euros provided by Edlich-Investment, this simple application can have much more domains and functionalities.
## Event storming:
During the following domains were decided.
### 1. Loan Application: 
Deals with Loan application processes such as submitting an application, approving/rejecting etc.
### 2. User Authentication:
This Domain will take of registering and logging-in/logging-out the various users of this application.
### 3. Loan processing:
Deals with various aspects of a loan such as disbursement, check if it is repaid or has the loan been defaulted.
### 4. Risk Assessment: 
Risk Assessment domain will have a part in deciding weather a loan is provided to an applicant or not.
### 5. Payment gateway:
This domain will take care of all payment related operations in our application
### 6. Notification:
As the name suggests, this domain deals with sending Notifications to users.
### 7. Audit Log:
The Audit log domain will create logs such as payment history, borrower track record, collateral details etc.
### 8. Credit Score:
This domain is responsible to check and send updates regarding Credit score.

## Core Domain Chart:
https://github.com/Spinal-Tap369/Debt-Collection/blob/main/uml/Domain_rel_diagram.png
## Relation between the Domains:
### Loan App and User Auth:
* User registration triggers Loan Application creation.
* User login is required for loan application submission.
### Loan App and Loan Processing:
* Loan approval triggers loan processing events.
* Loan rejection leads to further handling in loan processing.
### Loan Processing and Risk Assessment:
* Risk assessment events influence loan processing decisions.
### Loan Processing and Payment Gateway:
* Loan issuance triggers payment initiation.
* Successful payments lead to loan repayment events.
### Notification and Loan Processing:
* Notifications are sent based on loan processing events.
### Audit Logging and all Domains:
* Audit logs are created for important events across all domains.
### Credit Scoring and Loan Processing:
* Credit score checking is part of the risk assessment in loan processing.







