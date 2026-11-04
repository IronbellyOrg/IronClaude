---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-closeIronbellyOr-20261104-124207
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Install the Ponytail plugin on every workspace, always-on mode lite (issue #330)

Source: ./source.md
Goal: `superclaude install`, `superclaude update` and `update.sh` install and enable `ponytail@ponytail` (marketplace `DietrichGebert/ponytail`) on every workspace with `env.PONYTAIL_DEFAULT_MODE=lite` filled only when the user has not set it, every plugin install failure is reported by name, and the installation guide and CHANGELOG describe what lite does, the ledger (on), how to change the mode and how to opt out.

Design reference: `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md` (FR-001..FR-008, NFR-001..NFR-006, Design 3.1 and 3.2, Tests T1..T6, Docs and CHANGELOG). Two final decisions override it wherever it differs: the shipped mode is `lite` (not `off`), and the ledger is Ponytail's own default (on, outcome 2 of 3.1a, no `pluginConfigs` entry).

Lite behaviour, read from upstream Ponytail v5.3.3 (main `96608e07`) for the docs tasks:
- SessionStart (`hooks/ponytail-activate.js:53-71,169-174`): writes the mode flag `~/.claude/.ponytail-active` plus a per-project copy under `~/.claude/ponytail-modes/` (`hooks/ponytail-runtime.js:51-66`), injects the Ponytail ruleset filtered to the lite level (`skills/ponytail/SKILL.md:50`: "Build what was asked. Name the smaller option in one line and let the user pick."), and appends a codebase map (3 s cap; `PONYTAIL_MAP=0` turns it off).
- Statusline nudge (`hooks/ponytail-activate.js:73-164`): lite emits it. When `settings.statusLine` is unset and `~/.claude/.ponytail-statusline-nudged` does not exist, the hook copies `ponytail-statusline.sh` into `~/.claude`, writes that flag file and adds "STATUSLINE SETUP NEEDED ... Proactively offer to set this up for the user on first interaction." to the session context. It fires once per `~/.claude`: whichever session starts first on the workspace, an unattended Orca worker included, gets it. Any existing flag file (even empty) suppresses it.
- SubagentStart (`hooks/ponytail-subagent.js:17-49`): injects the same ruleset into every subagent while the mode is not off; `PONYTAIL_SUBAGENT_MATCHER` (a case-insensitive regex on the agent type) limits which ones.
- Mode resolution (`hooks/ponytail-config.js:80-105`): env `PONYTAIL_DEFAULT_MODE`, then `defaultMode` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`), then `full`. Valid values: `off`, `lite`, `full`, `ultra`. So `/ponytail default <mode>` has no effect while the env key is set.
- The band module and ledger run in every mode (brainstorm Interaction table, upstream `band/register.tsx`); the ledger `userConfig` option defaults to `true` (upstream `.claude-plugin/plugin.json`).

## Constraints

- Change only `src/superclaude/cli/user_settings_defaults.json`, `src/superclaude/cli/install_user_setup.py` (at most 5 changed lines, failure label only), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md` and `CHANGELOG.md`. No change to `main.py`, `update.sh`, `doctor.py`, output styles, rules, hooks, any skill, command or agent, or any `.claude/` file.
- Never run `superclaude install`, `superclaude update`, `./update.sh` or `claude plugin ...` against this workspace's `~/.claude`; any manual proof uses a throwaway `HOME` under `/tmp` that is removed afterwards.
- No `pluginConfigs` entry, no `statusLine` setting, no write outside `~/.claude`, no version pin, no new module, constant, flag or CLI option.
- A user's existing `enabledPlugins`, `env` and marketplace values are never changed.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); never stage `.claude/` paths.
- The superseded package `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/` and `.dev/reflect/pre-closeIronbellyOr-20261104084538/` stay on disk untouched.

## Phase 1: Ship Ponytail in the settings defaults

## Task 1: Add the three Ponytail entries to the defaults file and pin them with tests

Edit `src/superclaude/cli/user_settings_defaults.json` (FR-001..FR-003, Design 3.1): append `"ponytail@ponytail": true` to `enabledPlugins` after `understand-anything@understand-anything`; append `"ponytail": {"source": {"source": "github", "repo": "DietrichGebert/ponytail"}}` to `extraKnownMarketplaces`; append `"PONYTAIL_DEFAULT_MODE": "lite"` to `env`. No other key changes. `apply_settings_defaults` (`install_user_setup.py:150-164`, `_NESTED_KEYS` at `:36`) already fills these entry by entry, and `install_plugins` (`:251-311`) already installs every enabled default, so no Python change is needed for this.

In `tests/cli/test_install_user_setup.py`:
- T1: new `test_defaults_ship_ponytail` loads the defaults file and asserts `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"] == {"source": "github", "repo": "DietrichGebert/ponytail"}`, `env["PONYTAIL_DEFAULT_MODE"] == "lite"`, and that every `enabledPlugins` key's marketplace (text after `@`) has a `source.repo` in `extraKnownMarketplaces`. It must not assert key order and must assert no `pluginConfigs` key.
- T2: extend `test_plugins_install_missing_enabled_defaults` (`:182-209`) with `["plugin", "marketplace", "add", "DietrichGebert/ponytail"] in calls` and `"ponytail@ponytail" in installs`.
- T3/T4: extend `test_settings_defaults_fill_only_missing_values` (`:73-98`) or add a sibling test with two legs. Leg 1 (existing user): settings hold the old six plugins and the two old marketplaces; after `apply_settings_defaults`, `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]` is present, `env["PONYTAIL_DEFAULT_MODE"] == "lite"`, the existing values are unchanged, and a second run returns `(True, "✅ Settings defaults: already present")`. Leg 2 (user choice kept): with `enabledPlugins["ponytail@ponytail"] = False` and `env["PONYTAIL_DEFAULT_MODE"] = "full"` in settings, both values are unchanged after apply.

Acceptance criteria:
- `user_settings_defaults.json` is valid JSON and differs from master only by the three added entries (`git diff` shows three added lines plus the needed commas/braces).
- T1, T2 and both T3/T4 legs pass under `uv run pytest tests/cli/test_install_user_setup.py -v`; T1 fails if `PONYTAIL_DEFAULT_MODE` is anything other than `lite` or if the ponytail marketplace entry is removed.
- `test_plugins_skip_already_installed` (T6) passes unchanged.

## Phase 2: Name every failed plugin install

## Task 2: Report plugin install failures by plugin id or marketplace repo

Depends on: Task 1

Fix the shared failure label in `install_plugins` in `src/superclaude/cli/install_user_setup.py` (FR-005, Design 3.2). Today an install command is `["plugin", "install", p, "--scope", "user", "-y"]`, so `args[3]` is `"--scope"`: the non-zero-exit and exception paths (`:303`, `:305`) append `--scope`, and the time-limit path (`:292`) builds `install <p> --scope (time limit)`. Compute one name per command (the repo for a `marketplace add`, `args[3]`; the plugin id for an `install`, `args[2]`) and use it in all three places, the time-limit one as `f"{name} (time limit)"`. At most 5 changed lines; `ok` stays `True` on every path; no other change to the function.

In `tests/cli/test_install_user_setup.py`:
- T5: extend `test_plugin_failures_and_time_limit_never_fail_install` (`:229-242`, its `playwright`-only fixture). Non-zero-exit leg: `ok is True`, message contains `anthropics/claude-plugins-official` and `playwright@claude-plugins-official`, and `"--scope" not in message`. `deadline=0` leg: `ok is True`, message contains `(time limit)` and the same two names, and `"--scope" not in message`.
- T5c: new test that monkeypatches `setup.shutil.which` to return `None` and asserts `setup.install_plugins(home=tmp_path) == (True, "⏭️  Plugins: claude CLI not found; skipped")` (two spaces after the emoji, as at `install_user_setup.py:258`).

Acceptance criteria:
- `git diff src/superclaude/cli/install_user_setup.py` changes at most 5 lines, all inside `install_plugins`.
- A failed plugin install is reported as e.g. `⚠️  Plugins: not installed: DietrichGebert/ponytail, ponytail@ponytail; rerun ...` (never `--scope`); T5 fails on the unfixed code and passes after the fix.
- T5c passes.
- `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/unit/test_cli_install.py -v` passes, `make lint` is clean and `uv run ruff format --check src/ tests/` reports no change; output saved to `./artifacts/t2-tests.log`.

## Phase 3: Document Ponytail in the installation guide

## Task 3: Rewrite the default-plugin paragraph and add the Ponytail lite section in `docs/getting-started/installation.md`

Depends on: Task 2

At `docs/getting-started/installation.md:353-360`, replace "(six plugins, including `playwright` and `frontend-design`)" with a count-free list "(including `playwright`, `frontend-design` and `ponytail`)", keeping the budget and retry sentences. Then add a Ponytail block after that paragraph (before the `CLAUDE_CONFIG_DIR` note) that states, in plain English and from the lite facts at the top of this plan:
- What it adds: the `ponytail-*` skills and the `/ponytail` command, from `DietrichGebert/ponytail`; installed with its always-on mode `lite`: the installer sets `env.PONYTAIL_DEFAULT_MODE` to `lite` unless you already set it.
- What lite does: every session start injects Ponytail's ruleset at the lite level (quote the lite row) and a short codebase map (`PONYTAIL_MAP=0` turns the map off); every subagent gets the same ruleset (`PONYTAIL_SUBAGENT_MATCHER` limits which); the mode is recorded in `~/.claude/.ponytail-active`.
- The statusline note: on a workspace whose settings have no `statusLine`, the first session (an unattended Orca worker included) gets a one-time note asking Claude to offer to set up Ponytail's statusline badge; Ponytail copies `ponytail-statusline.sh` into `~/.claude` and records the note in `~/.claude/.ponytail-statusline-nudged`, so it never repeats; the installer never sets `statusLine`. An Orca worker may mention that offer in its reply; it changes no settings by itself.
- The band module (from the brainstorm's band text, valid in every mode): band above the prompt, `git grep` at session start, a watch on every Edit and Write, and a local per-turn ledger row in `$XDG_CONFIG_HOME/ponytail/band/<project>.csv` (or `~/.config/ponytail/band/<project>.csv`); webhook empty by default; `/ponytail band off` hides the band only. The ledger is on by default; set Ponytail's `ledger` option to `false` to stop it.
- Changing the mode: `/ponytail off|lite|full|ultra` switches every session in that repo until a new session starts there (a new session starts at the default again); bare `/ponytail` switches to `full` (brainstorm Opt-out item 2, upstream `ponytail-mode-tracker.js`); to change the default, set `env.PONYTAIL_DEFAULT_MODE` in `~/.claude/settings.json` to `off`, `lite`, `full` or `ultra`. That variable overrides `/ponytail default <mode>`, which prints "PONYTAIL DEFAULT SET" but has no effect while it is set.
- Opt-out: set `"ponytail@ponytail": false` in `enabledPlugins` in `~/.claude/settings.json`; do not delete the key (the next install adds it back as `true`) and do not only run `claude plugin uninstall` (the next install reinstalls it); a project `.claude/settings.json` that enables it wins over the user value.
- Existing workspaces get Ponytail only after the IronClaude package itself is upgraded (for a checkout, `git pull` before `./update.sh`), then `superclaude update` or `superclaude install`.
- Its hooks need `node` on the PATH; IronClaude's own SubagentStart hook already needs it.
- The Known Limitation sentence from the brainstorm, verbatim: "On a workspace where Orca's skill install uses the shared 30 s network budget on every run, the installer may not reach the Ponytail install. Such a workspace gets Ponytail on a later run that leaves budget, or through Claude Code's own background install of enabled plugins (UNVERIFIED)."

Acceptance criteria:
- `grep -rn "six plugins" docs/` prints nothing.
- The Ponytail block names `lite` as the shipped default and contains no sentence saying the shipped default is `off`, injects nothing, or that the ledger ships off.
- The block names `PONYTAIL_MAP=0`, `PONYTAIL_SUBAGENT_MATCHER`, `.ponytail-statusline-nudged`, the four modes, the `ledger` option set to `false`, and `"ponytail@ponytail": false`; every behaviour claim matches the lite facts at the top of this plan.
- No `src/superclaude/` path is added to the doc.

## Phase 4: Record the change in the CHANGELOG

## Task 4: Add the `[Unreleased]` entry for #330 to `CHANGELOG.md`

Depends on: Task 3

Under `## [Unreleased]` (`CHANGELOG.md:5`, empty today), add `### Ponytail plugin installed by default (#330)` with:
- `#### Added (default plugins)`: one bullet saying `superclaude install`, `superclaude update` and `update.sh` now install `ponytail@ponytail` from `DietrichGebert/ponytail` (verified against upstream v5.3.3) with `env.PONYTAIL_DEFAULT_MODE` set to `lite` when you have not set it; what lite does (ruleset at session start and in every subagent, codebase map, one-time statusline note on a workspace without `statusLine`, which an Orca worker may be the one to see); the band module and the ledger (on; Ponytail's `ledger` option set to `false` stops it); how to change the mode (`off`, `lite`, `full`, `ultra`); how to opt out (`"ponytail@ponytail": false`, do not delete the key); existing workspaces after a package upgrade; needs `node`; a link to the installation guide section.
- A second bullet: if you already use Ponytail with `defaultMode` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`), the new `PONYTAIL_DEFAULT_MODE=lite` wins over it and `/ponytail default <mode>` has no effect while the variable is set; set the env key to your preferred mode instead.
- `#### Fixed (plugin install report)`: "A plugin that fails to install is now listed by its name in the `Plugins: not installed` warning (it printed `--scope`)."

Also record the brainstorm's manual install proof (AC-M1 M1a/M1b/M1c, AC-M2, AC-M3; non-blocking) in `./artifacts/m1-install-proof.md`, run only in a throwaway `HOME` under `/tmp` (for example `HOME=$(mktemp -d /tmp/ponytail-home.XXXXXX)`), removed afterwards, never this workspace's `~/.claude`. M1a: after `superclaude install` in that HOME, `~/.claude/plugins/installed_plugins.json` lists `ponytail@ponytail`, `known_marketplaces.json` has the key `ponytail`, and a second run prints `✅ Plugins: already installed`. M1b (lite): a new session shows the Ponytail ruleset at level lite and `~/.claude/.ponytail-active` holds `lite`; counted only if M1c passed. M1c: the plugin's skill files exist under `~/.claude/plugins/`; if no Claude session can be started in that HOME, record M1b and M1c as UNVERIFIED. AC-M2: with `"ponytail@ponytail": false`, a rerun runs no Ponytail command and keeps `false`. AC-M3: with `claude` absent from `PATH`, exit 0 and the skip line.

Acceptance criteria:
- `./artifacts/m1-install-proof.md` exists and records each manual check as PASS, FAIL or UNVERIFIED with the commands run and their output; a FAIL or UNVERIFIED does not block, and the throwaway HOME is gone afterwards.
- `CHANGELOG.md` `[Unreleased]` holds exactly this new section, in the `### topic` / `#### Added (...)` / `#### Fixed (...)` style used under `[5.0.0]`, and no existing section changes.
- The entry says `lite` is the shipped default and the ledger is on; it never says the shipped default is `off`.
- `make verify-sync` passes and `git diff --stat master` lists only the five delivery files of this plan plus `.dev/` artifacts.
