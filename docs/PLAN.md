# Plan — school-calendar

_Scaffold + milestone plan. Written before any code (M0), per the
development-orchestration skill: scope is the plan; anything the
plan didn't authorize waits for Noah._

## What this repo is

`school-calendar` is the estate's events package (see
school-assistant `docs/PACKAGES.md`): event source adapters, a
normalized events store, and an ICS feed. It feeds (a) the
Guardian calendar feed and (b) lead-time event notifications
alongside the due-date watch (school-assistant
`docs/CALENDAR-EVENTS.md`).

One trustworthy picture of events and extracurricular dates/times
— band, choir, school events — from various calendars and emails.
Due dates are drivers (school MCP), not events: they project onto
the feed; they do not move into a calendar store.

## Layout (mirrors school-index's M0)

```
src/school_calendar/
  __init__.py       # package composition: the three subpackages
  event_sources/    # adapters per source (calendar readers, the
                    # email-event extractor agent's output sink)
  events/           # normalized event model + merge/dedup
  calendar_feed/    # ICS feed service + event query MCP
scripts/verify.sh   # unit -> coverage >=90 -> mypy strict ->
                    # 500-LOC cap -> system tests
tests/unit/         # unit tests (coverage-measured)
tests/system/       # end-to-end tests (gate merges, not counted
                    # toward unit coverage)
docs/PLAN.md        # this file
docs/CHECKLIST.md   # M0 work checklist
```

Language and shape follow school-assistant
`docs/CODING-STANDARD.md`: Python 3.12, src layout, frozen
dataclasses with keyword-only construction, named design patterns
in every module docstring, DI + strategy registries (never
if/else chains for config-driven selection), 500-LOC cap per file,
≥90% unit coverage (total and per key module), mypy strict.
Branches are stacked (`stack/m0-scaffold`, `stack/m1-…`, …),
one agent per milestone, discrete commits; main fast-forwards to
verified tips only, after the dispatcher re-runs
`scripts/verify.sh` independently.

## The contract (from CALENDAR-EVENTS.md — binding on all milestones)

**Normalized event fields.** Every event published to the store
carries: title, start/end (with timezone), location; provenance —
source kind (`email` | `calendar`), source id/link, collector
identity, extraction confidence; and per-source health — last
successful collection, recorded in the store exactly like the
adapter's per-source scrape health. A dead collector reads as a
stale source, never as "no events."

**Merge discipline (owned by the `events` package, same
precedence/freshness discipline as the adapter merge).**
Calendar entries outrank email mentions of the same event;
explicit updates supersede; low-confidence email extractions are
flagged, never silently fed. Consumers (Guardian feed,
orchestrator) read only the merged store.

**Boundaries.** An email that *mentions* a date is not an event
until an agent extracts it with a source link. Absence notices are
Noah's to read and are never surfaced — standing boundary.
Collectors publish through the calendar MCP's ingest tools; agents
do not message each other to coordinate — the shared events store
on hal9k is the blackboard, and the dispatch mechanism for
collectors is deferred (Noah: cross that bridge later). The store
is what makes deferring safe.

**Freshness is data.** Surfaces state how fresh their data is;
degraded inputs degrade outputs visibly (staleness banner, named
failed source), never silently.

## STANDING GATE — pagination and full time-range coverage

_Noah, 2026-10-24. This gate binds every milestone from M2 onward
and is a acceptance criterion for each, not a nice-to-have._

1. **Every MCP tool returning a collection MUST document** its
   default limit, its ordering, and how a consumer pages to
   exhaustion — cursor/offset where the backing store supports
   one, time-window parameters where no cursor exists (the ICS
   feed and any time-ordered event listing page by time window).
2. **Every consumer MUST page to exhaustion** and prove
   full-range coverage in tests: total count plus min/max bounds
   (earliest/latest event in the returned set) matching the
   store's ground truth for the queried range. A test that reads
   one default-limit page and asserts on it proves nothing and
   fails the gate.
3. **No consumer may rely on a single default-limit call** —
   not the feed, not the orchestrator, not a collector resuming
   from a source, not a smoke script. Where a source API itself
   pages (Google Calendar, ICS feeds, mailbox reads), the
   collector pages it to exhaustion for its window and records
   the window covered, so a partial pull reads as a partial
   pull, never as a complete one.
4. **Staleness interaction:** a paged-to-exhaustion result over a
   stale source is still labeled stale (per-source health rides
   with every response); completeness and freshness are separate
   claims and both must be true before a surface presents the
   data as the full picture.

This gate is written into the M2 collector spec, the M3 store
spec, and the M4 feed/MCP spec when those milestones are
planned in detail; M1's inventory records, per source, whether
its access API pages and by what mechanism, so no later
milestone discovers paging late.

## Milestones

### M0 — Scaffold (this milestone) — DONE when gates are green

Package `school_calendar` with empty subpackage shells for
`event_sources`, `events`, `calendar_feed`; `pyproject.toml`
(Python 3.12); `scripts/verify.sh` with all five gates; smoke
tests proving the shells import and name their patterns; system
tests skipping with a precise reason (no live dependency exists
yet — no store, no feed, no MCP server). Gates green on both
this VM and hal9k at the tip of `stack/m0-scaffold`. Pushed to
ululuth, NOT merged to main. No collector code, no event code,
no deploy. See `docs/CHECKLIST.md`.

### M1 — Source inventory ONLY — no collectors

Enumerate every event source before any build, reconciled
against ground truth (real calendars, real mailboxes, real
access — read them, don't remember them):

- The configured 8th grade calendar: which calendar, who owns
  it, what event types are already on it, what format/access
  (ICS? Google Calendar?).
- Other calendars: band/choir ensemble calendars,
  district/school calendars, family calendars.
- Email sources: director emails, school newsletters,
  schedule-change notices — which mailboxes, what volume, what
  prose shapes.
- Per source: owner, access mechanism + credentials path,
  paging mechanism (see the standing gate above), event-type
  coverage, and known overlap with other sources (dedup
  candidates for M3).

Deliverable: an inventory document plus a source-registry schema
draft (kinds, ids, health fields). NO collector code, NO
ingest code, NO store code — inventory only. Exit criterion:
every source in CALENDAR-EVENTS.md's expected list is either
inventoried or explicitly recorded as not found, with the
evidence for each.

### M2 — Collectors (outline)

One owning collector per inventoried source. Calendar
collectors are mostly not agents at all: ICS/Google Calendar
reads are tool calls on a schedule (the estate's connectors
already read both mail and calendars). The email collector is
an agent task — prose → events is extraction, not parsing —
publishing candidate events with a link to the source message.
Each collector pages its source to exhaustion for its window
(standing gate) and records per-source health on every run.
Collectors publish normalized events via the calendar MCP's
ingest tools. See OPEN ITEMS for the ingestion-time validator
follow-up attached to this milestone.

### M3 — Normalized store + merge/dedup (outline)

SQLite store on hal9k (system of record) holding normalized
events + provenance + per-source health. The `events` package
owns merge/dedup: calendar-outranks-email, explicit-updates-
supersede, low-confidence flagged. Consumers read only the
merged store. Store schema reconciled against the M1 inventory
and the CALENDAR-EVENTS.md contract before code.

### M4 — ICS feed + event query MCP (outline)

Token-gated ICS feed on haliffer.ululuth.com (same gateway
pattern as the sibling MCPs: app-root serving, public-host
allowlist, proxy headers, one path-scoped token, container
conventions per the coding standard's deployment section).
Feed carries events/extracurriculars plus due dates that
matter (quizzes/tests as all-day entries, projected from the
school MCP — not stored as events). Event query MCP tools
document default limit, ordering, and paging-to-exhaustion
(standing gate); time-window parameters where no cursor
exists. Deploy follows the adapter's runbook shape; human go
before any production change; rollback is a config/route
change, never a data migration.

## OPEN ITEMS (follow-ups, not M0 work)

- **Ingestion-time soft-formatting-drift validator** (Noah,
  2026-10-24, recorded in school-assistant
  `docs/REFINEMENT-NOTES.md`). An agent could be brought to
  bear during INGESTION to validate soft formatting drift —
  e.g. random HTML fragments leaking into extracted text.
  Placement: calendar collectors. Email-derived events already
  carry extraction confidence, and a validator would review
  low-confidence extractions before they reach the events
  store — the same flag-not-silent-feed discipline as
  CALENDAR-EVENTS.md. All validation happens at ingestion,
  never at read time, with verdicts recorded as provenance.
  Status: OPEN ITEM for a later collector milestone (M2
  follow-up). NOT built in M0; M0 remains scaffold + plan only.
  Open questions for that milestone: sampling vs full pass,
  quarantine-vs-flag thresholds, flag-only vs
  correction-writing. If a later plan would absorb this as
  work, it is recorded as a follow-up instead.
- **Collector dispatch mechanism** — deferred by Noah
  (CALENDAR-EVENTS.md); the store/schema contract is settled,
  the scheduling/dispatch mechanism is not.
- **RAG-style questions** do not apply here; the event query
  MCP is a store query, not a search index (school-index owns
  search).

## Out of scope for M0 (and for this repo's early milestones)

Any other repo's code; live MCP containers or gateway routes;
the profile-birth staging (`deploy-run/data/vault`,
`classroom-profile`, `:birth` images — read-only);
school-assistant `DECISIONS.md`; D-1 (deferred); any collector
or event-ingestion code (M1+); any production deploy.
