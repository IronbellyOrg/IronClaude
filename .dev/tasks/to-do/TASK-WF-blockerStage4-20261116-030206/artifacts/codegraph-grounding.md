# Codegraph grounding for TASK-WF-blockerStage4-20261116-030206

## Run state

- index_state: fresh
- checked_at: 2026-11-16T03:03:44Z (`codegraph_status`: 3570 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript, not Markdown. The skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read from the base grounding of `TASK-WF-loosenBlockerRev-20261115-210254` (read 2026-11-15) plus a `test -e` check today; no symbol lookup beyond that was repeated for this package.

## Resolved symbols

- Four digest templates under `src/superclaude/templates/` (`documents/agent_template_qa.md` merge rule near 85, `skill_template.md` near 828, two MDTM templates near 644 and 655) and `agent_template_analysis.md` (merge-rule text only); four rule prompts near lines 11, 27, 28, 27; the builder and researcher skills (`tech-reference`, `readme`, `tdd/refs/build-request-template.md`, `operational-guide`); `commands/spec-panel.md` and its plugin twin. Line numbers are from the base grounding and Task 1 of the base plan; every task re-reads before editing.
- `plugins/superclaude/skills/` holds 4 entries today (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`); the mirror folder is new.
- Existing paths named in the plan (`test -e` today): 16. Paths named that do not exist yet: 6: `plugins/superclaude/skills/sc-review-severity/`, `plugins/superclaude/skills/sc-review-severity/refs/rule.md`, `src/superclaude/skills/sc-review-severity/`, `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, `tests/skills/test_review_severity_plugin_parity.py`, `tests/skills/test_review_severity_registry.py`.

## Dependents

- Plugin twins (hand-kept, differ from source): `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`.
- Installed-only spec-panel variants in `~/.claude/commands/sc/` (`spec-panel-armb.md`, `-diffgate.md`, `-ledger.md`, `-ponytail.md`, `-stoprule.md`) are outside the scan and stay `installed-only`.
- `make verify-sync` covers `src/` to `.claude/`; the plugin mirror is checked by the new parity test.

## Pre-check

Checked 2026-11-16 with `test -e` over the 22 distinct `src/`, `tests/`, `plugins/` paths the plan names in backticks: 16 exist and 6 do not. Every absent path is a file or folder this package creates or one an earlier package creates (the stage 1 modules and tests, the skill folder `sc-review-severity`, the stage 2 `test_review_brief_rests_on.py`); the first task of each of stages 2, 3 and 4 checks the earlier package's evidence by package id before anything else runs. No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it after the generator wrote it and before the gate and the reflect call, to remove wording the gate rules reject: the literal task-folder prefix in the Constraints line for the spec, and leftover cross-package task numbers (a Phase or Task number of the old 46-task plan, replaced by the stage 3 package's name). No reflect finding drove these edits.
Not checked: the quoted line numbers in task bodies (they come from the 2026-11-15 grounding and each task re-reads before editing); that the old 46-task plan's task text is unchanged since extraction (it is the base text, extracted once on 2026-11-16).
