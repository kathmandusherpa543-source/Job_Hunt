# Accounting Job Hunt & Market Insights (Canada)
### Accounting Workflow Automation Portfolio

> **Scope:** Entry-level & Intermediate accounting roles — Toronto / GTA / Ontario / Canada

This project markets the repository owner as a **Business Administration (Accounting)** candidate and demonstrates practical accounting skills through automated job-market analysis and accounting workflow mini-modules built in Python.

---

## Target Roles

| Role | Seniority |
|---|---|
| Junior Accountant | Entry / Intermediate |
| Accounting Assistant | Entry |
| AP Clerk / AR Clerk | Entry |
| Bookkeeper | Entry / Intermediate |
| Payroll Assistant / Payroll Administrator | Entry / Intermediate |
| Accounting Clerk / Coordinator | Entry |
| Junior Financial Analyst | Entry / Intermediate |

**Seniority scope:** Entry-level and Intermediate **only**.  
Roles with titles containing *Senior, Manager, Director, Lead, Principal, Controller, VP* are automatically excluded.

---

## Target Locations

- Toronto, Ontario (primary)
- Mississauga / Brampton / Vaughan / Markham (GTA)
- Ontario-wide
- Canada-wide

---

## What This Project Demonstrates

### Job Market Analysis
- Automated scraping of accounting postings from Indeed & LinkedIn.
- Configurable seniority filter that excludes over-qualified roles.
- Summary reports showing counts by location, role category, and top in-demand skills (Excel, QuickBooks, reconciliation, month-end, HST/GST, etc.).

### Accounting Workflow Automation (Work Samples)
| Module | Task Demonstrated | Output |
|---|---|---|
| `modules/bank_reconciliation/` | Bank-to-GL cash reconciliation | `reports/bank_reconciliation_report.md` |
| `modules/ap_aging/` | AP Aging buckets (0-30, 31-60, 61-90, 90+) | `reports/ap_aging_report.md` + chart |
| `modules/budget_variance/` | Budget vs Actual variance analysis | `reports/budget_variance_report.md` + chart |

All work-sample modules use **synthetic (fictional) data only**. No real financial data is included.

---

## Repository Structure

```
Job_Hunt/
├── config.yaml                      # Configurable: locations, keywords, seniority rules
├── job_scraper.py                   # Main scraper (Indeed + LinkedIn -> Google Sheets)
├── seniority_filter.py              # Standalone seniority filter module
├── spam_filters.py                  # Title / company / description spam lists
├── requirements.txt
├── Makefile                         # One-command runner
│
├── data/                            # Synthetic CSV inputs for work-sample modules
│   ├── bank_statement.csv
│   ├── gl_cash_ledger.csv
│   ├── ap_invoices.csv
│   └── budget_vs_actual.csv
│
├── modules/
│   ├── bank_reconciliation/
│   │   └── bank_recon.py
│   ├── ap_aging/
│   │   └── ap_aging.py
│   └── budget_variance/
│       └── budget_variance.py
│
├── reports/
│   ├── generate_reports.py          # Runs all report modules
│   ├── job_market_summary.md        # Generated: job market overview
│   ├── bank_reconciliation_report.md
│   ├── ap_aging_report.md
│   ├── budget_variance_report.md
│   └── figures/                     # Generated PNG charts
│
└── tests/
    ├── test_seniority_filter.py
    └── test_reports.py
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate all reports (one command)
```bash
make reports
# or
python reports/generate_reports.py
```

This produces:
- `reports/job_market_summary.md`
- `reports/bank_reconciliation_report.md`
- `reports/ap_aging_report.md`
- `reports/budget_variance_report.md`
- `reports/figures/*.png`

### 3. Run individual accounting modules
```bash
make bank-recon
make ap-aging
make budget-variance
```

### 4. Run tests
```bash
make test
# or
pytest tests/ -v
```

### 5. Run the live job scraper (requires Google Sheets + email secrets)
```bash
python job_scraper.py
```

---

## Configuration (`config.yaml`)

Edit `config.yaml` to customize without touching Python code:

```yaml
# Locations to search
locations:
  - Toronto, Ontario
  - Ontario
  - Canada

# Accounting role keywords
search_terms:
  - Junior Accountant
  - AP Clerk
  - Bookkeeper
  ...

# Seniority filter — automatically applied during cleaning
seniority:
  include_terms:   [junior, entry, intermediate, assistant, clerk, ...]
  exclude_terms:   [senior, manager, director, lead, principal, controller, ...]
```

---

## Seniority Filter

The `seniority_filter.py` module provides configurable, case-insensitive filtering:

```python
from seniority_filter import apply_seniority_filter

# Filter a DataFrame — keeps only entry/intermediate titles
df_filtered = apply_seniority_filter(df, exclude_terms=[...])
```

**Excluded by default:** Senior, Manager, Director, Lead, Principal, Controller, VP, Supervisor, Head of, Chief, Executive.  
**"Intermediate" is explicitly included** — aligned with the entry/intermediate target scope.

---

## Live Scraper Setup (Google Sheets + Email)

The GitHub Actions workflow (`.github/workflows/scrape.yml`) runs daily at ~8 AM Toronto time.

### Required GitHub Secrets
| Secret | Description |
|---|---|
| `GSHEETS_CREDS_JSON` | Full JSON content of your Google service account key |
| `SHEET_URL` | Your Google Sheet URL |
| `GMAIL_USER` | Sender Gmail address |
| `MAIL_APP_PASSWORD` | Gmail App Password (16 chars, no spaces) |
| `TO_EMAIL` | Recipient email for completion notifications |

### Local Setup
```bash
# Create a .env file with:
SHEET_URL=https://docs.google.com/spreadsheets/d/<ID>/edit
GSHEETS_CREDS_PATH=service_account.json
GMAIL_USER=your@gmail.com
MAIL_APP_PASSWORD=yourapppassword
TO_EMAIL=notify@example.com
```

---

## Skills Demonstrated

- **Python:** pandas, matplotlib, data cleaning, report generation
- **Accounting:** bank reconciliation, AP aging, budget variance analysis
- **Automation:** scheduled GitHub Actions workflow, Google Sheets integration
- **Data Analysis:** keyword extraction, job market trend analysis
- **Tools:** Excel-compatible CSV outputs, Markdown reports, PNG charts
