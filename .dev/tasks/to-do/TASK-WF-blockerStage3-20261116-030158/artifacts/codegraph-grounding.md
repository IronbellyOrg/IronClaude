# Codegraph grounding for TASK-WF-blockerStage3-20261116-030158

## Run state

- index_state: fresh
- checked_at: 2026-11-16T03:03:44Z (`codegraph_status`: 3570 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript, not Markdown. The skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read from the base grounding of `TASK-WF-loosenBlockerRev-20261115-210254` (read 2026-11-15) plus a `test -e` check today; no symbol lookup beyond that was repeated for this package.

## Resolved symbols

- `src/superclaude/output-styles/pragmatic.md` lines 221-231 (reviewer brief and definition bullets), `src/superclaude/agents/rf-qa.md` (merge rule line 83; cap sentence lines 402 and 549), `rf-qa-qualitative.md` (merge rule line 84; eight FAIL-by-label bullets at 240, 291, 362, 429, 500, 567, 746, 784), `rf-analyst.md`, `src/superclaude/skills/task/SKILL.md` (merge text lines 252 and 361; cap sentence 258, 372, 409). Line numbers from the base grounding of 2026-11-15; every task re-reads before editing.
- New in this stage: `src/superclaude/cli/review/fixcheck.py`, `tests/review/test_review_fixcheck.py`, `tests/skills/test_review_merge_rule_scan.py`; `src/superclaude/skills/sc-review-severity/refs/rule.md` comes from the stage 1 package.
- Existing paths named in the plan (`test -e` today): 32. Paths named that do not exist yet: 5: `src/superclaude/cli/review/fixcheck.py`, `src/superclaude/skills/sc-review-severity/refs/rule.md`, `tests/review/test_review_fixcheck.py`, `tests/skills/test_review_brief_rests_on.py`, `tests/skills/test_review_merge_rule_scan.py`.

## Dependents

- Tests that pin the rule text and must be re-pinned: `tests/skills/test_review_severity_rule.py` (including `test_ej_fixtures_are_byte_copies_of_the_plan_tables`), `test_review_severity_mapping.py`, `test_implement_severity_static.py`, `test_review_loop_extension.py`, `test_review_prompt_overrides.py`, `test_spec_panel_review_loop.py`, `test_task_builder_merge.py`, `test_worker_contract.py`; `tests/audit/test_nfr_conv_9_zero_trust.py`, `test_invariant_preservation_NFR_6_through_10.py`, `test_severity_floor_unweakened.py`, `test_dnsp_all_agents_fail_bypass.py`; `tests/review/test_review_rules_text.py`; fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (base grounding).
- The hook `pragmatic-subagent.js` (`src/superclaude/hooks/hooks.json:173`) injects the installed output style into every subagent; the seeded-recall passes carry that confound, stated in the plan.

## Pre-check

Checked 2026-11-16 with `test -e` over the 37 distinct `src/`, `tests/`, `plugins/` paths the plan names in backticks: 32 exist and 5 do not. Every absent path is a file or folder this package creates or one an earlier package creates (the stage 1 modules and tests, the skill folder `sc-review-severity`, the stage 2 `test_review_brief_rests_on.py`); the first task of each of stages 2, 3 and 4 checks the earlier package's evidence by package id before anything else runs. No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it after the generator wrote it and before the gate and the reflect call, to remove wording the gate rules reject: the literal task-folder prefix in the Constraints line for the spec, and leftover cross-package task numbers (a Phase or Task number of the old 46-task plan, replaced by the stage 3 package's name). No reflect finding drove these edits.
Not checked: the quoted line numbers in task bodies (they come from the 2026-11-15 grounding and each task re-reads before editing); that the old 46-task plan's task text is unchanged since extraction (it is the base text, extracted once on 2026-11-16).
