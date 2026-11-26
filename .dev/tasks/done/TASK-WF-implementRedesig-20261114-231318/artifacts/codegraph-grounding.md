# Codegraph grounding: TASK-WF-implementRedesig-20261114-231318

## Run state

- index_state: fresh (`codegraph_status`: 3327 files, "Changes since index: 0 added, 0 modified, 0 removed"; one pending file of the sibling Sweep Sheet build, `20261114-sweep-sheet/sweep/assign.py`, was being indexed)
- checked_at: 2026-11-14T23:13Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
- access mode: MCP tools `mcp__codegraph__codegraph_*`
- graph tokens: none (no degraded state). Pending files of the sibling build are outside the symbols this plan names.

## Resolved symbols

The build writes only under `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger` and changes no existing symbol. It imports these existing symbols read-only (through a copied `scaffold/fnd.py`):

- `src/superclaude/cli/review/findings.py`: `parse_block(report_text: str) -> dict` at line 124; `_check_finding(obj: dict, seen: set[str]) -> str | None` at line 90 (private; pinned by the copied `test_fnd_contract.py`). The file is 457 lines.
- `src/superclaude/cli/review/merge_cmd.py` (118 lines): `command(ledger_path, doc, round_n, reports, resolution, out, cap)` at line 71, `_read(path)` at line 13.
- `src/superclaude/cli/review/ledger.py` (494 lines): the merge's finding ledger, not the `ledger-v1` block of the design.

Sibling files (read only; Tier A of DESIGN 3.1) that exist now: `20261114-sweep-sheet/scaffold/{__init__,briefs,cards,fnd,lint,normalise}.py`, `bin/{common,build-sandbox}.sh`, `briefs/` (nine parts), `cards/` (C1 to C8, schema, README), `config/{packages,panels,values}.json`, `tests/fakes/claude`. Tier B files `scaffold/{ledgerv1,telemetry,clock}.py`, `bin/{run-reviewer,judge-one,anon,judge-batch,run-panel,make-schedule,run-schedule}`, `analysis/{analyze,g0}.py` do not exist yet (listing of 2026-11-14T23:13Z), so they are built locally unless they appear and are stable at copy time.

## Dependents

- `_check_finding`: callers are `parse_block` (findings.py:124), the sibling's `scaffold/fnd.py` (import re-export), and the sibling's `tests/test_fnd_contract.py` (signature pin). The RL copy of `scaffold/fnd.py` and `test_fnd_contract.py` become two more dependents.
- `parse_block`: 52 callers (10 shown), among them `tests/review/test_review_findings.py` (`test_minor_blocking_is_an_error`, `test_unclosed_findings_block_is_invalid_even_when_empty`) and the sibling's `tests/test_fnd_contract.py::test_merge_accepts_class_probe_src_keys`. The repository suite `tests/review` is the guard: it must pass before and after (baseline of the sibling's step 0 note: 126 passed).
- `merge_cmd.command`: used by the sibling's `tests/test_fnd_contract.py` only (graph), and by `bin/run-panel.sh` of this build through `superclaude review merge`.
- No dependent of any `src/` symbol is edited by this plan.

## Pre-check

Read-only check of the plan against disk and the graph (2026-11-14, after the gate passed; no new readiness check):

- Files named by tasks that exist now: all of `SW/fixtures/{plans/p_basic,p_clean,source; specs/spec1,parent1; docs/doc1; repos/build_repo.py; reports/anchor_250,claim_301}`, `SW/config/packages.json`, `SW/tests/{conftest.py,helpers.py,fakes/claude}`, `EVAL/tools/run-reviewer.sh`, `EVAL/tools/tmp-scripts/judge-one.sh` (31 lines), `SW/DESIGN.md`, `src/superclaude/cli/review/{findings,merge_cmd}.py`, `tests/review/`, `pyproject.toml`.
- Symbols resolved: `scaffold/briefs.py` has `SEPARATOR` (line 28) and `render` (line 124); `findings.py` has `_blocks_after` (38), `_check_finding` (90), `parse_block` (124), `flat` (272), `locate` (276); `build-sandbox.sh` accepts `--raw`, `--packages FILE` and `<doc>`; the three study document ids each appear in `SW/config/packages.json`.
- The copied `SW/tests/conftest.py` already registers the markers `slow` and `freeze` (lines 21 to 25), which Task 4 of the plan handles with "only if not already defined".
- The eleven Tier T tests: none imports `sweep`. Three mention the word: `test_paths.py:11` asserts `/tmp/evalsb-sweep/...` is writable by `sw_assert_writable` (a direct call into `common.sh`, so K9's refusal in `rl-env.sh` does not touch it), `test_sandbox.py:39` writes a `"sweep-packages/1"` schema string into a fixture file, and `test_briefs.py` has 3 mentions (not inspected). If any of these fails in `RL`, Task 3 reports it; the copy is not edited.
- Dependents of touched symbols that no task names: none. The plan changes no `src/` symbol; the dependents of `parse_block` and `_check_finding` are recorded above and are guarded by `tests/review`, which Tasks 1 and 19 run.
- Tier B files of the sibling (`scaffold/{ledgerv1,telemetry,clock}.py`, `bin/{run-reviewer,judge-one,anon,judge-batch,run-panel,make-schedule,run-schedule}`, `analysis/{analyze,g0}.py`) are still absent: Tasks 7, 8, 12, 14, 15, 17 handle both the copied and the built-local case.
- Pre-check count: 19 files and 8 symbols confirmed, 0 missing, 0 unnamed dependents.

## Reflect pass (advisory)

See `./reflect-1/` in this folder when the reflect pass wrote output (section below the run).
