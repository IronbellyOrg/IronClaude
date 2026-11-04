---
topic: "Close IronbellyOrg/IronClaude issue #330: ensure the Ponytail Claude Code plugin is installed on every workspace by the installer and update scripts"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-04T06:40:00Z
---

# Seed Brief: ponytail-plugin-install

## Problem Statement

Issue #330 ("Ensure Ponytail is installed/added as a plugin on all workspaces"; problem: "Valuable skill missing"; proposed solution: "Ensure the installer and update scripts always install this from plugin") asks that every IronClaude workspace gets the Ponytail Claude Code plugin from `superclaude install`, `superclaude update` and `update.sh`. Today the default plugin list has 6 plugins from 2 marketplaces and Ponytail is not one of them, so new and existing workspaces lack the `ponytail-*` skills. Ponytail is not a passive skill pack: when enabled it runs SessionStart, SubagentStart and UserPromptSubmit hooks that inject an always-on ruleset, which overlaps IronClaude's own Pragmatic output style.

## Known Context

Verified this session (sources cited; full detail in `enrichment/codebase-context.md`):

- Plugin identity: marketplace `ponytail` (`DietrichGebert/ponytail/.claude-plugin/marketplace.json`, plugin `ponytail`, source `./`), so the id is `ponytail@ponytail`; `plugin.json` version 5.3.3, MIT, last release v5.3.3 on 2026-10-29.
- Ponytail's Claude hooks (`hooks/claude-codex-hooks.json`): SessionStart (`startup|resume|clear|compact`), SubagentStart and UserPromptSubmit, each `node -e ...`, timeout 15 s. `hooks/claude-band.json` registers a band module `./band/register.tsx`. `userConfig.ledger` defaults true (writes a per-turn row to `~/.config/ponytail/band/<project>.csv`); webhook empty by default (nothing leaves the machine).
- Mode resolution (`hooks/ponytail-config.js`): `PONYTAIL_DEFAULT_MODE` env, then `~/.config/ponytail/config.json` `defaultMode`, then `full`. Modes: `off|lite|full|ultra`. In `off` the SessionStart hook exits before writing the flag or emitting rules (`hooks/ponytail-activate.js` `activate`). In other modes it emits the ruleset, a codebase map (3 s cap) and, once, a statusline-setup nudge telling Claude to "Proactively offer to fix this for the user on first interaction" when `settings.statusLine` is unset.
- IronClaude installer: `install_user_setup()` (`src/superclaude/cli/install_user_setup.py:314-324`) runs rules, output styles, `apply_settings_defaults`, Orca skills, `install_plugins`. `apply_settings_defaults` fills nested `enabledPlugins`/`extraKnownMarketplaces`/`env` entries one by one, never overwriting a user value (`:137-172`). `install_plugins` (`:251-311`) installs only defaults whose user value `is True`, adds missing marketplaces from `extraKnownMarketplaces[market].source.repo`, skips installed plugins, shares a 30 s budget with Orca, and never fails the step; missing `claude` CLI prints a skip line.
- `superclaude update` already calls `install_user_setup(force=True)` (`src/superclaude/cli/main.py:403-405`); `update.sh` runs `superclaude install --force`. So both update paths already run the plugin step.
- Neither `superclaude install --list` (`main.py:86-172`) nor `superclaude doctor` (`doctor.py`) reports plugins today.
- Pragmatic output style (`src/superclaude/output-styles/pragmatic.md:136-160`, "The ladder") already carries a ponytail-style ladder. Design note `.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md:208-224`: `/sc:implement` never invokes ponytail-review and must not depend on it.
- Docs: `docs/getting-started/installation.md:353-360` says "six plugins". Tests: `tests/cli/test_install_user_setup.py:175-241` cover plugin install from the defaults file.

## Constraints

- Scope is #330 only: Ponytail on every workspace via install and update. No new plugin framework.
- Never run `superclaude install/update` or `./update.sh` against this workspace's `~/.claude`; prove behaviour with unit tests and, if needed, a throwaway HOME under /tmp.
- A user's own `enabledPlugins` choice (including `false`) must never be overwritten.
- Offline / no `claude` CLI must never fail `superclaude install` or `update`.
- Installed primitives must not hardcode `src/superclaude/` paths.
- Coder template changes are out of this PR; write a handoff if needed.
- Only install from `DietrichGebert/ponytail` (ponytail.dev guidance).

## Success Criteria

- After `superclaude install` (new user) or `superclaude update` / `update.sh` (existing user) with network and the `claude` CLI, `ponytail@ponytail` is in `~/.claude/plugins/installed_plugins.json` and enabled in settings, unless the user set it to `false`.
- A user who sets `enabledPlugins["ponytail@ponytail"]: false` keeps it off across reinstalls.
- Failure offline or without `claude` is reported, never fatal.
- Unit tests prove the defaults carry Ponytail and its marketplace, and that `install_plugins` adds the `DietrichGebert/ponytail` marketplace and installs `ponytail@ponytail`.
- Docs and CHANGELOG Unreleased updated; plugin count in docs correct.

## Open Questions

- Where to add Ponytail: the defaults file (`enabledPlugins` + `extraKnownMarketplaces`) versus a dedicated installer step?
- Enabled with Ponytail's own default mode (`full`, always-on rules in every session and subagent), enabled with an IronClaude default mode (`off` or `lite` via `env.PONYTAIL_DEFAULT_MODE`, filled only when unset), or installed but disabled (which hides its skills and so does not meet "valuable skill missing")?
- Does the always-on ruleset conflict with Pragmatic output style, the freshness hooks, or orchestrated Orca workers (statusline nudge, extra context per subagent)?
- Does adding a third marketplace clone (a large repo) fit the shared 30 s network budget, and what happens when it does not?
- Should `install --list` or `doctor` show plugin state, or is that beyond #330?
- What should docs and CHANGELOG say, including how to opt out?

## Enrichment Context

- Codebase (`enrichment/codebase-context.md`, quality fallback_1): the plugin step already runs on install, update and update.sh; adding entries to the defaults file reaches existing users on their next install or update because nested defaults are filled entry by entry; opt-out by `false` already works; nothing lists plugins in `install --list` or `doctor`; docs say "six plugins".
- Research (`enrichment/research-light.md`, quality fallback_1): `ponytail@ponytail` from `DietrichGebert/ponytail`; hooks need `node`; `PONYTAIL_DEFAULT_MODE=off` keeps the skills and commands but stops the always-on rules, codebase map and statusline nudge; `lite` keeps a lighter always-on ruleset.
