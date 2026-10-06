---
name: new-applet
description: Create a new teaching applet in apps/<slug>/ following the project template (core + tests + UI + i18n + card). Use whenever the user asks to start, scaffold or build a new applet.
---

# New applet

Follow these steps in order. Do not skip ahead to the UI.

## 0. Agree the content with the user

Before writing code, write (or confirm) the applet card `apps/<slug>/README.md` with:
key message, controls, outputs, assumptions, validation source, optional notes for the teacher.
Ask the user to confirm the card. **Do not proceed until the card is confirmed.**

## 1. Scaffold

Copy `apps/_template/` to `apps/<slug>/` (slug in English `snake_case`). Fill the front matter. `status: draft`.

The template is a minimal skeleton (one slider, one result, placeholder texts in both languages). For a complete example — structure drawing, charts, trace of previous states with `mo.state`, stable axis limits — see `apps/axial_bar`.
- Keep `__init__.py` (lets pytest tell applets apart); tests import with `from .core import ...`.
- Put drawings and charts (matplotlib, via `shared.plotting`) in a `figures.py`, as in `apps/axial_bar`; `app.py` only wires controls to `core` and `figures`.

## 2. Core

Write `core.py`:
- pure functions, internal units N, mm, MPa (see `docs/style.md`), NumPy, type hints, docstrings with equations;
- no marimo, no display strings, no plotting.

## 3. Tests

Write `test_core.py`:
- closed-form / textbook values from the `validation:` source;
- scaling and limit checks (e.g. doubling L divides Pcr by 4);
- boundary conditions of computed shapes.
Run `uv run pytest apps/<slug>`. All tests must pass before step 4.

## 4. Strings (Italian)

Write the `it` section of `strings.py`: introduction, labels, axis labels, result texts, *Why?* text (Markdown + LaTeX). No questions or quizzes. Follow `docs/applet-template.md`.

## 5. UI

Write `app.py` (marimo):
- language from `shared.i18n.get_lang()`;
- the three sections in order (Introduction, Explore, Why?) using `shared.ui`;
- plots via `shared.plotting`, units via `shared.units`, numbers via `shared.units.fmt`;
- at most 5–6 controls visible by default; realistic default values;
- list every runtime package (including those used only by `core.py` or `shared/`) in the PEP 723 `# /// script` block at the top, matching `dependencies:` in the card: the browser installs only what is listed there or imported by `app.py` itself;
- a cell that builds a figure must not end with a matplotlib call that returns an artist (e.g. `ax.set_ylabel(...)`), or marimo displays the figure there too.

## 6. Strings (English)

Translate to `en` using `docs/glossary.md`. Add missing terms to the glossary. Run `test_strings.py`.

## 7. Checks

```bash
uv run pytest apps/<slug>
uv run ruff check apps/<slug> && uv run ruff format apps/<slug>
uv run marimo check apps/<slug>/app.py
uv run python scripts/build_site.py --include-drafts --only <slug>
```

Open the exported page with `?lang=it` and `?lang=en`.

## 8. Hand over

Set `status: review`. Summarise for the user: key message, assumptions, validation results, anything uncertain. Publication (`status: published`) is done only by a human reviewer.
