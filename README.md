# Debt-Collection
A simple Debt Collection (Vasooli) manager created using the Flask framework.
An employee of a debt collection agency(user) will login to this application and will manually create new records of people given debts by loan sharks.
They will update the records daily in case a payment is made by the borrower. 
After a debt has been paid in full, the record will be deleted!

# Requirements
* The Various features to be added to the Debt-Collection manager has been planned out on Jira : https://spinal-tap369.atlassian.net/jira/software/projects/SCRUM/boards/1
## Functional Requirements
1. ### User Authentication:
* Users must be able to register for an account.
* Registered users should be able to log in securely.
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
* Error messages should be informative and user-friendly.
3. ### Security:
* The application must protect against common security threats such as SQL injection and cross-site scripting (XSS).
4. ### Scalability: 
* The architecture should allow for easy scalability to accommodate potential future growth.



