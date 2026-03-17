# Bank Reconciliation Report
**Period:** January 31, 2024  
**Prepared:** 2026-03-17  
**Status:** ✅ Demonstration — Synthetic Data Only

---

## 1. Matched Transactions
Items appearing on **both** the bank statement and the GL cash ledger (13 items):

| description                              | amount     |
|:-----------------------------------------|:-----------|
| Customer Payment - Maple Leaf Foods      | $4,500.00  |
| Supplier Invoice - Office Supplies       | $-320.45   |
| Payroll Run                              | $-8,750.00 |
| Customer Payment - CN Rail               | $12,000.00 |
| Customer Payment - Rogers Communications | $6,800.00  |
| CRA HST Remittance                       | $-2,340.00 |
| Customer Payment - TD Bank               | $3,200.00  |
| Rent Payment - Commercial Space          | $-4,200.00 |
| Customer Payment - Bell Canada           | $5,500.00  |
| Utilities Payment                        | $-410.00   |
| Customer Payment - Loblaw Companies      | $9,100.00  |
| Insurance Premium                        | $-875.00   |
| Customer Payment - Shoppers Drug Mart    | $2,750.00  |


## 2. Items in GL Only (Deposits in Transit / Unrecorded by Bank)
Recorded in GL but **not yet** on the bank statement (1 items):

| date                | description        | amount    | type    |
|:--------------------|:-------------------|:----------|:--------|
| 2024-01-31 00:00:00 | Deposit in Transit | $3,000.00 | receipt |


## 3. Items on Bank Statement Only
On bank statement but **not recorded** in GL (3 items):

| date                | description     | amount   | type       |
|:--------------------|:----------------|:---------|:-----------|
| 2024-01-10 00:00:00 | Bank Fee        | $-15.00  | withdrawal |
| 2024-01-30 00:00:00 | NSF Fee         | $-45.00  | withdrawal |
| 2024-01-31 00:00:00 | Interest Earned | $12.50   | deposit    |


## 4. Reconciliation Summary

| Item | Amount |
| --- | ---: |
| Bank Ending Balance | $17,112.05 |
| Add: Deposits in Transit | $3,000.00 |
| Less: Outstanding Items | $-60.00 |
| **Adjusted Bank Balance** | **$20,052.05** |

---

> **Note:** This report uses synthetic (fictional) data for portfolio demonstration purposes.
> No real company or financial data is included.
