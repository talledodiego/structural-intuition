"""UI building blocks for the layout in docs/applet-template.md.

Each applet shows: ``header`` → introduction → ``explore`` → ``why_panel``
→ ``footer``. Texts are passed in already translated.
"""

import marimo as mo

from shared.i18n import other_lang, translator
from shared.strings import STRINGS
from shared.style import PALETTE


def header(title: str, subtitle: str) -> mo.Html:
    """Applet title and one-line subtitle."""
    return mo.md(f"# {title}\n\n<span style='font-size:1.15em'>{subtitle}</span>")


def key_result(label: str, value: str, unit: str) -> mo.Html:
    """The key result in large text, e.g. "Pcr = 245 kN"."""
    return mo.Html(
        f"<div style='color:{PALETTE['reference']}'>{label}</div>"
        f"<div style='font-size:2.2em;font-weight:600;color:{PALETTE['deformed']}'>"
        f"{value} <span style='font-size:0.6em'>{unit}</span></div>"
    )


def explore(controls: list, outputs: list) -> mo.Html:
    """Controls on the left, outputs on the right (stacked on narrow screens)."""
    return mo.hstack(
        [mo.vstack(controls), mo.vstack(outputs, gap=1)],
        widths=[1, 3],
        gap=2,
        align="start",
        wrap=True,
    )


def why_panel(title: str, text: str) -> mo.Html:
    """The *Why?* section (Markdown + LaTeX), collapsed by default."""
    return mo.accordion({title: mo.md(text)})


def footer(lang: str) -> mo.Html:
    """Links to the gallery and to the other language; credits."""
    t = translator(STRINGS, lang)
    return mo.md(
        "---\n"
        f"[{t('footer_gallery')}](../?lang={lang}) · "
        f"[{t('footer_other_lang')}](?lang={other_lang(lang)})  \n"
        f"{t('footer_credits')}"
    )
