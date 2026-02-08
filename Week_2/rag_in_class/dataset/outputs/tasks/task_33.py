def decimal_To_Binary(N):
    """
    Convert a decimal number to its binary representation as an integer.

    Args:
        N (int): The decimal number to convert (must be non-negative).

    Returns:
        int: The binary representation of N as an integer (e.g., 5 becomes 101).

    Notes:
        - The binary digits are stored in the integer with the least significant digit
          as the least significant digit of the integer (e.g., 5 -> 101).
        - The function handles N = 0 correctly by returning 0.
    """
    B_Number = 0
    cnt = 0
    while N != 0:
        rem = N % 2
        c = pow(10, cnt)
        B_Number += rem * c
        N //= 2
        cnt += 1
    return B_Number
