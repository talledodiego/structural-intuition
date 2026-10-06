"""Localisation helpers. See docs/i18n.md.

The language comes from the ``?lang=`` URL parameter: ``it`` (default) or
``en``. Any other value falls back to Italian.
"""

from collections.abc import Callable

LANGS = ("it", "en")
DEFAULT_LANG = "it"


def get_lang() -> str:
    """Read the language from the ``?lang=`` URL parameter of the running app."""
    import marimo as mo

    try:
        lang = mo.query_params().get("lang")
    except Exception:  # not running inside a marimo app (e.g. `python app.py`)
        return DEFAULT_LANG
    return lang if lang in LANGS else DEFAULT_LANG


def other_lang(lang: str) -> str:
    """The other language, for the footer link."""
    return "en" if lang == "it" else "it"


def translator(strings: dict, lang: str) -> Callable[..., str]:
    """Return ``t(key, **values)``, looking ``key`` up in ``strings[lang]``.

    With values the text is filled in with ``str.format``; without values it
    is returned as it is, so texts with LaTeX braces can be used directly.
    """
    table = strings[lang if lang in LANGS else DEFAULT_LANG]

    def t(key: str, **values) -> str:
        return table[key].format(**values) if values else table[key]

    return t


def missing_keys(strings: dict) -> list[str]:
    """Keys missing in one of the languages, as ``"<lang>: <key>"``."""
    all_keys = set().union(*(strings.get(lang, {}) for lang in LANGS))
    return sorted(
        f"{lang}: {key}"
        for lang in LANGS
        for key in all_keys - set(strings.get(lang, {}))
    )
