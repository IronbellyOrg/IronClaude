# Codebase Context: pr360-followups

quality_tier: fallback_1 (the auggie codebase-retrieval tool is not available in this session; the native floor ran: full Read of src/superclaude/cli/install_user_setup.py and tests/cli/test_install_user_setup.py lines 280-588, Grep across src/ and tests/ for CLAUDE_CONFIG_DIR and the plugin helpers)

## install_user_setup.py (master 605da2ff, 427 lines)

- `_CATALOG_DIR = Path(".claude") / "ironclaude-marketplace"` (line 47); used as `home / _CATALOG_DIR` by `_write_catalog` (276), `_is_our_catalog` (292) and the refusal hint and `marketplace add` argument (349, 352).
- `_is_our_catalog(entry, home)` (284-292): directory source with an absolute path, then `Path(path).resolve() == (home / _CATALOG_DIR).resolve()`. Non-strict `resolve()` raises `RuntimeError` (Python < 3.13) or `OSError` (3.13+, ELOOP) on a symlink loop. Called once, at 343, outside any try block.
- `install_plugins(home, deadline)` (295-414):
  - `settings = _read_json(home / ".claude" / "settings.json")` (311) supplies `wanted`.
  - `plugins_dir = home / ".claude" / "plugins"` (315); `known` (316) and `installed` (317) read from it.
  - `stale` (323-330): pinned sha not in the set of `gitCommitSha` across ALL records of the plugin, any scope.
  - `p not in installed` (374): any record, any scope, suppresses `plugin install --scope user`.
  - Subprocess env (392): `None` (inherit) except for `plugin update`, which gets `{**os.environ, **_HTTPS_GITHUB}`; both inherit `CLAUDE_CONFIG_DIR`.
- `install_user_setup` (417-427) calls every step with no `home`, so production `home = Path.home()`.

## Other CLAUDE_CONFIG_DIR handling

- src/superclaude/cli/install_mcp.py:721 `read_user_mcp_servers`: empty string = unknown; else `Path(config_dir).expanduser()`; else `Path.home()`; reads `<root>/.claude.json`.
- No other installer step honours CLAUDE_CONFIG_DIR; rules, output styles, settings defaults, hooks, commands, skills, agents all write under `~/.claude`.
- tests/cli/test_update_command.py:40 sets `CLAUDE_CONFIG_DIR=home/config` and replaces `install_plugins` with a fake, so it does not exercise plugin paths.

## Test seams

- `_plugin_home(tmp_path, enabled)` writes `<tmp>/.claude/settings.json`; `_pinned_home(tmp, installed_sha, catalog_sha)` adds a user-scope record, an `ironclaude` registry entry pointing at `home/_CATALOG_DIR`, and the catalog file.
- `test_plugins_move_ponytail_to_a_new_pin` asserts `calls[0][1] is None` (marketplace update env) and `calls[1][1]["GIT_CONFIG_VALUE_0"]`; any env change for all subprocesses must update that assertion.
- `test_plugins_accept_ours_through_a_symlinked_home` pins that a symlinked home still matches (so resolution must stay).
