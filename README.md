# Strand Selector

A lightweight desktop application for rapid manual selection of Strand-seq cells from MosaiCatcher count plot PDFs.

Strand Selector was designed to speed up visual QC of Strand-seq libraries by allowing users to quickly classify cells using only the keyboard while automatically recording annotations and exporting selected cell IDs for downstream cluster workflows.

---

## Features

* Open MosaiCatcher count plot PDFs directly
* Automatic extraction of:

  * Sample name
  * Cell ID
  * Total reads
  * Duplicate rate
* Fast keyboard-driven annotation workflow
* Continuous autosave
* Export of:

  * Full annotation table (`annotations.csv`)
  * Selected cell list (`<sample>.txt`)
* Results organized by sample

---

## Installation

Clone the repository:

```bash
git clone git@github.com:pweidner/strand-selector.git
cd strand-selector
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Verify installation:

```bash
strand-selector
```

You should see the usage message.

---

## Usage

Launch Strand Selector on a MosaiCatcher count plot PDF:

```bash
strand-selector sample_count_plots.pdf
```

Example:

```bash
strand-selector IBD-CD19_CountComplete.raw.pdf
```

At startup the application will:

1. Scan the PDF
2. Extract sample metadata
3. Detect all cell pages
4. Create a results directory

Example:

```text
Loading PDF: IBD-CD19_CountComplete.raw.pdf
Scanning pages and extracting metadata...

Detected 384 cell pages
Sample: IBD-CD19-T
Results: results/IBD-CD19-T
```

---

## Keyboard Controls

| Key         | Annotation               |
| ----------- | ------------------------ |
| Right Arrow | selected                 |
| Down Arrow  | low_reads                |
| U           | brdu_under               |
| O           | brdu_over                |
| S           | spikey                   |
| Backspace   | undo previous annotation |

The application advances automatically after each classification.

---

## Outputs

Results are written to:

```text
results/
└── SAMPLE/
```

Example:

```text
results/
└── IBD-CD19-T/
    ├── annotations.csv
    ├── autosave.json
    └── IBD-CD19-T.txt
```

### annotations.csv

Contains one row per cell:

```csv
cell_id,label,reads,duplicate_rate
A6159_L2_1003,selected,183213,0.82
```

### SAMPLE.txt

Contains only selected cell IDs:

```text
A6159_L2_1003
A6159_L2_1007
A6159_L2_1011
...
```

This file can be used directly as input for downstream cluster jobs.

### autosave.json

Written after every annotation.

Can be used to recover work if the application crashes before export.

---

## Expected PDF Format

Each cell page should contain metadata similar to:

```text
Sample: IBD-CD19-T
Cell: A6159_L2_1003
Total number of reads: 183,213
Duplicate rate: 82%
```

The application extracts these fields automatically.

---

## Motivation

Manual Strand-seq cell selection remains one of the most time-consuming QC steps in many workflows.

Strand Selector aims to provide a minimal, fast, keyboard-only interface focused specifically on Strand-seq count plot review without requiring general-purpose PDF tools or manual note-taking.

---

## Status

Current status: v1.0

Successfully tested on multiple MosaiCatcher count plot PDFs containing hundreds of cells per sample.

