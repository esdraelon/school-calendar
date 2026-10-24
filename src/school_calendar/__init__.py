"""School Calendar: one trustworthy picture of school events.

Pattern: a composed pipeline of three subpackages — ``event_sources``
adapts each source (calendar readers, the email-event extractor
agent's output sink), ``events`` holds the normalized event model
plus merge/dedup, and ``calendar_feed`` serves the ICS feed and the
event query MCP over the merged store. Each stage names its own
pattern in its subpackage docstring (per the coding standard).

Design: school-assistant/docs/CALENDAR-EVENTS.md. Plan:
docs/PLAN.md. Consumers read only the merged store; a dead
collector reads as a stale source, never as "no events."
"""
