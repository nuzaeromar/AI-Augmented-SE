def count_Hexadecimal(L, R):
    """
    Counts the number of hexadecimal digits in the range [L, R].

    Args:
        L (int): The lower bound of the range (inclusive).
        R (int): The upper bound of the range (inclusive).

    Returns:
        int: The count of hexadecimal digits in the range [L, R].
    """
    count = 0
    for i in range(L, R + 1):
        if 10 <= i <= 15:
            count += 1
        elif i > 15:
            k = i
            while k != 0:
                if k % 16 >= 10:
                    count += 1
                k = k // 16
    return count
