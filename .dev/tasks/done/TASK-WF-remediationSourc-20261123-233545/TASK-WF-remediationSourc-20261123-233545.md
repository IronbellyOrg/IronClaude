---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261123-233545
version: "1"
priority: Medium
created_date: "2026-11-23"
---

# Retry a failed first run in the issue watcher sweep (issue 751)

Source: ./source.md
Goal: A later sweep completes first-run setup on its own for a generated config left `enabled: false` by a failed first run (for example `worktree_invalid` before the Coordinator worktree existed), while owner-disabled configs stay disabled, dry runs write nothing, and existing state is preserved.

## Constraints

- Reuse the existing `first_run` function as the only setup path; do not add GitHub writes, label creation or store creation to `dispatch.py` or `cycle.py` (the boundary pinned by `tests/issue_watch/test_security_invariants.py` stays intact).
- Do not change the config schema (`_TOP_KEYS` in `src/superclaude/cli/issue_watch/cycle.py`) and do not change `ensure_config` in `src/superclaude/cli/issue_watch/generate.py`.
- A config with no first-run report, or whose report starts with `first-run: passed`, is never retried.
- A dry-run sweep makes no `first_run` call and writes no file.
- Do not edit anything under `.claude/`; change `src/` and `tests/` only.

## Phase 1: Read the first-run report

## Task 1: Add a read-only failed-step helper to first_run.py

In `src/superclaude/cli/issue_watch/first_run.py`, add a public function `failed_step(config_path: Path) -> tuple[str, datetime] | None` next to `_report_dir` (line 78) and `_write_report` (line 86). It reads the raw config with `_raw_config`, takes the report directory with `_report_dir` and the report file name with the same rule `first_run` uses at lines 141-145 (`first-run.txt` when the directory is the config's absolute `state_dir`, else `<config stem>-first-run.txt` beside the config). It reads only the first line of that file, opened with `os.O_NOFOLLOW` and a read bounded to 4096 bytes, and decodes it as UTF-8. When the line starts with `first-run: failed ` it returns the step name (the word after `failed `, up to the next colon) and the file's modification time as a timezone-aware UTC datetime. In every other case, including a missing file, a symlink, a decode error and any `OSError`, it returns `None`. It never writes. Share the report-name rule with `first_run` through one small private function so the two cannot drift. Source requirements 4 and 5.

Acceptance criteria:
- `failed_step` returns `("config", <datetime>)` for a report whose first line is `first-run: failed config: worktree_invalid`, and `None` for `first-run: passed`, a missing file, a symlinked file and a non-UTF-8 first line.
- With a relative or missing `state_dir` in the config, `failed_step` finds `<stem>-first-run.txt` beside the config.
- `first_run()` writes the same report names as before (existing `tests/issue_watch/test_first_run.py` still pass unchanged).

## Phase 2: Retry in the sweep

## Task 2: Retry first_run for a failed, disabled config in run_sweep

Depends on: Task 1

In `src/superclaude/cli/issue_watch/dispatch.py`, add a module constant `RETRY_AFTER_S = 3600.0`, import `failed_step` from `.first_run` (next to the existing `first_run` import at line 45) and add `timedelta` to the `from datetime import ...` line (line 40). In `run_sweep`, immediately before `enabled = _enabled(config_path)` (line 428, after the generate branch that ends at line 427), add: when `not dry_run`, `_enabled(config_path) is False`, and `failed_step(config_path)` returns `(step, written_at)`, call `first_run(config_path, defaults, runner, deps_factory)` once when `step == "config"`, or when `since - written_at >= timedelta(seconds=RETRY_AFTER_S)` for any other step (`since` is the sweep start already computed at the top of `run_sweep`). Then fall through to the existing `_enabled` read, so a successful retry continues to the precheck and the child, and a failed retry is reported as `not_enabled`. A repo whose config was just generated in this same sweep is not retried a second time. Source requirements 1, 2, 3 and 5.

Acceptance criteria:
- A config that is `enabled: false` with a report `first-run: failed config: worktree_invalid` and a now-valid worktree is enabled by the next non-dry sweep and its child starts in that sweep.
- A failed retry leaves the config disabled, is skipped as `not_enabled`, and calls `first_run` exactly once in that sweep.
- A failure at a step other than `config` is retried only when the report is at least 3600 seconds older than the sweep start.
- A disabled config with no report or a `first-run: passed` report, and any config in a dry-run sweep, produces no `first_run` call and no file write.
- `grep -n "ensure_trigger_label\|init_state\|gh " src/superclaude/cli/issue_watch/dispatch.py` shows no new GitHub or store call in `dispatch.py`.

## Phase 3: Text

## Task 3: Update the dispatcher docstring and the not_enabled reason

Depends on: Task 2

In `src/superclaude/cli/issue_watch/dispatch.py`, update the module docstring step 2 (lines 7-8) to say that a repository whose first-run report says the last attempt failed is retried on a later sweep (immediately for a `config` failure, after one hour for other steps), and change the `not_enabled` entry of `SKIP_REASONS` (line 66) to say the config is `enabled: false` because the first run did not pass and has not yet been retried successfully, or because the owner set it. Source requirement 6.

Acceptance criteria:
- The docstring and the `SKIP_REASONS["not_enabled"]` text describe the retry rule and the one-hour delay.
- `tests/issue_watch/test_dispatch.py` and `tests/issue_watch/test_cli.py` still pass; no test pins the old wording (checked with `grep -rn "did not pass, or the owner" tests src`).

## Phase 4: Tests

## Task 4: Test failed_step in test_first_run.py

Depends on: Task 1

In `tests/issue_watch/test_first_run.py`, add tests for `failed_step` using the existing harness helpers (the class around lines 100-140 that builds a config and a state directory under `tmp_path`): a failed `config` report in `state_dir`, a `passed` report, no report, a symlinked report, a non-UTF-8 first line, and a relative `state_dir` with the report beside the config as `<stem>-first-run.txt` (follow the existing pin at lines 347-356).

Acceptance criteria:
- Each case above has its own test and the new tests fail if `failed_step` is removed.
- `uv run pytest tests/issue_watch/test_first_run.py -q` passes.

## Task 5: Test the retry in test_dispatch.py

Depends on: Task 2

In `tests/issue_watch/test_dispatch.py`, add a `World.report(name, first_line)` helper next to `World.config` (line 48) that writes `first-run.txt` in `World.state_dir(name)` with mode 600, and tests that monkeypatch `dispatch.first_run` as the existing tests at lines 364-369 and 390-397 do (the `sweep()` helper at line 141 uses a `deps_factory` that fails, so the real `first_run` must not run). Set report ages with `os.utime`. Cover: failed `config` report then valid worktree then the next sweep enables the config and starts the child (`world.started()`); a repeated failure stays `not_enabled` with exactly one fake `first_run` call; no report means no call (the existing test at line 421 stays as it is); a `passed` report on a disabled config means no call; a dry-run sweep means no call and no file change; a failure at `label` younger than 3600 seconds means no call and older than 3600 seconds means one call; an existing `dispatch.json` and `lock` in the state directory are unchanged after a retry that fails.

Acceptance criteria:
- Every case above has its own test, and the retry tests fail against the code before Task 2.
- `uv run pytest tests/issue_watch -q` passes with no change to `tests/issue_watch/test_security_invariants.py`.
