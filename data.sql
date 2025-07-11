/* Queries for initial database creation to support and manage user loans, savings, and bank balances */

-- Database creation
CREATE DATABASE IF NOT EXISTS VillageBankingDB; -- Create the database if it doesn't exist

USE VillageBankingDB; -- Use the created database

-- Table to store user data
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each user
    name VARCHAR(100) NOT NULL,             -- Full name of the user
    email VARCHAR(100) UNIQUE NOT NULL,     -- Email address of the user
    phone VARCHAR(15) UNIQUE,               -- Phone number of the user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the user was created
);

-- Table to store loan data
CREATE TABLE Loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each loan
    user_id INT NOT NULL,                   -- Foreign key linking to the Users table
    principal DECIMAL(10, 2) NOT NULL,      -- Loan principal amount
    interest_rate DECIMAL(5, 2) NOT NULL,   -- Monthly interest rate (as a percentage, e.g., 10 for 10%)
    installments INT NOT NULL,              -- Number of installments (months)
    total_payment DECIMAL(10, 2) NOT NULL,  -- Total payment for the loan
    total_interest DECIMAL(10, 2) NOT NULL, -- Total interest paid for the loan
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the loan was created
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE -- Link to Users table
);

-- Adjusted LoanPayments table
CREATE TABLE LoanPayments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each payment
    loan_id INT NOT NULL,                      -- Foreign key linking to the Loans table
    month INT NOT NULL,                        -- Month number of the payment
    monthly_payment DECIMAL(10, 2) NOT NULL,   -- Total payment for the month
    monthly_interest DECIMAL(10, 2) NOT NULL,  -- Interest paid for the month
    principal_payment DECIMAL(10, 2) NOT NULL, -- Principal portion of the payment
    due_date DATE NOT NULL,                    -- Due date for the payment
    status ENUM('pending', 'paid') DEFAULT 'pending', -- Payment status
    FOREIGN KEY (loan_id) REFERENCES Loans(loan_id) ON DELETE CASCADE
);

-- Table to store savings data
CREATE TABLE Savings (
    savings_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each savings entry
    user_id INT NOT NULL,                      -- Foreign key linking to the Users table
    monthly_savings DECIMAL(10, 2) NOT NULL,   -- Amount saved each month
    interest_rate DECIMAL(5, 2) NOT NULL,      -- Monthly interest rate (as a percentage, e.g., 10 for 10%)
    months INT NOT NULL,                       -- Number of months in the savings cycle
    total_interest DECIMAL(10, 2) NOT NULL,    -- Total interest earned for the savings cycle
    total_amount DECIMAL(10, 2) NOT NULL,      -- Total amount at the end of the savings cycle
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the savings entry was created
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE -- Link to Users table
);

-- Table to store and manage bank balances for each user
CREATE TABLE BankAccounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each bank account
    user_id INT NOT NULL,                      -- Foreign key linking to the Users table
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0, -- Current balance of the user's account
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the account was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp for the last update
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE -- Link to Users table
);

-- Adjusted Transactions table
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each transaction
    account_id INT NOT NULL,                       -- Foreign key linking to the BankAccounts table
    transaction_type ENUM('credit', 'debit') NOT NULL, -- Type of transaction (credit for deposits, debit for withdrawals)
    amount DECIMAL(15, 2) NOT NULL,                -- Amount of the transaction
    description VARCHAR(255),                      -- Description of the transaction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the transaction was created
    FOREIGN KEY (account_id) REFERENCES BankAccounts(account_id) ON DELETE CASCADE
);

-- Table to store threshold calculations for each cycle
CREATE TABLE Thresholds (
    threshold_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique identifier for each threshold entry
    cycle_name VARCHAR(100) NOT NULL,           -- Name or label for the cycle (e.g., 'June 2024')
    bank_balance DECIMAL(15, 2) NOT NULL,       -- Total funds available
    admin_fees DECIMAL(15, 2) NOT NULL,         -- Deductions for administrative costs
    prepaid_interest DECIMAL(15, 2) NOT NULL,   -- Interest paid in advance
    savings_in_advance DECIMAL(15, 2) NOT NULL, -- Member savings held for future cycles
    retained_balances DECIMAL(15, 2) NOT NULL,  -- Funds reserved for specific purposes
    other_adjustments DECIMAL(15, 2) NOT NULL,  -- Any additional deductions
    num_members INT NOT NULL,                   -- Number of members in the group
    threshold_amount DECIMAL(15, 2) NOT NULL,   -- The calculated threshold per member
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the threshold was calculated
);

