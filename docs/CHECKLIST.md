# Work checklist — M0 scaffold

_Plan before building: this checklist existed (in docs/PLAN.md)
before the first line of code. Tick order is execution order._

- [x] Read school-assistant CONTEXT.md, docs/PACKAGES.md (the
      school-calendar row), docs/CALENDAR-EVENTS.md,
      docs/CODING-STANDARD.md, and the development-orchestration
      skill.
- [x] Read the school-index M0 template (src layout,
      scripts/verify.sh, smoke tests, pyproject gates).
- [x] Write docs/PLAN.md (milestones M0–M4 outline, the
      CALENDAR-EVENTS.md contract, the pagination/full-coverage
      standing gate, open items) BEFORE any code.
- [x] Write this checklist BEFORE any code.
- [x] Create bare repo `~/git/school-calendar.git` on hal9k;
      clone on hal9k (`~/school-calendar`) and on this VM
      (`/home/hatch/workspace/school-calendar`, remote `ululuth`).
  - [x] Scaffold on branch `stack/m0-scaffold` (discrete commits):
  - [x] Package `school_calendar` with empty subpackage shells
        for `event_sources`, `events`, `calendar_feed`, each
        naming its design pattern in its docstring.
  - [x] `pyproject.toml` (Python 3.12, src layout; dev deps only
        — M0 code imports nothing external).
  - [x] `scripts/verify.sh` (unit → coverage ≥90 → mypy strict
        → 500-LOC cap → system tests) + `scripts/check_loc.py`.
  - [x] Smoke unit tests (shells import, patterns named);
        system tests skip with a precise reason (no live
        dependency exists yet).
  - [x] `.gitignore`, README.md.
- [x] Gates green on this VM at the tip (`scripts/verify.sh`).
- [x] Push `stack/m0-scaffold` to ululuth; gates green on hal9k
      at the same tip (hal9k clone checks out the branch).
- [ ] Report: branch + tip, gates evidence on both machines,
      repo paths, plan doc location, surprises. Do NOT merge to
      main — the dispatcher fast-forwards after independent
      verification.

# Work checklist — M1 source inventory (this branch)

_Plan before writing: this section existed (in docs/PLAN.md,
M1 section) before the inventory docs were written. Tick
order is execution order. Docs + inventory evidence only;
no code changes, so the M0 gates must stay green untouched._

- [x] Read school-assistant CONTEXT.md,
      docs/CALENDAR-EVENTS.md, docs/CODING-STANDARD.md
      (pagination & coverage section, branch
      `stack/pagination-rule`), docs/REFINEMENT-NOTES.md
      (agent-at-ingestion open item), and the
      development-orchestration skill.
- [x] Branch `stack/m1-source-inventory` off
      `stack/m0-scaffold` (tip 6c28b73); update docs/PLAN.md
      + this checklist for M1 before writing inventory.
- [x] Google Calendar ground truth: `calendarList list`
      (8 calendars), Smithborough window pull
      2026-08-01–2027-01-31 (60 events, no nextPageToken at
      maxResults 250), paging proof (maxResults 5 → token
      present, page 2 continues), Family calendar (0 events),
      primary calendar (11 events) in the same window.
- [x] Gmail ground truth: band director mail (Taylor
      Williamson), choir director mail (Abigail Justice,
      Kelly Murphy Sanchez), ParentSquare stream
      (newsletter digests + attendance alerts), absence
      stream sender/subject shape, "8th grade calendar"
      phrase search (no matches).
- [x] hal9k ground truth: adapter `deck_registry.json`
      (3 decks), school-index corpus (99 corpus_items:
      53 AGENDA ok / 27 failed / 5 tombstoned / 14 TEAM_SITE
      ok), Team Weekly Agenda extracted text (week-dated
      Topic/Agenda/Due; Math rows stub "Agenda: Class
      Calendar").
- [x] Public-web ground truth: LISD 2026-27 academic
      calendar approval (news article), Wiley MS
      ParentSquare community newsletter (dated event
      lists), Wiley Band Google Site homepage (no
      calendar/ICS surfaced), Wiley Choir Region Choir
      page (dated sectionals).
- [x] Write docs/SOURCE-INVENTORY.md: one entry per
      source with owner, event types, working access
      method + evidence, paging row (limit / ordering /
      exhaustion path, or single-shot), cadence,
      confidence, dedup candidates. District Google
      Calendar dead end recorded, not re-opened.
      Agenda-deck question recorded (deck items stay
      drivers per the CALENDAR-EVENTS.md boundary;
      math "Class Calendar" pointers unresolved — open
      question for Noah).
- [x] Write docs/EVENT-SCHEMA.md: normalized event
      draft per the CALENDAR-EVENTS.md contract + the
      standing pagination gate (per-pass source total +
      bounds, paging-exhausted flag), merge/dedup keys,
      per-source health record.
- [x] Record the ingestion-validator open item (Noah
      2026-10-24, REFINEMENT-NOTES.md) as an OPEN ITEM
      in both docs for a later collector milestone.
      Do NOT build it.
- [ ] Gates green on this VM at the tip
      (`scripts/verify.sh`) — no code changes, so the M0
      gates must pass untouched.
- [ ] Push `stack/m1-source-inventory` to ululuth;
      gates green on hal9k at the same tip.
- [ ] Report: branch + tip, inventory summary,
      schema location, open questions for Noah,
      surprises. Do NOT merge to main.
