"""
bank_recon.py — Bank Reconciliation Demo
=========================================
Demonstrates a typical bank-to-GL cash reconciliation workflow:

  1. Load the bank statement and GL cash ledger.
  2. Identify matched items (same amount & description on both sides).
  3. Report:
     - Deposits in transit (in GL but not yet on bank statement).
     - Outstanding items / NSF charges (on bank statement but not in GL).
     - Reconciled balance comparison.
  4. Write a Markdown report to ``reports/bank_reconciliation_report.md``.

Usage
-----
    python -m modules.bank_reconciliation.bank_recon
    # or
    python modules/bank_reconciliation/bank_recon.py
"""

from __future__ import annotations

import os
import sys
from datetime import date

import pandas as pd

# Resolve project root regardless of where the script is called from
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

DATA_DIR = os.path.join(_ROOT, "data")
REPORTS_DIR = os.path.join(_ROOT, "reports")

BANK_FILE = os.path.join(DATA_DIR, "bank_statement.csv")
GL_FILE = os.path.join(DATA_DIR, "gl_cash_ledger.csv")
REPORT_FILE = os.path.join(REPORTS_DIR, "bank_reconciliation_report.md")

REPORT_DATE = "January 31, 2024"
BANK_ENDING_BALANCE = 17_112.05   # balance shown on bank statement after all transactions


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    bank = pd.read_csv(BANK_FILE, parse_dates=["date"])
    bank = bank[bank["amount"].notna()].copy()
    bank["amount"] = pd.to_numeric(bank["amount"], errors="coerce")

    gl = pd.read_csv(GL_FILE, parse_dates=["date"])
    gl = gl[gl["amount"].notna()].copy()
    gl["amount"] = pd.to_numeric(gl["amount"], errors="coerce")

    return bank, gl


def reconcile(bank: pd.DataFrame, gl: pd.DataFrame):
    """
    Match items by description + amount (rounded to 2 dp).
    Returns (matched, bank_only, gl_only) DataFrames.
    """
    bank_set = bank[["description", "amount"]].copy()
    gl_set = gl[["description", "amount"]].copy()

    # Merge on description + amount to find matches
    matched = pd.merge(bank_set, gl_set, on=["description", "amount"], how="inner").drop_duplicates()

    matched_desc_amounts = set(zip(matched["description"], matched["amount"]))

    def is_matched(row):
        return (row["description"], row["amount"]) in matched_desc_amounts

    bank_only = bank[~bank.apply(is_matched, axis=1)].copy()
    gl_only = gl[~gl.apply(is_matched, axis=1)].copy()

    return matched, bank_only, gl_only


def compute_balances(bank_only: pd.DataFrame, gl_only: pd.DataFrame, bank_ending: float):
    """
    Standard bank reconciliation:
      Adjusted Bank Balance = Bank Ending + Deposits in Transit - Outstanding Cheques
      Adjusted GL Balance   = GL Ending  + Bank charges not in GL - NSF not in GL

    For simplicity we derive GL ending from the totals visible in the data.
    """
    deposits_in_transit = gl_only[gl_only["amount"] > 0]["amount"].sum()
    outstanding_withdrawals = bank_only[bank_only["amount"] < 0]["amount"].sum()
    bank_charges_not_in_gl = bank_only[bank_only["amount"] < 0]["amount"].sum()
    bank_credits_not_in_gl = bank_only[bank_only["amount"] > 0]["amount"].sum()

    adjusted_bank = bank_ending + deposits_in_transit + outstanding_withdrawals

    return {
        "bank_ending_balance": bank_ending,
        "deposits_in_transit": deposits_in_transit,
        "outstanding_items": outstanding_withdrawals,
        "adjusted_bank_balance": adjusted_bank,
    }


def build_report(matched: pd.DataFrame, bank_only: pd.DataFrame, gl_only: pd.DataFrame,
                 balances: dict) -> str:
    """Render the reconciliation as a Markdown string."""

    def df_to_md(df: pd.DataFrame) -> str:
        if df.empty:
            return "_No items._\n"
        cols = [c for c in ["date", "description", "amount", "type"] if c in df.columns]
        sub = df[cols].copy()
        if "amount" in sub.columns:
            sub["amount"] = sub["amount"].apply(lambda x: f"${x:,.2f}")
        return sub.to_markdown(index=False) + "\n"

    lines = [
        f"# Bank Reconciliation Report",
        f"**Period:** {REPORT_DATE}  ",
        f"**Prepared:** {date.today().isoformat()}  ",
        f"**Status:** ✅ Demonstration — Synthetic Data Only",
        "",
        "---",
        "",
        "## 1. Matched Transactions",
        f"Items appearing on **both** the bank statement and the GL cash ledger ({len(matched)} items):",
        "",
        df_to_md(matched),
        "",
        "## 2. Items in GL Only (Deposits in Transit / Unrecorded by Bank)",
        f"Recorded in GL but **not yet** on the bank statement ({len(gl_only)} items):",
        "",
        df_to_md(gl_only),
        "",
        "## 3. Items on Bank Statement Only",
        f"On bank statement but **not recorded** in GL ({len(bank_only)} items):",
        "",
        df_to_md(bank_only),
        "",
        "## 4. Reconciliation Summary",
        "",
        "| Item | Amount |",
        "| --- | ---: |",
        f"| Bank Ending Balance | ${balances['bank_ending_balance']:,.2f} |",
        f"| Add: Deposits in Transit | ${balances['deposits_in_transit']:,.2f} |",
        f"| Less: Outstanding Items | ${balances['outstanding_items']:,.2f} |",
        f"| **Adjusted Bank Balance** | **${balances['adjusted_bank_balance']:,.2f}** |",
        "",
        "---",
        "",
        "> **Note:** This report uses synthetic (fictional) data for portfolio demonstration purposes.",
        "> No real company or financial data is included.",
    ]
    return "\n".join(lines) + "\n"


def run():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    bank, gl = load_data()
    matched, bank_only, gl_only = reconcile(bank, gl)
    balances = compute_balances(bank_only, gl_only, BANK_ENDING_BALANCE)
    report_text = build_report(matched, bank_only, gl_only, balances)

    with open(REPORT_FILE, "w", encoding="utf-8") as fh:
        fh.write(report_text)

    print(f"✅ Bank reconciliation report written to: {REPORT_FILE}")
    print(f"   Matched items      : {len(matched)}")
    print(f"   GL-only items      : {len(gl_only)}  (deposits in transit)")
    print(f"   Bank-only items    : {len(bank_only)}")
    print(f"   Adjusted bank bal  : ${balances['adjusted_bank_balance']:,.2f}")


if __name__ == "__main__":
    run()
