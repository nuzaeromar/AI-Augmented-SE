def common_element(list1, list2):
    """Check if there is any common element between two lists.

    Args:
        list1: First list of elements.
        list2: Second list of elements.

    Returns:
        bool: True if there is at least one common element, False otherwise.
    """
    for x in list1:
        for y in list2:
            if x == y:
                return True
    return False
