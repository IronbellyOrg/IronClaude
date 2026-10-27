# D-0021 — OPS-001 decision-record closure spec

**Task:** T01.25 (Phase 1, Roadmap OPS-001 / R-021)
**Tier:** EXEMPT (Section 5.3 — documentation / ADR closure)
**Status:** Implemented 2026-05-20

## OPS-001 contract

Roadmap row 86 (OPS-001 / R-021) requires:

1. `decisions.md` updated.
2. D-5..D-8 queued for sign-off.
3. Unresolved blockers listed.
4. Implementation gates reference decisions (by ADR ID).

The authoritative satisfaction site is the new **"OPS-001 Closure"** section
appended to `.dev/releases/current/cliEval/decisions.md` (anchor follows the
D-9 reconciliation section). The Sign-off table above that section is also
updated in R3 to reflect the queued-for-sign-off status.

## What landed in this task

| AC bullet (T01.25)                                                       | Site |
|--------------------------------------------------------------------------|------|
| D-5..D-8 status flipped to `queued for sign-off`                         | `decisions.md` Sign-off table — column "Status" now reads `🟠 QUEUED FOR SIGN-OFF (R3)` for D-5..D-8 with date `2026-05-20`. |
| OQ-1/3/7/8/10 resolution-status field or owner pointer                   | `decisions.md` §"OPS-001 Closure" → §B. Five-row table with `Owner`, `Target`, `Resolution status as of 2026-05-20`, `Blocks` columns. |
| Implementation gates reference decisions by ADR ID                       | `decisions.md` §"OPS-001 Closure" → §C. Eight-row table mapping D-1..D-8 → implementation gate site + Phase/task ID. |
| `artifacts/D-0021/spec.md` records the update summary                    | This file. |

## OQ-1/3/7/8/10 resolution-status inventory

Verbatim status as recorded in `decisions.md` §"OPS-001 Closure" §B (copied
here so this file is self-contained for downstream tooling):

| OQ    | Owner    | Target                                                  | Resolution status                                                        |
|-------|----------|---------------------------------------------------------|--------------------------------------------------------------------------|
| OQ-1  | RyanW    | before M1 exit                                          | OPEN — pending maintainer sign-off pass on D-1..D-8.                     |
| OQ-3  | architect| before FR-CLI1 close (M4)                              | DEFERRED to M4 — captured in `suites/real.yaml` `no_pty:skip` tag per eval. |
| OQ-7  | RyanW    | before M1 exit                                          | OPEN — DOC-OQ7 awaits maintainer call (add `--junit` OR remove spec §9 conditional). |
| OQ-8  | architect| before COMP-005 close                                   | OPEN (deferred) — DOC-OQ8 records env-var honour OR layer removal.       |
| OQ-10 | QA Lead  | before M3 exit (empirical resolution accepted)         | DEFERRED to M3/M5 — R3-mit lands once OQ-10 closes.                      |

## Implementation-gate → ADR cross-reference

Verbatim from `decisions.md` §"OPS-001 Closure" §C:

| ADR | Implementation gate site                                                                                          |
|-----|-------------------------------------------------------------------------------------------------------------------|
| D-1 | `cli/eval/pty/` source drop + `PROVENANCE.md` (NFR-MAINT1, roadmap row 131)                                       |
| D-2 | `cli/eval/expect.py` (COMP-010 interface T01.14; primitives T04.x)                                                |
| D-3 | `cli/eval/isolation.py` referencing `cli/sprint/executor.py:107-182` (FR-ISO1)                                    |
| D-4 | `cli/eval/suites/*.yaml` + `suites/suite.schema.json` (DM-011, T01.02) + `suites/<name>_callbacks.py`             |
| D-5 | `loader.py` matcher-coverage check + `eval doctor --check-coverage` (FR-G5)                                       |
| D-6 | `DiskBudgetWatchdog` sidecar + `--max-disk-mb` flag in §4 (M3 RunOrchestrator)                                    |
| D-7 | `validate_eval_id` (FR-SCH2, T01.05) + `resolve_scratch_root` (AC12, T01.19) + `HomeIsolation.setup()`            |
| D-8 | `EvalOutcome` dataclass + `AggregatedRunReport.from_outcomes()` dimensional assertion (COMP-008, T03.13)          |

## Unresolved-blockers list (T01.25 explicit requirement)

Two M1-exit blockers remain after this task:

1. **OQ-1** — maintainer sign-off pass on D-1..D-8 (RyanW, before M1 exit).
2. **OQ-7** — `--junit` flag decision (RyanW, before M1 exit).

Three OQs are deferred-by-design and do not block M1 exit:

3. **OQ-3** — `--no-pty` exclusion set (M4).
4. **OQ-8** — `CLAUDE_FAKE_TIME_OFFSET` semantics (before COMP-005 close, scoped to EvalConfig contract).
5. **OQ-10** — MCP-flaky retry taxonomy (M3 empirical).

## Files touched

| Path                                                                  | Action |
|-----------------------------------------------------------------------|--------|
| `.dev/releases/current/cliEval/decisions.md`                          | Sign-off rows D-5..D-8 updated to QUEUED FOR SIGN-OFF (R3); R3 revision-log entry; new §"OPS-001 Closure" appended after D-9 reconciliation. |
| `.dev/releases/current/cliEval/artifacts/D-0021/spec.md`              | Created (this file). |
| `.dev/releases/current/cliEval/artifacts/D-0021/notes.md`             | Created. |
| `.dev/releases/current/cliEval/artifacts/D-0021/evidence.md`          | Created. |
| `.dev/releases/current/cliEval/evidence/T01.25/decisions_diff.md`     | Created — captures the decisions.md content delta. |

## Verification

Per task tier (EXEMPT, "Skip verification"), no test execution is required.
Manual maintainer review per `roadmap.md:86` AC is the gate. This spec lists
the four AC bullets and their landing sites so review is mechanical:
each AC has a single site reference, and each site exists at the cited path.

## Out of scope

- Flipping D-1..D-8 to 🟢 APPROVED (sign-off pass, SC1, M1-exit).
- Substantive resolution of any OQ (OPS-001 is queue + status only).
- Edits to `roadmap.md` or `.roadmap-state.json`.
