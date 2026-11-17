# Codegraph grounding: TASK-WF-stage3BRequest-20261117-172514

## Run state
- index_state: fresh (codegraph_status 2026-11-17: 3911 files, 0 added, 0 modified, 0 removed since index; latest file indexed 2026-11-17T17:15:09Z)
- access: mcp
- projectPath / worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- checked_at: 2026-11-17 (one check, Wave 1)
- graph tokens: none. The full CODEGRAPH.md section 2 pin and worktree-relation checks were not run; only codegraph_status was read.

## Resolved symbols
- `tests/skills/test_review_severity_rule.py`: `canonical_rule_bullets` (line 79), `S1_S3_FILES` (181), `S5_FILES` (193), `test_c_s1_s3_copied_verbatim` (197), `test_c_no_inventory_labels_or_annotation` (207), `test_a_no_any_severity_wording_in_tracked_primitives` (172). The "ten-file set" comment is at line 179.
- `src/superclaude/agents/reflect-reviewer.md` (not indexed as symbols; read by Grep): `## Output Format` at 69, "**Severity scale**" paragraph at 71, Deviations example rows at 86 and 87, `## Correctness gaps` at 101 and 108, `## Boundaries` at 117.

## Dependents
- `canonical_rule_bullets` callers (codegraph_callers, 8 rows; lines confirmed by Grep): `tests/skills/test_review_severity_mapping.py` (import line 20, use 119), `tests/skills/test_implement_severity_static.py` (import 12, use 487), and four tests inside `test_review_severity_rule.py` (104, 168, 199, 230). The helper is not changed by the plan.
- Tests parametrized over `S1_S3_FILES`: two (`test_c_s1_s3_copied_verbatim`, `test_c_no_inventory_labels_or_annotation`); nothing uses the tuple's length.
- Tests that read the agent file: `tests/cli/reflect/test_reviewer_readonly_tools.py` (tools line), `tests/agents/test_codegraph_rosters.py` (roster and the CODEGRAPH.md string); the plan's Task 1 names both.

## Pre-check
Every file the two tasks name exists; every symbol resolves; the dependents above are all named in Task 1 or left unchanged on purpose. Dependents of the touched symbols that no task names: none found.
