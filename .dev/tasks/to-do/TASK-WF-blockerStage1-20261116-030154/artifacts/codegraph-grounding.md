# Codegraph grounding for TASK-WF-blockerStage1-20261116-030154

## Run state

- index_state: fresh
- checked_at: 2026-11-16T03:03:44Z (`codegraph_status`: 3570 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript, not Markdown. The skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read from the base grounding of `TASK-WF-loosenBlockerRev-20261115-210254` (read 2026-11-15) plus a `test -e` check today; no symbol lookup beyond that was repeated for this package.

## Resolved symbols

- `src/superclaude/cli/review/__init__.py` lines 14-36: `review_group` registers subcommand modules from a tuple of names (nine `*_cmd` entries); each module exports `command`. `classify_cmd` joins by adding its name to that tuple (base grounding, read 2026-11-15; existence re-confirmed today).
- `src/superclaude/cli/review/ledger.py` (typed ledger `review-ledger/1`), `card_convert.py` and `telemetry.py` (split table rows on bare pipes, so the follow-up cell codec uses entities): the follow-up ledger is a separate Markdown file; the stage's reuse-auditor task runs before a reader or writer is built.
- `src/superclaude/cli/doctor.py`: `run_doctor` and the `_check_*` helpers; `_check_review_severity_digests` is added here.
- `src/superclaude/hooks/hooks.json` line 173: `pragmatic-subagent.js` entry. No root `hooks/hooks.json`.
- Plugin twins and installed-only spec-panel variants are not touched by this stage (stage 4 package).
- Existing paths named in the plan (`test -e` today): 14. Paths named that do not exist yet: 19: `src/superclaude/cli/review/classifier.py`, `src/superclaude/cli/review/classifier_inputs.py`, `src/superclaude/cli/review/classify_cmd.py`, `src/superclaude/cli/review/data/classifier_thresholds.json`, `src/superclaude/cli/review/follow_ups.py`, `src/superclaude/cli/review/safety_route.py`, `src/superclaude/skills/sc-review-severity/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`, `src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md`, `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, `src/superclaude/skills/sc-review-severity/refs/rule.md`, `src/superclaude/skills/sc-review-severity/refs/scale-map.md`, `tests/review/test_review_classifier.py`, `tests/review/test_review_classifier_inputs.py`, `tests/review/test_review_classify_cmd.py`, `tests/review/test_review_follow_ups.py`, `tests/review/test_review_follow_ups_filing.py`, `tests/review/test_review_safety_route.py`, `tests/skills/test_review_severity_registry.py`.

## Dependents

- `run_doctor`: `doctor` in `src/superclaude/cli/main.py`; `tests/unit/test_cli_doctor.py`; `tests/cli/test_install_retired_mcp.py`; `tests/cli/test_update_command.py` (base grounding; Grep by def line).
- `src/superclaude/cli/review/__init__.py`: imported by `src/superclaude/cli/main.py` and `tests/review/` modules; adding one name touches `review_group` only; `tests/review/test_review_cli.py` is named in the plan.
- No carrier file (agents, templates, rule prompts, task skill, tech-research, `WORKER-CONTRACT.md`) is edited by this stage, so the tests that pin rule text (`tests/skills/test_review_severity_rule.py` and the others in the base grounding) stay green by construction; the exit-summary task checks the carrier diff is empty.

## Pre-check

Checked 2026-11-16 with `test -e` over the 33 distinct `src/`, `tests/`, `plugins/` paths the plan names in backticks: 14 exist and 19 do not. Every absent path is a file or folder this package creates or one an earlier package creates (the stage 1 modules and tests, the skill folder `sc-review-severity`, the stage 2 `test_review_brief_rests_on.py`); the first task of each of stages 2, 3 and 4 checks the earlier package's evidence by package id before anything else runs. No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it after the generator wrote it and before the gate and the reflect call, to remove wording the gate rules reject: the literal task-folder prefix in the Constraints line for the spec, and leftover cross-package task numbers (a Phase or Task number of the old 46-task plan, replaced by the stage 3 package's name). No reflect finding drove these edits.
Not checked: the quoted line numbers in task bodies (they come from the 2026-11-15 grounding and each task re-reads before editing); that the old 46-task plan's task text is unchanged since extraction (it is the base text, extracted once on 2026-11-16).
