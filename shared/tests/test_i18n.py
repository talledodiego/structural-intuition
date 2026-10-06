import marimo
import pytest

from shared.i18n import get_lang, missing_keys, other_lang, translator

STRINGS = {
    "it": {"title": "Titolo", "result": "P = {value} kN", "why": r"$\frac{a}{b}$"},
    "en": {"title": "Title", "result": "P = {value} kN", "why": r"$\frac{a}{b}$"},
}


@pytest.mark.parametrize(
    ("param", "expected"),
    [
        ({"lang": "en"}, "en"),
        ({"lang": "it"}, "it"),
        ({"lang": "fr"}, "it"),
        ({}, "it"),
    ],
)
def test_get_lang(monkeypatch, param, expected):
    monkeypatch.setattr(marimo, "query_params", lambda: param)
    assert get_lang() == expected


def test_get_lang_outside_app_is_italian():
    assert get_lang() == "it"


def test_other_lang():
    assert other_lang("it") == "en"
    assert other_lang("en") == "it"


def test_translator():
    t = translator(STRINGS, "en")
    assert t("title") == "Title"
    assert t("result", value="245") == "P = 245 kN"
    assert t("why") == r"$\frac{a}{b}$"  # no values: braces left alone
    assert translator(STRINGS, "de")("title") == "Titolo"


def test_missing_keys():
    assert missing_keys(STRINGS) == []
    assert missing_keys({"it": {"a": "x", "b": "y"}, "en": {"a": "x"}}) == ["en: b"]
