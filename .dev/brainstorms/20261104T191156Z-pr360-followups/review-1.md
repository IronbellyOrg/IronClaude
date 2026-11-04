# Review 1: PR #360 follow-ups (adversarial)

Scope: uncommitted diff in `src/superclaude/cli/install_user_setup.py`,
`tests/cli/test_install_user_setup.py`, `CHANGELOG.md`,
`docs/getting-started/installation.md`. Baseline: `HEAD` (605da2ff).
Python used by `uv run`: 3.13.5.

## Verdict

FAIL. The code fixes are correct and the tests are sound; one user-facing
claim in the CHANGELOG and the installation guide is false.

## Blocking findings

### B1. "Like the rest of the setup" is false: the MCP step still writes into the `CLAUDE_CONFIG_DIR` profile

- Where: `CHANGELOG.md:13` ("`$HOME/.claude`, the profile it checks and every
  other install step writes" ... "the default plugins are now installed into
  `$HOME/.claude`, like the rest of the setup, not into that profile") and
  `docs/getting-started/installation.md:497-498` ("If you set
  `CLAUDE_CONFIG_DIR`, it is used only to find `.claude.json` when reading MCP
  registrations").
- Defect: `superclaude install` step 8 (`src/superclaude/cli/main.py:246`,
  `install_codegraph_mcp(scope="user")`) registers codegraph through
  `claude mcp add/remove --scope user` (`src/superclaude/cli/install_mcp.py:896`
  via `_exec_claude` -> `_bounded`, `install_mcp.py:769-783`, and the
  `claude mcp add` builder near `install_mcp.py:1255`). None of these pass
  `env=`, so the `claude` child inherits `CLAUDE_CONFIG_DIR` and writes
  `$CLAUDE_CONFIG_DIR/.claude.json`, which is also where the installer reads it
  back (`install_mcp.py:721-726`). So `CLAUDE_CONFIG_DIR` is not used "only to
  find `.claude.json` when reading": it also decides where MCP registrations
  are written, and "every other install step writes" `$HOME/.claude` is untrue.
- Failing scenario: a user with `CLAUDE_CONFIG_DIR=/cfg` runs
  `superclaude install`. After this change, codegraph is registered in
  `/cfg/.claude.json` while the default plugins go to `$HOME/.claude/plugins`.
  The CHANGELOG tells them everything now lands in `$HOME/.claude` "like the
  rest of the setup"; in fact the install is split across two profiles, and
  starting Claude Code with either profile misses part of it.
- Fix (wording only, the code is fine): say that the plugin commands now act on
  `$HOME/.claude` like the installer's files, while MCP registrations still
  follow `CLAUDE_CONFIG_DIR` (they go to `$CLAUDE_CONFIG_DIR/.claude.json`).
  Reword the guide sentence to "it decides where MCP registrations are read
  and written (`$CLAUDE_CONFIG_DIR/.claude.json`)". The task brief's "every
  other installer step ... ignores CLAUDE_CONFIG_DIR" premise is true only for
  files under `~/.claude/`, not for the `claude mcp` subprocesses.

## Minor findings

1. Unrecorded behaviour change for non-list or empty records
   (`install_user_setup.py:324-329`). Verified with temp homes:
   - `"plugin": []` was "installed" before (a non-pinned plugin was skipped, a
     pinned one got `plugin update`); now it gets `plugin install --scope user`.
   - a dict-shaped record (the older non-list `installed_plugins.json` layout)
     was "installed" before; now it is dropped and `plugin install` runs on
     every `superclaude install`.
   - `scope: "local"` now counts as not installed (consistent with the intent).
   - a record with no `scope` key still counts as user (unchanged).
   Probably the right call, but the CHANGELOG only mentions project scope, and
   `test_plugins_skip_already_installed` (`tests/cli/test_install_user_setup.py:645-661`)
   was edited from `[]` to `[{"scope": "user"}]`, which removes the old
   coverage instead of pinning the new empty-list behaviour. Add one case
   that asserts `[]` now yields `plugin install`, and mention it in the
   CHANGELOG bullet.
2. Remaining crash path, not new: `{e.get("gitCommitSha") for e in installed[p]}`
   (`install_user_setup.py:341`) raises `TypeError: unhashable type` when a
   user-scope record of a pinned plugin has a list or object `gitCommitSha`
   (reproduced: `install_plugins` raised). HEAD has the same expression, so this
   is not a regression. The change is about "the plugin step must never be
   fatal", so it is worth closing (e.g. keep only `str` values). The
   `isinstance(e, dict)` filter at line 341 is now redundant because line 325
   already filters.
3. Unverified CLI behaviour for the "project-only" case: the code now runs
   `claude plugin install <p> --scope user -y` when a plugin is installed only
   at project scope. I could not confirm (without running `claude`) that CLI
   2.1.318 accepts a user-scope install alongside a project-scope one instead of
   exiting non-zero with "already installed". If it refuses, that workspace gets
   a non-fatal warning on every run. Worth one manual check.
4. Test strength:
   - `test_plugins_move_ponytail_to_a_new_pin` asserts
     `"CLAUDE_CONFIG_DIR" not in calls[0][1]` (`tests/...:400`) without setting
     the variable, so on a clean shell it only proves an env dict is passed.
     It also never checks `HOME`/`CLAUDE_CONFIG_DIR` on the `plugin update` call
     (`calls[1]`). The new validated-home test covers `add` and `install` only.
     Setting `CLAUDE_CONFIG_DIR` there and asserting on both calls closes the
     gap for the update path.
   - In `test_plugins_run_claude_against_the_validated_home` (`:406-439`) the
     foreign `cfg/plugins/known_marketplaces.json` is never read by anything
     (the fake `claude` does not open it). It is decoration; the test would pass
     without it. Harmless, but it does not prove what its setup suggests.
   - `test_plugins_refuse_an_unresolvable_ironclaude_registration` (`:525`):
     on Python 3.13+ (this environment) the symlink-loop case does not raise
     and passes only because the resolved path differs. The comment at `:531`
     says so; only the NUL case exercises the new `except` here. That is
     acceptable, but the 3.10-3.12 branch is covered only by CI on those
     versions.
5. `docs/getting-started/installation.md:478-479` ("Ponytail keeps its files
   under `CLAUDE_CONFIG_DIR` when that variable is set") is now mostly moot:
   with the plugin installed only in `$HOME/.claude`, a session started with
   `CLAUDE_CONFIG_DIR` set (to another directory) does not load Ponytail at
   all. Not changed by this diff; consider folding it into the note at 494.
6. `env["HOME"] = str(home)` (`install_user_setup.py:407`): in production
   `home` is `Path.home()`, which on POSIX is `$HOME` (normalised), so this is
   effectively a no-op apart from setting `HOME` when it was unset, which is fine.
   It also changes `HOME` for git inside `claude plugin update`, but only in
   tests, where `home` is a temp dir.

## Self-audit

What I checked, and the result:

- Fix 1 (`_is_our_catalog`, `install_user_setup.py:292-295`): catches
  `OSError`, `RuntimeError`, `ValueError` around both `resolve()` calls, and
  returns False, which takes the "registered from another source" branch
  (`:355-362`): pinned plugins are dropped from `wanted`, the user's registry is
  left alone, other plugins proceed. Confirmed on this interpreter: the NUL
  path raises `ValueError` from `lstat`, the loop path does not raise on 3.13.
  The new test fails on HEAD: the uncaught `ValueError` escapes
  `install_plugins`.
- Fix 2 (`:320-342`): only `scope == "user"` (or missing scope) records count,
  for both the "installed?" and the "stale?" decisions. `records` that are not a
  dict, records that are not lists, and entries that are not dicts are tolerated
  (no new crash). Both cases of the new test fail on HEAD: "mixed" (HEAD sees the
  project record's pin, so no commands) and "project-only" (HEAD treats it as
  installed, so no install).
- Fix 3 (`:404-409`): every command gets a copy of `os.environ` without
  `CLAUDE_CONFIG_DIR` and with `HOME=home`; `update` adds `_HTTPS_GITHUB`;
  `marketplace update` does not (args[1] is "marketplace"). Matches the
  documented CLI rule (unset -> `$HOME/.claude`). The new test fails on HEAD for
  both the set and the empty `CLAUDE_CONFIG_DIR` cases (env None -> inherits the
  variable / the developer's real HOME), and the edited move-pin test fails on
  HEAD (`calls[0][1]` is None).
- Test isolation: the new tests use `monkeypatch` for `CLAUDE_CONFIG_DIR`,
  `SENTINEL`, `GIT_CONFIG_COUNT`, `which` and `subprocess.run`; no real `claude`
  is run, and no test reads the developer's `~/.claude`. Because the code now
  strips `CLAUDE_CONFIG_DIR` and sets `HOME`, a developer's own
  `CLAUDE_CONFIG_DIR` can no longer leak into plugin tests.
- Crash paths in `install_plugins`: probed empty list, dict record, missing
  scope, local scope, and list `gitCommitSha` in temp homes; only the last
  raised, and it is pre-existing (Minor 2).
- Docs and CHANGELOG checked against code: bullets 1 and 2 are accurate;
  bullet 3 and the guide note are wrong about MCP (B1).
- `uv run --extra dev pytest tests/cli/test_install_user_setup.py -q`: 29
  passed. `ruff check` and `ruff format --check` on both Python files: clean.
- Not done, as instructed: no `claude`, no `superclaude install`, no edits
  outside this report, no `git stash`.
