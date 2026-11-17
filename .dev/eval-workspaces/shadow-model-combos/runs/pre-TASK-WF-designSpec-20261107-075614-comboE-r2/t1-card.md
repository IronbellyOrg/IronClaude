# T1 reflection card (UC-1 pre): TASK-WF-designSpec-20261107-075614 vs its design spec

Run: pre-TASK-WF-designSpec-20261107-075614-comboE-r2. Plan = `TASK-WF-designSpec-20261107-075614.md` (13 tasks). Spec = `source.md` (design of the pr-submit merge guard, issue #375).
Paths below are repo-relative under `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/` (P = the plan file, S = source.md).

## Attribution note (read before judging any HEAD text)
This package already executed. The implementation landed in commit 0b8a5801d (#428), parent 0e486ab8d. Checked at the parent: EventType has 43 members (models.py docstring line 3 and class docstring line 24, `run_log.py` line 117), `conflicts.py` imports `.fsm` and `.models` only, `fsm.py` does not import `run_log` (no import cycle), `recovery.py` defines `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS` and writes `recovered: true`, the enum already has `FIX_APPLIED`, `PUSH_INITIATED`, `PUSH_COMPLETED`, `REREVIEW_REQUESTED`, `TERMINAL_HALTED`, no `plugins/` mirror of the pr-submit skill exists. The spec facts therefore hold at the parent. HEAD now carries the implementation, so a plan defect or gap claimed from HEAD text must be re-checked at 0e486ab8d. The audit is a plan-text audit: judge the plan and spec, not the shipped code.

## Coverage (Step 1B.0, two passes)
- Pass 1 (ID regex `R-|REQ-|SPEC-|T-`, fences skipped): 0 parsed IDs in the spec and 0 in the plan (the spec uses FR-n, F-n, G-n, O-n labels).
- Pass 2: 48 inferred rows INF-001..INF-048, every quote verified verbatim against its cited spec line (artifacts/coverage-matrix.json).
- Containment matching (>= 0.6 content-word ratio against one task section): 42 of 48 matched, `coverage_pct_union` 0.875, `coverage_pct` null (no parsed rows).
- `inferred_count` 48 > `parsed_count` 0: `coverage_degraded: parsed-sparse`, no Tier-1 stop; also pinned to Tier 2 by `--tier 2`.
- The 6 `none` rows are mostly matcher noise: INF-007 (merge_guard.py has no gh/git word: Task 3 states it), INF-012 (BRANCH constant equality test: Task 3 AC), INF-015 (engage row 3: Task 4 AC "each row"), INF-026 (RunConfig unchanged: Task 6 prose), INF-029 (verify_failed: Task 7 AC), INF-046 (cite by symbol name: Constraints bullet, no AC).

## Candidate gaps (hypotheses; none is final)
H1. Task 11 acceptance names only. Its first AC requires that twelve test names exist; behaviour ACs cover only the crash tests, the acceptance trace and the forbidden-call checks. A test named `test_guard_release_failure_retries_once_and_reports` that asserts nothing passes. The task prose never lists the release-failure retry, the unreadable-timeline-never-readies case or the moved-head case. Evidence: P:166, P:169, S:315, S:317, S:319.
H2. Cycle-id continuity is asserted by wording only. The spec says the SKILL mints one id at the end of Wave 3 and the push triad and `rereview_requested` reuse it (S:251); `held_cycle_published` depends on that id matching the `push_completed` event. Task 8 AC only requires the ref to state "the single place" and Task 10 checks that a Wave 3 bullet exists; no AC checks that the Wave 6 text or the ref says the push triad and the re-trigger reuse the id. Scenario tests append events with hand-matched ids. Evidence: P:124, P:127, P:150, S:108, S:251.
H3. Two pieces of glue have no owner. (a) `GuardRead` is "the parsed output of `--read`" (S:88-90) but the function list (S:99-110, P:56) has no parser from the script's JSON keys (`isDraft`, `headRefOid`, `autoMergeRequest`) to the dataclass fields (`is_draft`, `head_sha`, `auto_merge_armed`). (b) The request key `guard:<run_id>:<cycle_id>:<to>:a<k>` (S:184) has no builder and no AC checks the ref states the format. Both would be written in prose by the SKILL; the scenario driver builds both in test code. Evidence: S:88, S:184, S:230, P:56, P:124.
H4. Task 7 AC lists the `autoMergeRequest` key but not its type. The spec example prints a boolean (S:230) while `gh pr view --json autoMergeRequest` returns an object or null; a script that passes the object through satisfies the AC and breaks `GuardRead.auto_merge_armed`. Evidence: S:230, P:111.
H5. Byte-identical pins checked against start text only. Task 1 records "the literal start text" of the S5a sentence and the Wave 6 pre-push sentence (P:33); Task 10's AC says "byte-identical" by comparing with those constants (P:154). A prefix constant cannot detect an edit inside the sentence. Evidence: P:33, P:154, S:377 (spec section 10 says literal constants taken from the pins).
H6. Constraint without AC: protocol prose carries no `file:NNN` pointers (P:23, S:369). Task 8 prose repeats it (P:124) but its AC list tests `src/superclaude`, fences and `gh` scope only (P:128). Same plan-defect family as earlier shadow runs ("constraints without matching AC do not gate").
H7. Task 2 AC greps for "43" and expects no claim that the enum has 43 members (P:49). The parent `models.py` also has a comment "the 42nd-43rd" members of the conflict-cycle block, so the grep keeps matching a true statement; whether it passes depends on a judgment, not an exit code.
H8. Task 7 text makes adding the script to `_RESOLUTION_SCRIPTS` conditional on reading the list's purpose (P:108) but its AC states the script "passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests" (P:113): if the purpose check says no, the AC has nothing to run.
H9. Dependency order: Tasks 6, 7 depend only on Task 1 and Task 8 on Tasks 1, 4, 7, so the plan is acyclic and covers every spec file in section 6 (checked: merge_guard.py, models.py, run_log.py, fsm.py, `__init__.py`, the script, the ref, SKILL.md, state-machine.md, loop-guard.md, pr-submit.md, two user guides, five test files, test_worker_contract.py). No missing-file gap found.

## Reflection
No blocking defect found: the spec's engage, release and resume tables are covered by Tasks 3 and 4 row by row, the fold table by Task 3, the flag by Task 6, the script by Task 7, the protocol text by Tasks 8-10, the docs by Tasks 12-13. The weak spots are mechanical-gate quality (H1, H2, H3, H5, H6), not missing scope. Severity of every candidate is MINOR or low MAJOR and non-blocking.

## Findings block
(Tier 1 carries no findings-v2 block; the reviewers write one.)

confidence (self-reported): 0.70
