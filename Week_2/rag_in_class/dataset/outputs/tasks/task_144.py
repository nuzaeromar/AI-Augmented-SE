def sum_Pairs(arr, n):
    """
    Calculate the sum of pairs in the array based on the given formula.

    Args:
        arr (list): List of numerical values.
        n (int): Length of the array.

    Returns:
        float: The computed sum based on the formula.
    """
    total = 0.0
    for i in range(n - 1, -1, -1):
        total += i * arr[i] - (n - 1 - i) * arr[i]
    return total
