
# BANK_MANAGMENT_SYSTEM 


## Project Overview

**Project Title**:Bank Management System  

**Database**: `Bank_DB`
This project demonstrates how to integrate MySQL with Python for managing and analyzing datasets.
The data is cleaned and organized using SQL queries, then analyzed and visualized in Python to generate insights.
It represents a complete workflow from database management to data-driven decision-making.

![BANK_PROJECT](https://github.com/rahmasaber123/Bank_Management_system/blob/main/BANK.jpeg?raw=true)

## Objectives

1. **Database Integration: Connect Python with MySQL to store, retrieve, and manage datasets effectively
2. **Data Cleaning & Preparation: Use SQL queries to clean, filter, and structure raw data for analysis.
3. **CRUD Operations: Perform Create, Read, Update, and Delete operations on the database.
4. **End-to-End Workflow: Demonstrate the complete process from database management in MySQL to generating insights
5. **Business Analysis: Applying Advanced Queries Using MySQL 

## Project Structure

### 1. Database Setup
![ERD](https://raw.githubusercontent.com/rahmasaber123/Bank_Management_system/aa831f1c0e951438813f0295af3c9b83561327fd/SCHEMAA.jpeg)

- **Database Creation**: Created a database named `BANK_MANAGEMENT_SYSTEM`.
- **Table Creation**: Created tables for CUSTOMERS,EMPLOYEES,SERVICES,LOANS,BRANCHES,TRANSACTION.

```sql
CREATE DATABASE Bank;
USE Bank;

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(100),
    Email VARCHAR(60),
    Phone VARCHAR(20),
    Address VARCHAR(100),
    Date_Of_Birth DATE
);

CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT,
    AccountType VARCHAR(30),
    Balance NUMERIC,
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    TransactionDate DATE,
    Amount NUMERIC,
    TransactionType VARCHAR(50),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Loans (
    LoanID INT PRIMARY KEY,
    CustomerID INT,
    LoanType VARCHAR(50),
    Amount NUMERIC,
    Status VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

```

### 2. CRUD Operations

- **Create**: Create: Inserted new records into MySQL tables through Python.
- **Read**: Retrieved and displayed data using SQL queries
- **Update**:Modified existing records in the database Using SQL
  


**UPDATED SERVICES TABLE 
```sql
UPDATE Services
SET ServiceName = CASE ServiceID
    WHEN 1 THEN 'Loan Services'
    WHEN 2 THEN 'Online Banking'
    WHEN 3 THEN 'Saving Accounts'
    WHEN 4 THEN 'Fixed Deposit'
    WHEN 5 THEN 'Loan Services'
    WHEN 6 THEN 'Online Banking'
    WHEN 7 THEN 'Saving Accounts'
    WHEN 8 THEN 'Fixed Deposit'
    WHEN 9 THEN 'Loan Services'
    WHEN 10 THEN 'Online Banking'
END,
Description = CASE ServiceID
    WHEN 1 THEN 'Provides personal, home, and business loans.'
    WHEN 2 THEN 'Secure internet-based banking services.'
    WHEN 3 THEN 'Accounts for saving money with interest.'
    WHEN 4 THEN 'Fixed-term deposits with higher interest rates.'
    WHEN 5 THEN 'Provides personal, home, and business loans.'
    WHEN 6 THEN 'Secure internet-based banking services.'
    WHEN 7 THEN 'Accounts for saving money with interest.'
    WHEN 8 THEN 'Fixed-term deposits with higher interest rates.'
    WHEN 9 THEN 'Provides personal, home, and business loans.'
    WHEN 10 THEN 'Secure internet-based banking services.'
END; 


```

**CREATE TABLES AS SELECT TO HELP IN REPORTING PROCESS(SHOWING CUSTOMERS WHO PASSED THE LOAN PERIOD )
```sql
CREATE TABLE overdue_loans AS
SELECT 
    l.LoanID, 
    l.CustomerID, 
    l.Amount AS loan_amount,
    SUM(lp.AmountPaid) AS total_paid,
    l.EndDate,
    SUM(lp.AmountPaid) / l.Amount AS repayment_ratio
FROM Loans l
LEFT JOIN LoanPayments lp 
    ON lp.LoanID = l.LoanID
GROUP BY l.LoanID, l.CustomerID, l.Amount, l.EndDate
HAVING 
l.EndDate < CURRENT_DATE()       -- loan has already ended
AND SUM(lp.AmountPaid) < 0.5 * l.Amount;  -- paid less than 50% of total loan

SELECT * FROM overdue_loans;

--



```
### 3. CTAS (Create Table As Select)
**CREATE TABLES AS SELECT TO HELP IN REPORTING PROCESS(SHOWINGREMAINING BALANCE IN CUSTOMERS ACCOUNT )
```sql
CREATE TABLE loan_remaining_balance AS
SELECT 
    l.LoanID,
    l.Amount AS original_amount,
    SUM(lp.AmountPaid) AS total_paid,
    (l.Amount - SUM(lp.AmountPaid)) AS remaining_balance
FROM Loans l
LEFT JOIN LoanPayments lp 
    ON l.LoanID = lp.LoanID
GROUP BY l.LoanID, l.Amount;
SELECT * FROM loan_remaining_balance ;



```



## Advanced SQL Operations

**Task 13: Identify Members with Overdue Books**  
Write a query to identify members who have overdue books (assume a 300-day return period). Display the member's_id, member's name, book title, issue date, and days overdue.

```sql



```


**Task 14: Update Book Status on Return**  
Write a query to update the status of books in the books table to "Yes" when they are returned (based on entries in the return_status table).


```sql



```




**Task 15: Branch Performance Report**  
Create a query that generates a performance report for each branch, showing the number of books issued, the number of books returned, and the total revenue generated from book rentals.

```sql



```

**Task 16: CTAS: Create a Table of Active Members**  
Use the CREATE TABLE AS (CTAS) statement to create a new table active_members containing members who have issued at least one book in the last 20 months.

```sql



```


**Task 17: Find Employees with the Most Book Issues Processed**  
Write a query to find the top 3 employees who have processed the most book issues. Display the employee name, number of books processed, and their branch.

```sql
SELECT EMP_NAME,B.*,COUNT(IST.ISSUED_ID) AS NUM_BOOK_ISSUED
FROM ISSUED_STATUS IST
   JOIN
   EMPLOYEES E
ON E.EMP_ID=IST.ISSUED_EMP_ID
  JOIN BRANCH B
ON B.BRANCH_ID = E.BRANCH_ID
  GROUP BY 1,2
ORDER BY COUNT(IST.ISSUED_ID)
   LIMIT 3;

```

**Task 18: Identify Members Issuing High-Risk Books**  
Write a query to identify members who have issued books more than twice with the status "damaged" in the books table. Display the member name, book title, and the number of times they've issued damaged books.    
```sql
SELECT M.MEMBER_NAME, 
  B.BOOK_TITLE ,
COUNT(IST.ISSUED_BOOK_ISBN) AS HIGH_RISK_BOOKS
FROM ISSUED_STATUS IST
   LEFT JOIN RETURN_STATUS RS
ON IST.ISSUED_ID =RS.ISSUED_ID 
   JOIN MEMBERS M
ON M.MEMBER_ID=ISSUED_MEMBER_ID
   JOIN BOOKS B 
ON B.ISBN = IST.ISSUED_BOOK_ISBN 
   WHERE RS.BOOK_QUALITY ='Damaged'
GROUP BY 1,2
   HAVING count(RS.BOOK_QUALITY)>2;


```

**Task 19: Stored Procedure**
Objective:
Create a stored procedure to manage the status of books in a library system.
Description:
Write a stored procedure that updates the status of a book in the library based on its issuance. The procedure should function as follows:
The stored procedure should take the book_id as an input parameter.
The procedure should first check if the book is available (status = 'yes').
If the book is available, it should be issued, and the status in the books table should be updated to 'no'.
If the book is not available (status = 'no'), the procedure should return an error message indicating that the book is currently not available.

```sql

CREATE OR REPLACE PROCEDURE issue_book(p_issued_id VARCHAR(10), p_issued_member_id VARCHAR(30), p_issued_book_isbn VARCHAR(30), p_issued_emp_id VARCHAR(10))
LANGUAGE plpgsql
AS $$

DECLARE
-- all the variabable
    v_status VARCHAR(10);

BEGIN
-- all the code
    -- checking if book is available 'yes'
    SELECT 
        status 
        INTO
        v_status
    FROM books
    WHERE isbn = p_issued_book_isbn;

    IF v_status = 'yes' THEN

        INSERT INTO issued_status(issued_id, issued_member_id, issued_date, issued_book_isbn, issued_emp_id)
        VALUES
        (p_issued_id, p_issued_member_id, CURRENT_DATE, p_issued_book_isbn, p_issued_emp_id);

        UPDATE books
            SET status = 'no'
        WHERE isbn = p_issued_book_isbn;

        RAISE NOTICE 'Book records added successfully for book isbn : %', p_issued_book_isbn;


    ELSE
        RAISE NOTICE 'Sorry to inform you the book you have requested is unavailable book_isbn: %', p_issued_book_isbn;
    END IF;
END;
$$

-- Testing The function
SELECT * FROM books;
-- "978-0-553-29698-2" -- yes
-- "978-0-375-41398-8" -- no
SELECT * FROM issued_status;

CALL issue_book('IS155', 'C108', '978-0-553-29698-2', 'E104');
CALL issue_book('IS156', 'C108', '978-0-375-41398-8', 'E104');

SELECT * FROM books
WHERE isbn = '978-0-375-41398-8'

```



**Task 20: Create Table As Select (CTAS)**
Objective: Create a CTAS (Create Table As Select) query to identify overdue books and calculate fines.

Description: Write a CTAS query to create a new table that lists each member and the books they have issued but not returned within 30 days. The table should include:
    The number of overdue books.
    The total fines, with each day's fine calculated at $0.50.
    The number of books issued by each member.
    The resulting table should show:
    Member ID
    Number of overdue books
    Total fines

```sql

 SELECT  M.member_id, 
	M.member_name, 
	COUNT(member_id) AS books_overdue,
	SUM((CURRENT_DATE - (iST.issued_date + INTERVAL '30 Days')::DATE) * 0.50) AS total_fines	--::DATE MAKES SURE IT RETURNS DATE TYPE
FROM members AS M
JOIN issued_status AS iST
	ON iST.issued_member_id = M.member_id
LEFT JOIN return_status AS RS
	ON RS.issued_id = IST.issued_id
JOIN books AS b
	ON b.isbn = iST.issued_book_isbn
WHERE return_date IS NULL 
	AND CURRENT_DATE - (iST.issued_date + INTERVAL '30 Days')::DATE > 0
GROUP BY 1,2;

```
## Reports

- **Database Schema**: Detailed table structures and relationships.
- **Data Analysis**: Insights into SERVICES, LOANSPAYMENT, CUSTOMERS BEHAVIORS, and BRANCHES.
- **Summary Reports**: Aggregated data on high-demand TRANSACTONS and LOANSPAYMENT performance.

## Conclusion

This project demonstrates the application of SQL skills in creating and managing a library management system. It includes database setup, data manipulation Using Python , and advanced querying, providing a solid foundation for data management and analysis.

## How to Use

1. **Clone the Repository**: Clone this repository to your local machine.
   ```sh
   git clone 
   ```

2. **Set Up the Database**: Execute the SQL scripts in the `BANK_DB` file to create and populate the database.
3. **Run the Queries**: Use the SQL queries in the `BUSINESS_ANALYSIS.SQL` file to perform the analysis.
4. **Explore and Modify**: Customize the queries as needed to explore different aspects of the data or answer additional questions.

## Author - RAHMA SABER ABBAS 
