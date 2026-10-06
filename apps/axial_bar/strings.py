"""User-facing text. Italian is the source language; English is a translation.

Keys: English snake_case grouped by prefix (intro_, explore_, why_, axis_,
label_, result_). Texts with values use format fields and must not contain
LaTeX braces; long texts without values may use Markdown + LaTeX.
"""

STRINGS = {
    "it": {
        "title": "Barra soggetta a sforzo normale",
        "subtitle": "Legge di Hooke: la barra e il suo materiale",
        "intro_text": (
            "Tira o comprimi una barra e osserva come si allunga o si accorcia. "
            "Il grafico a sinistra descrive la **barra** (sforzo normale e allungamento), "
            "quello a destra il **materiale** (tensione e deformazione). "
            "Cambia lunghezza e area: il primo cambia, il secondo no."
        ),
        "label_force": "Sforzo normale N [kN]",
        "label_length": "Lunghezza L [m]",
        "label_area": "Area della sezione A [mm²]",
        "label_modulus": "Modulo di elasticità E [GPa]",
        "label_poisson": "Coefficiente di Poisson ν [-]",
        "label_magnification": "Fattore di amplificazione del disegno [-]",
        "label_clear_trace": "Cancella traccia",
        "result_elongation": "Allungamento ΔL",
        "result_details": (
            "σ = {stress} MPa · ε = {strain} ‰ · Δd = {lateral} mm (d = {diameter} mm)"
        ),
        "explore_undeformed": "indeformata",
        "explore_deformed": "deformata (amplificata ×{factor})",
        "explore_not_to_scale": "spessore non in scala",
        "explore_magnification_limited": (
            "Amplificazione ridotta a ×{factor} per mantenere il disegno leggibile."
        ),
        "explore_member_title": "Barra",
        "explore_material_title": "Materiale",
        "explore_elastic_law": "legge elastica",
        "explore_trace": "stati precedenti",
        "explore_current": "stato attuale",
        "axis_elongation": "Allungamento ΔL [mm]",
        "axis_force": "Sforzo normale N [kN]",
        "axis_strain": "Deformazione ε [‰]",
        "axis_stress": "Tensione σ [MPa]",
        "why_title": "Perché?",
        "why_text": r"""
Una barra tirata si allunga, una barra compressa si accorcia. Finché il materiale
resta elastico lineare, l'allungamento è proporzionale alla forza: raddoppiando $N$
raddoppia $\Delta L$.

Il grafico **N–ΔL** descrive la *barra*: la sua pendenza è la rigidezza assiale
$k = EA/L$. Una barra più corta o con area maggiore è più rigida.
Il grafico **σ–ε** descrive il *materiale*: dividendo la forza per l'area e
l'allungamento per la lunghezza si ottiene una retta di pendenza $E$, la stessa
per tutte le barre dello stesso materiale.

$$
\sigma = \frac{N}{A} \qquad \varepsilon = \frac{\Delta L}{L} \qquad
\sigma = E\,\varepsilon \qquad \Delta L = \frac{N L}{E A}
$$

Mentre si allunga, la barra si assottiglia (effetto Poisson):
$\varepsilon_t = -\nu\,\varepsilon$, quindi $\Delta d = \varepsilon_t\,d$.
In compressione, al contrario, la barra si accorcia e si ingrossa.

**Ipotesi.** Materiale elastico lineare e isotropo, senza snervamento né rottura.
Piccoli spostamenti. Tensione uniforme nella sezione: si trascurano gli effetti
locali vicino al vincolo e al punto di applicazione del carico (principio di
de Saint-Venant). In compressione si trascura l'instabilità (barra tozza o
vincolata lateralmente). La sezione è disegnata circolare piena con area $A$;
lo spessore non è in scala.

**Convenzione dei segni.** Trazione positiva.

**Validazione.** Gere & Goodno, *Mechanics of Materials*, cap. 2
(barre soggette a sforzo normale); verifiche con calcolo manuale in `test_core.py`.
""",
    },
    "en": {
        "title": "Axially loaded bar",
        "subtitle": "Hooke's law: the bar and its material",
        "intro_text": (
            "Pull or push a bar and watch it lengthen or shorten. "
            "The chart on the left describes the **bar** (axial force and elongation), "
            "the one on the right the **material** (stress and strain). "
            "Change length and area: the first changes, the second does not."
        ),
        "label_force": "Axial force N [kN]",
        "label_length": "Length L [m]",
        "label_area": "Cross-sectional area A [mm²]",
        "label_modulus": "Young's modulus E [GPa]",
        "label_poisson": "Poisson's ratio ν [-]",
        "label_magnification": "Drawing magnification factor [-]",
        "label_clear_trace": "Clear trace",
        "result_elongation": "Elongation ΔL",
        "result_details": (
            "σ = {stress} MPa · ε = {strain} ‰ · Δd = {lateral} mm (d = {diameter} mm)"
        ),
        "explore_undeformed": "undeformed",
        "explore_deformed": "deformed (amplified ×{factor})",
        "explore_not_to_scale": "thickness not to scale",
        "explore_magnification_limited": (
            "Magnification reduced to ×{factor} to keep the drawing readable."
        ),
        "explore_member_title": "Bar",
        "explore_material_title": "Material",
        "explore_elastic_law": "elastic law",
        "explore_trace": "previous states",
        "explore_current": "current state",
        "axis_elongation": "Elongation ΔL [mm]",
        "axis_force": "Axial force N [kN]",
        "axis_strain": "Strain ε [‰]",
        "axis_stress": "Stress σ [MPa]",
        "why_title": "Why?",
        "why_text": r"""
A bar in tension lengthens, a bar in compression shortens. As long as the
material stays linear elastic, the elongation is proportional to the force:
doubling $N$ doubles $\Delta L$.

The **N–ΔL** chart describes the *bar*: its slope is the axial stiffness
$k = EA/L$. A shorter bar, or one with a larger area, is stiffer.
The **σ–ε** chart describes the *material*: dividing the force by the area and
the elongation by the length gives a straight line of slope $E$, the same for
every bar made of that material.

$$
\sigma = \frac{N}{A} \qquad \varepsilon = \frac{\Delta L}{L} \qquad
\sigma = E\,\varepsilon \qquad \Delta L = \frac{N L}{E A}
$$

As it lengthens, the bar gets thinner (Poisson effect):
$\varepsilon_t = -\nu\,\varepsilon$, hence $\Delta d = \varepsilon_t\,d$.
In compression, conversely, the bar shortens and gets thicker.

**Assumptions.** Linear elastic, isotropic material, with no yielding or failure.
Small displacements. Uniform stress over the section: local effects near the
support and near the point of load application are neglected (Saint-Venant's
principle). Buckling in compression is neglected (stocky or laterally
restrained bar). The section is drawn as a solid circle of area $A$; the
thickness is not to scale.

**Sign convention.** Tension positive.

**Validation.** Gere & Goodno, *Mechanics of Materials*, ch. 2
(axially loaded members); hand-calculation checks in `test_core.py`.
""",
    },
}
