# school-calendar

One trustworthy picture of school events and extracurricular
dates/times — band, choir, school events — feeding the Guardian
calendar feed and lead-time event notifications.

- `src/school_calendar/event_sources/` — adapters per source
  (calendar readers, the email-event extractor agent's output sink)
- `src/school_calendar/events/` — normalized event model + merge/dedup
- `src/school_calendar/calendar_feed/` — ICS feed service + event query MCP

Plan: `docs/PLAN.md` (milestones M0–M4, the CALENDAR-EVENTS.md
contract, the pagination/full-coverage standing gate, open items).
Work checklist: `docs/CHECKLIST.md`.

Status: **M0 scaffold only** — package shells, gates, plan. No
collector code, no event code, no deploy. M1 is a source
inventory only.

## Gates

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
scripts/verify.sh   # unit -> coverage >=90 -> mypy strict ->
                    # 500-LOC cap -> system tests
```

Branches are stacked (`stack/m0-scaffold`, …); main
fast-forwards to verified tips only, after the dispatcher re-runs
`scripts/verify.sh` independently. Origin: hal9k
`~/git/school-calendar.git` (remote `ululuth`).
