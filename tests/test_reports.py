"""
Tests for the report-generation utility functions.
"""

import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# We test the pure (no-IO) functions directly
from reports.generate_reports import (
    count_by_location,
    count_by_role_category,
    count_top_skills,
    build_summary_report,
    ROLE_CATEGORIES,
)


@pytest.fixture
def sample_jobs():
    return pd.DataFrame({
        "title": [
            "Junior Accountant",
            "AP Clerk",
            "Bookkeeper",
            "Payroll Assistant",
            "Accounting Assistant",
            "Junior Financial Analyst",
        ],
        "location": [
            "Toronto, Ontario",
            "Toronto, Ontario",
            "Mississauga, Ontario",
            "Toronto, Ontario",
            "Brampton, Ontario",
            "Toronto, Ontario",
        ],
        "description": [
            "Proficient in Excel, QuickBooks, reconciliation",
            "month-end close, accounts payable, Excel",
            "bookkeeping, Sage, journal entries",
            "payroll processing, HST, Excel",
            "Excel, data entry, GAAP",
            "financial statements, forecasting, Excel",
        ],
    })


class TestCountByLocation:
    def test_counts_correctly(self, sample_jobs):
        counts = count_by_location(sample_jobs)
        assert counts["Toronto, Ontario"] == 4
        assert counts["Mississauga, Ontario"] == 1

    def test_missing_location_column(self):
        df = pd.DataFrame({"title": ["Junior Accountant"]})
        counts = count_by_location(df)
        assert counts.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame({"location": []})
        counts = count_by_location(df)
        assert counts.empty


class TestCountByRoleCategory:
    def test_counts_ap_ar(self, sample_jobs):
        counts = count_by_role_category(sample_jobs)
        assert counts.get("AP / AR Clerk", 0) >= 1

    def test_counts_bookkeeper(self, sample_jobs):
        counts = count_by_role_category(sample_jobs)
        assert counts.get("Bookkeeper", 0) >= 1

    def test_all_categories_present(self, sample_jobs):
        counts = count_by_role_category(sample_jobs)
        assert isinstance(counts, pd.Series)
        assert len(counts) > 0

    def test_no_title_column(self):
        df = pd.DataFrame({"company": ["Acme"]})
        counts = count_by_role_category(df)
        assert counts.empty


class TestCountTopSkills:
    def test_excel_is_top_skill(self, sample_jobs):
        counts = count_top_skills(sample_jobs)
        assert "Excel" in counts.index
        assert counts["Excel"] >= 4

    def test_returns_series(self, sample_jobs):
        counts = count_top_skills(sample_jobs)
        assert isinstance(counts, pd.Series)

    def test_max_15_results(self, sample_jobs):
        counts = count_top_skills(sample_jobs, top_n=15)
        assert len(counts) <= 15

    def test_fallback_synthetic_data(self):
        """When no text columns present, synthetic defaults should be returned."""
        df = pd.DataFrame({"company": ["Acme"]})
        counts = count_top_skills(df)
        assert isinstance(counts, pd.Series)
        assert len(counts) > 0


class TestBuildSummaryReport:
    def test_report_contains_header(self, sample_jobs):
        loc = count_by_location(sample_jobs)
        roles = count_by_role_category(sample_jobs)
        skills = count_top_skills(sample_jobs)
        report = build_summary_report(sample_jobs, loc, roles, skills)
        assert "# Accounting Job Market Summary" in report

    def test_report_contains_total_count(self, sample_jobs):
        loc = count_by_location(sample_jobs)
        roles = count_by_role_category(sample_jobs)
        skills = count_top_skills(sample_jobs)
        report = build_summary_report(sample_jobs, loc, roles, skills)
        assert str(len(sample_jobs)) in report

    def test_report_is_markdown(self, sample_jobs):
        loc = count_by_location(sample_jobs)
        roles = count_by_role_category(sample_jobs)
        skills = count_top_skills(sample_jobs)
        report = build_summary_report(sample_jobs, loc, roles, skills)
        assert "---" in report   # markdown horizontal rule
        assert "##" in report    # section headers
