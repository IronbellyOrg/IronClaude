# Codegraph grounding: TASK-WF-refactorTheScIss-20261118-054817

## Run state

- index_state: fresh (codegraph_status: 0 added, 0 modified, 0 removed since the last index at 2026-11-18T05:32:25Z)
- access: mcp
- checked_at: 2026-11-18T05:48:29Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
- projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline
- graph tokens: none. Every target of this plan is Markdown or a test file whose pins are text assertions, so the Read and Grep floor did the symbol work; no call sites of product code change.

## Resolved symbols

Read from the live files in this run:

- `src/superclaude/skills/sc-issue-protocol/refs/claim.md`: `## Wave 5: next steps` (lines 75-83; step 1 recommend, step 2 next-steps.md, step 3 plan boundary, step 4 launch prompt with `<L>` at line 82, step 5 do not run steps); `## Wave 7` (97); `## Wave 8: launch` (116; line 120 launch command, line 122 "`<L>` is the same level as in Wave 5."); `## Final output` (137; the `launched` text at line 144); the effort and complexity rubric (65-73).
- `src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md`: lines 7-9 carry `Type: <feature | bug>`, `Complexity: <simple | medium | complex>`, `Effort estimate: <hours> hours`.
- `src/superclaude/skills/sc-issue-protocol/SKILL.md`: line 17 (claim summary, `full (default)`), line 89 (Wave 5 summary line), line 91 (Wave 7), line 124 (`pipeline_level` field), line 138 (`pipeline_level` paragraph), line 156 (error table).
- `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md` line 7 ("default level `full`").
- `src/superclaude/commands/issue.md`: line 16 (claim summary), line 43 (`--pipeline` row), line 44 (`--submit` row), line 48 (paragraph under the table), line 59 (E-SUBMIT-NEEDS-FULL rule), lines 64-69 (examples).
- Tests that pin the text: `tests/commands/test_issue_command.py::test_option_defaults` (line 113, the default cell), `test_default_level_is_for_a_person_and_the_watcher_stays_explicit` (line 182), `test_submit_rule_stops_a_bare_submit_and_keeps_its_message` (188); `tests/skills/test_issue_protocol.py::test_st7_plan_boundary_line_and_the_k_rule` (431; needs "`--pipeline full` ignores the line" and the K wording in Wave 5), `test_st9_prompt_is_written_before_wave_7_and_wave_8_skips_none` (445; needs the `prompt` command text with `--out "<D>/launch-prompt.md"` and "not `none`" and "written before Wave 7" in Wave 5), `test_default_level_is_full_and_only_worktree_waits_for_a_person` (681; asserts "or `full` when the flag was omitted" in Wave 5), the ten-field return-contract test (line 545 onward, `pipeline_level` at 562).
- `refs/chains.md:27` names "claim Wave 5 step 1" (the recommend call): inserting a new step after step 2 leaves step 1 where it is.

## Dependents

- `src/superclaude/cli/issue_watch/launch.py` (lines 33 and 92) passes `--pipeline none`; `tests/issue_watch/` pins it. Unchanged by this plan.
- `scripts/orca_worktree.py prompt --level` and `launch --level` take the level as a required argument; they never see the omitted-flag case. Unchanged.
- Docs that state the default: `docs/user-guide/commands.md` (lines 368, 371, 377-378, 388), `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (lines 1557, 1635), `docs/designs/sc-issue-claim-pipeline-flag.md` (lines 21, 43, 66, 78, 87, 274), `docs/designs/sc-issue-command.md` (lines 44, 64-66), `src/superclaude/core/HOW-WE-WORK.md` line 328 and its plugin copy.

## Pre-check

Floor (Grep, Read, `test -f`), read-only, no new readiness check. 9 tasks checked: all 16 named files exist; the lines the tasks name hold the text they say (issue.md:16 and :43, SKILL.md:17, :89 and :138, claim.md:75-83, :116-122 and :144, the user-guide rows at 368 and 378, architecture reference 1557, design-record notes at flag.md 21/43/66/78/87/274 and command.md 44/66, HOW-WE-WORK.md:328). Dependents no task names: none found. `refs/chains.md:27` ("claim Wave 5 step 1") is named in Task 1 and does not move. `tests/skills/test_model_alias_policy.py` is only run, not edited.
