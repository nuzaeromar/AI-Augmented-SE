def get_max_sum(n: int) -> int:
    """
    Calculate the maximum sum for a given integer n using a dynamic programming approach.

    The function computes the maximum sum for each integer from 0 to n by considering:
    - The integer itself
    - The sum of the maximum sums of its divisors (2, 3, 4, 5)

    Args:
        n: The integer for which to compute the maximum sum (must be >= 0)

    Returns:
        The maximum sum for the integer n
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    # Initialize the result list with base cases
    res = [0, 1]  # res[0] = 0, res[1] = 1

    # Handle the case when n is 0 or 1 directly
    if n <= 1:
        return res[n]

    # Compute maximum sums for integers from 2 to n
    for i in range(2, n + 1):
        # Calculate the sum of maximum sums of divisors (2, 3, 4, 5)
        divisor_sum = res[i // 2] + res[i // 3] + res[i // 4] + res[i // 5]
        # The maximum sum is either the integer itself or the sum of its divisors
        res.append(max(i, divisor_sum))

    return res[n]
