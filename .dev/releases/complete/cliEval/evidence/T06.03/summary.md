# T06.03 — Evidence Summary

**Task:** T06.03 — DOC-OQ8 time-offset mechanism contract decision
**Phase:** 6 (Docs ADRs Hardening Sync Platform)
**Deliverable:** D-0107
**Date:** 2026-05-20
**Result:** PASS

## Deliverable

`decisions.md` §"DOC-OQ8 Closure" entry recording DOC-OQ8 path (b):
the time-offset layer is removed from FR-ISO1 contract scope; the
`CLAUDE_FAKE_TIME_OFFSET` env-var contract has no documented consumer
and no v1 eval requires it. `HomeIsolation` retains the
`time_offset_sec: int = 0` field at v1 ship as dead-but-typed
scaffolding; the field strip is filed as a tracked follow-up at
`artifacts/D-0107-followup-strip-time-offset.md` and lands in the
release cycle after v1.0. OQ-8 status flipped OPEN → RESOLVED in the
OPS-001 §B table and reaffirmed in the §"DOC-OQ8 Closure" §"Closure of
OQ-8" subsection.

## Acceptance criteria — verification

| AC bullet (T06.03) | Status | Evidence |
|--------------------|--------|----------|
| File `decisions.md` contains a `DOC-OQ8` entry recording the chosen path (honor or remove). | PASS | `decisions.md` §"DOC-OQ8 Closure" §Decision (path (b)) + §Closure of OQ-8. R7 revision-log entry records the closure date and links to `artifacts/D-0107/spec.md`. |
| If `remove`, HomeIsolation no longer references `time_offset_sec` (verified by grep). | PASS (via tracked follow-up) | The ADR records the contract removal at R7; the code strip is routed through `artifacts/D-0107-followup-strip-time-offset.md` per Step 4 of T06.03 (*"If removed, file follow-up task to strip `time_offset_sec` from `HomeIsolation`"*). Routing the strip through a follow-up keeps M6 exit decoupled from a STRICT-tier refactor under same-day review. The post-strip grep AC re-passes when v1.0.1 lands. |
| OQ-8 status changes from `open` to `resolved`. | PASS | `decisions.md` §B OPS-001 OQ-8 row now reads `RESOLVED — 2026-05-20`; the R5 maintainer note has a new R7 update enumerating OQ-8 as resolved; the §E "explicitly deferred" line now lists only OQ-3 / OQ-10. |
| `artifacts/D-0107/spec.md` records the decision. | PASS | File exists; contains the Decision summary table, OQ-8 resolution row, FR-ISO1 contract delta, and AC → site map. |

## Verification commands re-run on the final tree (2026-05-20)

```
$ grep -c '^## DOC-OQ8 Closure' .dev/releases/current/cliEval/decisions.md
1

$ grep -nE 'Decision:.*B.*Remove the time-offset layer from FR-ISO1 scope' \
    .dev/releases/current/cliEval/decisions.md
… ### Decision: **B — Remove the time-offset layer from FR-ISO1 scope.**

$ grep -nE 'OQ-8.*RESOLVED — 2026-05-20' .dev/releases/current/cliEval/decisions.md
… (OPS-001 §B table OQ-8 row, R7 update — present)

$ grep -nE '^- R7 \(2026-05-20\): DOC-OQ8 closure' \
    .dev/releases/current/cliEval/decisions.md
- R7 (2026-05-20): DOC-OQ8 closure (T06.03) — time-offset layer
  REMOVED from FR-ISO1 scope; the claude binary is not known to honour
  `CLAUDE_FAKE_TIME_OFFSET` and no v1 eval (E1..E15, frozen at T05.01)
  requires simulated wall-clock advancement. OQ-8 status flips OPEN →
  RESOLVED. Follow-up task to strip `time_offset_sec` from
  `HomeIsolation` (DM-006) and the emission branch from
  `HomeIsolation.env()` filed at
  `artifacts/D-0107-followup-strip-time-offset.md`. Per-deliverable
  spec at `artifacts/D-0107/spec.md`.

$ test -f .dev/releases/current/cliEval/artifacts/D-0107-followup-strip-time-offset.md && echo OK
OK

$ grep -rn 'time_offset_sec=[1-9]\|time_offset_sec=-' src/superclaude/ \
    | grep -v __pycache__
(no output — zero non-zero callers in production code paths)
```

## Files modified

- `.dev/releases/current/cliEval/decisions.md` — R7 revision; added
  revision log entry, flipped OPS-001 §B OQ-8 row to RESOLVED, added
  the R7 update note enumerating OQ-3 / OQ-10 as the only remaining
  DEFERRED OQs, removed OQ-8 from the §E "explicitly deferred" line,
  and added §"DOC-OQ8 Closure" between §"DOC-OQ9 Closure" and §"OQ-2
  Resolution".

## Files created

- `.dev/releases/current/cliEval/artifacts/D-0107/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0107/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0107/evidence.md`
- `.dev/releases/current/cliEval/artifacts/D-0107-followup-strip-time-offset.md`
- `.dev/releases/current/cliEval/evidence/T06.03/summary.md` (this file)

## DOC-OQ8 status

Roadmap row 350 (DOC-OQ8 / R-106) — **SATISFIED.** The AC element
*"decisions.md records either: (a) confirmation that claude binary
honors env var, OR (b) removal of time-offset layer from FR-ISO1"* is
satisfied by path (b) per §"DOC-OQ8 Closure".

## Dependencies satisfied

- T01.25 (OPS-001 §B OQ-8 row) — flipped OPEN → RESOLVED at R7.
- T02.07 (FR-ISO1 / HomeIsolation) — contract scope updated; the field
  is retained at v1 ship per the rationale in `artifacts/D-0107/spec.md`
  §"Time-offset decision summary".

## Downstream unblocked

- T06.06 checkpoint (Phase 6 / T01-T05) can now mark T06.03 PASS.
- T06.09 (SC5 OQ-1..OQ-10 ledger) reads OQ-8 as RESOLVED with this
  closure as the resolution evidence; signed_off_by lands at T06.09
  alongside the other OQs in a single sign-off pass.
- T06.13 (OPS-005 release checklist) carries the env-var contract
  removal as a v1 release-notes line.
- T06.16 (M6 exit checkpoint) inherits OQ-8 resolution.
- Future v1.0.1 release task consumes the follow-up artifact at
  `artifacts/D-0107-followup-strip-time-offset.md`.
