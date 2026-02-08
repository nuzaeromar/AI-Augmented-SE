import math

def sum_of_odd_Factors(n):
    """
    Calculate the sum of odd factors of a given integer n.

    Args:
        n (int): The input integer for which to calculate the sum of odd factors.

    Returns:
        int: The sum of all odd factors of n.
    """
    res = 1
    # Remove all factors of 2 (even factors)
    while n % 2 == 0:
        n = n // 2

    # Check for odd factors from 3 to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        count = 0
        curr_sum = 1
        curr_term = 1
        while n % i == 0:
            count += 1
            n = n // i
            curr_term *= i
            curr_sum += curr_term
        res *= curr_sum

    # If remaining n is a prime number greater than 2
    if n > 2:
        res *= (1 + n)

    return res
