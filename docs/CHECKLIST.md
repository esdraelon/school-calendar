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
- [ ] Create bare repo `~/git/school-calendar.git` on hal9k;
      clone on hal9k (`~/school-calendar`) and on this VM
      (`/home/hatch/workspace/school-calendar`, remote `ululuth`).
- [ ] Scaffold on branch `stack/m0-scaffold` (discrete commits):
  - [ ] Package `school_calendar` with empty subpackage shells
        for `event_sources`, `events`, `calendar_feed`, each
        naming its design pattern in its docstring.
  - [ ] `pyproject.toml` (Python 3.12, src layout; dev deps only
        — M0 code imports nothing external).
  - [ ] `scripts/verify.sh` (unit → coverage ≥90 → mypy strict
        → 500-LOC cap → system tests) + `scripts/check_loc.py`.
  - [ ] Smoke unit tests (shells import, patterns named);
        system tests skip with a precise reason (no live
        dependency exists yet).
  - [ ] `.gitignore`, README.md.
- [ ] Gates green on this VM at the tip (`scripts/verify.sh`).
- [ ] Push `stack/m0-scaffold` to ululuth; gates green on hal9k
      at the same tip (hal9k clone checks out the branch).
- [ ] Report: branch + tip, gates evidence on both machines,
      repo paths, plan doc location, surprises. Do NOT merge to
      main — the dispatcher fast-forwards after independent
      verification.
