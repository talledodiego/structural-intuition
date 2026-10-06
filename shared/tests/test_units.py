import numpy as np
import pytest

from shared import units


def test_conversions():
    assert units.m_to_mm(3.0) == pytest.approx(3000.0)
    assert units.kn_to_n(245.0) == pytest.approx(245_000.0)
    assert units.knm_to_nmm(12.5) == pytest.approx(12.5e6)
    assert units.gpa_to_mpa(210.0) == pytest.approx(210_000.0)
    assert units.mm_to_m(units.m_to_mm(2.5)) == pytest.approx(2.5)
    assert units.n_to_kn(units.kn_to_n(7.0)) == pytest.approx(7.0)
    assert units.nmm_to_knm(units.knm_to_nmm(4.0)) == pytest.approx(4.0)
    assert units.mpa_to_gpa(units.gpa_to_mpa(70.0)) == pytest.approx(70.0)


def test_conversions_accept_arrays():
    np.testing.assert_allclose(units.m_to_mm(np.array([1.0, 2.5])), [1000, 2500])


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1.4286, "1.43"),
        (0.000714286, "0.000714"),
        (245123.0, "245000"),
        (9.996, "10.0"),
        (-0.5, "-0.500"),
        (0.0, "0"),
    ],
)
def test_fmt(value, expected):
    assert units.fmt(value) == expected
