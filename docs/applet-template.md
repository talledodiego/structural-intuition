# Applet template

Every applet follows the same structure and the same UI conventions, so that students who have used one applet immediately know how to use the next.

Applets are **pure playgrounds**: no questions, no quizzes, no grading. Predictions and guided questions are handled by the teacher in class (slides, AhaSlides). At home, students open the applet and explore freely. See `docs/decisions/0005-applets-as-playgrounds.md`.

## The three sections

Sections appear in this order, from top to bottom.

### 1. Introduction
Title, one-line subtitle and two or three sentences on what the applet shows. No equations here.

### 2. Explore
The interactive core: controls on the left (or top on narrow screens), outputs on the right.

- **At most 5–6 controls** visible by default. Additional ones go in a collapsible "More parameters" panel.
- Every output updates live. No "Run" button unless a computation takes more than ~1 s.
- At least one output is a **picture of the structure** (deformed shape, section, stress state), not only a chart.
- Show the current value of the key result in large text (e.g. "Pcr = 245 kN").
- Default values represent a realistic, recognisable case (e.g. a 3 m steel column, not L = 1).

### 3. Why?
The theory behind what the student sees, in a collapsible panel (closed by default).

- Start with the physical explanation in words, then the equations.
- Declare all assumptions and simplifications explicitly.
- Cite the validation source (book, code clause).
- Keep it under one screen. Link to course material for more.

## Layout conventions

- Language is read from the URL (`?lang=it` default, `?lang=en`). No visible language switch is required, but a small link to the other language is shown in the footer.
- Header: applet title and one-line subtitle.
- Footer: link to the gallery, link to the other language, copyright and licences (one text in `shared/strings.py`, the same for all applets). The link to the source code is in the gallery.
- All texts come from `strings.py` (see `docs/i18n.md`).
- Plots follow `docs/style.md`.

## Applet card (`README.md` front matter)

```yaml
---
slug: euler_buckling
title: {it: "Instabilità euleriana", en: "Euler buckling"}
subtitle: {it: "...", en: "..."}
courses: [lab2, disaster]          # courses where it is used
level: base                        # base | intermediate | advanced
tier: A                            # A = runs in browser, B = needs a Python server
dependencies: [numpy, matplotlib]
validation: "Timoshenko & Gere, Theory of Elastic Stability, ch. 2"
status: draft                      # draft | review | published
thumbnail: public/thumbnail.svg    # required: small image on the gallery card
---
```

Every applet has a `thumbnail`: without it, its card looks empty next to the others in the gallery. A test (`scripts/test_build_site.py`) fails if it is missing. The thumbnail is an image in the applet's `public/` folder (SVG preferred, about 4:1, white background). It is shown in both languages, so it contains **no text**. It is typically a small drawing of the structure, in the palette of `docs/style.md`: draw it with matplotlib (`shared.plotting.figure(figsize=(4.0, 0.8))`), reusing the drawing helpers of the applet's `figures.py`, and save it as SVG. Check it in the gallery next to the other cards.

Below the front matter: a short description, the key message, controls and outputs, the list of assumptions, validation, and optional **notes for the teacher** (e.g. suggested in-class questions). These notes are for the teacher only and never appear in the applet.
