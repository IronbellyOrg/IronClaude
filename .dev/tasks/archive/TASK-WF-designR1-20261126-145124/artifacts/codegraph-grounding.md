# Codegraph grounding: TASK-WF-designR1-20261126-145124

## Run state

- index_state: fresh
- checked_at: 2026-11-26T13:27:57Z (carried from the first generation of this run: the regenerate route of workflow Wave 4R runs Waves 0 to 3 again inside the same run, and the protocol allows one readiness check per run; the repo code has not changed since, `git status` shows only untracked `.dev/` folders and one memory file)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-838
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-838
- access: mcp (lookup tools listed)
- tokens: none (SUPERCLAUDE_CODEGRAPH_PRIMITIVES is unset)
- Note: the graph covers Python and YAML only; the JSON and Markdown files below were read with Read, Grep and Glob.

## Resolved symbols

Graph rows located these in the first generation; each was then confirmed with Grep or Read (graph rows are leads). The rows marked "new" were added in this regeneration and read directly.

| Symbol or file | Where | Confirmed by |
|---|---|---|
| `main(argv, env, get, put, now)` and the `if __name__ == "__main__"` guard | `scripts/merged_pr_log.py` (def at line 622, guard at line 688) | Grep |
| `RefusedCommand`, `CommandRecord`, `Result`, `Runner`, `Runner.check_allowed`, `Runner.run` | `scripts/worktree_cleanup.py` (lines 130, 135, 142, 246, 284, 528) | Grep |
| new: `Runner.run` calls `check_allowed`, appends a `CommandRecord`, then `_execute(argv, cwd, stdin)` | `scripts/worktree_cleanup.py` lines 528 to 537 | Read |
| `EXIT_OK = 0`, `EXIT_USAGE = 64`, `EXIT_FAILED = 69` | `scripts/worktree_cleanup.py` lines 96 to 98 | Grep |
| new: session fixture `wc` loads the script once; `RecordingRunner(wc.Runner)` overrides only `_execute` | `tests/worktree_cleanup/conftest.py` lines 26 to 37 and 68 to 88 | Read |
| new: the comment that a fixture imported into several test modules crashes `pytest --fixtures` | `tests/worktree_cleanup/conftest.py` lines 44 to 46; CI lists fixtures at `.github/workflows/test.yml` line 114 | Read, Grep |
| Test loads a script with `importlib.util.spec_from_file_location` and registers it in `sys.modules` | `tests/merged_pr_log/test_merged_pr_log.py` lines 23 to 30; the folder also holds `__init__.py` | Grep, Glob |
| `tests/__init__.py`, `tests/worktree_cleanup/__init__.py`, `tests/merged_pr_log/__init__.py` exist | `tests/` | Glob |
| `test_guide_has_apply_and_check_commands` pins three guide strings plus the three JSON file names | `tests/docs/test_branch_protection_rulesets.py` lines 71 to 77 | Grep |
| `test_no_default_branch_token_anywhere` globs only `.github/rulesets/*.json` | `tests/docs/test_branch_protection_rulesets.py` line 66 | Grep |
| Three ruleset files; `protect-release-tags.json` holds `deletion`, `non_fast_forward` and `update` (lines 10 to 12) | `.github/rulesets/` | Read |
| Ruff rules `E,F,I,N,W,TID`, line length 88, target py310; pytest `testpaths = ["tests"]` | `pyproject.toml` | Read |
| `make lint` runs `lint-architecture` (commands and skills only) then `uv run ruff check .` | `Makefile` lines 48 to 50 and 362 onward | Read, Grep |
| Guide entries for `branch-protection.md` | `docs/developer-guide/documentation-index.md` lines 37 and 168 | Grep |

Not present yet (Glob found nothing): `scripts/org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`.

## Dependents

| Changed file | Dependents found | Effect on the plan |
|---|---|---|
| `docs/developer-guide/branch-protection.md` (one link line added) | Pinned by `test_guide_has_apply_and_check_commands`; linked from `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59, `docs/developer-guide/release-procedure.md` line 215 and `docs/developer-guide/documentation-index.md` lines 37 and 168 | The added line must not touch the pinned strings; the other four links stay as they are (Task 18) |
| `docs/developer-guide/documentation-index.md` (two link lines added) | No test under `tests/` names it (Grep over `tests/`) | Free to edit; keep the existing entries (Task 18) |
| `scripts/org_rulesets.py` (new) | None. No test enumerates `scripts/*.py`; `ruff check .` covers `scripts/` | Must pass ruff on the repo rules above (every task) |
| `tests/org_rulesets/` (new) | None | Folder needs `__init__.py` like `tests/merged_pr_log/` (Task 1); fixtures only in `conftest.py` (Constraints) |
| `.github/rulesets/*.json`, `tests/docs/test_branch_protection_rulesets.py` (read only) | Pinned by the same test | Must stay unchanged and passing (AC-4) |

## Pre-check

Run at the Wave 4 pre-check of this regenerated plan, read-only, with Glob, Grep and Read (no new readiness check; the graph holds no JSON or Markdown, so the floor was used).

- Existing files named by the plan: all exist (`.github/rulesets/protect-master.json`, `protect-integration.json`, `protect-release-tags.json`, `scripts/merged_pr_log.py`, `scripts/worktree_cleanup.py`, `tests/worktree_cleanup/conftest.py`, `tests/merged_pr_log/test_merged_pr_log.py`, `tests/docs/test_branch_protection_rulesets.py`, `docs/developer-guide/branch-protection.md`, `docs/developer-guide/documentation-index.md`, `pyproject.toml`, `.github/workflows/test.yml`, `.dev/issues/838/issue-summary.md`).
- New files named by the plan, absent as expected: `scripts/org_rulesets.py`, `tests/org_rulesets/` (13 files: `__init__.py`, `conftest.py`, and `test_render.py`, `test_verify.py`, `test_runner.py`, `test_store.py`, `test_gates.py`, `test_facts.py`, `test_checks.py`, `test_plan.py`, `test_apply.py`, `test_cli.py`, `test_page.py`), `docs/developer-guide/branch-protection-multi-repo.md`.
- Symbols named by the plan resolve: `main` in `scripts/merged_pr_log.py`; `Runner`, `check_allowed`, `run`, `_execute`, `RefusedCommand`, `CommandRecord`, `Result`, `EXIT_OK`, `EXIT_USAGE`, `EXIT_FAILED` in `scripts/worktree_cleanup.py`; the fixture `wc` and `RecordingRunner` in `tests/worktree_cleanup/conftest.py`; `test_guide_has_apply_and_check_commands` in `tests/docs/test_branch_protection_rulesets.py`.
- Documentation-index entries: Task 18 names a heading entry (line 37) and a list entry (line 168); both exist.
- Dependents of touched files that no task names: `CONTRIBUTING.md` line 70, `docs/developer-guide/README.md` line 59 and `docs/developer-guide/release-procedure.md` line 215 link to the guide. None needs an edit, because Task 18 adds one link line and leaves the guide's existing text alone.
- Result: 0 unresolved names, 1 unnamed dependent set (three links, no edit needed).
