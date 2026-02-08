import cmath

def convert(numbers):
    """Convert a complex number to its polar form.

    Args:
        numbers: A complex number (as a complex type or a tuple/list of (real, imag)).

    Returns:
        A tuple (magnitude, phase) where:
        - magnitude: The magnitude (r) of the complex number as a float.
        - phase: The phase (theta) in radians as a float.
    """
    num = cmath.polar(numbers)
    return num
