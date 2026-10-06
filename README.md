# Structural Intuition

**Interactive applets to build intuition about structural behaviour.**

Structural Intuition is a collection of small, interactive web applets for students of architecture, urban planning and engineering. Each applet isolates one structural concept — buckling, stress transformation, anisotropic elasticity, reinforced concrete in bending — and lets students *explore, observe and interpret* by changing parameters and watching the response change in real time.

The goal is not to compute numbers, but to understand **why** structures behave the way they do.

🔗 **Gallery:** <https://talledodiego.github.io/structural-intuition/> (published with GitHub Pages).

---

## How it works

- Applets are written as [marimo](https://marimo.io) notebooks in plain Python.
- Most applets are exported to **WebAssembly** and run entirely in the browser: no installation, no account, no server. Students just open a link.
- Applets that need heavier tools (e.g. OpenSeesPy) can be opened on [molab](https://molab.marimo.io) or run locally.
- Every applet is available in **Italian and English**. Add `?lang=en` (or `?lang=it`) to the URL. Italian is the default.

Every applet is a free playground with the same structure:

1. **Introduction** — what the applet shows
2. **Explore** — change parameters, watch the response
3. **Why?** — the theory behind what you observe (collapsible)

## Applets

| Applet | Topic | Status |
|---|---|---|
| [Axially loaded bar](apps/axial_bar/) | Hooke's law: stiffness of the bar vs the material | ✅ available |
| [Euler buckling](apps/euler_buckling/) | Elastic instability of compressed members | 🚧 in development |
| Lateral-torsional buckling | Instability of beams in bending | planned |
| RC bending | Reinforced concrete sections, M–N interaction | planned |
| Hooke's law for anisotropic materials | Isotropic, transversely isotropic, orthotropic, anisotropic | planned |
| Mohr's circle | Stress transformation | planned |
| Rule of mixtures | Stiffness of fibre composites | planned |

## Run locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone <repository-url>
cd structural-intuition
uv sync
uv run marimo run apps/axial_bar/app.py --no-sandbox   # use the applet
uv run marimo edit apps/axial_bar/app.py --no-sandbox  # edit it
uv run pytest                                          # run the tests
```

## Project documentation

- [Vision](docs/vision.md) — purpose, audience, principles
- [Applet template](docs/applet-template.md) — the learning structure and UI conventions
- [Localisation](docs/i18n.md) and [glossary](docs/glossary.md)
- [Style](docs/style.md) — plots, colours, sign conventions
- [Deployment](docs/deploy.md)
- [Decision records](docs/decisions/)

## Licence

- Code: [MIT](LICENSE)
- Educational content (texts, explanations, figures): [CC BY 4.0](LICENSE-CONTENT)

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Forks and adaptations for other courses are welcome too, keeping the licence notices.

---

## In italiano

**Structural Intuition** è una raccolta di applet interattive per studenti di architettura, pianificazione e ingegneria. Ogni applet isola un concetto strutturale e permette di esplorare, osservare e interpretare il comportamento cambiando i parametri in tempo reale. L'obiettivo non è calcolare, ma capire **perché** le strutture si comportano come si comportano.

Le applet funzionano direttamente nel browser, senza installare nulla. Sono disponibili in italiano (predefinito) e in inglese aggiungendo `?lang=en` all'indirizzo.

👉 **Galleria:** <https://talledodiego.github.io/structural-intuition/>
