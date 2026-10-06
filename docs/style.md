# Style

## General

- **Light backgrounds only**, for both UI and plots. No dark themes.
- Clean, minimal layout. One accent colour per meaning.
- Plots are produced through `shared.plotting`, which sets the defaults below. Do not override them locally without a reason.

## Palette

| Role | Colour | Hex |
|---|---|---|
| Structure (undeformed) | grey | `#9AA0A6` |
| Structure (deformed / response) | blue | `#1F5FAD` |
| Current state / highlighted point | orange | `#E8710A` |
| Limit / threshold / failure | red | `#C5221F` |
| Safe region | green (light fill) | `#E6F4EA` |
| Reference / analytical curve | dark grey, dashed | `#3C4043` |
| Background | white | `#FFFFFF` |
| Grid | very light grey | `#ECEFF1` |

Never use colour alone to carry meaning: combine with line style, markers or labels.

## Plots

- Font: sans-serif, minimum 11 pt in the rendered figure.
- Always label axes with quantity, symbol and unit: `Slenderness λ [-]`, `Critical load Pcr [kN]`.
- Light grid, no top/right spines.
- Show the current state as an orange marker on every chart that has one.
- Prefer one clear chart over several small ones.

## Drawings of structures

- Supports drawn with standard symbols (hinge triangle, roller, hatched fixed end).
- Deformed shapes amplified and labelled as "amplified" / "amplificata".
- Loads as arrows in red, with value label.

## Sign conventions

- Compression positive in buckling applets (stated in the *Why?* section).
- Tension positive in stress-state applets (Mohr, Hooke), as in continuum mechanics.
- Each applet states its convention explicitly in *Why?*.

## Numbers and units

- **Internal** (all of `core.py`): consistent system N, mm, MPa (= N/mm²). Derived: moments in N·mm, areas in mm², second moments of area in mm⁴. With these units, $P_{cr} = \pi^2 E I / L_0^2$ gives N directly.
- **Display** (UI), converted via `shared.units`. Member lengths are entered and shown in m but converted to mm before any computation:

| Quantity | Display unit |
|---|---|
| Forces | kN |
| Moments | kNm |
| Lengths of structural members (spans, heights, effective lengths) | m |
| Section dimensions | mm |
| Second moments of area | mm⁴ |
| Stresses / strengths | MPa |
| Elastic moduli | GPa |

- Significant figures: 3 for results, no more than needed for inputs.
