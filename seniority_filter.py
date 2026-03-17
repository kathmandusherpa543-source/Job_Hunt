"""
seniority_filter.py
-------------------
Configurable seniority filter for accounting job postings.

Rules (all case-insensitive, applied to job title):
  - A posting is EXCLUDED if its title matches any exclude_term.
  - Among the remaining postings, this module can optionally restrict
    to only those that match at least one include_term (strict mode).

The default mode is *permissive*: a posting is kept as long as it does
not match any exclude term (so a plain "Accountant" title passes even
though it doesn't explicitly say "junior").
"""

from __future__ import annotations
import re
from typing import Iterable


def _make_pattern(terms: Iterable[str]) -> re.Pattern:
    """Compile a single regex that matches any of the given terms (word-boundary aware)."""
    escaped = [re.escape(t.strip().lower()) for t in terms if t.strip()]
    if not escaped:
        return re.compile(r"(?!)")  # never matches
    return re.compile(r"(?:^|[\s\-/])(?:" + "|".join(escaped) + r")(?:$|[\s\-/,.])", re.IGNORECASE)


def build_seniority_filter(exclude_terms: list[str], include_terms: list[str] | None = None):
    """
    Returns a callable ``filter_fn(title: str) -> bool`` that returns True when
    the title passes the seniority gate (i.e. should be KEPT).

    Parameters
    ----------
    exclude_terms : list[str]
        Terms that signal the role is too senior.
    include_terms : list[str] | None
        If provided and non-empty, strict mode is used: the title must match
        at least one include term (in addition to not matching any exclude term).
        Pass ``None`` or an empty list for permissive mode (default).
    """
    exclude_pattern = _make_pattern(exclude_terms)
    include_pattern = _make_pattern(include_terms) if include_terms else None

    def filter_fn(title: str) -> bool:
        title_str = str(title)
        if exclude_pattern.search(title_str):
            return False
        if include_pattern is not None and not include_pattern.search(title_str):
            return False
        return True

    return filter_fn


def apply_seniority_filter(df, exclude_terms: list[str], include_terms: list[str] | None = None,
                           title_col: str = "title", strict: bool = False):
    """
    Filter a pandas DataFrame to keep only entry/intermediate postings.

    Parameters
    ----------
    df : pd.DataFrame
    exclude_terms : list[str]
    include_terms : list[str] | None
        Only used when ``strict=True``.
    title_col : str
        Column containing the job title.
    strict : bool
        If True, also require the title to match at least one include term.
    """
    if df.empty:
        return df
    effective_include = include_terms if strict else None
    filter_fn = build_seniority_filter(exclude_terms, effective_include)
    mask = df[title_col].apply(filter_fn)
    return df[mask].copy()
