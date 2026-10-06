# 0001 — marimo notebooks exported to WebAssembly

- **Status:** accepted
- **Date:** 2026-10-05

## Context

Students (mostly architecture and urban planning) must be able to open an interactive applet without installing anything. The university cannot be expected to run a server for the project at the start. Content must be versionable and editable with AI coding agents.

## Decision

Write applets as **marimo** notebooks and publish them as **WebAssembly HTML** (Pyodide) on GitHub Pages.

## Reasons

- Reactive execution: changing a control updates all dependent outputs, with no hidden state.
- Notebooks are plain `.py` files: good for git, tests and coding agents.
- WASM export: computation runs in the student's browser. No server, no account, no cost, unlimited students, no student data leaves the browser (GDPR-friendly).
- Static pages keep working for years.

## Alternatives considered

- **Jupyter + Voilà / JupyterLite:** hidden state, `.ipynb` format less suited to git.
- **Streamlit / Panel on a server:** requires hosting and maintenance.
- **molab only:** free and convenient, but no service guarantee; kept as an option for Tier B (see 0004).
- **GitHub Codespaces:** developer-oriented, too heavy for non-programming students.
- **Hugging Face Spaces:** free CPU tier no longer available to new accounts.

## Consequences

- Only Pyodide-compatible packages can be used in browser applets (see 0004).
- First load takes some seconds (Pyodide download, then cached).
- Internet connection required.
