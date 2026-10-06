"""User-facing text. Italian is the source language; English is a translation.

Keys: English snake_case grouped by prefix (intro_, explore_, why_, axis_,
label_, result_). Texts with values use format fields and must not contain
LaTeX braces; long texts without values may use Markdown + LaTeX.
"""

STRINGS = {
    "it": {
        "title": "Instabilità euleriana",
        "subtitle": "Perché la snellezza conta più della resistenza",
        "intro_text": (
            "Comprimi un'asta e osserva come cede: può **inflettersi lateralmente** "
            "(instabilità) oppure **schiacciarsi** perché il materiale raggiunge la "
            "sua resistenza. Cambia lunghezza, vincoli e sezione: per un'asta snella "
            "conta la rigidezza, non la resistenza del materiale."
        ),
        "label_load": "Carico assiale P [kN]",
        "label_support": "Vincoli (base – sommità)",
        "support_pinned_pinned": "cerniera – cerniera (β = 1)",
        "support_fixed_free": "incastro – libero (β = 2)",
        "support_fixed_pinned": "incastro – cerniera (β = 0.7)",
        "support_fixed_fixed": "incastro – incastro (β = 0.5)",
        "support_fixed_guided": "incastro – pattino (β = 1)",
        "label_length": "Lunghezza L [m]",
        "label_section": "Sezione",
        "section_i": "profilo laminato a I",
        "section_rect": "rettangolare",
        "section_circ": "circolare",
        "section_custom": "personalizzata",
        "label_profile": "Profilo",
        "label_b": "Base b [mm]",
        "label_h": "Altezza h [mm]",
        "label_d": "Diametro d [mm]",
        "label_custom_area": "Area A [mm²]",
        "label_custom_jy": "J_y, asse forte [mm⁴]",
        "label_custom_jz": "J_z, asse debole [mm⁴]",
        "label_axis": "Asse di inflessione",
        "axis_weak": "debole",
        "axis_strong": "forte",
        "label_material": "Materiale",
        "material_steel": "acciaio S235",
        "material_timber": "legno C24",
        "material_concrete": "calcestruzzo C25/30",
        "explore_steel_only": "Materiale: acciaio S235 (profili laminati).",
        "result_pcr": "Carico critico Pcr",
        "result_details": (
            "Npl = A·f = {npl} kN · λ = L₀/i = {lam} (λ₁ = {lam1}) · "
            "i = {i} mm · L₀ = β·L = {l0} m · P / min(Pcr, Npl) = {ratio}"
        ),
        "state_ok": "**L'asta regge**: P è minore sia di Pcr sia di Npl.",
        "state_buckling": (
            "**Instabilità**: P ≥ Pcr. L'asta si inflette lateralmente prima che "
            "il materiale raggiunga la sua resistenza."
        ),
        "state_crushing": (
            "**Resistenza del materiale raggiunta**: P ≥ Npl. L'asta è abbastanza "
            "tozza da arrivare allo schiacciamento (snervamento per l'acciaio) "
            "prima di instabilizzarsi."
        ),
        "explore_undeformed": "indeformata",
        "explore_mode": "modo critico (amplificato)",
        "explore_member": "asta",
        "explore_crushing": "resistenza raggiunta",
        "explore_section_title": "Sezione",
        "explore_safe": "l'asta regge",
        "explore_euler": "iperbole di Eulero",
        "explore_npl": "limite del materiale Npl",
        "explore_capacity": "min(Pcr, Npl)",
        "explore_current": "carico P",
        "explore_region_material": "governa il materiale",
        "explore_region_buckling": "governa l'instabilità",
        "axis_slenderness": "Snellezza λ [-]",
        "axis_load": "Carico assiale [kN]",
        "why_title": "Perché?",
        "why_text": r"""
Un'asta compressa perfettamente dritta resta dritta finché il carico è piccolo.
Se però la si sposta un poco di lato, il carico $P$, agendo sull'asta inflessa,
produce un momento $P\,v$ che tende ad aumentare l'inflessione, mentre la
rigidezza a flessione $EJ$ tende a raddrizzarla. Il **carico critico** $P_{cr}$
è il carico per cui le due azioni si equilibrano: oltre $P_{cr}$ l'asta non
torna più dritta e si inflette lateralmente (Eulero, 1744).

$$
EJ\,v'''' + P\,v'' = 0
\qquad\Rightarrow\qquad
P_{cr} = \frac{\pi^2 E J}{L_0^2}, \qquad L_0 = \beta L
$$

La **lunghezza libera di inflessione** $L_0$ è la distanza tra due punti di
flesso consecutivi del modo critico (eventualmente prolungato oltre l'asta,
come per la mensola): dipende dai vincoli tramite il coefficiente $\beta$
(1 cerniera–cerniera, 2 mensola, 0.7 incastro–cerniera, 0.5 incastro–incastro,
1 incastro–pattino). Raddoppiando $L$, $P_{cr}$ diventa **un quarto**.

$P_{cr}$ dipende da $E$ e $J$, ma **non dalla resistenza** del materiale.
La resistenza dà un secondo limite, $N_{pl} = A\,f$. Dividendo per $A$ e
introducendo il raggio d'inerzia $i = \sqrt{J/A}$ e la **snellezza**
$\lambda = L_0/i$:

$$
\frac{P_{cr}}{A} = \frac{\pi^2 E}{\lambda^2}
\qquad\text{uguale a } f \text{ per}\qquad
\lambda_1 = \pi\sqrt{\frac{E}{f}}
$$

Per $\lambda > \lambda_1$ governa l'instabilità, per $\lambda < \lambda_1$
il materiale. L'asta si inflette attorno all'asse con $J$ minore (asse debole),
a meno che non sia vincolata in quella direzione.

| Materiale | $E$ | $f$ | $\lambda_1$ |
|---|---|---|---|
| Acciaio S235 | 210 GPa | 235 MPa | 93.9 |
| Legno C24 | 11 GPa | 21 MPa | 71.9 |
| Calcestruzzo C25/30 | 31 GPa | 25 MPa | 110.6 |

**Ipotesi.** Asta ideale di Eulero: materiale elastico lineare, asse
perfettamente rettilineo, carico centrato. Nessuna imperfezione e nessuna
tensione residua: per questo, vicino a $\lambda_1$, la capacità reale è
molto minore di $\min(P_{cr}, N_{pl})$ (curve di instabilità dell'EC3 e
dell'EC5, non trattate qui). Piccoli spostamenti: l'ampiezza del modo critico
è indeterminata ed è disegnata amplificata. Valori indicativi di $E$ e di
$f$, senza coefficienti di sicurezza: servono a confrontare i materiali, non
a verificare l'asta secondo le norme (per il calcestruzzo, sezione non
armata). Le proprietà dei profili laminati (raccordi inclusi) sono quelle
dei sagomari ArcelorMittal.

**Convenzione dei segni.** Compressione positiva.

**Validazione.** Timoshenko & Gere, *Theory of Elastic Stability*, cap. 2;
EN 1993-1-1 §6.3.1 per la definizione di snellezza; verifiche con calcolo
manuale in `test_core.py`.
""",
    },
    "en": {
        "title": "Euler buckling",
        "subtitle": "Why slenderness matters more than strength",
        "intro_text": (
            "Compress a member and watch how it fails: it can **bend sideways** "
            "(buckling) or be **crushed** because the material reaches its "
            "strength. Change length, supports and cross-section: for a slender "
            "member stiffness matters, not the strength of the material."
        ),
        "label_load": "Axial load P [kN]",
        "label_support": "Supports (base – top)",
        "support_pinned_pinned": "pinned – pinned (β = 1)",
        "support_fixed_free": "fixed – free (β = 2)",
        "support_fixed_pinned": "fixed – pinned (β = 0.7)",
        "support_fixed_fixed": "fixed – fixed (β = 0.5)",
        "support_fixed_guided": "fixed – guided (β = 1)",
        "label_length": "Length L [m]",
        "label_section": "Cross-section",
        "section_i": "rolled I-section",
        "section_rect": "rectangular",
        "section_circ": "circular",
        "section_custom": "custom",
        "label_profile": "Section",
        "label_b": "Width b [mm]",
        "label_h": "Depth h [mm]",
        "label_d": "Diameter d [mm]",
        "label_custom_area": "Area A [mm²]",
        "label_custom_jy": "J_y, strong axis [mm⁴]",
        "label_custom_jz": "J_z, weak axis [mm⁴]",
        "label_axis": "Bending axis",
        "axis_weak": "weak",
        "axis_strong": "strong",
        "label_material": "Material",
        "material_steel": "steel S235",
        "material_timber": "timber C24",
        "material_concrete": "concrete C25/30",
        "explore_steel_only": "Material: steel S235 (rolled sections).",
        "result_pcr": "Critical load Pcr",
        "result_details": (
            "Npl = A·f = {npl} kN · λ = L₀/i = {lam} (λ₁ = {lam1}) · "
            "i = {i} mm · L₀ = β·L = {l0} m · P / min(Pcr, Npl) = {ratio}"
        ),
        "state_ok": "**The member holds**: P is below both Pcr and Npl.",
        "state_buckling": (
            "**Buckling**: P ≥ Pcr. The member bends sideways before the "
            "material reaches its strength."
        ),
        "state_crushing": (
            "**Material strength reached**: P ≥ Npl. The member is stocky "
            "enough to be crushed (to yield, for steel) before it buckles."
        ),
        "explore_undeformed": "undeformed",
        "explore_mode": "buckling mode (amplified)",
        "explore_member": "member",
        "explore_crushing": "strength reached",
        "explore_section_title": "Cross-section",
        "explore_safe": "the member holds",
        "explore_euler": "Euler hyperbola",
        "explore_npl": "material limit Npl",
        "explore_capacity": "min(Pcr, Npl)",
        "explore_current": "load P",
        "explore_region_material": "material governs",
        "explore_region_buckling": "buckling governs",
        "axis_slenderness": "Slenderness λ [-]",
        "axis_load": "Axial load [kN]",
        "why_title": "Why?",
        "why_text": r"""
A perfectly straight compressed member stays straight while the load is small.
If it is pushed slightly sideways, however, the load $P$ acting on the bent
member produces a moment $P\,v$ that tends to increase the deflection, while
the bending stiffness $EJ$ tends to straighten it. The **critical load**
$P_{cr}$ is the load at which the two balance: beyond $P_{cr}$ the member no
longer returns straight and bends sideways (Euler, 1744).

$$
EJ\,v'''' + P\,v'' = 0
\qquad\Rightarrow\qquad
P_{cr} = \frac{\pi^2 E J}{L_0^2}, \qquad L_0 = \beta L
$$

The **effective length** $L_0$ is the distance between two consecutive
inflection points of the buckling mode (extended beyond the member if needed,
as for the cantilever): it depends on the supports through the factor $\beta$
(1 pinned–pinned, 2 cantilever, 0.7 fixed–pinned, 0.5 fixed–fixed,
1 fixed–guided). Doubling $L$ makes $P_{cr}$ **one quarter**.

$P_{cr}$ depends on $E$ and $J$, but **not on the strength** of the material.
Strength gives a second limit, $N_{pl} = A\,f$. Dividing by $A$ and
introducing the radius of gyration $i = \sqrt{J/A}$ and the **slenderness**
$\lambda = L_0/i$:

$$
\frac{P_{cr}}{A} = \frac{\pi^2 E}{\lambda^2}
\qquad\text{equal to } f \text{ at}\qquad
\lambda_1 = \pi\sqrt{\frac{E}{f}}
$$

For $\lambda > \lambda_1$ buckling governs, for $\lambda < \lambda_1$ the
material does. The member bends about the axis with the smaller $J$ (weak
axis), unless it is restrained in that direction.

| Material | $E$ | $f$ | $\lambda_1$ |
|---|---|---|---|
| Steel S235 | 210 GPa | 235 MPa | 93.9 |
| Timber C24 | 11 GPa | 21 MPa | 71.9 |
| Concrete C25/30 | 31 GPa | 25 MPa | 110.6 |

**Assumptions.** Ideal Euler column: linear elastic material, perfectly
straight axis, centred load. No imperfections and no residual stresses: this
is why, near $\lambda_1$, the real capacity is much lower than
$\min(P_{cr}, N_{pl})$ (EC3 and EC5 buckling curves, not covered here).
Small displacements: the amplitude of the buckling mode is undetermined and is
drawn amplified. Indicative values of $E$ and $f$, without partial safety
factors: they serve to compare materials, not to check the member against
design codes (for concrete, a plain unreinforced section). Properties of rolled sections
(root fillets included) from the ArcelorMittal tables.

**Sign convention.** Compression positive.

**Validation.** Timoshenko & Gere, *Theory of Elastic Stability*, ch. 2;
EN 1993-1-1 §6.3.1 for the definition of slenderness; hand-calculation checks
in `test_core.py`.
""",
    },
}
