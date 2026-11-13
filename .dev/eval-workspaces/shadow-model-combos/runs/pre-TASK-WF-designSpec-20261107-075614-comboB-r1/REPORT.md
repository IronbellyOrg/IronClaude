```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.68
citations_total: 124
citations_revalidated: 124
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report: pre-execution review of the pr-submit merge-guard plan (issue 375)

Run: `pre-TASK-WF-designSpec-20261107-075614-comboB-r1` (shadow measurement run, combo B: orchestrator and judge on the sonnet alias). Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`. Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks).

**Verdict.** No blocking finding. 3 MEDIUM and 8 LOW findings. Status is `partial` because the evidence validator dropped 1 citation (plan:73-74 under M11) and because the base selection of the adversarial merge was abbreviated (see Notes). Tier 2 ran (pinned with `--tier 2`), engine `shadow`; the legacy debate and merge stayed authoritative.

**What matters.** Two MEDIUM findings (M2, M3) touch the guard's own safety rule that unpublished work keeps the PR draft (spec:69). Both are defects in the spec's decision tables that the plan copies, not plan drift. Recommend amending the spec and adding two scenario criteria to the plan before execution. This package was already executed (the merged feature at HEAD added a `REBIND` action for the M2 case, HEAD-only evidence, not evidence about this plan).

## Coverage (Step 1B)

- Pass 1 (labelled IDs): 0 parsed rows. The spec labels FR-1..FR-23, F1..F13, G1..G6, O1..O4; none match the ID pattern. `coverage_pct` = null (parsed-only), `coverage_degraded: parsed-sparse` (73 inferred rows against 0 parsed), which forbids a Tier 1 stop.
- Pass 2 (73 inferred rows, each quote verified verbatim at its cited spec line by script): 63 matched to a task by containment, 10 unmatched. `coverage_pct_union` = 0.863, `S_dev_density` = 0.137.
- The 10 unmatched rows (INF-004, 006, 015, 019, 043, 044, 046, 062, 067, 069) were checked by reviewer 2 against the plan; all ten are carried by Tasks or Constraints in different words. They are mechanical misses, not plan gaps.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | Task 8 (0.889) |
| INF-002 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | Task 8 (0.778) |
| INF-003 | engage at the first verified Medium-or-higher finding routed to a fix | source.md:6 | Task 8 (0.875) |
| INF-004 | the core DECIDES and the SKILL performs | source.md:51 | none (best Task 1 0.25) |
| INF-005 | No new `MonitorState`. | source.md:51 | Task 10 (1.0) |
| INF-006 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none (best Task 8 0.556) |
| INF-007 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger | source.md:58 | Task 8 (0.692) |
| INF-008 | Remediation is unprotected: --merge-guard off. | source.md:59 | Task 9 (1.0) |
| INF-009 | PR #N is still mergeable; this run's fixes are local only. | source.md:60 | Task 9 (1.0) |
| INF-010 | Read, decide, request, `--to draft`, settle. Print the clear command once. | source.md:61 | Task 8 (0.667) |
| INF-011 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | Task 3 (0.857) |
| INF-012 | Release, cause `no_edits`. | source.md:63 | Task 4 (1.0) |
| INF-013 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | Task 8 (1.0) |
| INF-014 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | Task 8 (0.75) |
| INF-015 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none (best Task 3 0.545) |
| INF-016 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | Task 8 (0.714) |
| INF-017 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | Task 8 (1.0) |
| INF-018 | PR stays draft; report `held` with the clear command. | source.md:69 | Task 8 (0.857) |
| INF-019 | No `gh` or `git` word on any line, comments included (F6). | source.md:75 | none (best Task 3 0.571) |
| INF-020 | Imports only `enum`, `dataclasses`, `re`, `.conflicts.is_conflict_cycle`. | source.md:75 | Task 3 (1.0) |
| INF-021 | Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | Task 3 (0.667) |
| INF-022 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | source.md:102 | Task 3 (0.667) |
| INF-023 | Returns `None` when the log holds no guard record. | source.md:103 | Task 3 (0.833) |
| INF-024 | Guard requests with no matching settle, matched by `idempotency_key` | source.md:104 | Task 3 (0.833) |
| INF-025 | `applied_edits` is THIS cycle's count of applied edits | source.md:107 | Task 4 (1.0) |
| INF-026 | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id` | source.md:108 | Task 3 (0.778) |
| INF-027 | a test imports both modules and asserts equality | source.md:109 | Task 3 (0.667) |
| INF-028 | phase `HELD` gives `held` | source.md:112 | Task 3 (1.0) |
| INF-029 | observed = read.transitions - guard.baseline | source.md:118 | Task 4 (0.8) |
| INF-030 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:127 | Task 4 (0.6) |
| INF-031 | `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) | source.md:133 | Task 4 (0.6) |
| INF-032 | `ENGAGE`; `notes` carries `auto_merge_armed` when set | source.md:143 | Task 4 (0.8) |
| INF-033 | `push_completed` and `read.head_sha == target_sha` | source.md:156 | Task 4 (0.75) |
| INF-034 | `REPORT_HELD` (no mutation; prints the clear command) | source.md:164 | Task 8 (0.6) |
| INF-035 | Each reason has its own test. | source.md:165 | Task 4 (0.667) |
| INF-036 | re-enter `release_decision` with `push_completed=True` | source.md:166 | Task 4 (1.0) |
| INF-037 | 43 to 45, update the docstring | source.md:175 | Task 2 (1.0) |
| INF-038 | appended and fsynced BEFORE the draft/ready call | source.md:177 | Task 7 (0.6) |
| INF-039 | default `None`, added to `_NEW_KEY_DEFAULTS` | source.md:187 | Task 5 (0.75) |
| INF-040 | the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`) | source.md:201 | Task 3 (0.889) |
| INF-041 | `original_is_draft` is never read from GitHub after the first record | source.md:208 | Task 3 (0.833) |
| INF-042 | `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | source.md:215 | Task 6 (1.0) |
| INF-043 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none (best Task 12 0.4) |
| INF-044 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none (best Task 6 0.429) |
| INF-045 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing | source.md:221 | Task 7 (0.882) |
| INF-046 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none (best Task 8 0.5) |
| INF-047 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | Task 8 (0.75) |
| INF-048 | No new python fence | source.md:241 | Task 9 (1.0) |
| INF-049 | update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | source.md:242 | Task 2 (1.0) |
| INF-050 | Overlay note: the guard phases are fold values, not `MonitorState` members. | source.md:243 | Task 10 (0.875) |
| INF-051 | `--merge-guard {draft,off}` in the argument-hint and the Options table | source.md:244 | Task 12 (1.0) |
| INF-052 | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | source.md:245 | Task 13 (0.778) |
| INF-053 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247 | Task 8 (0.889) |
| INF-054 | The SKILL mints it at the end of Wave 3 | source.md:251 | Task 8 (1.0) |
| INF-055 | The entries are added after the text of each file is final, as the last step of the task that writes the file | source.md:255 | Task 8 (0.667) |
| INF-056 | Acceptance trace (must appear in this order in the run log): | source.md:270 | Task 11 (0.833) |
| INF-057 | phase stays `HELD`; report `merge_guard: held` plus the clear command | source.md:275 | Task 8 (0.625) |
| INF-058 | `not_landed` keeps the PR draft (row 5); `ambiguous` holds (row 6). | source.md:279 | Task 4 (0.857) |
| INF-059 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:281 | Task 8 (0.75) |
| INF-060 | export the public guard names | source.md:291 | Task 5 (1.0) |
| INF-061 | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441` | source.md:299 | Task 2 (0.667) |
| INF-062 | Never stage `.claude/`. | source.md:301 | none (best Task 3 0.333) |
| INF-063 | the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record | source.md:301 | Task 1 (0.857) |
| INF-064 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | Task 1 (0.833) |
| INF-065 | The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. | source.md:326 | Task 1 (1.0) |
| INF-066 | Cite tests and constants by symbol name | source.md:362 | Task 1 (0.6) |
| INF-067 | The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet. | source.md:364 | none (best Task 9 0.583) |
| INF-068 | Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task. | source.md:368 | Task 2 (0.909) |
| INF-069 | Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | none (best Task 8 0.556) |
| INF-070 | the plan passes `published` and the recovery branch strings of F13 | source.md:375 | Task 8 (0.714) |
| INF-071 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | source.md:377 | Task 11 (0.7) |
| INF-072 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | Task 3 (1.0) |
| INF-073 | the script test for a missing `jq` (exit 127) | source.md:322 | Task 7 (1.0) |

Postscript: no inferred row was dropped by validation. One row (INF-060) cited the wrong line at emission, was dropped by the script at that point and re-emitted with the corrected line (spec:291) before the matrix was used.

## Findings

All findings are non-blocking. Source variants: V1 analyzer card, V2 qa card, V3 refactorer card, INV invariant probe. Citations are `spec:` (source.md) and `plan:` (the tasklist).

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

### Refuted or dropped in the debate

- V3 claim "Dependency lines checked against spec:363; all complete": withdrawn (false for Tasks 9, 10, 12, 13; see M7).
- V2 F3 (note on the reviewer's own coverage matrix): dropped, not a plan defect.
- T1 candidate 5 (`guard is None` rows) and candidate 6 (`from __future__` import): refuted by reviewers 1 and 3.
- Evidence validator: citation plan:73-74 under M11 dropped (it concerns `classify_toggles` tests, not engage ordering). Six claim wordings corrected (M2 conditional on the `target_sha` resume passes, M4, M6, M8, M10, M11).

## Recommendations

### Recommendation R-001: Settle the held-guard cross-cycle rule before building (M2)
- **File:** `source.md` section 4.1 and 4.2, and plan Task 4 and Task 11
- **Change:** State which event moves `cycle_id` when a held guard meets a later cycle, and which `target_sha` resume passes to release row 8; add one scenario criterion for a guard held across two cycles.
- **Verifier:** a Task 11 test where cycle 1 holds, cycle 2 crashes before its push, and resume leaves the PR draft.
- **Linked deviation(s):** M2
- **Priority:** P1

### Recommendation R-002: Do not let a zero-edit release hide an earlier unpublished fix (M3)
- **File:** `source.md` release table row 7, plan Task 4 criterion on a zero-edit cycle after a fixing cycle
- **Change:** Condition `RELEASE(no_edits)` on the guard holding no earlier unpublished commit, or state why that cannot occur.
- **Verifier:** test with cycle 1 edits and held push, cycle 2 zero edits: the decision is `HOLD`.
- **Linked deviation(s):** M3
- **Priority:** P1

### Recommendation R-003: Assign the `--read` JSON to `GuardRead` conversion (M1)
- **File:** plan Task 3 (or Task 4)
- **Change:** Add a function and a test that feeds the exact JSON line printed by `set-draft-state.sh --read` (camelCase keys, `autoMergeRequest` as printed) and returns a `GuardRead`.
- **Verifier:** `uv run pytest tests/pr_submit/test_merge_guard.py -q` including that test.
- **Linked deviation(s):** M1
- **Priority:** P1

### Recommendation R-004: Plan hygiene, low risk (M4 to M11)
- **File:** plan Tasks 7, 9, 10, 12, 13 and the Task 4 and Task 5 criteria
- **Change:** Add `Depends on: Task 1` to Tasks 9, 10, 12, 13 (M7); make Task 7 criterion 3 conditional on the O2 outcome (M4); name the source of the per-cycle applied-edit count (M5); choose dict or attribute access for the guard record (M6); add the paragraph to `flags.md` or say the split is intended (M8); carry the PR-body gate into Task 13's `final-checks.md` (M10); note the engage row 8 versus row 10 ordering in the spec (M11).
- **Verifier:** re-run `/sc:reflect --mode pre` on the amended plan; the M4 to M11 findings no longer appear.
- **Linked deviation(s):** M4, M5, M6, M7, M8, M9, M10, M11
- **Priority:** P2

## Inferred-claim audit

- `citations_inferred: 1` (the M2 inference that the fold does not reassign `cycle_id` on a `NOOP`; it is stated as an inference in the finding).
- Inferred-fraction: 1 / 124 = 0.01.

## Notes (run mechanics)

- Panel (shadow): reviewer 1 analyzer sonnet class (self-report claude-gw-tier1b), reviewer 2 qa haiku class (self-report "OpenAI GPT", `identity_mismatch_suspected: true`, pin is claude-haiku-5-5), reviewer 3 refactorer opus class (self-report claude-gw-tier1a). Identity source `requested-pinned`; executor class unresolved, so no claim of verified independence.
- Calibration: T1 card C = 0.72, reviewer cards 0.57, 0.76, 0.72, blind-calibrated by an opus-class calibrator (`calibrator_diversity: degraded`, Anthropic-only).
- Debate: 3 advocates, rounds 1 and 2, invariant probe (0 HIGH, 2 MEDIUM, 3 LOW unaddressed), convergence 1.0 with a caveat that Round 2 positions moved to a common MEDIUM after the advocates read each other; the probe, not the advocates, raised M3 and M11. Judge identity not named by the adversarial contract (`judge_identity: unknown`); the orchestrating session ran on the sonnet-class alias.
- Deviations from the full adversarial protocol, recorded rather than hidden: base-selection quantitative metrics estimated by the orchestrator (not scripted), qualitative rubric reported as dimension subtotals (no 30-row CEV table), no reverse-order second pass, and the 73 inferred-row quotes were verified by script instead of by the evidence validator.
- `verify-citations` flagged all 38 card citations as `not-in-snapshot` because the input snapshot lists bare file names while the cards cite repo-relative paths; the flagged set joined the validator re-read set. Snapshot path form should be repo-relative in future runs.
