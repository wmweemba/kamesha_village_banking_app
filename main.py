# Main file to be used for the village banking application

# Import necessary modules
from loan_payment_calculator.vb_loan_calculator import LoanPaymentCalculator
from savings_tracker.savings import SavingsTracker
from db_handler import DatabaseHandler
from user_handler import UserHandler  # Import the UserHandler class

def main():
    """
    Main function to orchestrate the village banking application.
    """
    print("Welcome to the Village Banking Application!")

    # Initialize the database handlers
    db_handler = DatabaseHandler(
        host="localhost",
        user="root",
        password="S3k3l3t1*",
        database="VillageBankingDB"
    )
    user_handler = UserHandler(
        host="localhost",
        user="root",
        password="S3k3l3t1*",
        database="VillageBankingDB"
    )

    while True:
        print("\nPlease select an option:")
        print("1. Loan Payment Calculator")
        print("2. Savings Tracker")
        print("3. User Management")
        print("5. Loan Repayment")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/5/4): ")

        if choice == "1":
            # Loan Payment Calculator
            print("\n--- Loan Payment Calculator ---")
            principal = float(input("Enter the loan principal amount: "))
            interest_rate = float(input("Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): ")) / 100
            installments = int(input("Enter the number of installments (months): "))

            loan_calculator = LoanPaymentCalculator(principal, interest_rate, installments)
            loan_results = loan_calculator.calculate_monthly_payments()

            print("\nLoan Payment Breakdown:")
            for payment in loan_results["monthly_payments"]:
                print(f"Month {payment['month']}: Payment = {payment['monthly_payment']:.2f}, "
                      f"Interest = {payment['monthly_interest']:.2f}, "
                      f"Remaining Principal = {payment['remaining_principal']:.2f}")
            print(f"Total Payment: {loan_results['total_payment']:.2f}")
            print(f"Total Interest: {loan_results['total_interest']:.2f}")

            # Ask the user if they want to save the loan data to the database
            save_to_db = input("Would you like to save this loan data to the database? (yes/no): ").strip().lower()
            if save_to_db == "yes":
                user_id = int(input("Enter your user ID: "))  # Assuming user ID is known

                # Check if the user exists
                if not user_handler.user_exists(user_id):
                    print(f"User with ID {user_id} does not exist. Please create the user first.")
                else:
                    loan_id = db_handler.save_loan(
                        user_id=user_id,
                        principal=principal,
                        interest_rate=interest_rate,
                        installments=installments,
                        total_payment=loan_results['total_payment'],
                        total_interest=loan_results['total_interest']
                    )

                    if loan_id:
                        # Generate and save payment schedule
                        payment_schedule = loan_calculator.generate_payment_schedule()
                        db_handler.save_loan_payments(loan_id, payment_schedule)

                        # Retrieve or create the bank account for the user
                        account_id = db_handler.get_or_create_bank_account(user_id)
                        if account_id:
                            # Record loan issuance transaction
                            db_handler.save_transaction(
                                account_id=account_id,
                                transaction_type='debit',
                                amount=principal,
                                description=f"Loan issued to user {user_id}"
                            )
                        else:
                            print("Failed to retrieve or create a bank account for the user.")
                    else:
                        print("Failed to save loan data.")
            else:
                print("Loan data was not saved to the database.")

        elif choice == "2":
            # Savings Tracker
            print("\n--- Savings Tracker ---")
            savings = float(input("Enter the monthly savings amount: "))
            savings_interest_rate = float(input("Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): ")) / 100
            months = int(input("Enter the number of months in the savings cycle: "))

            savings_tracker = SavingsTracker(savings, savings_interest_rate, months)
            savings_results = savings_tracker.get_summary()

            print(f"\nTotal Savings: {savings_results['total_savings']:.2f}")
            print(f"Total Interest Earned: {savings_results['total_interest']:.2f}")
            print(f"Total Amount at End of Cycle: {savings_results['total_amount']:.2f}")

            # Ask the user if they want to save the savings data to the database
            save_to_db = input("Would you like to save this savings data to the database? (yes/no): ").strip().lower()
            if save_to_db == "yes":
                user_id = int(input("Enter your user ID: "))
                # Save the savings record
                db_handler.save_savings(
                    user_id=user_id,
                    monthly_savings=savings,
                    interest_rate=savings_interest_rate,
                    months=months,
                    total_interest=savings_results['total_interest'],
                    total_amount=savings_results['total_amount']
                )
                # Retrieve or create the bank account for the user
                account_id = db_handler.get_or_create_bank_account(user_id)
                if account_id:
                    # Record savings deposit transaction. Treat the total savings deposit as a credit to the bank.
                    db_handler.save_transaction(
                        account_id=account_id,
                        transaction_type='credit',
                        amount=savings_results['total_amount'],
                        description=f"Savings deposit by user {user_id}"
                    )
                else:
                    print("Failed to retrieve or create a bank account for the user.")
            else:
                print("Savings data was not saved to the database.")

        elif choice == "3":
            # User Management
            print("\n--- User Management ---")
            print("1. Create New User")
            print("2. Delete Existing User")
            user_choice = input("Enter your choice (1/2): ")

            if user_choice == "1":
                # Create New User
                name = input("Enter the user's full name: ")
                email = input("Enter the user's email address: ")
                phone = input("Enter the user's phone number: ")
                user_handler.create_user(name, email, phone)

            elif user_choice == "2":
                # Delete Existing User
                user_id = int(input("Enter the user ID to delete: "))
                user_handler.delete_user(user_id)

            else:
                print("Invalid choice. Returning to the main menu.")

        elif choice == "5":
            # Loan Repayment
            print("\n--- Loan Repayment ---")
            user_id = int(input("Enter your user ID: "))
            loan_id = int(input("Enter the loan ID you wish to repay: "))
            installment = int(input("Enter the installment month to repay: "))
            payment_amount = float(input("Enter the repayment amount: "))

            # Process the repayment. For this, we assume a new method exists:
            repayment_success = db_handler.process_loan_repayment(
                loan_id=loan_id,
                installment=installment,
                payment_amount=payment_amount
            )

            if repayment_success:
                print("Loan repayment processed successfully.")
            else:
                print("Failed to process loan repayment.")

        elif choice == "4":
            print("Thank you for using the Village Banking Application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

