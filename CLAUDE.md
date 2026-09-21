# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

**Implemented (functional, unstyled).** All 5 tabs (개요/분포/시계열/상관관계/데이터 품질) work end-to-end against `merged_df.csv` with live year/column filters. Run with `python src/app.py` (see `README.md` for venv/install steps), test with `pytest`. Still read `docs/PRD.md` (scope, priorities) and `docs/DESIGN.md` (architecture, module layout) before changing structure — they remain the source of truth, and code should follow them rather than inventing a new layout.

**Visual design is intentionally untouched** — plain Dash defaults + inline `style={}` dicts only, no `assets/` folder or custom CSS exists yet, even though ADR-001 (`docs/DECISIONS.md`) calls for "Dash + custom CSS". A dedicated design/styling pass is planned as separate work; don't restructure components or introduce a component library (e.g. dash-bootstrap-components) to fix styling — ADR-001 chose plain Dash + custom CSS specifically for layout freedom, so styling should stay CSS-based (`assets/*.css`, which Dash auto-loads) rather than swapping frameworks.

**`docs/` and `backup/` are gitignored** (ADR-004 in `docs/DECISIONS.md`) — `docs/` isn't meant to be pushed/shared in this repo, and `backup/` holds unused data kept only for local reference. Don't assume either is present in a fresh clone; still read and maintain `docs/` locally as the working reference. `data/raw/merged_df.csv` is the one data file that **is** tracked in git — it's a required runtime dependency, not a design doc.

## Documentation map

- `docs/PRD.md` — what/why: background, goals, scope, priorities (P0/P1/P2), risks
- `docs/DESIGN.md` — how: tech stack, architecture, module design, screen design, directory layout, deployment options
- `docs/DECISIONS.md` — ADR log: why specific choices were made (e.g. Dash over Streamlit, single active dataset). Check this before revisiting a settled decision.

Treat `docs/PRD.md` and `docs/DESIGN.md` as the source of truth for scope and structure. If code needs to diverge from them, update the docs in the same change rather than letting them drift.

## Data

- **Active dataset: `data/raw/merged_df.csv` only** (36,733 rows, columns: `datetime, AT, AP, AH, AFDP, GTEP, TIT, TAT, TEY, CDP, CO, NOX`). This is the sole data source the dashboard should read.
- `backup/gt_2011.csv`–`gt_2015.csv` (top-level, outside `data/`) are the original per-year files `merged_df.csv` was built from. They are **unused and kept only as backup**, and gitignored (ADR-003, ADR-004 in `docs/DECISIONS.md`) — do not wire them into the app as a selectable data source.
- `merged_df.csv`'s `datetime` column was flagged in `docs/PRD.md` §1.1 / `docs/DESIGN.md` §6 as a possible artifact (continuous hourly stamping across concatenated files rather than true measurement times). This has since been **verified reliable** and is used as-is (e.g. for year filtering) — `docs/PRD.md`/`docs/DESIGN.md` still describe it as an open risk and haven't been updated to reflect this; treat the code's usage (trusting `datetime`) as current, not those doc sections.
- Per-year row counts are uneven: 2011–2014 have ~8,760–8,784 rows (full years), but **2015 has only 1,669 rows** (partial year, not a bug) — surfaced in the 데이터 품질 tab, not hidden or filled in.

## Architecture (implemented)

`src/data_loader.py` (cached CSV load) → `src/filters.py` (pure filter/summary functions) → `src/components/{overview,distribution,timeseries,correlation,data_quality}.py` (each exposes a pure `build_*` figure/table function plus a thin `render(filtered_df)` wrapper) → `src/app.py` (Dash layout + two callbacks: filter summary, tab content dispatch by `dcc.Tabs` value). `src/data_processor.py` from `docs/DESIGN.md` §3 was never created — its planned responsibilities (missing-value checks, summary stats, quality flags) ended up living directly in `components/data_quality.py` and `components/overview.py` instead; if that changes, update `docs/DESIGN.md` accordingly.

Design/plan history for this implementation lives in `docs/superpowers/specs/` and `docs/superpowers/plans/` (gitignored along with the rest of `docs/`, so it won't appear in a fresh clone).

Model inference (`model_adapter.py`, `components/prediction.py`, Tab 6) is a second-phase addition that depends on a teammate's model, delivered from a **separate repository** — see `docs/DECISIONS.md` ADR-002 for the (proposed, not yet accepted) integration approach. Don't build model integration ahead of that model actually existing.
