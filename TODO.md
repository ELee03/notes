# Claude Agent TODO
<!-- Keep this file updated as work progresses. Read it at the start of every session. -->

Last updated: 2026-05-28

---

## In Progress

- [ ] **GPIO hand-coded SVG redraw** — replacing schemdraw `<img>` tags with
  clean inline SVGs for push-pull and open-drain circuits (gate-on-left
  convention, no label overlaps). Input modes (floating/pull-up/pull-down)
  schemdraw SVGs may also need revisiting once output modes are confirmed good.

---

## Pending — Embedded cluster visual/math pass

- [ ] **Wavedrom timing diagrams** — convert hand-coded waveform SVGs to inline
  Wavedrom JSON specs in:
  - `embedded/uart.html` (UART 8N1 frame)
  - `embedded/spi.html` (SCLK/MOSI/MISO/CS timing)
  - `embedded/i2c.html` (START/data/ACK/STOP waveforms)
  - `embedded/timers-pwm.html` (PWM duty cycle)
  - `embedded/can.html` (CAN dominant/recessive bit timing)

- [ ] **KaTeX audit pass** — now that the DOMContentLoaded fix is deployed,
  scan all 5 KaTeX pages (power-thermal, adc-dac, i2c, high-speed-rf, bode)
  to confirm inline `$...$` math renders correctly after hard-refresh.

- [ ] **CLAUDE.md update** — remove stale "known visual debt" entry for
  gpio.html (now fixed), add note about `.nojekyll` and DOMContentLoaded
  KaTeX pattern being the correct approach.

- [ ] **Per-lesson references section** — user requested references at the
  bottom of each individual lesson page (not just cluster index). Need to
  decide whether to use a static list or the `renderBooks` dynamic approach.
  Requires knowing which specific textbook chapters each lesson draws from;
  ask user or leave as a template with TODOs.

---

## Completed This Session

- [x] GPIO push-pull/open-drain + input mode diagrams — replaced hand-coded SVG
  with schemdraw-generated SVGs (`_gpio_*.svg` files), embedded via `<img>`
- [x] `.nojekyll` added to repo root — fixes GitHub Pages silently dropping
  `_`-prefixed files (was causing all schemdraw SVGs to 404)
- [x] KaTeX `onload` → `DOMContentLoaded` fix applied to all 5 KaTeX pages
  — `onload` on a `defer` CDN script is unreliable across browsers; the
  DOMContentLoaded event fires specifically after all defer scripts execute
- [x] power-thermal.html — moved `$$...$$` display blocks out of prose divs
  into dedicated `<div class="math-block">` elements (mixed display+inline
  math in one element breaks KaTeX auto-render)
- [x] high-speed-rf, i2c, adc-dac, gpio — KaTeX CDN added, math notation
  converted from monospace code blocks to proper LaTeX
- [x] power-thermal.html — T_J worked examples converted from C-comment style
  to KaTeX display equations
- [x] Confirmed reference library system already exists: `data/books.yaml` →
  `build.py` → `books.json` → `books-render.js`. embedded/index.html already
  uses `renderBooks()`. No per-lesson references yet.

---

## Known Issues / Decisions Pending

- **GPIO input modes (floating/pull-up/pull-down)**: schemdraw SVGs
  (`_gpio_floating.svg`, `_gpio_pullup.svg`, `_gpio_pulldown.svg`) loaded via
  `<img>`. User hasn't flagged these as broken yet but they may have similar
  layout issues to the output mode SVGs. Review after output modes are fixed.

- **KiCad for future complex schematics**: agreed to revisit when Circuits
  cluster is written. For simple educational circuits (≤5 components), hand-
  coded SVG is preferred.

- **Diagrams strategy (settled)**: generate locally → embed as static SVG/PNG.
  Hand-coded SVG for circuit schematics. Wavedrom (in-browser) only for timing
  diagrams (pure rectangle/line geometry, platform-consistent). Plotly for
  interactive math plots.
