"""Normalized event model + merge/dedup.

Pattern: Repository over the normalized events store, plus the
merge as a pure function over candidate events — same
precedence/freshness discipline as the adapter merge.

Merge discipline (CALENDAR-EVENTS.md): calendar entries outrank
email mentions of the same event; explicit updates supersede;
low-confidence email extractions are flagged, never silently fed.
Normalized fields: title, start/end (with timezone), location;
provenance (source kind, source id/link, collector identity,
extraction confidence); per-source health. Consumers read only
the merged store. Model + merge land in M3; the store schema is
reconciled against the M1 inventory before code.
"""
