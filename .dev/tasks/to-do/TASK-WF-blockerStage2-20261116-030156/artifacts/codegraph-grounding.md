# Codegraph grounding for TASK-WF-blockerStage2-20261116-030156

## Run state

- index_state: fresh
- checked_at: 2026-11-16T03:03:44Z (`codegraph_status`: 3570 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript, not Markdown. The skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read from the base grounding of `TASK-WF-loosenBlockerRev-20261115-210254` (read 2026-11-15) plus a `test -e` check today; no symbol lookup beyond that was repeated for this package.

## Resolved symbols

- `src/superclaude/skills/task/SKILL.md`: section "Post-Completion Validation (Final Phase Only)" near line 288 (base grounding); the sweep call and the one offer go there. Re-read before editing.
- `src/superclaude/skills/tech-research/SKILL.md`: Gate 5 near line 415 and the A.7 checklist; it gets the ledger writing only, no sweep and no offer.
- `WORKER-CONTRACT.md` (installed core doc, `src/superclaude/core/`): the keys the worker contract gains; the review briefs that pin `rests-on` text are guarded by `tests/skills/test_review_brief_rests_on.py` (new).
- Stage 1 modules this stage imports (`follow_ups`, `safety_route`, `classifier_inputs`) do not exist today; Task 1 of this package checks they import.
- Existing paths named in the plan (`test -e` today): 7. Paths named that do not exist yet: 4: `src/superclaude/cli/review/sweep.py`, `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, `tests/review/test_review_sweep.py`, `tests/skills/test_review_brief_rests_on.py`.

## Dependents

- Tests that pin the task skill text: `tests/skills/test_task_builder_merge.py`, `test_worker_contract.py`, `test_review_loop_extension.py`, `test_review_prompt_overrides.py` (base grounding).
- The sweep records only (`promote` off): no gate outcome changes, so no existing review loop test should change.

## Pre-check

Checked 2026-11-16 with `test -e` over the 11 distinct `src/`, `tests/`, `plugins/` paths the plan names in backticks: 7 exist and 4 do not. Every absent path is a file or folder this package creates or one an earlier package creates (the stage 1 modules and tests, the skill folder `sc-review-severity`, the stage 2 `test_review_brief_rests_on.py`); the first task of each of stages 2, 3 and 4 checks the earlier package's evidence by package id before anything else runs. No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it after the generator wrote it and before the gate and the reflect call, to remove wording the gate rules reject: the literal task-folder prefix in the Constraints line for the spec, and leftover cross-package task numbers (a Phase or Task number of the old 46-task plan, replaced by the stage 3 package's name). No reflect finding drove these edits.
Not checked: the quoted line numbers in task bodies (they come from the 2026-11-15 grounding and each task re-reads before editing); that the old 46-task plan's task text is unchanged since extraction (it is the base text, extracted once on 2026-11-16).
