"""
ap_aging.py — Accounts Payable Aging Report Demo
==================================================
Demonstrates a standard AP aging report:

  1. Load vendor invoice data.
  2. Calculate how many days each invoice is overdue as of the report date.
  3. Bucket invoices into standard aging periods:
       Current (not yet due), 1–30 days, 31–60 days, 61–90 days, 90+ days.
  4. Generate:
     - A Markdown aging report  → ``reports/ap_aging_report.md``
     - A stacked-bar chart PNG  → ``reports/figures/ap_aging_chart.png``

Usage
-----
    python -m modules.ap_aging.ap_aging
    # or
    python modules/ap_aging/ap_aging.py
"""

from __future__ import annotations

import os
from datetime import date

import pandas as pd
import matplotlib
matplotlib.use("Agg")   # non-interactive backend for CI / headless environments
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

DATA_DIR = os.path.join(_ROOT, "data")
REPORTS_DIR = os.path.join(_ROOT, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

INVOICE_FILE = os.path.join(DATA_DIR, "ap_invoices.csv")
REPORT_FILE = os.path.join(REPORTS_DIR, "ap_aging_report.md")
CHART_FILE = os.path.join(FIGURES_DIR, "ap_aging_chart.png")

# Report "as-of" date — use a fixed date so the report is deterministic
REPORT_DATE = date(2024, 2, 1)

BUCKETS = ["Current", "1-30 Days", "31-60 Days", "61-90 Days", "90+ Days"]


def load_invoices() -> pd.DataFrame:
    df = pd.read_csv(INVOICE_FILE, parse_dates=["invoice_date", "due_date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def classify_aging(df: pd.DataFrame, report_date: date) -> pd.DataFrame:
    df = df.copy()
    df["days_overdue"] = (pd.Timestamp(report_date) - df["due_date"]).dt.days

    def bucket(days):
        if days <= 0:
            return "Current"
        elif days <= 30:
            return "1-30 Days"
        elif days <= 60:
            return "31-60 Days"
        elif days <= 90:
            return "61-90 Days"
        else:
            return "90+ Days"

    df["aging_bucket"] = df["days_overdue"].apply(bucket)
    return df


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("aging_bucket")["amount"]
        .agg(count="count", total="sum")
        .reindex(BUCKETS)
        .fillna(0)
        .astype({"count": int})
    )
    summary["total"] = summary["total"].round(2)
    return summary


def build_report(df: pd.DataFrame, summary: pd.DataFrame) -> str:
    total_owing = summary["total"].sum()

    # Format detail table
    detail_cols = ["invoice_id", "vendor", "invoice_date", "due_date", "amount", "days_overdue", "aging_bucket"]
    detail = df[detail_cols].copy()
    detail["amount"] = detail["amount"].apply(lambda x: f"${x:,.2f}")
    detail["invoice_date"] = detail["invoice_date"].dt.strftime("%Y-%m-%d")
    detail["due_date"] = detail["due_date"].dt.strftime("%Y-%m-%d")
    detail_md = detail.to_markdown(index=False)

    # Format summary table
    sum_display = summary.reset_index().rename(columns={
        "aging_bucket": "Aging Bucket", "count": "# Invoices", "total": "Total Owing ($)"
    })
    sum_display["Total Owing ($)"] = sum_display["Total Owing ($)"].apply(lambda x: f"${x:,.2f}")
    sum_md = sum_display.to_markdown(index=False)

    lines = [
        "# Accounts Payable Aging Report",
        f"**As of:** {REPORT_DATE.strftime('%B %d, %Y')}  ",
        f"**Prepared:** {date.today().isoformat()}  ",
        f"**Status:** ✅ Demonstration — Synthetic Data Only",
        "",
        "---",
        "",
        "## Summary by Aging Bucket",
        "",
        sum_md,
        "",
        f"**Total AP Outstanding: ${total_owing:,.2f}**",
        "",
        "---",
        "",
        "## Invoice Detail",
        "",
        detail_md,
        "",
        "---",
        "",
        f"![AP Aging Chart](figures/ap_aging_chart.png)",
        "",
        "> **Note:** This report uses synthetic (fictional) data for portfolio demonstration purposes.",
    ]
    return "\n".join(lines) + "\n"


def build_chart(summary: pd.DataFrame):
    os.makedirs(FIGURES_DIR, exist_ok=True)

    colors = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c", "#8e44ad"]
    fig, ax = plt.subplots(figsize=(8, 5))

    totals = summary["total"].values
    buckets = summary.index.tolist()

    bars = ax.bar(buckets, totals, color=colors, edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, labels=[f"${v:,.0f}" for v in totals], padding=4, fontsize=9)

    ax.set_title("AP Aging — Outstanding Balances by Bucket", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Aging Bucket", fontsize=11)
    ax.set_ylabel("Amount ($)", fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"📊 Chart saved to: {CHART_FILE}")


def run():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    df = load_invoices()
    df = classify_aging(df, REPORT_DATE)
    summary = build_summary(df)

    report_text = build_report(df, summary)
    with open(REPORT_FILE, "w", encoding="utf-8") as fh:
        fh.write(report_text)
    print(f"✅ AP aging report written to: {REPORT_FILE}")

    build_chart(summary)

    total = summary["total"].sum()
    overdue = summary.loc[summary.index != "Current", "total"].sum()
    print(f"   Total AP outstanding : ${total:,.2f}")
    print(f"   Total overdue (>0d)  : ${overdue:,.2f}")


if __name__ == "__main__":
    run()
