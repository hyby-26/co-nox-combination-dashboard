# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

**Pre-implementation.** This repo currently contains only design docs and raw data — no application code, no `requirements.txt`, no build/lint/test tooling exists yet. There is nothing to build or run. Before writing implementation code, read `docs/PRD.md` (scope, priorities) and `docs/DESIGN.md` (architecture, module layout, directory structure) — they define what should exist once implementation starts, and code should follow that structure rather than inventing a new one.

**`docs/` and `backup/` are gitignored** (ADR-004 in `docs/DECISIONS.md`) — `docs/` isn't meant to be pushed/shared in this repo, and `backup/` holds unused data kept only for local reference. Don't assume either is present in a fresh clone; still read and maintain `docs/` locally as the working reference. `data/raw/merged_df.csv` is the one data file that **is** tracked in git — it's a required runtime dependency, not a design doc.

## Documentation map

- `docs/PRD.md` — what/why: background, goals, scope, priorities (P0/P1/P2), risks
- `docs/DESIGN.md` — how: tech stack, architecture, module design, screen design, directory layout, deployment options
- `docs/DECISIONS.md` — ADR log: why specific choices were made (e.g. Dash over Streamlit, single active dataset). Check this before revisiting a settled decision.

Treat `docs/PRD.md` and `docs/DESIGN.md` as the source of truth for scope and structure. If code needs to diverge from them, update the docs in the same change rather than letting them drift.

## Data

- **Active dataset: `data/raw/merged_df.csv` only** (36,733 rows, columns: `datetime, AT, AP, AH, AFDP, GTEP, TIT, TAT, TEY, CDP, CO, NOX`). This is the sole data source the dashboard should read.
- `backup/gt_2011.csv`–`gt_2015.csv` (top-level, outside `data/`) are the original per-year files `merged_df.csv` was built from. They are **unused and kept only as backup**, and gitignored (ADR-003, ADR-004 in `docs/DECISIONS.md`) — do not wire them into the app as a selectable data source.
- `merged_df.csv`'s `datetime` column has a known reliability issue: it looks like a continuous hourly sequence stamped across the concatenated files rather than each row's true measurement time (see `docs/PRD.md` §1.1 and `docs/DESIGN.md` §6). Don't treat it as ground truth without accounting for this; the conditions for fixing it are tracked in `docs/DESIGN.md` §6.

## Planned architecture (not yet implemented)

Per `docs/DESIGN.md`: a Dash (Plotly) app with `data_loader.py` → `data_processor.py` → chart components (`components/distribution.py`, `timeseries.py`, `correlation.py`, `data_quality.py`) feeding a single `app.py`. Model inference (`model_adapter.py`, `components/prediction.py`) is a second-phase addition that depends on a teammate's model, delivered from a **separate repository** — see `docs/DECISIONS.md` ADR-002 for the (proposed, not yet accepted) integration approach. Don't build model integration ahead of that model actually existing.
