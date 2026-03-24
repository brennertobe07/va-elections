# Vantage Election Explorer — Reference Document

**Created:** March 23, 2026  
**Project:** NCEC Targeting Data Explorer for Virginia Elections

---

## Overview

Vantage is a single-file HTML application that displays NCEC targeting data for Virginia's 2026 election cycle. It provides interactive exploration of statewide, county, and precinct-level Democratic performance metrics, with district overlays and a targeting/flagging system.

**Live URL:** https://vantage.vadems.org

---

## File Locations

### GitHub Repository
- **Repo:** `brennertobe07/Vantage`
- **Local Path:** `C:\Users\brenner_tobe\Documents\GitHub\Vantage\`
- **Main File:** `index.html`

### Source Data
- **NCEC Targeting File:** `va_26_02_17_legislative_ncec_targeting__for_2026_election__with_perfrange26_.xlsx`
- **Sheet:** "NCEC Targeting"
- **Records:** 2,694 total (1 statewide, 133 counties, 2,560 precincts)

---

## App Features

### Tabs
1. **Dashboard** — Statewide stats (ExpVote, DemPerf, Persuasion, DemBase), performance distribution bar chart, recent race results
2. **Counties** — 133 counties, searchable/filterable by performance category, sortable columns, flag button
   - **Drill-down:** Click county name → switches to Precincts tab filtered to that county
3. **Precincts** — 2,560 precincts, filter by County + HD + SD + Performance category
4. **Districts** — HD grid (1-100) + SD grid (1-40), color-coded by party
   - Click any district → Modal popup with incumbent info, stats, and precinct list
5. **Targets** — All flagged items, Mobilize/Persuade tags, Export CSV, Clear All

### Flagging System
- Counties: key = `county-{name}`
- Precincts: key = `precinct-{county}-{precinct_code}`
- Districts: key = `hd-{n}` or `sd-{n}`
- Stored in browser localStorage (device-specific)

### Incumbent Data (Embedded)
- **HOUSE_MEMBERS:** All 100 House Delegates with name and party
- **SENATE_MEMBERS:** All 40 State Senators with name and party
- Notable: HD 98 = VACANT (Barry Knight died Feb 2026), SD 39 = Elizabeth Bennett-Parker (D, new Feb 2026)

---

## NCEC Metrics

| Field | Description |
|-------|-------------|
| `demperf26` | Weighted composite Democratic performance (proprietary NCEC) |
| `perfrange26` | Persuasion/swing voter range |
| `dembase26` | Democratic base floor |
| `expvote26` | Expected 2026 turnout |
| `gov25dem2way` | Governor 2025 Dem two-way % |
| `pres24dem2way` | President 2024 Dem two-way % |
| `ltgov25dem2way` | Lt Governor 2025 Dem two-way % |
| `ussen24dem2way` | US Senate 2024 Dem two-way % |
| `ag25dem2way` | Attorney General 2025 Dem two-way % |

### Performance Categories
| Cat | Label | Dem Performance |
|-----|-------|-----------------|
| 1 | Strong Dem | 70%+ |
| 2 | Lean Dem | 60-70% |
| 3 | Tilt Dem | 55-60% |
| 4 | Comp Dem | 50-55% |
| 5 | Comp Rep | 45-50% |
| 6 | Tilt Rep | 40-45% |
| 7 | Lean Rep | 30-40% |
| 8 | Strong Rep | <30% |

---

## Styling / Branding

Vantage uses the DPVA dark theme (same as Absentee Dashboard):

### Fonts
- **UI:** DM Sans (Google Fonts)
- **Numbers:** DM Mono (Google Fonts)

### Colors
| Variable | Value | Usage |
|----------|-------|-------|
| `--bg` | #0f1117 | Page background |
| `--surface` | #1a1d27 | Card/panel background |
| `--surface2` | #20243a | Secondary surface |
| `--border` | #2a2d3a | Borders |
| `--text` | #e8eaf0 | Main text |
| `--text-muted` | #8890a8 | Muted/secondary text |
| `--accent` | #3a8fd4 | Accent blue (links, active tabs, "Vantage" title) |
| `--dem-blue` | #2166ac | Democratic indicators |
| `--dem-lt` | #74add1 | Democratic light |
| `--rep-red` | #c0392b | Republican indicators |
| `--rep-lt` | #e57368 | Republican light |

### Logo
- VA Dems logo (base64 embedded)
- Style: `height:28px; background:#fff; border-radius:4px; padding:2px 6px;`

---

## Related Dashboards (Same Branding)

### Absentee Tracker
- **URL:** (April Referendum dashboard)
- **Repo:** `brennertobe07/april-referendum-absentee`
- **Local Path:** `C:\Scripts\Python\Python_Absentee\April\april-referendum-absentee\`

### Cure Dashboard
- **Local Path:** (cure tracking dashboard)
- Uses same logo/header styling

---

## Deployment Workflow

1. Edit `index.html` locally in `C:\Users\brenner_tobe\Documents\GitHub\Vantage\`
2. Open **GitHub Desktop**
3. Commit changes
4. Push to GitHub
5. Site updates automatically within 1-2 minutes

---

## Data Regeneration (if needed)

If NCEC data needs to be re-embedded:

```python
import pandas as pd, json

xl = pd.ExcelFile('va_26_02_17_legislative_ncec_targeting__for_2026_election__with_perfrange26_.xlsx')
df = pd.read_excel(xl, sheet_name='NCEC Targeting')

levels_needed = ['STATEWIDE', 'COUNTY', 'PRECINCT (FULL SPLITS)']
df_filtered = df[df['summary_level'].isin(levels_needed)].copy()

cols = ['summary_level', 'county', 'precinct', 'precinct_code', 'hd', 'sd',
        'expvote26', 'demperf26', 'perfrange26', 'dembase26',
        'gov25dem2way', 'pres24dem2way', 'ltgov25dem2way', 'ussen24dem2way',
        'ag25dem2way', 'gov21dem2way', 'pres20dem2way']

df_export = df_filtered[cols].copy()
data_json = df_export.to_json(orient='records')

# Embed into HTML template replacing the NCEC_DATA constant
```

---

## Version History

| Date | Version | Notes |
|------|---------|-------|
| Mar 2026 | v1 (blue) | Original DPVA blue theme |
| Mar 2026 | v2 (Vantage) | Dark theme rebrand, logo, drill-down from counties |

---

## Notes

- Single-file HTML — all data, CSS, and JS embedded
- No server/API required — runs entirely in browser
- Flags persist in localStorage (browser/device specific)
- Export produces CSV with all flagged targets and their metrics
