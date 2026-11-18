```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.76
citations_total: 139
citations_revalidated: 139
citations_dropped: 1
citations_inferred: 2
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (UC-1 pre-execution, Tier 2, `--t2-engine shadow`)

> **Status: partial.** The evidence validator dropped 1 citation (a wrong plan line number, listed under Grounding Gaps), and section 11.2 forces `partial` for any drop. No finding was lost: the claim behind the dropped citation holds and is restated against the right line. No finding is blocking; two are MAJOR.

- Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines). Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks).
- Temporal anchor: the spec says it read master `e8db2fe66`. The plan was executed later, so HEAD holds the finished feature. All repository facts were read from a `git archive` of `e8db2fe66` (`artifacts/base-e8db2fe6/`), never from HEAD; a claim true only at HEAD is later change, not a plan defect.
- Panel: analyzer (sonnet class), qa (haiku class), refactorer (opus class); blind calibration by opus-class calibrators (`calibrator_diversity: degraded`, no disjoint class); vendor diversity `single`. Debate judge is the orchestrator session (sonnet class), so `judge_class_collision: true`. Panel parity with the legacy rotation: true. Findings-block compliance: 3 of 3 on first parse.
- Convergence 0.9333 (14 of 15 diff points; unresolved: card layout). Invariant probe: 13 entries, 0 HIGH unaddressed, 2 MEDIUM unaddressed (INV-012, INV-013).

## Verdict

The plan is close to ready. Ten findings, none blocking: **M1** and **M6** are MAJOR, the other eight MINOR. M1 and M2 originate in the spec text itself, so a spec amendment is recommended next to the plan fix.

## Coverage (Step 1B.0)

- Pass 1 (labeled IDs): 0 hits, so `coverage_pct` is null and `coverage_degraded: parsed-sparse` (34 inferred > 0 parsed) forbade a Tier 1 stop.
- `coverage_pct_union` 0.8824 (30 of 34 rows matched by the 0.6 containment rule); `S_dev_density` 0.1176; `unmapped_requirements_union`: INF-008, INF-016, INF-019, INF-032. The reviewers examined these four and found them covered in substance (lexical misses, not plan gaps). INF-035 matched Task 4 at 0.6667 although the docs rows belong to Task 13: a false positive of the same rule.
- No inferred row was dropped by the validator.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:6 | containment Task 12(1.0) |
| INF-002 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | containment Task 8(0.8889) |
| INF-003 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | containment Constraints(0.7778) |
| INF-004 | No new `MonitorState`. | source.md:51 | containment Task 10(1.0) |
| INF-005 | No `gh` or `git` word on any line, comments included (F6). | source.md:75 | containment Constraints(0.8571) |
| INF-006 | maps, first match wins | source.md:112 | containment Task 4(0.75) |
| INF-007 | observed = read.transitions - guard.baseline | source.md:118 | containment Task 4(0.8) |
| INF-008 | `HALT_UNAVAILABLE(timeline_unreadable)` | source.md:140 | none (0.0) |
| INF-009 | `push_completed` and `read.head_sha == target_sha` | source.md:156 | containment Task 4(0.75) |
| INF-010 | re-enter `release_decision` with `push_completed=True` | source.md:166 | containment Task 4(1.0) |
| INF-011 | Add to `EventType` in `models.py` (43 to 45 | source.md:175 | containment Task 2(1.0) |
| INF-012 | `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` | source.md:184 | containment Task 3(0.75) |
| INF-013 | the whole record is erased (the fold returns `None` | source.md:201 | containment Task 3(0.8333) |
| INF-014 | `original_is_draft` is never read from GitHub after the first record | source.md:208 | containment Task 3(0.8333) |
| INF-015 | `DEFAULT_MERGE_GUARD = "draft"` | source.md:214 | containment Task 6(1.0) |
| INF-016 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none (0.4) |
| INF-017 | Modelled on `scripts/retrigger-review.sh` | source.md:221 | containment Task 7(1.0) |
| INF-019 | Exit codes: 0 success; 1 `gh` failure or failed verification | source.md:234 | none (0.5714) |
| INF-020 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | containment Task 8(0.75) |
| INF-021 | No new python fence | source.md:241 | containment Constraints(1.0) |
| INF-022 | update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | source.md:242 | containment Task 2(1.0) |
| INF-023 | PR #N is still mergeable; this run's fixes are local only. | source.md:247 | containment Task 9(1.0) |
| INF-024 | `fix_cycle_id` gives guard-enabled cycles an explicit id | source.md:251 | containment Task 8(0.7143) |
| INF-025 | needs one entry in `WRITE_VERB_CLASSIFICATION` | source.md:255 | containment Constraints(1.0) |
| INF-026 | Acceptance trace (must appear in this order in the run log) | source.md:270 | containment Task 11(0.8333) |
| INF-027 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` | source.md:301 | containment Constraints(1.0) |
| INF-028 | the final task runs the FULL suite | source.md:301 | containment Task 13(1.0) |
| INF-029 | protocol assertions that the Wave 0 bullet names `--resume`, is not gated on L3 or `draft` | source.md:322 | containment Task 9(0.7778) |
| INF-030 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | containment Task 1(0.8333) |
| INF-031 | Cite tests and constants by symbol name | source.md:362 | containment Constraints(1.0) |
| INF-032 | Declare dependencies completely, one `Depends on:` line per dependency | source.md:363 | none (0.3333) |
| INF-033 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | source.md:377 | containment Task 11(0.6) |
| INF-034 | `--merge-guard {draft,off}` in the argument-hint and the Options table | source.md:244 | containment Task 12(1.0) |
| INF-035 | Flag row and a paragraph | source.md:245 | containment Task 4(0.6667) |

Postscript: INF-018 and INF-036 were dropped at emission (quote not in the cited line) and never entered the matrix. The validator confirmed all 34 remaining quotes are substrings of their spec lines.

## Findings

### M1 (MAJOR, not blocking, unpassable-check): resume row 4 cannot be built from its signature

- Spec line 166 says row 4 re-enters `release_decision` with `push_completed=True`; `release_decision` needs `cycle_id`, `applied_edits` and `target_sha` (spec:107), and `resume_decision` receives none of them (spec:109). Task 4 repeats the row (plan:70) and only asserts the returned action (plan:77).
- An implementation that passes `target_sha=read.head_sha` makes release row 8's head check always true and passes every listed test; passing `applied_edits=0` releases with cause `no_edits` instead of `pushed`.
- Found by reviewers 1 and 3; reviewer 3's remedy chosen in the debate (78%). The defect originates in the spec.

### M2 (MINOR, contradiction): the Wave 0 bullet is specified two ways and placed too loosely

- Spec line 241 says the bullet "contains no L3 or `draft` condition" and also that "at L3 with `--merge-guard off` it prints the unprotected line once". Task 9 copies both (plan:137) and its acceptance fails a bullet that "names an L3 or `draft` condition" (plan:140). The test description on plan:137 is narrower ("no `L3 only` or `draft` gate wording"), so the defect is ambiguous wording, not an unpassable check (reviewer 1 downgraded it from MAJOR in Round 2).
- Task 9 only requires the bullet before the Wave 1 bullet; the branch for resume comes from the head-binding bullet at base `SKILL.md:275`, so the bullet must follow it.

### M3 (MINOR, other): the classification wording covers fewer verbs than the rule

- Constraints (plan:22) and spec 4.7 (spec:255) include git write verbs; Tasks 7, 8 and 12 say only `gh pr` or `gh api` (plan:108, plan:124, plan:182). Base `WRITE_VERB_RE` (`test_worker_contract.py:1098-1101`) also matches git write verbs, so a `git push` line in `refs/merge-guard.md` would fail Task 8's own run without a prompt to classify it.

### M4 (MINOR, other): same-file edits have no declared order; Task 1 dependencies are implied

- `test_static_grep.py` is edited by Task 5 (plan:85) and Task 7 (plan:108); `test_merge_guard_protocol.py` by Tasks 9, 10 and 12 with no order against Task 12 (plan:179-182). Tasks 9, 10, 12 and 13 use the Task 1 record but declare it only through other tasks (plan:137, plan:154, plan:182, plan:195). The ordering hazard is the real one (debate point X-001, 90%).

### M5 (MINOR, missing-requirement): nothing tests one cycle id across guard, push triad and re-trigger

- Spec 4.6 (spec:251) requires one id; `held_cycle_published` matches on it (spec:108), so a mismatch means a normal push never releases. Task 8 reuses it in prose (plan:124); no task asserts equality (plan:127-128, plan:170-171). Calibrated MINOR: the plan assigns the mint place through Task 1 O1.

### M6 (MAJOR, not blocking, missing-requirement): the FR-16 release retry has no bound and no test body

- Spec section 7 names the test (spec:315) and `settled(ready, failed)` yields `RELEASE_PENDING` (spec:205). Task 8 mentions one retry only in prose (plan:124, plan:129); Task 11 lists the test name without a case body (plan:166-169). No decision row enforces the one-retry bound.

### M7 (MINOR, other): every existing Wave bullet line is a classification key

- Task 10 protects two sentences and allows new sentences "after" them (plan:150, plan:154), but the whole Wave 6 line (`SKILL.md:282`) is a `WRITE_VERB_CLASSIFICATION` key (`test_worker_contract.py:1199-1206`), and so is the head-binding bullet. Appending a sentence makes the entry stale and fails `test_classification_table_has_no_stale_entries`.

### M8 (MINOR, missing-requirement): `guard_status` takes no halt reason

- Spec line 112 maps a `draft_guard_unavailable` halt to `unavailable`, but the function (spec:110) has no such input and Task 3 does not assign the case (plan:56-61). A read-failed engage writes no guard record, so the mapping would return `released` and Task 3's own test would lock that in.

### M9 (MINOR, missing-requirement): crash boundaries are narrower than spec section 7

- Spec section 7 requires crashes before and after each request and settle (spec:318); Task 11 covers the gap between request and settle plus the branch and publish cases (plan:166, plan:171).

### M10 (MINOR, missing-requirement): exit paths after engage need a held-report test

- The spec says any exit with unpublished work reports `held` with the clear command (spec:69, spec:313). The base SKILL has several post-engage halts (`fix_commit_failed`, `pr_head_mismatch`, `push_range_mismatch`, max rounds, validation); Task 11 names the test but no exit list (plan:166, plan:169). Found by the invariant probe (INV-012), not by a card. [INFERRED] that a halt skipping the report would leave a draft PR without the clear command: no card traced the SKILL exit text end to end.

## Rows checked and found sound

- No import cycle: `run_log` would import `merge_guard`, which imports only `conflicts`; `conflicts` imports `fsm` and `models`; none imports `run_log` or `recovery` (base `conflicts.py:34-35`, `recovery.py:37`).
- `_NEW_KEY_DEFAULTS` and the key-set asserts (`test_run_log.py:312-317`, `:403-404`); the 43 to 45 change covers every count claim (six places in the base copy, all in Task 2); `test_allowed_tools_cover_every_program` scans only `NEW_REFS`; `_RESOLUTION_SCRIPTS` tests are satisfied by a copy of `retrigger-review.sh`; `fix-<n>` and `ci-<n>` do not collide with `CONFLICT_CYCLE_PREFIXES`.

## Grounding Gaps

### Gap G-1 (dropped citation, section 11.2)

- **Hunk ref:** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:138` (cited in the merged draft for the narrower Task 9 test description)
- **Evidence missing:** line 138 is blank; the quoted wording is on line 137.
- **Why not classifiable:** not a deviation; a report-claim citation that failed re-Read.
- **Next evidence needed:** none: the claim is restated against plan:137 above. Counts toward `citations_dropped` and forces `partial`; no `grounding-gaps.yaml` was written because this is not an unclassifiable hunk (section 10.6 is UC-2).

## Inferred-claim audit

- `citations_inferred: 2` (the M10 consequence above; the calibrated-MINOR reasoning that a failing test would later reveal each gap).
- Inferred-fraction: 2 / 139 = 0.01.

## Recommendations

### Recommendation R-001: Give resume row 4 real release inputs
- **File:** .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
- **Change:** In Task 4, state that `cycle_id` comes from `guard.cycle_id`, `target_sha` from the dangling push record (branch `landed`) or the cycle's `push_completed` event (`published`), and `applied_edits` is at least 1; add an acceptance case that fails when `target_sha` is read from the live head. Amend spec lines 107-109 and 166 to match.
- **Verifier:** re-read Task 4 acceptance; the new case fails on an implementation using `read.head_sha`.
- **Linked deviation(s):** M1
- **Priority:** P0

### Recommendation R-002: Bound and test the FR-16 release retry
- **File:** .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
- **Change:** Give Task 11's `test_guard_release_failure_retries_once_and_reports` a case body (first release fails, one retry, `already in target state` is confirmed, `release_pending` is reported) and add the bound to Task 8's phrase checks.
- **Verifier:** re-read Task 8 and Task 11 acceptance for the retry bound.
- **Linked deviation(s):** M6
- **Priority:** P0

### Recommendation R-003: Make Task 10 and Task 9 respect whole-line pins and branch order
- **File:** .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
- **Change:** Say the Wave 3, 6 and 8 additions are separate bullet lines and every existing Wave bullet stays byte-identical as a whole line; require the Wave 0 bullet after the head-binding bullet; reword Task 9's acceptance to the listed forbidden phrases; amend spec line 241.
- **Verifier:** `uv run pytest tests/skills/test_worker_contract.py -q` passes after the SKILL edits.
- **Linked deviation(s):** M2, M7
- **Priority:** P1

### Recommendation R-004: Assert one cycle id and enumerate held exits
- **File:** .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
- **Change:** Add a Task 11 assertion that the guard, push-triad and `rereview_requested` cycle ids are equal; enumerate the held exits (spec D7 plus the base SKILL halts) in Task 11 and extend the crash cases to all request and settle boundaries.
- **Verifier:** re-read Task 11 acceptance for the equality assertion and the exit list.
- **Linked deviation(s):** M5, M9, M10
- **Priority:** P1

### Recommendation R-005: Fix classification wording, task order and the guard_status halt case
- **File:** .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
- **Change:** Say "every line that `WRITE_VERB_RE` matches" in Tasks 7, 8 and 12; add `Depends on: Task 5` to Task 7, `Depends on: Task 10` to Task 12 and `Depends on: Task 1` to Tasks 9, 10, 12, 13; assign the `draft_guard_unavailable` report to the SKILL in Task 3.
- **Verifier:** re-read the Depends-on lines and the Task 3 acceptance.
- **Linked deviation(s):** M3, M4, M8
- **Priority:** P2
