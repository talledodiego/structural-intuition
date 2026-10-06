"""User-facing text. Italian is the source language; English is a translation.

Keys: English snake_case grouped by prefix (intro_, explore_, why_, axis_,
label_, result_). Placeholders: replace them, keeping both languages.
"""

STRINGS = {
    "it": {
        "title": "Titolo dell'applet",
        "subtitle": "Sottotitolo di una riga",
        "intro_text": "Due o tre frasi su cosa mostra l'applet. Nessuna equazione qui.",
        "label_x": "Parametro x [unità]",
        "result_x": "Valore di x",
        "why_title": "Perché?",
        "why_text": r"""
Spiegazione fisica a parole, poi le equazioni, ad esempio $y = x$.

**Ipotesi.** Elenco delle ipotesi e semplificazioni.

**Convenzione dei segni.** Da dichiarare.

**Validazione.** Fonte usata per validare `core.py` (libro e capitolo, oppure norma e punto).
""",
    },
    "en": {
        "title": "Applet title",
        "subtitle": "One-line subtitle",
        "intro_text": "Two or three sentences on what the applet shows. No equations here.",
        "label_x": "Parameter x [unit]",
        "result_x": "Value of x",
        "why_title": "Why?",
        "why_text": r"""
Physical explanation in words, then the equations, for example $y = x$.

**Assumptions.** List of assumptions and simplifications.

**Sign convention.** To be stated.

**Validation.** Source used to validate `core.py` (book and chapter, or standard and clause).
""",
    },
}
