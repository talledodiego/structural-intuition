---
slug: euler_buckling
title: {it: "Instabilità euleriana", en: "Euler buckling"}
subtitle: {it: "Perché la snellezza conta più della resistenza", en: "Why slenderness matters more than strength"}
courses: [lab2]
level: base
tier: A
dependencies: [numpy, matplotlib]
validation: "Timoshenko & Gere, Theory of Elastic Stability, ch. 2; EN 1993-1-1 §6.3.1 for slenderness definition; ArcelorMittal sales programme for HEA/IPE section properties"
status: published
---

# Euler buckling

This is the project's pilot applet. The content is simple, but it uses the full structure: template, i18n, shared code, tests and WASM export.

## Key message

The load a slender compressed member can carry depends on its **slenderness** (stiffness and effective length), not on the strength of its material: doubling the length divides the critical load by four.

## What the student can do

Visible controls:

- **Axial load** P, compression, from 0 to about Npl. An ideal member cannot carry more than Npl, so the last slider value is Npl rounded up to 10 kN (395.5 → 400 kN, 1265.1 → 1270 kN). The other values are about 200 steps of a 1-2-5 size. The range depends only on section and material: moving L or changing the supports never rescales P. When the range changes, P keeps its value, snapped to the nearest step (or to Npl if it is larger).
- **Support conditions:** pinned–pinned, fixed–free, fixed–pinned, fixed–fixed, fixed–guided (effective length factor β = 1, 2, 0.7, 0.5, 1).
- **Length** L (1 … 12 m, step 0.1 m).
- **Cross-section type:** I-section (rolled), rectangular, circular, custom.
- **Section size**, depending on the type: a profile from a list (HEA 100…400, IPE 100…400); b and h for a rectangular section (20 … 600 mm, default 100 × 160); d for a circular section (20 … 600 mm, default 60); or, for a custom section, A [mm²], J_y (strong axis) and J_z (weak axis) [mm⁴]. If J_z > J_y the two values are swapped. The controls for the other types are hidden.
- **Buckling axis:** weak / strong. Hidden for circular sections.
- **Material:** steel S235, timber C24, concrete C25/30. This sets E and an indicative strength f. I-sections are always steel S235, so for them the material control is replaced by a note.

Up to 7 controls are visible (8 for a custom section), one more than the template's 5–6. This was accepted because the axis choice is central to the key message.

Default: steel HEA120, L = 3 m, pinned–pinned, weak axis, P = 560 kN. The applet opens on a buckled member, with Pcr = 532 kN just below Npl = 595 kN.

| Material | E | f (indicative) | λ₁ = π√(E/f) |
|---|---|---|---|
| Steel S235 | 210 GPa | f_y = 235 MPa | 93.9 |
| Timber C24 (parallel to grain) | E₀,mean = 11 GPa | f_c,0,k = 21 MPa | 71.9 |
| Concrete C25/30 | E_cm = 31 GPa | f_ck = 25 MPa | 110.6 |

## Outputs

- **Drawing of the member** with its supports and the load arrow (red, with its value). The base is a hatched fixed end or a hinge. At the top, every restraint lets the member slide vertically: pinned is a horizontal link to a side wall; fixed is a sleeve that restrains sway and rotation; guided is a rigid cap that stays horizontal and is free to sway. The member can be in one of three states:
  - P < min(Pcr, Npl): the member is OK and is drawn straight.
  - Pcr < Npl and P ≥ Pcr: **buckling**. The amplified buckling mode is drawn in blue.
  - Npl ≤ Pcr and P ≥ Npl: **crushing / yielding**. There is no buckling mode, and the member is drawn red with the label "material strength reached".
- A small drawing of the cross-section, with the bending axis (dashed orange, labelled y or z) and the direction of the deflection (blue arrow). A custom section is drawn as a dashed square.
- **Critical load Pcr** in large text. Below it: Npl = A f, λ, λ₁, i, L₀ and the utilisation P / min(Pcr, Npl), followed by a coloured message with the state (holds, buckling, or material strength reached).
- **Pcr–λ chart** for the current section area A. It shows the Euler hyperbola π²EA/λ² (dashed), the material limit Npl = A f (red) and the capacity min(Pcr, Npl) (blue), with the area below the capacity filled green ("the member holds"). It also shows λ₁ (dotted), with the labels "material governs" and "buckling governs" on either side, the current Pcr (hollow blue marker) and the current state (λ, P) (orange). The load axis ends at the next 1-2-5 value above 1.5 Npl, so it changes only with section and material and leaves room above the material limit. The λ axis goes to 300, or further if λ is larger.
- Slenderness λ = L₀/i, radius of gyration i and effective length L₀ = βL.

## Assumptions and simplifications

- Ideal Euler column: linear elastic material, perfectly straight member, centred load.
- No imperfections, no residual stresses and no interaction curves. The EC3/EC5 buckling curves are out of scope for v1, so for λ ≈ λ₁ the real capacity is well below min(Pcr, Npl).
- Small displacements. The amplitude of the buckling mode is arbitrary and is drawn amplified.
- The "material limit" Npl = A f uses an indicative characteristic strength, with no partial safety factors. It is for comparison only.
- E and f are indicative values for comparing materials, not for code checks: timber E ≈ 11 GPa (E₀,mean of C24), concrete E ≈ 31 GPa (E_cm of C25/30, plain unreinforced section), steel E = 210 GPa. Code checks (EC3, EC5) are left to separate applets.
- Rolled-section properties (A, J_y, J_z, i) come from the tables and include the root fillets.
- Compression is taken as positive.

## Validation

- $P_{cr} = \pi^2 E J / (\beta L)^2$ checked against hand calculations for each support case. Examples, S235, L = 3 m, pinned–pinned, weak axis: HEA120 (J_z = 230.9 cm⁴): Pcr = 532 kN, Npl = 595 kN, λ = 99.4; HEA300 (J_z = 6310 cm⁴): Pcr = 14 530 kN, Npl = 2644 kN, λ = 40.1.
- Scaling checks: $P_{cr} \propto 1/L^2$, $\propto E$ and $\propto J$.
- The table section properties are checked against the geometry: A against 2 b t_f + (h − 2t_f) t_w + (4 − π) r².
- The mode shapes satisfy the boundary conditions: zero displacement at the supports, and zero slope at fixed ends.
- Tests are in `test_core.py`.

## Scope

This applet is for reasoning about the Euler formula for an ideal member. Imperfections, amplification of deflection (Perry–Robertson) and the EC3 buckling curves (χ–λ̄) are left to a separate, planned applet on the buckling of steel members, and will not be added here.

## Possible v2

- Intermediate restraints (bracing) to show the effect on effective length.

## Notes for the teacher

Suggested in-class questions to ask before opening the applet (these are not shown in the applet):

- "If you double the length of the member, the critical load…" (a) halves · (b) becomes one quarter ✅ · (c) stays the same
- "Steel or timber column of the same size: which buckles first, and by how much?"
- "Which way will a rectangular column bend?"
- "The default HEA120 buckles. Change to HEA160 with the same length: buckling or yielding?"
