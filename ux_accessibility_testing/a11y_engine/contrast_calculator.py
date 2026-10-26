"""
W3C WCAG 2.1 Relative Luminance & Color Contrast Ratio Engine.
Implements W3C formula: Contrast = (L1 + 0.05) / (L2 + 0.05)
"""
from typing import Tuple


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)


def srgb_channel_to_linear(channel: int) -> float:
    c = channel / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def calculate_relative_luminance(r: int, g: int, b: int) -> float:
    """Calculates relative luminance L in the range 0.0 to 1.0."""
    r_lin = srgb_channel_to_linear(r)
    g_lin = srgb_channel_to_linear(g)
    b_lin = srgb_channel_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def calculate_contrast_ratio(color1_hex: str, color2_hex: str) -> float:
    """Returns contrast ratio between 1.0 and 21.0."""
    r1, g1, b1 = hex_to_rgb(color1_hex)
    r2, g2, b2 = hex_to_rgb(color2_hex)

    lum1 = calculate_relative_luminance(r1, g1, b1)
    lum2 = calculate_relative_luminance(r2, g2, b2)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def evaluate_wcag_contrast(ratio: float, is_large_text: bool = False) -> dict:
    threshold_aa = 3.0 if is_large_text else 4.5
    threshold_aaa = 4.5 if is_large_text else 7.0

    return {
        "contrast_ratio": ratio,
        "required_aa": threshold_aa,
        "pass_aa": ratio >= threshold_aa,
        "required_aaa": threshold_aaa,
        "pass_aaa": ratio >= threshold_aaa,
    }
