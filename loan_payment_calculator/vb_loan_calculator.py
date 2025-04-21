# Title: Loan Payment Calculator for village banking application

"""
This module contains functionality that calculates loan payments for a village banking application.
It includes a class to calculate the monthly payment, total payment, and total interest paid on a loan.
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

class LoanPaymentCalculator:
    """
    A class to calculate loan payments, total payment, and total interest for a loan.
    """

    def __init__(self, principal, interest_rate, installments):
        """
        Initialize the LoanPaymentCalculator with loan details.

        Args:
            principal (float): The amount of the loan.
            interest_rate (float): The flat interest rate per month (as a decimal, e.g., 0.05 for 5%).
            installments (int): The number of months/installments over which the loan will be repaid.
        """
        self.principal = principal
        self.interest_rate = interest_rate
        self.installments = installments

    def calculate_monthly_payments(self):
        """
        Calculate the monthly payments, total payment, and total interest for the loan.

        Returns:
            dict: A dictionary containing the monthly payments breakdown, total payment, and total interest.
        """
        # Calculate the monthly principal
        monthly_principal = self.principal / self.installments

        # Initialize variables for total payment and total interest
        total_payment = 0
        total_interest = 0
        remaining_principal = self.principal

        # List to store monthly payment details
        monthly_payments = []

        # Calculate monthly payments and accumulate totals
        for month in range(1, self.installments + 1):
            # Interest for the current month is calculated on the remaining principal
            monthly_interest = remaining_principal * self.interest_rate
            monthly_payment = monthly_principal + monthly_interest

            # Accumulate totals
            total_payment += monthly_payment
            total_interest += monthly_interest

            # Append monthly payment details
            monthly_payments.append({
                "month": month,
                "monthly_payment": monthly_payment,
                "monthly_interest": monthly_interest,
                "remaining_principal": remaining_principal - monthly_principal
            })

            # Reduce the remaining principal
            remaining_principal -= monthly_principal

        return {
            "monthly_payments": monthly_payments,
            "total_payment": total_payment,
            "total_interest": total_interest,
        }

    def generate_payment_schedule(self):
        """
        Generate the monthly payment schedule for the loan.

        Returns:
            list: A list of dictionaries containing payment details for each month.
        """
        monthly_principal = self.principal / self.installments
        remaining_principal = self.principal
        payment_schedule = []

        for month in range(1, self.installments + 1):
            monthly_interest = remaining_principal * self.interest_rate
            monthly_payment = monthly_principal + monthly_interest
            due_date = (datetime.now() + relativedelta(months=month)).date()

            payment_schedule.append({
                "month": month,
                "monthly_payment": monthly_payment,
                "monthly_interest": monthly_interest,
                "principal_payment": monthly_principal,
                "due_date": due_date
            })

            remaining_principal -= monthly_principal

        return payment_schedule


# Example usage
if __name__ == "__main__":
    # Input from the user
    principal = float(input("Enter the loan principal amount: "))
    interest_rate = float(input("Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): ")) / 100
    installments = int(input("Enter the number of installments (months): "))

    # Create an instance of LoanPaymentCalculator
    calculator = LoanPaymentCalculator(principal, interest_rate, installments)

    # Calculate loan payments
    results = calculator.calculate_monthly_payments()

    # Display results
    print("\nMonthly Payment Breakdown:")
    for payment in results["monthly_payments"]:
        print(f"Month {payment['month']}: Payment = {payment['monthly_payment']:.2f}, "
              f"Interest = {payment['monthly_interest']:.2f}, "
              f"Remaining Principal = {payment['remaining_principal']:.2f}")

    print(f"\nTotal Payment: {results['total_payment']:.2f}")
    print(f"Total Interest: {results['total_interest']:.2f}")

