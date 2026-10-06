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

`build_site.py` must not hard-code the owner or the site URL. It derives the base URL from the `GITHUB_REPOSITORY` environment variable (`owner/repo`) in CI, so that a fork publishes to `https://<owner>.github.io/<repo>/` without changes. All links between pages are relative.

### Points to verify with the pilot applet

- `shared/` is outside the applet folder: the export must resolve it (configure the Python path in `pyproject.toml`).
- Reading `?lang=` from the URL works in the WASM export.

## Tier B (needs a Python server)

For applets using native packages (e.g. OpenSeesPy):

- **Preferred for teaching:** precompute results locally and ship them in `public/`; the browser applet explores them (Tier A).
- **Full computation:** "Open in molab" badge linking to the notebook on GitHub, or local run with `uv run marimo run`.

## Moodle

Link to the gallery or to single applets. Use the `?lang=` parameter to choose the language per course.
