# Data Cleaning Script — README

A reusable Python script to automatically clean messy CSV/Excel files.
Built for freelance data-cleaning gigs (Fiverr/Upwork) — works on most
real-world "messy sales/customer data" without needing to rewrite the code
for every client.

---

## What's in this folder

| File | Purpose |
|---|---|
| `clean_data.py` | The reusable cleaning script |
| `messy_sales_data.csv` | Sample messy input (for demo/portfolio) |
| `cleaned_sales_data.csv` | Output after running the script on the sample |
| `data_cleaning_report.txt` | Auto-generated before/after summary report |
| `README.md` | This file |

---

## Requirements

- Python 3.8+
- pandas
- openpyxl (only needed if you're cleaning `.xlsx` files)

Install once:
```bash
pip install pandas openpyxl
```

---

## How to run it

```bash
python clean_data.py <input_file> <output_file>
```

Examples:
```bash
python clean_data.py messy_sales_data.csv cleaned_sales_data.csv
python clean_data.py client_data.xlsx client_data_cleaned.xlsx
```

Input and output can be `.csv`, `.xlsx`, or `.xls` — the script auto-detects
the format from the file extension. You can even mix them (e.g. read a
`.xlsx` and save as `.csv`).

After running, you'll get:
1. The cleaned file, saved at the output path you specified
2. `data_cleaning_report.txt` — a before/after summary (row counts, missing
   values per column, duplicates removed) — great to attach when delivering
   work to a client

---

## What it cleans automatically

- **Column names** — strips spaces, lowercases, converts to `snake_case`
  (e.g. `" Customer Name "` → `customer_name`)
- **Whitespace** — trims stray spaces in every text column; normalizes
  blank strings, `"N/A"`, `"none"` etc. to proper missing values
- **Duplicate rows** — removes exact duplicates
- **Currency fields** — strips `$`, `₹`, commas and converts to plain
  numbers (`"$1,200.00"` → `1200.0`)
- **Dates** — parses a mix of formats (`2024-01-05`, `05/01/2024`,
  `08-01-2024`, `2024/01/11`, etc.) into a single consistent `YYYY-MM-DD`
  format. Genuinely invalid dates (like `2099-13-45`) are correctly left
  blank rather than guessed
- **Category/text fields** — standardizes casing to Title Case
  (`"south"` / `"SOUTH"` → `"South"`)
- **Impossible numeric values** — e.g. negative quantities are nulled out
  instead of silently kept
- **Rows missing a key field** (like Order ID) — dropped, since they're not
  usable records
- **Missing values** — filled with sensible defaults where configured
  (e.g. blank customer name → `"Unknown"`)

---

## Customizing for a new client (the important part)

Every dataset is a little different, so at the top of `clean_data.py` there's
a `CONFIG` section you edit — **you never need to touch the logic below it**:

```python
CURRENCY_COLUMNS = ["amount"]              # which columns hold money values
DATE_COLUMNS = ["sale_date"]               # which columns hold dates
CATEGORY_COLUMNS = ["region", "product"]   # which columns to Title Case
NUMERIC_COLUMNS = ["qty"]                  # numeric columns that can't be negative
DROP_ROWS_MISSING_KEY = ["order_id"]       # rows missing these are dropped
FILL_MISSING = {                           # column -> value to fill blanks with
    "customer_name": "Unknown",
    "region": "Unknown",
}
```

**Workflow for a new client file:**
1. Open the file and note the actual column names (the script standardizes
   them to snake_case, so `"Customer Name"` becomes `customer_name` — use
   the *standardized* name in the config)
2. Update the 6 config lists above to match that client's columns
3. Run the script

That's it — no need to rewrite any function.

---

## Using this as a portfolio/gig sample

- `messy_sales_data.csv` and `cleaned_sales_data.csv` are a ready-made
  before/after pair — attach both (or a side-by-side screenshot) to your
  Fiverr/Upwork gig listing
- `data_cleaning_report.txt` doubles as a "proof of work" deliverable —
  it's the kind of summary a client can skim in 10 seconds to see exactly
  what was fixed

---

## Known limitations (be upfront with clients about these)

- Assumes messy data is still in a single flat table (one header row, one
  row per record) — it doesn't fix merged cells or multi-header Excel sheets
- Duplicate detection is exact-match only (won't catch "Rahul Sharma" vs
  "rahul sharma " typo-duplicates on their own — though whitespace/casing
  cleanup often resolves this indirectly for category columns)
- Currency cleaning strips `$` and `₹` — add more symbols in
  `clean_currency()` if a client uses other currencies (`€`, `£`, etc.)
