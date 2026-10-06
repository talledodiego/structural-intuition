"""Figures of the applet: member with supports, cross-section, Pcr–λ chart.

Inputs in internal units (N, mm, MPa); ``t`` is the translator from
``shared.i18n``. Computation stays in ``core.py``.
"""

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle

from shared.plotting import PALETTE, figure, mark_current, nice_limit
from shared.units import fmt, n_to_kn

import core

# The member is drawn with unit height; the buckling mode is amplified to
# this fraction of the height (its true amplitude is undetermined).
MODE_AMPLITUDE = 0.16
MEMBER_WIDTH = 5  # line width of the member [pt], not to scale
LAMBDA_AXIS_MIN = 300.0  # the λ axis extends at least to this value


def explore_figure(
    support,
    state,
    section_kind,
    dims,
    axis,
    lam,
    lam1,
    E,
    A,
    f,
    P,
    P_cr,
    N_pl,
    P_axis,
    t,
):
    """Member (left), cross-section (centre) and Pcr–λ chart (right).

    ``state`` is ``core.member_state``: the buckling mode is drawn only for
    ``"buckling"``, the member is drawn red for ``"crushing"``.
    """
    fig, ax = figure(figsize=(10.0, 4.4))
    ax.remove()
    ax_m, ax_s, ax_c = fig.subplots(1, 3, width_ratios=[1.0, 0.8, 2.6])
    _member(ax_m, support, state, P, t)
    _section(ax_s, section_kind, dims, axis, t)
    _chart(ax_c, lam, lam1, E, A, f, P, P_cr, N_pl, P_axis, t)
    return fig


# --- Member ---------------------------------------------------------------


def _hatched_line(ax, p0, p1, side, n=7, size=0.035):
    """Support surface from p0 to p1, hatched towards ``side`` (unit vector)."""
    (x0, y0), (x1, y1) = p0, p1
    ax.plot([x0, x1], [y0, y1], color=PALETTE["reference"], lw=2)
    sx, sy = side
    for s in np.linspace(0.0, 1.0, n):
        x, y = x0 + s * (x1 - x0), y0 + s * (y1 - y0)
        # Hatches at 45°: along `side`, tilted along the surface.
        tx, ty = (x1 - x0), (y1 - y0)
        norm = np.hypot(tx, ty)
        tx, ty = tx / norm, ty / norm
        ax.plot(
            [x, x + size * (sx - tx)],
            [y, y + size * (sy - ty)],
            color=PALETTE["reference"],
            lw=1,
        )


def _hinge(ax, x, y, r=0.018):
    ax.add_patch(
        Circle(
            (x, y),
            r,
            facecolor="white",
            edgecolor=PALETTE["reference"],
            lw=1.5,
            zorder=6,
        )
    )


def _base(ax, support):
    """Fixed end (hatched ground) or hinge on a triangle."""
    if support == "pinned_pinned":
        h, w = 0.08, 0.06
        ax.add_patch(
            Polygon(
                [(0, 0), (-w, -h), (w, -h)],
                closed=True,
                facecolor="white",
                edgecolor=PALETTE["reference"],
                lw=1.5,
            )
        )
        _hinge(ax, 0, 0)
        _hatched_line(ax, (-1.6 * w, -h), (1.6 * w, -h), (0, -1))
    else:
        _hatched_line(ax, (-0.12, 0), (0.12, 0), (0, -1))


def _top(ax, support, x_top):
    """Top restraint; the top is free to move vertically in every case."""
    wall = 0.26
    if support == "pinned_pinned" or support == "fixed_pinned":
        # Horizontal link (pendulum) to a side wall: restrains sway only.
        ax.plot([0, wall], [1, 1], color=PALETTE["reference"], lw=1.5)
        _hinge(ax, 0, 1)
        _hinge(ax, wall, 1)
        _hatched_line(ax, (wall, 0.92), (wall, 1.08), (1, 0), n=5)
    elif support == "fixed_fixed":
        # Sleeve: restrains sway and rotation, lets the top slide vertically.
        for side in (-1, 1):
            x = side * 0.045
            _hatched_line(ax, (x, 0.86), (x, 1.02), (side, 0), n=5)
    elif support == "fixed_guided":
        # Rigid cap: stays horizontal (rotation restrained), free to sway.
        ax.plot(
            [x_top - 0.08, x_top + 0.08],
            [1, 1],
            color=PALETTE["reference"],
            lw=4,
            solid_capstyle="butt",
        )


def _member(ax, support, state, P, t):
    ax.set_aspect("equal")
    ax.set_axis_off()
    y = np.linspace(0.0, 1.0, 201)
    v = MODE_AMPLITUDE * core.mode_shape(y, 1.0, support)
    if state == "buckling":
        x_top = v[-1]
        ax.plot(
            np.zeros_like(y),
            y,
            "--",
            color=PALETTE["undeformed"],
            lw=2,
            label=t("explore_undeformed"),
        )
        ax.plot(
            v,
            y,
            color=PALETTE["deformed"],
            lw=MEMBER_WIDTH,
            solid_capstyle="butt",
            label=t("explore_mode"),
        )
    else:
        x_top = 0.0
        color = PALETTE["limit"] if state == "crushing" else PALETTE["deformed"]
        label = t("explore_crushing") if state == "crushing" else t("explore_member")
        ax.plot(
            [0, 0],
            [0, 1],
            color=color,
            lw=MEMBER_WIDTH,
            solid_capstyle="butt",
            label=label,
        )
    _base(ax, support)
    _top(ax, support, x_top)

    # Load P at the top, pointing down (compression).
    if P > 0:
        ax.annotate(
            "",
            xy=(x_top, 1.01),
            xytext=(x_top, 1.24),
            arrowprops={"arrowstyle": "-|>", "color": PALETTE["limit"], "lw": 2},
        )
    ax.text(
        x_top + 0.03,
        1.2,
        f"P = {fmt(n_to_kn(P))} kN",
        color=PALETTE["limit"],
        va="center",
    )
    ax.set_xlim(-0.35, 0.4)
    ax.set_ylim(-0.42, 1.3)
    ax.legend(
        loc="lower center", bbox_to_anchor=(0.5, -0.02), fontsize=10, handlelength=1.5
    )


# --- Cross-section --------------------------------------------------------


def _i_outline(h, b, tw, tf):
    """Outline of an I-section centred at the origin (fillets omitted)."""
    x = [
        -b / 2,
        b / 2,
        b / 2,
        tw / 2,
        tw / 2,
        b / 2,
        b / 2,
        -b / 2,
        -b / 2,
        -tw / 2,
        -tw / 2,
        -b / 2,
    ]
    y = [
        -h / 2,
        -h / 2,
        -h / 2 + tf,
        -h / 2 + tf,
        h / 2 - tf,
        h / 2 - tf,
        h / 2,
        h / 2,
        h / 2 - tf,
        h / 2 - tf,
        -h / 2 + tf,
        -h / 2 + tf,
    ]
    return np.column_stack([x, y])


def _section(ax, kind, dims, axis, t):
    """Cross-section with the bending axis (dashed) and the deflection (arrow).

    ``dims``: profile name (``"i"``), ``(b, h)`` (``"rect"``), ``d``
    (``"circ"``), ``(J_y, J_z)`` (``"custom"``). Axis y is horizontal, z
    vertical, as in the tables for I-sections.
    """
    ax.set_aspect("equal")
    ax.set_axis_off()
    style = {
        "facecolor": PALETTE["deformed"],
        "alpha": 0.45,
        "edgecolor": PALETTE["deformed"],
        "lw": 1.5,
    }
    if kind == "i":
        p = core.PROFILES[dims]
        ax.add_patch(Polygon(_i_outline(p.h, p.b, p.tw, p.tf), closed=True, **style))
        w, h = p.b, p.h
        horizontal_is_strong = True
    elif kind == "rect":
        w, h = dims
        ax.add_patch(Rectangle((-w / 2, -h / 2), w, h, **style))
        horizontal_is_strong = h >= w
    elif kind == "circ":
        w = h = dims
        ax.add_patch(Circle((0, 0), dims / 2, **style))
        horizontal_is_strong = True
    else:  # custom: no geometry, a generic dashed outline
        w = h = 100.0
        ax.add_patch(
            Rectangle(
                (-w / 2, -h / 2),
                w,
                h,
                facecolor="white",
                edgecolor=PALETTE["deformed"],
                ls="--",
                lw=1.5,
            )
        )
        horizontal_is_strong = dims[0] >= dims[1]

    s = max(w, h)
    horizontal = (axis == "strong") == horizontal_is_strong
    ext = 0.68 * s
    line = {"color": PALETTE["current"], "ls": "--", "lw": 1.5}
    arrow = {"arrowstyle": "<|-|>", "color": PALETTE["deformed"], "lw": 1.8}
    if horizontal:
        ax.plot([-ext, ext], [0, 0], **line)
        ax.text(ext, 0, " y", color=PALETTE["current"], va="center")
        ax.annotate(
            "", xy=(0.88 * s, 0.35 * s), xytext=(0.88 * s, -0.35 * s), arrowprops=arrow
        )
    else:
        ax.plot([0, 0], [-ext, ext], **line)
        ax.text(0, ext, "z", color=PALETTE["current"], ha="center", va="bottom")
        ax.annotate(
            "",
            xy=(0.35 * s, -0.82 * s),
            xytext=(-0.35 * s, -0.82 * s),
            arrowprops=arrow,
        )
    ax.set_title(t("explore_section_title"), fontsize=11)
    ax.set_xlim(-s, s)
    ax.set_ylim(-1.05 * s, 0.95 * s)


# --- Pcr–λ chart ----------------------------------------------------------


def _chart(ax, lam, lam1, E, A, f, P, P_cr, N_pl, P_axis, t):
    """Euler hyperbola, material limit, capacity and current state (λ, P).

    The load axis ends at ``P_axis`` (``core.load_axis_limit``), so it
    changes only with section and material; the λ axis ends at 300 (more if needed).
    """
    lam_max = max(LAMBDA_AXIS_MIN, nice_limit(1.1 * lam))
    y_max = n_to_kn(P_axis)
    lams = np.linspace(lam_max / 600, lam_max, 600)
    euler = n_to_kn(core.euler_load(lams, E, A))
    n_pl = n_to_kn(N_pl)
    cap = np.minimum(euler, n_pl)

    ax.fill_between(lams, 0, cap, color=PALETTE["safe"], label=t("explore_safe"))
    ax.plot(
        lams, euler, "--", color=PALETTE["reference"], lw=1.2, label=t("explore_euler")
    )
    ax.axhline(n_pl, color=PALETTE["limit"], lw=1.5, label=t("explore_npl"))
    ax.plot(lams, cap, color=PALETTE["deformed"], lw=2.2, label=t("explore_capacity"))
    ax.axvline(lam1, color=PALETTE["undeformed"], ls=":", lw=1.2)
    ax.text(lam1, 0.97 * y_max, " λ₁", color=PALETTE["reference"], va="top")
    ax.text(
        0.5 * lam1,
        0.04 * y_max,
        t("explore_region_material"),
        ha="center",
        fontsize=10,
        color=PALETTE["reference"],
    )
    ax.text(
        0.5 * (lam1 + lam_max),
        0.04 * y_max,
        t("explore_region_buckling"),
        ha="center",
        fontsize=10,
        color=PALETTE["reference"],
    )
    ax.plot(
        [lam],
        [n_to_kn(P_cr)],
        "o",
        markersize=8,
        markerfacecolor="white",
        markeredgecolor=PALETTE["deformed"],
        markeredgewidth=2,
        zorder=5,
        label="Pcr",
    )
    mark_current(ax, lam, n_to_kn(P), label=t("explore_current"))
    ax.set(xlim=(0, lam_max), ylim=(0, y_max))
    ax.set(xlabel=t("axis_slenderness"), ylabel=t("axis_load"))
    ax.legend(loc="upper right", fontsize=9)
