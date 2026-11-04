# Codebase Context: ponytail-plugin-install

quality_tier: fallback_1 (auggie MCP is not available in this session; native Read/Grep used directly on the named files)

## Install and update entry points

| Path | Fact |
|---|---|
| `src/superclaude/cli/main.py:231-237` | `superclaude install` step 7 calls `install_user_setup(force=force)`. |
| `src/superclaude/cli/main.py:403-405` | `superclaude update` calls `install_user_setup(force=True)`: the plugin step already runs on update. |
| `update.sh:8,10` | `superclaude install --force`, then `superclaude doctor`. |
| `src/superclaude/cli/main.py:86-172` | `install --list` prints core, commands, agents, skills, templates, codegraph and retired MCP. No plugins. |
| `src/superclaude/cli/doctor.py` | No plugin check (only "pytest plugin loaded"). |

## User setup and plugins (`src/superclaude/cli/install_user_setup.py`)

| Lines | Fact |
|---|---|
| 31-36 | `_NETWORK_BUDGET = 30` s shared by Orca skills and plugins; `_NESTED_KEYS` includes `env`, `enabledPlugins`, `extraKnownMarketplaces`. |
| 137-172 | `apply_settings_defaults`: fills each nested entry the user lacks; never overwrites; backs up settings.json. An existing user gets new `enabledPlugins` entries on the next install or update. |
| 251-311 | `install_plugins`: no `claude` CLI -> skip line; wanted = defaults whose settings value `is True`; adds a marketplace only when absent from `known_marketplaces.json` and the defaults give `source.repo`; installs with `claude plugin install <p> --scope user -y`; skips installed; per-command time limit from the shared deadline; any failure -> `⚠️ Plugins: not installed: ...; rerun superclaude install`, still `ok=True`. |
| 314-324 | `install_user_setup` order: rules, output styles, settings defaults, Orca skills, plugins. |

## Defaults (`src/superclaude/cli/user_settings_defaults.json`)

`enabledPlugins` (lines 28-35): frontend-design, playwright, notion, dropbox, google-cloud-storage (all `@claude-plugins-official`), `understand-anything@understand-anything`. `extraKnownMarketplaces` (36-49): `claude-plugins-official` -> `anthropics/claude-plugins-official`; `understand-anything` -> `Lum1104/Understand-Anything`. `env` (10-13): two Claude Code variables. `outputStyle: "Pragmatic"`.

## Tests touching these files

- `tests/cli/test_install_user_setup.py:75-93` (defaults never overwrite user plugin values), `:175-241` (plugin install from defaults, skip installed, failures and time limit never fatal).
- `tests/cli/test_update_command.py:42-45` stubs `install_plugins`.
- `tests/unit/test_cli_install.py` (packaging; not plugin-list specific).

## Docs

- `docs/getting-started/installation.md:353-360`: "six plugins, including playwright and frontend-design", opt-out by disabling in `enabledPlugins`, 30 s shared budget, non-fatal.
- `CHANGELOG.md:5` empty `## [Unreleased]`.

## Overlap with IronClaude behaviour

- `src/superclaude/output-styles/pragmatic.md:136-160` "The ladder" (ponytail-derived wording: "The best code is the code that does not need to exist").
- `.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md:208-224`: `/sc:implement` embeds the fix-cost lens and never invokes `ponytail-review`.
- The installer never sets `statusLine` (grep of `src/superclaude/cli/*.py`), so a new workspace has none and Ponytail's one-time statusline nudge would fire in a non-off mode.
