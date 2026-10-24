# Normalized event schema — DRAFT (school-calendar M1)

_Draft only. No store, no ingest code, no MCP tools in this
milestone. This draft follows the CALENDAR-EVENTS.md
contract and the standing pagination/full-coverage gate,
and must be reconciled against the M1 inventory
(docs/SOURCE-INVENTORY.md) and the contract again before
M3 code. Field names are proposed, not frozen._

## Design notes

- **Frozen dataclasses, keyword-only construction** (coding
  standard) when this becomes code; this doc is the
  contract the code must match.
- **Timezone:** America/Chicago for this household.
  Timed events carry an explicit offset; all-day events
  carry dates with an exclusive end (Google's convention:
  a one-day event ends on the next date). Never mix the
  two shapes in one event, and never shift an all-day
  date across timezones.
- **Fuzzy ends are data, not defects.** Director mail
  often gives an arrival time and a pickup window
  ("finished between 11:00 AM and 1:00 PM"). The schema
  keeps `end` nullable + an `end_fuzzy` note instead of
  letting an extractor invent a sharp end time. A sharp
  end invented by extraction is a corruption bug.
- **Completeness and freshness are separate claims.**
  A paged-to-exhaustion result over a stale source is
  still labeled stale (standing gate §4). Every response
  carries both.
- **Consumers read only the merged store.** Raw
  collector output is never a surface (CALENDAR-EVENTS.md).

## 1. Normalized event

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | Deterministic id assigned at ingest (see §4). Stable across re-collections of the same source item. |
| `title` | string | As published by the source, trimmed. No reformatting beyond whitespace. |
| `start` | datetime + offset, or date | Timed: RFC 3339 with offset. All-day: date. |
| `end` | datetime + offset, or date, nullable | Exclusive end for all-day. Nullable when the source gives no end. |
| `end_fuzzy` | string, nullable | Verbatim source wording when the end is a window ("finished between 11:00 AM and 1:00 PM", "pickup on call/text"). |
| `all_day` | bool | True iff start/end are dates. |
| `timezone` | string (IANA) | `America/Chicago` for household sources; the source's own zone otherwise, never assumed. |
| `location` | string, nullable | Verbatim when present; empty is empty, not "TBD". |
| `description` | string, nullable | Source body excerpt or notes (e.g. transportation, what to bring). No invented detail. |
| `status` | enum | `confirmed` \| `tentative` \| `cancelled` \| `superseded`. Explicit updates supersede (see §4); cancellation is an event state, not a deletion. |
| `is_school_event` | bool | Collector's classification: does this belong on the Guardian school feed? (Smithborough also carries haircuts and dentist trips — the filter is part of ingest, and its verdict is stored, not recomputed at read time.) |

## 2. Provenance (every event carries all of these)

| Field | Type | Notes |
|---|---|---|
| `source_kind` | enum | `calendar` \| `email` \| `public_page`. (Agenda-deck items are NOT events — see inventory S10 — so there is no `deck` kind here. If Noah later decides otherwise, that is a schema change, not a silent addition.) |
| `source_id` | string | The inventory's source key: calendar id (S1–S3), sender+mailbox key (S5–S7), page URL (S8–S9). Stable per source, not per event. |
| `source_item_id` | string | The source's own item identity: Google event id, Gmail message id, page URL + fetch date. The dedup/update anchor. |
| `source_link` | string, nullable | Deep link: Google Calendar event link, Gmail message link, page URL. Email-derived events MUST carry the source message link (CALENDAR-EVENTS.md). |
| `collector_id` | string | Identity of the owning collector (one per source, M2). Format: `school-calendar:<source-key>`. |
| `extraction_confidence` | enum | `high` \| `medium` \| `low`. Calendar reads are `high` by construction (structured data). Email extractions grade on: date/time explicitness, location presence, fuzzy vs sharp end, single vs conflicting dates in the body. Low-confidence email extractions are flagged, never silently fed. |
| `validation_verdict` | enum, nullable | RESERVED for the ingestion-validator open item (Noah 2026-10-24; see §5): `pass` \| `flag` \| `quarantine` \| null (not yet validated / not applicable). No validator exists in M1; the field exists so M2/M3 don't retrofit provenance. |
| `collected_at` | datetime | When this record was collected, in UTC + America/Chicago local. |
| `source_updated_at` | datetime, nullable | The source item's own update timestamp when the source provides one (Google `updated`); null for email/pages. Drives explicit-updates-supersede. |

## 3. Per-source health (recorded in the store exactly like the adapter's per-source scrape health)

One health record per source per collection pass. A dead
collector reads as a stale source, never as "no events."

| Field | Type | Notes |
|---|---|---|
| `source_id` | string | As §2. |
| `last_successful_collection` | datetime, nullable | Last pass that completed (even if it returned zero events). Null = never successfully collected. |
| `last_attempt_at` | datetime | Last pass attempted, successful or not. |
| `last_error` | string, nullable | Last failure, verbatim-ish. Null on success. |
| `window_start` / `window_end` | datetime | The time window this pass covered. A pass that covered a window is not a claim about outside it. |
| `items_returned` | int | Events/items returned by this pass. |
| `source_total_claimed` | int, nullable | Total the source claims for the window, when the source reports one (Google does not return a total for `events.list` — null there; see §6 for how coverage is still proven without it). |
| `paging_exhausted` | bool | True iff the collector looped to the end of the source's paging mechanism for this window (no `nextPageToken` remaining / all pages consumed / single-shot page fetched). False = partial pull, and it must READ as partial everywhere downstream. |
| `bounds_min` / `bounds_max` | datetime or date, nullable | Earliest/latest event start in the returned set for this pass. The coverage-proof bounds (standing gate). |

## 4. Merge / dedup keys (owned by the `events` package, M3)

- **Identity of "the same event" across sources:**
  `dedup_key = (normalized_title, start_day, location_token)`
  where `normalized_title` lowercases, strips punctuation
  and ensemble prefixes ("Wiley", "Wind Ensemble" kept —
  they disambiguate, not noise), `start_day` is the
  America/Chicago calendar date of `start`, and
  `location_token` is the first distinctive location
  token (venue name or street number) when a location
  exists, else empty. Two records sharing a dedup key
  are merge candidates, not automatic merges — M3
  confirms the merge rule against the confirmed
  candidates (Fall Choir Concert 2026-10-19: S1 × S6;
  Band Concerts: S1 × S5).
- **Precedence:** calendar entries outrank email
  mentions of the same event; explicit updates
  supersede (newer `source_updated_at` on the same
  `source_item_id` replaces, keeping the old record as
  `superseded`, never deleting history); low-confidence
  email extractions are flagged, not silently fed.
- **Update identity:** (`source_id`, `source_item_id`)
  is the update anchor. A re-collection that returns
  the same anchor with a newer `source_updated_at`
  supersedes; a re-collection that drops the anchor is
  a candidate deletion — but see the standing-gate
  warning: a truncated page must never tombstone live
  items (the 2026-10-23 adapter incident). M3 must
  only tombstone on a paging-exhausted pass.
- **Collection-pass proof (standing gate):** every
  pass that feeds a surface records `items_returned`,
  `paging_exhausted`, `bounds_min`/`bounds_max`, and
  the window covered. A surface presenting "all events
  in range R" must show: total count + bounds matching
  the store's ground truth for R, per contributing
  source, with each source's freshness alongside. A
  test whose fixture fits under the source's default
  limit proves nothing about paging and fails the gate
  — M3/M4 fixtures must exceed 250 items for the
  Google Calendar path (and 500 for the Gmail path).

## 5. OPEN ITEM — ingestion-time validator (not built)

Per Noah 2026-10-24 (school-assistant
`docs/REFINEMENT-NOTES.md`): an agent may review
low-confidence email extractions at INGESTION before
they reach the events store — ingestion-only, verdicts
recorded as provenance (`validation_verdict` above).
Unsettled: sampling vs full pass, quarantine-vs-flag
thresholds, flag-only vs correction-writing (verdict
as provenance is the safer default). This schema
reserves the field; no validator logic, prompt, or
agent task is defined in M1. If a later plan absorbs
it as work, it is recorded as a follow-up, not folded
in silently.

## 6. Per-source paging contract (from the M1 inventory — the collector spec's starting point)

| Source (inventory key) | Default limit | Ordering | Exhaustion path |
|---|---|---|---|
| Google Calendar (S1–S3, S11) | `maxResults` 250 | `orderBy=startTime` ascending | Loop `nextPageToken` until absent. Proven M1 (S1). `+agenda` (50/calendar) is NOT a collection path. No source total is returned — coverage is proven by bounds + exhausted flag + window, not by a total. |
| Gmail (S5–S7) | `maxResults` 500/page | Gmail search order (newest first) unless sorted otherwise | Loop `pageToken` (`--page-all`) until pages run out. `+triage --max` (default 20) is NOT a collection path. Budget: per-account request units; narrow queries, bodies only for candidates. |
| Public HTML pages (S8–S9) | n/a — single-shot | Document order | One fetch = whole page. No paging mechanism. Staleness carried by fetch date + health record, not by paging. |
| Agenda decks as drivers (S10) | n/a — single-shot | Deck order | One fetch per deck. NOT an event source; listed so no collector mistakes a deck fetch for event coverage. |

## 7. What this draft deliberately does NOT decide

- The `event_id` generation scheme (UUID vs content
  hash) — M3 decides; the requirement is stability
  across re-collections.
- Recurrence representation (Google recurring series
  vs expanded instances): collection uses
  `singleEvents=true` (expanded instances); whether
  the store keeps the series link is M3's call.
- The `is_school_event` classifier's rules (keyword
  list vs agent judgment) — M2's collector spec, with
  the verdict stored per §1.
- Whether the math "Class Calendar" pointers (S10)
  become sources at all — open question for Noah
  (inventory §Open questions). No schema change is
  needed if they do: they would arrive as
  `source_kind=calendar` with their own `source_id`.
