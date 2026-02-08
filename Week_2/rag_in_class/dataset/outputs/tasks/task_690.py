def mul_consecutive_nums(nums):
    """
    Multiplies each pair of consecutive numbers in the input list.

    Args:
        nums (list[float]): A list of numbers (int or float).

    Returns:
        list[float]: A list where each element is the product of consecutive elements
                    from the input list. The length of the result is len(nums) - 1.

    Precision:
        - For integer inputs, the result will be an integer.
        - For floating-point inputs, the result will maintain the precision of Python floats.
        - No rounding or truncation is applied.
    """
    result = [b * a for a, b in zip(nums[:-1], nums[1:])]
    return result
