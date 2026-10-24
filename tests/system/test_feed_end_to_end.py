"""System tests for the calendar feed (M0 placeholder).

SKIPPED with a precise reason, per the coding standard: M0 is a
scaffold — there is no events store, no ICS feed, and no MCP
server yet, so there is no live dependency to run end-to-end
against. The real system tests land with their milestones (M3
store, M4 feed + event query MCP) and this skip is reconciled
then, not carried forward silently.
"""

import pytest


@pytest.mark.skip(
    reason=(
        "no live dependency: M0 scaffold has no events store, ICS "
        "feed, or MCP server; system tests land with M3/M4"
    )
)
def test_feed_end_to_end_placeholder() -> None:
    raise AssertionError("unreachable: test is skipped, never runs")
