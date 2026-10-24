"""Event source adapters: one owning collector per source.

Pattern: Adapter + Strategy registry — a Mapping from source key
to collector strategy, injected at the composition root (no
if/else selection, per the coding standard).

Calendar collectors are mostly not agents at all (ICS/Google
Calendar reads are tool calls on a schedule); the email collector
is an agent task (prose -> events) publishing candidate events
with a link to the source message. Every collector pages its
source to exhaustion for its window and records per-source health
on every run (see the pagination/full-coverage standing gate in
docs/PLAN.md). Collectors publish normalized events via the
calendar MCP's ingest tools. No collector code lands before M2;
M1 is the source inventory only.
"""
