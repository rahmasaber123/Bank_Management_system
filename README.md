
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

**Identify Loans Details**  


```sql

-- PROCEDURES
 DELIMITER $$

CREATE PROCEDURE GetLoanDetails(IN loan_id INT)
BEGIN
    SELECT l.LoanID, l.Amount, SUM(lp.AmountPaid) AS TotalPaid
    FROM loans l
    LEFT JOIN loanpayments lp ON l.LoanID = lp.LoanID
    WHERE l.LoanID = loan_id
    GROUP BY l.LoanID, l.Amount;
END $$

DELIMITER ;
CALL GetLoanDetails(114);



```


**Identify Total Payment Trasnact In Term Of Loans**  


```sql

DELIMITER $$

CREATE PROCEDURE GetTotalPayment(IN loan_id INT)
BEGIN
    SELECT SUM(lp.AmountPaid) / l.Amount AS PaymentRatio
    FROM loanpayments lp
    JOIN loans l ON lp.LoanID = l.LoanID
    WHERE l.LoanID = loan_id
    GROUP BY l.LoanID,l.Amount;
END $$

DELIMITER ;
 CALL GetTotalPayment(5);


```




**Average transaction amount per account**  

SELECT t.AccountID,
       AVG(t.Amount) AS avg_txn_amount,
       COUNT(*) AS txn_count
FROM Transactions t
GROUP BY t.AccountID
HAVING txn_count > 5
ORDER BY avg_txn_amount DESC
LIMIT 10;


```sql



```

**Loan repayment rate per loan**  

```sql


SELECT l.LoanID,
       l.CustomerID,
       l.Amount AS loan_amount,
       SUM(lp.AmountPaid) AS total_paid,
       CASE WHEN l.Amount > 0
     THEN SUM(lp.AmountPaid) / l.Amount -- This calculates how much of the loan has been paid as a ratio
     ELSE NULL
END AS repayment_ratio
FROM Loans l
LEFT JOIN LoanPayments lp ON lp.LoanID = l.LoanID
GROUP BY l.LoanID
ORDER BY repayment_ratio ASC
LIMIT 20;


```


**customers with >= 2 services**  


```sql


SELECT cs.CustomerID, c.FullName, COUNT(*) AS num_services
FROM Customer_Services cs
JOIN Customers c ON c.CustomerID = cs.CustomerID
GROUP BY cs.CustomerID
HAVING num_services >= 2
ORDER BY num_services DESC
LIMIT 20;


```

**Total balances attributable to each branch**  
  
```sql

WITH branch_customers AS (
  SELECT DISTINCT e.BranchID, ec.CustomerID
  FROM Employees_Customers ec
  JOIN Employees e ON ec.EmployeeID = e.EmployeeID
)
SELECT b.BranchID, b.BranchName,
       SUM(a.Balance) AS total_balance
FROM Branches b
JOIN branch_customers bc ON bc.BranchID = b.BranchID
JOIN Accounts a ON a.CustomerID = bc.CustomerID
GROUP BY b.BranchID
ORDER BY total_balance DESC;



```

**Flag accounts with suspicious same-day activity**


```sql


SELECT AccountID,
       DATE(TransactionDate) AS tx_date,
       COUNT(*) AS tx_count,
       SUM(Amount) AS total_amount
FROM Transactions
GROUP BY AccountID, DATE(TransactionDate)
HAVING tx_count > 10 OR total_amount > 10000; 


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
   git clone https://github.com/rahmasaber123/Bank_Management_system.git
   ```

2. **Set Up the Database**: Execute the SQL scripts in the `BANK_DB` file to create and populate the database.
3. **Run the Queries**: Use the SQL queries in the `BUSINESS_ANALYSIS.SQL` file to perform the analysis.
4. **Explore and Modify**: Customize the queries as needed to explore different aspects of the data or answer additional questions.

## Author - RAHMA SABER ABBAS 
