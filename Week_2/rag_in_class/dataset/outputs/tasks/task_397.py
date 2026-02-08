def median_numbers(a, b, c):
    """
    Calculate the median of three numbers.

    Args:
        a (float): First number
        b (float): Second number
        c (float): Third number

    Returns:
        float: The median value of the three input numbers
    """
    if a > b:
        if a < c:
            median = a
        elif b > c:
            median = b
        else:
            median = c
    else:
        if a > c:
            median = a
        elif b < c:
            median = b
        else:
            median = c
    return median
