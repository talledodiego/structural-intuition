from pathlib import Path

import pytest
from build_site import ROOT, find_applets, gallery, read_card

README = """---
title: {it: "Titolo", en: "Title"}
subtitle: {it: "Sotto", en: "Sub"}
status: STATUS
---
"""
CARD = {"title": {"it": "Titolo", "en": "Title"}, "subtitle": {"it": "S", "en": "S"}}


@pytest.fixture
def apps(tmp_path: Path) -> Path:
    for name, status in {"a": "published", "b": "draft", "_t": "draft"}.items():
        (tmp_path / name).mkdir()
        (tmp_path / name / "README.md").write_text(README.replace("STATUS", status))
        (tmp_path / name / "app.py").write_text("")
    return tmp_path


def test_read_card(apps):
    assert read_card(apps / "a")["title"] == {"it": "Titolo", "en": "Title"}


def test_only_published_by_default(apps):
    assert list(find_applets(apps)) == ["a"]
    assert list(find_applets(apps, include_drafts=True)) == ["a", "b"]


def test_template_only_when_named(apps):
    assert list(find_applets(apps, include_drafts=True, only=["_t"])) == ["_t"]
    assert list(find_applets(apps, only=["_t"])) == []  # a draft is never built


def test_repository_cards_are_valid():
    assert "_template" in find_applets(ROOT / "apps", True, only=["_template"])


@pytest.mark.parametrize("slug", list(find_applets(ROOT / "apps", True)))
def test_every_applet_has_a_thumbnail(slug):
    """Every applet declares a gallery image, and the file exists."""
    card = read_card(ROOT / "apps" / slug)
    assert "thumbnail" in card, f"{slug}/README.md: add `thumbnail:`"
    assert (ROOT / "apps" / slug / card["thumbnail"]).is_file()


def test_gallery_both_languages_relative_links():
    page = gallery({"demo": CARD}, "someone/fork")
    assert 'href="demo/?lang=it"' in page and 'href="demo/?lang=en"' in page
    assert "Titolo" in page and "Title" in page
    assert "https://github.com/someone/fork" in page
    assert "<script" not in page


def test_gallery_without_repository_has_no_source_link():
    assert "github.com" not in gallery({"demo": CARD}, None)


def test_gallery_thumbnail_only_when_declared():
    page = gallery({"demo": {**CARD, "thumbnail": "public/thumbnail.svg"}}, None)
    assert '<img src="demo/public/thumbnail.svg" alt="Titolo / Title">' in page
    assert "<img" not in gallery({"demo": CARD}, None)
