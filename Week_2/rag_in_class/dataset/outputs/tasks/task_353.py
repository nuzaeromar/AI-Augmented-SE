def remove_column(list1, n):
    """Remove the nth column from each row in the 2D list.

    Args:
        list1: A 2D list (list of lists) where each sublist represents a row.
        n: The index of the column to remove (0-based).

    Returns:
        The modified 2D list with the nth column removed from each row.

    Note:
        This function modifies the input list in-place and also returns it.
        The function assumes all rows in the list have at least n+1 columns.
    """
    for row in list1:
        del row[n]
    return list1
