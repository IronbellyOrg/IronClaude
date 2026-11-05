---
variant: 2
persona: refactorer
model: sonnet
type: spec
topic: pr360-followups
source_commit: 605da2ff (master) / branch ironbelly/pr360-followups
---

# Variant 2 (refactorer): fix spec for the three PR #360 findings

## Summary

Three small, independent edits in `src/superclaude/cli/install_user_setup.py` fix all three findings. No new function, constant, import or dependency. Finding 3 takes **option C**: pin every `claude` subprocess to the validated `home`.

| Finding | Decision | Where |
|---|---|---|
| 1. resolve() escape | Wrap only the final comparison in `_is_our_catalog` in `try/except (OSError, RuntimeError, ValueError)`; return `False` (fail closed, so the existing "registered from another source" refusal fires) | line 292 |
| 2. scope-blind stale check | Filter `installed_plugins.json` to user-scope records once, at the read. Both the stale check and the "already installed" check then see only the scope the step manages. A project-only record means "not installed", so the step installs at user scope | line 317 |
| 3. profile mismatch | Build one env for every `claude` subprocess: `os.environ` minus `CLAUDE_CONFIG_DIR`, plus `HOME=str(home)` (plus `_HTTPS_GITHUB` for `plugin update`, as now) | line 392 |

Edit count in `install_user_setup.py`: **3 blocks** (one per finding). One source file plus its test file, at most 5 edits: this qualifies as a direct level-2 change; no written plan is required.

Two facts found while verifying the seed brief, both of which change the work:

1. **Python 3.13 does not raise on a symlink loop.** The seed brief says non-strict `resolve()` raises `OSError` on 3.13+. I ran `Path(...).resolve()` on a self-symlink and on an `a -> b -> a` loop in a temp dir: Python 3.11.15 raised `RuntimeError` for both; Python 3.13.5 raised nothing and returned the unresolved path. With 3.13 the loop case already ends in the existing refusal. The finding is real on 3.10 to 3.12 (and `uv run` in this checkout uses 3.11.15), but a loop-only regression test cannot fail on 3.13.
2. **An embedded NUL byte makes `resolve()` raise `ValueError` on both 3.11.15 and 3.13.5** (probed the same way). `known_marketplaces.json` is JSON, so `"path": "/x/\u0000y"` is reachable. `ValueError` must be in the except tuple, and the finding-1 regression test must use a NUL path so that it fails on every interpreter.

## Finding 1: symlink-loop `resolve()` escapes `_is_our_catalog`

### Decision (Open Question: catch only OSError/RuntimeError, or wrap the whole comparison?)

Wrap **only the final `resolve()` comparison**, and catch `(OSError, RuntimeError, ValueError)`.

Rationale:
- The rest of `_is_our_catalog` is already type-guarded (`isinstance` checks, `is_absolute()`, lines 286-291) and cannot raise. Wrapping the whole function would only hide future programming errors.
- `RuntimeError` is the symlink-loop error on Python 3.10 to 3.12 (probed: 3.11.15). `ValueError` is an embedded-NUL path (probed on 3.11.15 and 3.13.5). `OSError` stays because `resolve()` documents it and a future non-strict change may raise it; it costs nothing.
- Fail closed: an entry that cannot be resolved cannot be proven to be our catalog, so return `False`. The caller (line 343) then takes its existing refusal branch (lines 346-350): `refused` is set, pinned plugins are dropped from `wanted` and `stale` (lines 358-361), other plugins proceed, and the function still returns `(True, "⚠️ ...")`.
- The refusal text says "registered from another source". For an unresolvable path that is slightly imprecise but still safe and actionable: the hint it prints is `claude plugin marketplace add <home>/.claude/ironclaude-marketplace`, which re-registers our catalog. A distinct message would need a tri-state return, which is a new abstraction. Not worth it.
- `(home / _CATALOG_DIR).resolve()` is inside the same `try`: the right-hand side can fail the same way if `home` itself holds a loop.

### Change (`install_user_setup.py` line 292, edit 1)

Replace

```python
    return Path(path).resolve() == (home / _CATALOG_DIR).resolve()
```

with

```python
    try:
        return Path(path).resolve() == (home / _CATALOG_DIR).resolve()
    except (OSError, RuntimeError, ValueError):
        return False  # not provably ours, so treated as another source
```

### Regression test (`tests/cli/test_install_user_setup.py`, new, after `test_plugins_refuse_a_foreign_ironclaude_marketplace`)

Name: `test_plugins_refuse_an_unresolvable_ironclaude_registration`

Setup (loop over two bad registered paths, each in its own `tmp_path / str(index)` home like the existing refusal test at lines 435-446):
1. `loop = tmp_path / "loop"; loop.symlink_to(loop)`; bad paths are `str(tmp_path / "nul\x00dir")` and `str(loop)`.
2. `home = _pinned_home(tmp_path / str(index), PONYTAIL_SHA, PONYTAIL_SHA)`.
3. Rewrite `home/.claude/settings.json` so `enabledPlugins` is `{"ponytail@ironclaude": True, "playwright@claude-plugins-official": True}`.
4. Rewrite `plugins/known_marketplaces.json` to `{"ironclaude": {"source": {"source": "directory", "path": bad}}, "claude-plugins-official": {}}` (the second key stops a `marketplace add` for the official marketplace, so the only expected command is one install).
5. `monkeypatch.setattr(setup.shutil, "which", lambda _name: "/bin/claude")` and `setup.subprocess.run` replaced with `_recording_run(calls)`.

Assertions:
- `ok and message.startswith("⚠️  Plugins")`
- `"ironclaude (registered from another source" in message`
- `calls == [["plugin", "install", "playwright@claude-plugins-official", "--scope", "user", "-y"]]` (other plugins proceed; nothing mentions `ironclaude`)
- the registry file bytes are unchanged

Why it fails on current code: line 292 is outside any `try` and line 343 calls it unguarded, so `ValueError` (NUL path, every Python version) or `RuntimeError` (loop, Python < 3.13) propagates out of `install_plugins`. The NUL case guarantees a red test on 3.13 too; the loop case documents the reported scenario and is red on 3.10 to 3.12.

## Finding 2: scope-blind stale check

### Decision (Open Question: does a project-scope-only record count as installed?)

**Not installed.** Only records with `scope == "user"` count, for both the stale check and the "already installed" check.

Rationale:
- Every command this step issues is `--scope user` (`plugin install ... --scope user -y`, line 372; `plugin update ... --scope user`, line 377). The promise is about the user-scope copy, so only user-scope records are evidence about it.
- Today the stale check (lines 323-330) takes the set of `gitCommitSha` over all records of the plugin, so a project-scope copy at the pin hides a stale user-scope copy. The install check (`p not in installed`, line 374) has the mirror bug: a project-scope-only record suppresses the user-scope install.
- Both checks read the same `installed` dict (read at line 317). Filtering that dict once fixes both and leaves lines 323-330 and 374 untouched. That is the refactorer's convergence: change the data, not each consumer.
- `claude` also has `local` scope. A record that is not `"user"` (project or local) is filtered out the same way.
- A record **without** a `scope` key is treated as user scope (`e.get("scope", "user")`). That preserves today's behaviour for any older record shape, where the record would have counted.
- The same edit makes the read robust against a hand-edited file: a non-dict `plugins` value or a non-list record value currently makes `installed[p]` raise `TypeError`/`KeyError`-class errors at lines 327-329 (`for e in installed[p]`). With the guard they are treated as "not installed". This is a free side effect of writing the filter, not an extra feature.

### Change (`install_user_setup.py` line 317, edit 2)

Replace

```python
    installed = _read_json(plugins_dir / "installed_plugins.json").get("plugins", {})
```

with

```python
    records = _read_json(plugins_dir / "installed_plugins.json").get("plugins", {})
    records = records if isinstance(records, dict) else {}
    # Only user-scope records count: this step installs and updates --scope user.
    installed = {
        p: [e for e in r if isinstance(e, dict) and e.get("scope", "user") == "user"]
        for p, r in records.items()
        if isinstance(r, list)
    }
    installed = {p: r for p, r in installed.items() if r}
```

One contiguous block. Lines 323-330 (stale) and 374 (`p not in installed`) stay as they are; the `isinstance(e, dict)` inside the stale set (line 329) becomes redundant but harmless, and leaving it keeps the diff to one block.

### Regression test (new, after `test_plugins_keep_ponytail_at_its_pin`)

Name: `test_plugins_judge_the_pin_by_the_user_scope_record`

Setup (two homes in one test, same pattern as `test_plugins_skip_dependents_of_a_failed_marketplace`):
1. Both: `home = _pinned_home(tmp_path / name, "1" * 40, PONYTAIL_SHA)` (registry is ours, catalog on disk equals the shipped catalog so `changed` is False), `monkeypatch.setattr(setup.shutil, "which", ...)`, `_recording_run(calls)`.
2. Home `mixed`: overwrite `installed_plugins.json` with `{"plugins": {"ponytail@ironclaude": [{"scope": "user", "gitCommitSha": "1" * 40}, {"scope": "project", "projectPath": "/work/app", "gitCommitSha": PONYTAIL_SHA}]}}`.
3. Home `project_only`: `installed_plugins.json` holds only the project record at `PONYTAIL_SHA`.

Assertions:
- `mixed`: `calls == [["plugin", "marketplace", "update", "ironclaude"], ["plugin", "update", "ponytail@ironclaude", "--scope", "user"]]` (the marketplace update is queued because `stale` is non-empty, line 355).
- `project_only`: `["plugin", "install", "ponytail@ironclaude", "--scope", "user", "-y"] in calls` and no `plugin update` call.

Why it fails on current code: for `mixed`, `PONYTAIL_SHA` is in the all-scopes sha set, so `stale` is empty, no command is built, and `install_plugins` returns `"✅ Plugins: already installed"`; the `calls == [...]` assertion fails. For `project_only`, `p in installed` is true, so no install is queued; the `in calls` assertion fails.

## Finding 3: `CLAUDE_CONFIG_DIR` mismatch between validation and `claude` subprocesses

### The deciding fact

Everything `install_plugins` validates, and everything that decides what it does, lives under `home/.claude`:
- the wanted list: `settings = _read_json(home / ".claude" / "settings.json")` (line 311);
- the registry and the installed records: `plugins_dir = home / ".claude" / "plugins"` (line 315; reads at 316-317);
- the catalog it writes and registers: `home / _CATALOG_DIR` (lines 276, 292, 349, 352; `_CATALOG_DIR` is `.claude/ironclaude-marketplace`, line 47).

`apply_settings_defaults` is the step that writes `enabledPlugins` into that settings file, and it writes `home / ".claude" / "settings.json"` (line 163), ignoring `CLAUDE_CONFIG_DIR`. The same is true of every other step (`Path.home()` at lines 111, 143, 156, 234, 303). The only code in `src/` that reads `CLAUDE_CONFIG_DIR` is `read_user_mcp_servers` (`install_mcp.py:721-726`), and it reads, never writes. The mismatch is therefore a single leak: the subprocesses inherit an environment variable that no installer step honours (`subprocess.run(..., env=...)` at lines 392-401).

### Options

| | A. Honour `CLAUDE_CONFIG_DIR` for plugin state, subprocesses inherit | B. Refuse pinned plugins when `CLAUDE_CONFIG_DIR` differs from `home/.claude` | C. Pin every `claude` subprocess: drop `CLAUDE_CONFIG_DIR`, set `HOME=home` |
|---|---|---|---|
| What validation sees vs what commands touch | Same profile, but the profile differs from where `apply_settings_defaults` wrote `enabledPlugins` | Same profile (nothing runs on mismatch) | Same profile: `home/.claude`, the one every other step writes |
| Coherence with the wanted list (line 311) | Broken unless line 311 also moves; then `wanted` is read from a `settings.json` the installer never populated (it is empty of `enabledPlugins` defaults, so nothing is wanted) | Intact | Intact |
| Edits in `install_user_setup.py` | At least 4 blocks: new resolver, lines 311, 315, and every `_CATALOG_DIR` use if the catalog moves (276, 292, 349, 352) | 2 to 3: resolver plus gate before line 335; and it must cover non-pinned plugins too, because `installed` (line 317) would still describe the wrong profile for them | 1 block (line 392) |
| New semantics to decide | Empty string (CLI treats `""` as unset, per the seed's real-CLI proof; the only existing resolver, `install_mcp.py:722-723`, treats it as "unknown"), `~`, relative paths, symlinks | The same set, because a comparison needs the same resolver | None: the variable is removed, so its value is irrelevant |
| Outcome for a `CLAUDE_CONFIG_DIR` user | Plugins land in the profile they run, but their opt-outs and defaults come from `~/.claude`, and nothing else was installed there | Pinned Ponytail never installs for them (and, to be correct, no plugin does) | Plugins land in `~/.claude`, exactly like rules, output styles, settings defaults, skills |
| Test cost | Every plugin test needs `monkeypatch.delenv` or it depends on the developer's shell | A new test per resolver edge case | One test; 1 assertion update |
| Production behaviour change when `CLAUDE_CONFIG_DIR` is unset | Resolver path executes | None | None: `HOME` equals `Path.home()` (POSIX `Path.home()` is `expanduser("~")`, which reads `$HOME`); only the unset or differing cases change |

### Decision: **C**

Rationale:
1. **It is the only option that matches what the installer already does.** A needs the plugin step alone to honour a variable the other five steps ignore, which makes the profile the plugin lands in different from the profile whose `settings.json` says which plugins are wanted. B turns the feature off for exactly the users who set the variable.
2. **It is one edit and removes the question.** With the variable gone, empty, `~`-prefixed, relative and symlinked values all stop mattering. A and B each need a resolver whose edge cases are the open bugs of the next review round.
3. **It makes the invariant true by construction.** "Validation read `home/.claude`, so the commands act on `home/.claude`" holds for every command, pinned or not, rather than only the pinned ones B would gate.
4. **Evidence that `HOME` pins the profile once the variable is absent.** The seed's real-CLI proof shows that with `CLAUDE_CONFIG_DIR=""` the CLI behaves as unset and reads `$HOME/.claude/plugins` and writes `$HOME/.claude.json`, under a throwaway `HOME`. Removing the variable is the same state as that observation. I did not run `claude` (forbidden); a pre-merge throwaway-`HOME` check with the variable unset is listed under Risks.

Rejected: A because it is incoherent with line 311 and the rest of the installer; B because it disables the feature instead of fixing it and still leaves non-pinned plugins pointing at an unvalidated profile.

### Answer to Open Question 2 (catalog directory location)

Stay at `home/.claude/ironclaude-marketplace` (`_CATALOG_DIR`, line 47). Under C the profile never moves, so there is nothing to follow. The catalog is registered by absolute path (line 352), so its location does not affect correctness either way.

### Change (`install_user_setup.py` line 392, edit 3)

Replace

```python
        env = {**os.environ, **_HTTPS_GITHUB} if args[1] == "update" else None
```

with

```python
        # Act on the profile this run validated, never one CLAUDE_CONFIG_DIR names.
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
        env["HOME"] = str(home)
        if args[1] == "update":
            env.update(_HTTPS_GITHUB)
```

`args[1] == "update"` keeps its current meaning: it matches `plugin update` only, so `plugin marketplace update` still does not get `_HTTPS_GITHUB` (existing behaviour, pinned by `assert calls[0][1] is None` at test line 397, which becomes the updated assertion below). `os` is already imported (line 24).

### Regression test (new, after `test_plugins_move_ponytail_to_a_new_pin`)

Name: `test_plugins_pin_claude_commands_to_the_validated_home`

Setup:
1. `old = "16352ac229eb08a9598dcae48fe9f2b342567d86"`; `home = _pinned_home(tmp_path, installed_sha=old, catalog_sha=old)` (same fixture as the move-pin test: yields a marketplace update and a plugin update).
2. `monkeypatch.setenv("SENTINEL", "kept")`.
3. For each `profile` in `(str(tmp_path / "other-profile"), "")`: `monkeypatch.setenv("CLAUDE_CONFIG_DIR", profile)`, then run with a fake `subprocess.run` that appends `(command[1:], kwargs.get("env"))` to a list.

Assertions, for every recorded call in both iterations:
- `env is not None` and `"CLAUDE_CONFIG_DIR" not in env`
- `env["HOME"] == str(home)`
- `env["SENTINEL"] == "kept"` (the rest of the environment is preserved)
- at least two calls were recorded (so the loop is not vacuous)

Why it fails on current code: for `marketplace update`, `env` is `None` (line 392), so `env is not None` fails; for `plugin update` the env is `{**os.environ, **_HTTPS_GITHUB}`, which still contains `CLAUDE_CONFIG_DIR` and the developer's `HOME`.

## Convergence point and edit count

There are two convergence points, one per kind of state, and neither needs a new abstraction.

1. **Plugin-state root: the `home` parameter of `install_plugins` (line 303).** Every path the step reads or writes derives from it: settings (line 311), `plugins_dir` (line 315), the catalog (`home / _CATALOG_DIR`, lines 276, 292, 349, 352). Option C leaves all of these as they are, so "fix the plugin-state paths once where they converge" is satisfied by not moving them: the paths already converge on `home`, and the bug was that the subprocesses did not.
2. **Process boundary: the one `subprocess.run` call inside the command loop (lines 394-401).** Every `claude` command the step runs goes through it, and its `env` is built on the single line 392. The fix goes there. `shutil.which("claude")` (line 304) is a lookup, not a profile access.

Exact changes in `src/superclaude/cli/install_user_setup.py` (edit = one block of consecutive changed lines):

| # | Function | Original lines | Change |
|---|---|---|---|
| 1 | `_is_our_catalog` | 292 | one line becomes a 4-line `try`/`except` returning `False` on `(OSError, RuntimeError, ValueError)` |
| 2 | `install_plugins` | 317 | one line becomes an 8-line read-and-filter to user-scope records |
| 3 | `install_plugins` | 392 | one line becomes 5 lines: env without `CLAUDE_CONFIG_DIR`, `HOME=str(home)`, `_HTTPS_GITHUB` only for `plugin update` |

**Total: 3 edits** in `install_user_setup.py` (limit for a direct change: 5). Lines 323-330, 343, 374 and 383-414 are not edited; findings 1 and 2 reach them through their data. No new imports, constants, helpers or dependencies. Run: `uv run pytest tests/cli/test_install_user_setup.py -v`.

## Existing test impact

All in `tests/cli/test_install_user_setup.py`. Grep of `tests/` shows no other file calls `install_plugins` for real; `tests/cli/test_update_command.py:45` replaces it with a fake, so it is unaffected.

| Test | Lines | Needs change? | Change |
|---|---|---|---|
| `test_plugins_move_ponytail_to_a_new_pin` | 378-398 | **Yes** | Line 397 `assert calls[0][1] is None` fails (the marketplace-update env is now a dict). Replace with `assert "CLAUDE_CONFIG_DIR" not in calls[0][1]`, `assert calls[0][1]["HOME"] == str(home)` and `assert "GIT_CONFIG_COUNT" not in calls[0][1]` (keeps pinning that only `plugin update` gets the HTTPS settings). Line 398 (`calls[1][1]["GIT_CONFIG_VALUE_0"] == "git@github.com:"`) stays valid. |
| `test_plugins_skip_already_installed` | 537-551 | **Yes (fixture only)** | The fixture writes `"playwright@claude-plugins-official": []` (line 545), an empty record list that meant "installed" by key presence. After the filter an empty list is "not installed", so the fake `run` would be called and raise `AssertionError`. Change the fixture value to `[{"scope": "user"}]`. The assertion is unchanged. |
| `test_plugins_keep_ponytail_at_its_pin` | 401-407 | No | `_pinned_home` writes a `"scope": "user"` record (line 366). |
| `test_plugins_accept_ours_through_a_symlinked_home` | 449-462 | No | Uses `_pinned_home`; resolution for the real home still runs and still matches. |
| `test_plugins_refuse_a_foreign_ironclaude_marketplace` | 421-446 | No | Every entry is rejected before `resolve()` or resolves to a different path; `_recording_run` ignores `env`. |
| `test_plugins_install_missing_enabled_defaults`, `test_plugins_skip_dependents_of_a_failed_marketplace`, `test_plugins_catalog_write_failure_is_not_fatal`, `test_plugin_failures_and_time_limit_never_fail_install`, `test_plugins_skip_when_claude_cli_is_absent` | 317-355, 465-518, 521-534, 554-572, 575-580 | No | Fake `run` functions take `**kwargs`/`**_kwargs` or `**k` and never assert `env`; none writes an `installed_plugins.json` with an empty list. |

New tests: 3 (one per finding), named above.

## Risks and edge cases

| Case | Behaviour after the fix | Notes |
|---|---|---|
| **Empty `CLAUDE_CONFIG_DIR`** | Removed from the env like any other value. The CLI already treated `""` as unset (seed's real-CLI proof), so nothing changes for the CLI. | The regression test covers `""`. Note this differs from `read_user_mcp_servers`, which treats `""` as "unknown" (`install_mcp.py:722-723`); that function is out of scope and is not touched. |
| **`~` in `CLAUDE_CONFIG_DIR`** | Irrelevant: the variable is dropped before use, so `expanduser` is never called and its `RuntimeError` for an unknown `~user` cannot occur here (probed: `Path("~nosuchuserxyz").expanduser()` raises `RuntimeError` on 3.11.15 and 3.13.5). | This is a gain of option C over A and B, both of which would have to call `expanduser` and guard it. |
| **Symlinked `home`** | `HOME` is `str(home)` unresolved, so the CLI writes through the symlink to the real directory. `_is_our_catalog` still resolves both sides, so `test_plugins_accept_ours_through_a_symlinked_home` (lines 449-462) keeps matching. | The registered path is the unresolved `str(home / _CATALOG_DIR)` (line 352); resolution at compare time is what makes either spelling match. |
| **Project-scope-only record** | Not installed: the step queues `plugin install ... --scope user -y`. If the same plugin is also installed in a project, both copies then exist; the project copy is never touched. | Decision for the open question; see Finding 2. |
| **Project record at the pin plus user record off the pin** | `stale` is non-empty: queues `marketplace update ironclaude` then `plugin update ponytail@ironclaude --scope user`. | The success criterion of the seed brief. |
| **Record without a `scope` key** | Counted as user scope. | Keeps today's behaviour for any record shape that predates the `scope` field. If a future CLI writes another scope name, it is ignored (treated as not user). |
| **Empty record list for a plugin** | Now "not installed". Before: "installed" by key presence. | Only a hand-made fixture wrote this (test line 545). Whether the real CLI ever leaves `[]` after an uninstall is UNVERIFIED. If it does, the step would run an install that either succeeds or is reported as a normal failure, never fatal. |
| **Python 3.13 and `resolve()`** | Loop: no exception at all (probed 3.13.5: returns the unresolved path), so the comparison is simply `False` and the existing refusal fires. NUL: `ValueError` on 3.11.15 and 3.13.5. Python 3.10 to 3.12: loop is `RuntimeError`. | The seed brief's "`OSError` on 3.13+" is not what 3.13.5 does. Keeping `OSError` in the tuple is defensive, not evidenced. This is why the regression test uses a NUL path. |
| **`HOME` unset in the parent** | `Path.home()` falls back to the user database, and `home` is that path; the subprocess now gets `HOME` set to it. | Harmless: the CLI needs a home anyway. |
| **Relative `home`** | `HOME` would be relative. | Production passes `Path.home()` (absolute); tests pass `tmp_path`. No code path passes a relative `home`; not guarded, to stay minimal. |
| **Windows** | `HOME` does not pin the profile there (`USERPROFILE` does). | UNVERIFIED whether this installer step runs on Windows at all; the step already assumes `/` paths and POSIX `git@github.com:` rewrites. Not addressed. |
| **Auth stored under the user's `CLAUDE_CONFIG_DIR`** | The subprocess no longer sees it. | UNVERIFIED whether `marketplace add` / `plugin install` / `plugin update` for public GitHub or local directory sources need a login; the seed's proof ran all three against a throwaway profile. Mitigation if it matters: failures are reported, never fatal (lines 403-408, 409-413). |
| **User who runs `claude` with `CLAUDE_CONFIG_DIR`** | Plugins are installed into `~/.claude`, not the profile they run. The success line still says "installed". | Same situation as rules, output styles, settings defaults, skills and agents today, so the installer stays consistent. A user-visible note would be new behaviour. |

Pre-merge manual check (not run here; it would execute `claude`): in a throwaway `HOME` with `CLAUDE_CONFIG_DIR` set to a second directory, run `install_plugins(home=<throwaway>)` and confirm nothing is written under the second directory. This confirms point 4 of the finding-3 rationale.

## Out of scope

- Moving or honouring `CLAUDE_CONFIG_DIR` in any other installer step (`install_rules`, `install_output_styles`, `apply_settings_defaults`, `install_orca_skills`, commands, skills, agents, hooks).
- Aligning `read_user_mcp_servers` (`install_mcp.py:709-741`) with the CLI's "empty means unset" behaviour.
- A distinct refusal message for an unresolvable registration (needs a tri-state return).
- Giving `plugin marketplace update` the `_HTTPS_GITHUB` settings. The existing test pins that it does not get them; whether it should is a separate question.
- Hardening the other reads in `install_plugins` against hand-edited JSON (for example `known[name]` shape, `defaults` shape). Only the `installed_plugins.json` read is touched, because finding 2 rewrites it.
- Setting `USERPROFILE` for Windows.
- A user-visible warning when `CLAUDE_CONFIG_DIR` is set.
- Any change to the catalog location, `_CATALOG_DIR`, `_write_catalog`, or `user_settings_defaults.json`.
- Docs changes; none of the three fixes alters a documented flag or command.
