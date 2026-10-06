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
    from shared.units import fmt, gpa_to_mpa, kn_to_n, m_to_mm

    import core
    import figures
    from strings import STRINGS

    lang = get_lang()
    t = translator(STRINGS, lang)
    return core, figures, fmt, gpa_to_mpa, kn_to_n, lang, m_to_mm, mo, t, ui


@app.cell
def _(mo, t, ui):
    # 1. Introduction
    mo.vstack([ui.header(t("title"), t("subtitle")), mo.md(t("intro_text"))])
    return


@app.cell
def _(mo):
    # Forces applied so far, for the trace; reset when L, E or A change.
    get_trace, set_trace = mo.state({"member": None, "forces": []})
    return get_trace, set_trace


@app.cell
def _(mo, set_trace, t):
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

    # Ranges and defaults: see README.md ("What the student can do").
    N_MAX_KN = 50
    force = slider(-N_MAX_KN, N_MAX_KN, 1, 10, "label_force")
    length = slider(0.5, 6.0, 0.1, 1.0, "label_length")
    area = slider(50, 1000, 10, 200, "label_area")
    modulus = slider(10, 250, 5, 210, "label_modulus")
    poisson = slider(0.0, 0.5, 0.01, 0.3, "label_poisson")
    magnification = mo.ui.slider(
        steps=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000],
        value=1,
        label=t("label_magnification"),
        show_value=True,
        full_width=True,
    )
    clear_trace = mo.ui.button(
        label=t("label_clear_trace"),
        on_click=lambda _: set_trace(lambda tr: {**tr, "forces": []}),
    )
    return N_MAX_KN, area, clear_trace, force, length, magnification, modulus, poisson


@app.cell
def _(area, core, force, gpa_to_mpa, kn_to_n, length, m_to_mm, modulus, poisson):
    # Display units -> internal units (N, mm, MPa), then the computation.
    N = kn_to_n(force.value)
    L = m_to_mm(length.value)
    A = float(area.value)
    E = gpa_to_mpa(modulus.value)
    nu = poisson.value

    sigma = core.axial_stress(N, A)
    eps = core.axial_strain(sigma, E)
    dL = core.elongation(N, L, E, A)
    d = core.equivalent_diameter(A)
    dd = core.lateral_strain(eps, nu) * d
    return A, E, L, N, d, dL, dd, eps, nu, sigma


@app.cell
def _(A, E, L, N, set_trace):
    # Add the current force to the trace; a new member (L, E, A) starts over.
    def _add(trace):
        if trace["member"] != (L, E, A):
            return {"member": (L, E, A), "forces": [N]}
        if trace["forces"][-1:] == [N]:
            return trace
        return {"member": (L, E, A), "forces": [*trace["forces"], N][-500:]}

    set_trace(_add)
    return


@app.cell
def _(
    A,
    E,
    L,
    N,
    N_MAX_KN,
    area,
    clear_trace,
    d,
    dL,
    dd,
    eps,
    figures,
    fmt,
    force,
    get_trace,
    kn_to_n,
    length,
    magnification,
    mo,
    modulus,
    nu,
    poisson,
    sigma,
    t,
    ui,
):
    # 2. Explore
    _trace = get_trace()
    _forces = _trace["forces"] if _trace["member"] == (L, E, A) else []
    _drawing, _s = figures.bar_drawing(L, d, N, eps, nu, magnification.value, t)
    _details = t(
        "result_details",
        stress=fmt(sigma),
        strain=fmt(1e3 * eps),
        lateral=fmt(dd),
        diameter=fmt(d),
    )
    if _s < magnification.value:
        _details += "  \n" + t("explore_magnification_limited", factor=fmt(_s))

    ui.explore(
        controls=[force, length, area, modulus, poisson, magnification, clear_trace],
        outputs=[
            ui.key_result(t("result_elongation"), fmt(dL), "mm"),
            mo.md(_details),
            _drawing,
            figures.response_charts(L, E, A, N, _forces, kn_to_n(N_MAX_KN), t),
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
