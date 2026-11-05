---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementGitHubI-20261105-170815
version: "1"
priority: Medium
created_date: "2026-11-05"
---

# ccsession: CCSESSION_PERMISSIONS=default starts Claude without the permission bypass (issue 390)

Source: ./source.md
Goal: A caller can set `CCSESSION_PERMISSIONS=default` and `ccsession` (directly and through `ccsession-orca`, shim and tier models included) starts Claude without `--dangerously-skip-permissions`, while every launch without that variable behaves exactly as it does today.

## Constraints

- Design is fixed by the user: option B, a new explicit opt-in variable. Do not implement the issue's other option (dropping the flags automatically on scripted launches) and do not touch `src/superclaude/cli/reflect/runner.py` or `src/superclaude/cli/pipeline/process.py`; callers such as the Coder `claude` wrapper opt in themselves.
- Do not change how an empty `CC_CLAUDE_FLAGS` is handled: the `:-` default expansion stays, so an empty or unset value still takes the default flags. A non-empty `CC_CLAUDE_FLAGS` still replaces the default completely, including when `CCSESSION_PERMISSIONS=default` is set.
- Plan decision for the user to confirm at approval: with `CCSESSION_PERMISSIONS=default` the default flags become `--allowedTools=Grep` only. That flag is not a permission bypass; dropping it would remove the Grep and Glob tools on Linux and macOS (see the comment block above `CC_CLAUDE_FLAGS` in `src/superclaude/skills/ccsession-tag/ccsession`).
- Plan decision for the user to confirm at approval: any `CCSESSION_PERMISSIONS` value other than empty or `default` stops `ccsession` with exit status 2 and a message on standard error, so a typo can never fall back to the bypass silently.
- The variable is read from the shell environment at the same point as `CC_CLAUDE_FLAGS`, before `~/.claude/ccsession.env` is sourced, so it is not settable from that file; the docs say so.
- Edit only `src/superclaude/` sources, tests, docs and `CHANGELOG.md`. The `.claude/` copies are gitignored sync output and are never staged.
- Delivery note, not a code task: the pull request that ships this plan must say in its description that it unblocks Coder PR 458 and link issue 390; `/sc:pr-submit` writes that description after the plan is approved and executed.

## Phase 1: Tests that fail on the old launcher

## Task 1: Add launcher tests for CCSESSION_PERMISSIONS to tests/unit/test_ccsession_tag.py

Source requirement: tests that fail on the old code (set: no bypass flag and shim/model routing kept; unset: unchanged). Work in `tests/unit/test_ccsession_tag.py`, next to `test_every_launch_restores_grep_and_glob` (it asserts the default flags on all six launch lines).

- Give `_label_launch` an optional keyword argument `extra_env: dict[str, str] | None = None` that is merged into the child environment after `HOME`, `CLAUDE_BIN` and `CCSESSION_ENV_FILE`; existing callers stay unchanged.
- Add `CCSESSION_PERMISSIONS` to the variables deleted by the autouse environment-clearing block near the top of the file (the list that holds `CCSESSION_LAUNCH_ID` and `CLAUDE_TOPIC`), and to the excluded-names tuple in `_orca_env` (the tuple that holds `CC_CLAUDE_FLAGS`), so a value in the developer's shell never leaks into a test.
- Name every new test in this task `test_permissions_default_<what it checks>` so `-k permissions` selects them. Add a parametrized test over the same arguments-and-transcript matrix as `test_every_launch_restores_grep_and_glob` (all six launch lines: untagged, new and resumed, each with and without `--profile claude`) that runs with `CCSESSION_PERMISSIONS=default` and `CC_CLAUDE_FLAGS` removed, and asserts the launched argument list starts with `--allowedTools=Grep`, contains no `--dangerously-skip-permissions`, contains `--model` exactly when `--profile` was given, and contains `--resume` exactly when a transcript exists.
- Add tests for: `CCSESSION_PERMISSIONS=""` (empty) behaving like unset (starts with `--dangerously-skip-permissions`, `--allowedTools=Grep`); `CC_CLAUDE_FLAGS=--verbose` together with `CCSESSION_PERMISSIONS=default` launching with `--verbose` first and neither default flag; an empty `CC_CLAUDE_FLAGS` with `CCSESSION_PERMISSIONS=default` taking the `--allowedTools=Grep` default and an empty `CC_CLAUDE_FLAGS` with the variable unset taking the full old default; and `CCSESSION_PERMISSIONS=bypass` making `ccsession demo` exit with status 2, print a message naming `CCSESSION_PERMISSIONS` on standard error, and never run the fake Claude (call `subprocess.run` directly with `check=False`, as `test_help_and_unknown_profile_list_data_profiles` does).

Acceptance criteria:
- Run `uv run pytest tests/unit/test_ccsession_tag.py -k "permissions or grep_and_glob" -q` against the unchanged launcher and save the output to `./artifacts/t1-red.log`: every test that sets `CCSESSION_PERMISSIONS=default` or `bypass` fails, and `test_every_launch_restores_grep_and_glob` and the empty-variable and empty-`CC_CLAUDE_FLAGS` tests pass.
- The new tests do not read or depend on the developer's own `CCSESSION_PERMISSIONS` or `CC_CLAUDE_FLAGS` values.

## Task 2: Add the ccsession-orca print-mode test to tests/unit/test_ccsession_tag.py

Depends on: Task 1

Source requirement: shim routing is kept when the variable is set, on the path the Coder wrapper actually uses (`ccsession-orca -p ...`, which hands off to `ccsession --shim --claude-args`). Work in `tests/unit/test_ccsession_tag.py`, next to `test_orca_print_mode_is_untagged_and_never_asked`, using its `_orca_no_tty(tmp_path, *args, **extra)` helper, whose record holds `argv` and `base_url`.

- Add a test named `test_orca_print_mode_permissions_default_keeps_shim_routing` that runs `_orca_no_tty(tmp_path, "-p", "hello")` once without the variable (control) and once with `CCSESSION_PERMISSIONS="default"` (passed as an extra environment value). Both calls may share one `tmp_path`: each returns its own parsed `record.json` before the next call overwrites it.

Acceptance criteria:
- The control run records `argv == [*ORCA_FLAGS, "-p", "hello"]` and the opted-in run records `argv == ["--allowedTools=Grep", "-p", "hello"]`.
- Both records pass the existing `_assert_through_shim(record)` helper (`base_url == "http://127.0.0.1:4555"` and one credential set), proving shim routing is kept.
- Saved output of `uv run pytest tests/unit/test_ccsession_tag.py -k orca_print_mode_permissions -q` against the unchanged launcher is in `./artifacts/t2-red.log` and shows this test failing on the argument list.

## Task 3: Add the tier-mode test to tests/unit/test_ccsession_tiers.py

Source requirement: tier models are kept when the variable is set. Work in `tests/unit/test_ccsession_tiers.py`, next to the launch tests that call `_launch(tmp_path, *args, defaults=TIER_BLOCK, **extra)` and read `seen["argv"]`, `seen["settings"]` and `seen["base_url"]` (the fake Claude in `_launch_env` writes them).

- Add `CCSESSION_PERMISSIONS` to the names deleted in the autouse `_isolated` fixture (the list that holds `CCSESSION_SHOW_ALL_MODELS`).
- Add a test named `test_tier_launch_permissions_default_keeps_tier_routing` that launches a tier session twice with the same arguments (one `--tier` launch that already appears in the neighbouring tests): once without the variable and once with `CCSESSION_PERMISSIONS="default"`.

Acceptance criteria:
- The opted-in run's `seen["argv"]` contains no `--dangerously-skip-permissions` and begins with `--allowedTools=Grep`; the control run's begins with `--dangerously-skip-permissions`.
- The opted-in run has the same `--settings` value, the same `--model` argument (when the control has one) and the same `base_url` as the control run.
- Saved output of `uv run pytest tests/unit/test_ccsession_tiers.py -k permissions -q` against the unchanged launcher is in `./artifacts/t3-red.log` and shows this test failing.

## Phase 2: Launcher change

## Task 4: Add the CCSESSION_PERMISSIONS switch to src/superclaude/skills/ccsession-tag/ccsession

Depends on: Task 1, Task 2, Task 3

Source requirement: when `CCSESSION_PERMISSIONS=default` is set, no permission-bypass flag on any launch; unset is unchanged; empty `CC_CLAUDE_FLAGS` handling is unchanged. Replace the single assignment `CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:---dangerously-skip-permissions --allowedTools=Grep}"` (line 124) with a `case` on `"${CCSESSION_PERMISSIONS:-}"` that picks the default flag string, then keeps the existing `:-` expansion:

```
case "${CCSESSION_PERMISSIONS:-}" in
  "") _cc_default_flags="--dangerously-skip-permissions --allowedTools=Grep" ;;
  default) _cc_default_flags="--allowedTools=Grep" ;;
  *) echo "ccsession: CCSESSION_PERMISSIONS must be 'default' or unset (got '$CCSESSION_PERMISSIONS')" >&2; exit 2 ;;
esac
CC_CLAUDE_FLAGS="${CC_CLAUDE_FLAGS:-$_cc_default_flags}"
```

The six `exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ...` launch lines (around lines 1799 to 1868) already expand the variable and are not edited.

Acceptance criteria:
- `bash -n src/superclaude/skills/ccsession-tag/ccsession` reports no syntax error.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py -q` passes completely, with the output saved to `./artifacts/t4-green.log`; the tests from Tasks 1 to 3 that failed in their red logs now pass.
- `git diff` of `src/superclaude/skills/ccsession-tag/ccsession` shows changes only in the flag-default block (no launch line and no handling of an empty `CC_CLAUDE_FLAGS` changed).

## Task 5: Document CCSESSION_PERMISSIONS in the header of src/superclaude/skills/ccsession-tag/ccsession

Depends on: Task 4

Source requirement: document the variable where ccsession documents its other variables. The comment block above the code (printed by `ccsession --help`) states that the wrapper "always runs claude with --dangerously-skip-permissions and --allowedTools=Grep" and that `CC_CLAUDE_FLAGS` overrides it (lines 109 to 114), and lists settings such as `CCSESSION_SHOW_ALL_MODELS=1` near line 96.

- Rewrite the sentence "always runs claude with ..." so it no longer says "always", and add a short paragraph: `CCSESSION_PERMISSIONS=default ccsession ...` (shell environment, not `~/.claude/ccsession.env`) starts Claude with only `--allowedTools=Grep` and no `--dangerously-skip-permissions`, any other non-empty value is an error, and a non-empty `CC_CLAUDE_FLAGS` still replaces the defaults either way. Keep the existing explanation of why `--allowedTools=Grep` is kept and the note about the `=` form.

Acceptance criteria:
- `src/superclaude/skills/ccsession-tag/ccsession --help` output contains `CCSESSION_PERMISSIONS=default` and no longer contains the word "always" in the permissions paragraph.
- `uv run pytest tests/unit/test_ccsession_tag.py -q` still passes (its help-text tests included).

## Phase 3: User documentation

## Task 6: Add CCSESSION_PERMISSIONS to the settings table in src/superclaude/skills/ccsession-tag/README.md

Depends on: Task 4

Source requirement: document the variable beside the other variables. The settings table (header `| Setting | Effect |`, rows such as `CCSESSION_SHOW_ALL_MODELS=1` and `CCSESSION_COOLDOWN_SECONDS`, around lines 498 to 515) is where the README lists ccsession's variables.

- Add a row `CCSESSION_PERMISSIONS=default` with the effect: start Claude without `--dangerously-skip-permissions` (only `--allowedTools=Grep` stays, so Grep and Glob remain available); shim and tier-model routing are unchanged; read from the shell environment, not `~/.claude/ccsession.env`; any other non-empty value exits with status 2; a non-empty `CC_CLAUDE_FLAGS` still wins. Add a second row `CC_CLAUDE_FLAGS` only if the table has none, stating it replaces the default flags and that an empty value takes the default.

Acceptance criteria:
- The README table contains a `CCSESSION_PERMISSIONS=default` row with all the points above and renders as a valid Markdown table (same column count on every row).
- `grep -n CCSESSION_PERMISSIONS src/superclaude/skills/ccsession-tag/README.md` shows the row.

## Task 7: Note the variable in src/superclaude/skills/ccsession-tag/ccsession.env.example

Depends on: Task 4

Source requirement: document the variable where ccsession's other variables are documented, and prevent the trap that the env file cannot set it. In the "Coder workspaces (tier mode) — optional settings" comment block (around line 25), add one comment line explaining that `CCSESSION_PERMISSIONS=default` must be set in the shell environment that starts `ccsession`, because this file is read after the launch flags are chosen.

Acceptance criteria:
- `src/superclaude/skills/ccsession-tag/ccsession.env.example` has one added comment line naming `CCSESSION_PERMISSIONS` and the shell-environment limit, and the file stays all comments (no active `export` line added).

## Task 8: Update the permission sentence in the two v5.0.0 testing guides

Depends on: Task 4

Source requirement: docs that state the permission default must stay true. Two guides say `ccsession` starts Claude Code with `--dangerously-skip-permissions --allowedTools=Grep` "unless `CC_CLAUDE_FLAGS` is set": `docs/testing/v5.0.0/user/D08-ccsession.md` (line 23) and `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` (line 21).

- In each file, extend only that sentence: or `CCSESSION_PERMISSIONS=default` is set, in which case only `--allowedTools=Grep` is added. Do not add test steps and do not change the other `CC_CLAUDE_FLAGS` lines of D08 (lines 199 and 210).

Acceptance criteria:
- Both sentences mention `CCSESSION_PERMISSIONS=default`; `git diff --stat` for these two files shows one changed line each.

## Phase 4: Release note

## Task 9: Add the CHANGELOG.md entry under Unreleased

Depends on: Task 4, Task 5, Task 6, Task 7

Source requirement: the repository records user-visible changes in `CHANGELOG.md` under `## [Unreleased]`, newest section first, as `### <area>: <summary> (#<issue>)` with `#### Added (...)` bullets.

- Add a section at the top of `## [Unreleased]`: `### ccsession: start Claude without the permission bypass (#390)` with an `#### Added (ccsession permissions)` bullet describing `CCSESSION_PERMISSIONS=default` (what it drops, what it keeps, unset is unchanged, other values exit 2, shell environment only, a non-empty `CC_CLAUDE_FLAGS` still wins, an empty one still takes the default) and one sentence saying callers such as the Coder `claude` wrapper opt in themselves; `superclaude reflect` is not changed.

Acceptance criteria:
- `CHANGELOG.md` has the new section directly under `## [Unreleased]` and above the existing onboarding-deck section, with every behavior in the bullet matching the tests of Tasks 1 to 3.
- After all edits to `src/superclaude/skills/ccsession-tag/`, `make sync-dev` followed by `make verify-sync` exits 0 (the gitignored `.claude/` copies are refreshed and never staged).
