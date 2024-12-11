# Function to find the closest 2-digit hex value for an RGB color
def rgb_to_hex(color_code):
    # If hex string was passed in, convert to RGB tuple
    if isinstance(color_code, str):
        color_code = tuple(int(color_code.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Handle special cases
    if color_code == (0, 0, 0):  # "off"
        return "FE"
    if color_code == (255, 255, 255):  # "white"
        return "FF"

    # Predefined data points for color matching
    data_points = {
        0x00: (255, 0, 0), 0x07: (252, 136, 59), 0x10: (251, 250, 110),
        0x17: (218, 240, 91), 0x20: (178, 240, 83), 0x27: (139, 243, 69),
        0x30: (18, 245, 79), 0x37: (0, 247, 78), 0x40: (0, 255, 182),
        0x47: (0, 255, 255), 0x50: (0, 196, 250), 0x57: (0, 174, 254),
        0x60: (0, 137, 251), 0x67: (0, 117, 253), 0x70: (0, 64, 253),
        0x77: (0, 1, 255), 0x80: (91, 0, 255), 0x87: (103, 0, 255),
        0x90: (146, 0, 255), 0x97: (164, 0, 254), 0xA0: (190, 0, 254),
        0xA7: (255, 0, 253), 0xB0: (255, 0, 191), 0xB7: (255, 80, 14),
        0xC0: (250, 198, 85), 0xC7: (245, 237, 91), 0xD0: (203, 236, 83),
        0xD7: (168, 239, 93), 0xE0: (106, 242, 95), 0xE7: (14, 245, 93),
        0xF0: (0, 249, 85), 0xF7: (0, 242, 211), 0xFC: (0, 234, 243),
        0xFD: (252, 181, 141), 0xFE: (0, 0, 0), 0xFF: (255, 255, 255),
    }

    # Find the closest match using squared distance
    closest_key = min(
        data_points, 
        key=lambda k: sum((a - b) ** 2 for a, b in zip(data_points[k], color_code))
    )
    return f"{closest_key:02X}"
