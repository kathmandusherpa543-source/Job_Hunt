.PHONY: install reports bank-recon ap-aging budget-variance test clean help

## Default target
help:
	@echo ""
	@echo "Accounting Job Hunt — Makefile"
	@echo "================================"
	@echo "  make install         Install Python dependencies"
	@echo "  make reports         Generate ALL reports + charts (market summary + work samples)"
	@echo "  make bank-recon      Run bank reconciliation demo only"
	@echo "  make ap-aging        Run AP aging report demo only"
	@echo "  make budget-variance Run budget vs actual variance report only"
	@echo "  make test            Run pytest test suite"
	@echo "  make clean           Remove generated report files"
	@echo ""

install:
	pip install -r requirements.txt

## Generate all reports and charts
reports:
	python reports/generate_reports.py

## Individual accounting work-sample modules
bank-recon:
	python -m modules.bank_reconciliation.bank_recon

ap-aging:
	python -m modules.ap_aging.ap_aging

budget-variance:
	python -m modules.budget_variance.budget_variance

## Run test suite
test:
	pytest tests/ -v

## Remove generated outputs (keeps source data)
clean:
	rm -f reports/job_market_summary.md \
	      reports/bank_reconciliation_report.md \
	      reports/ap_aging_report.md \
	      reports/budget_variance_report.md
	rm -f reports/figures/*.png
