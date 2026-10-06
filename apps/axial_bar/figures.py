"""Figures of the applet: drawing of the bar and the N–ΔL / σ–ε charts.

Inputs in internal units (N, mm, MPa); ``t`` is the translator from
``shared.i18n``. Computation stays in ``core.py``.
"""

import numpy as np

from shared.plotting import PALETTE, figure, mark_current, nice_limit
from shared.units import fmt, n_to_kn

import core

# The bar is drawn thicker than in reality so that it is visible.
THICKNESS_SCALE = 8.0


def bar_drawing(L, d, N, eps, nu, magnification, t):
    """Undeformed (grey) and deformed (blue) bar, support and load.

    Returns ``(fig, s)`` where ``s`` is the magnification actually used
    (reduced by ``core.drawing_magnification`` for large strains).
    """
    s = core.drawing_magnification(magnification, eps, nu)
    w = THICKNESS_SCALE * d
    L_def, w_def = core.deformed_dimensions(L, w, eps, nu, s)

    fig, ax = figure(figsize=(9.0, 2.6))
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.fill(
        *core.bar_outline(L, w),
        facecolor=PALETTE["undeformed"],
        alpha=0.25,
        edgecolor=PALETTE["undeformed"],
        label=t("explore_undeformed"),
    )
    ax.fill(
        *core.bar_outline(L_def, w_def),
        facecolor=PALETTE["deformed"],
        alpha=0.25,
        edgecolor=PALETTE["deformed"],
        linewidth=2,
        label=t("explore_deformed", factor=fmt(s)),
    )

    # Fixed support at x = 0: wall with hatching.
    h = 0.75 * max(w, w_def) + 0.04 * L
    ax.plot([0, 0], [-h, h], color=PALETTE["reference"], linewidth=2)
    for y in np.linspace(-h, h, 9):
        ax.plot([0, -0.03 * L], [y, y - 0.03 * L], color=PALETTE["reference"], lw=1)

    # Load at the free end, pointing away from the bar in tension.
    a = 0.18 * L
    if N != 0:
        start, end = (L_def, L_def + a) if N > 0 else (L_def + a, L_def)
        ax.annotate(
            "",
            xy=(end, 0),
            xytext=(start, 0),
            arrowprops={"arrowstyle": "-|>", "color": PALETTE["limit"], "lw": 2},
        )
        ax.text(
            L_def + a / 2,
            0.12 * L,
            f"N = {fmt(n_to_kn(N))} kN",
            color=PALETTE["limit"],
            ha="center",
        )

    ax.text(0, -h - 0.02 * L, t("explore_not_to_scale"), fontsize=10, va="top")
    ax.set_xlim(-0.08 * L, 1.5 * L + a)
    ax.set_ylim(-max(h + 0.12 * L, 0.3 * L), max(h, 0.3 * L))
    ax.legend(loc="upper left", ncols=2, bbox_to_anchor=(0.0, 1.12))
    return fig, s


def response_charts(L, E, A, N, trace, n_max, t):
    """N–ΔL (the bar) and σ–ε (the material), with trace and current state.

    Axis limits are the 1-2-5 values reached at ``n_max``, so that a change
    of stiffness shows as a change of slope, not as a rescaled axis.
    """
    trace = np.asarray(trace, dtype=float)
    laws = np.array([-2 * n_max, 2 * n_max])  # beyond the axes on both sides
    fig, (ax_bar, ax_mat) = figure(1, 2, figsize=(9.0, 3.8))

    def panel(ax, xs, ys, x_lim, y_lim, title, xlabel, ylabel):
        """Elastic law, trace and current state; ``xs``/``ys`` map forces."""
        ax.axhline(0, color=PALETTE["undeformed"], linewidth=0.8)
        ax.axvline(0, color=PALETTE["undeformed"], linewidth=0.8)
        ax.plot(
            xs(laws),
            ys(laws),
            "--",
            color=PALETTE["reference"],
            lw=1.2,
            label=t("explore_elastic_law"),
        )
        if len(trace) > 1:
            ax.plot(
                xs(trace),
                ys(trace),
                "o-",
                color=PALETTE["deformed"],
                alpha=0.45,
                lw=1,
                markersize=3.5,
                label=t("explore_trace"),
            )
        mark_current(ax, xs(N), ys(N), label=t("explore_current"))
        ax.set(xlim=(-x_lim, x_lim), ylim=(-y_lim, y_lim))
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)

    def strain_permille(f):
        return 1e3 * core.axial_strain(core.axial_stress(f, A), E)

    s_lim = nice_limit(core.axial_stress(n_max, A))
    panel(
        ax_bar,
        lambda f: core.elongation(f, L, E, A),
        n_to_kn,
        nice_limit(core.elongation(n_max, L, E, A)),
        n_to_kn(n_max),
        t("explore_member_title"),
        t("axis_elongation"),
        t("axis_force"),
    )
    panel(
        ax_mat,
        strain_permille,
        lambda f: core.axial_stress(f, A),
        nice_limit(1e3 * core.axial_strain(s_lim, E)),
        s_lim,
        t("explore_material_title"),
        t("axis_strain"),
        t("axis_stress"),
    )
    ax_bar.legend(loc="upper left")
    return fig
