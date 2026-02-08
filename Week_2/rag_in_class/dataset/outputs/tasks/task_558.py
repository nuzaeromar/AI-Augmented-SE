def digit_distance_nums(n1: int, n2: int) -> int:
    """Calculate the sum of digits in the absolute difference between two integers.

    Args:
        n1: First integer
        n2: Second integer

    Returns:
        Sum of digits in the absolute difference between n1 and n2
    """
    return sum(map(int, str(abs(n1 - n2))))
