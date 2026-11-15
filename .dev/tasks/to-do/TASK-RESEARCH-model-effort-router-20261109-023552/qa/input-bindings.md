# QA input-bindings inventory (qa/input-bindings.md)

Execution-time accepted-addition inventory for TASK-RESEARCH-model-effort-router-20261109-023552. This file is a future execution output created per item 1.1's bootstrap clause; it was NOT fabricated at construction time. Updated before each dependent dispatch whenever a planning/measurement/consolidation accepts an addition.

Columns: Consumer item ID | Exact path or pinned URL/revision/passage | Purpose | Accepted | Producer/evidence | Partition | Disposition (consuming or audit-only) | Replacement/acceptance evidence.

## Bootstrap history (copied from Task Log per item 1.1)

- 2026-11-12 22:30 UTC: item 1.1 metadata bootstrap recorded in Task Log (inventory did not yet exist). Baseline 12 inputs measured 1092 lines > 1000 budget; bootstrap overflow clause invoked; six preparation-page items emitted into bounded-phase1. See Task Log entry "item 1.1 started".
- 2026-11-12 22:36 UTC: coordinator re-bind refused by session issue-463-1109-021326-50bc (settled worker, no live pane, tier3 model). Executor (person-opened /task session) took over dispatch via Orca Run run_c974cafd0eb6 with worker-start, verified Tier1b (backend claude-sonnet-5-5 in live slot T1bModel01). See Task Log entry "coordinator re-bind refused".
- 2026-11-12 22:44 UTC: duplicate-dispatch incident (two concurrent producers of page-1; both disclosed; one complete file; process correction: one orca call per Bash). See Task Log entry "duplicate-dispatch incident logged".
- Bootstrap additions accepted: page-1 digest (check PASS 2026-11-12), page-2 digest (check PASS 2026-11-12), reconciliation (losslessness check PASS 2026-11-12). Zero additions were accepted before these.

## Inventory

| Consumer item ID | Exact path or pinned URL/revision/passage | Purpose | Accepted | Producer/evidence | Partition | Disposition | Replacement/acceptance evidence |
|---|---|---|---|---|---|---|---|
| 1.1 | `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/prep-pages/reconciliation.md` | Consuming root for item 1.1: merged scope-boundary + construction-gate boundary replacing the 1092-line raw baseline corpus for this consumer | yes | dispatches ctx_0b13838d4d59 (producer), ctx_aa2c9a7c8b1d (verifier); `qa/prep-pages/reconcile-check.md` VERDICT: PASS (line 108), 0 blocking, 7 minor | whole file (481 lines) | consuming | none (this IS the root; not a replacement of anything accepted earlier) |
| 1.1 | `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/prep-pages/page-1-scope-boundary.md` | Scope-boundary digest of 6 baseline inputs; superseded for 1.1 by the reconciliation root | yes | dispatches ctx_8e984f6299f6 + ctx_99fa431d0dfe (duplicate-dispatch incident, both disclosed, merged output), check ctx_b47369a2ad50 `qa/prep-pages/page-1-check.md` VERDICT: PASS (line 70), 0 blocking, 4 minor | whole file (194 lines) | audit-only | reconciliation root; losslessly covered per `qa/prep-pages/reconcile-check.md` PASS (every digest element survives, no false dedup) |
| 1.1 | `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/prep-pages/page-2-construction-gates.md` | Construction-gate digest of 6 QA reports; superseded for 1.1 by the reconciliation root | yes | dispatch ctx_d9fb785d1b09 (producer), check ctx_838ddd220886 `qa/prep-pages/page-2-check.md` VERDICT: PASS (line 58), 0 blocking, 3 minor | whole file (127 lines) | audit-only | reconciliation root; losslessly covered per `qa/prep-pages/reconcile-check.md` PASS |
| 1.1 | `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/prep-pages/page-1-check.md` | Independent PASS evidence for the page-1 digest | yes | dispatch ctx_b47369a2ad50 | whole file (72 lines) | audit-only | cited within reconciliation section 7; evidence preserved, not separately consumed |
| 1.1 | `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/prep-pages/page-2-check.md` | Independent PASS evidence for the page-2 digest | yes | dispatch ctx_838ddd220886 | whole file (60 content lines + trailing blank) | audit-only | cited within reconciliation section 7; evidence preserved, not separately consumed |

## Fixed baseline inputs (kept in consuming paragraphs, not replacable by this inventory)

The 12 baseline inputs (BUILD-REQUEST.md, research-notes.md, scope-01..04, six construction QA reports) remain fixed baseline corpus named by the task's consuming items; their aggregate coverage for item 1.1 is discharged through the accepted page digests and reconciliation above, per the item's own bootstrap clause. Later items (1.2 onward) re-select their own Accepted=yes AND Disposition=consuming rows from this inventory; explicit zero consuming rows is valid when an item has no registered additions.

## Registration notes

- Every later dispatch that accepts an addition registers its rows here BEFORE the dependent consumer runs, with the consumer's full item ID including any cycle suffix.
- Local partitions are bounded to at most six research files; synthesis partitions to at most four synthesis files; each lens splits through declared expansion regions rather than dropping coverage.
- No accepted addition may be omitted because it postdates the initial baseline.
