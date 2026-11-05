# Reviewer 2 brief (persona: qa)

Read-only audit (UC-1, pre-execution). Audit the implementation PLAN against its spec (source.md -> the linked design). Do not edit, write, or run anything; Read/Grep/Glob only, from repo root /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex. Return a reviewer card as YAML: reviewer, persona, findings (list of {id, claim, citation file:line, class: aligned|refinement|drift|gap, severity: high|medium|low, recommendation naming a task}), self_confidence 0-1. Tag any claim without a file:line with [INFERRED].

## T1 card excerpt

## Coverage / acceptance section

- The plan maps design sections 4-16 onto 15 tasks in 5 phases: models/contract/run-log (Tasks 1-3), core adapter/merge/dedup (Tasks 4-9), tests (Tasks 10-11), skill/refs/command (Tasks 12-14), docs/changelog (Task 15).
- Every test file named in acceptance criteria exists on disk (checked with `test -e`: tests/pr_submit/test_detection_contract.py, test_cosmos_review.py, test_cosmos_protocol.py, test_silence.py, test_severity_router.py, test_crash_recovery.py, test_review_retrigger.py, test_static_grep.py, test_skill_parse.py, test_edge_cases.py, test_cosmos_poll.py, tests/skills/test_primitive_dual_surface_lookup.py, tests/unit/test_cli_install.py, tests/core/test_how_we_work_routing_table.py).
- The only existing 39-member assertion is `tests/pr_submit/test_run_log.py:165-168`; Task 1 updates it.
- Source requirement "plugins/superclaude mirrors" is handled only by a Constraint ("no pr-submit twin"), not a task; `find plugins -iname '*pr-submit*'` returned nothing, so no task is needed.


## Grounding hunks

### .dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md:1-187
The plan under audit (Read the whole file).

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 8: ## 1. Problem and goal
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 28: ## 2. Evidence: what Codex actually posts (observed on PRs 334, 335, 336)
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 43: ## 3. Current system (read before designing)
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 73: ## 4. Design overview: one reviewer-agnostic path, one small adapter per reviewer
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 111: ## 5. Reviewer detection and fail-open
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 137: ## 6. Polling both reviewers in one round, and the terminal conditions
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 170: ## 7. Parsing Codex findings and mapping P0-P3 onto severity routing
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 213: ## 8. Re-grade, verification and troubleshoot dispatch (reused)
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 220: ## 9. Dedup when both reviewers flag the same line
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 237: ## 10. Reply and resolve
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 247: ## 11. Re-trigger after a push
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 268: ## 12. Loop guard, round counter and the re-trigger count
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 282: ## 13. Run-log events and state machine naming the reviewer
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 298: ## 14. Interfaces (new and changed)
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 351: ## 15. Files changed
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 381: ## 16. Tests
### .dev/pr-submit-codex/design/pr-submit-codex-design.md section starting line 409: ## 17. Out of scope, risks and UNVERIFIED items
(Read each design section; the spec body is 425 lines, so it is given per section.)

### .dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/reflect-pre/artifacts/coverage-matrix.yaml
The deterministic coverage matrix and its semantic_gaps list.

## Coverage slice

| Requirement area | Tasks | Status |
|---|---|---|
| all 141 inferred rows (see coverage-matrix.yaml) | 1-15 | 76 matched, 65 unmatched by containment |
| design s16 tests | 10,11,15 | mapped |
