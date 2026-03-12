# Real-time Speech Translation to English (Whisper)

This repository now includes two standalone tools:

1. **`realtime_translate.py`** — continuously listens to your microphone, detects spoken language, transcribes, and translates to English.
2. **`spinesignal.html`** — a single-page **Spine Surgery Research Evidence Platform** that simulates aggregated evidence from PubMed/Cochrane/Embase/Google Scholar/Web of Science for manuscript support.

---

## 1) Real-time translation script

### Setup

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### Run

```bash
python realtime_translate.py
```

### Optional flags

- `--model small` (default: `small`)
- `--chunk-seconds 5`
- `--sample-rate 16000`
- `--device <name_or_index>`

Example:

```bash
python realtime_translate.py --model base --chunk-seconds 4
```

---

## 2) SpineSignal web app

### Run locally (no build needed)

```bash
python -m http.server 8000
```

Then open:

- `http://localhost:8000/spinesignal.html`

### Included capabilities

- 30+ seeded spine research topics across 6+ categories
- Topic directory with search + filters
- Topic-level evidence dashboard:
  - Evidence Strength Score (0–100)
  - Database-wise publication/quality breakdown
  - 10-year trend chart
  - Level of Evidence pie chart (I–V)
  - Supporting vs contradicting findings with DOI links
- Evidence Quadrant scatter plot (quality vs publication volume)
- Head-to-head comparison with manuscript-ready paragraph generation
- Manuscript assistant:
  - Introduction builder
  - PRISMA flow template generator
  - Statistical summary table generator
  - Reference formatter (Vancouver/AMA/journal presets)

### Notes

- Data are realistic simulations intended for sandbox/demo use.
- No backend required; everything runs client-side.
