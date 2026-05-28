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

- [ ] **KiCad circuit replacements (5 SVGs)** — KiCad 10.0.3 confirmed installed at
  `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`. Targets:
  - `gpio.html` — Push-pull + open-drain output circuits
  - `power-thermal.html` — Buck converter hot loop
  - `can.html` — CAN bus with 120Ω termination resistors
  - `i2c.html` — Open-drain pull-up bus topology (multiple devices + resistors)

## Assessed — Keep as SVG (Mermaid not appropriate)

The following SVGs were reviewed and decided to keep as hand-coded SVG because
Mermaid cannot replicate their layout, custom shapes, or semantic content:
- `bare-metal.html` startup sequence — has Flash/RAM side annotation box
- `bare-metal.html` ring buffer — circular layout with head/tail pointers
- `gpio.html` pin routing — trapezoid MUX symbol + fan-out
- `spi.html` shift register loop — hardware circuit diagram
- `spi.html` CPOL/CPHA waveforms — kept as SVG (complex timing with sample markers)
- `spi.html` CS topologies — two-panel comparison with colored CS lines
- `dma.html` CPU utilization — timeline/bar chart
- `dma.html` ping-pong buffer — timeline with DMA+CPU bands
- `dma.html` descriptor structure — 32-bit memory layout
- `memory-clocks.html` SRAM layout — address-annotated memory region stack
- `interrupts-nvic.html` exception stacking — stack frame memory layout
- `debug.html` connection block — clean as-is, MCU has nested sub-components

---

## Completed This Session

- [x] **Mermaid batch 3** — clock tree in memory-clocks.html
  - `memory-clocks.html` — Clock tree (`flowchart LR`; 4 color-coded sources → HF/LF Muxes → Prescaler → outputs)
  - Mermaid CDN added to memory-clocks.html head
  - Pushed in commit 95ef1a3; verified in Chrome

- [x] **Mermaid batch 2** — replaced 3 more SVGs:
  - `rtos.html` — Task state machine (`stateDiagram-v2`, LR; Running/Ready/Blocked/Suspended with `classDef`)
  - `usb.html` — USB enumeration sequence (`sequenceDiagram`, HOST↔DEVICE, 11 messages + Note)
  - `usb.html` — Descriptor hierarchy tree (`flowchart TD`; blue/green/amber `classDef` by level)
  - Mermaid CDN added to rtos.html and usb.html heads
  - All changes pushed in commit ca0559e
  - Visual verification: all 3 diagrams confirmed rendering in Chrome

- [x] **Mermaid batch 1** — replaced 3 SVG state/flow diagrams with Mermaid:
  - `mcu-architecture.html` — Processor mode state machine (`stateDiagram-v2`, LR, Handler Mode amber `classDef`)
  - `mcu-architecture.html` — Reset startup flow (`flowchart TD`, stadium RESET, color-coded steps)
  - `can.html` — Error confinement state machine (`stateDiagram-v2`, green/amber/red `classDef`)
  - Mermaid CDN added to `can.html` head
  - WaveDrom skin fix (skins/default.js) confirmed working in uart.html and i2c.html
  - All changes pushed in commit b64597c
  - Visual verification: all 3 diagrams confirmed rendering in Chrome

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
