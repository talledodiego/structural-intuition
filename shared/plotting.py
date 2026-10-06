"""Plot defaults and palette from docs/style.md."""

import math

import matplotlib as mpl
from matplotlib.figure import Figure

from shared.style import PALETTE

STYLE = {
    "figure.facecolor": PALETTE["background"],
    "axes.facecolor": PALETTE["background"],
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.edgecolor": PALETTE["reference"],
    "axes.labelcolor": PALETTE["reference"],
    "xtick.color": PALETTE["reference"],
    "ytick.color": PALETTE["reference"],
    "axes.grid": True,
    "grid.color": PALETTE["grid"],
    "axes.axisbelow": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
}


def figure(nrows: int = 1, ncols: int = 1, figsize=(7.0, 4.0)):
    """Create a figure in the project style; returns ``(fig, axes)``.

    Uses ``matplotlib.figure.Figure`` directly (no pyplot), which marimo
    displays as it is.
    """
    mpl.rcParams.update(STYLE)
    fig = Figure(figsize=figsize, layout="constrained")
    return fig, fig.subplots(nrows, ncols)


def mark_current(ax, x: float, y: float, label: str | None = None) -> None:
    """Mark the current state with the orange marker."""
    ax.plot(
        [x],
        [y],
        "o",
        color=PALETTE["current"],
        markersize=9,
        markeredgecolor="white",
        zorder=5,
        label=label,
    )


def nice_limit(value: float) -> float:
    """Smallest of 1, 2, 5 × 10^k that is ≥ |value| (stable axis limits)."""
    value = abs(value)
    if value == 0:
        return 1.0
    power = 10.0 ** math.floor(math.log10(value))
    return next(s * power for s in (1, 2, 5, 10) if s * power >= value * (1 - 1e-9))
