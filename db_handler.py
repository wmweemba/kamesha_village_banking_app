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