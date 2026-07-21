"""
clean_data.py
A reusable CSV/Excel cleaning script for freelance data-cleaning gigs.

USAGE:
    python clean_data.py input_file.csv output_file.csv

WHAT IT DOES (fully automatic):
    1. Loads CSV or Excel (auto-detects by extension)
    2. Standardizes column names (strips spaces, lowercase, snake_case)
    3. Strips whitespace from all text/object columns
    4. Removes exact duplicate rows
    5. Standardizes casing in categorical/text columns (Title Case)
    6. Cleans currency columns (removes $, ₹, commas -> converts to float)
    7. Parses inconsistent date formats into a single standard format (YYYY-MM-DD)
    8. Flags/removes impossible values (negative quantities, invalid dates)
    9. Handles missing values with sensible defaults (configurable)
    10. Generates a before/after summary report (data_cleaning_report.txt)

You can tweak the CONFIG section below per client/project without touching
the core logic.
"""

import pandas as pd
import numpy as np
import re
import sys
from datetime import datetime

# ============================================================
# CONFIG — tweak these per client/gig
# ============================================================
CURRENCY_COLUMNS = ["amount"]          # columns that hold money values
DATE_COLUMNS = ["sale_date"]           # columns that hold dates
CATEGORY_COLUMNS = ["region", "product"]  # columns to Title Case
NUMERIC_COLUMNS = ["qty"]              # columns that should be numeric, >= 0
DROP_ROWS_MISSING_KEY = ["order_id"]   # rows missing these are dropped entirely
FILL_MISSING = {                       # column -> fill strategy
    "customer_name": "Unknown",
    "region": "Unknown",
}
# ============================================================


def standardize_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
    )
    return df


def strip_whitespace(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": np.nan, "N/A": np.nan, "": np.nan, "none": np.nan})
    return df


def clean_currency(df, columns):
    for col in columns:
        if col not in df.columns:
            continue
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[₹$,]", "", regex=True)
            .str.strip()
            .replace({"nan": np.nan, "N/A": np.nan, "": np.nan})
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _parse_single_date(value):
    if pd.isna(value):
        return pd.NaT
    value = str(value).strip()
    # try a list of common real-world formats, in order
    formats = [
        "%Y-%m-%d", "%Y/%m/%d",
        "%d-%m-%Y", "%d/%m/%Y",
        "%m-%d-%Y", "%m/%d/%Y",
        "%d-%b-%Y", "%d %b %Y", "%d %B %Y",
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(value, format=fmt)
        except ValueError:
            continue
    # last resort: let pandas guess (may still fail -> NaT, which is correct
    # for garbage/impossible dates like "2099-13-45")
    return pd.to_datetime(value, errors="coerce")


def parse_dates(df, columns):
    for col in columns:
        if col not in df.columns:
            continue
        df[col] = df[col].apply(_parse_single_date)
    return df


def title_case_columns(df, columns):
    for col in columns:
        if col not in df.columns:
            continue
        df[col] = df[col].astype(str).str.strip().str.title()
        df[col] = df[col].replace({"Nan": np.nan})
    return df


def clean_numeric(df, columns):
    for col in columns:
        if col not in df.columns:
            continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # negative values in a "quantity" column are impossible -> null them out
        df.loc[df[col] < 0, col] = np.nan
    return df


def drop_invalid_rows(df, key_columns):
    for col in key_columns:
        if col in df.columns:
            df = df[df[col].notna()]
    return df


def fill_missing(df, fill_map):
    for col, value in fill_map.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)
    return df


def load_file(path):
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def save_file(df, path):
    if path.lower().endswith((".xlsx", ".xls")):
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False)


def generate_report(before, after, before_missing, after_missing, dupes_removed, report_path):
    lines = []
    lines.append("DATA CLEANING REPORT")
    lines.append("=" * 50)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"Rows before cleaning : {before}")
    lines.append(f"Rows after cleaning  : {after}")
    lines.append(f"Duplicate rows removed: {dupes_removed}")
    lines.append(f"Rows removed (missing key fields): {before - after - dupes_removed if before - after - dupes_removed > 0 else 0}")
    lines.append("")
    lines.append("Missing values BEFORE cleaning (per column):")
    lines.append(before_missing.to_string())
    lines.append("")
    lines.append("Missing values AFTER cleaning (per column):")
    lines.append(after_missing.to_string())
    lines.append("")
    lines.append("=" * 50)
    lines.append("Cleaning steps applied:")
    lines.append("- Standardized column names")
    lines.append("- Stripped whitespace, normalized blank/N-A markers to NaN")
    lines.append("- Removed exact duplicate rows")
    lines.append("- Cleaned currency fields (removed $/₹/commas, converted to numeric)")
    lines.append("- Parsed inconsistent date formats to YYYY-MM-DD")
    lines.append("- Title-cased category fields (region, product) for consistency")
    lines.append("- Nulled out impossible numeric values (e.g. negative quantities)")
    lines.append("- Dropped rows missing critical key fields (e.g. order_id)")
    lines.append("- Filled missing values with sensible defaults where configured")

    report = "\n".join(lines)
    with open(report_path, "w") as f:
        f.write(report)
    return report


def main(input_path, output_path):
    df = load_file(input_path)
    before_rows = len(df)

    df = standardize_column_names(df)
    df = strip_whitespace(df)

    before_missing = df.isna().sum()

    rows_before_dedup = len(df)
    df = df.drop_duplicates()
    dupes_removed = rows_before_dedup - len(df)

    df = clean_currency(df, CURRENCY_COLUMNS)
    df = parse_dates(df, DATE_COLUMNS)
    df = title_case_columns(df, CATEGORY_COLUMNS)
    df = clean_numeric(df, NUMERIC_COLUMNS)
    df = drop_invalid_rows(df, DROP_ROWS_MISSING_KEY)
    df = fill_missing(df, FILL_MISSING)

    after_rows = len(df)
    after_missing = df.isna().sum()

    save_file(df, output_path)

    report_path = "data_cleaning_report.txt"
    report = generate_report(before_rows, after_rows, before_missing, after_missing, dupes_removed, report_path)

    print(report)
    print(f"\nCleaned file saved to: {output_path}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_data.py <input_file> <output_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
