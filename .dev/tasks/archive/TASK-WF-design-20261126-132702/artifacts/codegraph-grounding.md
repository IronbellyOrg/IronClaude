# Codegraph grounding: TASK-WF-design-20261126-132702

## Run state

- index_state: fresh
- checked_at: 2026-11-26T13:27:57Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-838
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-838
- access: mcp (lookup tools listed)
- tokens: none (SUPERCLAUDE_CODEGRAPH_PRIMITIVES is unset)
- Note: `codegraph_status` answered "0 added, 0 modified, 0 removed". The graph covers Python and YAML only; the JSON and Markdown files below were read with Read, Grep and Glob.

## Resolved symbols

Graph rows located these; each was then confirmed with Grep or Read (graph rows are leads).

| Symbol or file | Where | Confirmed by |
|---|---|---|
| `main(argv, env, get, put, now)` and the `if __name__ == "__main__"` guard | `scripts/merged_pr_log.py` (def at line 622, guard at line 688) | Grep |
| `RefusedCommand`, `CommandRecord`, `Result`, `Runner`, `Runner.check_allowed`, `Runner.run` | `scripts/worktree_cleanup.py` (lines 130, 135, 142, 246, 284, 528) | Grep |
| `EXIT_OK = 0`, `EXIT_USAGE = 64`, `EXIT_FAILED = 69` | `scripts/worktree_cleanup.py` lines 96 to 98 | Grep |
| Test loads a script with `importlib.util.spec_from_file_location` and registers it in `sys.modules` | `tests/merged_pr_log/test_merged_pr_log.py` lines 23 to 30; the folder also holds `__init__.py` | Grep, Glob |
| `test_guide_has_apply_and_check_commands` pins three guide strings plus the three JSON file names | `tests/docs/test_branch_protection_rulesets.py` lines 71 to 77 | Grep |
| `test_no_default_branch_token_anywhere` globs only `.github/rulesets/*.json` | `tests/docs/test_branch_protection_rulesets.py` line 66 | Grep |
| Three ruleset files | `.github/rulesets/protect-master.json`, `protect-integration.json`, `protect-release-tags.json` | Read (earlier in this run) |
| Ruff rules `E,F,I,N,W,TID`, line length 88, target py310; pytest `testpaths = ["tests"]` | `pyproject.toml` | Read |
| `make lint` runs `lint-architecture` (commands and skills only) then `uv run ruff check .` | `Makefile` lines 48 to 50 and 362 onward | Read, Grep |

Not present yet (Glob found nothing): `scripts/org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`.

## Dependents

| Changed file | Dependents found | Effect on the plan |
|---|---|---|
| `docs/developer-guide/branch-protection.md` (one link line added) | Pinned by `test_guide_has_apply_and_check_commands`; linked from `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59, `docs/developer-guide/release-procedure.md` line 215 and `docs/developer-guide/documentation-index.md` lines 37 and 168 | The added line must not touch the pinned strings; the other four links stay as they are |
| `docs/developer-guide/documentation-index.md` (two link lines added) | No test under `tests/` names it (Grep over `tests/`) | Free to edit; keep the existing entries |
| `scripts/org_rulesets.py` (new) | None. No test enumerates `scripts/*.py`; `ruff check .` covers `scripts/` | Must pass ruff on the repo rules above |
| `tests/org_rulesets/` (new) | None | Folder needs `__init__.py` like `tests/merged_pr_log/` |
| `.github/rulesets/*.json`, `tests/docs/test_branch_protection_rulesets.py` (read only) | Pinned by the same test | Must stay unchanged and passing (AC-4) |

## Pre-check

Run at the Wave 4 pre-check, read-only, with Glob, Grep and `test -e` (no new readiness check; the graph holds no JSON or Markdown, so the floor was used).

- Existing files named by the plan: all exist (`.github/rulesets/protect-master.json`, `protect-integration.json`, `protect-release-tags.json`, `scripts/merged_pr_log.py`, `scripts/worktree_cleanup.py`, `tests/merged_pr_log/test_merged_pr_log.py`, `tests/docs/test_branch_protection_rulesets.py`, `docs/developer-guide/branch-protection.md`, `docs/developer-guide/documentation-index.md`, `pyproject.toml`, `.dev/issues/838/issue-summary.md`).
- New files named by the plan, absent as expected: `scripts/org_rulesets.py`, `tests/org_rulesets/` (13 files), `docs/developer-guide/branch-protection-multi-repo.md`.
- Symbols named by the plan resolve: `main` in `scripts/merged_pr_log.py`; `Runner`, `check_allowed`, `RefusedCommand`, `CommandRecord`, `Result`, `EXIT_OK`, `EXIT_USAGE`, `EXIT_FAILED` in `scripts/worktree_cleanup.py`; `test_guide_has_apply_and_check_commands` in `tests/docs/test_branch_protection_rulesets.py`.
- Documentation-index entries: Task 17 names a heading entry and a list entry for `branch-protection.md`; they are at lines 37 and 168 of `docs/developer-guide/documentation-index.md`.
- Dependents of touched files that no task names: `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59 and `docs/developer-guide/release-procedure.md` line 215 link to the guide. None needs an edit, because Task 17 changes only one added link line and leaves the guide's existing text alone. `docs/developer-guide/README.md` has its own list of links; the design asks for links only in the guide and the documentation index, so it is left out on purpose.
- Result: 0 unresolved names, 1 unnamed dependent set (three links, no edit needed).
