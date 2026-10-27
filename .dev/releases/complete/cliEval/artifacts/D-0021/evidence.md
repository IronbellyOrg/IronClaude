# D-0021 — verification evidence

**Task:** T01.25 (Phase 1, Roadmap OPS-001 / R-021)
**Date:** 2026-05-20
**Tier:** EXEMPT (Section 5.3 — documentation/ADR closure, "Skip verification")

## 1. Files landed

| File                                                              | Action  |
|-------------------------------------------------------------------|---------|
| `.dev/releases/current/cliEval/decisions.md`                      | Edited — Sign-off rows D-5..D-8 flipped to `🟠 QUEUED FOR SIGN-OFF (R3)`; R3 revision-log entry added; new §"OPS-001 Closure" section appended. |
| `.dev/releases/current/cliEval/artifacts/D-0021/spec.md`          | Created. |
| `.dev/releases/current/cliEval/artifacts/D-0021/notes.md`         | Created. |
| `.dev/releases/current/cliEval/artifacts/D-0021/evidence.md`      | Created (this file). |
| `.dev/releases/current/cliEval/evidence/T01.25/decisions_diff.md` | Created — content delta capture. |

## 2. AC verification (manual)

| AC bullet (T01.25)                                                                                       | Pass/Fail | Evidence |
|----------------------------------------------------------------------------------------------------------|-----------|----------|
| File `.dev/releases/current/cliEval/decisions.md` contains entries D-5..D-8 with status `queued for sign-off`. | PASS | Sign-off table — D-5..D-8 rows now read `🟠 QUEUED FOR SIGN-OFF (R3)` (verified by reading the file post-edit). |
| Each OQ-1, OQ-3, OQ-7, OQ-8, OQ-10 has a resolution-status field or owner pointer.                       | PASS | `decisions.md` §"OPS-001 Closure" §B — five-row table with `Owner`, `Target`, `Resolution status`, `Blocks`. |
| Implementation gates reference decisions by ADR ID.                                                       | PASS | `decisions.md` §"OPS-001 Closure" §C — eight-row table mapping D-1..D-8 → implementation gate sites with Phase/task IDs. |
| `TASKLIST_ROOT/artifacts/D-0021/spec.md` records the update summary.                                      | PASS | `artifacts/D-0021/spec.md` exists with the full update summary. |

## 3. Roadmap row 86 AC satisfaction

Roadmap text: *"decisions.md updated; D-5..D-8 queued for sign-off; unresolved blockers listed; implementation gates reference decisions"*.

| AC clause                                       | Site                                                         |
|-------------------------------------------------|--------------------------------------------------------------|
| "decisions.md updated"                          | R3 revision-log entry + new §"OPS-001 Closure" section.      |
| "D-5..D-8 queued for sign-off"                  | Sign-off table — rows D-5..D-8 stamped 🟠 QUEUED FOR SIGN-OFF.|
| "unresolved blockers listed"                    | §"OPS-001 Closure" §B (OQ-1 + OQ-7 listed as M1-exit blockers); also explicitly enumerated in `artifacts/D-0021/spec.md` "Unresolved-blockers list". |
| "implementation gates reference decisions"     | §"OPS-001 Closure" §C — eight ADR rows × implementation-gate-site mapping. |

## 4. Tier-proportional verification

Tier EXEMPT (Section 5.3) — "Skip verification" per the tasklist. The
verification method is maintainer review, not test execution. No CLI or
pytest invocation is required for this task.

The manual review surface is bounded:

- Sign-off table — 4 rows changed.
- Revision log — 1 line added.
- New section — single appended block at end of file (before the D-9
  reconciliation? No: after, by design — D-9 is a historical
  reconciliation entry; OPS-001 closure is a fresh post-D-9 section).
- 3 new files under `artifacts/D-0021/`.
- 1 new file under `evidence/T01.25/`.

## 5. Out of scope (per spec)

- Flipping any of D-1..D-8 to 🟢 APPROVED.
- Resolving any OQ substantively.
- Editing `roadmap.md` or `.roadmap-state.json`.

## 6. Follow-on actions

| Owner      | Action                                                  | Tracking site |
|------------|---------------------------------------------------------|---------------|
| RyanW      | Sign off D-1..D-8 (Sign-off table → 🟢 APPROVED).      | SC1 (roadmap row 348). |
| RyanW      | Resolve OQ-7 (`--junit`) before M1 exit.                 | DOC-OQ7 (roadmap row 253). |
| architect  | Resolve OQ-3 (`--no-pty` exclusion set) before M4 exit.  | DOC-OQ3 (roadmap row 254). |
| architect  | Resolve OQ-8 (`CLAUDE_FAKE_TIME_OFFSET`) before COMP-005 close. | DOC-OQ8 (roadmap row 350). |
| QA Lead    | Resolve OQ-10 empirically before M3 exit.                | OQ-10 row (roadmap row 331). |
