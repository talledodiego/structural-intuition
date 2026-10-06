# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
# The browser installs only the packages listed above (plus those imported
# directly in this file): keep the list in sync with `dependencies:` in
# README.md, including packages used only by core.py, figures.py or shared/
# (e.g. "numpy", "matplotlib" for shared.plotting).
# For a complete example (drawing, charts, trace) see apps/axial_bar.

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from shared import ui
    from shared.i18n import get_lang, translator
    from shared.units import fmt

    import core
    from strings import STRINGS

    lang = get_lang()
    t = translator(STRINGS, lang)
    return core, fmt, lang, mo, t, ui


@app.cell
def _(mo, t, ui):
    # 1. Introduction
    mo.vstack([ui.header(t("title"), t("subtitle")), mo.md(t("intro_text"))])
    return


@app.cell
def _(mo, t):
    x = mo.ui.slider(0, 10, step=0.5, value=5, label=t("label_x"), show_value=True)
    return (x,)


@app.cell
def _(core, fmt, t, ui, x):
    # 2. Explore
    ui.explore(
        controls=[x],
        outputs=[ui.key_result(t("result_x"), fmt(core.example(x.value)), "")],
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
