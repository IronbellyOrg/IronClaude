# Spec (refactorer variant): Ponytail plugin on every workspace via install and update (issue #330)

Persona: refactorer. Bias: smallest diff, no new mechanism, behaviour change confined to what the issue asks, every existing workspace safe by default.
Evidence date: 2026-11-04. Upstream facts re-read with `gh api` this session. Anything not read is marked UNVERIFIED.

## Decision Summary
Positions on the nine open questions:

| # | Question | Position |
|---|---|---|
| 1 | Where to add Ponytail | Defaults file only (`user_settings_defaults.json`): one `enabledPlugins` entry, one `extraKnownMarketplaces` entry, one `env` entry. No new installer step, no new function. |
| 2 | `superclaude update` / `update.sh` | No change. Verified: `update()` calls `install_user_setup(force=True)` (`main.py:404`); `update.sh:8` runs `superclaude install --force`; `install_user_setup` runs `apply_settings_defaults` then `install_plugins` (`install_user_setup.py:320-322`). A test pins that existing users receive the new entries. |
| 3 | Always-on behaviour | Ship enabled, with `env.PONYTAIL_DEFAULT_MODE = "off"` (filled only when unset). Skills and `/ponytail` commands are available; no rules, map, nudge or per-subagent injection until the user opts in. |
| 4 | Failure behaviour | Reuse the existing non-fatal path. One tiny fix on that path: an install failure is reported as `--scope` instead of the plugin name (`install_user_setup.py:292,305`). Fix it so a Ponytail failure is reported by name. |
| 5 | Opt-out | `enabledPlugins["ponytail@ponytail"]: false` (already honoured, `:266`). Mode control through `env.PONYTAIL_DEFAULT_MODE`. |
| 6 | `install --list` / `doctor` | No change. No plugin appears there today (`main.py:86-172`, `doctor.py:27-49`); showing seven plugins is its own feature. |
| 7 | Docs / CHANGELOG | Remove the plugin count from `installation.md:354` instead of editing "six" to "seven"; add a short Ponytail paragraph; add one `[Unreleased]` entry. |
| 8 | Tests | Five small additions to `tests/cli/test_install_user_setup.py`; no new test file. |
| 9 | Coder handoff | No Coder edit in this PR. A short confirmation note (three checks) goes in the PR description; it is not a blocker. |

Why `off` and not Ponytail's own `full`: `full` changes every session, every subagent and every prompt on every workspace, including unattended Orca workers, and duplicates the ladder Pragmatic already carries (`pragmatic.md:136-152`). `off` still delivers the issue's stated value, the missing skills.


## Requirements
Functional:

- **FR-001** `user_settings_defaults.json` `enabledPlugins` gains `"ponytail@ponytail": true`, appended after `understand-anything@understand-anything` (`:34`).
- **FR-002** `extraKnownMarketplaces` gains `ponytail` with `source.source = "github"`, `source.repo = "DietrichGebert/ponytail"`. No other repo is accepted (seed constraint; marketplace name verified as `ponytail` in upstream `.claude-plugin/marketplace.json`).
- **FR-003** `env` gains `"PONYTAIL_DEFAULT_MODE": "off"`. It is written only when the user has no such key (`apply_settings_defaults`, `:158-161`); a user value, including `full`, is never changed.
- **FR-004** `install_plugins` installs `ponytail@ponytail` through its existing loop (`:271-284`) with no Ponytail-specific code, no version pin and no extra flags.
- **FR-005** The install-failure label in `install_plugins` names the plugin (or the marketplace repo) for both the time-limit and the command-failure case. This is the only Python change. It must not change `ok` (always `True`, `:306-311`).
- **FR-006** `superclaude update`, `update.sh`, `install --list` and `doctor` are not modified.
- **FR-007** `docs/getting-started/installation.md` and `CHANGELOG.md` `[Unreleased]` are updated as in "Docs and CHANGELOG".
- **FR-008** The Pragmatic output style, rules, hooks and `/sc:*` commands are not modified; none may depend on Ponytail being present.

Non-functional:

- **NFR-001** Never fatal: `install_user_setup` success is unchanged when `claude` is missing, the network is down, `node` is missing or the 30 s budget is spent.
- **NFR-002** No overwrite: a user's `enabledPlugins`, `env` and marketplace values survive every install and update.
- **NFR-003** Net diff target: 3 JSON entries, about 4 changed Python lines, tests, 2 doc files. No new module, constant, flag or CLI option.
- **NFR-004** Idempotent: a second `superclaude install` after success reports `✅ Plugins: already installed` (`:285-286`) and adds no settings keys.
- **NFR-005** No `src/superclaude/` path is added to any installed primitive (project rule).
- **NFR-006** Behaviour change visible to existing users on update is limited to: one more plugin, one more env key, no injected context (mode `off`).


## Design
### 3.1 JSON (`src/superclaude/cli/user_settings_defaults.json`)

```json
"env": {
  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
  "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION": "5000",
  "PONYTAIL_DEFAULT_MODE": "off"
},
"enabledPlugins": {
  "...existing six...": true,
  "ponytail@ponytail": true
},
"extraKnownMarketplaces": {
  "...existing two...": {},
  "ponytail": { "source": { "source": "github", "repo": "DietrichGebert/ponytail" } }
}
```

Why this is enough, with evidence:

- `apply_settings_defaults` fills `env`, `enabledPlugins` and `extraKnownMarketplaces` entry by entry (`_NESTED_KEYS`, `:36`; loop `:153-161`), so existing users get the three new keys on their next install or update without losing anything.
- `install_plugins` derives everything from the same file: wanted = defaults whose settings value `is True` (`:266`); marketplace name = text after `@` (`:273`); repo from `extraKnownMarketplaces[market].source.repo` (`:274-278`); install command `claude plugin install <p> --scope user -y` (`:281`). The upstream marketplace name `ponytail` and plugin name `ponytail` make `ponytail@ponytail` resolve with no special case.
- Order: appended last. Reordering for time-budget priority is rejected: it is a behaviour change to six working plugins to help one, and a starved install is retried by rerunning (`:309`).

### 3.2 Python (`src/superclaude/cli/install_user_setup.py`, the only change)

Current defect (verified): for an install command `args = ["plugin","install",p,"--scope","user","-y"]`, so `args[3]` is `"--scope"`. The command-failure path appends `args[3]` (`:305`, `:303`) and the time-limit path builds `"install <p> --scope (time limit)"` (`:292`). A repo log already shows this output: `.dev/codegraph-migration/evidence/P2-layer2.md:358` ("install frontend-design@claude-plugins-official --scope (time limit)").

Proposed shape (illustrative; behaviour is what is pinned):

```python
for args in commands:
    name = args[3] if args[1] == "marketplace" else args[2]   # repo, or plugin id
    remaining = deadline - time.monotonic()
    if remaining < 2:
        failed.append(f"{name} (time limit)")
        continue
    ...
            if result.returncode != 0:
                failed.append(name)
    ...
        except (OSError, subprocess.SubprocessError):
            failed.append(name)
```

Net: one added line, three changed lines. Message becomes `⚠️  Plugins: not installed: DietrichGebert/ponytail, ponytail@ponytail; rerun ...`. The existing assertions (`message.startswith("⚠️  Plugins")`, `"time limit" in message`, `tests/cli/test_install_user_setup.py:240,242`) still hold.

### 3.3 Considered and rejected

- Dedicated `install_ponytail()` step: duplicates `install_plugins` (marketplace add, installed check, deadline handling) for no behavioural gain, and adds a fourth place to keep in sync with the defaults file.
- Writing `~/.config/ponytail/config.json` instead of an `env` key: needs Ponytail's private path resolution (`XDG_CONFIG_HOME`, Windows `APPDATA`, upstream `ponytail-config.js`), new Python, and a new write outside `~/.claude`. See Risks R2 for what the env route costs.
- A `node` pre-check in `install_plugins`: no existing plugin has a prerequisite check (the `playwright` plugin already needs a Node toolchain, UNVERIFIED), so this would be a new concept; deferred.


## Interaction with IronClaude behaviour
What Ponytail does, read from upstream source today (v5.3.3):

| Component | In `full`/`lite`/`ultra` | In `off` |
|---|---|---|
| SessionStart `ponytail-activate.js` | Writes flag, emits ruleset, codebase map (3 s cap), and once a statusline-setup nudge ending "Proactively offer to fix this for the user on first interaction" when `settings.statusLine` is unset | `clearMode()` then `process.exit(0)`: nothing emitted |
| SubagentStart `ponytail-subagent.js` | Injects the ruleset into every subagent | Exits when mode is absent or `off` |
| UserPromptSubmit `ponytail-mode-tracker.js` | Re-injects the ruleset each prompt while mode is active | Injects only for `/ponytail ...` commands |
| Band (`claude-band.json` -> `band/register.tsx`) and ledger CSV | Runs | Runs; the ledger write is gated on the `ledger` option and a project name, not on the level (`register.tsx:158`). UNVERIFIED end to end |

Interactions, each with the position taken:

- **Pragmatic ladder** (`pragmatic.md:136-152`, "Stop at the first rung..."): same doctrine as Ponytail's. Running both at `full` states it twice per session and per subagent with different wording, which can conflict on edge cases. In `off` there is one authority: Pragmatic. A user who wants Ponytail's rules on can opt in per session (`/ponytail`, which upstream switches `off` default to `full`, `ponytail-mode-tracker.js` bare-command branch) or persistently (see Opt-out).
- **Statusline nudge**: the installer never sets `statusLine` (grep of `src/superclaude` finds no `statusLine`), so every fresh workspace would trigger the nudge in a non-`off` mode, and an unattended Orca worker would be told to raise it with a user who is not there. `off` removes it. Rejected: setting `statusLine` ourselves (new settings scope, not asked).
- **Freshness / Edit hooks and rules**: Ponytail registers only SessionStart, SubagentStart and UserPromptSubmit (`hooks/claude-codex-hooks.json`), none on tool use, so it cannot block or reorder Edit-time checks. IronClaude's freshness check is a PreToolUse Edit hook (observed this session: `PreToolUse:Edit hook error: [~/.claude/hooks/freshness-pre-edit.sh]`), a different event, so the two do not touch.
- **`/sc:implement`**: must not depend on Ponytail. The design note recorded in the enrichment (`.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md:208-224`, not re-read here) says it embeds the fix-cost lens and never calls `ponytail-review`. This spec adds no reference to Ponytail in any primitive (FR-008). The only other `src/superclaude` hits for "ponytail" are `sc-pr-submit-protocol/scripts/*.sh` and `sc-implement-protocol/refs/qa.md`; their content was not read, UNVERIFIED, and they are untouched.
- **Orca workers / subagents**: in `off` there is zero per-subagent injection; the three hooks still start a `node` process per event (cost UNVERIFIED, each has a 15 s timeout upstream).
- **Environment**: settings `env` reaching plugin hook processes is expected but not verified against Claude Code docs here: UNVERIFIED. AC-M1 proves it on a throwaway HOME before merge.


## Failure Behaviour
All cases go through code that exists today; none gets new handling.

| Case | Behaviour (verified in `install_plugins`) | Result |
|---|---|---|
| No `claude` CLI | `shutil.which("claude")` is `None` -> `⏭️  Plugins: claude CLI not found; skipped` (`:256-258`). Settings entries are already written by the earlier defaults step, so a later install with `claude` present installs it. | `ok=True` |
| Offline | `claude plugin marketplace add DietrichGebert/ponytail` returns non-zero; the install command also fails; both names are reported by FR-005 | `ok=True`, `⚠️  Plugins: not installed: ...; rerun superclaude install to retry` |
| 30 s shared budget spent | Each command checks `remaining < 2` and is listed as `(time limit)` (`:290-293`); each run is also capped by `timeout=remaining` (`:299`). Orca runs first and may use up to 25 s (`_ORCA_TIMEOUT`, `:34`). | `ok=True`, rerun resumes where it stopped because installed plugins are skipped (`:283`) |
| `node` missing | Not checked by the installer. The plugin installs; its hooks call `node -e ...` (upstream `claude-codex-hooks.json`) and fail. How Claude Code displays that failure: UNVERIFIED. | Documented prerequisite; opt-out is `false` |
| Marketplace add fails but plugin install is attempted anyway | Existing behaviour (commands are appended unconditionally, `:277-284`); the install fails and is reported | unchanged |
| Malformed `settings.json` | `apply_settings_defaults` returns `ok=False` and leaves the file (`:147-148`); pre-existing, unchanged | unchanged |

Clone size: upstream repo `size` is 13130 KB (about 13 MB, `gh api repos/DietrichGebert/ponytail`, 2026-11-04), so it is not an outlier next to the two existing marketplaces; actual clone time on a Coder workspace is UNVERIFIED. The three clones plus up to seven installs share one 30 s budget; an earlier run shows the budget can be fully spent (`.dev/codegraph-migration/evidence/P2-layer2.md:358`, environment of that run unknown).


## Opt-out
No new opt-out mechanism. The documented ones:

1. **Do not want Ponytail at all**: set `"ponytail@ponytail": false` in `~/.claude/settings.json` `enabledPlugins`. `apply_settings_defaults` keeps a present key (`:159`) and `install_plugins` only installs entries that are `True` (`:266`). Do not delete the key (the next run re-adds `true`) and do not only run `claude plugin uninstall` (the next run reinstalls it).
2. **Want Ponytail's always-on rules**: set `env.PONYTAIL_DEFAULT_MODE` to `lite`, `full` or `ultra` in `settings.json`. For one session, type `/ponytail` (or `/ponytail lite|full|ultra`).
3. **Want to stop the local ledger/band**: UNVERIFIED how plugin `userConfig.ledger` is set from a settings file; point users to `/ponytail band off` (upstream tracker, hides the band; whether it stops the CSV write is UNVERIFIED) or opt-out 1.
4. The env default beats Ponytail's own `~/.config/ponytail/config.json` `defaultMode` (upstream resolution order: env, then file, then `full`; `ponytail-config.js`). So `/ponytail default full` is ignored while our `env` key is `off`. The docs must say this in one sentence (Risk R2).

The existing test pattern (`tests/cli/test_install_user_setup.py:73-99`) already proves a user `False` survives; FR tests below extend it to Ponytail and to the env key.


## Visibility (install --list / doctor)
Decision: neither command changes in this PR.

- `install --list` prints core, commands, agents, skills, templates, codegraph and retired MCP only (`main.py:86-172`). None of the six existing plugins appears; adding only Ponytail would be inconsistent, adding all seven is a feature.
- `doctor` runs pytest-plugin, agents, skills, configuration, ccsession, codegraph and retired-MCP checks (`doctor.py:27-49`); "plugin" there means the pytest plugin. `update.sh:10` runs `superclaude doctor`, so a new plugin check would also gate updates on network/CLI state, which contradicts "never fatal".
- The install summary line already names what happened: `✅ Plugins: installed ...` or the warning above. That is the visibility this issue needs.
- If wanted later: one backlog issue, "report default-plugin state in doctor (informational, never failing)", per `~/.claude/ISSUE-BACKLOG.md`.


## Docs and CHANGELOG
**`docs/getting-started/installation.md:353-360`** (read this session). Replace the count so it cannot drift again, and add one short block:

```text
`superclaude install` also installs the default Claude Code plugins listed in
its settings defaults (including `playwright`, `frontend-design` and `ponytail`)
with `claude plugin install <plugin> --scope user`, skipping any you disabled in
`enabledPlugins`. ... [unchanged budget/retry sentences] ...

`ponytail` (from `DietrichGebert/ponytail`) is installed with its always-on mode
off: `env.PONYTAIL_DEFAULT_MODE` is set to `off` unless you already set it, so
its skills and `/ponytail` commands are available and nothing is added to your
sessions. Type `/ponytail` for one session, or set that variable to `lite`,
`full` or `ultra` to make it your default (the variable overrides
`/ponytail default <mode>`). Its hooks need `node` on your PATH. To turn it off
completely set `"ponytail@ponytail": false` in `enabledPlugins`.
```

Also update the "Hook registrations and settings defaults" table row only if it lists plugins (it does not, `:345`), so no change there. `docs/testing/v5.0.0/post-release-manifest.json:28` says "default plugins" without a count: no change.

**`CHANGELOG.md`** (`[Unreleased]` is empty at `:5`; headings follow the `#### Changed (topic)` style used at `:13`):

```text
### Ponytail plugin installed by default (#330)

#### Added (default plugins)

- `superclaude install` and `superclaude update` (and `update.sh`) now install the Ponytail plugin (`ponytail@ponytail`, from `DietrichGebert/ponytail`). It ships with `env.PONYTAIL_DEFAULT_MODE` set to `off`, so its skills and `/ponytail` commands are available but it adds no rules, codebase map or statusline prompt to your sessions. Set that variable to `lite`, `full` or `ultra` to turn the always-on mode on, or set `enabledPlugins["ponytail@ponytail"]` to `false` to opt out. If you already use Ponytail with a default in `~/.config/ponytail/config.json`, set `env.PONYTAIL_DEFAULT_MODE` to the same value: the variable takes priority over that file. Needs `node` on the PATH.

#### Fixed (plugin install report)

- A plugin that fails to install is now listed by its name in the `Plugins: not installed` warning (it printed `--scope`).
```


## Tests and Acceptance Criteria
All in `tests/cli/test_install_user_setup.py` (helpers `_settings`, `_plugin_home`, `fake_run` pattern at `:15,175-209`). Run with `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py -v`.

| ID | Test | Proves |
|---|---|---|
| T1 | New `test_defaults_ship_ponytail`: load the defaults file; assert `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"] == {"source": "github", "repo": "DietrichGebert/ponytail"}`, `env["PONYTAIL_DEFAULT_MODE"] == "off"`; assert every `enabledPlugins` key's marketplace has a `source.repo` (guards every future add) | FR-001..003 |
| T2 | Extend `test_plugins_install_missing_enabled_defaults` (`:182-209`): assert `["plugin","marketplace","add","DietrichGebert/ponytail"]` in calls and `ponytail@ponytail` in installs | FR-002, FR-004 |
| T3 | Extend `test_settings_defaults_fill_only_missing_values` (`:73-99`): user has `enabledPlugins["ponytail@ponytail"]: False` and `env.PONYTAIL_DEFAULT_MODE: "full"`; after apply both unchanged | FR-003, NFR-002, opt-out |
| T4 | New `test_existing_user_gets_ponytail_on_update`: settings hold only the old six plugins and two marketplaces; `apply_settings_defaults` adds `enabledPlugins.ponytail@ponytail`, `extraKnownMarketplaces.ponytail`, `env.PONYTAIL_DEFAULT_MODE`, leaves the rest; a second run is `(True, "✅ Settings defaults: already present")` | existing users, NFR-004 |
| T5 | Extend `test_plugin_failures_and_time_limit_never_fail_install` (`:229-242`): with `ponytail@ponytail` enabled and `returncode=1`, `ok is True`, message contains `ponytail@ponytail` and not `--scope`; with `deadline=0` it contains `(time limit)` and the name | FR-005, NFR-001 |
| T6 | `test_plugins_skip_already_installed` (`:212-226`) stays green unchanged | NFR-004 |

Update path coverage: `tests/cli/test_update_command.py:24-48,253-289` already stub and assert `install_user_setup` inside `update`; no new test, because `update.sh:8` and `main.py:404` are unchanged and T4 covers what `install_user_setup` does for an existing user.

Acceptance criteria:

- **AC-1** With T1..T5 green, `uv run pytest tests/cli tests/unit/test_cli_install.py` passes and `make lint` is clean.
- **AC-2** `git diff --stat` touches only: `user_settings_defaults.json`, `install_user_setup.py` (at most 5 changed lines), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md`, `CHANGELOG.md`. No `update.sh`, `main.py`, `doctor.py`, output style, `.claude/` file.
- **AC-3** `grep -rn 'src/superclaude' ` on files changed adds no installed-primitive hit.
- **AC-M1 (manual, throwaway HOME under /tmp, never the real `~/.claude`)** After `superclaude install` in a new HOME with network and `claude`: `installed_plugins.json` lists `ponytail@ponytail`; `settings.json` has the three keys; a started session shows no `PONYTAIL` ruleset context and `~/.claude/.ponytail-active` is absent (this also proves `env` reaches the hook, resolving the UNVERIFIED in Interaction). Then `/ponytail lite` switches it on for the session.
- **AC-M2 (manual)** Set `enabledPlugins["ponytail@ponytail"]` to `false`, rerun install: no Ponytail command runs, the value stays `false`.
- **AC-M3 (manual)** Run install with `PATH` lacking `claude`: exit 0 and the skip line; with the network blocked: exit 0 and the named warning.


## Risks
| ID | Risk | Prob. | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Our `env` default overrides a user's own `~/.config/ponytail/config.json` `defaultMode` (env has top priority upstream) for someone who already runs Ponytail | Low | Low-Med (their always-on mode silently turns off) | CHANGELOG sentence (above); user fixes with one `env` line. Accepted over adding config-file code |
| R2 | `/ponytail default <mode>` is silently ignored while the env key is `off` | Med (among Ponytail users) | Low | One docs sentence; in-session `/ponytail <level>` works; fix is editing the env key |
| R3 | `node` absent: hooks fail on each SessionStart, SubagentStart and prompt, even in `off` | Low-Med | Med (noise; display UNVERIFIED) | Docs prerequisite; opt-out `false`; follow-up for a prerequisite check if seen in practice |
| R4 | 30 s budget starves the last-listed plugin (Ponytail, Orca runs first) on a fresh workspace | Med | Low (reported by name, rerun resumes) | FR-005 naming; documented rerun; Coder handoff check 3 |
| R5 | Unpinned third-party code runs three hooks every session; upstream `main` can change (v5.3.1-v5.3.3 shipped in Oct 2026) | Low | High | Same trust model as `understand-anything`; only `DietrichGebert/ponytail` allowed (seed constraint); `off` removes rules injection but not code execution; pinning syntax for `claude plugin install` UNVERIFIED, so none proposed |
| R6 | Band/ledger CSV (`~/.config/ponytail/band/<project>.csv`, local, webhook empty by default) is written even in `off` | Med | Low | Documented; opt-out 1; gating UNVERIFIED end to end |
| R7 | Users read "installed but does nothing" as broken | Med | Low | Docs and CHANGELOG say `off` is deliberate and give the one-line switch |
| R8 | Message-text change (FR-005) breaks a consumer that parses `--scope` | Very low | Low | Repo grep found only the evidence log `.dev/codegraph-migration/evidence/P2-layer2.md`, not code |
| R9 | `PONYTAIL_DEFAULT_MODE=off` value stops being valid upstream | Very low | Low | `off` is a runtime mode in `RUNTIME_MODES` (`ponytail-config.js`); an unknown value falls through to `full`, so a future rename degrades to Ponytail's default, which T1 does not catch; re-check on upstream major bumps |


## Out of Scope
- Any edit to `update.sh`, `main.py` (`update()`, `install --list`, the install banner at `:233` that omits "plugins"), `doctor.py`.
- A `node` or `claude`-version prerequisite check, a per-plugin "requires" table, version pinning, or a generic plugin framework.
- Reordering or prioritising plugins under the 30 s budget; changing `_NETWORK_BUDGET` or `_ORCA_TIMEOUT`.
- Setting `statusLine`, writing `~/.config/ponytail/config.json`, or setting plugin `userConfig` (ledger, webhook).
- Reworking the Pragmatic ladder, adding Ponytail references to any skill, command or agent, or making `/sc:implement` call `ponytail-review`.
- Any edit in the Coder repo; any run of `superclaude install/update`, `update.sh` or `claude plugin` against the real `~/.claude`.
- Plugin state in `doctor` / `install --list` (backlog candidate).


## Coder Handoff
A handoff is needed only as a confirmation, not as a Coder change. The Coder repo was not read (UNVERIFIED); `install_user_setup.py:31-33` records that `superclaude install` runs under a 60 s limit in Coder workspaces, which is why the budget exists. This PR reaches a workspace only when `superclaude install` or `update` runs in it, so "all workspaces" holds only if the template does that. Put this in the PR description for the Coder owner (no file in the Coder repo, no Orca link flags):

1. Does the template run `superclaude install` (or `update`) on workspace create and on refresh? If a template pre-writes `~/.claude/settings.json` with its own `enabledPlugins`, entries it omits are still filled (nested fill), but a template that pins `PONYTAIL_DEFAULT_MODE` or sets `"ponytail@ponytail": false` wins by design.
2. Are the `claude` CLI and `node` on PATH before that step runs? Without `claude` the plugin is skipped; without `node` the hooks fail (R3).
3. Is there headroom in the 60 s limit for one more marketplace clone inside the existing 30 s network budget (R4)? If not, the owner can raise the limit or accept a second `superclaude install` run.

No answer blocks this PR. If answers 1 or 2 are "no", open a backlog issue in the Coder repo, filled from `~/.claude/ISSUE-HANDOFF.md`.

