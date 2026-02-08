import math

def sumofFactors(n):
    """
    Calculate the sum of all factors of a given number n.

    Args:
        n (int): The input number for which to calculate the sum of factors.

    Returns:
        int: The sum of all factors of n. Returns 0 if n is odd.
    """
    if n % 2 != 0:
        return 0
    res = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        count = 0
        curr_sum = 1
        curr_term = 1
        while n % i == 0:
            count += 1
            n = n // i
            if i == 2 and count == 1:
                curr_sum = 0
            curr_term *= i
            curr_sum += curr_term
        res *= curr_sum
    if n >= 2:
        res *= (1 + n)
    return res
