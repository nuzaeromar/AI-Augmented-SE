def first_non_repeating_character(str1):
    """Return the first non-repeating character in the input string.

    Args:
        str1 (str): The input string to search for the first non-repeating character.

    Returns:
        str or None: The first non-repeating character, or None if all characters repeat.
    """
    char_order = []
    ctr = {}
    for c in str1:
        if c in ctr:
            ctr[c] += 1
        else:
            ctr[c] = 1
            char_order.append(c)
    for c in char_order:
        if ctr[c] == 1:
            return c
    return None
