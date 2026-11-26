# Codegraph grounding: TASK-WF-scopeCut-20261126-165750

## Run state

- index_state: fresh
- checked_at: 2026-11-26T13:27:57Z (carried from the first readiness check of this run; the repo code has not changed since, `git status` shows only `.dev/` files and one memory file)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-838
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-838
- access: mcp (lookup tools listed)
- tokens: none
- Note: the graph covers Python and YAML only; JSON and Markdown files were read with Read, Grep and Glob.

## Resolved symbols

| Symbol or file | Where | Confirmed by |
|---|---|---|
| `main(argv, env, get, put, now)` and the `if __name__ == "__main__"` guard | `scripts/merged_pr_log.py` (def line 622, guard line 688) | Grep |
| `Runner`, `check_allowed`, `run` (check, record, `_execute`), `RefusedCommand`, `CommandRecord`, `Result` | `scripts/worktree_cleanup.py` (Runner at 246, `run` at 528 to 537, `_execute` at 570) | Grep, Read |
| `EXIT_OK = 0`, `EXIT_USAGE = 64`, `EXIT_FAILED = 69` | `scripts/worktree_cleanup.py` lines 96 to 98 | Grep |
| session fixture `wc`; `RecordingRunner(wc.Runner)` overriding `_execute` | `tests/worktree_cleanup/conftest.py` lines 26 to 37 and 68 to 109 | Read |
| `pytest --fixtures` listing in CI | `.github/workflows/test.yml` line 114 | Grep |
| `test_guide_has_apply_and_check_commands` pins guide strings | `tests/docs/test_branch_protection_rulesets.py` lines 71 to 77 | Grep |
| three ruleset files; tag file holds `deletion`, `non_fast_forward`, `update` (lines 10 to 12) | `.github/rulesets/` | Read |
| ruff rules `E,F,I,N,W,TID`, line length 88, py310 | `pyproject.toml` | Read |
| index entries for `branch-protection.md` | `docs/developer-guide/documentation-index.md` lines 37 and 168 | Grep |

Not present yet: `scripts/apply_org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`.

## Dependents

| Changed file | Dependents | Effect on the plan |
|---|---|---|
| `docs/developer-guide/branch-protection.md` (one link line) | pinned by `test_guide_has_apply_and_check_commands`; linked from `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59, `release-procedure.md` line 215 | the added line must not touch the pinned strings (Task 7) |
| `docs/developer-guide/documentation-index.md` (two links) | no test names it | keep existing entries (Task 7) |
| `scripts/apply_org_rulesets.py`, `tests/org_rulesets/` (new) | none; `ruff check .` covers them | pass ruff check and format (every task) |

## Pre-check

Run read-only with Glob, Grep and Read (no new readiness check). All existing files named by the plan exist; the new files are absent as expected; all symbols named resolve; 0 unresolved names, 1 unnamed dependent set (three links, no edit needed).
