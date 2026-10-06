# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
# ]
# ///
# The browser installs only the packages listed above (plus those imported
# directly in this file): keep the list in sync with `dependencies:` in
# README.md, including packages used only by core.py, figures.py or shared/.

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from shared import ui
    from shared.i18n import get_lang, translator
    from shared.units import fmt, kn_to_n, m_to_mm, mm_to_m, n_to_kn

    import core
    import figures
    from strings import STRINGS

    lang = get_lang()
    t = translator(STRINGS, lang)
    return core, figures, fmt, kn_to_n, lang, m_to_mm, mm_to_m, mo, n_to_kn, t, ui


@app.cell
def _(mo, t, ui):
    # 1. Introduction
    mo.vstack([ui.header(t("title"), t("subtitle")), mo.md(t("intro_text"))])
    return


@app.cell
def _(mo):
    # Load P [kN], kept when the load slider is rebuilt with a new range.
    get_load, set_load = mo.state(560.0)
    return get_load, set_load


@app.cell
def _(core, mo, t):
    # Ranges and defaults: see README.md ("What the student can do").
    def options(prefix, keys):
        return {t(f"{prefix}_{k}"): k for k in keys}

    def dropdown(prefix, keys, value, key):
        return mo.ui.dropdown(
            options=options(prefix, keys),
            value=t(f"{prefix}_{value}"),
            label=t(key),
            full_width=True,
        )

    def slider(start, stop, step, value, key):
        return mo.ui.slider(
            start,
            stop,
            step=step,
            value=value,
            label=t(key),
            show_value=True,
            full_width=True,
        )

    def number(start, stop, step, value, key):
        return mo.ui.number(
            start=start, stop=stop, step=step, value=value, label=t(key)
        )

    support = dropdown("support", core.SUPPORTS, "pinned_pinned", "label_support")
    length = slider(1.0, 12.0, 0.1, 3.0, "label_length")
    section_kind = dropdown(
        "section", ["i", "rect", "circ", "custom"], "i", "label_section"
    )
    profile = mo.ui.dropdown(
        options=list(core.PROFILES),
        value="HEA120",
        label=t("label_profile"),
        full_width=True,
    )
    width = slider(20, 600, 10, 100, "label_b")
    depth = slider(20, 600, 10, 160, "label_h")
    diameter = slider(20, 600, 5, 60, "label_d")
    custom_area = number(100, 100_000, 100, 5_000, "label_custom_area")
    custom_jy = number(1e4, 1e10, 1e5, 5e7, "label_custom_jy")
    custom_jz = number(1e4, 1e10, 1e5, 1e7, "label_custom_jz")
    axis = mo.ui.radio(
        options=options("axis", ["weak", "strong"]),
        value=t("axis_weak"),
        label=t("label_axis"),
        inline=True,
    )
    material = dropdown("material", list(core.MATERIALS), "steel", "label_material")
    return (
        axis,
        custom_area,
        custom_jy,
        custom_jz,
        depth,
        diameter,
        length,
        material,
        profile,
        section_kind,
        support,
        width,
    )


@app.cell
def _(
    core,
    custom_area,
    custom_jy,
    custom_jz,
    depth,
    diameter,
    material,
    profile,
    section_kind,
    width,
):
    # Section and material (internal units). Independent of L and supports,
    # so that the load slider is rebuilt only when these change.
    kind = section_kind.value
    if kind == "i":
        dims = profile.value
        section = core.profile_section(dims)
    elif kind == "rect":
        dims = (float(width.value), float(depth.value))
        section = core.rectangular_section(*dims)
    elif kind == "circ":
        dims = float(diameter.value)
        section = core.circular_section(dims)
    else:
        dims = (float(custom_jy.value), float(custom_jz.value))
        section = core.custom_section(float(custom_area.value), *dims)
    mat = core.MATERIALS["steel" if kind == "i" else material.value]
    N_pl = core.squash_load(section.A, mat.f)
    P_axis = core.load_axis_limit(N_pl)
    P_steps = core.load_steps(N_pl)
    return N_pl, P_axis, P_steps, dims, kind, mat, section


@app.cell
def _(P_steps, core, get_load, kn_to_n, mo, n_to_kn, set_load, t):
    # The slider ends at Npl: an ideal member cannot carry more.
    _value = core.snap_load(kn_to_n(get_load()), P_steps)
    load = mo.ui.slider(
        steps=[round(n_to_kn(p), 6) for p in P_steps],
        value=round(n_to_kn(_value), 6),
        label=t("label_load"),
        show_value=True,
        full_width=True,
        on_change=set_load,
    )
    return (load,)


@app.cell
def _(N_pl, axis, core, kn_to_n, length, load, m_to_mm, mat, section, support):
    # Display units -> internal units (N, mm, MPa), then the computation.
    P = kn_to_n(load.value)
    L = m_to_mm(length.value)
    J = section.J_weak if axis.value == "weak" else section.J_strong
    L0 = core.effective_length(L, support.value)
    P_cr = core.critical_load(mat.E, J, L0)
    i = core.radius_of_gyration(J, section.A)
    lam = core.slenderness(L0, i)
    lam1 = core.transition_slenderness(mat.E, mat.f)
    state = core.member_state(P, P_cr, N_pl)
    ratio = P / core.capacity(P_cr, N_pl)
    return L0, P, P_cr, i, lam, lam1, ratio, state


@app.cell
def _(
    L0,
    N_pl,
    P,
    P_cr,
    P_axis,
    axis,
    custom_area,
    custom_jy,
    custom_jz,
    depth,
    diameter,
    dims,
    figures,
    fmt,
    i,
    kind,
    lam,
    lam1,
    length,
    load,
    mat,
    material,
    mm_to_m,
    mo,
    n_to_kn,
    profile,
    ratio,
    section,
    section_kind,
    state,
    support,
    t,
    ui,
    width,
):
    # 2. Explore: the controls shown depend on the section type.
    _size = {
        "i": [profile],
        "rect": [width, depth],
        "circ": [diameter],
        "custom": [custom_area, custom_jy, custom_jz],
    }[kind]
    _axis = [] if kind == "circ" else [axis]
    _material = [mo.md(t("explore_steel_only"))] if kind == "i" else [material]
    _controls = [load, support, length, section_kind, *_size, *_axis, *_material]

    _details = t(
        "result_details",
        npl=fmt(n_to_kn(N_pl)),
        lam=fmt(lam),
        lam1=fmt(lam1),
        i=fmt(i),
        l0=fmt(mm_to_m(L0)),
        ratio=fmt(ratio),
    )
    _callout = {"ok": "success", "buckling": "danger", "crushing": "danger"}[state]
    _figure = figures.explore_figure(
        support.value,
        state,
        kind,
        dims,
        axis.value,
        lam,
        lam1,
        mat.E,
        section.A,
        mat.f,
        P,
        P_cr,
        N_pl,
        P_axis,
        t,
    )
    ui.explore(
        controls=_controls,
        outputs=[
            ui.key_result(t("result_pcr"), fmt(n_to_kn(P_cr)), "kN"),
            mo.md(_details),
            mo.callout(mo.md(t(f"state_{state}")), kind=_callout),
            _figure,
        ],
    )
    return


@app.cell
def _(t, ui):
    # 3. Why?
    ui.why_panel(t("why_title"), t("why_text"))
    return


@app.cell
def _(lang, ui):
    ui.footer(lang)
    return


if __name__ == "__main__":
    app.run()
