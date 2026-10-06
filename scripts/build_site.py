"""Build the static site into site/: WASM export of the applets + gallery.

See docs/deploy.md. Usage:

    uv run python scripts/build_site.py                    # published applets
    uv run python scripts/build_site.py --include-drafts   # also draft/review
    uv run python scripts/build_site.py --include-drafts --only euler_buckling

Only applets with ``status: published`` are built by default. Folders whose
name starts with "_" (the template) are built only when named in --only.
The source-code link in the gallery comes from GITHUB_REPOSITORY (set by
GitHub Actions), so forks link to their own repository.
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shared.strings import STRINGS  # noqa: E402


def read_card(folder: Path) -> dict:
    """The YAML front matter of ``folder/README.md``."""
    text = (folder / "README.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"{folder.name}/README.md: no front matter")
    return yaml.safe_load(match.group(1))


def find_applets(
    apps_dir: Path, include_drafts: bool = False, only: list[str] | None = None
) -> dict[str, dict]:
    """Applets to build, as {folder name: card}."""
    applets = {}
    for folder in sorted(apps_dir.iterdir()):
        if not (folder / "app.py").is_file():
            continue
        if only is not None and folder.name not in only:
            continue
        if only is None and folder.name.startswith("_"):
            continue
        card = read_card(folder)
        if card["status"] == "published" or include_drafts:
            applets[folder.name] = card
    return applets


def export(app: Path, target: Path) -> None:
    """Export one notebook to WASM HTML in ``target``."""
    subprocess.run(
        [
            sys.executable, "-m", "marimo", "export", "html-wasm", str(app),
            "--mode", "run", "--output", str(target), "--force",
            "--no-sandbox",  # use the project environment, do not prompt
        ],
        check=True,
    )  # fmt: skip
    # marimo copies an AI-assistant prompt among its static files: drop it.
    (target / "CLAUDE.md").unlink(missing_ok=True)


def both(key: str) -> str:
    """A shared text in both languages: "italiano / english"."""
    return html.escape(f"{STRINGS['it'][key]} / {STRINGS['en'][key]}")


def thumbnail(slug: str, card: dict) -> str:
    """The card image (``thumbnail:`` in the front matter), if any."""
    if "thumbnail" not in card:
        return ""
    alt = html.escape(f"{card['title']['it']} / {card['title']['en']}")
    return f'<img src="{slug}/{card["thumbnail"]}" alt="{alt}">'


def gallery(applets: dict[str, dict], repository: str | None) -> str:
    """The gallery page: every card shows both languages, links are relative."""
    cards = "".join(
        f"""
  <div class="card">{thumbnail(slug, card)}
    <h2>{html.escape(card["title"]["it"])}</h2>
    <p>{html.escape(card["subtitle"]["it"])}</p>
    <h2 class="en">{html.escape(card["title"]["en"])}</h2>
    <p class="en">{html.escape(card["subtitle"]["en"])}</p>
    <p><a href="{slug}/?lang=it">{STRINGS["it"]["language_name"]}</a> ·
       <a href="{slug}/?lang=en">{STRINGS["en"]["language_name"]}</a></p>
  </div>"""
        for slug, card in applets.items()
    )
    source = (
        f' · <a href="https://github.com/{repository}">{both("gallery_source")}</a>'
        if repository
        else ""
    )
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{STRINGS["it"]["gallery_title"]}</title>
<style>
  body {{ margin: 0 auto; max-width: 960px; padding: 24px 16px; background: #fff;
         color: #202124; font-family: system-ui, sans-serif; line-height: 1.5; }}
  .sub {{ color: #3C4043; margin: 0; }}
  .grid {{ display: grid; gap: 16px; margin: 24px 0;
           grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
  .card {{ padding: 4px 18px; border: 1px solid #ECEFF1;
           border-top: 4px solid #1F5FAD; border-radius: 10px; }}
  .card h2 {{ font-size: 1.15rem; margin: 12px 0 0; color: #1F5FAD; }}
  .card p {{ margin: 4px 0 8px; }}
  .card img {{ display: block; width: 100%; height: 80px; object-fit: contain;
               margin-top: 14px; }}
  .en {{ color: #3C4043; }}
  a {{ color: #1F5FAD; }}
  footer {{ border-top: 1px solid #ECEFF1; padding-top: 12px; color: #3C4043;
            font-size: 0.9rem; }}
</style>
</head>
<body>
<h1>{STRINGS["it"]["gallery_title"]}</h1>
<p class="sub">{html.escape(STRINGS["it"]["gallery_subtitle"])}</p>
<p class="sub">{html.escape(STRINGS["en"]["gallery_subtitle"])}</p>
<div class="grid">{cards}
</div>
<footer>{html.escape(STRINGS["it"]["footer_credits"])}<br>
{html.escape(STRINGS["en"]["footer_credits"])}{source}</footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the static site.")
    parser.add_argument("--include-drafts", action="store_true")
    parser.add_argument("--only", nargs="+", metavar="SLUG")
    args = parser.parse_args()

    out = ROOT / "site"
    if not args.only:
        shutil.rmtree(out, ignore_errors=True)
    out.mkdir(exist_ok=True)

    applets = find_applets(ROOT / "apps", args.include_drafts, args.only)
    for slug in applets:
        print(f"Exporting {slug}", flush=True)
        export(ROOT / "apps" / slug / "app.py", out / slug)

    repository = os.environ.get("GITHUB_REPOSITORY")
    (out / "index.html").write_text(gallery(applets, repository), encoding="utf-8")
    (out / ".nojekyll").touch()
    print(f"Built {len(applets)} applet(s) into {out}")


if __name__ == "__main__":
    main()
