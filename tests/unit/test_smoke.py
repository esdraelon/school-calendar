"""Smoke tests for the M0 scaffold.

Proves every subpackage imports and that each one names its design
pattern in its docstring (a coding-standard contract, so it is
tested, not just asserted in review). Real behavior tests arrive
with each subpackage's milestone.
"""

import school_calendar
from school_calendar import calendar_feed, event_sources, events

SUBPACKAGES = [school_calendar, event_sources, events, calendar_feed]


def test_subpackages_import() -> None:
    for package in SUBPACKAGES:
        assert package.__name__.startswith("school_calendar")


def test_subpackages_document_their_pattern() -> None:
    for package in SUBPACKAGES:
        doc = package.__doc__ or ""
        assert "Pattern" in doc, f"{package.__name__} docstring names no pattern"
