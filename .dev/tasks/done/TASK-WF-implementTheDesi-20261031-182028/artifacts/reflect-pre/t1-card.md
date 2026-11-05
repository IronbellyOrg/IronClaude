# Tier 1 reflection card (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/source.md` (one-line prompt; links the design `.dev/pr-submit-codex/design/pr-submit-codex-design.md`)
- Tasklist: `.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md`
- Hypothesis source: inline orchestrator card (UC-1 has no root-cause-analyst step)

## Coverage / acceptance section

- The plan maps design sections 4-16 onto 15 tasks in 5 phases: models/contract/run-log (Tasks 1-3), core adapter/merge/dedup (Tasks 4-9), tests (Tasks 10-11), skill/refs/command (Tasks 12-14), docs/changelog (Task 15).
- Every test file named in acceptance criteria exists on disk (checked with `test -e`: tests/pr_submit/test_detection_contract.py, test_cosmos_review.py, test_cosmos_protocol.py, test_silence.py, test_severity_router.py, test_crash_recovery.py, test_review_retrigger.py, test_static_grep.py, test_skill_parse.py, test_edge_cases.py, test_cosmos_poll.py, tests/skills/test_primitive_dual_surface_lookup.py, tests/unit/test_cli_install.py, tests/core/test_how_we_work_routing_table.py).
- The only existing 39-member assertion is `tests/pr_submit/test_run_log.py:165-168`; Task 1 updates it.
- Source requirement "plugins/superclaude mirrors" is handled only by a Constraint ("no pr-submit twin"), not a task; `find plugins -iname '*pr-submit*'` returned nothing, so no task is needed.

## Root-cause / deviation section

- No deviation from the design found in task scope: Task 6-9 interfaces match design section 14 names (`parse_codex_priority`, `codex_review_state`, `classify_codex`, `codex_finding_comments`, `merge_wait`, `dedup_groups`, `pending_retriggers`, `list_review_threads`).
- Refinement (not drift): Task 2 decides that a local override YAML without Codex fields disables Codex for that override; design section 4 says "a local override can change or blank them" but does not state the default for an override that omits the fields. `[INFERRED]`

## Structural / risk section

- Regression candidate R1: Task 4 changes `_thread_findings` (src/superclaude/pr_submit/classifier.py:259) used by `_selection` (classifier.py:380-383) for every Augment Cosmos classification; the default-argument path must keep Augment behaviour identical. Task 4's acceptance criteria name the Cosmos and silence test files as the guard.
- Regression candidate R2: Task 3 changes `rereview_request_count` folding (src/superclaude/pr_submit/run_log.py:189-191), which INV-R1 tests and crash recovery (src/superclaude/pr_submit/recovery.py:136-141) read; old logs without `cycle_id` must rebuild to the same count (Task 3 AC covers it).
- Risk R3: SKILL.md / refs are markdown with no executable test of the new two-reviewer loop; correctness of the orchestration text rests on test_skill_parse.py / test_static_grep.py plus review. The core functions it calls are unit-tested (Task 10).
- Risk R4: the Task 7 dry check needs network access to GitHub and the PR 336 threads; it is read-only.
- Risk R5: an operator's existing local override (Augment-only) would silently disable Codex (Task 2 choice).

## Recommendations

- Keep Task 4's default-argument contract and run the named Cosmos tests before Task 7 builds on it.
- In Task 2, state the override behaviour in refs/detection-contract.md (Task 13) so an operator knows to add the Codex fields to an override.
