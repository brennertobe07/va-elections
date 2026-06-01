"""
embed_ncec_data.py — Regenerate the embedded NCEC_DATA array in index.html.

Reads the NCEC targeting workbook, filters to the three summary levels the
Vantage app uses (STATEWIDE / COUNTY / PRECINCT FULL SPLITS), selects the
columns the app expects, and replaces the single `const NCEC_DATA = [...]`
line in index.html with the regenerated JSON.

Run this whenever the NCEC source data refreshes. It edits index.html in place
(writing index.html.bak first) and prints a verification summary.

Usage:
    python embed_ncec_data.py
"""

import json
import re
from pathlib import Path

import pandas as pd

# --- Config -----------------------------------------------------------------
XLSX_PATH = Path(
    r"C:\Temp\NCEC 2026"
    r"\va_26.02.17_legislative_ncec_targeting (for 2026 election, with perfrange26).xlsx"
)
SHEET = "NCEC Targeting"
HTML_PATH = Path(__file__).with_name("index.html")

LEVELS = ["STATEWIDE", "COUNTY", "PRECINCT (FULL SPLITS)"]

# Column order embedded in the app. `cd` sits right after precinct_code.
# gov21dem2way / pres20dem2way are historical columns the app already uses —
# keep them.
COLS = [
    "summary_level", "county", "precinct", "precinct_code",
    "cd",
    "hd", "sd",
    "expvote26", "demperf26", "perfrange26", "dembase26",
    "gov25dem2way", "pres24dem2way", "ltgov25dem2way", "ussen24dem2way",
    "ag25dem2way", "gov21dem2way", "pres20dem2way",
]

# District columns (cd/hd/sd) are float64 in the source with NaN on non-precinct
# rows. to_json renders them as e.g. 2.0 and writes NaN as null — which matches
# how hd/sd were already embedded, and parses to the JS number 2. No casting
# needed; left as-is for byte-compatibility with the existing embed.


def build_json() -> str:
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET)

    missing = [c for c in COLS if c not in df.columns]
    if missing:
        raise SystemExit(f"Source workbook is missing expected columns: {missing}")

    df = df[df["summary_level"].isin(LEVELS)].copy()
    df = df[COLS]

    # double_precision=10 matches the precision already in index.html
    data_json = df.to_json(orient="records", double_precision=10)

    # Verification summary
    n_pre = int((df["summary_level"] == "PRECINCT (FULL SPLITS)").sum())
    cd_counts = (
        df.loc[df["summary_level"] == "PRECINCT (FULL SPLITS)", "cd"]
        .value_counts()
        .sort_index()
        .to_dict()
    )
    print(f"Records embedded : {len(df)}")
    print(f"  STATEWIDE      : {int((df['summary_level'] == 'STATEWIDE').sum())}")
    print(f"  COUNTY         : {int((df['summary_level'] == 'COUNTY').sum())}")
    print(f"  PRECINCT       : {n_pre}")
    print(f"Precinct CD dist : {cd_counts}")
    return data_json


def replace_in_html(data_json: str) -> None:
    text = HTML_PATH.read_text(encoding="utf-8")

    # Match the whole `const NCEC_DATA = [...];` statement (single line),
    # preserving its leading indentation.
    pattern = re.compile(
        r"(?P<indent>[ \t]*)const NCEC_DATA = \[.*?\];",
        re.DOTALL,
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise SystemExit(
            f"Expected exactly one NCEC_DATA declaration, found {len(matches)}."
        )

    indent = matches[0].group("indent")
    replacement = f"{indent}const NCEC_DATA = {data_json};"

    HTML_PATH.with_suffix(".html.bak").write_text(text, encoding="utf-8")
    new_text = text[: matches[0].start()] + replacement + text[matches[0].end():]
    HTML_PATH.write_text(new_text, encoding="utf-8")
    print(f"Wrote {HTML_PATH.name} (backup: {HTML_PATH.name}.bak)")


if __name__ == "__main__":
    replace_in_html(build_json())
