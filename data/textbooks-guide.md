# Textbooks — Organisation & Coordination Guide

Reference for managing the physical PDF collection and its integration with the
notes site's book-reference system.

---

## Physical folder location

```
C:\Users\eugle\OneDrive - University of Toronto\School Stuff\Textbooks\
├── analog\
├── bioelectricity\
├── computing\
├── embedded\
├── mathematics\        ← also holds complexity/dynamics books
├── neuroscience\
├── quantum\
└── rl\
```

New subject folders to create when PDFs arrive:
`circuits\`, `physics\` (classical mechanics, EM, thermo), `life-sciences\`

---

## File naming convention

```
Author(s) - Title (Xth ed, YYYY).pdf
```

Examples:
- `Griffiths & Schroeter - Introduction to Quantum Mechanics (3rd ed, 2018).pdf`
- `Bear, Connors & Paradiso - Neuroscience Exploring the Brain (4th ed, 2015).pdf`
- `Sutton & Barto - Reinforcement Learning An Introduction (2nd ed, 2018).pdf`

Rules:
- **1 author:** `Surname - Title`
- **2 authors:** `Surname1 & Surname2 - Title`
- **3+ authors:** `Surname1, Surname2 & Surname3 - Title` (or `Surname et al` if long)
- Include edition and year in parentheses when known
- No underscores, no libgen/pdfcoffee prefixes, no degree suffixes (PhD, etc.)
- Papers go in `[Paper] Title.pdf` format — kept separate from textbooks

---

## Adding a new book

### Step 1 — Get the PDF
Either:
- Drop the file in the appropriate subfolder under `Textbooks\`, or
- Give Claude a direct URL and it will download it with `Invoke-WebRequest`

### Step 2 — Add an entry to `data/books.yaml`

```yaml
- id: author-shorttitle          # kebab-case, unique
  title: Full Title Here
  authors: [Author One, Author Two]
  edition: 3rd                   # omit if not applicable
  publisher: Publisher Name
  year: 2024
  clusters: [cluster-id-1, cluster-id-2]
  annotation: One or two sentences on what this covers and why it's here.
  source: SchoolStuff:Textbooks/subfolder/Exact Filename.pdf
  # url: https://... (for freely available online books — use instead of or alongside source)
```

### Step 3 — Run `push.ps1`
`build.py` auto-regenerates `data/resource-gaps.md` and `books.json`.
The book immediately appears on `references.html` and in any cluster page
that lists its cluster ID.

---

## The `source` field

Format: `SchoolStuff:Textbooks/subfolder/Exact Filename.pdf`

`SchoolStuff:` is a shorthand prefix for
`C:\Users\eugle\OneDrive - University of Toronto\School Stuff\`.

The filename in the `source` field must exactly match the file on disk.
When a file is renamed, update the `source` field to match.

For books freely available online, use `url:` instead of (or alongside) `source:`.

---

## Downloading PDFs

Claude can download any publicly accessible PDF directly to the folder:

> "Download [URL] to the textbooks folder as [filename]"

Uses `Invoke-WebRequest` — no token cost, runs locally.

Freely available books worth downloading:
| Book | URL |
|---|---|
| Astrom & Murray — *Feedback Systems* | https://www.cds.caltech.edu/~murray/books/AM08/pdf/am08-complete_22Feb09.pdf |
| Osborne & Rubinstein — *A Course in Game Theory* | https://arielrubinstein.tau.ac.il/books/GT.pdf |
| Shoham & Leyton-Brown — *Multiagent Systems* | https://www.masfoundations.org/mas.pdf |
| MacKay — *Information Theory, Inference, and Learning Algorithms* | https://www.inference.org.uk/itprnn/book.pdf |
| Barabási — *Network Science* | http://networksciencebook.com/ (chapter PDFs) |

---

## Resource gap tracker

`data/resource-gaps.md` is auto-generated on every `push.ps1` run.
It lists every cluster with and without textbook entries in `books.yaml`.
Check it before starting any new cluster — a cluster with no books should
get its primary reference added to `books.yaml` first.

---

## Books in the folder not yet in books.yaml

These files exist on disk but have no YAML entry yet. Add entries when the
relevant cluster is ready to be written.

| File | Likely cluster |
|---|---|
| `mathematics/Bak - How Nature Works (1996).pdf` | `complex-systems` |
| `mathematics/Strogatz - Sync (2003).pdf` | `nonlinear-dynamics` |
| `mathematics/The Geometry of Biological Time.pdf` | `nonlinear-dynamics` |
| `bioelectricity/2020_Electronic_neural_interfaces.pdf` | `bioelectricity` (confirm title/author) |
| `bioelectricity/Design_of_Efficient_and_Safe_Neural_Stimulators...pdf` | `bioelectricity` |
| `bioelectricity/Electrical Circuits in Biomedical Engineering.pdf` | `bioelectricity` |
| `bioelectricity/Principles of Electrical Neural Interfacing.pdf` | `bioelectricity` |
| `bioelectricity/Textbook of Neuromodulation.pdf` | `bioelectricity` |
| `computing/Computer Architecture - Patterson & Hennessy.pdf` | `computing` |
| `analog/Understanding DeltaSigma Data Converters.pdf` | `analog` |

---

## Pending PDFs (roadmap subjects — user to supply)

| Subject | Primary reference |
|---|---|
| Calculus & Real Analysis | Abbott *Understanding Analysis*; Spivak *Calculus* |
| Linear Algebra | Axler *Linear Algebra Done Right*; Strang *Introduction to Linear Algebra* |
| Differential Equations | Boyce & DiPrima *Elementary Differential Equations*; Strauss *PDEs* |
| Classical Mechanics | Taylor *Classical Mechanics*; Goldstein *Classical Mechanics* |
| Electromagnetism | Griffiths *Introduction to Electrodynamics* |
| Circuit Theory | Nilsson & Riedel *Electric Circuits* |
| Probability Theory | Blitzstein & Hwang *Introduction to Probability* |
| Statistics & Inference | DeGroot & Schervish *Probability and Statistics* |
