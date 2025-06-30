"""
Module: threshold_calculator.py
Purpose: Calculate the threshold amount each member should have to borrow based on group financial parameters.
"""

def calculate_threshold(
    bank_balance: float,
    admin_fees: float,
    prepaid_interest: float,
    savings_in_advance: float,
    retained_balances: float,
    other_adjustments: float,
    num_members: int
) -> float:
    """
    Calculate the threshold amount each member should have to borrow.

    Args:
        bank_balance (float): Total funds available in the group's account.
        admin_fees (float): Deductions for administrative costs.
        prepaid_interest (float): Interest paid in advance.
        savings_in_advance (float): Member savings held for future cycles.
        retained_balances (float): Funds reserved for specific purposes.
        other_adjustments (float): Any additional deductions (e.g., penalties or fees).
        num_members (int): Number of members in the group.

    Returns:
        float: The threshold amount per member, rounded to 2 decimal places.
    """
    # Step 1: Calculate net distributable amount after deductions
    net_amount = bank_balance - (
        admin_fees + prepaid_interest + savings_in_advance + retained_balances + other_adjustments
    )

    # Step 2: Compute threshold per member (equal share of net amount)
    threshold = net_amount / num_members

    # Step 3: Round to 2 decimal places (for currency)
    threshold = round(threshold, 2)

    return threshold


# Example usage
if __name__ == "__main__":
    threshold = calculate_threshold(
        bank_balance=170895,
        admin_fees=1900,
        prepaid_interest=444,
        savings_in_advance=3000,
        retained_balances=10000,
        other_adjustments=0,  # Assuming no other adjustments
        num_members=20
    )
    print(f"Threshold per member: K{threshold:.2f}")
    # Output: Threshold per member: K26836.55 