# Reviewer 2 brief (persona: qa; UC-1 pre-execution review of a workflow plan)

You are a read-only reviewer. Audit ONLY the plan and the hunks below; do not run commands, do not edit anything. Return one card as YAML text (the orchestrator saves it).

Inputs (repo root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline):
- Spec (driving request): .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/source.md
- Plan under review: .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/TASK-WF-refactorScIssueC-20261118-041634.md

Lens: test and acceptance quality. For every task, would its acceptance criteria actually fail if the change were wrong or missing? Will the existing tests (tests/commands/test_issue_command.py, tests/skills/test_issue_protocol.py, tests/issue_watch/*, tests/commands/test_routing_plugin_parity.py, tests/core/test_how_we_work_routing_table.py) still pass after the planned edits, and are there tests that would break that no task updates? Search the tests for anything that pins the text the tasks change.

## T1 card slice
Candidate findings: C-1 (bare --submit now runs at full), C-2 (ship-gate sentence kept while full becomes default), C-3 (claim.md final output text wrong for full), C-4 (test_launch.py not edited).

## Codegraph run state
index_state: fresh, checked_at: 2026-11-18T04:16:47Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline. Use Grep and Read unless your tool list shows a codegraph tool.

## Grounding hunks
- tests/commands/test_issue_command.py:104-116 `test_option_defaults` (asserts `rows["--pipeline"][2] == "`worktree`"` and that `--pipeline full` appears in the `--submit` row cell); lines 137-149 `test_st2_pipeline_and_submit_stop_rules_come_after_the_old_ones` (pins the order create-only, claim-only, bad value, submit and the quoted message "--submit needs --pipeline full", and `"with no value" in rules[values:submit]`); line 188 `test_no_source_tree_path` forbids `src/superclaude/` in the command file.
- tests/skills/test_issue_protocol.py:431-459 pin Wave 5 and Wave 8 sentences of refs/claim.md; 653-667 `test_brainstorm_steps_have_no_handoff_and_use_default_models` expects 3 brainstorm steps.
- tests/issue_watch/test_launch.py:929-939 pin the watcher's `--pipeline none` prompt.
- The plan's Task 3 changes the `E-SUBMIT-NEEDS-FULL` rule text; Task 5 adds tests; Task 6 adds a protocol test.

## Card format
```yaml
reviewer: 2
persona: qa
verdict: pass | pass-with-findings | fail
confidence: <0-1>
coverage_assessment: <text>
findings:
  - id: F1
    severity: blocking | medium | note
    claim: <one sentence>
    evidence: <file:line, quoted>
    class: weak-acceptance | breaks-existing-test | missing-test | other
    tag: grounded | INFERRED
```
Tag every claim grounded or [INFERRED]. A zero-finding review must say what you checked.
