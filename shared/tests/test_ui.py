import marimo as mo

from shared import ui
from shared.i18n import missing_keys
from shared.strings import STRINGS


def test_shared_strings_in_both_languages():
    assert missing_keys(STRINGS) == []


def test_building_blocks_return_html():
    slider = mo.ui.slider(0, 1)
    assert "Titolo" in ui.header("Titolo", "Sotto").text
    assert "1.43" in ui.key_result("ΔL", "1.43", "mm").text
    assert isinstance(ui.explore([slider], [mo.md("x")]), mo.Html)
    assert isinstance(ui.why_panel("Perché?", "$x$"), mo.Html)


def test_footer_links():
    it = ui.footer("it").text
    assert "../?lang=it" in it and "?lang=en" in it and "Codice" in it
    en = ui.footer("en").text
    assert "../?lang=en" in en and "?lang=it" in en and "Code" in en
