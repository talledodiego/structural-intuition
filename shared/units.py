"""Conversions between display units and the internal N, mm, MPa system.

See docs/style.md. ``core.py`` works only in N, mm, MPa; ``app.py`` converts
inputs before calling it and results before showing them. Functions accept
floats or NumPy arrays.
"""

import math


def m_to_mm(x):
    return x * 1e3


def mm_to_m(x):
    return x * 1e-3


def kn_to_n(x):
    return x * 1e3


def n_to_kn(x):
    return x * 1e-3


def knm_to_nmm(x):
    return x * 1e6


def nmm_to_knm(x):
    return x * 1e-6


def gpa_to_mpa(x):
    return x * 1e3


def mpa_to_gpa(x):
    return x * 1e-3


def fmt(value: float, sig: int = 3) -> str:
    """Format with ``sig`` significant figures, a dot as decimal separator.

    Examples: 1.4286 -> "1.43", 0.000714 -> "0.000714", 245123 -> "245000".
    """
    if value == 0:
        return "0"
    digits = sig - 1 - math.floor(math.log10(abs(value)))
    value = round(value, digits)
    # Rounding may add a digit (9.996 -> 10.0): count again.
    digits = sig - 1 - math.floor(math.log10(abs(value)))
    return f"{round(value, digits):.{max(0, digits)}f}"
