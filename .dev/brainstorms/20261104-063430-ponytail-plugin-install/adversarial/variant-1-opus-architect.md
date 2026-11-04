# Spec: Ponytail on every workspace through the existing plugin defaults (issue #330)

Variant 1, persona: architect (Opus). Generated 2026-11-04.

## Decision Summary

The plugin step is already data-driven: `install_plugins` reads `enabledPlugins` and `extraKnownMarketplaces` from `user_settings_defaults.json` and installs what it finds (`src/superclaude/cli/install_user_setup.py:251-311`). The maintainable change is therefore **data, not code**: three entries in that one file, plus docs, CHANGELOG and tests. No new installer step, no Ponytail-specific Python, no change to `update` or `update.sh`.

| # | Open question | Position |
|---|---|---|
| 1 | Where | Defaults file only: `enabledPlugins["ponytail@ponytail"]`, `extraKnownMarketplaces.ponytail`, `env.PONYTAIL_DEFAULT_MODE`. |
| 2 | Update paths | No change. `superclaude update` calls `install_user_setup(force=True)` (`main.py:403-405`); `update.sh:8` runs `superclaude install --force`, which reaches step 7 (`main.py:231-237`). |
| 3 | Always-on behaviour | Ship **enabled, with `env.PONYTAIL_DEFAULT_MODE = "off"`**, filled only when unset. Skills and `/ponytail` commands are present (closes "valuable skill missing"); no ruleset, codebase map or statusline nudge is injected into sessions or subagents unless the user turns it on. |
| 4 | Failure | Inherit the existing non-fatal contract unchanged; Ponytail is placed last so it cannot starve the six existing plugins of the 30 s budget. |
| 5 | Opt-out | `enabledPlugins["ponytail@ponytail"]: false` (already honoured). Deleting the key is not an opt-out; the next install re-adds it. |
| 6 | Visibility | No change to `install --list` or `doctor`. The install step's own line already reports success, skip or failure. |
| 7 | Docs | `installation.md:353-360` becomes "seven plugins" with a short Ponytail paragraph; one CHANGELOG Unreleased entry. |
| 8 | Tests | Extend `tests/cli/test_install_user_setup.py`: defaults carry the three entries; `install_plugins` adds `DietrichGebert/ponytail` and installs `ponytail@ponytail`; user `false` and user mode are kept. |
| 9 | Coder | No handoff needed for this PR; one optional note (see Coder Handoff). |

Rejected alternatives: (a) a dedicated `install_ponytail()` step: duplicates `install_plugins` for one plugin and breaks the single place that lists default plugins; (b) Ponytail's own default `full`: doubles the ladder already in Pragmatic and fires a statusline nudge on every new workspace; (c) installed but disabled: hides the skills, so #330 stays open; (d) writing `~/.config/ponytail/config.json` instead of `env`: new installer code outside `~/.claude` for a value the existing env merge already handles (kept as the fallback if V-1 below fails).

## Requirements

Functional:

- **FR-001** `user_settings_defaults.json` `enabledPlugins` contains `"ponytail@ponytail": true`, as the last entry.
- **FR-002** `extraKnownMarketplaces` contains `"ponytail": {"source": {"source": "github", "repo": "DietrichGebert/ponytail"}}`. No other source repo for Ponytail anywhere in the change.
- **FR-003** `env` contains `"PONYTAIL_DEFAULT_MODE": "off"`.
- **FR-004** `superclaude install`, `superclaude install --force`, `superclaude update` and `update.sh` install `ponytail@ponytail` at user scope when the `claude` CLI and network are available and the user value is `true`. Achieved through the existing call chain; no code change.
- **FR-005** An existing workspace gets the three entries on its next install or update, because nested defaults are filled entry by entry (`install_user_setup.py:153-161`).
- **FR-006** A user value for `enabledPlugins["ponytail@ponytail"]` (including `false`) or for `env.PONYTAIL_DEFAULT_MODE` is never overwritten (`install_user_setup.py:159`).
- **FR-007** With the user value `false`, `install_plugins` neither adds the marketplace nor installs the plugin (`wanted` filter, `install_user_setup.py:266`).

Non-functional:

- **NFR-001** Zero lines of Python change in `src/superclaude/cli/`. If an implementer finds a code change is needed, that is a spec deviation to report, not to absorb.
- **NFR-002** Failure of any Ponytail command never changes the exit code of install or update (existing `ok=True` contract, `install_user_setup.py:306-311`).
- **NFR-003** The shared network budget stays 30 s (`install_user_setup.py:35`); it is not raised for Ponytail.
- **NFR-004** No installed primitive gains a `src/superclaude/` path (no primitive is edited).
- **NFR-005** Ponytail is sourced only from `DietrichGebert/ponytail`.

## Design

Single file edit, `src/superclaude/cli/user_settings_defaults.json` (current lines 10-13, 28-35, 36-49):

```json
"env": {
  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
  "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION": "5000",
  "PONYTAIL_DEFAULT_MODE": "off"
},
...
"enabledPlugins": {
  ...existing six unchanged...,
  "understand-anything@understand-anything": true,
  "ponytail@ponytail": true
},
"extraKnownMarketplaces": {
  ...existing two unchanged...,
  "ponytail": {
    "source": { "source": "github", "repo": "DietrichGebert/ponytail" }
  }
}
```

Why this works with no code (all in `install_user_setup.py`):

- `apply_settings_defaults` (`:137-172`) runs before `install_plugins` (`:317-323`), so a new user's settings carry `true` by the time `wanted` is computed.
- `install_plugins` maps `ponytail@ponytail` to market `ponytail` (`:273`), reads `source.repo` (`:274-276`), and queues `claude plugin marketplace add DietrichGebert/ponytail` only when `ponytail` is absent from `known_marketplaces.json` (`:277-279`). Upstream `.claude-plugin/marketplace.json` names the marketplace `ponytail` (read via `gh api`, 2026-11-04). UNVERIFIED: that `claude` keys `known_marketplaces.json` by that `name`; the two existing marketplaces rely on the same assumption.
- Marketplace adds are queued before installs (`:271-284`) and installs follow `enabledPlugins` order, so placing Ponytail last means its commands run after the six existing plugins' commands.

Extension rule (already true, nothing new built): the next default plugin is added the same way, by data. No registry, hook or per-plugin config is introduced.

## Interaction with IronClaude behaviour

Ponytail facts below were read from `DietrichGebert/ponytail` `main` with `gh api` on 2026-11-04.

| Ponytail surface | In mode `full`/`lite` | In mode `off` (this spec) | IronClaude overlap |
|---|---|---|---|
| SessionStart `ponytail-activate.js` | Emits ruleset; codebase map unless `PONYTAIL_MAP=0` (`:66`); one-time statusline nudge "Proactively offer to set this up for the user on first interaction" when `settings.statusLine` is unset (`:146-162`) | Exits before writing the flag or emitting anything (`:31-35`) | Pragmatic "The ladder" already carries the same rule ("The best code is the code that does not need to exist", `pragmatic.md:136-152`). The installer never sets `statusLine`, so the nudge would fire on every new workspace and invite an unrequested settings edit. |
| SubagentStart `ponytail-subagent.js` | Injects the ruleset into every subagent (or those matching `PONYTAIL_SUBAGENT_MATCHER`) | Absent or `off` flag: injects nothing | IronClaude already injects two blocks per subagent: `freshness-subagent-start.sh` and `pragmatic-subagent.js` (`src/superclaude/hooks/hooks.json:110-128`). `full` would add a third, duplicating the ladder in every Orca worker and `/sc:*` subagent. |
| UserPromptSubmit `ponytail-mode-tracker.js` | Reacts only to `/ponytail ...` and "stop ponytail"/"normal mode"; per-prompt ruleset injection is Qoder-only | Same; ordinary prompts produce no output in Claude Code | None. |
| Band `band/register.tsx` and ledger | Band shown; ledger row per turn | **Not gated on mode**: `turn.complete` reads the level for display only, and `record()` writes the CSV unless `userConfig.ledger` is `false` (`register.tsx:154-163`) | Writes `~/.config/ponytail/band/<project>.csv` locally; webhook empty by default. Accepted as the plugin's normal footprint; see R-4. |
| Skills `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-help`, `ponytail-gain` | Available | Available | `/sc:implement` never invokes `ponytail-review` and must not depend on it (`.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md:208-224`, asserted by `tests/skills/test_implement_severity_static.py:149`). Nothing in this spec changes that. |

Why `off` rather than `lite`: every non-`off` mode runs the statusline nudge and the subagent injection; only `off` keeps IronClaude's Pragmatic style the single always-on ruleset while still delivering the skills the issue asks for. A user who wants the always-on mode types `/ponytail` (bare `/ponytail` with default `off` switches the session to `full`, per `ponytail-mode-tracker.js`) or sets their own `env.PONYTAIL_DEFAULT_MODE`.

Freshness hooks: no interaction. Ponytail's hooks emit context only and never block tools; IronClaude's `freshness-*` hooks are unaffected.

**V-1 (must be checked before merge, in a throwaway `HOME` under `/tmp`):** that a value in `settings.json` `env` reaches plugin hook subprocesses. Claude Code docs say a settings-file `env` value "applies every time `claude` runs" (code.claude.com/docs/en/env-vars); propagation to hook processes is UNVERIFIED. Pass: a new session in that HOME shows no Ponytail ruleset and no `.ponytail-active` flag is written. Fail: replace FR-003 with rejected alternative (d), writing `{"defaultMode": "off"}` to `~/.config/ponytail/config.json` only when the file is absent, which needs a code change and an NFR-001 waiver.

## Failure Behaviour

All rows are existing behaviour of `install_plugins`; the spec adds no handling.

| Condition | What happens | Evidence |
|---|---|---|
| No `claude` CLI | `⏭️  Plugins: claude CLI not found; skipped`; settings defaults (including the three entries) are still written, since that step runs first | `install_user_setup.py:256-258`, `:317-323` |
| Offline | `marketplace add` and `plugin install` exit non-zero; line `⚠️  Plugins: not installed: DietrichGebert/ponytail, ponytail@ponytail; rerun superclaude install to retry`; exit code unchanged | `:302-310` |
| Budget exhausted (less than 2 s left) | Each remaining command reported with `(time limit)`, e.g. `marketplace add DietrichGebert/ponytail (time limit)`; never fatal | `:290-293` |
| Next run after a partial run | Installed plugins and known marketplaces are skipped, so only Ponytail's commands run; reruns converge | `:268-284` |
| No `node` | Install succeeds (it is a git clone). At runtime each Ponytail hook (`node -e ...`, 15 s timeout) fails to start, including in mode `off`, since the hook must run to read the mode. IronClaude's own `pragmatic-subagent.js` already needs `node` (`install_hooks.py:66-68`), so a workspace without `node` is already degraded. No `node` check is added. How Claude Code shows the failed hook is UNVERIFIED. |
| Enabled in settings but not installed (any failure above) | Same state the six existing plugins can already be in; Claude Code's handling is UNVERIFIED and not changed here. |

Budget fit: the Ponytail repository is 13,130 KB (`gh api repos/DietrichGebert/ponytail` `.size`, 2026-11-04). On a fresh workspace it is the last of three marketplace clones and the last of seven installs, so it is the plugin most likely to hit the time limit. That is acceptable: the existing six keep their share, and the next `install`/`update` finishes it. Raising `_NETWORK_BUDGET` is rejected because the comment at `install_user_setup.py:31-33` ties it to Coder's 60 s install limit.

## Opt-out

- Turn it off: set `"ponytail@ponytail": false` in `~/.claude/settings.json` `enabledPlugins`. `apply_settings_defaults` keeps it (`:159`); `install_plugins` skips it (`:266`). Already-downloaded files remain under `~/.claude/plugins/`; removing them is Claude Code's `/plugin` UI, not the installer (exact uninstall command UNVERIFIED, so docs do not name one).
- Deleting the key is not an opt-out: the next install re-adds `true` (`:159-161`). Docs say so.
- Turn the always-on mode on: `/ponytail` per session, or set `env.PONYTAIL_DEFAULT_MODE` to `lite`/`full`/`ultra` in `settings.json`; the installer keeps that value.
- Caveat: Ponytail resolves the env variable before its own config file (`ponytail-config.js` `getDefaultMode`), so `/ponytail default full` writes the config file and prints "new sessions start in full", but the `off` env value still wins. Docs tell users to change the env value instead (R-2).

## Visibility (install --list / doctor)

No change. `install --list` (`main.py:86-172`) lists files IronClaude copies; plugins are downloaded by `claude`, not copied. `doctor` (`doctor.py:17-49`) has no plugin check for the existing six either. Adding a plugin report for one issue would be a new feature with its own `installed_plugins.json` parsing and tests; #330 does not ask for it. The install and update output already prints the plugin line (`✅ Plugins: installed ...`, `✅ Plugins: already installed`, or the `⚠️` line), which is the visibility the existing six have.

## Docs and CHANGELOG

`docs/getting-started/installation.md:353-360`: change "six plugins, including `playwright` and `frontend-design`" to "seven plugins, including `playwright`, `frontend-design` and `ponytail`", and add one paragraph after it:

> Ponytail (`ponytail@ponytail`, from the `DietrichGebert/ponytail` marketplace) adds the `ponytail-*` skills and the `/ponytail` command. The installer also sets `PONYTAIL_DEFAULT_MODE` to `off` in your settings `env` (only if you have not set it), so Ponytail adds no always-on rules, codebase map or statusline offer to your sessions or subagents; IronClaude's Pragmatic output style already carries the same rules. Type `/ponytail` to switch it on for one session, or change `PONYTAIL_DEFAULT_MODE` in `~/.claude/settings.json` (`/ponytail default` has no effect while that variable is set). Its hooks need `node`. Ponytail keeps a local per-turn ledger under `~/.config/ponytail/band/`. To opt out, set `"ponytail@ponytail": false` in `enabledPlugins`; deleting the entry does not opt out, because the next install adds it back.

`CHANGELOG.md:5` `## [Unreleased]`, in the file's existing style:

```markdown
### Installer: Ponytail plugin on every workspace (#330)

#### Added (Ponytail plugin)

- `superclaude install`, `superclaude update` and `update.sh` install the Ponytail plugin (`ponytail@ponytail`, from `DietrichGebert/ponytail`) with the other default plugins, and set `PONYTAIL_DEFAULT_MODE=off` in the settings `env` when unset, so its skills are available without a second always-on ruleset next to the Pragmatic output style. Opt out with `"ponytail@ponytail": false` in `enabledPlugins`.
```

`docs/testing/v5.0.0/c-e2e-transcript.txt:308` is a historical transcript and is not edited.

## Tests and Acceptance Criteria

Tests, all in `tests/cli/test_install_user_setup.py`, using the existing `_plugin_home` and `fake_run` patterns (`:175-209`); no network, no real `claude`:

- **T-1** Defaults carry Ponytail: `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"] == {"source": "github", "repo": "DietrichGebert/ponytail"}`, `env["PONYTAIL_DEFAULT_MODE"] == "off"`, and `ponytail@ponytail` is the last `enabledPlugins` key.
- **T-2** Extend `test_plugins_install_missing_enabled_defaults` (`:182-209`): assert `["plugin", "marketplace", "add", "DietrichGebert/ponytail"] in calls` and `"ponytail@ponytail" in installs`. It already enables every default, so this is two assertions.
- **T-3** Opt-out: with `{"ponytail@ponytail": False}` plus one other default enabled, no call contains `DietrichGebert/ponytail` or `ponytail@ponytail`.
- **T-4** Extend `test_settings_defaults_fill_only_missing_values` (`:73-98`): a user `env.PONYTAIL_DEFAULT_MODE = "full"` and `enabledPlugins["ponytail@ponytail"] = False` survive `apply_settings_defaults`; a fresh settings file gets `"off"` and `True`.
- No change to `tests/cli/test_update_command.py`: it stubs `install_plugins` (`:44-46`) and the update-to-user-setup call is already covered.

Acceptance criteria:

- **AC-1** `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py -v` passes, including T-1 to T-4.
- **AC-2** `git diff --stat` touches only `user_settings_defaults.json`, the test file, `installation.md` and `CHANGELOG.md` (plus `.dev/tasks/` per repo rule). No file under `src/superclaude/cli/*.py`.
- **AC-3** V-1 passes in a throwaway `HOME` under `/tmp` (never this workspace's `~/.claude`): after `superclaude install` there, `installed_plugins.json` lists `ponytail@ponytail`, settings show the three entries, and a new `claude` session emits no Ponytail ruleset; `/ponytail` then switches it on. Evidence recorded in the PR. If the run cannot reach the network, record that and rely on AC-1 for install mechanics, but V-1's env propagation still needs a session check.
- **AC-4** Offline or without `claude`, `superclaude install` still exits 0 when every other phase succeeds (covered by existing `test_plugin_failures_and_time_limit_never_fail_install`, `:229-242`).
- **AC-5** `make lint` and `make verify-sync` pass.

## Risks

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-1 | `settings.env` does not reach plugin hooks, so Ponytail runs `full` despite FR-003 | Low | High (duplicate ruleset in every session and subagent, statusline nudge) | V-1 gate before merge; fallback (d) defined above |
| R-2 | User runs `/ponytail default full`, sees "new sessions start in full", but env `off` wins | Medium | Low (confusion only) | Docs paragraph names the env value as the switch |
| R-3 | Ponytail times out on fresh Coder workspaces (13 MB clone, last in queue) | Medium | Low (installed on the next install/update) | Placed last; non-fatal; reruns converge |
| R-4 | Band and ledger run even in `off`: per-turn CSV under `~/.config/ponytail/band/`, a band above the prompt, `git grep` after turns | High | Low (local only, webhook empty by default) | Documented; `/ponytail band off` hides the band. Disabling the ledger needs Ponytail `userConfig.ledger=false`; how to set userConfig non-interactively is UNVERIFIED, so it is not automated |
| R-5 | Upstream changes mode resolution, hook names or marketplace name in a later release | Low | Medium | Tests pin only IronClaude's data, not upstream internals; V-1 is the integration check; failure stays non-fatal |
| R-6 | Supply chain: an always-on third-party hook from a personal GitHub account runs on every workspace | Low | High | Single named source (NFR-005); MIT; opt-out documented. No version pin: `claude plugin install` takes the marketplace head and pinning is not supported by the existing step (UNVERIFIED whether `claude` supports a ref) |
| R-7 | No `node`: three failing hooks per session | Low | Low | IronClaude already needs `node`; documented |

## Out of Scope

- Plugin state in `superclaude install --list` or `superclaude doctor` (for any plugin).
- Raising `_NETWORK_BUDGET`, retry logic, or pinning plugin versions.
- Writing `~/.config/ponytail/config.json`, setting `PONYTAIL_MAP`, `PONYTAIL_SUBAGENT_MATCHER` or Ponytail `userConfig` (unless V-1 fails, then only the config file per fallback (d)).
- Setting a `statusLine`.
- Any change to Pragmatic, rules, freshness hooks, `/sc:implement` or other primitives.
- The Coder template repository.

## Coder Handoff

Not needed for this PR. Coder workspaces get Ponytail through the same `superclaude install`/`update` they already run, and the 60 s install limit is already respected by the shared 30 s budget. One note for the Coder owner, to be filed only if they want it (with `~/.claude/ISSUE-HANDOFF.md`): a workspace image without `node` would show Ponytail hook failures; IronClaude's `pragmatic-subagent.js` has the same need today, so this is not new work created by #330.
