import matplotlib as mpl
import pytest

from shared.plotting import PALETTE, figure, mark_current, nice_limit


def test_figure_style():
    fig, ax = figure()
    assert mpl.colors.to_hex(fig.get_facecolor()) == "#ffffff"
    assert not ax.spines["top"].get_visible()
    assert mpl.rcParams["font.size"] >= 11


def test_mark_current_is_orange():
    _, ax = figure()
    mark_current(ax, 1.0, 2.0)
    (line,) = ax.get_lines()
    assert mpl.colors.to_hex(line.get_color()) == PALETTE["current"].lower()


@pytest.mark.parametrize(
    ("value", "expected"),
    [(1.43, 2), (2.0, 2), (3.1, 5), (7.0, 10), (0.012, 0.02), (-140, 200), (0, 1)],
)
def test_nice_limit(value, expected):
    assert nice_limit(value) == pytest.approx(expected)
