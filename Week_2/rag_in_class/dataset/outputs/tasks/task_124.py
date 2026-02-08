import cmath

def angle_complex(a, b):
    """Calculate the phase angle of the complex number formed by a and b.

    Args:
        a (float): Real part of the complex number.
        b (float): Imaginary part of the complex number.

    Returns:
        float: The phase angle in radians, in the range [-π, π].
    """
    cn = complex(a, b)
    angle = cmath.phase(cn)
    return angle
