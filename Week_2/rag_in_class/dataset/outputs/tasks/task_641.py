def is_nonagonal(n):
    """
    Calculate the nth nonagonal number.

    The nth nonagonal number is given by the formula: n * (7 * n - 5) / 2

    Args:
        n (int): The position in the sequence of nonagonal numbers.

    Returns:
        int: The nth nonagonal number.
    """
    return int(n * (7 * n - 5) / 2)
