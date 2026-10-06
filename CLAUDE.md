# CLAUDE.md

Operational rules for working on this repository. Read this file at the start of every session. Detailed rationale lives in `docs/`; this file only states what to do.

## What this project is

Interactive teaching applets (marimo notebooks) about structural behaviour, for students of architecture, urban planning and engineering. Most applets run in the browser via WebAssembly (Pyodide) and are published on GitHub Pages. See `docs/vision.md`.

A human reviewer with structural engineering expertise checks every applet's content before publication. **Physics correctness matters more than features.**

## Repository layout

```
apps/<slug>/app.py          marimo notebook — UI only
apps/<slug>/core.py         computation — pure functions, no UI, no text
apps/<slug>/strings.py      all user-facing text, {"it": {...}, "en": {...}}
apps/<slug>/README.md       applet card with YAML front matter (feeds the gallery)
apps/<slug>/test_*.py       tests for this applet
apps/<slug>/public/         static data files (optional)
apps/_template/             skeleton to copy for a new applet
shared/                     code shared by all applets (i18n, ui, plotting, units)
scripts/build_site.py       WASM export of all published applets + gallery page
docs/                       project documentation and decision records
```

## Hard rules

1. **Separate computation from UI.** `core.py` contains pure functions (inputs → outputs, internal units N, mm, MPa, NumPy). No marimo imports, no strings for display. `app.py` only wires UI elements to `core` functions and lays out outputs.
2. **No hard-coded user-facing text.** Every label, title, explanation and axis label comes from `strings.py` via `shared.i18n`. Code, identifiers and comments are in English.
3. **Both languages, always.** Every key in `strings.py` must exist in `it` and `en`. Italian is the source language; English is a translation. Use `docs/glossary.md` for technical terms; if a term is missing, add it to the glossary in the same change.
4. **Tests before UI.** Write `core.py` and `test_core.py` first. Validate against closed-form solutions or textbook values cited in the applet card (`validation:` field). Do not mark an applet `review` if tests fail.
5. **Tier A applets must be WASM-compatible.** Only use packages available in Pyodide or with pure-Python wheels (numpy, scipy, matplotlib, shapely, structuralcodes, …). Never add OpenSeesPy or other native-only packages to a Tier A applet. See `docs/decisions/0004-tier-a-b.md`.
6. **Follow the applet template.** Every applet has the three sections defined in `docs/applet-template.md` (Introduction, Explore, Why?), in that order. Applets are playgrounds: **no questions, quizzes or grading** (see `docs/decisions/0005-applets-as-playgrounds.md`).
7. **Light backgrounds only.** Plots and UI use light backgrounds and the palette in `docs/style.md`.
8. **Units.** Internally use the consistent system N, mm, MPa (= N/mm²); moments in N·mm, second moments of area in mm⁴. Display: forces in kN, moments in kNm, lengths of structural members (spans, heights, effective lengths) in m, section dimensions in mm, second moments of area in mm⁴, stresses in MPa, elastic moduli in GPa, converting with `shared.units`. Never mix units inside `core.py`. See `docs/style.md`.
9. **Never publish on your own.** You may set `status: draft` or `status: review`. Never set `status: published`: that is done only by a human, after reviewing the content.

## Commands

```bash
uv sync                                         # install dev environment
uv run marimo edit apps/<slug>/app.py           # edit an applet
uv run marimo run apps/<slug>/app.py            # run as app
uv run pytest                                   # all tests
uv run pytest apps/<slug>                       # one applet
uv run ruff check . && uv run ruff format .     # lint and format
uv run marimo check apps/<slug>/app.py          # marimo lint
uv run python scripts/build_site.py             # build the static site into site/
```

Test the language switch with `?lang=en` and `?lang=it` in the browser URL.

## Creating a new applet

Use the `new-applet` skill (`.claude/skills/new-applet/SKILL.md`). Do not start from scratch.

## Personal preferences

This file is shared by everyone who works on the project and must stay generic: no names, accounts or personal preferences. Personal instructions go in your user-level `~/.claude/CLAUDE.md`, which is not part of the repository.

## When in doubt

- About physics or pedagogy: ask the user, do not guess. State assumptions explicitly in the applet's "Why?" section.
- About a technical choice: check `docs/decisions/` first. If a new decision is needed, propose a new decision record.
- Prefer fewer controls and one clear message over many features.
