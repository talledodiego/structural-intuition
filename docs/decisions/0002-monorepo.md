# 0002 — Single repository for all applets

- **Status:** accepted
- **Date:** 2026-10-05

## Decision

All applets live in one repository (`apps/<slug>/`), sharing code in `shared/`, one CI pipeline and one GitHub Pages site with a gallery.

## Reasons

- One link for students, one gallery.
- Consistent look, conventions and i18n across applets through `shared/`.
- One CI/deploy pipeline to maintain.
- Each applet stays self-contained (own `core.py`, tests, strings, card), so it can be extracted later if needed.

## When to split

An applet moves to its own repository only if it becomes a project of its own (e.g. a Tier B tool also used in research, with its own release cycle).
