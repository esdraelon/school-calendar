# Source inventory — school-calendar M1

_Inventory only. No collectors, no ingestion code, no store,
no feed. Every entry was read from a real calendar, mailbox,
page, or on-disk config on 2026-10-24 — not remembered.
Where evidence ran out, the entry says so instead of
inventing a source._

## Standing rules applied to every entry

- **Paging row required.** Per Noah's 2026-10-24 standing
  rule, no source entry is complete without its paging
  mechanism: default limit, ordering, and how a consumer
  pages to exhaustion — or "single-shot source" where no
  paging mechanism exists. A later milestone must never
  discover paging late.
- **Absence notices are NEVER surfaced.** Standing boundary
  (CALENDAR-EVENTS.md): scope is events/schedules only.
  The absence stream is inventoried below (S7) only so a
  collector can recognize and exclude it, never to feed it.
- **District-owned Google Calendar dead end: recorded, not
  re-opened.** Settled 2026-10-22: no ICS, no sharing.
  See S8. Nothing in this inventory re-litigates it.
- **Due dates are drivers, not events.** Per
  CALENDAR-EVENTS.md, due dates project onto the feed from
  the school MCP; they do not move into a calendar store.
  See S10 for how this bears on the agenda decks.

## Access paths used for this inventory

- Google Calendar via the estate's connected connector
  (`hatch_gws_cli calendar`): account
  `en.gannim@gmail.com`, timezone America/Chicago.
- Gmail via the estate's connected connector
  (`hatch_gws_cli gmail`): same account.
- hal9k over SSH: adapter `deploy-run/deck_registry.json`,
  school-index `~/school-index-data/corpus.db` (read-only
  queries; no tokens printed, logged, or committed).
- Public web: text search + page fetch only.

## S1 — Smithborough Calendar (family Google Calendar) ★ operative school calendar

- **What it is:** the shared family calendar that already
  carries Sam's school/ensemble events. Calendar id
  `544e19de…@group.calendar.google.com`
  (full id in the evidence note below); summary
  "Smithborough Calendar"; `dataOwner`
  `dianascarborough@gmail.com`; Noah's account holds
  `accessRole: owner` on it.
- **Event types observed** (window 2026-08-01–2027-01-31,
  60 events returned, single page, no `nextPageToken` at
  `maxResults` 250): Wind Ensemble Rehearsal ×18 (weekly,
  Fri 16:30–17:45 America/Chicago), Band Concert ×4
  (18:30, Don Tew Performing Arts Center / Knox Wiley MS),
  Fall Choir Concert (2026-10-19 19:30, Leander HS),
  8th Grade Rouse Rehearsal (2026-08-28 17:15), Band
  Preview (2026-08-28 18:45), "No school" ×4, "First day
  of school!" (2026-08-12), "Winter Break" (2026-12-19),
  plus ordinary family entries (appointments, haircuts,
  trips) — a collector must filter by school/ensemble
  signal, not ingest the whole calendar.
- **Creators:** Noah (`en.gannim@gmail.com`), Diana
  (`dianascarborough@gmail.com`), and legacy
  `dave.bot@ululuth.com` (2 events; the Dave gateway is
  shut down — those entries are history, not a live
  writer).
- **Access that works:** Google Calendar API
  `events.list` on this calendar id, `singleEvents=true`,
  `orderBy=startTime`, `timeMin`/`timeMax` window.
- **Paging:** default `maxResults` 250; ordering
  `startTime` (ascending) when requested; exhaustion =
  loop on `nextPageToken` until absent. **Proven
  2026-10-24:** `maxResults=5` over the same window
  returned 5 items + a `nextPageToken`, and page 2
  continued from it. The connector's `+agenda` shortcut
  caps at 50 events per calendar and is NOT exhaustive —
  never use it for collection.
- **Cadence:** manual human entry, irregular (rehearsals
  entered in batches; concerts entered weeks ahead).
- **Dedup candidates:** Fall Choir Concert vs choir
  director email (S6); Band Concerts vs band director
  email (S5). Calendar entries outrank email mentions
  (merge discipline, CALENDAR-EVENTS.md).
- **Confidence: high.** Direct API read, full window.
- **Gap proof:** the Sat 2026-10-24 District Band
  Auditions (S5 email, 2026-10-23) do NOT appear on this
  calendar — email is not a redundant copy of it.

## S2 — Primary calendar (Noah's own Google Calendar)

- **What it is:** `en.gannim@gmail.com` primary calendar.
- **Event types observed** (same window, 11 events):
  mostly personal/travel; two school-adjacent items —
  "WMS 8th Grade Football vs Running Brushy MS" and
  "Choir Party". No rehearsal/concert series lives here.
- **Access / paging:** same Google Calendar API
  mechanism as S1 (`maxResults` 250 default,
  `nextPageToken` loop, `orderBy=startTime`).
- **Cadence:** manual, irregular.
- **Confidence: high** (direct read); **weight: low** —
  a secondary sweep source, not a series home.

## S3 — "Family" Google Calendar (empty)

- **What it is:** calendar id
  `family18409994413072149220@group.calendar.google.com`,
  summary "Family", owner Noah.
- **Event types:** none observed — 0 events in the
  2026-08-01–2027-01-31 window.
- **Access / paging:** same Google Calendar API
  mechanism as S1.
- **Confidence: high** that it exists and is empty in
  this window. It is NOT a school-event source in
  practice; M2 should not assume it fills later without
  re-checking.

## S4 — "The configured 8th grade calendar" — NOT FOUND as a distinct calendar

- **What was checked:** full `calendarList` for Noah's
  connected Google account (8 calendars: Holidays in
  United States, Amtgard Polaris Events, MetzOhanian,
  Surface Machine Systems, primary, Smithborough,
  Family, Amtgard). None is named for 8th grade or a
  school. A Gmail search for the phrase "8th grade
  calendar" returned no messages.
- **Candidate explanations (unresolved, not decided):**
  1. Smithborough (S1) IS what Noah meant — it is the
     calendar carrying 8th-grade events, configured by
     the family rather than the district.
  2. The math "Class Calendar" pointers in the team
     agenda deck (S10) — link targets not yet resolved
     to a calendar id or URL.
  3. A calendar on another account or device that the
     connected Google account cannot see.
- **Access / paging:** unknown until the calendar is
  identified. If it turns out to be a Google Calendar,
  S1's paging row applies; if it is an ICS feed, M2
  must record that feed's own paging (ICS is normally
  single-shot per fetch — see S8).
- **Confidence: high that no such distinct calendar is
  visible to the estate today; low on which candidate
  is right.** OPEN QUESTION for Noah (see Open
  questions).

## S5 — Band director email (Taylor Williamson) ★ operative ensemble source

- **What it is:** mail from
  `taylor.williamson@leanderisd.org` (Director of Bands,
  Wiley MS) to Noah's Gmail (BCC). Weekly "Wind
  Ensemble: Week N-N" letters plus logistics mail:
  "District Band Auditions: Saturday, October 24
  Information" (2026-10-23), "Festival of Bands
  Information (Monday, September 28)" (2026-09-22),
  "Wiley Band – Missing MakeMusic Assignments" (recurring
  assignment mail — NOT events; a collector must not
  treat every director mail as an event).
- **Event types:** rehearsals (incl. schedule changes),
  concerts, auditions, festivals, apparel-store deadlines
  (deadline-shaped; treat as event only if it has a
  date/time/place, else it is not an event).
- **Prose shape (read in full, audition mail):** date in
  subject + body ("Saturday, October 24"), location
  ("Cedar Park Middle School, 2100 Sun Chase Blvd."),
  arrival time ("7:00 AM"), FUZZY end ("finished
  between 11:00 AM and 1:00 PM", pickup on call/text).
  Fuzzy ends must be preserved as ranges/notes, not
  sharpened by the extractor — this is a direct driver
  of extraction-confidence values.
- **Access that works:** Gmail search
  (`from:taylor.williamson@leanderisd.org`) + message
  read. Broad director query estimates ~201 matches
  (Gmail `resultSizeEstimate` is an estimate only).
- **Paging:** `users.messages.list` with
  `maxResults=500` per page + `pageToken` loop
  (`--page-all`); the `+triage` shortcut defaults to
  `--max 20` and is NOT exhaustive — never use it for
  collection. Gmail enforces a per-account request-unit
  budget; collectors page narrow queries, not
  whole-mailbox scans.
- **Cadence:** weekly letters (Sun/Mon pattern in the
  sample) + ad-hoc logistics mail days before events.
- **Confidence: high.** Sender, volume, and a full
  event-bearing body verified.

## S6 — Choir director email (Abigail Justice, Kelly Murphy Sanchez)

- **What it is:** mail from
  `abby.justice@leanderisd.org` and
  `Kelly.Sanchez@leanderisd.org` (Wiley Choir) to Noah's
  Gmail: "7th/8th Grade Fall Choir Concert - Monday,
  October 19th" (2026-10-06), "Choir Concert and Picture
  Day TOMORROW!" (2026-10-18), "Choir Concert MONDAY!!"
  (Sanchez, 2026-10-14), "Region Choir Information"
  (2026-09-21), "Rouse HS Choir 8th Grade Night & LISD
  Choral Showcase" (2026-09-10). Varsity Tenor-Bass
  Choir confirmed as a Wiley ensemble: "Varsity
  Tenor-Bass Choir UIL - TOMORROW!" (Justice,
  2026-03-30); "Choir UIL schedule!!!" (Sanchez,
  2026-03-09).
- **Event types:** concerts, picture day, region/UIL
  auditions and showcases, choir parent meetings,
  sectionals (see also the public Region Choir page, S9).
- **Access / paging:** same Gmail mechanism as S5.
- **Cadence:** ad-hoc around concerts/auditions; weekly
  pattern less regular than band.
- **Dedup candidate (confirmed):** Fall Choir Concert
  2026-10-19 appears BOTH as Smithborough event
  (S1, creator Diana) and in three director emails —
  the textbook calendar-outranks-email merge case.
- **Confidence: high.**

## S7 — Wiley MS / LISD newsletters via ParentSquare (email-derived)

- **What it is:** ParentSquare mail to Noah's Gmail
  (`donotreply+…` senders, "Wiley MS via ParentSquare",
  "Leander ISD via ParentSquare", "Rouse HS via
  ParentSquare"): periodic digests ("Oct 2, 2026 Digest",
  "Sep 18, 2026 Digest") plus the weekly Wiley community
  newsletter whose dated event lists appear on public
  ParentSquare feeds (e.g. week of 2026-09-28: Festival
  of Bands, PTA Spirit Night, football/volleyball games,
  cross-country meet; week of 2026-09-21: Band Send Off
  Concert, Choir Back to School Bash, games/meets).
- **Event types:** school-wide dated lists — games,
  meets, concerts, spirit nights, testing windows.
  Broad but shallow (often date + name only, no time
  or location).
- **Access that works:** Gmail search for the
  ParentSquare senders + digest read. The public
  ParentSquare feed pages carry the same newsletter
  text; whether a given digest body contains the full
  newsletter text was NOT verified in M1 (digest bodies
  not read) — M2 must verify before treating digests
  as the collection path.
- **Paging:** same Gmail mechanism as S5.
- **Cadence:** weekly newsletter + digests; attendance
  alerts daily (see exclusion below).
- **ABSENCE-NOTICE EXCLUSION (standing boundary):**
  the same ParentSquare stream carries "Daily
  Attendance Alert" (Wiley MS, Rouse HS), "Truancy
  Warning Notice", and `wmsattendance@leanderisd.org`
  absence threads — all EXCLUDED from collection,
  enforceable by sender + subject before any body is
  read. Noah reads absence mail himself; the collector
  must never surface it. The exclusion filter is part
  of the M2 collector spec, not an M1 judgment call.
- **Confidence: medium.** Stream + public newsletter
  content verified; digest-body completeness unverified.

## S8 — District / school public calendar pages

- **Leander ISD 2026-27 academic calendar:** Board
  approved Feb 19 (news article): first day Wed
  2026-08-12, last day Thu 2027-05-27 (early release),
  full-week Fall Break, two-week Winter Break, one-week
  Spring Break. This matches the Smithborough entries
  for first day / winter break — a cross-check, not a
  separate feed.
- **Access that works:** HTML/news pages only. No
  subscribable feed found in M1's searches
  (`lisd.net` calendar pages are HTML at-a-glance
  pages, e.g. the staff professional-learning calendar).
- **Paging:** single-shot HTML per fetch; no paging
  mechanism — each fetch returns the whole published
  page. A collector re-fetches on schedule and diffs.
- **District-owned Google Calendar: DEAD END (settled
  2026-10-22, recorded not re-opened).** No ICS, no
  sharing. M1's searches found nothing contradicting
  that settlement.
- **Open lead (not a source yet):** the Wiley
  newsletter text says "check out the WMS calendar"
  but captures no URL or feed for it. If a public WMS
  calendar page exists, M2 may resolve it; until then
  it is not inventoried as a source.
- **Confidence: medium-high** for the academic-calendar
  facts; **high** for the dead-end settlement (prior
  decision, nothing found against it).

## S9 — Ensemble public pages (band / choir sites)

- **Wiley Band site** (`sites.google.com/view/wileymsband`,
  linked from the director's mail signature): homepage
  fetched 2026-10-24 — program blurb only (est. 2006,
  375+ students, 2022 CC State Honor Band). No
  calendar, ICS, or dated event list surfaced in the
  fetched text. Director email (S5) remains the
  operative band source; the site is a fallback
  reference, not a collection source today.
- **Wiley Choir Region Choir page**
  (`sites.google.com/leanderisd.org/wiley-middle-school-choir/region-choir`):
  dated sectional list (Sep 3–Oct 22, 4:30–5:30;
  Oct 9 Region Bootcamp 6–7:30pm; Oct 24 mock
  audition; Oct 25 Region Auditions @ Cedar Park MS
  7:30am; Nov 8 Region Clinic & Concert @ Lake Travis
  HS). Candidate public-page source for choir
  sectionals that may never reach email or Smithborough.
- **Access / paging:** single-shot HTML fetch per page;
  no paging mechanism. Staleness risk: seasonal pages
  (region choir) go stale after the season — a
  collector must record fetch date and treat absence
  of new dates as "page unchanged", not "no events".
- **Confidence: medium.** Pages and dates verified by
  search/fetch; no live site crawl was run to prove a
  stable collection path.

## S10 — Adapter agenda decks (drivers, NOT an event source)

- **What they are:** the school-info-adapter's deck
  registry (`deploy-run/deck_registry.json`,
  captured 2026-10-22): (1) Math 8 weekly-grid deck,
  (2) Algebra I weekly-grid deck, (3) "2026 - 2027 8th
  Grade Team Weekly Agenda" team-table deck (ELA /
  Math / Social Studies / Science). Corpus check:
  99 `corpus_items` (53 AGENDA ok, 27 failed,
  5 tombstoned, 14 TEAM_SITE ok); the team agenda
  item's extracted text is a week-dated table
  ("Week 10/26 - 10/30", columns Mon–Fri) with
  Topic/Agenda/Due per subject (e.g. Social Studies
  Unit 2 Test due 10/30, Science Phet Simulation due
  10/27).
- **Decision recorded (settled by the contract, not
  invented here):** the decks' dated items are
  classwork/due items — they stay DRIVERS in the
  school MCP and merely PROJECT onto the feed, per
  CALENDAR-EVENTS.md ("Due dates are drivers, not
  events — they project onto the feed; they don't move
  into a calendar store"). They are NOT ingested as
  calendar events. A collector that copied deck Due
  dates into the events store would double-count every
  assignment as an event.
- **The unresolved part (OPEN QUESTION):** every Math
  row in the team agenda is a stub reading "Agenda:
  Class Calendar" — the math agenda lives in class
  calendars whose ids/URLs are NOT in the extracted
  text (link targets don't survive text extraction).
  Those class calendars may be the "configured 8th
  grade calendar" of S4, or per-class calendars. M2
  needs the link targets (deck SVG/hyperlink layer or
  Noah) before they can be inventoried as sources.
- **Access / paging (for the decks as drivers):**
  adapter scrape on its 6h timer; deck text is a
  single published Slides document per deck —
  single-shot per fetch, no paging. This row is about
  the driver path, not event collection.
- **Confidence: high** for the driver decision
  (contract + extracted text); **low** for the class
  calendar pointers (unresolved).

## S11 — Other calendars in the connected account (out of scope, listed so M2 doesn't re-survey)

- Holidays in United States (Google public calendar,
  reader) — generic holidays, not school events.
- Amtgard Polaris Events + Amtgard (Noah's LARP
  community) — out of scope.
- MetzOhanian, Surface Machine Systems, LLC — family /
  business calendars, no school events observed in
  scope; same Google paging mechanism if ever needed.

## Coverage summary (CALENDAR-EVENTS.md expected list)

| Expected source | Status |
|---|---|
| Configured 8th grade calendar | NOT FOUND as distinct (S4) — open question |
| Band ensemble calendar / mail | Inventoried: S1 (calendar) + S5 (mail) |
| Choir ensemble calendar / mail | Inventoried: S1 (calendar) + S6 (mail) + S9 (site) |
| District / school calendars | Inventoried: S8 (HTML only; Google dead end settled) |
| Family calendars | Inventoried: S1 operative, S3 empty, S2 secondary |
| Email-derived (director, newsletter, schedule-change) | Inventoried: S5, S6, S7 |
| Agenda decks | Decided as drivers, not events (S10); class-calendar pointers open |

## OPEN ITEM — ingestion-time validator (later collector milestone, NOT built)

Per Noah 2026-10-24 (school-assistant
`docs/REFINEMENT-NOTES.md`): an agent may review
low-confidence email extractions at INGESTION before
they reach the events store — ingestion-only, verdicts
recorded as provenance, same flag-not-silent-feed
discipline as CALENDAR-EVENTS.md. Unsettled: sampling
vs full pass, quarantine-vs-flag thresholds, flag-only
vs correction-writing. M2's collector spec must carry
this as an open item; M1 builds nothing for it. The
schema draft (docs/EVENT-SCHEMA.md) reserves a
`validation_verdict` provenance field for it.

## Open questions for Noah

1. **What is the "configured 8th grade calendar"?**
   No distinct calendar by that name is visible to the
   estate's connected Google account, and no mail
   mentions it. Is it Smithborough (S1), the math
   "Class Calendar" pointers (S10), or a calendar on
   another account/device?
2. **Math class-calendar link targets:** can the
   "Class Calendar" links in the team agenda deck be
   resolved (deck hyperlink layer, or a URL from a
   teacher) so M2 can inventory them?
3. **Is there a public WMS calendar page?** The
   newsletter references "the WMS calendar" without a
   URL. Worth resolving, or is Smithborough + LISD
   HTML enough?
4. **ParentSquare digest bodies:** should the M2
   collector read digests for newsletter text, or is
   the public ParentSquare feed the cleaner path?
5. **Scope check:** are Rouse HS calendars/mail (Owen,
   Aiden) in scope for this package, or is
   school-calendar Sam/Wiley-only for now? M1
   inventoried Wiley/Sam sources; Rouse items appear
   only incidentally (attendance alerts, 8th Grade
   Night).

## Evidence notes (so the dispatcher can re-verify)

- Smithborough window pull: 60 events, 2026-08-01 to
  2027-01-31, `singleEvents=true`,
  `orderBy=startTime`, `maxResults=250`, no
  `nextPageToken`. Paging proof: `maxResults=5` →
  5 items + token; page 2 via that token → 5 more.
  Smithborough id:
  `544e19de3f830c6f6e5edc6a5330686aad36a51b86e6c4f7247a200c9440d076@group.calendar.google.com`.
- Family id:
  `family18409994413072149220@group.calendar.google.com`
  (0 events, same window). Primary: 11 events.
- Gmail: Williamson query estimate 201 (broad query);
  audition mail id `1a1691de980492fa` read in full;
  choir Justice/Sanchez queries; ParentSquare query;
  absence query (subjects only — bodies not needed
  for exclusion-shape evidence).
- hal9k: `~/school-info-adapter/deploy-run/deck_registry.json`;
  `corpus.db` read-only: `corpus_items` 99 rows by
  (`source_kind`, `status`); team agenda text via
  `item_text`.
- No tokens, credentials, or message bodies beyond the
  one event-bearing director mail were copied into
  this inventory; calendar/event ids above are the
  minimum needed for re-verification.
