"""Axially loaded bar, linear elastic (Hooke's law).

Template example: a minimal but complete ``core.py``. Pure functions, no UI,
no display text. Internal units: N, mm, MPa (= N/mm²).

Sign convention: tension positive (N > 0 elongates the bar).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def axial_stress(force: ArrayLike, area: float) -> ArrayLike:
    """Normal stress σ = N / A  [MPa]."""
    return np.divide(force, area)


def axial_strain(stress: ArrayLike, modulus: float) -> ArrayLike:
    """Axial strain ε = σ / E  [-] (Hooke's law)."""
    return np.divide(stress, modulus)


def axial_stiffness(length: float, modulus: float, area: float) -> float:
    """Axial stiffness of the member k = E A / L  [N/mm]."""
    return modulus * area / length


def elongation(
    force: ArrayLike, length: float, modulus: float, area: float
) -> ArrayLike:
    """Change in length ΔL = N L / (E A) = ε L  [mm]."""
    return np.divide(force, axial_stiffness(length, modulus, area))


def lateral_strain(strain: ArrayLike, poisson: float) -> ArrayLike:
    """Transverse strain ε_t = −ν ε  [-] (isotropic material, uniaxial stress)."""
    return np.multiply(-poisson, strain)


def equivalent_diameter(area: float) -> float:
    """Diameter of the solid circular section with area A: d = √(4A/π)  [mm]."""
    return float(np.sqrt(4.0 * area / np.pi))


def drawing_magnification(
    requested: float,
    strain: float,
    poisson: float,
    max_relative_change: float = 0.5,
) -> float:
    """Magnification actually used to draw the deformed bar.

    The drawn length and width are L(1 + s ε) and d(1 + s ε_t). The factor
    ``requested`` is reduced, if needed, so that neither changes by more than
    ``max_relative_change``: otherwise a large magnification in compression
    would draw a bar with zero or negative length.
    """
    largest = max(abs(strain), abs(poisson * strain))
    if largest == 0:
        return float(requested)
    return float(min(requested, max_relative_change / largest))


def bar_outline(length: float, width: float) -> tuple[np.ndarray, np.ndarray]:
    """Closed rectangle of a bar along x from 0 to ``length``, centred on y = 0."""
    half = width / 2.0
    x = np.array([0.0, length, length, 0.0, 0.0])
    y = np.array([-half, -half, half, half, -half])
    return x, y


def deformed_dimensions(
    length: float,
    diameter: float,
    strain: float,
    poisson: float,
    magnification: float = 1.0,
) -> tuple[float, float]:
    """Drawn length and width of the deformed bar, displacements magnified.

    Returns ``(L (1 + s ε), d (1 + s ε_t))`` with ε_t = −ν ε. The bar is
    restrained axially at x = 0 and free to contract laterally.
    """
    lateral = float(lateral_strain(strain, poisson))
    return (
        length * (1.0 + magnification * strain),
        diameter * (1.0 + magnification * lateral),
    )
