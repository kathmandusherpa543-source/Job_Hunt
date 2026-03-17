"""
Tests for the seniority_filter module.
"""

import pytest
import pandas as pd

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from seniority_filter import build_seniority_filter, apply_seniority_filter

# Standard exclude/include lists mirroring config.yaml
EXCLUDE_TERMS = [
    "senior", "sr.", " sr ", "principal", "lead", "staff",
    "director", "head of", "vice president", " vp ", "chief",
    "executive", "controller", "manager", "mgr",
    "management", "supervisor", "team lead",
]
INCLUDE_TERMS = [
    "junior", "entry", "entry-level", "entry level",
    "intermediate", "associate", "assistant", "clerk",
    "coordinator", "administrator",
]


class TestBuildSeniorityFilter:
    """Unit tests for build_seniority_filter (permissive mode)."""

    def setup_method(self):
        self.filter_fn = build_seniority_filter(EXCLUDE_TERMS)

    # --- Titles that SHOULD pass ---
    @pytest.mark.parametrize("title", [
        "Junior Accountant",
        "Accounting Assistant",
        "AP Clerk",
        "AR Clerk",
        "Bookkeeper",
        "Payroll Assistant",
        "Intermediate Accountant",
        "Accounting Coordinator",
        "Financial Analyst",   # permissive: no exclude term
        "Accountant",          # plain title — permissive allows it
        "Accounts Payable Administrator",
    ])
    def test_passes_entry_intermediate_titles(self, title):
        assert self.filter_fn(title) is True, f"Expected PASS for: {title!r}"

    # --- Titles that SHOULD be excluded ---
    @pytest.mark.parametrize("title", [
        "Senior Accountant",
        "Senior Financial Analyst",
        "Finance Manager",
        "Accounting Manager",
        "Director of Finance",
        "VP Finance",
        "Controller",
        "Chief Financial Officer",
        "Principal Accountant",
        "Team Lead, Accounting",
        "Supervisor, Accounts Payable",
    ])
    def test_rejects_senior_titles(self, title):
        assert self.filter_fn(title) is False, f"Expected FAIL for: {title!r}"

    def test_case_insensitive(self):
        fn = build_seniority_filter(["senior"])
        assert fn("SENIOR Accountant") is False
        assert fn("senior accountant") is False
        assert fn("Senior Accountant") is False

    def test_intermediate_is_not_excluded(self):
        """Regression: 'intermediate' must NOT be in exclude list."""
        fn = build_seniority_filter(EXCLUDE_TERMS)
        assert fn("Intermediate Accountant") is True

    def test_empty_title_passes(self):
        assert self.filter_fn("") is True

    def test_none_as_string_passes(self):
        assert self.filter_fn("None") is True


class TestBuildSeniorityFilterStrict:
    """Unit tests for build_seniority_filter in strict (include_terms) mode."""

    def setup_method(self):
        self.filter_fn = build_seniority_filter(EXCLUDE_TERMS, INCLUDE_TERMS)

    @pytest.mark.parametrize("title", [
        "Junior Accountant",
        "Accounting Assistant",
        "Intermediate Accountant",
        "AP Clerk",
    ])
    def test_strict_passes_include_titles(self, title):
        assert self.filter_fn(title) is True

    @pytest.mark.parametrize("title", [
        "Financial Analyst",    # no include term → rejected in strict mode
        "Accountant",           # no include term
    ])
    def test_strict_rejects_no_include_term(self, title):
        assert self.filter_fn(title) is False

    @pytest.mark.parametrize("title", [
        "Senior Accountant",
        "Finance Manager",
    ])
    def test_strict_rejects_excluded_titles(self, title):
        assert self.filter_fn(title) is False


class TestApplySeniorityFilter:
    """Integration tests for apply_seniority_filter on DataFrames."""

    def _make_df(self, titles):
        return pd.DataFrame({"title": titles, "company": ["Acme"] * len(titles)})

    def test_filters_senior_from_dataframe(self):
        df = self._make_df([
            "Junior Accountant",
            "Senior Accountant",
            "AP Clerk",
            "Finance Manager",
        ])
        result = apply_seniority_filter(df, EXCLUDE_TERMS)
        assert set(result["title"]) == {"Junior Accountant", "AP Clerk"}

    def test_empty_dataframe_returns_empty(self):
        df = pd.DataFrame({"title": []})
        result = apply_seniority_filter(df, EXCLUDE_TERMS)
        assert result.empty

    def test_preserves_all_columns(self):
        df = self._make_df(["Junior Accountant"])
        result = apply_seniority_filter(df, EXCLUDE_TERMS)
        assert list(result.columns) == ["title", "company"]

    def test_result_is_copy(self):
        df = self._make_df(["Junior Accountant"])
        result = apply_seniority_filter(df, EXCLUDE_TERMS)
        result["title"] = "MODIFIED"
        # original unchanged
        assert df.iloc[0]["title"] == "Junior Accountant"
