"""Euler buckling of an ideal column compared with the strength of its material.

Pure functions, no UI, no display text. Internal units: N, mm, MPa (= N/mm²);
second moments of area in mm⁴.

Sign convention: compression positive (P > 0 compresses the member).

The member is vertical, x measured upwards from the base (x = 0) to the top
(x = L). The base is fixed or pinned; the top is free, pinned, fixed or
guided (see ``SUPPORTS``). Top restraints let the top move vertically, so the
load P is always carried by the member.
"""

from __future__ import annotations

import math
from typing import NamedTuple

import numpy as np
from numpy.typing import ArrayLike

# Effective length factors β (L0 = β L), Timoshenko & Gere, ch. 2. The exact
# value for fixed–pinned is π / 4.4934 = 0.699; 0.7 is the customary rounding.
SUPPORTS = {
    "pinned_pinned": 1.0,
    "fixed_free": 2.0,
    "fixed_pinned": 0.7,
    "fixed_fixed": 0.5,
    "fixed_guided": 1.0,
}

# Smallest root of tan(kL) = kL: the fixed–pinned column.
_KL_FIXED_PINNED = 4.493409457909064


class Material(NamedTuple):
    """Young's modulus E and indicative (characteristic) strength f [MPa]."""

    E: float
    f: float


# Indicative values, no partial safety factors (see README.md).
MATERIALS = {
    "steel": Material(E=210_000.0, f=235.0),  # S235, f = f_y
    "timber": Material(E=11_000.0, f=21.0),  # C24, E0,mean and f_c,0,k
    "concrete": Material(E=31_000.0, f=25.0),  # C25/30, E_cm and f_ck
}


class Section(NamedTuple):
    """Area A [mm²] and second moments of area [mm⁴] about the two axes."""

    A: float
    J_strong: float
    J_weak: float


class Profile(NamedTuple):
    """Rolled I-section: dimensions [mm] and tabulated properties.

    ``A`` [mm²], ``J_y`` (strong axis) and ``J_z`` (weak axis) [mm⁴] include
    the root fillets of radius ``r``.
    """

    h: float
    b: float
    tw: float
    tf: float
    r: float
    A: float
    J_y: float
    J_z: float


def _profile(h, b, tw, tf, r, A_cm2, Jy_cm4, Jz_cm4) -> Profile:
    return Profile(h, b, tw, tf, r, A_cm2 * 1e2, Jy_cm4 * 1e4, Jz_cm4 * 1e4)


# ArcelorMittal sales programme (h, b, tw, tf, r in mm; A in cm²; J in cm⁴).
PROFILES = {
    "HEA100": _profile(96, 100, 5.0, 8.0, 12, 21.24, 349.2, 133.8),
    "HEA120": _profile(114, 120, 5.0, 8.0, 12, 25.34, 606.2, 230.9),
    "HEA140": _profile(133, 140, 5.5, 8.5, 12, 31.42, 1033, 389.3),
    "HEA160": _profile(152, 160, 6.0, 9.0, 15, 38.77, 1673, 615.6),
    "HEA180": _profile(171, 180, 6.0, 9.5, 15, 45.25, 2510, 924.6),
    "HEA200": _profile(190, 200, 6.5, 10.0, 18, 53.83, 3692, 1336),
    "HEA220": _profile(210, 220, 7.0, 11.0, 18, 64.34, 5410, 1955),
    "HEA240": _profile(230, 240, 7.5, 12.0, 21, 76.84, 7763, 2769),
    "HEA260": _profile(250, 260, 7.5, 12.5, 24, 86.82, 10450, 3668),
    "HEA280": _profile(270, 280, 8.0, 13.0, 24, 97.26, 13670, 4763),
    "HEA300": _profile(290, 300, 8.5, 14.0, 27, 112.5, 18260, 6310),
    "HEA320": _profile(310, 300, 9.0, 15.5, 27, 124.4, 22930, 6985),
    "HEA340": _profile(330, 300, 9.5, 16.5, 27, 133.5, 27690, 7436),
    "HEA360": _profile(350, 300, 10.0, 17.5, 27, 142.8, 33090, 7887),
    "HEA400": _profile(390, 300, 11.0, 19.0, 27, 159.0, 45070, 8564),
    "IPE100": _profile(100, 55, 4.1, 5.7, 7, 10.32, 171.0, 15.92),
    "IPE120": _profile(120, 64, 4.4, 6.3, 7, 13.21, 317.8, 27.67),
    "IPE140": _profile(140, 73, 4.7, 6.9, 7, 16.43, 541.2, 44.92),
    "IPE160": _profile(160, 82, 5.0, 7.4, 9, 20.09, 869.3, 68.31),
    "IPE180": _profile(180, 91, 5.3, 8.0, 9, 23.95, 1317, 100.9),
    "IPE200": _profile(200, 100, 5.6, 8.5, 12, 28.48, 1943, 142.4),
    "IPE220": _profile(220, 110, 5.9, 9.2, 12, 33.37, 2772, 204.9),
    "IPE240": _profile(240, 120, 6.2, 9.8, 15, 39.12, 3892, 283.6),
    "IPE270": _profile(270, 135, 6.6, 10.2, 15, 45.95, 5790, 419.9),
    "IPE300": _profile(300, 150, 7.1, 10.7, 15, 53.81, 8356, 603.8),
    "IPE330": _profile(330, 160, 7.5, 11.5, 18, 62.61, 11770, 788.1),
    "IPE360": _profile(360, 170, 8.0, 12.7, 18, 72.73, 16270, 1043),
    "IPE400": _profile(400, 180, 8.6, 13.5, 21, 84.46, 23130, 1318),
}


# --- Cross-sections -------------------------------------------------------


def rectangular_section(b: float, h: float) -> Section:
    """Solid rectangle b × h: A = b h, J = b h³/12 and h b³/12."""
    J1, J2 = b * h**3 / 12.0, h * b**3 / 12.0
    return Section(b * h, max(J1, J2), min(J1, J2))


def circular_section(d: float) -> Section:
    """Solid circle of diameter d: A = π d²/4, J = π d⁴/64 about any axis."""
    J = math.pi * d**4 / 64.0
    return Section(math.pi * d**2 / 4.0, J, J)


def profile_section(name: str) -> Section:
    """Tabulated properties of a rolled I-section from ``PROFILES``."""
    p = PROFILES[name]
    return Section(p.A, p.J_y, p.J_z)


def custom_section(A: float, J_y: float, J_z: float) -> Section:
    """Section from given A, J_y, J_z; the larger J is the strong axis."""
    return Section(A, max(J_y, J_z), min(J_y, J_z))


def i_section_geometry(p: Profile) -> Section:
    """A, J_y, J_z of an I-section computed from its dimensions.

    Two flanges b × t_f, a web t_w × (h − 2 t_f) and four root fillets, each a
    square r × r minus a quarter circle: area (1 − π/4) r², centroid at
    r (10 − 3π)/(12 − 3π) from the two sides of the corner (own second
    moment of area neglected). Used to check the table values.
    """
    hw = p.h - 2.0 * p.tf
    a = (1.0 - math.pi / 4.0) * p.r**2
    c = p.r * (10.0 - 3.0 * math.pi) / (12.0 - 3.0 * math.pi)
    A = 2.0 * p.b * p.tf + hw * p.tw + 4.0 * a
    J_y = (p.b * p.h**3 - (p.b - p.tw) * hw**3) / 12.0 + 4.0 * a * (
        p.h / 2.0 - p.tf - c
    ) ** 2
    J_z = (2.0 * p.tf * p.b**3 + hw * p.tw**3) / 12.0 + 4.0 * a * (p.tw / 2.0 + c) ** 2
    return Section(A, J_y, J_z)


# --- Buckling and strength ------------------------------------------------


def effective_length(L: float, support: str) -> float:
    """Effective (buckling) length L0 = β L  [mm]."""
    return SUPPORTS[support] * L


def critical_load(E: float, J: float, L0: float) -> float:
    """Euler critical load Pcr = π² E J / L0²  [N]."""
    return math.pi**2 * E * J / L0**2


def radius_of_gyration(J: float, A: float) -> float:
    """Radius of gyration i = √(J / A)  [mm]."""
    return math.sqrt(J / A)


def slenderness(L0: float, i: float) -> float:
    """Slenderness λ = L0 / i  [-]."""
    return L0 / i


def squash_load(A: float, f: float) -> float:
    """Material limit Npl = A f  [N] (squashing, or yielding for steel)."""
    return A * f


def transition_slenderness(E: float, f: float) -> float:
    """λ₁ = π √(E / f): slenderness at which Pcr = Npl  [-]."""
    return math.pi * math.sqrt(E / f)


def euler_load(lam: ArrayLike, E: float, A: float) -> ArrayLike:
    """Euler hyperbola Pcr(λ) = π² E A / λ²  [N] for a section of area A."""
    lam = np.asarray(lam, dtype=float)
    with np.errstate(divide="ignore"):
        return np.pi**2 * E * A / lam**2


def capacity(P_cr: float, N_pl: float) -> float:
    """Load capacity of the ideal member: min(Pcr, Npl)  [N]."""
    return min(P_cr, N_pl)


def governing_failure(P_cr: float, N_pl: float) -> str:
    """``"buckling"`` if Pcr < Npl, otherwise ``"material"``."""
    return "buckling" if P_cr < N_pl else "material"


def member_state(P: float, P_cr: float, N_pl: float) -> str:
    """State of the member under the load P.

    ``"ok"`` if P < min(Pcr, Npl); otherwise ``"buckling"`` or ``"crushing"``,
    according to which limit is reached first.
    """
    if P < capacity(P_cr, N_pl):
        return "ok"
    return "buckling" if governing_failure(P_cr, N_pl) == "buckling" else "crushing"


def _nice_up(value: float) -> float:
    """Smallest 1-2-5 × 10^k value ≥ ``value`` (> 0)."""
    power = 10.0 ** math.floor(math.log10(value))
    return next(s * power for s in (1, 2, 5, 10) if s * power >= value * (1 - 1e-9))


def load_axis_limit(N_pl: float) -> float:
    """Upper limit of the load axis of the chart [N].

    The smallest 1-2-5 × 10^k value ≥ 1.5 Npl: it depends only on section and
    material, and leaves room above the material limit.
    """
    return _nice_up(1.5 * N_pl)


def load_steps(N_pl: float, n: int = 200) -> np.ndarray:
    """Values of the load slider, from 0 to Npl [N].

    The last value is Npl rounded up to 10 kN (395.5 → 400 kN), so that the
    slider reaches the material limit and goes beyond it by less than 10 kN
    (an ideal member cannot carry more than Npl). The other values are about
    ``n`` steps of a 1-2-5 × 10^k size.
    """
    last = math.ceil(N_pl / 1e4) * 1e4
    step = _nice_up(last / n)
    values = np.arange(0.0, last, step)
    # Drop a value too close to the last one, which would be hard to pick.
    values = values[values < last - 0.5 * step]
    return np.append(values, last)


def snap_load(P: float, steps: ArrayLike) -> float:
    """The value in ``steps`` nearest to P [N]."""
    steps = np.asarray(steps, dtype=float)
    return float(steps[np.argmin(np.abs(steps - P))])


# --- Buckling mode --------------------------------------------------------


def mode_shape(x: ArrayLike, L: float, support: str) -> np.ndarray:
    """First buckling mode v(x), 0 ≤ x ≤ L, scaled to max |v| = 1.

    - pinned–pinned:  v = sin(πx/L)
    - fixed–free:     v = 1 − cos(πx/2L)
    - fixed–pinned:   v = sin kx − kx + kL (1 − cos kx), tan kL = kL
    - fixed–fixed:    v = 1 − cos(2πx/L)
    - fixed–guided:   v = 1 − cos(πx/L)
    """
    s = np.asarray(x, dtype=float) / L
    if support == "pinned_pinned":
        v = np.sin(np.pi * s)
    elif support == "fixed_free":
        v = 1.0 - np.cos(np.pi * s / 2.0)
    elif support == "fixed_pinned":
        k = _KL_FIXED_PINNED
        v = np.sin(k * s) - k * s + k * (1.0 - np.cos(k * s))
    elif support == "fixed_fixed":
        v = 1.0 - np.cos(2.0 * np.pi * s)
    elif support == "fixed_guided":
        v = 1.0 - np.cos(np.pi * s)
    else:
        raise ValueError(f"unknown support: {support}")
    # Normalise on the whole member, not only on the points requested.
    return v / _mode_peak(support)


def _mode_peak(support: str) -> float:
    """max |v| over 0 ≤ x ≤ L of the unscaled mode."""
    if support == "fixed_pinned":
        k = _KL_FIXED_PINNED
        s = np.linspace(0.0, 1.0, 2001)
        return float(np.max(np.abs(np.sin(k * s) - k * s + k * (1.0 - np.cos(k * s)))))
    return 2.0 if support in ("fixed_fixed", "fixed_guided") else 1.0
