# Title: Village Banking savings tracker

"""
This module contains functionality that tracks savings for a village banking application.
It includes a class to calculate the monthly savings, total savings, and total interest earned on savings for each month.
It then adds all the earnings in a cycle and returns the total savings and interest earned for the cycle.
The module will ask for savings made in each month and the interest rate for each month.
It will also ask for the number of months left in the cycle to determine the total savings and interest earned.
"""

class SavingsTracker:
    """
    A class to track savings and calculate total savings, interest earned, and final amount for a savings cycle.
    """

    def __init__(self, savings, interest_rate, months):
        """
        Initialize the SavingsTracker with savings amount, interest rate, and number of months.

        Args:
            savings (float): The amount saved each month.
            interest_rate (float): The monthly interest rate (as a decimal, e.g., 0.10 for 10%).
            months (int): The number of months in the savings cycle.
        """
        self.savings = savings
        self.interest_rate = interest_rate
        self.months = months

    def calculate_total_interest(self):
        """
        Calculate the total interest earned for the savings cycle.

        Returns:
            float: The total interest earned.
        """
        monthly_interest = self.savings * self.interest_rate
        return monthly_interest * self.months

    def calculate_total_amount(self):
        """
        Calculate the total amount at the end of the savings cycle.

        Returns:
            float: The total amount (savings + interest).
        """
        total_interest = self.calculate_total_interest()
        return self.savings + total_interest

    def get_summary(self):
        """
        Get a summary of the savings cycle.

        Returns:
            dict: A dictionary containing the total savings, total interest earned, and final amount.
        """
        total_interest = self.calculate_total_interest()
        total_amount = self.calculate_total_amount()
        return {
            "total_savings": self.savings,
            "total_interest": total_interest,
            "total_amount": total_amount,
        }


# Example usage
if __name__ == "__main__":
    # Input from the user
    savings = float(input("Enter the monthly savings amount: "))
    interest_rate = float(input("Enter the monthly interest rate (as a percentage, e.g., 10 for 10%): ")) / 100
    months = int(input("Enter the number of months in the savings cycle: "))

    # Create an instance of SavingsTracker
    tracker = SavingsTracker(savings, interest_rate, months)

    # Get the summary of the savings cycle
    results = tracker.get_summary()

    # Display results
    print(f"\nTotal Savings: {results['total_savings']:.2f}")
    print(f"Total Interest Earned: {results['total_interest']:.2f}")
    print(f"Total Amount at End of Cycle: {results['total_amount']:.2f}")

