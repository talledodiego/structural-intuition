"""Validation of core.py: Timoshenko & Gere ch. 2, hand calculations, tables."""

import math

import numpy as np
import pytest

from .core import (
    MATERIALS,
    PROFILES,
    SUPPORTS,
    capacity,
    circular_section,
    critical_load,
    custom_section,
    effective_length,
    euler_load,
    governing_failure,
    i_section_geometry,
    load_axis_limit,
    load_steps,
    member_state,
    mode_shape,
    profile_section,
    radius_of_gyration,
    rectangular_section,
    slenderness,
    snap_load,
    squash_load,
    transition_slenderness,
)

STEEL = MATERIALS["steel"]


# --- Hand calculations (README.md, Validation) ----------------------------


def test_hea120_default_buckles():
    """HEA120 S235, L = 3 m, pinned–pinned, weak axis: Pcr = 532 kN < Npl = 596 kN."""
    s = profile_section("HEA120")
    L0 = effective_length(3000.0, "pinned_pinned")
    P_cr = critical_load(STEEL.E, s.J_weak, L0)
    N_pl = squash_load(s.A, STEEL.f)
    lam = slenderness(L0, radius_of_gyration(s.J_weak, s.A))
    assert P_cr == pytest.approx(531.7e3, rel=1e-3)
    assert N_pl == pytest.approx(595.5e3, rel=1e-3)
    assert lam == pytest.approx(99.4, abs=0.1)
    assert member_state(560e3, P_cr, N_pl) == "buckling"
    assert member_state(500e3, P_cr, N_pl) == "ok"


def test_hea300_material_governs():
    """HEA300 S235, L = 3 m, weak axis: Pcr = 14 530 kN, Npl = 2644 kN, λ = 40.1."""
    s = profile_section("HEA300")
    L0 = effective_length(3000.0, "pinned_pinned")
    P_cr = critical_load(STEEL.E, s.J_weak, L0)
    N_pl = squash_load(s.A, STEEL.f)
    assert P_cr == pytest.approx(14.53e6, rel=1e-3)
    assert N_pl == pytest.approx(2.644e6, rel=1e-3)
    assert slenderness(L0, radius_of_gyration(s.J_weak, s.A)) == pytest.approx(
        40.1, abs=0.1
    )
    assert governing_failure(P_cr, N_pl) == "material"
    assert member_state(3e6, P_cr, N_pl) == "crushing"


@pytest.mark.parametrize(
    ("support", "beta"),
    [
        ("pinned_pinned", 1.0),
        ("fixed_free", 2.0),
        ("fixed_pinned", 0.7),
        ("fixed_fixed", 0.5),
        ("fixed_guided", 1.0),
    ],
)
def test_critical_load_each_support(support, beta):
    """Pcr = π² E J / (β L)² for each support case (E = 210 GPa, J = 1e6 mm⁴)."""
    L = 4000.0
    expected = math.pi**2 * 210_000.0 * 1e6 / (beta * L) ** 2
    assert critical_load(210_000.0, 1e6, effective_length(L, support)) == (
        pytest.approx(expected)
    )


def test_fixed_pinned_beta_close_to_exact():
    assert SUPPORTS["fixed_pinned"] == pytest.approx(math.pi / 4.4934, abs=2e-3)


def test_transition_slenderness():
    """λ₁ = π √(E/f): 93.9 (S235), 71.9 (C24), 110.6 (C25/30)."""
    assert transition_slenderness(*MATERIALS["steel"]) == pytest.approx(93.9, abs=0.1)
    assert transition_slenderness(*MATERIALS["timber"]) == pytest.approx(71.9, abs=0.1)
    assert transition_slenderness(*MATERIALS["concrete"]) == pytest.approx(
        110.6, abs=0.1
    )


def test_pcr_equals_npl_at_transition_slenderness():
    E, f = STEEL
    A = 1000.0
    lam1 = transition_slenderness(E, f)
    assert euler_load(lam1, E, A) == pytest.approx(squash_load(A, f))


def test_euler_hyperbola_matches_critical_load():
    s = rectangular_section(100.0, 160.0)
    L0 = 3000.0
    lam = slenderness(L0, radius_of_gyration(s.J_weak, s.A))
    assert euler_load(lam, 11_000.0, s.A) == pytest.approx(
        critical_load(11_000.0, s.J_weak, L0)
    )


# --- Scaling --------------------------------------------------------------


def test_scaling():
    base = critical_load(210_000.0, 1e6, 3000.0)
    assert critical_load(210_000.0, 1e6, 6000.0) == pytest.approx(base / 4)
    assert critical_load(420_000.0, 1e6, 3000.0) == pytest.approx(2 * base)
    assert critical_load(210_000.0, 3e6, 3000.0) == pytest.approx(3 * base)


def test_capacity_and_states():
    assert capacity(100.0, 200.0) == 100.0
    assert member_state(150.0, 100.0, 200.0) == "buckling"
    assert member_state(250.0, 300.0, 200.0) == "crushing"
    assert member_state(0.0, 100.0, 200.0) == "ok"


# --- Sections -------------------------------------------------------------


def test_rectangular_section():
    s = rectangular_section(100.0, 200.0)
    assert s.A == pytest.approx(20_000.0)
    assert s.J_strong == pytest.approx(100.0 * 200.0**3 / 12)
    assert s.J_weak == pytest.approx(200.0 * 100.0**3 / 12)
    # Strong/weak do not depend on which side is called b.
    assert rectangular_section(200.0, 100.0) == s


def test_circular_section():
    s = circular_section(60.0)
    assert s.A == pytest.approx(2827.4, rel=1e-4)
    assert s.J_strong == s.J_weak == pytest.approx(636_172.5, rel=1e-6)
    assert radius_of_gyration(s.J_weak, s.A) == pytest.approx(15.0)  # d/4


def test_custom_section_orders_axes():
    assert custom_section(5000.0, 1e7, 5e7) == (5000.0, 5e7, 1e7)


@pytest.mark.parametrize("name", list(PROFILES))
def test_profile_table_matches_geometry(name):
    """Tabulated A, J_y, J_z agree with the dimensions (fillets included)."""
    p = PROFILES[name]
    g = i_section_geometry(p)
    assert g.A == pytest.approx(p.A, rel=2e-3)
    assert g.J_strong == pytest.approx(p.J_y, rel=3e-3)
    assert g.J_weak == pytest.approx(p.J_z, rel=3e-3)
    assert p.J_y > p.J_z


# --- Load slider range ----------------------------------------------------


def test_load_axis_limit():
    assert load_axis_limit(595.5e3) == pytest.approx(1000e3)  # HEA120: 893 kN
    assert load_axis_limit(2.644e6) == pytest.approx(5e6)  # HEA300
    assert load_axis_limit(1e6 / 1.5) == pytest.approx(1e6)  # exact 1-2-5 value


@pytest.mark.parametrize("N_pl", [595.49e3, 2.644e6, 6.597e3, 1e6, 1265.1e3])
def test_load_steps_end_at_npl(N_pl):
    """The slider starts at 0 and ends at Npl rounded up to 10 kN."""
    steps = load_steps(N_pl)
    assert steps[0] == 0.0
    assert N_pl <= steps[-1] < N_pl + 10e3
    assert steps[-1] % 10e3 == 0
    assert np.all(np.diff(steps) > 0)
    assert 100 <= len(steps) <= 401


@pytest.mark.parametrize(
    ("N_pl", "last"), [(395.5e3, 400e3), (1265.1e3, 1270e3), (400e3, 400e3)]
)
def test_load_steps_rounding(N_pl, last):
    """Examples from the review: 395.5 → 400 kN, 1265.1 → 1270 kN."""
    assert load_steps(N_pl)[-1] == pytest.approx(last)


def test_load_steps_hea120():
    """Npl = 595.49 kN: steps of 5 kN up to 600 kN."""
    steps = load_steps(595.49e3)
    assert steps[1] == pytest.approx(5e3)
    assert steps[-2] == pytest.approx(595e3)
    assert steps[-1] == pytest.approx(600e3)
    # At the end of the slider the material limit is reached.
    assert member_state(steps[-1], 1e9, 595.49e3) == "crushing"


def test_snap_load():
    steps = load_steps(595.49e3)
    assert snap_load(560e3, steps) == pytest.approx(560e3)
    assert snap_load(1e7, steps) == pytest.approx(600e3)
    assert snap_load(-5.0, steps) == 0.0


# --- Buckling modes -------------------------------------------------------

X = np.linspace(0.0, 1.0, 4001)


def _slope(v):
    return np.gradient(v, X)


@pytest.mark.parametrize("support", list(SUPPORTS))
def test_mode_normalised_and_zero_at_base(support):
    v = mode_shape(X, 1.0, support)
    assert np.max(np.abs(v)) == pytest.approx(1.0, abs=1e-6)
    assert v[0] == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize(
    ("support", "top_displacement_zero", "base_fixed", "top_slope_zero"),
    [
        ("pinned_pinned", True, False, False),
        ("fixed_free", False, True, False),
        ("fixed_pinned", True, True, False),
        ("fixed_fixed", True, True, True),
        ("fixed_guided", False, True, True),
    ],
)
def test_mode_boundary_conditions(
    support, top_displacement_zero, base_fixed, top_slope_zero
):
    v = mode_shape(X, 1.0, support)
    dv = _slope(v)
    if top_displacement_zero:
        assert v[-1] == pytest.approx(0.0, abs=1e-9)
    else:
        assert abs(v[-1]) > 0.5
    if base_fixed:
        assert dv[0] == pytest.approx(0.0, abs=1e-2)
    else:
        assert abs(dv[0]) > 1.0
    if top_slope_zero:
        assert dv[-1] == pytest.approx(0.0, abs=1e-2)


def test_fixed_pinned_zero_moment_at_top():
    """Pinned top: v''(L) = 0."""
    v = mode_shape(X, 1.0, "fixed_pinned")
    d2v = np.gradient(_slope(v), X)
    assert abs(d2v[-3]) < 1e-2 * np.max(np.abs(d2v))


def test_mode_satisfies_differential_equation():
    """EJ v'''' + P v'' = 0 with P = Pcr, i.e. v'''' = −k² v'', k = π/L0."""
    for support, beta in SUPPORTS.items():
        if support == "fixed_pinned":
            k = 4.493409457909064  # exact eigenvalue, not the rounded β = 0.7
        else:
            k = math.pi / beta
        x = np.linspace(0.2, 0.8, 7)
        h = 1e-3

        def v(s, support=support):
            return mode_shape(np.asarray(s), 1.0, support)

        d2 = (v(x + h) - 2 * v(x) + v(x - h)) / h**2
        d4 = (
            v(x + 2 * h) - 4 * v(x + h) + 6 * v(x) - 4 * v(x - h) + v(x - 2 * h)
        ) / h**4
        np.testing.assert_allclose(d4, -(k**2) * d2, rtol=1e-3, atol=1e-3 * k**4)
