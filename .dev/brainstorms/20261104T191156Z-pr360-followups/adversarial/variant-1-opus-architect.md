# Variant 1 (architect): fix spec for the PR #360 follow-up findings

Persona: architect. Source: src/superclaude/cli/install_user_setup.py at master 605da2ff.

## Summary

All three findings share one root: `install_plugins` resolves a single `home` (install_user_setup.py:303) and derives every read and write from it (settings 311, plugin registry and records 315-317, catalog 276, 292, 349, 352), but two things leak outside that root. A path comparison can throw out of the function (292), and every `claude` subprocess picks its profile from the inherited environment (392), not from `home`. The stale check also reads records of every scope while every command it drives acts at user scope (323-330, 372-378).

The fix keeps `home` as the only root of truth and makes everything agree with it:

| Finding | Decision | Where |
|---|---|---|
| 1. Symlink loop escapes `_is_our_catalog` | Catch `(OSError, RuntimeError)` around the `resolve()` comparison only; an unresolvable path means "not ours", so the existing refusal path runs | install_user_setup.py:292 |
| 2. Stale check ignores scope | Build `installed` from user-scope records only; a project-scope-only plugin counts as not installed at user scope and gets `plugin install --scope user` | install_user_setup.py:317 |
| 3. Profile mismatch | Option C: each `claude` subprocess gets an environment without `CLAUDE_CONFIG_DIR` and with `HOME=str(home)` | install_user_setup.py:392 |

Three edits in install_user_setup.py, one source file plus its test file, so this is a level-2 direct change (at most 5 edits). No new helper, no new dependency, no other installer step touched.

## Finding 1: symlink loop in `_is_our_catalog`

### Decision

Catch exactly `(OSError, RuntimeError)` around the comparison on line 292 and return `False`. Do not wrap the whole function or catch `Exception`.

Rationale:

- Lines 286-291 cannot raise: they only call `dict.get`, `isinstance` and `Path(...).is_absolute()` on a value already checked to be `str` (install_user_setup.py:286-291). Only the two `resolve()` calls on 292 touch the filesystem.
- `(OSError, RuntimeError)` is the tuple the repo's only other `CLAUDE_CONFIG_DIR`-aware reader already uses for the same class of path failure (install_mcp.py:739). Reusing it keeps one convention.
- Verified on the project interpreter (CPython 3.11.15, via `uv run python -I`, two symlinks pointing at each other under `/tmp`): non-strict `Path.resolve()` raises `RuntimeError: Symlink loop from ...`. The Python 3.13 documentation for `Path.resolve` says that from 3.13 loops are treated like other errors: `OSError` in strict mode, and no exception in non-strict mode (the path is resolved as far as possible). That 3.13 point was not reproduced here (no 3.13 interpreter in this workspace), and it contradicts the seed brief's "OSError (3.13+, ELOOP)" for the non-strict call used on 292. Either way, catching both covers 3.10-3.12 (`RuntimeError`) and any `OSError` a non-strict resolve still lets through (for example a permission error on `readlink`).
- `False` means "not IronClaude's catalog". Line 343 then takes the refusal branch (346-350), line 360 drops the pinned plugins from `wanted`, and line 361 clears `stale`. Other plugins still go through 362-379. That is exactly the success criterion: `(True, "⚠️ ...")`, `ironclaude` refused, others proceed.
- A catch-all would hide programming errors in a function that guards a security decision (which marketplace may install a pinned plugin). The narrow catch is correct here.

The loop on our own side (`home / _CATALOG_DIR`) is reached first by `_write_catalog` (276-280); `mkdir` on a looping path raises `OSError`, caught at 340 ("catalog not written"). The new catch also covers it on 292 should the loop appear between the two calls.

### Change (edit 1, line 292)

```python
    try:
        return Path(path).resolve() == (home / _CATALOG_DIR).resolve()
    except (OSError, RuntimeError):  # a symlink loop or unreadable link
        return False
```

### Regression test

`test_plugins_refuse_a_catalog_path_that_cannot_resolve`, looping over `exc in (RuntimeError, OSError)` (one subdirectory of `tmp_path` per case).

- Setup: `home = _pinned_home(case_dir, PONYTAIL_SHA, PONYTAIL_SHA)`; rewrite `home/.claude/settings.json` to enable both `ponytail@ironclaude` and `playwright@claude-plugins-official`; create a real loop (`case_dir/"loop"` -> `case_dir/"loop2"` -> `case_dir/"loop"`); write `known_marketplaces.json` with `{"ironclaude": {"source": {"source": "directory", "path": str(case_dir/"loop")}}, "claude-plugins-official": {}}`. Monkeypatch `setup.Path.resolve` with a wrapper that raises `exc` when `self.name == "loop"` and otherwise calls the original (so `Path(__file__).resolve()` at 309 still works). The wrapper makes the test fail on current code on every Python version; on 3.13 the real loop alone might not raise. Fake `subprocess.run` with `_recording_run(calls)`.
- Assert: `ok is True`; message starts with `"⚠️  Plugins"`; `"ironclaude (registered from another source"` in message; no recorded call contains `ironclaude`; `["plugin", "install", "playwright@claude-plugins-official", "--scope", "user", "-y"]` in calls.
- Why it fails today: line 292 has no handler and line 343 is outside any `try` (the `try` at 338-341 covers only `_write_catalog`), so the exception propagates out of `install_plugins` and the test errors.

## Finding 2: scope-blind stale and installed checks

### Decision

Count only records with `"scope": "user"`. A plugin whose only records are project scope is **not installed** for this installer's purposes, so it gets `claude plugin install <id> --scope user -y`, never `plugin update`.

Rationale:

- Every command the step issues acts at user scope: `plugin install ... --scope user -y` (372) and `plugin update ... --scope user` (377). The wanted list comes from the user-scope settings file (311). A record of any other scope says nothing about the copy those commands manage.
- A project-scope copy is active only inside its `projectPath`. Treating it as "installed" leaves every other project without the plugin even though user settings enable it.
- Treating project-only as "stale" (the current outcome when its sha is off the pin) issues `plugin update --scope user` for a plugin with no user-scope copy to update. Install is the right verb.
- The seed brief's real-CLI proof shows one plugin id maps to a list holding both a user and a project record, so a user-scope install alongside an existing project copy is a supported state, not a conflict.
- Strict `scope == "user"`: the proven record format always carries `scope` (seed brief, Known Context). A record without it is not provably user scope; the cost of misjudging it is one `plugin install` that either succeeds or is reported as a non-fatal warning (409-413).

The filter goes where the data enters (317), not into the two consumers (323-330 and 374). Both consumers then become scope-correct with no further edit. Line 329's own `isinstance(e, dict)` filter becomes redundant but harmless (left alone to keep the diff minimal).

### Change (edit 2, line 317)

```python
    records = _read_json(plugins_dir / "installed_plugins.json").get("plugins")
    records = records if isinstance(records, dict) else {}
    # Only user-scope copies count: every command below acts at user scope, and
    # a project-scope copy (even one at the pin) covers a single project.
    installed = {
        p: [e for e in entries if isinstance(e, dict) and e.get("scope") == "user"]
        for p, entries in records.items()
        if isinstance(entries, list)
    }
    installed = {p: user for p, user in installed.items() if user}
```

This mirrors the existing "read, then coerce the shape" pattern at 312-313. The `isinstance(records, dict)` guard is required because the new code calls `.items()`; today a non-dict `plugins` value is tolerated by `in` (317, 327, 374), and the change must not add a crash path.

### Regression test

`test_plugins_update_a_stale_user_copy_beside_a_project_copy_at_the_pin`.

- Setup: `old = "16352ac229eb08a9598dcae48fe9f2b342567d86"`; `home = _pinned_home(tmp_path / "both", old, PONYTAIL_SHA)` (catalog on disk already equals the defaults, so `changed` is False); overwrite `installed_plugins.json` with `{"plugins": {"ponytail@ironclaude": [{"scope": "project", "projectPath": str(tmp_path / "proj"), "gitCommitSha": PONYTAIL_SHA}, {"scope": "user", "gitCommitSha": old}]}}`. Record calls with `_recording_run(calls)`.
- Assert: `calls == [["plugin", "marketplace", "update", "ironclaude"], ["plugin", "update", "ponytail@ironclaude", "--scope", "user"]]`.
- Second case in the same test (project scope only, `tmp_path / "project"`): records hold only the project record at `PONYTAIL_SHA`; assert `calls == [["plugin", "install", "ponytail@ironclaude", "--scope", "user", "-y"]]`.
- Why it fails today: the sha set at 329 includes the project record's `PONYTAIL_SHA`, so `stale` is empty; with `changed` False nothing is queued and the function returns `"✅ Plugins: already installed"` (380-381). In the second case `p in installed` is true at 374, so no install is queued either.

## Finding 3: profile mismatch between validation and `claude` subprocesses

### Options

| | A. Honour `CLAUDE_CONFIG_DIR` for plugin state | B. Refuse pinned plugins when the profile differs | C. Pin every `claude` subprocess to `home` |
|---|---|---|---|
| What changes | `plugins_dir` (315) and probably the catalog (276, 292, 352) move to `$CLAUDE_CONFIG_DIR` (no `.claude` segment, per the real-CLI proof); subprocesses inherit as today | Compare `$CLAUDE_CONFIG_DIR` with `home/.claude`; on mismatch refuse the `ironclaude` marketplace like 346-350 | Subprocess env = `os.environ` minus `CLAUDE_CONFIG_DIR`, plus `HOME=str(home)` (392) |
| Coherence with the wanted list | Broken. `wanted` and the user's `false` opt-outs come from `home/.claude/settings.json` (311), written by `apply_settings_defaults` (163, 191). The CLI under `CLAUDE_CONFIG_DIR` reads and writes `$CLAUDE_CONFIG_DIR/settings.json`. Opt-outs live in one file, installs and enablement in another | Partial. Pinned plugins are safe, but non-pinned plugins still check `installed` in `home` (374) and install into the other profile, so they are re-installed on every run | Full. Settings read (311), registry and records read (315-317), catalog (276) and every command all use `home/.claude` |
| Coherence with other installer steps | Plugins land in one profile; rules (115), output styles (147), settings defaults (163), Orca skills (235), commands, skills, agents and hooks in another. A half-installed profile on both sides | The other profile gets non-pinned plugins and nothing else | Matches every other step: everything lands in `home/.claude` |
| Finding 3 success criterion | Met only if every path moves together and is validated against the same root | Met for `ironclaude` commands only | Met: no command can run against an unvalidated profile, because the only profile a command can see is the validated one |
| New surface | A resolver (empty string, `~`, relative path rules), path moves, fixtures for two roots | A path comparison (needs its own loop handling, finding 1 again), a new refusal message | None. One env block |
| Edits in this file | 4 or more (315, 276, 292, 349/352, plus a resolver) | 2 or more | 1 |
| User-visible cost | None, if done right everywhere | Ponytail silently missing whenever the variable is set, even when the user wants it | A user who runs `claude` with `CLAUDE_CONFIG_DIR=X` does not get the plugins in profile X, just as they already do not get rules, skills, commands, agents or hooks there |

### Decision: Option C

The installer has one notion of where Claude Code lives: `Path.home()/.claude`. `apply_settings_defaults` writes `enabledPlugins` there (163-191), and `install_plugins` reads its wanted list from the same file (311). Option A makes the plugin step the only step that follows `CLAUDE_CONFIG_DIR`, which splits the user's opt-outs from the profile that gets installed and leaves both profiles half-built. Option B keeps the split for every non-pinned plugin and only hides the symptom for one marketplace. Option C removes the divergence at the one point where it enters, the subprocess boundary, and makes the plugin step consistent with every other step.

Long-term view: supporting `CLAUDE_CONFIG_DIR` is a whole-installer decision (one root resolved once in `install_user_setup`, 417-427, and passed to every step as `home`). Option C keeps that future change in one place: after C, the plugin step's profile is fully determined by its `home` argument, so a later change that passes a different root needs no change inside `install_plugins`. Option A would bake a second, plugin-only root into this function that a whole-installer change would have to undo.

Why `HOME=str(home)` as well as dropping `CLAUDE_CONFIG_DIR`: without the variable, the CLI falls back to its home directory (proven: `CLAUDE_CONFIG_DIR=""` behaves as unset and reads `$HOME/.claude/plugins`). Setting `HOME` makes the command's profile equal to the validated `home` by construction rather than by assumption. In production `home = Path.home()` (303), and on POSIX `Path.home()` returns `$HOME` when it is set, so this is a no-op for the normal case. It matters only when `HOME` is unset (Python then falls back to the password database) and in tests, where `home` is a temporary directory.

### Catalog location (open question)

The catalog stays at `home/.claude/ironclaude-marketplace` (`_CATALOG_DIR`, 47). It is registered by absolute path (352), so its location does not affect correctness, and under Option C it already sits inside the validated profile. Moving it would add edits and a migration for existing registrations with no benefit.

### Change (edit 3, line 392)

```python
        # Every command uses the profile validated above (home/.claude), the one
        # every other install step writes, whatever CLAUDE_CONFIG_DIR says.
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
        env["HOME"] = str(home)
        if args[1] == "update":
            env.update(_HTTPS_GITHUB)
```

`os` is already imported (24). Built inside the loop to keep this a single edit block; the cost is one dict copy per command, a handful per run.

### Regression test

`test_plugins_run_claude_against_the_validated_home`.

- Setup: `monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "cfg"))`; write `tmp_path/"cfg"/"plugins"/"known_marketplaces.json"` holding a foreign `ironclaude` (`{"ironclaude": {"source": {"source": "github", "repo": "someone/ironclaude"}}}`); `home = _plugin_home(tmp_path / "home", {"ponytail@ironclaude": True})` (no registry in `home`, so the run queues `marketplace add` for our catalog and `plugin install`). Fake `subprocess.run` records `(command[1:], kwargs.get("env"))`.
- Assert: commands are `[["plugin", "marketplace", "add", str(home / setup._CATALOG_DIR)], ["plugin", "install", "ponytail@ironclaude", "--scope", "user", "-y"]]`; for every recorded env: `env is not None`, `"CLAUDE_CONFIG_DIR" not in env`, `env["HOME"] == str(home)`.
- Why it fails today: line 392 passes `env=None` for every command except `plugin update`, so the child inherits `CLAUDE_CONFIG_DIR` and runs against `cfg`, the profile holding the foreign `ironclaude`, which was never validated. `env is not None` fails on the first call.

## Convergence point and edit count

Convergence point: the `home` value resolved at install_user_setup.py:303. Every plugin-state path already derives from it (settings 311, `plugins_dir` 315, records 317, catalog 276/292/349/352). The single place where state escaped that root is the subprocess environment at 392, so finding 3's fix goes there and no path changes. Findings 1 and 2 are fixed where their data enters the function: the one filesystem comparison (292) and the one records read (317).

Edits in src/superclaude/cli/install_user_setup.py (an edit = one block of consecutive changed lines):

| # | Lines today | Function | Finding |
|---|---|---|---|
| 1 | 292 | `_is_our_catalog` | 1 |
| 2 | 317 | `install_plugins` | 2 |
| 3 | 392 | `install_plugins` | 3 |

Total: 3 edits, one source file plus tests/cli/test_install_user_setup.py. Within the 5-edit limit for a direct change. `_read_json` (266-271) and `_write_catalog` (274-281) are unchanged.

## Existing test impact

| Test | Line | Change needed | Why |
|---|---|---|---|
| `test_plugins_move_ponytail_to_a_new_pin` | 397 | Replace `assert calls[0][1] is None` with `assert calls[0][1]["HOME"] == str(home)` and `assert "GIT_CONFIG_VALUE_0" not in calls[0][1]`. Line 398 stays | The marketplace-update env is no longer `None` (finding 3); the intent of 397 (only `plugin update` gets the HTTPS git settings) is kept |
| `test_plugins_skip_already_installed` | 545 | Fixture: `"playwright@claude-plugins-official": [{"scope": "user"}]` instead of `[]` | An empty record list has no user-scope copy, so it now counts as not installed (finding 2); the fake then raises `AssertionError`, which the `except` at 403 does not catch. A real installed plugin always has a record |
| `_pinned_home` | 366 | None | Its record already carries `"scope": "user"` |
| `test_plugins_accept_ours_through_a_symlinked_home` | 449-462 | None | Resolution is kept; the new `try` only adds a fallback |
| `test_plugins_refuse_a_foreign_ironclaude_marketplace` | 421-446 | None | No `resolve()` failure in its entries; asserts no `ironclaude` command, unaffected by env |
| tests/cli/test_update_command.py | 40, 45 | None | Sets `CLAUDE_CONFIG_DIR` but replaces `install_plugins` with a fake |

The other plugin tests (317-354, 401-407, 465-534, 554-580, and the opt-out check at 219-233) record only commands or use no installed records and are unaffected.

## Risks and edge cases

- **Empty `CLAUDE_CONFIG_DIR`.** The real CLI treats `""` as unset (seed brief). Option C removes the key whatever its value, so empty, unset and set all behave the same. No resolver is needed, so the install_mcp.py:722 "empty means unknown" rule does not have to be copied.
- **`~` in `CLAUDE_CONFIG_DIR`.** Irrelevant under C: the value is never read or expanded. Under A it would have needed `expanduser` (as install_mcp.py:725 does) plus an unverified guess about whether the Node CLI expands `~` itself; that uncertainty is one more reason against A.
- **Symlinked home.** `HOME=str(home)` is the unresolved path; the CLI writes through the symlink into the same directory. `marketplace add` registers `str(home / _CATALOG_DIR)` unresolved (352), and `_is_our_catalog` keeps resolving both sides (292), so `test_plugins_accept_ours_through_a_symlinked_home` still passes.
- **Project-scope-only record.** Counts as not installed at user scope, so `plugin install --scope user -y` runs (finding 2 decision). If the real CLI refused a user install while a project copy exists, the result is a non-fatal warning (409-413), not an abort. The seed brief's proof that both records coexist in one list makes this unlikely. Not verified against the real CLI here (forbidden by constraints).
- **Python 3.13 resolve behaviour.** Python < 3.13 raises `RuntimeError` on a loop (verified on 3.11.15). The 3.13 docs say non-strict resolve no longer raises on loops (not verified locally); a loop then simply compares unequal and is refused, which is the same outcome the catch produces. `OSError` from other causes is still possible on every version and is caught. The regression test forces the exception with a scoped `Path.resolve` wrapper so it fails on current code on every interpreter.
- **Records without `scope`.** Treated as not user scope; at worst one extra `plugin install` per run, reported if it fails.
- **`HOME` on Windows.** Node's `os.homedir()` uses `USERPROFILE` on Windows, so `HOME` there is harmless and `CLAUDE_CONFIG_DIR` removal still applies. Coder workspaces are Linux.
- **Git under `plugin update`.** `HOME` decides which `~/.gitconfig` git reads; in production it is unchanged, and the HTTPS rewrite still comes from the `_HTTPS_GITHUB` env (50-54), which git applies on top of config files.
- **User expectation under C.** A user who deliberately runs Claude Code with `CLAUDE_CONFIG_DIR` gets no plugins in that profile from `superclaude install`. That matches every other installer step today and is the honest scope boundary. It is not a regression of anything that worked: before this fix the plugin step validated one profile and wrote another.
- **Non-dict `plugins` in `installed_plugins.json`.** Guarded in edit 2, so no new crash path.

## Out of scope

- Making `superclaude install` honour `CLAUDE_CONFIG_DIR` for any step (rules, output styles, settings defaults, Orca skills, commands, skills, agents, hooks). That is a whole-installer root decision for `install_user_setup` (417-427), not a plugin fix.
- A warning when `CLAUDE_CONFIG_DIR` is set and differs from `home/.claude`. Useful, but a new user-facing behaviour, not a fix for the three findings.
- Changing `_read_json`, `_write_catalog`, the catalog location or `_CATALOG_DIR`.
- Records with no `gitCommitSha` (non-git sources) being flagged stale on every run; pre-existing and unrelated.
- Running real `claude plugin` commands or `superclaude install` to confirm CLI behaviour for a user install beside a project copy.
- The `read_user_mcp_servers` resolver in install_mcp.py (709-741); not reused because Option C needs no resolver.
