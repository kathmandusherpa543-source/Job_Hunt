"""
budget_variance.py — Budget vs Actual Variance Analysis Demo
=============================================================
Demonstrates a month-end budget-vs-actual variance analysis:

  1. Load department budget and actual spend data.
  2. Calculate variance (Actual – Budget) and variance %.
  3. Flag significant variances (|variance %| > threshold).
  4. Generate:
     - Markdown variance report  → ``reports/budget_variance_report.md``
     - Bar chart PNG             → ``reports/figures/budget_variance_chart.png``

Usage
-----
    python -m modules.budget_variance.budget_variance
    # or
    python modules/budget_variance/budget_variance.py
"""

from __future__ import annotations

import os
from datetime import date

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

DATA_DIR = os.path.join(_ROOT, "data")
REPORTS_DIR = os.path.join(_ROOT, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

BUDGET_FILE = os.path.join(DATA_DIR, "budget_vs_actual.csv")
REPORT_FILE = os.path.join(REPORTS_DIR, "budget_variance_report.md")
CHART_FILE = os.path.join(FIGURES_DIR, "budget_variance_chart.png")

REPORT_PERIOD = "January 2024"
VARIANCE_FLAG_PCT = 10.0   # flag variances larger than ±10 %


def load_data() -> pd.DataFrame:
    df = pd.read_csv(BUDGET_FILE)
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce").fillna(0)
    df["actual"] = pd.to_numeric(df["actual"], errors="coerce").fillna(0)
    return df


def calculate_variance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["variance"] = df["actual"] - df["budget"]
    df["variance_pct"] = df.apply(
        lambda r: (r["variance"] / r["budget"] * 100) if r["budget"] != 0 else 0.0,
        axis=1,
    ).round(1)
    df["flag"] = df["variance_pct"].abs() > VARIANCE_FLAG_PCT
    df["flag_label"] = df["flag"].map({True: "⚠️", False: ""})
    return df


def department_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("department")[["budget", "actual", "variance"]]
        .sum()
        .assign(
            variance_pct=lambda d: (d["variance"] / d["budget"] * 100).round(1)
        )
        .reset_index()
    )


def build_report(df: pd.DataFrame, dept_summary: pd.DataFrame) -> str:
    total_budget = df["budget"].sum()
    total_actual = df["actual"].sum()
    total_variance = total_actual - total_budget
    total_variance_pct = (total_variance / total_budget * 100) if total_budget else 0

    # Top 5 variance drivers (by absolute $ variance)
    top5 = df.iloc[df["variance"].abs().nlargest(5).index].head(5)

    # Detail table
    detail = df[["department", "category", "budget", "actual", "variance", "variance_pct", "flag_label"]].copy()
    for col in ["budget", "actual", "variance"]:
        detail[col] = detail[col].apply(lambda x: f"${x:,.2f}")
    detail["variance_pct"] = detail["variance_pct"].apply(lambda x: f"{x:+.1f}%")
    detail = detail.rename(columns={"flag_label": "Flag"})
    detail_md = detail.to_markdown(index=False)

    # Dept summary table
    dept_disp = dept_summary.copy()
    for col in ["budget", "actual", "variance"]:
        dept_disp[col] = dept_disp[col].apply(lambda x: f"${x:,.2f}")
    dept_disp["variance_pct"] = dept_disp["variance_pct"].apply(lambda x: f"{x:+.1f}%")
    dept_md = dept_disp.to_markdown(index=False)

    # Top 5 table
    top5_disp = top5[["department", "category", "budget", "actual", "variance", "variance_pct"]].copy()
    for col in ["budget", "actual", "variance"]:
        top5_disp[col] = top5_disp[col].apply(lambda x: f"${x:,.2f}")
    top5_disp["variance_pct"] = top5_disp["variance_pct"].apply(lambda x: f"{x:+.1f}%")
    top5_md = top5_disp.to_markdown(index=False)

    variance_symbol = "over" if total_variance > 0 else "under"

    lines = [
        "# Budget vs Actual Variance Report",
        f"**Period:** {REPORT_PERIOD}  ",
        f"**Prepared:** {date.today().isoformat()}  ",
        f"**Variance Flag Threshold:** ±{VARIANCE_FLAG_PCT:.0f}%  ",
        f"**Status:** ✅ Demonstration — Synthetic Data Only",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"Total company spend came in **${abs(total_variance):,.2f} ({abs(total_variance_pct):.1f}%)**"
        f" **{variance_symbol} budget** for {REPORT_PERIOD}.",
        "",
        "| | Budget | Actual | Variance | Variance % |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| **Total** | **${total_budget:,.2f}** | **${total_actual:,.2f}** | **${total_variance:+,.2f}** | **{total_variance_pct:+.1f}%** |",
        "",
        "---",
        "",
        "## Department Summary",
        "",
        dept_md,
        "",
        "---",
        "",
        "## Top 5 Variance Drivers",
        "",
        top5_md,
        "",
        "---",
        "",
        "## Full Variance Detail",
        f"> ⚠️ = variance exceeds ±{VARIANCE_FLAG_PCT:.0f}%",
        "",
        detail_md,
        "",
        "---",
        "",
        f"![Budget vs Actual Chart](figures/budget_variance_chart.png)",
        "",
        "> **Note:** This report uses synthetic (fictional) data for portfolio demonstration purposes.",
    ]
    return "\n".join(lines) + "\n"


def build_chart(dept_summary: pd.DataFrame):
    os.makedirs(FIGURES_DIR, exist_ok=True)

    depts = dept_summary["department"].tolist()
    x = np.arange(len(depts))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars_b = ax.bar(x - width / 2, dept_summary["budget"], width, label="Budget", color="#3498db", alpha=0.85)
    bars_a = ax.bar(x + width / 2, dept_summary["actual"], width, label="Actual", color="#e74c3c", alpha=0.85)

    ax.set_title(f"Budget vs Actual by Department — {REPORT_PERIOD}", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Department", fontsize=11)
    ax.set_ylabel("Amount ($)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(depts, fontsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.legend(fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"📊 Chart saved to: {CHART_FILE}")


def run():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    df = load_data()
    df = calculate_variance(df)
    dept_sum = department_summary(df)

    report_text = build_report(df, dept_sum)
    with open(REPORT_FILE, "w", encoding="utf-8") as fh:
        fh.write(report_text)
    print(f"✅ Budget variance report written to: {REPORT_FILE}")

    build_chart(dept_sum)

    total_variance = df["actual"].sum() - df["budget"].sum()
    flagged = df["flag"].sum()
    print(f"   Total variance : ${total_variance:+,.2f}")
    print(f"   Flagged lines  : {flagged} (>{VARIANCE_FLAG_PCT:.0f}% threshold)")


if __name__ == "__main__":
    run()
