import cmath

def len_complex(a: float, b: float) -> float:
    """Calculate the magnitude (length) of a complex number.

    Args:
        a: Real part of the complex number.
        b: Imaginary part of the complex number.

    Returns:
        The magnitude (length) of the complex number as a float.
    """
    cn = complex(a, b)
    length = abs(cn)
    return length
