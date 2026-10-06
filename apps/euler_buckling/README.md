---
slug: euler_buckling
title: {it: "Instabilità euleriana", en: "Euler buckling"}
subtitle: {it: "Perché la snellezza conta più della resistenza", en: "Why slenderness matters more than strength"}
courses: [lab2]
level: base
tier: A
dependencies: [numpy, matplotlib]
validation: "Timoshenko & Gere, Theory of Elastic Stability, ch. 2; EN 1993-1-1 §6.3.1 for slenderness definition"
status: draft
---

# Euler buckling

Pilot applet of the project: simple in content, complete in structure (template, i18n, shared code, tests, WASM export).

## Key message

The load a slender compressed member can carry depends on its **slenderness** (stiffness and effective length), not on the strength of its material: doubling the length divides the critical load by four.

## What the student can do

- **Support conditions:** pinned–pinned, fixed–free, fixed–pinned, fixed–fixed, fixed–guided (effective length factor β = 1, 2, 0.7, 0.5, 1).
- **Length** L.
- **Cross-section:** rectangular or circular, dimensions, choice of buckling axis (weak / strong).
- **Material:** steel, timber, concrete (sets E and a reference strength).

## Outputs

- Drawing of the member with supports and the **amplified buckling mode**.
- Current **critical load** Pcr in large text.
- **Pcr–λ chart**: Euler hyperbola, material squash/yield limit, current point. Shows where buckling governs and where the material does.
- Slenderness λ and transition slenderness λ₁ for the selected material.

## Assumptions and simplifications

- Linear elastic material, perfectly straight member, centred load (ideal Euler column).
- No imperfections, no residual stresses, no interaction curves (EC3 buckling curves are out of scope for v1).
- Small displacements; the buckling mode amplitude is arbitrary and drawn amplified.
- The "material limit" line is $N_{pl} = A f$ with an indicative strength $f$ per material, for comparison only.

## Validation

- $P_{cr} = \pi^2 E I / (\beta L)^2$ checked against hand calculations for each support case.
- Scaling checks: $P_{cr} \propto 1/L^2$, $\propto E$, $\propto I$.
- Mode shapes satisfy boundary conditions (zero displacement at supports, zero slope at fixed ends).
- Tests in `test_core.py`.

## Possible v2

- Initial imperfections and amplification of deflection (Perry–Robertson).
- EC3 buckling curves (χ–λ̄).
- Intermediate restraints (bracing) to show the effect on effective length.

## Notes for the teacher

Suggested in-class questions before opening the applet (not shown in the applet):

- "If you double the length of the member, the critical load…" (a) halves · (b) becomes one quarter ✅ · (c) stays the same
- "Steel or timber column of the same size: which buckles first, and by how much?"
- "Which way will a rectangular column bend?"
