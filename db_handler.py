import mysql.connector

class DatabaseHandler:
    """
    A class to handle database operations for the Village Banking application.
    """

    def __init__(self, host, user, password, database):
        """
        Initialize the database connection.

        Args:
            host (str): Database host.
            user (str): Database user.
            password (str): Database password.
            database (str): Database name.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        Establish a connection to the database.
        """
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def save_savings(self, user_id, monthly_savings, interest_rate, months, total_interest, total_amount):
        """
        Save savings data to the database.

        Args:
            user_id (int): The ID of the user.
            monthly_savings (float): The amount saved each month.
            interest_rate (float): The monthly interest rate.
            months (int): The number of months in the savings cycle.
            total_interest (float): The total interest earned.
            total_amount (float): The total amount at the end of the cycle.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = """
            INSERT INTO Savings (user_id, monthly_savings, interest_rate, months, total_interest, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, monthly_savings, interest_rate, months, total_interest, total_amount))
            connection.commit()

            print("Savings data has been successfully saved to the database.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save_loan(self, user_id, principal, interest_rate, installments, total_payment, total_interest):
        """
        Save loan data to the database and return the loan_id.

        Args:
            user_id (int): The ID of the user.
            principal (float): The loan principal amount.
            interest_rate (float): The monthly interest rate.
            installments (int): The number of installments (months).
            total_payment (float): The total payment for the loan.
            total_interest (float): The total interest paid for the loan.

        Returns:
            int: The ID of the newly inserted loan.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = """
            INSERT INTO Loans (user_id, principal, interest_rate, installments, total_payment, total_interest)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, principal, interest_rate, installments, total_payment, total_interest))
            connection.commit()

            # Retrieve the ID of the newly inserted loan
            loan_id = cursor.lastrowid
            print("Loan data has been successfully saved to the database.")
            return loan_id

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save_loan_payments(self, loan_id, monthly_payments):
        """
        Save loan payment schedule to the LoanPayments table.

        Args:
            loan_id (int): The ID of the loan.
            monthly_payments (list): A list of dictionaries containing payment details.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = """
            INSERT INTO LoanPayments (loan_id, month, monthly_payment, monthly_interest, principal_payment, due_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            for payment in monthly_payments:
                cursor.execute(query, (
                    loan_id,
                    payment['month'],
                    payment['monthly_payment'],
                    payment['monthly_interest'],
                    payment['principal_payment'],
                    payment['due_date'],
                    'pending'
                ))
            connection.commit()

            print("Loan payment schedule has been successfully saved to the database.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save_transaction(self, account_id, transaction_type, amount, description):
        """
        Save a transaction to the Transactions table and update the bank balance.

        Args:
            account_id (int): The ID of the bank account.
            transaction_type (str): The type of transaction ('credit' or 'debit').
            amount (float): The transaction amount.
            description (str): A description of the transaction.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            # Insert the transaction
            query = """
            INSERT INTO Transactions (account_id, transaction_type, amount, description)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (account_id, transaction_type, amount, description))

            # Update the bank balance
            if transaction_type == 'credit':
                update_query = "UPDATE BankAccounts SET balance = balance + %s WHERE account_id = %s"
            else:  # debit
                update_query = "UPDATE BankAccounts SET balance = balance - %s WHERE account_id = %s"
            cursor.execute(update_query, (amount, account_id))

            connection.commit()

            print("Transaction has been successfully saved and bank balance updated.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_or_create_bank_account(self, user_id):
        """
        Retrieve the bank account for a user. If it doesn't exist, create one.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The account_id of the user's bank account.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            # Check if the bank account exists
            query = "SELECT account_id FROM BankAccounts WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                # Bank account exists, return the account_id
                return result[0]
            else:
                # Create a new bank account for the user
                insert_query = "INSERT INTO BankAccounts (user_id, balance) VALUES (%s, %s)"
                cursor.execute(insert_query, (user_id, 0))  # Initialize balance to 0
                connection.commit()

                # Return the newly created account_id
                return cursor.lastrowid

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def process_loan_repayment(self, loan_id, installment, payment_amount):
        """
        Process a loan repayment for a specific installment.
        
        This method:
          - Checks that the installment is pending.
          - Validates that the payment amount is sufficient.
          - Updates the LoanPayments record to mark it as 'paid'.
          - Retrieves (or creates) the user's bank account using user_id from the Loans table.
          - Records a 'credit' transaction for the repayment.
          
        Args:
            loan_id (int): The ID of the loan.
            installment (int): The installment (month) number to be repaid.
            payment_amount (float): The repayment amount provided by the user.
            
        Returns:
            bool: True if repayment was processed successfully, False otherwise.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            # Check if the specific installment exists and is pending.
            query = """
                SELECT payment_id, monthly_payment 
                FROM LoanPayments 
                WHERE loan_id = %s AND month = %s AND status = 'pending'
            """
            cursor.execute(query, (loan_id, installment))
            result = cursor.fetchone()
            if not result:
                print("No pending installment found or installment already paid.")
                return False

            payment_id, monthly_payment = result

            # Validate that the payment amount is sufficient.
            if payment_amount < monthly_payment:
                print(f"Payment amount ({payment_amount}) is less than the required installment ({monthly_payment}).")
                return False

            # Mark the installment as 'paid'
            update_query = "UPDATE LoanPayments SET status = 'paid' WHERE payment_id = %s"
            cursor.execute(update_query, (payment_id,))
            connection.commit()  # Commit after updating the installment status

            # Retrieve the user_id for the loan from the Loans table.
            query_loan = "SELECT user_id FROM Loans WHERE loan_id = %s"
            cursor.execute(query_loan, (loan_id,))
            loan_data = cursor.fetchone()
            if not loan_data:
                print("Loan not found.")
                return False
            user_id = loan_data[0]

            # Retrieve (or create) the bank account for the user.
            account_id = self.get_or_create_bank_account(user_id)
            if not account_id:
                print("Failed to retrieve or create a bank account for the user.")
                return False

            # Record the repayment transaction.
            description = f"Loan repayment for loan {loan_id}, installment {installment}"
            self.save_transaction(
                account_id=account_id,
                transaction_type='credit',  # Repayment brings money into the bank account.
                amount=payment_amount,
                description=description
            )

            print("Loan repayment processed successfully.")
            return True

        except mysql.connector.Error as err:
            print(f"Error processing loan repayment: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save_threshold(self, cycle_name, bank_balance, admin_fees, prepaid_interest, savings_in_advance, retained_balances, other_adjustments, num_members, threshold_amount):
        """
        Save threshold calculation data to the Thresholds table.

        Args:
            cycle_name (str): Name or label for the cycle (e.g., 'June 2024').
            bank_balance (float): Total funds available.
            admin_fees (float): Deductions for administrative costs.
            prepaid_interest (float): Interest paid in advance.
            savings_in_advance (float): Member savings held for future cycles.
            retained_balances (float): Funds reserved for specific purposes.
            other_adjustments (float): Any additional deductions.
            num_members (int): Number of members in the group.
            threshold_amount (float): The calculated threshold per member.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = """
            INSERT INTO Thresholds (
                cycle_name, bank_balance, admin_fees, prepaid_interest, savings_in_advance, retained_balances, other_adjustments, num_members, threshold_amount
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                cycle_name, bank_balance, admin_fees, prepaid_interest, savings_in_advance, retained_balances, other_adjustments, num_members, threshold_amount
            ))
            connection.commit()
            print("Threshold data has been successfully saved to the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()