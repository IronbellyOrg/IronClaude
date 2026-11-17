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

## Revision 2

Re-checked 2026-11-16 (index not used: every file touched is Markdown or a new module; resolved with `test -e`, Grep and Read).

- `test -e` over 32 paths the revised plan names in backticks: existing 25 (`src/superclaude/cli/review/__init__.py` and `ledger.py`; the `/sc:implement` protocol `SKILL.md`, `refs/managed-workspace.md` and `refs/qa.md` in `src/` and in `plugins/superclaude/skills/sc-implement-protocol/`; `src/superclaude/skills/tech-research/SKILL.md`; `src/superclaude/core/WORKER-CONTRACT.md`; `src/superclaude/output-styles/pragmatic.md`; the 14 existing test files named in the plan). Absent 7, all created by this package or an earlier one: `src/superclaude/cli/review/follow_ups.py`, `safety_route.py`, `classifier_inputs.py`, `classify_cmd.py` and `src/superclaude/skills/sc-review-severity/refs/registry.yaml` (stage 1), and `sweep.py` and `follow_ups_cmd.py` (this package).
- `grep -rn "follow_up\|follow-up" src/superclaude/cli` (source files only): no hit in `cli/review`; the command group does not exist today.
- `src/superclaude/cli/review/__init__.py` lists nine subcommand modules: panel, merge, ledger, telemetry, lint, estimate, cluster, verify, manifest.
- `sha256sum` of `refs/qa.md`: `93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004` in `src/` and in the plugin twin (equal).
- Anchors read today (re-read before editing): `refs/managed-workspace.md` step 5 begins "5. Re-run step 3." (line 56) and step 6 begins "6. `pass` → run the helper in archive mode" (line 62); `SKILL.md` has "### Whole-list review" (line 184) and "## Done" (line 190); `refs/qa.md` line 225 says the summary "is informational and never asks the user anything" and line 288 closes the interrupt list. tech-research prompt templates at lines 859, 906, 950, 1001, 1048; consolidation items at lines 487, 516, 549; cap sentences at lines 490 and 555.
- Existing static pins that constrain new text: `tests/skills/test_implement_severity_static.py` `_SITE` scan (halt, Ruling, `E-HALT-QA`, `E-ARCHIVE-BLOCKED` on any line of the five protocol files, with an allow-list that pins archive gate steps 2, 3 and 6); `test_h_implement_protocol_plugin_twins_byte_equal` and the managed-workspace mirror assertion in `test_reflect_input_snapshot.py`; `test_protocol_prose_has_no_cross_file_line_pointers` in `test_task_workspace_lifecycle.py`; the content fixtures `review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (tech-research rows).
- `pytest --collect-only -q -k tech_research` over `test_review_prompt_overrides.py` and `test_review_severity_rule.py`: 0 selected of 95.
- `/tmp/gate_check.py` from the task folder: stage 2 prints `8 tasks 4 phases PASS`.

Findings applied or not applied: see the Revision 2 section of the stage 2 request (`stage-requests/stage2-request.md` in the program folder), copied to `source.md`. Summary: R1-1, R3-1, R1-2, R3-3, R1-3, R2-1, R1-4, R3-2, R1-5, R1-6, R2-2, R1-7, R2-3, R3-4, R2-4, R3-6, R3-5, R3-7 applied; R1-8 partly applied; R3-8 not applied (no offer exists in this stage).

## Revision 3

Re-checked 2026-11-16 for fix cycle 2 (index not used: the files touched are Markdown or new modules; resolved with `test -e`, Grep, Read and `sha256sum`).

- `test -e` over 16 paths: existing 10 (`src/superclaude/cli/review/__init__.py` and `ledger.py`; `sc-implement-protocol/SKILL.md`, `refs/managed-workspace.md`, `refs/qa.md`; `tech-research/SKILL.md`; `core/WORKER-CONTRACT.md`; `tests/skills/test_worker_contract.py`, `test_review_prompt_overrides.py`, `test_review_severity_rule.py`). Absent 6, all stage 1 outputs checked by Task 1 before any edit: `cli/review/follow_ups.py`, `safety_route.py`, `classifier_inputs.py`, `classify_cmd.py`, `skills/sc-review-severity/refs/scale-map.md`, `refs/registry.yaml`.
- `sha256sum` of `refs/qa.md` in `src/` and in the plugin twin: `93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004` (equal, unchanged).
- `grep -rin "follow-up\|follow_up" src/superclaude/skills/sc-implement-protocol`: one hit, `refs/ledger.md` line 60 (the verdict note). Nothing in the protocol writes a `follow-ups.md`.
- `grep -n "LEGACY PROMPT" src/superclaude/skills/tech-research/SKILL.md`: two hits, the "Report Validation QA Agent Prompt" and the "Qualitative QA Agent Prompt" templates ("Do NOT use ... for Phase 6 QA"). Active templates: "Research Analyst Agent Prompt" (heading near line 819), "Research QA" (859), "Synthesis QA" (906), "Lens-Specific QA Agent Prompt Template" (1048). Step 3.1 (478) and Step 5.N+1 (506) each run `rf-analyst` and `rf-qa-qualitative` agents; Steps 6.7 (557) and 6.7b (564) have their own consolidation. `grep -in unattended` over the file finds nothing.
- `WORKER-CONTRACT.md`: WC-4 has the bullet "Mapping from a command's own status" (the pinned `success` to `succeeded` text) and no GR12 mapping. Spec section 6.4 requires one.
- Spec section 6.2 (run-scoped row ids), 6.4 (safety row makes the run `partial`), 7.1 and 7.2 (code supplies M, C, E inputs): re-read. Stage 1 plan Task 10 (`questions_to_ask`) and Task 12 (`classify` reads a judge answers file): re-read.
- `uv run python /tmp/gate_check.py` from the task folder: stage 2 prints `8 tasks 4 phases PASS`.

Findings applied or not applied: see the Revision 3 section of the stage 2 request (`stage-requests/stage2-request.md` in the program folder), copied to `source.md`. Summary: MB-1, MB-2, MB-3, MB-4, MN-1 to MN-9, MN-11 (as a precaution), MN-12, MN-13, MN-14 and MN-15 (INV-006, INV-010 applied; INV-007 partly) applied; MN-10 not applied (both of its requirements are met together; the review found no defect).
