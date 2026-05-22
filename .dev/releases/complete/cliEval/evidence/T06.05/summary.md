# T06.05 — Evidence Summary

**Task:** T06.05 — AC2 CI integration deferral note
**Phase:** 6 (Docs ADRs Hardening Sync Platform)
**Deliverable:** D-0109
**Date:** 2026-05-20
**Result:** PASS

## Deliverable

`decisions.md` entry recording AC2 deferral: local-only for v1; CI
revisit trigger documented; AC1 (Linux-only) cross-referenced; MIG-003
(T06.15) cross-referenced as v2 follow-up consolidation site; AC2
status flipped OPEN → RESOLVED.

## Acceptance criteria — verification

| AC bullet (T06.05) | Status | Evidence |
|--------------------|--------|----------|
| File `decisions.md` contains an `AC2` entry stating "CI: deferred (local-only v1)" with a named revisit trigger. | PASS | `decisions.md` §"AC2 Closure" §Decision table records `v1 execution context: Local developer machines only`, `CI status (v1): NON-GOAL`, and `Revisit trigger (whichever first)` enumerating three concrete clauses (a) 3+ regressions/month, (b) first formal request, (c) v2 planning gate 2026-07-01. |
| Cross-reference to AC1 Linux-only declaration is recorded. | PASS | `decisions.md` §"AC2 Closure" §"Cross-reference to AC1 (Linux-only declaration)" subsection cites roadmap row 353 / R-109 / T06.07. |
| AC2 entry status is `resolved`. | PASS | `decisions.md` §"AC2 Closure" §"Closure of AC2" subsection: `Resolution status: RESOLVED — 2026-05-20`. |
| `artifacts/D-0109/spec.md` records the deferral summary. | PASS | File exists; contains Decision table, AC2 resolution row, AC1 cross-reference, MIG-003 cross-reference, AC → site map. |

## Verification commands re-run on the final tree (2026-05-20)

```
$ grep -c '^## AC2 Closure' .dev/releases/current/cliEval/decisions.md
1
$ grep -E 'CI status \(v1\).*NON-GOAL' .dev/releases/current/cliEval/decisions.md
| **CI status (v1)** | NON-GOAL. No GitHub Actions workflow, no scheduled job, no CI badge, no `--ci` flag. The harness has no CI-tuned output mode at v1 ship. |
| **CI status (v1)** | NON-GOAL. No GitHub Actions workflow, no scheduled job, no `--ci` flag, no CI badge at v1 ship. |
$ grep -E '3\+ harness regressions' .dev/releases/current/cliEval/decisions.md
| **Revisit trigger (whichever first)** | **(a)** 3+ harness regressions caught locally in a single calendar month (a regression here = an `eval run --suite real` failure on `master` HEAD that a CI smoke run would have caught earlier); **(b)** first formal CI-integration request filed against this repo (e.g., GitHub issue, PR, or stakeholder request from RyanW); **(c)** v2 planning gate 2026-07-01 — whichever first surfaces the question, the revisit lands in a fresh ADR (this section is amended with an `Outcome:` line per the Reject/revise rule). |
1. **(a) 3+ harness regressions in a calendar month** — the only data-driven trigger. The threshold is calibrated to *"would CI have saved enough developer time to pay for itself"*: 3+ regressions per month sustains the cost of authoring + maintaining a workflow file (estimated ~80 LOC of YAML + maintainer overhead on flake triage). Below that rate, the local `make verify-sync` + manual `eval run --suite real` cadence is cheaper than CI overhead. The month-long observation window dampens noise from a single bad week.
| (a) 3+ harness regressions caught locally in a single calendar month; (b) first formal CI-integration request filed against this repo; (c) v2 planning gate 2026-07-01. |
$ grep -E '^- R9 \(2026-05-20\)' .dev/releases/current/cliEval/decisions.md
- R9 (2026-05-20): AC2 closure (T06.05) — CI integration deferred to v2; v1 ships local-only per AC1 (Linux-only). Revisit trigger recorded: any of (a) 3+ harness regressions caught locally in a single calendar month, (b) first formal CI-integration request filed against this repo, or (c) v2 planning gate 2026-07-01 — whichever first. AC1 Linux-only declaration cross-referenced; MIG-003 (T06.15) inherits the deferral as v2 follow-up scope. AC2 status flips OPEN → RESOLVED. Per-deliverable spec at `artifacts/D-0109/spec.md`.
```

(Note: `Resolution status: RESOLVED — 2026-05-20` now matches four
times across `decisions.md` — DOC-OQ4 / D-10 closure, DOC-OQ7 closure,
DOC-OQ9 closure, and the AC2 closure added by this task.)

## Files modified

- `.dev/releases/current/cliEval/decisions.md` — R9 revision; added
  revision log entry and §"AC2 Closure" section between §"DOC-OQ6
  Closure" and §"OQ-2 Resolution".

## Files created

- `.dev/releases/current/cliEval/artifacts/D-0109/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0109/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0109/evidence.md`
- `.dev/releases/current/cliEval/evidence/T06.05/summary.md` (this file)

## AC2 status

Roadmap row 352 (AC2 / R-108) — **SATISFIED.** Both AC elements
("decisions.md entry says local-only for v1; trigger for CI revisit
recorded") are landed by this task.

## Dependencies satisfied

- None upstream — T06.05 has no task dependencies in phase-6-tasklist.md.
- AC1 is referenced by roadmap row 353 / R-109; T06.07 will land the
  reciprocal AC1 entry that cross-references §"AC2 Closure".

## Downstream unblocked

- T06.06 checkpoint (Phase 6 / T01-T05) can now mark T06.05 PASS.
- T06.07 (AC1 wiring) has the upstream local-only commitment to
  cross-reference in its own AC1 decisions.md entry.
- T06.09 (SC5 OQ-1..OQ-10 ledger) reads AC1+AC2 closures together as
  the v1 scope-boundary attestation paired with the OQ ledger.
- T06.13 (OPS-005 release checklist) inherits "local-only" alongside
  "Linux only" as v1 release-notes headlines.
- T06.15 (MIG-003 v2 follow-up roadmap entry) inherits the CI deferral
  verbatim, paired with the macOS deferral from DOC-OQ9 (R6).
