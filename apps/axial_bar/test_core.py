"""Validation of core.py against hand calculations (Hooke's law, ΔL = N L / E A).

Reference case = the applet defaults: steel bar, L = 1 m, A = 200 mm²,
E = 210 GPa, ν = 0.3, N = 10 kN.
    σ   = 10 000 / 200                         = 50 MPa
    ε   = 50 / 210 000                         = 2.381e-4  (0.238 ‰)
    ΔL  = 10 000 · 1000 / (210 000 · 200)      = 0.2381 mm
    ε_t = −0.3 · 2.381e-4                      = −7.143e-5
    d   = √(4 · 200 / π)                       = 15.96 mm
    Δd  = ε_t · d                              = −0.00114 mm
"""

import numpy as np
import pytest

from .core import (
    axial_stiffness,
    axial_strain,
    axial_stress,
    bar_outline,
    deformed_dimensions,
    drawing_magnification,
    elongation,
    equivalent_diameter,
    lateral_strain,
)

N = 10_000.0  # N
L = 1000.0  # mm
A = 200.0  # mm²
E = 210_000.0  # MPa
NU = 0.3


def test_reference_case_hand_calculation():
    assert axial_stress(N, A) == pytest.approx(50.0)
    assert axial_strain(50.0, E) == pytest.approx(2.3810e-4, rel=1e-4)
    assert elongation(N, L, E, A) == pytest.approx(0.23810, rel=1e-4)
    assert lateral_strain(2.3810e-4, NU) == pytest.approx(-7.1429e-5, rel=1e-4)
    d = equivalent_diameter(A)
    assert d == pytest.approx(15.958, rel=1e-4)
    assert lateral_strain(2.3810e-4, NU) * d == pytest.approx(-1.1398e-3, rel=1e-3)


def test_elongation_equals_strain_times_length():
    eps = axial_strain(axial_stress(N, A), E)
    assert elongation(N, L, E, A) == pytest.approx(eps * L)


def test_stiffness_relates_force_and_elongation():
    assert N / elongation(N, L, E, A) == pytest.approx(axial_stiffness(L, E, A))


@pytest.mark.parametrize("factor", [0.5, 2.0, 3.0])
def test_scaling(factor):
    base = elongation(N, L, E, A)
    assert elongation(factor * N, L, E, A) == pytest.approx(factor * base)
    assert elongation(N, factor * L, E, A) == pytest.approx(factor * base)
    assert elongation(N, L, factor * E, A) == pytest.approx(base / factor)
    assert elongation(N, L, E, factor * A) == pytest.approx(base / factor)


def test_stress_strain_independent_of_length():
    # σ–ε describes the material; only F–ΔL depends on the member's L.
    eps_short = axial_strain(axial_stress(N, A), E)
    assert elongation(N, 2 * L, E, A) / (2 * L) == pytest.approx(eps_short)


def test_tension_positive_compression_negative():
    assert elongation(N, L, E, A) > 0
    assert elongation(-N, L, E, A) < 0
    assert lateral_strain(1e-3, NU) < 0  # tension: the bar gets thinner
    assert lateral_strain(-1e-3, NU) > 0  # compression: the bar gets thicker


def test_vectorised_over_force():
    forces = np.array([-N, 0.0, N])
    np.testing.assert_allclose(
        elongation(forces, L, E, A), [-0.23810, 0.0, 0.23810], rtol=1e-4
    )


def test_equivalent_diameter():
    assert equivalent_diameter(np.pi * 20.0**2 / 4.0) == pytest.approx(20.0)


def test_deformed_dimensions_unmagnified():
    eps = 1e-3
    length, width = deformed_dimensions(L, 36.0, eps, NU)
    assert length == pytest.approx(L * (1 + eps))
    assert width == pytest.approx(36.0 * (1 - NU * eps))


def test_deformed_dimensions_magnified():
    length, width = deformed_dimensions(L, 36.0, 1e-3, NU, magnification=100)
    assert length == pytest.approx(L * 1.1)
    assert width == pytest.approx(36.0 * (1 - 0.03))


def test_zero_poisson_keeps_width():
    _, width = deformed_dimensions(L, 36.0, 1e-3, 0.0, magnification=500)
    assert width == pytest.approx(36.0)


def test_drawing_magnification_not_limited_for_small_strains():
    assert drawing_magnification(100.0, 4.76e-4, NU) == 100.0


def test_drawing_magnification_limited_in_compression():
    s = drawing_magnification(1000.0, -4.76e-3, NU)
    length, _ = deformed_dimensions(L, 36.0, -4.76e-3, NU, magnification=s)
    assert s < 1000.0
    assert length == pytest.approx(0.5 * L)


def test_drawing_magnification_zero_strain():
    assert drawing_magnification(50.0, 0.0, NU) == 50.0


def test_bar_outline_is_closed_rectangle():
    x, y = bar_outline(L, 36.0)
    assert (x[0], y[0]) == (x[-1], y[-1])
    assert x.max() == L and x.min() == 0.0
    assert y.max() == pytest.approx(18.0) and y.min() == pytest.approx(-18.0)
