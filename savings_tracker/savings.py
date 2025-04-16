# Title: Village Banking savings tracker

"""
This module contains functionality that tracks savings for a village banking application.
It includes functions to calculate the monthly savings, total savings, and total interest earned on savings for each month
It then adds all the earnings in a cycle and returns the total savings and interest earned for the cycle.
The module will ask for savings made in each month and the interest rate for each month.
It will also ask for the number of months left in the cycle to determine the total savings and interest earned.
"""

def calculate_savings(savings, interest_rate, months):
    """
    Calculate the total savings and interest earned for a savings cycle.

    Args:
        savings (float): The amount saved each month.
        interest_rate (float): The monthly interest rate (as a decimal, e.g., 0.10 for 10%).
        months (int): The number of months in the savings cycle.

    Returns:
        dict: A dictionary containing the total savings, total interest earned, and final amount.
    """
    # Calculate monthly interest
    monthly_interest = savings * interest_rate

    # Calculate total interest for the cycle
    total_interest = monthly_interest * months

    # Calculate total amount at the end of the cycle
    total_amount = savings + total_interest

    return {
        "total_savings": savings,
        "total_interest": total_interest,
        "total_amount": total_amount,
    }


# Example usage
if __name__ == "__main__":
    # Input from the user
    savings = float(input("Enter the monthly savings amount: "))
    interest_rate = float(input("Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): ")) / 100
    months = int(input("Enter the number of months in the savings cycle: "))

    # Calculate savings
    results = calculate_savings(savings, interest_rate, months)

    # Display results
    print(f"\nTotal Savings: {results['total_savings']:.2f}")
    print(f"Total Interest Earned: {results['total_interest']:.2f}")
    print(f"Total Amount at End of Cycle for this saving: {results['total_amount']:.2f}")

