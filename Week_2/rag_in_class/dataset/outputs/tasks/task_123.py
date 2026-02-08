def amicable_numbers_sum(limit):
    """
    Calculate the sum of all amicable numbers up to a given limit.

    An amicable number is a number that is the sum of its proper divisors,
    excluding itself, and the sum of the proper divisors of that sum is the
    original number, with the condition that the two numbers are different.

    Args:
        limit (int): The upper bound for finding amicable numbers.

    Returns:
        int: The sum of all amicable numbers up to the limit.
        str: Error message if the input is invalid.
    """
    if not isinstance(limit, int):
        return "Input is not an integer!"
    if limit < 1:
        return "Input must be bigger than 0!"

    amicables = set()

    for num in range(2, limit + 1):
        if num in amicables:
            continue

        # Calculate the sum of proper divisors of num
        sum_fact = sum(fact for fact in range(1, num) if num % fact == 0)

        # Calculate the sum of proper divisors of sum_fact
        sum_fact2 = sum(fact for fact in range(1, sum_fact) if sum_fact % fact == 0)

        # Check if num and sum_fact form an amicable pair
        if num == sum_fact2 and num != sum_fact:
            amicables.add(num)
            amicables.add(sum_fact2)

    return sum(amicables)
