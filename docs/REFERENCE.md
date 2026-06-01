# Virginia Candidate Explorer — Reference Document

**Project:** Searchable explorer of Virginia candidates combining election results,
campaign finance, and voter-file/VAN data — DPVA.

---

## Overview

A single-file HTML app (`index.html`) that loads five JSON files from `data/` in
the browser and presents a filterable, sortable table of Virginia candidates with
a per-candidate detail modal. No server/API — everything runs client-side; the
JSON is a static export refreshed periodically.

---

## ⚠️ Not to be confused with `Vantage`

Two similarly-themed repos exist:

- **`brennertobe07/va-elections`** (THIS repo) — the **Virginia Candidate Explorer**
  (candidate results + finance + voter-file data). Served at
  `brennertobe07.github.io/va-elections/` (no custom domain).
- **`brennertobe07/Vantage`** — a *different* project: the **Vantage Election
  Explorer** (NCEC targeting), custom domain **vantage.vadems.org**.

A stray copy of the Vantage app once lived here and caused confusion; it has been
removed. Vantage work does NOT go in this repo.

---

## File Locations

- **Repo:** `brennertobe07/va-elections`
- **Local Path:** `C:\Users\brenner_tobe\Documents\GitHub\va-elections\`
- **Main File:** `index.html` (the Candidate Explorer; loads `data/`)
- **Deploy:** GitHub Pages, source `main` / root → `brennertobe07.github.io/va-elections/`

---

## Architecture

`index.html` is plain HTML/CSS/JS (Open Sans, light theme — note this is a
*different* look from the Vantage dark theme). On load it `fetch`es all five
`data/*.json` files in parallel (`loadData()`), then renders.

### Data files (`data/`)
| File | Records | Purpose / key fields |
|------|---------|----------------------|
| `candidates.json` | 7,602 | The main dataset (≈9 MB). One row per candidate-election summary. See schema below. |
| `elections.json` | 84 | `ElectionDate`, `ElectionName`, `ElectionYear` — populates the Year filter. |
| `offices.json` | 163 | `OfficeSoughtName`, `OfficeType`, `CandidateCount` — populates the Office filter (with counts). |
| `localities.json` | 152 | `LocalityName`, `CandidateCount` — populates the Locality filter. |
| `meta.json` | — | Summary stats + `LastRefreshDate` + `ExportedBy` — shown in the header meta bar. |

### `candidates.json` record schema
Identity / election: `SummaryId` (modal key), `CandidateFullName` (+ First/Middle/Last/Suffix),
`CommitteeCode`, `CommitteeName`, `CandidateId`, `ElectionDate`, `ElectionName`,
`OfficeSoughtName`, `OfficeType` (State/Local), `OfficeGroup`, `LocalityName`,
`DistrictName`, `PoliticalPartyName`, `PartyCode`, `TotalVotes`, `Won`.

Campaign finance: `ContributionCount`, `TotalAmount`, `MaxAmount`, `AvgAmount`,
`FirstContribDate`, `LastContribDate`, `LastDType`, `HasFedContrib`,
`HasStateContrib`, `HasDPVAContrib`, `HasABContrib` (ActBlue).

Voter file / VAN: `StateFileID`, `VoterRegistrationid` (VAN ID), `LikelyParty`
(`SD`/`SR` = modeled Dem/Rep), `DNCDemPartySupport` (0-100 support score),
`VAN_MatchStatus`.

Districts: `Current_CD` + `Current_CD_Member` + `Current_CD_Party`, `New_CD`
(proposed), `SD` + `SD_Member` + `SD_Party`, `HD` + `HD_Member` + `HD_Party`,
`District_MatchStatus`, `RefreshDate`.

---

## Features

- **Filter panel:** free-text search (name/office/locality/committee/district),
  Election Year, Office Type (State/Local), Office Group (Governor, HoD, BOS,
  School Board, Sheriff, …), specific Office, Locality, Party, Result
  (Winners/Non-winners).
- **Table:** sortable columns (Candidate, Election, Office, Locality, Votes,
  Total Raised); party badge (with modeled-party fallback via `LikelyParty`),
  Won marker, Dem-support bar, CD/SD/HD district tags. **Capped at 500 rows** —
  footer prompts to narrow filters when more match.
- **Detail modal** (click a row → by `SummaryId`): four sections — Election,
  Campaign Finance, Voter File, Districts (incl. current + proposed CD and
  HD/SD members & parties). Esc or overlay click closes.

---

## Data Regeneration

The JSON in `data/` is a static export. `meta.json` records `ExportedBy:
export_candidates.py` and `LastRefreshDate`. The export combines SBE election
results, campaign-finance, and voter-file/VAN district data (per the candidate
schema above) — almost certainly a SQL Server → JSON export in Brenner's Python
tooling.

> **TODO:** `export_candidates.py` is not committed to this repo and was not found
> by name under `C:\Scripts\Python` during setup. Confirm its location and, if
> useful, vendor it (or a pointer to it) into this repo so refreshes are
> reproducible. To refresh the site: regenerate the five `data/*.json` files, then
> commit + push.

---

## Deployment Workflow

Deploy model: commit the JSON/`index.html` → GitHub Pages serves it (`main`, root).

1. Refresh `data/*.json` if the underlying data changed (see above)
2. Commit and push to `main`
3. Site updates at `brennertobe07.github.io/va-elections/` within 1-2 min
   (hard-refresh to bypass browser cache)

---

## Notes
- Single-file `index.html` + static `data/` JSON. No build step, no dependencies
  beyond a Google Fonts stylesheet.
- `candidates.json` is ~9 MB; the 500-row render cap keeps the table responsive.
- Light theme here is intentional and distinct from the Vantage dark theme.
