---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementGitHubI-20261105-184607
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# ccsession: CCSESSION_PERMISSIONS=default starts Claude without the permission bypass (issue 390, corrected plan)

Source: ./source.md
Goal: A caller can set `CCSESSION_PERMISSIONS=default` and `ccsession` adds no `--dangerously-skip-permissions` of its own (directly and through `ccsession-orca`, shim and tier models included), while every launch without that variable behaves exactly as it does today. Flags the caller passes itself, and a `CC_CLAUDE_FLAGS` set in the shell or in the env file, still apply.

## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Decisions accepted by the user: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only (that flag is not a permission bypass, and dropping it would remove the Grep and Glob tools on Linux and macOS; see the comment above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`); any value other than empty or `default` (including `Default` and `bypass`) stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass.
- The exit-2 check applies to every `ccsession` invocation, `--help`, `--list` and the hook and installer helper calls included, because it runs at the flag-default line (line 124 before this plan) ahead of the argument dispatch. The docs state this and a test pins it. The check stays at that spot: do not move the `case` below the env-file sourcing (a later launch-scoping change must keep computing the flags at that spot and defer only the `exit 2`), or an env-file value would start choosing the flags and an env-file `CC_CLAUDE_FLAGS=""` would take the default.
- The variable is read from the shell environment at that spot, before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file; the docs say so and a test pins it. The variable stays exported to nested launches (a nested `ccsession` or Claude Code started from inside the session inherits the non-bypass choice); the docs say so and a test pins it.
- `show_help` in `src/superclaude/skills/ccsession-tag/ccsession` (line 1652 before this plan) prints the header only up to the first line that starts with `# The wrapper always runs`. Do not change the first words of that line and do not edit `show_help`; new `--help` text goes above that line.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.

## Phase 1: Tests first, and test isolation

## Task 1: Add launcher tests for CCSESSION_PERMISSIONS to tests/unit/test_ccsession_tag.py

Source requirement: tests that fail on the old code (set: no bypass flag and shim/model routing kept; unset: unchanged), the exit-2 behavior, and the documented `--help` text. Work in `tests/unit/test_ccsession_tag.py`, next to `test_every_launch_restores_grep_and_glob`, which asserts the default flags on all six launch lines.

- Give `_label_launch` an optional keyword argument `extra_env: dict[str, str] | None = None` that is merged into the child environment after `HOME`, `CLAUDE_BIN` and `CCSESSION_ENV_FILE`; existing callers stay unchanged.
- Add a helper `_run_ccsession(tmp_path, *args, **extra)` that returns the `subprocess.CompletedProcess` without raising. It is modelled on the environment of `_label_launch` and must be safe on the unchanged launcher: it creates `tmp_path / "work"` and `tmp_path / "home"` with `mkdir(parents=True, exist_ok=True)`; `CLAUDE_BIN` is a fake script that only writes a marker file `tmp_path / "claude-ran"`; `HOME` is `tmp_path / "home"`; `CCSESSION_ENV_FILE` is a missing file in `tmp_path` unless `extra` sets it; `CC_CLAUDE_FLAGS` and `CCSESSION_PERMISSIONS` are removed from the inherited environment before `extra` is applied; and the call uses `stdin=subprocess.DEVNULL`, `timeout=60`, `check=False` and `cwd=tmp_path / "work"`.
- Add `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` to the variables deleted by the autouse environment-clearing block near the top of the file (the list that holds `CCSESSION_LAUNCH_ID` and `CLAUDE_TOPIC`), and `CCSESSION_PERMISSIONS` to the excluded-names tuple in `_orca_env` (the tuple that already holds `CC_CLAUDE_FLAGS`), so a value in the developer's shell never leaks into a test.
- Name every new test `test_permissions_default_<what it checks>` so `-k permissions` selects them, and add: a parametrized test over the same arguments-and-transcript matrix as `test_every_launch_restores_grep_and_glob` (all six launch lines: untagged, new and resumed, each with and without `--profile claude`) that runs with `CCSESSION_PERMISSIONS=default` and asserts the launched argument list starts with `--allowedTools=Grep`, contains no `--dangerously-skip-permissions`, contains `--model` exactly when `--profile` was given and `--resume` exactly when a transcript exists; `CCSESSION_PERMISSIONS=""` behaving like unset (starts with `--dangerously-skip-permissions`, `--allowedTools=Grep`); `CC_CLAUDE_FLAGS=--verbose` with the variable set to `default` launching with `--verbose` first and neither default flag; an empty `CC_CLAUDE_FLAGS` with the variable set to `default` launching with `--allowedTools=Grep` first and no bypass flag; an empty `CC_CLAUDE_FLAGS` with the variable unset taking the full old default; the variable set to `default` inside a `CCSESSION_ENV_FILE` (an `export` line) not enabling it, so the launched argument list still starts with `--dangerously-skip-permissions`; `CC_CLAUDE_FLAGS=--verbose` set inside a `CCSESSION_ENV_FILE` together with `CCSESSION_PERMISSIONS=default` in the shell launching with `--verbose` first (the env file still wins); and `ccsession demo --claude-args --dangerously-skip-permissions` with the variable set to `default` launching with `--allowedTools=Grep` first and the caller's `--dangerously-skip-permissions` still present in the argument list.
- Add exit-2 tests through `_run_ccsession`, parametrized over the values `bypass` and `Default`: `ccsession demo` returns 2, standard error names `CCSESSION_PERMISSIONS`, and the `claude-ran` marker does not exist; and one test that the value `bypass` with `--help` also returns 2 (the check is global).
- Add one help test through `_run_ccsession(tmp_path, "--help")` with no bad value: standard output contains `CCSESSION_PERMISSIONS=default` and contains neither `set -e` nor `CLAUDE_BIN=`, which proves the new text is in `--help` and that `show_help` still stops at the header.

Acceptance criteria:
- Run `uv run pytest tests/unit/test_ccsession_tag.py -k "permissions or grep_and_glob" -q` against the unchanged launcher and save the output to `./artifacts/t1-red.log`. These fail: the opt-in matrix, the empty-`CC_CLAUDE_FLAGS`-with-`default` test, the caller-passed-flag test (its first-argument check), the exit-2 test (both parametrized values, `bypass` and `Default`), the `--help` bad-value test and the help test. These pass: `test_every_launch_restores_grep_and_glob`, the empty-variable test, the `CC_CLAUDE_FLAGS=--verbose` override test, the env-file `CC_CLAUDE_FLAGS` test, the empty-`CC_CLAUDE_FLAGS`-with-variable-unset test and the env-file `CCSESSION_PERMISSIONS` test.
- During that red run no real `claude` process starts: every new test that launches `ccsession` uses a fake `CLAUDE_BIN`, and the exit-2 tests assert the marker file is absent.
- The new tests do not read or depend on the developer's own `CCSESSION_PERMISSIONS` or `CC_CLAUDE_FLAGS` values.

## Task 2: Add the ccsession-orca print-mode test to tests/unit/test_ccsession_tag.py

Depends on: Task 1

Source requirement: shim routing is kept when the variable is set, on the path the Coder wrapper actually uses (`ccsession-orca -p ...`, which hands off to `ccsession --shim --claude-args`), and the variable stays exported. Work in `tests/unit/test_ccsession_tag.py`, next to `test_orca_print_mode_is_untagged_and_never_asked`, using its `_orca_no_tty(tmp_path, *args, **extra)` helper, whose record holds `argv`, `base_url` and `env_names`.

- Add a test named `test_orca_print_mode_permissions_default_keeps_shim_routing` that runs `_orca_no_tty(tmp_path, "-p", "hello")` once without the variable (control) and once with `CCSESSION_PERMISSIONS="default"` (passed as an extra environment value). Both calls may share one `tmp_path`: each returns its own parsed `record.json` before the next call overwrites it.

Acceptance criteria:
- The control run records `argv == [*ORCA_FLAGS, "-p", "hello"]` and the opted-in run records `argv == ["--allowedTools=Grep", "-p", "hello"]`.
- Both records pass the existing `_assert_through_shim(record)` helper (`base_url == "http://127.0.0.1:4555"` and one credential set), proving shim routing is kept.
- The opted-in record's `env_names` contains `CCSESSION_PERMISSIONS` and the control record's does not, proving the variable stays exported to Claude.
- Saved output of `uv run pytest tests/unit/test_ccsession_tag.py -k orca_print_mode_permissions -q` against the unchanged launcher is in `./artifacts/t2-red.log` and shows this test failing on the argument list.

## Task 3: Add the tier-mode test and the tier fixture isolation to tests/unit/test_ccsession_tiers.py

Source requirement: tier models are kept when the variable is set, and the tier tests do not depend on the developer's shell. Work in `tests/unit/test_ccsession_tiers.py`, which has `_launch(tmp_path, *args, defaults=TIER_BLOCK, **extra)` (it runs `ccsession` with a fake `claude` that writes `seen.json` with `argv`, `settings` and `base_url`) and the autouse `_isolated` fixture.

- Add `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` to the names deleted in the autouse `_isolated` fixture (the list that holds `CCSESSION_SHOW_ALL_MODELS`).
- Add a test named `test_tier_launch_permissions_default_keeps_tier_routing` that calls `_launch(tmp_path, "work", "--tier", "tier0")` once as the control and once more with the extra argument `CCSESSION_PERMISSIONS="default"`. Neither call passes `--dangerously-skip-permissions` or any other flag explicitly (the tests that call `ccsession-orca` with that flag, for example the ones that pass it at the start of their argument list, are not the model for this test).

Acceptance criteria:
- The opted-in run's `seen["argv"]` contains no `--dangerously-skip-permissions` and begins with `--allowedTools=Grep`; the control run's begins with `--dangerously-skip-permissions`.
- The opted-in run has the same `settings` value, the same `--model` argument (when the control has one) and the same `base_url` as the control run.
- Saved output of `uv run pytest tests/unit/test_ccsession_tiers.py -k permissions -q` against the unchanged launcher is in `./artifacts/t3-red.log` and shows this test failing.

## Task 4: Isolate the install and update tests that run ccsession from the developer's shell

Source requirement: because the exit-2 check runs on every `ccsession` call, a bad `CCSESSION_PERMISSIONS` exported in a developer's shell would make other tests that run `ccsession` with the inherited environment fail. Work in two files.

- In `tests/unit/test_install_ccsession.py`, add an autouse fixture that deletes `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` with `monkeypatch.delenv(..., raising=False)`. It covers `test_wire_moves_names_saved_per_folder_into_the_repo_list` (the install step runs `ccsession --migrate-names` with the inherited environment) and `test_wire_symlink_runs_help` (runs `ccsession --help` with `**os.environ` and `check=True`).
- In `tests/cli/test_update_command.py`, add the same autouse fixture next to the existing autouse fixture of that file. It covers `test_real_install_launches_ccsession`, which runs the installed `ccsession --help` with `**os.environ` and `check=True`.

Acceptance criteria:
- With `CCSESSION_PERMISSIONS=typo` and `CC_CLAUDE_FLAGS=--verbose` exported, `uv run pytest tests/unit/test_install_ccsession.py tests/cli/test_update_command.py -q` passes on the unchanged launcher. This run is a smoke check only (the unchanged launcher ignores the variable, so it passes with or without the fixtures); the proof that the fixtures isolate the tests is the Task 5 isolation log on the changed launcher.
- Each of the two files has exactly one new autouse fixture and no other behavior change.

## Phase 2: Launcher change and its --help text

## Task 5: Add the CCSESSION_PERMISSIONS switch and its --help text to src/superclaude/skills/ccsession-tag/ccsession

Depends on: Task 1, Task 2, Task 3, Task 4

Source requirement: when `CCSESSION_PERMISSIONS=default` is set, no permission-bypass flag on any launch; unset is unchanged; empty `CC_CLAUDE_FLAGS` handling is unchanged; the variable is documented where ccsession documents its other variables (the header printed by `ccsession --help`). Make both edits in this one task so the tests of Task 1 pass together at its end.

Edit (a), the flag-default block. Replace the single assignment `CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:---dangerously-skip-permissions --allowedTools=Grep}"` (line 124) with a `case` on `"${CCSESSION_PERMISSIONS:-}"` that picks the default flag string, then keeps the existing `:-` expansion:

```
case "${CCSESSION_PERMISSIONS:-}" in
  "") _cc_default_flags="--dangerously-skip-permissions --allowedTools=Grep" ;;
  default) _cc_default_flags="--allowedTools=Grep" ;;
  *) echo "ccsession: CCSESSION_PERMISSIONS must be 'default' or unset (got '$CCSESSION_PERMISSIONS')" >&2; exit 2 ;;
esac
CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:-$_cc_default_flags}"
```

The six `exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ...` launch lines (around lines 1799 to 1868) already expand the variable and are not edited. The variable is not unset before any `exec`.

Edit (b), the header text. `ccsession --help` prints the header only up to the first line that starts with `# The wrapper always runs` (line 109; `show_help` at line 1652), so the new text goes above it. Do not edit `show_help`.
- Add a usage entry in the same format as its neighbours, directly before the `ccsession --refresh-models` entry (line 99) and after the line `In tier mode --profile is not used and the shim is always on.`, outside the Coder-workspaces tier block: `CCSESSION_PERMISSIONS=default ccsession <topic>`, with continuation lines saying it starts Claude without `--dangerously-skip-permissions` (only `--allowedTools=Grep` is added), that shim and tier routing are unchanged, that any other non-empty value exits 2 on every `ccsession` call including `--help`, that it is read from the shell environment and not from `~/.claude/ccsession.env`, that it stays exported to nested launches, and that flags the caller passes and a `CC_CLAUDE_FLAGS` set in the shell or in the env file still apply. The text must not contain the strings `--tier tier`, `--tier tier0` or `--tier tier1a`: existing help tests assert they are absent outside tier mode.
- Reword the sentence at lines 109 to 114 so it stays true, keeping its first words: `# The wrapper always runs claude with --allowedTools=Grep and, unless CCSESSION_PERMISSIONS=default is set, with --dangerously-skip-permissions.` Keep the existing explanation of why `--allowedTools=Grep` is kept and the note about the `=` form.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` reports no syntax error.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py tests/cli/test_update_command.py -q` passes completely, with the output saved to `./artifacts/t5-green.log`; every test that failed in the red logs of Tasks 1 to 3 now passes, the help test included.
- The same four files pass with `CCSESSION_PERMISSIONS=typo` and `CC_CLAUDE_FLAGS=--verbose` exported in the shell (output in `./artifacts/t5-isolation.log`), proving Tasks 1, 3 and 4 isolate the suite.
- `grep -n '^# The wrapper always runs' src/superclaude/skills/ccsession-tag/ccsession` finds exactly one line, and `git diff` shows no change to the `show_help` function and no change to any launch line; the `${CC_CLAUDE_FLAGS:-...}` expansion is kept as written (an empty value still takes the default); the only changed regions are the flag-default block and the header comment above `show_help`.

## Phase 3: User documentation

## Task 6: Add CCSESSION_PERMISSIONS to the settings table in src/superclaude/skills/ccsession-tag/README.md

Depends on: Task 5

Source requirement: document the variable beside the other variables. The settings table (header `| Setting | Effect |`, rows such as `CCSESSION_SHOW_ALL_MODELS=1` and `CCSESSION_COOLDOWN_SECONDS`, around lines 498 to 515) is where the README lists ccsession's variables.

- Add a row `CCSESSION_PERMISSIONS=default` with the effect: start Claude without `--dangerously-skip-permissions` (only `--allowedTools=Grep` stays, so Grep and Glob remain available); shim and tier-model routing are unchanged; read from the shell environment, not `~/.claude/ccsession.env`; stays exported to nested launches; any other non-empty value exits 2 on every `ccsession` call, `--help` included; a non-empty `CC_CLAUDE_FLAGS` (from the shell or the env file) still wins; flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply; under a bad value `ccsession-orca` also prints its "not a valid session name; ignoring it" warning before the exit. Add a second row `CC_CLAUDE_FLAGS` only if the table has none, stating it replaces the default flags and that an empty value takes the default.

Acceptance criteria:
- The README table contains a `CCSESSION_PERMISSIONS=default` row with all the points above and renders as a valid Markdown table (same column count on every row).
- `grep -n CCSESSION_PERMISSIONS src/superclaude/skills/ccsession-tag/README.md` shows the row.

## Task 7: Note the variable in src/superclaude/skills/ccsession-tag/ccsession.env.example

Depends on: Task 5

Source requirement: document the variable where ccsession's other variables are documented, and prevent the trap that the env file cannot set it. In the "Coder workspaces (tier mode) — optional settings" comment block (around line 25), add one comment line explaining that `CCSESSION_PERMISSIONS=default` must be set in the shell environment that starts `ccsession`, because the variable is read before this file is sourced. Known side effect, accepted: `seed-env.py` treats an env file as untouched when it equals the shipped example, so a file that is an unmodified copy of the previous example stops matching, as with any edit to this example; the tests read the current example and stay green.

Acceptance criteria:
- `src/superclaude/skills/ccsession-tag/ccsession.env.example` has one added comment line naming `CCSESSION_PERMISSIONS` and the shell-environment limit, and the file stays all comments (no active `export` line added).

## Task 8: Update the permission sentence in the two v5.0.0 testing guides

Depends on: Task 5

Source requirement: docs that state the permission default must stay true. Two guides say `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` "unless `CC_CLAUDE_FLAGS` is set (`ccsession:78-83,93`)": `docs/testing/v5.0.0/user/D08-ccsession.md` (line 23, which continues "Claude Code then runs tools without asking") and `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` (line 21, without that trailing clause).

- In each file, change only that one line: add that `CCSESSION_PERMISSIONS=default` is the other way out (then only `--allowedTools=Grep` is added), replace the stale citation `ccsession:78-83,93` with the line numbers of the permissions paragraph and of the flag-default block as they are after Task 5 (find them with `grep -n` in `src/superclaude/skills/ccsession-tag/ccsession`; do not copy numbers from this plan), and in D08 tie the trailing clause to the default launch ("by default Claude Code then runs tools without asking"). Do not add test steps and do not change the other `CC_CLAUDE_FLAGS` lines of D08 (lines 199 and 210); line 210 keeps its old `ccsession:78-83,93` citation on purpose, to keep the diff to the one sentence.

Acceptance criteria:
- Both sentences mention `CCSESSION_PERMISSIONS=default` and cite line numbers that `grep -n` on the changed `ccsession` shows hold the permissions paragraph and the flag-default block; the D08 sentence no longer claims Claude Code runs tools without asking in every case.
- `git diff --stat` for these two files shows one changed line each.

## Phase 4: Release note and sync

## Task 9: Add the CHANGELOG.md entry under Unreleased

Depends on: Task 5, Task 6, Task 7, Task 8

Source requirement: the repository records user-visible changes in `CHANGELOG.md` under `## [Unreleased]`, newest section first, as `### <area>: <summary> (#<issue>)` with `#### Added (...)` bullets.

- Add a section at the top of `## [Unreleased]`: `### ccsession: start Claude without the permission bypass (#390)` with an `#### Added (ccsession permissions)` bullet describing `CCSESSION_PERMISSIONS=default` (what it drops, what it keeps, unset is unchanged, any other value exits 2 on every `ccsession` call including `--help`, shell environment only and not settable from the env file, stays exported to nested launches, a non-empty `CC_CLAUDE_FLAGS` still wins, an empty one still takes the default, and flags the caller passes or a `CC_CLAUDE_FLAGS` set in the env file still apply) and one sentence saying callers such as the Coder `claude` wrapper opt in themselves; `superclaude reflect` is not changed.

Acceptance criteria:
- `CHANGELOG.md` has the new section directly under `## [Unreleased]` and above the existing onboarding-deck section, and every behavior in the bullet is covered by a test of Tasks 1 to 3.
- After all edits to `src/superclaude/skills/ccsession-tag/`, `make sync-dev` followed by `make verify-sync` exits 0, or reports no drift that this plan did not cause (run `make verify-sync` once before Task 5 to know the baseline); the gitignored `.claude/` copies are refreshed and never staged.
