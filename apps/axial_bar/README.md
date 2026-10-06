---
slug: axial_bar
title: {it: "Barra soggetta a sforzo normale", en: "Axially loaded bar"}
subtitle: {it: "Legge di Hooke: la barra e il suo materiale", en: "Hooke's law: the bar and its material"}
courses: ['lab2']
level: base
tier: A
dependencies: [numpy, matplotlib]
validation: "Gere & Goodno, Mechanics of Materials, ch. 2 (axially loaded members)"
status: published
thumbnail: public/thumbnail.svg
---

# Axially loaded bar

## Key message

The stiffness of a bar depends on the bar properties (dimensions and material), $k = EA/L$; the stress–strain law depends only on the material, $\sigma = E\varepsilon$. Changing length or area changes the first, not the second.

## What the student can do

- **Axial force** N, from compression to tension (−50 … +50 kN, step 1 kN).
- **Length** L (0.5 … 6 m) and **cross-sectional area** A (50 … 1000 mm², step 10 mm²).
- **Young's modulus** E (10 … 250 GPa) and **Poisson's ratio** ν (0 … 0.5).
- **Drawing magnification factor** (1 … 1000), for the drawing only.
- **Clear trace** of the previous states.

Defaults: steel bar, L = 1 m, A = 200 mm², E = 210 GPa, ν = 0.3, N = 10 kN.

## Outputs

- Elongation ΔL in large text; σ, ε, lateral change Δd and equivalent diameter d.
- Drawing of the bar: undeformed (grey) and deformed (blue), fixed support, load arrow. The deformed shape shows the Poisson effect (thinner in tension, thicker in compression). Thickness not to scale; displacements multiplied by the magnification factor, reduced automatically when the drawn length or width would change by more than 50 %.
- Two charts with the elastic law, the current state and the trace of the previous states: **N–ΔL** (the bar, slope EA/L) and **σ–ε** (the material, slope E). The trace is cleared when L, E or A change. Axis limits change in 1-2-5 steps, so a change of stiffness shows as a change of slope.

## Assumptions and simplifications

- Linear elastic, isotropic material; no yielding or failure. With the smallest area and the largest force σ reaches 1000 MPa, well above the yield strength of structural steel: the applet stays elastic on purpose.
- Small displacements.
- Uniform stress over the section and along the bar: local effects near the support and the load are neglected (Saint-Venant's principle).
- Buckling in compression is neglected (stocky or laterally restrained bar).
- The section is drawn as a solid circle of area A.
- Sign convention: tension positive.

## Validation

- $\Delta L = NL/(EA)$, $\sigma = N/A$, $\varepsilon = \sigma/E$, $\varepsilon_t = -\nu\varepsilon$ checked against a hand calculation for the defaults (σ = 50 MPa, ε = 0.238 ‰, ΔL = 0.238 mm, d = 16.0 mm, Δd = −0.00114 mm).
- Scaling checks: ΔL ∝ N, ∝ L, ∝ 1/E, ∝ 1/A; ε independent of L.
- Tests in `test_core.py`.

## Notes for the teacher

Suggested in-class questions (not shown in the applet):

- "Two bars of the same steel, one twice as long: which one elongates more under the same force? And which one has the larger strain?"
- "If you double the area, what happens to the N–ΔL line? And to the σ–ε line?"
