# Village Banking Application

## Overview
The Village Banking Application is a comprehensive system designed to manage the core financial operations of a village banking group. It supports loan management, savings tracking, user management, threshold calculations for fair loan distribution, and more. The application is built with modularity and extensibility in mind, using Python and MySQL for robust data handling.

## Features
- **Loan Payment Calculator:** Calculate monthly payments, total payment, and interest for user loans. Save loan data and payment schedules to the database.
- **Savings Tracker:** Track monthly savings, calculate total savings and interest, and save savings records to the database.
- **User Management:** Create and delete users, and manage user data securely.
- **Loan Repayment:** Process loan repayments, update payment status, and record transactions.
- **Threshold Calculator:** Calculate and store the minimum borrowing threshold per member for each cycle, ensuring fair distribution of funds.
- **Forced Loan Calculation:** Determine if a member must take a forced loan to meet the threshold, and calculate the required amount.
- **Database Integration:** All financial records are stored in a MySQL database for persistence and reporting.

## Directory Structure
```
kamesha_village_banking_app/
├── main.py                         # Main entry point for the application
├── db_handler.py                   # Handles all database operations
├── user_handler.py                 # Manages user creation, deletion, and existence checks
├── data.sql                        # SQL schema for database setup
├── requirements.txt                # Python dependencies
├── loan_payment_calculator/
│   ├── vb_loan_calculator.py       # Loan payment calculation logic
│   └── threshold_calculator.py     # Threshold calculation logic
├── savings_tracker/
│   └── savings.py                  # Savings tracking logic
├── fines_penalties_tracker/
│   └── fines.py                    # (Reserved for future fines/penalties logic)
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd kamesha_village_banking_app
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database:**
   - Ensure you have MySQL installed and running.
   - Run the SQL script to create the necessary tables:
     ```bash
     mysql -u <username> -p < data.sql
     ```
   - Update database credentials in `main.py`, `db_handler.py`, and `user_handler.py` if needed.

## Usage
Run the main application:
```bash
python main.py
```
You will be presented with a menu to:
- Calculate and save loan payments
- Track and save savings
- Manage users
- Process loan repayments
- Calculate and save borrowing thresholds
- Exit the application

### Example: Threshold Calculation
1. Select "Threshold Calculator" from the menu.
2. Enter the required financial parameters and cycle name.
3. The app will display the calculated threshold per member and prompt to save it to the database.

## Usage Examples

### 1. Loan Payment Calculator
**Goal:** Calculate monthly loan payments and optionally save the loan to the database.

**Steps:**
1. Select `1` from the main menu.
2. Enter the loan principal amount (e.g., `10000`).
3. Enter the monthly interest rate as a percentage (e.g., `10` for 10%).
4. Enter the number of installments (e.g., `12`).
5. Review the monthly payment breakdown, total payment, and total interest displayed.
6. When prompted, type `yes` to save the loan data, then enter your user ID.
   - If the user does not exist, you will be asked to create the user first.
7. The loan and payment schedule will be saved, and a transaction will be recorded.

**Sample Output:**
```
--- Loan Payment Calculator ---
Enter the loan principal amount: 10000
Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): 10
Enter the number of installments (months): 12

Loan Payment Breakdown:
Month 1: Payment = 1083.33, Interest = 1000.00, Remaining Principal = 9166.67
... (other months) ...
Total Payment: 13000.00
Total Interest: 3000.00
Would you like to save this loan data to the database? (yes/no): yes
Enter your user ID: 1
Loan data has been successfully saved to the database.
```

### 2. Savings Tracker
**Goal:** Track savings, calculate total interest, and save savings data.

**Steps:**
1. Select `2` from the main menu.
2. Enter the monthly savings amount (e.g., `500`).
3. Enter the monthly interest rate as a percentage (e.g., `5`).
4. Enter the number of months in the savings cycle (e.g., `6`).
5. Review the total savings, interest earned, and final amount.
6. When prompted, type `yes` to save the savings data, then enter your user ID.

**Sample Output:**
```
--- Savings Tracker ---
Enter the monthly savings amount: 500
Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): 5
Enter the number of months in the savings cycle: 6

Total Savings: 500.00
Total Interest Earned: 150.00
Total Amount at End of Cycle: 650.00
Would you like to save this savings data to the database? (yes/no): yes
Enter your user ID: 1
Savings data has been successfully saved to the database.
```

### 3. User Management
**Goal:** Create or delete users in the system.

**Steps:**
1. Select `3` from the main menu.
2. Choose `1` to create a new user or `2` to delete an existing user.
   - For creation, enter the user's full name, email, and phone number.
   - For deletion, enter the user ID to delete.

**Sample Output (Create):**
```
--- User Management ---
1. Create New User
2. Delete Existing User
Enter your choice (1/2): 1
Enter the user's full name: Jane Doe
Enter the user's email address: jane@example.com
Enter the user's phone number: 1234567890
User has been successfully created.
```

**Sample Output (Delete):**
```
--- User Management ---
1. Create New User
2. Delete Existing User
Enter your choice (1/2): 2
Enter the user ID to delete: 1
User has been successfully deleted.
```

### 4. Loan Repayment
**Goal:** Repay a loan installment and update payment status.

**Steps:**
1. Select `5` from the main menu.
2. Enter your user ID, the loan ID, the installment month, and the repayment amount.
3. The system will process the repayment and update the database.

**Sample Output:**
```
--- Loan Repayment ---
Enter your user ID: 1
Enter the loan ID you wish to repay: 2
Enter the installment month to repay: 3
Enter the repayment amount: 1200
Loan repayment processed successfully.
```

### 5. Threshold Calculator
**Goal:** Calculate the minimum borrowing threshold per member for a cycle and save it.

**Steps:**
1. Select `6` from the main menu.
2. Enter the cycle name (e.g., `June 2024`).
3. Enter the required financial parameters as prompted.
4. Review the calculated threshold per member.
5. When prompted, type `yes` to save the threshold to the database.

**Sample Output:**
```
--- Threshold Calculator ---
Enter the cycle name or period (e.g., 'June 2024'): June 2024
Enter the total bank balance: 170895
Enter the total admin fees: 1900
Enter the prepaid interest: 444
Enter the savings in advance: 3000
Enter the retained balances: 10000
Enter any other adjustments (0 if none): 0
Enter the number of members: 20
Threshold per member: K26836.55
Would you like to save this threshold to the database? (yes/no): yes
Threshold data has been successfully saved to the database.
```

### 6. Forced Loan Calculation
**Goal:** Determine if a member needs a forced loan to meet the group threshold, and calculate the required amount.

**How it works:**
- The threshold is calculated once for the cycle using the Threshold Calculator.
- For each member, compare their total borrowed amount to the threshold.
- If the member has borrowed less than the threshold, the difference is the forced loan amount.
- If the member meets or exceeds the threshold, no forced loan is required.

**Formula:**
```
forced_loan = max(0, threshold - total_borrowed_by_member)
```

**Sample Usage:**
```python
from loan_payment_calculator.threshold_calculator import calculate_forced_loan

threshold = 26836.55  # Example threshold for the cycle
member_borrowed_amount = 20000
forced_loan = calculate_forced_loan(threshold, member_borrowed_amount)
print(f"Forced loan for member: K{forced_loan:.2f}")  # Output: Forced loan for member: K6836.55
```

**Key Takeaway:**
- The threshold is a fixed value for the group/cycle.
- Forced loans ensure all members meet the minimum borrowing requirement for fairness.

## Database Schema Summary
The application uses the following main tables:
- **Users:** Stores user information.
- **Loans:** Stores loan details for each user.
- **LoanPayments:** Tracks payment schedules and statuses for each loan.
- **Savings:** Records savings cycles and interest for each user.
- **BankAccounts:** Manages user bank account balances.
- **Transactions:** Logs all financial transactions (credits/debits).
- **Thresholds:** Stores threshold calculations for each cycle, including all input parameters and the result.

See `data.sql` for full schema details.

## Dependencies
- Python 3.x
- mysql-connector-python
- python-dateutil

## Extending the Application
- Add new modules for fines, penalties, or additional financial logic as needed.
- Integrate reporting or export features for group transparency.

## License
This project is provided for educational and community banking purposes. Please adapt and extend as needed for your group or organization.
