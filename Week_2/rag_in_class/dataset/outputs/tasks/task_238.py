def number_of_substrings(str):
    """Calculate the number of possible substrings in a given string.

    Args:
        str: Input string for which to count substrings.

    Returns:
        int: Number of possible substrings, calculated as n*(n+1)/2 where n is the string length.
    """
    str_len = len(str)
    return int(str_len * (str_len + 1) / 2)
