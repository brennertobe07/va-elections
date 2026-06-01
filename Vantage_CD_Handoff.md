# Vantage Election Explorer — CD Functionality Handoff

**Date:** March 23, 2026  
**Purpose:** Add Congressional District (CD) functionality to the Vantage Election Explorer  
**Continuation:** Work in Claude Code on local machine

---

## Project Overview

Vantage is a single-file HTML application displaying NCEC targeting data for Virginia's 2026 election cycle. It currently has filtering and targeting for:
- Counties (133)
- Precincts (2,560)
- House Districts (HD 1-100)
- Senate Districts (SD 1-40)

**What's missing:** Congressional District (CD) functionality

---

## File Locations

| Item | Path |
|------|------|
| **GitHub Repo** | `brennertobe07/Vantage` |
| **Local Repo** | `C:\Users\brenner_tobe\Documents\GitHub\Vantage\` |
| **Main File** | `index.html` |
| **NCEC Source Data** | `va_26_02_17_legislative_ncec_targeting__for_2026_election__with_perfrange26_.xlsx` |

---

## Current State

The app already has the dark "Vantage" theme with:
- DPVA logo (28px height, white bg, rounded corners)
- "Vantage" title in accent blue (#3a8fd4)
- DM Sans / DM Mono fonts
- Dark background (#0f1117)

Features working:
- Dashboard with statewide stats
- Counties tab with drill-down to precincts (click county name → filters precinct tab)
- Precincts tab with County/HD/SD/Performance filters
- Districts tab with HD grid (1-100) and SD grid (1-40)
- Click district → modal with incumbent, stats, precinct list
- Flagging system with localStorage persistence
- Targets tab with export CSV

---

## What Needs to Be Added

### 1. CD Data in Embedded JSON

The NCEC source file has a `cd` column that's NOT currently embedded. Need to add it.

Current embedded columns:
```
summary_level, county, precinct, precinct_code, hd, sd,
expvote26, demperf26, perfrange26, dembase26,
gov25dem2way, pres24dem2way, ltgov25dem2way, ussen24dem2way, ag25dem2way
```

**Add:** `cd` column

### 2. CD Filter on Precincts Tab

Add a CD dropdown filter alongside the existing County/HD/SD/Performance filters.

```html
<div class="filter-group">
    <label>CD:</label>
    <select id="precinctCDFilter" onchange="filterPrecincts()">
        <option value="">All CDs</option>
        <!-- Options 1-11 -->
    </select>
</div>
```

Update `filterPrecincts()` function to include CD filtering.

### 3. CD Section on Districts Tab

Add a third grid section for Congressional Districts (11 buttons, CD 1-11).

Structure to match existing HD/SD sections:
```html
<div class="category-section">
    <h2>Congressional Districts</h2>
    <div class="district-grid" id="cdGrid"></div>
</div>
```

### 4. CD_MEMBERS Constant

Add this JavaScript constant (similar to HOUSE_MEMBERS and SENATE_MEMBERS):

```javascript
const CD_MEMBERS = {
    1:  { name: 'Rob Wittman', party: 'R' },
    2:  { name: 'Jen Kiggans', party: 'R' },
    3:  { name: 'Bobby Scott', party: 'D' },
    4:  { name: 'Jennifer McClellan', party: 'D' },
    5:  { name: 'John McGuire', party: 'R' },
    6:  { name: 'Ben Cline', party: 'R' },
    7:  { name: 'Eugene Vindman', party: 'D' },
    8:  { name: 'Don Beyer', party: 'D' },
    9:  { name: 'Morgan Griffith', party: 'R' },
    10: { name: 'Suhas Subramanyam', party: 'D' },
    11: { name: 'James Walkinshaw', party: 'D' }
};
```

**Party breakdown:** 6 D, 5 R

### 5. CD Grid Rendering

Add function to render CD grid (similar to `renderHDGrid()` and `renderSDGrid()`):

```javascript
function renderCDGrid() {
    const grid = document.getElementById('cdGrid');
    let html = '';
    
    for (let i = 1; i <= 11; i++) {
        const member = CD_MEMBERS[i];
        const partyClass = member.party === 'D' ? 'dem-district' : 'rep-district';
        const flaggedClass = flaggedTargets[`cd-${i}`] ? 'district-flagged' : '';
        
        html += `<button class="district-btn ${partyClass} ${flaggedClass}" 
                         onclick="showCDModal(${i})" 
                         title="${member.name} (${member.party})">
                    CD ${i}
                 </button>`;
    }
    
    grid.innerHTML = html;
}
```

### 6. CD Modal Function

Add `showCDModal(cd)` function (similar to `showHDModal()` and `showSDModal()`):

```javascript
function showCDModal(cd) {
    const member = CD_MEMBERS[cd];
    const cdPrecincts = precinctData.filter(p => p.cd === cd);
    
    // Calculate aggregated stats
    const totalExpVote = cdPrecincts.reduce((sum, p) => sum + (p.expvote26 || 0), 0);
    const avgDemPerf = cdPrecincts.reduce((sum, p) => sum + (p.demperf26 || 0), 0) / cdPrecincts.length;
    const avgPerfRange = cdPrecincts.reduce((sum, p) => sum + (p.perfrange26 || 0), 0) / cdPrecincts.length;
    
    // Build modal content (same structure as HD/SD modals)
    // Include: incumbent box, stats grid, precinct table with flag buttons
    
    // Show modal
    document.getElementById('districtModal').classList.add('active');
}
```

### 7. CD Flagging

Add CD to the flagging system:
- Flag key format: `cd-{n}` (e.g., `cd-7`)
- Update `toggleFlag()` to handle 'cd' type
- Update `renderTargetsList()` to display CD targets
- Update `exportTargets()` to include CD in CSV

### 8. Update Targets Tab

CD targets should appear in the Targets tab alongside counties, precincts, and state districts.

---

## NCEC Data Structure

The source Excel file (`va_26_02_17_legislative_ncec_targeting__for_2026_election__with_perfrange26_.xlsx`) has:

**Sheet:** "NCEC Targeting"

**Key columns:**
| Column | Description |
|--------|-------------|
| `summary_level` | 'STATEWIDE', 'COUNTY', or 'PRECINCT (FULL SPLITS)' |
| `county` | County name |
| `precinct` | Precinct name |
| `precinct_code` | Precinct code |
| `cd` | Congressional District (1-11) - **precinct level only** |
| `hd` | House District (1-100) |
| `sd` | Senate District (1-40) |
| `expvote26` | Expected 2026 turnout |
| `demperf26` | Dem performance composite |
| `perfrange26` | Persuasion/swing range |
| `dembase26` | Dem base floor |

**Note:** CD is only populated at precinct level (counties can span multiple CDs).

**CD distribution across precincts:**
- CD 1: 222 precincts
- CD 2: 225 precincts
- CD 3: 184 precincts
- CD 4: 252 precincts
- CD 5: 306 precincts
- CD 6: 255 precincts
- CD 7: 197 precincts
- CD 8: 172 precincts
- CD 9: 367 precincts
- CD 10: 199 precincts
- CD 11: 181 precincts

**Counties spanning multiple CDs:**
- Albemarle (2 CDs)
- Bedford (3 CDs)
- Chesapeake City (2 CDs)
- Chesterfield (2 CDs)
- Fairfax (3 CDs)
- Hanover (2 CDs)
- Henrico (2 CDs)
- Prince William (2 CDs)
- Roanoke (2 CDs)
- Southampton (2 CDs)

---

## Data Regeneration Script

If you need to re-embed the NCEC data with the CD column:

```python
import pandas as pd
import json

xl = pd.ExcelFile('va_26_02_17_legislative_ncec_targeting__for_2026_election__with_perfrange26_.xlsx')
df = pd.read_excel(xl, sheet_name='NCEC Targeting')

levels_needed = ['STATEWIDE', 'COUNTY', 'PRECINCT (FULL SPLITS)']
df_filtered = df[df['summary_level'].isin(levels_needed)].copy()

# Updated column list - NOW INCLUDES CD
cols = ['summary_level', 'county', 'precinct', 'precinct_code', 'cd', 'hd', 'sd',
        'expvote26', 'demperf26', 'perfrange26', 'dembase26',
        'gov25dem2way', 'pres24dem2way', 'ltgov25dem2way', 'ussen24dem2way', 'ag25dem2way']

df_export = df_filtered[cols].copy()
data_json = df_export.to_json(orient='records')

# Embed into HTML by replacing the NCEC_DATA constant
print(f"Records: {len(df_export)}")
print(data_json[:500])  # Preview
```

---

## Styling Reference

### CSS Variables (already in place)
```css
:root {
    --dem-blue: #2166ac;
    --dem-lt: #74add1;
    --rep-red: #c0392b;
    --rep-lt: #e57368;
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #20243a;
    --border: #2a2d3a;
    --text: #e8eaf0;
    --text-muted: #8890a8;
    --accent: #3a8fd4;
    --radius: 8px;
    --mono: 'DM Mono', monospace;
    --sans: 'DM Sans', sans-serif;
}
```

### District Button Styling (already exists)
```css
.district-btn.dem-district {
    border-left: 3px solid var(--dem-blue);
}

.district-btn.rep-district {
    border-left: 3px solid var(--rep-red);
}

.district-btn.district-flagged {
    background: rgba(243, 156, 18, 0.1);
    border-right: 3px solid var(--warning-amber);
}
```

---

## Testing Checklist

After implementing, verify:

- [ ] CD filter dropdown appears on Precincts tab
- [ ] CD filter correctly filters precinct table
- [ ] CD grid appears on Districts tab with 11 buttons
- [ ] CD buttons show correct party colors (blue left border = D, red = R)
- [ ] Clicking CD button opens modal with incumbent info
- [ ] CD modal shows aggregated stats (ExpVote, DemPerf, Persuasion, precinct count)
- [ ] CD modal shows precinct table for that district
- [ ] CD flag button in modal works
- [ ] Flagged CDs appear in Targets tab
- [ ] Export CSV includes CD targets
- [ ] Clear All removes CD flags

---

## Context Notes

- Virginia's congressional map was challenged but courts denied the change, so current districts remain for 2026 cycle
- This is the key battleground for 2026 - need to target/explore CDs
- Jen Kiggans (CD-2) and Eugene Vindman (CD-7) are likely top targets
- The app is deployed via GitHub Pages at `https://vantage.vadems.org`

---

## Questions for Implementation

1. Should CD aggregations show on the Dashboard tab? (Currently only shows statewide)
2. Should the Counties tab show which CD(s) each county is in? (Some span multiple)
3. Any specific CD-level metrics beyond what's calculated from precincts?

---

## Files to Reference

- Current `index.html` in `C:\Users\brenner_tobe\Documents\GitHub\Vantage\`
- NCEC source data (if re-embedding needed)
- This handoff document
