def parabola_vertex(a: float, b: float, c: float) -> tuple[float, float]:
    """
    Calculate the vertex of a parabola defined by the quadratic equation ax² + bx + c.

    Args:
        a: Coefficient of x² (must not be zero)
        b: Coefficient of x
        c: Constant term

    Returns:
        A tuple containing (x, y) coordinates of the vertex.
        x = -b / (2a)
        y = (4ac - b²) / (4a)

    Note:
        The function assumes a ≠ 0 to avoid division by zero.
        Floating-point precision follows Python's default behavior.
    """
    x = (-b) / (2 * a)
    y = ((4 * a * c) - (b * b)) / (4 * a)
    return (x, y)
