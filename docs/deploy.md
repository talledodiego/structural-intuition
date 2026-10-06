# Deployment

## Tier A (browser, default)

Applets are exported to WebAssembly HTML with marimo and published on GitHub Pages:

```
https://<owner>.github.io/<repo>/                   gallery
https://<owner>.github.io/<repo>/<slug>/            applet (Italian)
https://<owner>.github.io/<repo>/<slug>/?lang=en    applet (English)
```

After the first deployment, set the GitHub Pages URL as the website in the repository's *About* panel: the README links to it from there, so no file contains owner-specific URLs.

### Pipeline

1. Push to `main`.
2. `ci.yml` runs: `ruff`, `pytest`, `marimo check`, WASM compatibility lint.
3. `deploy.yml` runs `scripts/build_site.py`:
   - reads the front matter of every `apps/*/README.md`;
   - exports applets with `status: published` using `marimo export html-wasm --mode run`;
   - generates the gallery page;
   - publishes `site/` to GitHub Pages.

Applets in `draft` or `review` can be built locally (`--include-drafts`) but are never published.

### Forks

`build_site.py` does not hard-code the owner or the site URL. All links between pages are relative, so a fork publishes to `https://<owner>.github.io/<repo>/` without changes; the only absolute link, to the source code in the gallery, comes from the `GITHUB_REPOSITORY` environment variable (`owner/repo`) set by GitHub Actions.

### How the export works (verified with `apps/_template` and `apps/axial_bar`, marimo 0.25)

- **Local modules.** `[tool.marimo.runtime] pythonpath = ["."]` in `pyproject.toml` makes `shared/` importable in `marimo edit/run`. `marimo export html-wasm` also uses it: it finds the local modules the notebook imports (`shared`, `core`, `figures`, `strings`), packs them as wheels into `<slug>/public/wheels/` and installs them in the browser.
- **Third-party packages.** In the browser, marimo installs only the packages imported *by the notebook itself*, not those imported by `shared/` or `core.py`. Every `app.py` therefore declares its runtime packages in a PEP 723 `# /// script` block (same list as `dependencies:` in the card). `build_site.py` exports with `--no-sandbox`, using the project environment; for the same reason, run `marimo run/edit` locally with `--no-sandbox` (otherwise marimo asks whether to create a separate environment).
- **Language.** `?lang=` is read by `mo.query_params()` in the browser as well; the footer link switches language by reloading with the other parameter.
- **Display settings** (`[tool.marimo.display]` in `pyproject.toml`) are embedded in the export: `theme = "light"` (light backgrounds even on dark-mode systems) and `locale = "it-CH"`, so widget numbers use a dot as decimal separator in both languages (`0.3`, `1000`, `12'345`).
- **Credits and source link.** The applet footer shows the copyright and licences from `shared/strings.py` (forks must keep the original copyright notice anyway). The source-code link is only in the gallery, built from `GITHUB_REPOSITORY`, so a fork links to its own repository.
- marimo copies an AI-assistant prompt (`CLAUDE.md`) among its static assets; `build_site.py` deletes it from each export.

## Tier B (needs a Python server)

For applets using native packages (e.g. OpenSeesPy):

- **Preferred for teaching:** precompute results locally and ship them in `public/`; the browser applet explores them (Tier A).
- **Full computation:** "Open in molab" badge linking to the notebook on GitHub, or local run with `uv run marimo run`.

## Moodle

Link to the gallery or to single applets. Use the `?lang=` parameter to choose the language per course.
