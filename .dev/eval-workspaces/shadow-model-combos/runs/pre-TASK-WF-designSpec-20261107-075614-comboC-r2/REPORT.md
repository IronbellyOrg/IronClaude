```yaml
contract_version: 1.8.0
status: partial                      # 2 of 64 merged-finding citations dropped by the evidence validator
mode: pre
tier_reached: 2
confidence_calibrated: 0.74          # mean of the three blind-calibrated Tier 2 cards (0.73, 0.74, 0.75); Tier 1 card was 0.59
citations_total: 148                 # 64 in merged findings + 84 inferred-requirement rows
citations_revalidated: 148
citations_dropped: 2
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
reachability_gate_ran: false         # UC-1: not applicable
reachability_skip_reason: null
```

# Reflect report: UC-1 pre-execution audit, TASK-WF-designSpec-20261107-075614 (pr-submit merge guard plan)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines). Plan: `.../TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks). Run: `--mode pre --tier 2 --t2-engine shadow` (combo C of the model-combination experiment; run c-r2). Output: `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/`.

## Verdict

**Not ready to build as written.** The panel found 15 merged findings: 2 blocking (M-1 and M-2, both begin in the spec), 5 MAJOR non-blocking, 8 MINOR. Tier 2 ran because of the `--tier 2` pin (also rule 4, three domains, and rule 6, calibrated C 0.59 below 0.85). Coverage by the deterministic match is 70 of 84 inferred requirement rows (0.8333); the 14 unmatched rows are mostly lexical misses and are listed below. The merged verdict comes from the adversarial merge (`adversarial/merged-verdict.yaml`, convergence 1.0 after round 2).

Orchestrator note on severity, not a change to the merge: M-1 and M-2 are blocking because an advocate majority kept them so. M-1 is weaker than M-2: `release_decision` is a pure function, so a test for resume row 4 can pass explicit values; what is missing is a stated source for `target_sha` and this cycle's `applied_edits` on resume. M-2 stands on spec line 315 alone, because the retry behaviour is named in no table, fold row or criterion.

## Inferred requirements (Pass 2)

Pass 1 found 0 parsed ids (the spec labels FR-n, F-n, G-n, O-n, which the id pattern does not cover), so `coverage_pct` is null and `coverage_degraded` is `parsed-sparse`. Pass 2 emitted 86 rows; 2 were dropped at emission for a quote that is not verbatim in the cited lines (rows 61 and 80 of the extraction list, spec lines 255 and 362), 84 kept. Each kept quote was checked as a substring of the cited spec lines by `artifacts/coverage_calc.py`. Match rule: word containment >= 0.6 against a single `## Task` section. `S_dev_density` = 14/84 = 0.1667.

Postscript: no inferred row was dropped by the evidence validator, so `coverage_pct_union` (0.8333), `unmapped_requirements_union` and `S_dev_density` need no recompute.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:6 | Task 12 (1.0) |
| INF-002 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | Task 8 (0.8889) |
| INF-003 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | Task 8 (0.7778) |
| INF-004 | draft not label; engage at the first verified Medium-or-higher finding routed to a fix | source.md:6 | Task 8 (0.8) |
| INF-005 | Rule: the core DECIDES and the SKILL performs, the same split as the push triad and the re-trigger (NFR-6). No | source.md:51 | none (best 0.5385 Task 1) |
| INF-006 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none (best 0.5556 Task 8) |
| INF-007 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit | source.md:58 | Task 8 (0.6923) |
| INF-008 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | source.md:59 | Task 9 (1.0) |
| INF-009 | The final report prints "PR #N is still mergeable; this run's fixes are local only." | source.md:60 | Task 9 (0.8889) |
| INF-010 | Read, decide, request, `--to draft`, settle. Print the clear command once. | source.md:61 | Task 8 (0.6667) |
| INF-011 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | Task 3 (0.8571) |
| INF-012 | Release, cause `no_edits`. | source.md:63 | Task 4 (1.0) |
| INF-013 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | Task 8 (1.0) |
| INF-014 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | Task 8 (0.75) |
| INF-015 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none (best 0.5455 Task 3) |
| INF-016 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | Task 8 (0.625) |
| INF-017 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | Task 8 (1.0) |
| INF-018 | PR stays draft; report `held` with the clear command. | source.md:69 | Task 8 (0.8571) |
| INF-019 | No `gh` or `git` word on any line, comments included (F6). Imports only `enum`, `dataclasses`, `re`, `.conflic | source.md:75 | Task 3 (0.7692) |
| INF-020 | `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | Task 3 (0.6) |
| INF-021 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | source.md:102 | Task 3 (0.6667) |
| INF-022 | Guard requests with no matching settle, matched by `idempotency_key` | source.md:104 | Task 3 (0.8333) |
| INF-023 | so a zero-edit cycle after a fixing cycle still releases with `no_edits` | source.md:107 | Task 11 (0.8571) |
| INF-024 | whether written by the push triad or synthesized by recovery (`recovered: true`) | source.md:108 | none (best 0.375 Task 1) |
| INF-025 | a test imports both modules and asserts equality, because the core cannot import `recovery`. | source.md:109 | none (best 0.4545 Task 3) |
| INF-026 | phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded | source.md:112 | Task 3 (0.7273) |
| INF-027 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user a | source.md:127 | Task 4 (0.6) |
| INF-028 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:133 | Task 3 (1.0) |
| INF-029 | `RETRY_RELEASE` (release first, then re-decide) | source.md:137 | Task 1 (0.6) |
| INF-030 | `HALT_UNAVAILABLE(timeline_unreadable)` | source.md:140 | none (best 0.0 null) |
| INF-031 | `ENGAGE`; `notes` carries `auto_merge_armed` when set | source.md:143 | Task 4 (0.8) |
| INF-032 | `push_completed` and `read.head_sha == target_sha` | source.md:156 | Task 4 (0.75) |
| INF-033 | `HOLD(head_mismatch or push_not_completed)` | source.md:157 | none (best 0.3333 Task 4) |
| INF-034 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | source.md:164 | Task 3 (1.0) |
| INF-035 | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` | source.md:165 | Task 4 (1.0) |
| INF-036 | re-enter `release_decision` with `push_completed=True` | source.md:166 | Task 4 (1.0) |
| INF-037 | 43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117` | source.md:175 | Task 2 (0.7273) |
| INF-038 | appended and fsynced BEFORE the draft/ready call | source.md:178 | Task 7 (0.6) |
| INF-039 | `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` | source.md:184 | Task 3 (0.75) |
| INF-040 | `run_log.rebuild_state()` stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`) | source.md:187 | Task 5 (0.7778) |
| INF-041 | For a draft request that was the first guard record, the whole record is erased | source.md:201 | Task 3 (0.8571) |
| INF-042 | `original_is_draft` is never read from GitHub after the first record | source.md:208 | Task 3 (0.8333) |
| INF-043 | `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | source.md:215 | Task 6 (1.0) |
| INF-044 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none (best 0.4 Task 12) |
| INF-045 | `RunConfig` and `run_skill` do not change (F5) | source.md:217 | none (best 0.4 Task 6) |
| INF-046 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 1 | source.md:221 | Task 7 (0.875) |
| INF-047 | `gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest` | source.md:230 | Task 7 (0.8889) |
| INF-048 | `gh pr ready "$PR" --repo "$REPO" --undo` | source.md:231 | Task 7 (0.8) |
| INF-049 | Exit codes: 0 success; 1 `gh` failure or failed verification (the JSON line is still printed with `ok:false`); | source.md:234 | Task 7 (0.7059) |
| INF-050 | A verification mismatch after a mutation is `ok:false, error:"verify_failed"` | source.md:234 | Task 7 (0.8571) |
| INF-051 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | Task 8 (0.75) |
| INF-052 | The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `draft` condition | source.md:241 | Task 9 (1.0) |
| INF-053 | it must not contain the words `evidence-validator` or `conflict-intent.md` | source.md:241 | Task 9 (0.8571) |
| INF-054 | No new python fence | source.md:241 | Task 9 (1.0) |
| INF-055 | update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git` | source.md:242 | Task 2 (1.0) |
| INF-056 | Respect the wait-only sentences pinned at `test_static_grep.py:791`. | source.md:243 | Task 1 (0.7143) |
| INF-057 | `--merge-guard {draft,off}` in the argument-hint and the Options table | source.md:244 | Task 12 (1.0) |
| INF-058 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247 | Task 8 (0.8889) |
| INF-059 | uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested` | source.md:251 | Task 8 (0.8571) |
| INF-060 | With `--merge-guard off` nothing changes. | source.md:251 | Task 8 (0.8) |
| INF-062 | Acceptance trace (must appear in this order in the run log) | source.md:270 | Task 11 (0.8333) |
| INF-063 | Message names `--merge-guard off` and prints the clear command. | source.md:274 | Task 8 (0.875) |
| INF-064 | phase stays `HELD`; report `merge_guard: held` plus the clear command. | source.md:275 | Task 8 (0.625) |
| INF-065 | W6 blocks the push (INV-016 predicate 5), `release_decision=RELEASE(no_edits)`. | source.md:276 | none (best 0.3333 Task 4) |
| INF-066 | `classify_toggles == foreign` -> `settled(skipped, user_override)` -> phase `DISABLED`; the push and reply con | source.md:277 | none (best 0.4545 Task 3) |
| INF-067 | the request settles `skipped/not_applied`, the phase returns to `phase_before_request`, and the next cycle eng | source.md:278 | Task 3 (0.7273) |
| INF-068 | `not_landed` keeps the PR draft (row 5); `ambiguous` holds (row 6). | source.md:279 | Task 4 (0.8571) |
| INF-069 | The SKILL passes `published = held_cycle_published(events, guard)`, which is true; row 4 releases first | source.md:280 | Task 3 (0.8) |
| INF-070 | `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:281 | Task 8 (0.9) |
| INF-071 | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441` | source.md:299 | Task 2 (0.6667) |
| INF-072 | Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result | source.md:301 | Task 1 (0.9231) |
| INF-073 | Never stage `.claude/`. | source.md:301 | none (best 0.3333 Task 3) |
| INF-074 | Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests | source.md:301 | Task 2 (0.6364) |
| INF-075 | never injected strings | source.md:318 | Task 8 (0.6667) |
| INF-076 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | Task 3 (1.0) |
| INF-077 | the script test for a missing `jq` (exit 127) | source.md:322 | Task 7 (1.0) |
| INF-078 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | Task 1 (0.8333) |
| INF-079 | The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. | source.md:326 | Task 1 (1.0) |
| INF-081 | one `Depends on:` line per dependency | source.md:363 | Task 7 (0.75) |
| INF-082 | The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a  | source.md:364 | none (best 0.5833 Task 9) |
| INF-083 | Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | none (best 0.5556 Task 8) |
| INF-084 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | source.md:377 | Task 11 (0.7) |
| INF-085 | "no push after a `pr_not_open` halt" is asserted on `RunLog.read_events()` | source.md:377 | Task 11 (0.8333) |
| INF-086 | its acceptance criterion is a test that the literal line is in `SKILL.md` | source.md:374 | Task 1 (0.8571) |

Matcher caveat: a mapped row is only a word-overlap match. INF-086 maps to Task 1 (0.857) although Task 9 carries the L2-line test; the 14 unmapped rows are listed in the contract and checked in the next sections.

## Findings

Origin = where the defect starts (spec or plan), as tagged by the advocates in round 2. Citations are plan (`P`) and spec (`S`) line numbers from a fresh read this run; both files are in the input folder named above.

### M-1 (MAJOR, blocking, spec-origin): resume row 4 re-enters `release_decision` without its inputs
`release_decision` needs `target_sha` and this cycle's `applied_edits` (S 107-109). `resume_decision` takes neither (S 109), row 4 re-enters release (S 166), and the fold fields hold neither (S 190-191). Task 4 and its row-4 criterion copy the signature (P 70, 77). Fix: state where the SKILL gets both values on resume (for example from the held cycle's push event and a stored per-cycle edit count), and add a row-4 test that supplies them.

### M-2 (MAJOR, blocking, spec and plan): the FR-16 release retry has no row, fold rule or criterion
S 315 names "one retry, `already_in_state` counts as confirmed, `release_pending`" only as a test name. The release table (S 147-157) has no retry row, the script never prints `already_in_state` (S 228-234), Task 8 mentions "one retry" as prose (P 124) and Task 11 lists the test name only (P 166, 169). Fix: add the rule to the spec tables and a behavioural criterion to Tasks 4, 8 and 11.

### M-3 (MAJOR, not blocking, plan): nothing ties the guard, push triad and `rereview_requested` to one cycle id
S 251 requires one id and unchanged behaviour with `off`. Task 1 only records where the id is minted (P 37), Task 8 only names the place (P 127), and the trace test checks event order, not id equality (P 170). Fix: assert equality of the three ids in the Task 11 trace and with `off`.

### M-4 (MAJOR, not blocking, plan): the Wave 3 text test accepts an unconditional engage
P 153 says an unconditional "engage at the end of Wave 3" fails, but the test only checks that two phrases are present (spec line S 241 gives the bullet). Fix: assert the trigger phrase sits in a conditional clause ("only when ...") and that the sentence says once per cycle id.

### M-5 (MAJOR, not blocking, plan): Task 11 names twelve tests but asserts only some
P 169 requires the test names. Behavioural bullets exist for the trace, crash and forbidden-call tests (P 170-172), not for the rest, and the case list has no moved-head, unreadable-timeline or per-exit case (S 313, 317, 319). Resolved 2 of 3 in the debate. Fix: one asserted outcome per named test.

### M-12 (MAJOR, not blocking, plan): the fsync-before-call order is untested
S 178-179 and 262 require the request to be appended and fsynced before the draft or ready call. In the plan the order exists only as ref prose (P 124); protocol tests assert phrase presence (P 128-129) and the Task 11 driver writes the order itself (P 166, 170). Adopted from the invariant probe (INV-011, HIGH, unaddressed): not debated, because depth `standard` has no further round. Fix: assert step order on the ref text and check call order against the log in a scenario test.

### M-6 (MINOR, spec): after a failed draft settle the fold sits at `RELEASE_PENDING` with `owned_draft` false
Engage row 6 then returns `HOLD(ownership_unproven)` (S 138, 199) and no document says what the SKILL does on that HOLD. Only the resume path reaches it, because a failed engage halts before any edit (S 68, 274).

### M-7 (MINOR, spec): Task 9 rejects "an L3 condition" while the same bullet must say "at L3 with off"
P 137-140 (quote: "carries no L3 or `draft` condition"); the same tension is in S 241. Fix: test the ref-load gate, not the word L3.

### M-8 (MINOR, spec and plan): `autoMergeRequest` conversion and the `transitions` value are untested
S 230 shows a boolean; Task 7 checks keys only (P 111); the value feeds only the `auto_merge_armed` note (S 143). [INFERRED] that `gh` returns an object or null (not checked offline).

### M-9 (MINOR, plan): the PR body and the opening run's `--merge-guard off` have no producing task
S 326; Task 1 only records the decision (P 33).

### M-10 (MINOR, plan): `not_applied` for a ready request is tested for one outcome
Only the return to `HELD` is a criterion (P 60); S 201 also returns to `RELEASE_PENDING` after a failed release.

### M-11 (MINOR, spec): "byte-identical" compares only the recorded start text
P 154 and P 33 against S 342 and 377; the existing pins are fragments, so a late edit passes.

### M-13 (MINOR, plan): `Depends on:` lines are incomplete
Tasks 9, 10, 12 and 13 consume Task 1's `pre-build-gate.md` without declaring Task 1, and Task 10 extends Task 8's files while listing only Task 9 (P 134-137, 148-150, 179-182, 190-195; rule at S 363).

### M-14 (MINOR, plan or spec): hygiene group
Plan line 25 calls limits "non-goals of ./source.md" (P 25; three of six come from the spec header, S 6, 57, 60; commit statuses, rulesets and concurrent runs do not); Phase string values undefined in Task 3, lowercase in Task 5 (P 90); `file:NNN` ban unchecked (P 124); Wave 8 test weaker than Wave 6 (P 153); `git status` wording (P 200); fold test list shorter than the spec table (S 196-206). [INFERRED] that git write verbs are missing from the classification steps (the plan lines that show it, P 22 and 108, are not cited).

### M-15 (MINOR, spec): four spec-origin warnings from the invariant probe
`guard.cycle_id` is never advanced by any fold row; a zero-edit release (S 155-156, P 75) can cover an unpublished earlier fix; a `landed` branch is not matched to the guard's cycle (S 166, P 76-77); drafting disarms auto-merge with no action on it (S 143). Warnings, not debated.

## Checked and held (no defect)

All 12 test names of S 305-320 appear in Task 11; every file in S 283-301 has a task; the 14 unmapped inferred rows are carried by the plan in other words (for example INF-030 `HALT_UNAVAILABLE(timeline_unreadable)` by Task 8's engage-halt text, P 129; INF-073 "never stage .claude/" by Task 13, P 200). The flag-inertness finding (V2:F9) was withdrawn: P 73 returns NOOP at ordinal 2 and with `off`, and P 172 forbids any `pr ready` call there.

## Panel and merge record

- Resolved panel (`panel/resolution.json`, unmodified): t1b-1 sonnet (claude-sonnet-5-5), t4-1 haiku (claude-haiku-5-5), t1a-1 opus (claude-opus-5-5); template `@reflect-pre`; parity true.
- Observed served models (from the agent transcripts, `model_observed` in each card header): claude-sonnet-5-5, claude-haiku-5-5, claude-opus-5-5, equal to the pins. Executor class unknown (`executor_class_resolved: false`).
- Cards: 3 of 3 complete, 27 findings as filed (7, 12, 8), 4 blocking as filed; first-parse findings-block compliance 3 of 3 (the cards use the heading `## Findings`; the panel copies in `panel/cards/` carry `## Findings block`). Calibration (opus, class not disjoint, `calibrator_diversity: degraded`): card C 0.73, 0.74, 0.75; per-finding confidences 27 of 27; Tier 1 card C 0.59.
- Cluster agreement 0.2552 (telemetry only); citation precheck 0 of 90 flagged on the repo-path snapshot (the plain snapshot flags all 90 `not-in-snapshot`, see `panel/precheck.json`).
- Debate: 3 advocates, round 1 convergence 0.90, round 2 convergence 1.00, invariant probe 12 rows (1 HIGH unaddressed, adopted as M-12). Base: reviewer-2 card (score 0.7527 against 0.6354 and 0.6046; scoring was done by the orchestrator, see `adversarial/adversarial/base-selection.md`). The merge judge was the orchestrator session (sonnet class, which is also reviewer 1's class): a class collision that is recorded, not avoided. The debate-orchestrator role was performed inline.
- Evidence validator (agent without a Write tool; the orchestrator wrote `artifacts/evidence-validation.md`): 64 merged citations, 2 dropped (S 311 for M-4, S 150 for M-6). Not a zero-drop pass.

## Grounding gaps

None filed (`grounding-gaps.yaml` not created). Limits that matter: the working tree already contains the feature (`merge_guard.py`, 45-member `EventType`), so grounding could not check pre-build facts; the merged requirements document (FR-1..FR-23) is not in the input, so FR ids are taken from the spec text.

## Inferred-claim audit

citations_inferred 3 (M-1 code-state claim, M-8, M-14 sub-claim) against citations_total 148: well below the WARN threshold.

## Recommendations

### Recommendation R-001: close the spec gaps behind M-1 and M-2 before building
Edit `source.md` sections 4.1 (`resume_decision` and release tables) so row 4 names its source for `target_sha` and `applied_edits`, and add the retry row; then add criteria to Task 4 and Task 8 that a wrong implementation fails. Verify: `uv run pytest tests/pr_submit/test_merge_guard.py -q` has one test per new row.

### Recommendation R-002: add failable criteria for M-3, M-4, M-5 and M-12 in Tasks 8, 10 and 11
Assert id equality across guard, push and `rereview_requested` (also with `off`), a conditional clause in the Wave 3 sentence, one asserted outcome per named scenario test, and request-before-call order. Verify by deleting each behaviour from a copy and seeing the test fail.

### Recommendation R-003: reword the Task 9 criterion (M-7) and fix the dependency lines (M-13)
Test that the Wave 0 bullet is not gated on L3 or `draft` for the ref load, while it may name L3 for the `off` line; add `Depends on: Task 1` to Tasks 9, 10, 12 and 13 and `Task 8` to Task 10.

### Recommendation R-004: sweep the MINOR items (M-6, M-8 to M-11, M-14, M-15) in one pass of the plan
Add the PR-body and `--merge-guard off` step (M-9), the `RELEASE_PENDING` branch (M-10), Phase string values (M-14), and decide the SKILL action on a HOLD at engage on resume (M-6). `--remediate` was not requested, so no remediation package was built.
