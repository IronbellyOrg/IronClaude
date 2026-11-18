<!-- Merged output of the adversarial pipeline (Step 5, merge-executor) -->
<!-- Base variant: Variant 3 (reviewer-3 card, opus class), variant-3-original.md -->
<!-- Incorporated: Variant 1 (F1, F2), Variant 2 (F1, F2), invariant probe (INV-001, INV-002, INV-006) -->
<!-- Merge date: 2026-11-13 -->
<!-- Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md (cited "spec") -->
<!-- Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (cited "plan") -->

# Merged Findings (UC-1 pre-execution review of the plan against its spec)

All findings are non-blocking. Severity follows the Round 2 consensus of the debate. Line cites are to the spec and plan files named above, re-read at merge time. Source variants: V1 = variant 1 (analyzer), V2 = variant 2 (qa), V3 = variant 3 (refactorer, base), INV = invariant probe.

| id | severity | blocking | category | claim | source variants | evidence |
|----|----------|----------|----------|-------|-----------------|----------|
| M1 | MEDIUM | false | missing-requirement | No task writes or tests the conversion of the camelCase `--read` JSON (`isDraft`, `headRefOid`, `autoMergeRequest`) into the snake_case `GuardRead`; Task 3 makes only the dataclass, so the ref prose and the Task 11 driver would each invent an unchecked mapping. A malformed read falls into the unreadable path and holds (spec:117), which bounds the harm. | V3 F1, V1 F1 | spec:88-90, spec:117, spec:230; plan:56, plan:124, plan:166 |
| M2 | MEDIUM | false | safety (spec defect copied by the plan) | A guard held from cycle fix-1 keeps `cycle_id` fix-1 when fix-2 gets `NOOP(already_held)`; on a crash before fix-2 pushes, `held_cycle_published` returns true from fix-1's push and resume row 4 re-enters release, so the PR can become ready with fix-2's fixes local only if resume passes fix-1's head (or any sha equal to the pushed head) as `target_sha` (the fold does not reassign `cycle_id` on a `NOOP`; that is an inference from the tables, not a quoted line). The spec also never says which `target_sha` resume passes to release row 8. No plan task or test covers a guard held across two cycles. HEAD REBIND/`cycle_rebound` is HEAD-only evidence, not evidence for this plan. | V3 F2, V1 and V2 Round 2, INV-006 | spec:69, spec:107-109, spec:139, spec:156, spec:166; plan:70, plan:75, plan:77, plan:124 |
| M3 | MEDIUM | false | safety | Release row 7 (`applied_edits == 0` gives `RELEASE(no_edits)`) precedes the published-head check in row 8, so a zero-edit cycle can release a guard that still holds an earlier cycle's unpublished fix (cycle 1 edits and its push is held, cycle 2 makes no edits, the PR is readied with cycle 1's commit still local). The plan requires exactly this release. Probe-only finding, one agent. | INV-001 | spec:69, spec:155, spec:156; plan:75, plan:166 |
| M4 | LOW | false | unpassable-check | Task 7 adds the script to `_RESOLUTION_SCRIPTS` only after reading the purpose of that list (Task 1 O2), yet its acceptance criterion unconditionally requires passing the `_RESOLUTION_SCRIPTS` resolution tests; if O2 says no, the criterion is vacuous or cannot be met. | V3 F3, V1 F2 | plan:108, plan:113; spec:299 |
| M5 | LOW | false | missing-requirement | Release needs this cycle's applied-edit count, not the run-wide `applied_edits` field. The plan names the per-cycle meaning but no source for the number (no core helper, no protocol test); Task 4 tests only prove the pure function given a correct count. | V3 F4 | spec:107; plan:70, plan:75, plan:124 |
| M6 | LOW | false | contradiction | The guard record type is inconsistent: the spec's fold returns a dict and Task 5 reads it with `["phase"]`, while the decision rules Task 4 copies use attribute access (`guard.baseline`, `guard.phase` in spec:118-123; `guard.owned_draft` in spec:137-138). Notation inconsistency that causes rework, not a silent bug. | V3 F7 | spec:118-123, spec:137-138, spec:187; plan:70, plan:90 |
| M7 | LOW | false | missing-requirement | Tasks 9, 10, 12 and 13 consume Task 1's `pre-build-gate.md` record but declare no `Depends on: Task 1`, against the spec rule "a task depends on every earlier task whose output it imports or consumes". Order is preserved transitively (9 via 6, 10 via 9, 12 via 6, 13 via 2), so no execution failure is shown. | V2 F1 | spec:363; plan:134-137, plan:148-154, plan:179-182, plan:190-199 |
| M8 | LOW | false | missing-requirement | Task 13 gives `docs/user-guide/flags.md` only a values/default row; the spec gives one row for both guides ("Flag row and a paragraph: what it does, the clear command, `held` meaning, default on"), the plan splits the row to `flags.md` and the paragraph to `commands.md`, and the acceptance criterion permits that split; whether each guide needs both is ambiguous. | V2 F2 | spec:245; plan:195-198 |
| M9 | LOW | false | other | The scenario tests run a driver written in Task 11, not the engage, release and resume steps in the SKILL and ref prose; Task 8 only checks that phrases are present, so prose that disagrees with the driver (step order, which `target_sha` or `cycle_id` is passed) still passes. This mirrors the spec's fixture request, so it is advisory. | V3 F5 | spec:322; plan:129, plan:166 |
| M10 | LOW | false | missing-requirement | The PR-body release-gate statement and the `--merge-guard off` rule for the PR-opening run are recorded only in Task 1's artifact (the release-gate fact itself also sits in plan constraints, plan:24 and plan:26); Task 13's `final-checks.md` does not carry them forward, and Task 12 puts a PR-body remark into the user-facing command doc. A handoff improvement, not a proven omission. | V3 F6 | spec:326; plan:24, plan:33, plan:182, plan:195 |
| M11 | LOW | false | other | Engage row 8 (`HALT_UNAVAILABLE(timeline_unreadable)`) precedes row 10 (`SKIP_ALREADY_DRAFT`), so an originally-draft PR with an unreadable timeline halts before any edit instead of being skipped. This is a spec-level ambiguity between spec:62 (first engage finds a draft PR: skip) and spec:68 (timeline unreadable at engage: halt before any edit), which the plan copies as "all 11 rows". | INV-002 | spec:62, spec:68, spec:140, spec:142; plan:70 |

## Refuted or dropped

- V3 claim "Dependency lines checked against spec:363; all complete": refuted and withdrawn by V3 in Round 2 (false for Tasks 9, 10, 12, 13; see M7).
- V2 F3 (coverage-matrix note about the reviewer's own matrix): dropped in Round 2 as not a plan defect.
- T1 candidate 5 (the `guard is None` path for engage rows 2 and 5-7): refuted; the row-10 test must pass `guard=None` through rows 2 to 9 (spec:142, plan:73).
- T1 candidate 6 (`from __future__ import annotations` counts as an import): refuted as a defect; no plan test checks the exact import list.
- V1 and V2 severity MINOR for the GuardRead adapter: superseded by the MEDIUM consensus (M1).
- Probe INV-003, INV-004, INV-005: kept in invariant-probe.md only (LOW, weak or addressed).

## Post-merge validation

- Structure: 11 findings M1..M11 with unique ids; every row has blocking=false, severity, category, claim, sources and evidence cites.
- Line cites were re-read against the spec and plan files named in the header (spec:69, 88-90, 107-109, 117-123, 139-142, 155-156, 166, 187, 230, 245, 322, 326, 363; plan:24, 33, 56, 70, 73-77, 90, 108, 113, 124, 129, 134-137, 148-154, 166, 179-182, 190-199). Cites for spec:299 and plan:90 are taken from the variant findings blocks; spec:299 was not re-read.
- Contradiction re-scan: no two findings disagree; M2 and M3 are independent paths to the same safety rule (spec:69) and are kept separate because their triggers differ.
- No finding or citation was added beyond the inputs.
