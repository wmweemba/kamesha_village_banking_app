# Title: Loan Payment Calculator for village banking application

"""
This module contains functionality that calculaes loan payments for a village banking application.
It includes functions to calculate the monthly payment, total payment, and total interest paid on a loan.

The following variables are used in the calculations:
- principal: The amount of the loan.
- interest_rate: The flat interest rate charged on the principal amount that is pending for that month.
- installments: The number of months/installments over which the loan will be run and be repaid.
- monthly_principal: The amount of the principal that is paid each month. This is the principal amount divided
by the number of installments.
- monthly_payment: The amount to be paid each month. Which includes the principal amount and the interest 
charged on the principal amount for that month/installment.
- total_payment: The total amount paid over the life of the loan. This is the sum of all monthly payments.
- total_interest: The total interest paid over the life of the loan. This is the difference between the 
total payment and the principal amount.

Loan Payment Calculation Logic:
1. To calculate the monthly payment, you need to know the principal amount, interest rate, and number of 
installments and monthly_principal.
2. All the inputs are gotten from the user except the monthly_principal which is calculated by dividing the 
principal amount by the number of installments.
3. The monthly payment is calculated by adding the monthly principal and the interest charged on the principal
   amount for that month.
"""

def calculate_loan_payments(principal, interest_rate, installments):
    """
    Calculate the monthly payment, total payment, and total interest for a loan.

    Args:
        principal (float): The amount of the loan.
        interest_rate (float): The flat interest rate per month (as a decimal, e.g., 0.05 for 5%).
        installments (int): The number of months/installments over which the loan will be repaid.

    Returns:
        dict: A dictionary containing the monthly payments breakdown, total payment, and total interest.
    """
    # Calculate the monthly principal
    monthly_principal = principal / installments

    # Initialize variables for total payment and total interest
    total_payment = 0
    total_interest = 0
    remaining_principal = principal

    # List to store monthly payment details
    monthly_payments = []

    # Calculate monthly payments and accumulate totals
    for month in range(1, installments + 1):
        # Interest for the current month is calculated on the remaining principal
        monthly_interest = remaining_principal * interest_rate
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


# Example usage
if __name__ == "__main__":
    # Input from the user
    principal = float(input("Enter the loan principal amount: "))
    interest_rate = float(input("Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): ")) / 100
    installments = int(input("Enter the number of installments (months): "))

    # Calculate loan payments
    results = calculate_loan_payments(principal, interest_rate, installments)

    # Display results
    print("\nMonthly Payment Breakdown:")
    for payment in results["monthly_payments"]:
        print(f"Month {payment['month']}: Payment = {payment['monthly_payment']:.2f}, "
              f"Interest = {payment['monthly_interest']:.2f}, "
              f"Remaining Principal = {payment['remaining_principal']:.2f}")

    print(f"\nTotal Payment: {results['total_payment']:.2f}")
    print(f"Total Interest: {results['total_interest']:.2f}")

