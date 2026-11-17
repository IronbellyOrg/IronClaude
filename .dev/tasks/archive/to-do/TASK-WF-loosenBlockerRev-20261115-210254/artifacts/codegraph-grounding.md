# Codegraph grounding for TASK-WF-loosenBlockerRev-20261115-210254

## Run state

- index_state: fresh
- checked_at: 2026-11-15T21:04:00Z (readiness check at the start of Wave 1; re-confirmed at the Wave 4 pre-check by `codegraph_status`: 3552 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp (lookup tools listed)
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript only, not Markdown, so the skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read (the permanent floor), not codegraph.

## Resolved symbols

- `src/superclaude/cli/review/__init__.py` lines 14-36: `review_group` registers subcommand modules from a tuple of names (nine `*_cmd` entries: `panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `lint_cmd`, `estimate_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`); each module exports `command`. `classify_cmd` joins by adding its name to that tuple.
- `src/superclaude/cli/review/ledger.py`: existing typed ledger, schema `review-ledger/1`. The follow-up ledger is a separate Markdown file; Task 17 runs the reuse-auditor before building a reader or writer.
- `src/superclaude/cli/review/card_convert.py` and `telemetry.py`: split table rows on bare pipes, so the follow-up cell codec uses entities and no backslash before a pipe.
- `src/superclaude/cli/doctor.py`: `run_doctor` and the `_check_*` helpers; `_check_review_severity_digests` is added here (Task 24).
- `src/superclaude/hooks/hooks.json` line 173: `pragmatic-subagent.js` hook entry. There is no root `hooks/hooks.json`.
- Anchors re-read from disk on 2026-11-15 before the plan cited them:
  - `src/superclaude/skills/task/SKILL.md`: merge text at lines 252 and 361 ("Preserve the highest severity rating when duplicates disagree", 2 hits); cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" at lines 258, 372 and 409 (3 hits); section "Post-Completion Validation (Final Phase Only)" near line 288.
  - `src/superclaude/skills/tech-research/SKILL.md`: cap sentence at lines 490 and 555 (2 hits, both checklist items under section A.7); Gate 5 near line 415.
  - `src/superclaude/agents/rf-qa.md`: merge rule line 83; cap sentence at line 402 (Fix Cycle bullet) and line 549 (numbered rule 10) (2 hits).
  - `src/superclaude/agents/rf-qa-qualitative.md`: merge rule line 84; eight "FAIL - Any CRITICAL or IMPORTANT issue exists" bullets at lines 240, 291, 362, 429, 500, 567, 746, 784.
  - `src/superclaude/templates/documents/agent_template_qa.md`: merge rule line 85, one FAIL-by-label bullet.
  - `src/superclaude/skills/task-builder/SKILL.md` line 875: one cap sentence. `src/superclaude/agents/rf-task-builder.md`: zero cap sentences (Task 44 corrected for this).
  - Merge-rule phrases, case-insensitive, in Markdown under the Task 40 scope: 11 files, 14 lines (rf-analyst 1, rf-qa-qualitative 1, rf-qa 1, task skill 2, tech-reference 2, readme 2, tdd build-request-template 1, operational-guide 1, agent_template_qa 1, agent_template_analysis 1, sc-auggie-review-protocol 1). Each is covered by a task or by the allow-list.
  - Definition carriers of "Grade every review finding as blocking or minor": 11 files, matching the registry's 11 `digest` rows.
- Not existing yet (confirmed by `test -e`): the folder `src/superclaude/skills/sc-review-severity/`, `classifier.py`, `classifier_inputs.py`, `classify_cmd.py`, `follow_ups.py`, `safety_route.py`, `sweep.py`, `fixcheck.py`, `data/classifier_thresholds.json`, and the 12 new test modules.

## Dependents

- `run_doctor`: `doctor` in `src/superclaude/cli/main.py`; `tests/unit/test_cli_doctor.py`; `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`); `tests/cli/test_update_command.py`. Resolution: def-line plus Grep.
- `src/superclaude/cli/review/__init__.py`: imported by many files including `src/superclaude/cli/main.py` and the `tests/review/` modules; adding one name to the tuple touches `review_group` only. `tests/review/test_review_cli.py` is named in Task 22.
- Tests that pin the rule text (existence confirmed): `tests/skills/test_review_severity_rule.py` (including `test_ej_fixtures_are_byte_copies_of_the_plan_tables`), `test_review_severity_mapping.py`, `test_implement_severity_static.py`, `test_review_loop_extension.py`, `test_review_prompt_overrides.py`, `test_spec_panel_review_loop.py`, `test_task_builder_merge.py`, `test_worker_contract.py`; `tests/audit/test_nfr_conv_9_zero_trust.py`, `test_invariant_preservation_NFR_6_through_10.py`, `test_severity_floor_unweakened.py`, `test_dnsp_all_agents_fail_bypass.py`; `tests/review/test_review_rules_text.py`; fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml`; the two plan tables `.dev/review-severity-rule/cap-edits.yaml` and `sweep-edits.yaml`.
- Plugin twins (hand-kept, differ from source): `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; `plugins/superclaude/skills/` holds 4 entries today (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`).
- Installed-only spec-panel variants live in `~/.claude/commands/sc/` (`spec-panel-armb.md`, `-diffgate.md`, `-ledger.md`, `-ponytail.md`, `-stoprule.md`); `src/superclaude/commands/` holds only `spec-panel.md`.

## Pre-check

Checked 2026-11-15 with `test -e` over the 83 distinct `src/`, `tests/`, `plugins/` and `.dev/review-severity-rule/` paths the plan names in backticks: 55 exist and 28 are files or folders the plan creates (the skill folder, its `SKILL.md` and 5 refs, 7 modules and the thresholds file under `src/superclaude/cli/review/`, 12 test modules, the plugin mirror folder). No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it, to correct three factual errors of its own before the reflect call (reflect had not run, so no reflect finding drove them):
- Task 44 said the cap sentence is in `rf-task-builder.md`; it has none. Now limited to `task-builder/SKILL.md` (one hit) with `rf-task-builder.md` named as not edited.
- Task 34 named one cap site in `rf-qa.md`; there are two (line 402 and rule 10 near line 549). Now both.
- Task 28 named wrong step numbers for the tech-research cap sites; they are two checklist items under section A.7 (lines 490 and 555).
Dependents of touched symbols that no task names: `src/superclaude/cli/main.py` (registers `review_group` and `doctor`; neither registration changes). No other gap found.
Not checked: that the line numbers the plan quotes for the five templates and rule prompts other than `agent_template_qa.md` (`skill_template.md` near 828, the two MDTM templates near 644 and 655, the four rule prompts near lines 11, 27, 28, 27) still match; Task 1 freezes them from a live grep before those tasks run, and Phase 5 tasks re-read before editing.
