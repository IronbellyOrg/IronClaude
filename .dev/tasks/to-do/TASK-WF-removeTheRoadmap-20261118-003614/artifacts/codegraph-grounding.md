# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-18T00:35:58Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-roadmap-family
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-roadmap-family
- access: mcp
- tokens: none

## Resolved symbols

- `sprint_group`, `roadmap_group`, `tasklist_group`: registered only in `src/superclaude/cli/main.py` (lines 525-535), confirmed by Grep.
- `SprintConfig`: callers (199 found, 40 shown) are all inside `src/superclaude/cli/sprint/`, `tests/sprint/`, `.dev/` records, plus three kept test files: `tests/integration/test_sprint_wiring.py`, `tests/integration/test_wiring_e2e_shadow.py`, `tests/pipeline/test_full_flow.py` (rows are leads; each file's import line was read through Grep).
- `execute_roadmap`: impact is limited to `cli/roadmap/executor.py`, `cli/roadmap/commands.py`, `tests/roadmap/*` and `tests/cli/test_tdd_extract_prompt.py`.
- `IsolationLayers` (`cli/sprint/executor.py:137`): impact is `tests/cli/eval/test_isolation_layers_probe.py` and one case in `tests/cli/eval/test_home_isolation_extend.py:535`.

## Dependents

Kept test files that import a removed package (from Grep, line read): `tests/pipeline/test_full_flow.py:39,345-360,472`, `tests/pipeline/test_trailing_gate.py:558-607`, `tests/pipeline/test_process.py:243`, `tests/cli/eval/test_home_isolation_extend.py:542`, `tests/unit/test_cli_install.py:35`, `tests/swarm/test_module_shape.py` (reads `cli/sprint/` on disk). No kept source module imports the three packages except `src/superclaude/cli/main.py`.

## Pre-check

Every repo path the plan names exists at plan time (checked with a path-exists loop over the backticked paths; the only miss is the literal rule text `src/superclaude/...`). Dependents of the touched symbols that no task names: none found; the kept test files that import removed code are all named in Task 5. `.roadmap-state.json` is also written by the plain `roadmap` skill, so Task 7 and Task 11 keep it.
