# Contributing

Thank you for your interest in Structural Intuition. Contributions of new applets, fixes and translations are welcome.

## Before you start

- Read `docs/vision.md` and `docs/applet-template.md`.
- For a new applet, open an issue first describing the concept, the key message and the validation source. This avoids duplicate work.

## Workflow

1. Fork the repository and create a **dedicated branch** from the latest `main` (e.g. `add-mohr-circle`, `fix-euler-units`).
2. Keep each pull request to **one topic**: one new applet, one fix, one translation.
3. Do not include unrelated changes. In particular, do not modify `README.md`, `CLAUDE.md`, `LICENSE` or `LICENSE-CONTENT`, except to add a new applet to the table in `README.md`.
4. Make sure all checks pass locally:
   ```bash
   uv run pytest
   uv run ruff check . && uv run ruff format --check .
   uv run marimo check apps/<slug>/app.py
   ```
5. Open the pull request with a short description: what changes, why, how it was validated.

## Requirements for applets

- Follow the structure in `docs/applet-template.md` (Introduction, Explore, Why?).
- Computation in `core.py`, validated in `test_core.py` against a cited source.
- All user-facing text in `strings.py`, in **both Italian and English**. Use `docs/glossary.md` for technical terms.
- Tier A applets must run in the browser (WASM-compatible packages only).
- New applets are submitted with `status: draft` or `status: review`. Publication is decided after content review.

## AI-assisted contributions

Using coding agents is welcome. The project's `CLAUDE.md` and `.claude/skills/` describe the rules agents must follow. You remain responsible for the correctness of the physics and of the texts you submit.

## Forks for your own course

You are free to fork and adapt the project for your own teaching under the terms of the licences (MIT for code, CC BY 4.0 for content). Keep the copyright notices and credit the original project. Customise your fork as you like; if you later want to contribute back, start a new branch from this repository's `main`.
