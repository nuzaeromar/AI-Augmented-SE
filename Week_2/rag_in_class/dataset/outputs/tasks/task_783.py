def rgb_to_hsv(r, g, b):
    """
    Convert RGB color values to HSV color space.

    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)

    Returns:
        tuple: (h, s, v) where:
            h (float): Hue in degrees (0-360)
            s (float): Saturation percentage (0-100)
            v (float): Value percentage (0-100)
    """
    # Normalize RGB values to [0, 1] range
    r_normalized = r / 255.0
    g_normalized = g / 255.0
    b_normalized = b / 255.0

    # Find max and min values
    max_val = max(r_normalized, g_normalized, b_normalized)
    min_val = min(r_normalized, g_normalized, b_normalized)
    delta = max_val - min_val

    # Calculate Hue
    if max_val == min_val:
        hue = 0.0
    elif max_val == r_normalized:
        hue = (60 * ((g_normalized - b_normalized) / delta) + 360) % 360
    elif max_val == g_normalized:
        hue = (60 * ((b_normalized - r_normalized) / delta) + 120) % 360
    elif max_val == b_normalized:
        hue = (60 * ((r_normalized - g_normalized) / delta) + 240) % 360

    # Calculate Saturation
    if max_val == 0:
        saturation = 0.0
    else:
        saturation = (delta / max_val) * 100

    # Calculate Value
    value = max_val * 100

    return hue, saturation, value
