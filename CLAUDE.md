# CLAUDE.md — Virginia Candidate Explorer

Single-file HTML app that explores Virginia candidates by combining **election
results + campaign finance + voter-file/VAN data**. Client-side only: `index.html`
fetches static JSON from `data/` and renders a filterable/sortable table with a
per-candidate detail modal. Served at `brennertobe07.github.io/va-elections/`.

**Read `docs/REFERENCE.md` before any non-trivial change** — it has the data
schema (`candidates.json` fields), the filter/table/modal feature map, and the
data-refresh notes.

## Quick facts
- **Repo:** `brennertobe07/va-elections` · **Main file:** `index.html` (plain HTML/CSS/JS, light theme, no build step)
- **Data:** `data/candidates.json` (~9 MB, 7,602 records) + `elections/offices/localities/meta.json`. Static export, refreshed periodically.
- **Deploy:** commit + push to `main` → GitHub Pages serves it (root path). ~1-2 min; hard-refresh to bust cache.
- **Data regen:** produced by `export_candidates.py` (per `meta.json`) — not yet in this repo; see the TODO in `docs/REFERENCE.md`.

## ⚠️ Not the same as `Vantage`
`brennertobe07/Vantage` is a *different* project — the **Vantage Election Explorer**
(NCEC targeting, dark theme, vantage.vadems.org). Don't mix the two. See the note
at the top of `docs/REFERENCE.md`.

## Conventions
- Keep it single-file HTML + static `data/` JSON — no build tooling or new deps without asking.
- When architecture/workflow changes, update `docs/REFERENCE.md` in the same task.
