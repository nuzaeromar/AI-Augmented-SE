def sum_list(lst1, lst2):
    """Return a new list where each element is the sum of corresponding elements in lst1 and lst2.

    Args:
        lst1: List of numbers (int or float)
        lst2: List of numbers (int or float) with same length as lst1

    Returns:
        List of numbers where each element is lst1[i] + lst2[i]
        Precision: Same as Python's built-in float addition (IEEE 754 double precision)
    """
    return [lst1[i] + lst2[i] for i in range(len(lst1))]
