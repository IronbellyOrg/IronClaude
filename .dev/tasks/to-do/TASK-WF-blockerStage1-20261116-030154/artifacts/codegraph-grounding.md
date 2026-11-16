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

## Revision 2

Re-checked 2026-11-16 (no code symbol changed; the index does not cover Markdown, so existence and phrase checks used `test -e`, `grep` and `git ls-files`, run from the repository root in one read-only batch):

- `test -e` over 11 paths named by the revision: all exist (`src/superclaude/cli/roadmap/remediate_parser.py`, `src/superclaude/cli/pipeline/fmea_classifier.py`, `src/superclaude/skills/task/SKILL.md`, `src/superclaude/skills/task-builder`, `src/superclaude/agents/rf-task-builder.md`, `src/superclaude/cli/review/ledger.py`, `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, and the installed `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`).
- `test -e` over 5 paths that must be absent: all absent (`src/superclaude/cli/review/lint_cmd.py`, `src/superclaude/cli/review/estimate_cmd.py`, `src/superclaude/skills/sc-spec-panel-stoprule-protocol`, `src/superclaude/agents/finding-grader.md`, `plugins/superclaude/skills/sc-review-severity`).
- `git ls-files src plugins | grep -i -E "stoprule|finding-grader"` prints nothing: the stoprule rubric and `finding-grader` have no tracked copy under `src/` or `plugins/` (the tracked copies sit under `.dev/experiments/`), which is why their scale-map row is `installed-only`.
- `grep -rl -i "highest severity\|more severe rating\|higher severity" src --include=*.md --include=*.py` lists 13 files: `agents/rf-analyst.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `cli/pipeline/fmea_classifier.py`, `cli/roadmap/remediate_parser.py`, `skills/operational-guide/SKILL.md`, `skills/readme/SKILL.md`, `skills/sc-auggie-review-protocol/SKILL.md`, `skills/task/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/tech-reference/SKILL.md`, `templates/documents/agent_template_analysis.md` and `templates/documents/agent_template_qa.md` (paths relative to `src/superclaude/`). The allow-list of Task 3 now covers the auggie file, the six stage 4 files and the two code files; `skills/task/SKILL.md` is the one retired carrier among them.
- `src/superclaude/cli/review/__init__.py` lists nine module names in the subcommand tuple; seven modules exist (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`).
- `git diff --stat HEAD` over the carrier paths of Task 16 (plus `plugins` and `ledger.py`) prints no line today.
- `plugins/superclaude/skills/` holds four skills (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`), so no existing plugin test requires a mirror of a new skill folder.
- `uv run python /tmp/gate_check.py` from the repository task folder: the stage 1 package prints PASS (16 tasks, 4 phases).

Findings: F1 applied (Task 7 end point and allowed importers); F2 applied, option (a) (Task 3 and Task 15 T4 `installed-only` exemption); F3 applied (allow-list lists `remediate_parser.py` and `fmea_classifier.py`; `stage3-request.md` line 14 edited to match); F4 applied (decision sentence in Task 7, audit verdict in Task 16); F5 applied (columns, path root, `none` labels, Task 3 dependencies in Tasks 9, 12 and 15); F6 and F7 applied (Task 10 depends on Task 7; `run_questions` in Task 9 and `questions_to_ask` in Task 10; the safety-route half of T12 moved to Task 13); F8 applied (full grep path; seven review subcommands named); F9 applied (`sweep-flagged` defined as a ninth state, no rollout stage named). Decisions 1, 2, 4 and 5 applied as listed in the Revision 2 section of the stage request. Not applied: none.

## Revision 3

Re-checked 2026-11-16 (fix cycle 2; the index does not cover Markdown, so checks used `test -e`, `grep`, `sed` and Read from the repository root):

- `test -e` over `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`, `src/superclaude/contracts/__init__.py`, `src/superclaude/cli/review/verify_cmd.py`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`: all exist. `origin_repo.py` defines `read_origin()` (line 156) which raises `ClaimError`; it is a script in a folder with no `__init__`, so load by file path is right.
- `grep -n "click.command\|@click.group" src/superclaude/cli/review/*_cmd.py`: the verify command is named `verify-citations`; the seven present names are `panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations`, `manifest`.
- `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review` prints nothing today; the old form `grep -rln "ledger" src/superclaude/cli/review` lists 11 `.pyc` files under `__pycache__` beside 4 `.py` files, which confirms M-F1.
- `grep -c -i "High or Medium\|High and Medium\|Medium (blocking)\|High/Medium" src/superclaude/skills/sc-tasklist-protocol/SKILL.md` prints 9 (lines 1439, 1450, 1531, 1537, 1567, 1571, 1608, 1610, 1614); the spec lists 7.
- `src/superclaude/contracts/__init__.py` defines `THRESHOLDS` and `CONVERGENCE_THRESHOLDS`; `make lint` check 11 runs `superclaude.tools.arch_lint --check-contracts` over `src/superclaude/cli/`.
- `uv run python /tmp/gate_check.py` from the repository task folder: the stage 1 package prints PASS (16 tasks, 4 phases).

Findings: M-F1 applied; M-F2 applied (grammar rules in Task 3, lookup in Task 9, T4 in Task 15); M-F3 applied (`earlier_decisions` in Task 7; the offer step is a stage 2 task); M-F4 applied by supplying the inputs (Task 10), not by deferring them; M-F5 applied; M-F6 applied; M-F7 applied; M-F8 applied; M-F9 applied (the tasklist count is 9, not the reviewer's "9 or 7": the live grep wins); M-F10 applied. Not applied: none. Not checked: the quoted spec line numbers (the plan names spec sections, not lines).

## Revision 4

Re-checked 2026-11-16 (cuts-debate trim; two tasks remain; the index does not cover Markdown, so checks used `test -e`, `grep`, `sha256sum` and Read from the repository root):

- `test -e` over the 11 test files the print task runs: all exist (`tests/skills/test_implement_severity_static.py`, `test_review_severity_rule.py`, `test_task_workspace_lifecycle.py`, `test_task_workspace_smoke.py`, `test_workflow_archive.py`, `test_implement_saved_prompt_rule.py`, `test_reflect_input_snapshot.py`, `test_codegraph_adoption.py`, `tests/commands/test_impact_command.py`, `tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`). `tests/review/test_review_cli.py` also exists. None dropped.
- `test -e` over the files the print task edits and copies: `src/superclaude/skills/sc-implement-protocol/SKILL.md`, `refs/managed-workspace.md`, `refs/qa.md` and the same three under `plugins/superclaude/skills/sc-implement-protocol/`: all exist. SHA-256 of both `refs/qa.md` copies today: `93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004` (equal).
- `test -e` over the four new paths (`src/superclaude/cli/review/safety_route.py`, `safety_cmd.py`, `tests/review/test_review_safety_route.py`, `test_review_safety_cmd.py`): all absent, as they must be before Task 1.
- `src/superclaude/cli/review/__init__.py` lists nine module names in its tuple (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `lint_cmd`, `estimate_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`); the seven existing commands are `panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations`, `manifest` (`grep -n "click.command\|click.group" src/superclaude/cli/review/*_cmd.py`). `safety-scan` does not clash. `tests/review/test_review_cli.py` checks only that the help lists `panel`, `merge`, `ledger` and `telemetry`.
- `refs/managed-workspace.md`: the `FINAL: <pass|issues> evidence=<ev-list> state=<sha256>` block is the one that ends step 5, and the line "6. `pass` → run the helper in archive mode" follows it. `refs/qa.md` notes file: line 1 holds the `start` sha, lines 2 to m are live, lines after m begin with `superseded `; a clean task writes no notes file.
- Carrier diff: nothing under `src/` or `plugins/` was edited by this trim (plan, request, source and grounding only).

Findings: cuts rows C1, C2, C3, C4, C7 and C10 applied to the plan (Tasks 1 to 12, 14, 15 and 16 cut; Task 13 rebuilt as Task 1; stage 2 Task 3 absorbed as Task 2). Not applied: none. Not checked: that the gate checker passes (it requires `depth: standard` and 4 to 8 phases).
