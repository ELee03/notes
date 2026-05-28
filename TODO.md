# Claude Agent TODO
<!-- Keep this file updated as work progresses. Read it at the start of every session. -->

Last updated: 2026-05-28

---

## In Progress

*(nothing actively in-flight)*

---

## Pending — Embedded cluster visual/math pass

- [ ] **KaTeX audit pass** — now that the DOMContentLoaded fix is deployed,
  scan all 5 KaTeX pages (power-thermal, adc-dac, i2c, high-speed-rf, bode)
  to confirm inline `$...$` math renders correctly after hard-refresh.

- [ ] **Per-lesson references section** — user requested references at the
  bottom of each individual lesson page (not just cluster index). Need to
  decide whether to use a static list or the `renderBooks` dynamic approach.
  Requires knowing which specific textbook chapters each lesson draws from;
  ask user or leave as a template with TODOs.

---

## Completed This Session

- [x] **Wavedrom timing diagrams** implemented:
  - `embedded/uart.html` — RTS/CTS flow control → WaveDrom (3 signals: TX data bus,
    RTS_N, CTS_N; propagation delay shown as 1-unit lag)
  - `embedded/i2c.html` — START/STOP conditions → WaveDrom (SCL + SDA showing
    SDA transitions during SCL=HIGH as bus conditions)
  - `embedded/i2c.html` — Address frame + ACK → WaveDrom (9 clocks: A6-A0 + R/W
    driven by master, 9th clock ACK driven by slave)
  - **Kept as SVG** (WaveDrom would be worse):
    - `uart.html` UART 8N1 frame — sampling dots and per-bit color coding can't be
      replicated in WaveDrom
    - `spi.html` CPOL/CPHA 4-mode grid — sample-point markers, complex layout
    - `timers-pwm.html` counter waveforms — analog sawtooth/triangle shapes
    - `can.html` arbitration table — table format, not waveform
- [x] **CLAUDE.md update** — removed stale "known visual debt" GPIO entry; added
  WaveDrom usage guidelines and when to use SVG vs WaveDrom
- [x] GPIO push-pull/open-drain + input mode diagrams — replaced hand-coded SVG
  with schemdraw-generated SVGs (`_gpio_*.svg` files), embedded via `<img>`
- [x] `.nojekyll` added to repo root — fixes GitHub Pages silently dropping
  `_`-prefixed files (was causing all schemdraw SVGs to 404)
- [x] KaTeX `onload` → `DOMContentLoaded` fix applied to all 5 KaTeX pages
  — `onload` on a `defer` CDN script is unreliable across browsers; the
  DOMContentLoaded event fires specifically after all defer scripts execute
- [x] power-thermal.html — moved `$$...$$` display blocks out of prose divs
  into dedicated `<div class="math-block">` elements
- [x] high-speed-rf, i2c, adc-dac, gpio — KaTeX CDN added, math notation
  converted from monospace code blocks to proper LaTeX
- [x] power-thermal.html — T_J worked examples converted from C-comment style
  to KaTeX display equations
- [x] Confirmed reference library system already exists: `data/books.yaml` →
  `build.py` → `books.json` → `books-render.js`. embedded/index.html already
  uses `renderBooks()`. No per-lesson references yet.

---

## Known Issues / Decisions Pending

- **GPIO input modes (floating/pull-up/pull-down)**: schemdraw SVGs loaded via
  `<img>`. Not flagged as broken but may have layout issues similar to the
  output-mode SVGs that were redrawn. Review if user reports problems.

- **KiCad for schematics — pending install**: user is installing KiCad; will
  confirm when ready. Plan: use `kicad-cli sch export svg` for ALL circuit
  schematics going forward — Circuits cluster AND any Embedded diagrams that
  warrant it (GPIO output stages, power topologies, etc.). Hand-coded SVG is
  the fallback only while KiCad is unavailable.
  Expected CLI path: `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`
  Export command: `kicad-cli sch export svg --output <dir> <file>.kicad_sch`
  Once confirmed, also add a note to CLAUDE.md under Visuals.

- **Diagrams strategy (settled)**: WaveDrom for digital timing diagrams;
  hand-coded SVG for circuit schematics, analog waveforms, and anything needing
  custom markers or complex layout; Plotly for interactive math plots.
