# 0004 — Tier A (browser) and Tier B (server) applets

- **Status:** accepted
- **Date:** 2026-10-05

## Decision

- **Tier A** applets run in the browser (WASM). They may only use packages available in Pyodide or with pure-Python wheels: numpy, scipy, matplotlib, shapely, structuralcodes (to be confirmed), etc. This is the default.
- **Tier B** applets need native packages (e.g. OpenSeesPy) and therefore a Python server: molab, a local run, or a future university server.

## Guidelines

- Prefer writing the model directly (closed-form or simple numerics) when the concept *is* the model (Euler, Mohr, Hooke, rule of mixtures).
- Use libraries when the concept is the *behaviour* and the computation is only a means (structuralcodes for RC sections, OpenSeesPy for global response).
- For Tier B content used in class, prefer **precomputed results** stored in `public/` and explored by a Tier A applet.
- The tier is declared in the applet card (`tier:`).

## Open points

- Verify that structuralcodes works in Pyodide before planning the RC bending applet as Tier A.
