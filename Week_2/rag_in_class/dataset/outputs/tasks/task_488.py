import math

def area_pentagon(a):
    """Calculate the area of a regular pentagon with side length a.

    Args:
        a (float): Side length of the pentagon.

    Returns:
        float: Area of the pentagon calculated using the formula:
               (sqrt(5*(5 + 2*sqrt(5))) * a^2) / 4
    """
    area = (math.sqrt(5 * (5 + 2 * math.sqrt(5))) * pow(a, 2)) / 4.0
    return area
