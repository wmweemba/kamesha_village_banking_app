# Main file to be used for the village banking application

# Import necessary modules
from loan_payment_calculator.vb_loan_calculator import LoanPaymentCalculator
from savings_tracker.savings import SavingsTracker
from db_handler import DatabaseHandler

def main():
    """
    Main function to orchestrate the village banking application.
    """
    print("Welcome to the Village Banking Application!")

    # Initialize the database handler
    db_handler = DatabaseHandler(
        host="localhost",
        user="root",
        password="S3k3l3t1*",
        database="VillageBankingDB"
    )

    while True:
        print("\nPlease select an option:")
        print("1. Loan Payment Calculator")
        print("2. Savings Tracker")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

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
                db_handler.save_loan(
                    user_id=user_id,
                    principal=principal,
                    interest_rate=interest_rate,
                    installments=installments,
                    total_payment=loan_results['total_payment'],
                    total_interest=loan_results['total_interest']
                )
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

            # Ask the user if they want to save the data to the database
            save_to_db = input("Would you like to save this savings data to the database? (yes/no): ").strip().lower()
            if save_to_db == "yes":
                user_id = int(input("Enter your user ID: "))  # Assuming user ID is known
                db_handler.save_savings(
                    user_id=user_id,
                    monthly_savings=savings,
                    interest_rate=savings_interest_rate,
                    months=months,
                    total_interest=savings_results['total_interest'],
                    total_amount=savings_results['total_amount']
                )
            else:
                print("Savings data was not saved to the database.")

        elif choice == "3":
            print("Thank you for using the Village Banking Application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

