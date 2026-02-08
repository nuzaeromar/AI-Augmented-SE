def parallel_lines(line1, line2):
    """
    Check if two lines are parallel by comparing their slopes.

    Args:
        line1: A tuple (a1, b1) representing the line equation a1*x + b1*y + c1 = 0
        line2: A tuple (a2, b2) representing the line equation a2*x + b2*y + c2 = 0

    Returns:
        bool: True if the lines are parallel, False otherwise
    """
    return line1[0] / line1[1] == line2[0] / line2[1]
