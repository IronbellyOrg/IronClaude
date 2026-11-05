<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:refactorer) -->
<!-- Merge date: 2026-11-04T07:51:51Z -->
<!-- Incorporated: Variant A (opus:architect), Variant C (haiku:qa), invariant-probe.md orchestrator decisions; plan: adversarial/refactor-plan.md (22 changes); log: adversarial/merge-log.md -->

# Spec (refactorer variant): Ponytail plugin on every workspace via install and update (issue #330)
<!-- Source: Base (original) -->

Persona: refactorer. Bias: smallest diff, no new mechanism, behaviour change confined to what the issue asks, every existing workspace safe by default.
Evidence date: 2026-11-04. Upstream facts re-read with `gh api` this session. Anything not read is marked UNVERIFIED.

## Decision Summary
<!-- Source: Base (original, modified) — rows 2, 4, 7, 8, 9 per Change #21; row 3 per Change #7 (INV-001); row 6 count removed in post-merge validation; "Why off" paragraph: Variant A (opus:architect), Interaction table SubagentStart row — merged per Change #5, footprint sentence per Change #7 -->
Positions on the nine open questions:

| # | Question | Position |
|---|---|---|
| 1 | Where to add Ponytail | Defaults file only (`user_settings_defaults.json`): one `enabledPlugins` entry, one `extraKnownMarketplaces` entry, one `env` entry. No new installer step, no new function. |
| 2 | `superclaude update` / `update.sh` | No change. Verified: `update()` calls `install_user_setup(force=True)` (`main.py:404`); `update.sh:8` runs `superclaude install --force`; `install_user_setup` runs `apply_settings_defaults` then `install_plugins` (`install_user_setup.py:320-322`). A test pins that existing users receive the new entries. Existing workspaces get the entries only after the IronClaude package itself is upgraded (Docs and CHANGELOG). |
| 3 | Always-on behaviour | Ship enabled, with `env.PONYTAIL_DEFAULT_MODE = "off"` (filled only when unset). Skills and `/ponytail` commands are available. In `off`, Ponytail injects no ruleset, codebase map, statusline offer or subagent context until the user opts in; its band module still runs in every session, Orca workers included (band above the prompt, `git grep` at session start, Edit/Write watch, per-turn ledger row; see Interaction, "`off` footprint"). |
| 4 | Failure behaviour | Reuse the existing non-fatal path. One tiny fix on that path: a failed `plugin install` is reported as `--scope` instead of the plugin id (`install_user_setup.py:303,305`), and a time-limited one as `install <id> --scope (time limit)` (`:292`). Fix both paths so every failure is named by plugin id (or marketplace repo), with no `--scope`. |
| 5 | Opt-out | `enabledPlugins["ponytail@ponytail"]: false` (already honoured, `:266`). Mode control through `env.PONYTAIL_DEFAULT_MODE`. |
| 6 | `install --list` / `doctor` | No change. No plugin appears there today (`main.py:86-172`, `doctor.py:27-49`); showing all default plugins is its own feature. |
| 7 | Docs / CHANGELOG | Remove the plugin count from `installation.md:354` instead of editing "six" to "seven"; add a short Ponytail paragraph; add one `[Unreleased]` entry. Opt out in user settings; do not delete the key; `grep -rn "six plugins" docs/` returns nothing. |
| 8 | Tests | T1-T5 plus T5c in `tests/cli/test_install_user_setup.py`; T3/T4 merged into the extended fill test; no new test file. |
| 9 | Coder handoff | No Coder edit in this PR. Coder Handoff section (confirmation only, four questions); a summary goes in the PR description; it is not a blocker. The PR keeps `Closes #330`. |

Why `off` and not Ponytail's own `full`: `full` changes every session, every subagent and every prompt on every workspace, including unattended Orca workers, and duplicates the ladder Pragmatic already carries (`pragmatic.md:136-152`). IronClaude already injects two blocks into every subagent (`freshness-subagent-start.sh` and `pragmatic-subagent.js`, `src/superclaude/hooks/hooks.json:110-128`); a non-`off` mode would add a third to every Orca worker and `/sc:*` subagent. `off` still delivers the issue's stated value, the missing skills. `off` is not silent: Ponytail's band module keeps running in every session (Interaction, "`off` footprint").


## Requirements
<!-- Source: Base (original, modified) — NFR-003: Variant A (opus:architect), Round 2 R-2 replacement rule — merged per Change #3; NFR-006 per Change #7 (INV-001) -->
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
- **NFR-003** A default plugin is added by data only; there is no per-plugin code. Code changes are allowed only for defects on the shared plugin path, each pinned by a test and named in AC-2. This PR's only such change is FR-005 (at most 5 changed Python lines). No new module, constant, flag or CLI option.
- **NFR-004** Idempotent: a second `superclaude install` after success reports `✅ Plugins: already installed` (`:285-286`) and adds no settings keys.
- **NFR-005** No `src/superclaude/` path is added to any installed primitive (project rule).
- **NFR-006** Behaviour change visible to existing users on update is limited to: one more plugin, one more env key, no injected ruleset in mode `off`, and the band module's footprint (Interaction, "`off` footprint").


## Design
### 3.1 JSON (`src/superclaude/cli/user_settings_defaults.json`)
<!-- Source: Base (original, modified) — "Order" bullet per Change #1 (Round 2 consensus of A, B, C) -->

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
- Order: appended last as a diff-hygiene convention (one added line per key, no churn in the six existing entries). Order is not a budget lever, because every missing marketplace add runs before any install (`:271-284`). No test pins the order; T1 must not assert key order.

### 3.1a Open Decision: ledger default
<!-- Source: Orchestrator instruction on invariant-probe.md INV-001 — merged per Change #8 (new subsection; OPEN DECISION, both outcomes kept, none picked) -->

**Status: PENDING coordinator decision. The implementer must not pick.**

- **Outcome 1, ledger off by default**: the defaults file gains `pluginConfigs["ponytail@ponytail"].options.ledger = false`. The top-level `pluginConfigs` key is filled only when the user's settings lack it (it is not in `_NESTED_KEYS`, so `apply_settings_defaults` copies it whole or not at all, `install_user_setup.py:36,162-164`), so a user value is never changed. T1 asserts the entry. Docs and CHANGELOG say the ledger ships off and how to turn it back on. M1c records whether a ledger row appears (UNVERIFIED until then). Under this outcome only, the defaults change is four entries, not three (FR-001..FR-003, NFR-006).
- **Outcome 2, Ponytail's default (ledger on)**: no defaults entry. Docs and CHANGELOG say the ledger is on and that the `ledger` userConfig option turns it off.
- The `off` footprint wording (Interaction, "`off` footprint") holds for both outcomes; only the default sentence differs.

### 3.2 Python (`src/superclaude/cli/install_user_setup.py`, the only change)
<!-- Source: Base (original) -->

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
<!-- Source: Variant A (opus:architect), Decision Summary rejected alternatives (A:21) + Base 3.3 (B:96-98) — merged per Change #4; (d) path per Change #10 -->

- (a) A dedicated `install_ponytail()` step: duplicates `install_plugins` (marketplace add, installed check, deadline handling) for no behavioural gain, and adds a fourth place to keep in sync with the defaults file.
- (b) Ponytail's own default `full`: changes every session, every subagent and every prompt on every workspace, doubles the ladder Pragmatic already carries, and fires the statusline nudge on every new workspace.
- (c) Installed but disabled: hides the skills, so #330 stays open.
- (d) The installer writes Ponytail's `config.json` (`$XDG_CONFIG_HOME/ponytail/config.json`, or `~/.config/ponytail/config.json` when `XDG_CONFIG_HOME` is unset) instead of an `env` key: needs Ponytail's private path resolution (`XDG_CONFIG_HOME`, Windows `APPDATA`, upstream `ponytail-config.js`), new Python, and a new write outside `~/.claude`. See Risks R2 for what the env route costs. If M1b fails, this file becomes a documented user step, never an installer write (AC-M1).
- (e) A `node` pre-check in `install_plugins`: no existing plugin has a prerequisite check, so this would be a new concept; IronClaude's own SubagentStart hook `pragmatic-subagent.js` already needs `node` (`install_hooks.py:66-68`). Deferred.
- (f) Reordering plugins for budget priority: every missing marketplace add runs before any install, so order protects nothing (3.1, "Order").
- (g) A merge-blocking env-propagation gate: settings `env` reaching spawned subprocesses is documented and observed (`enrichment/env-propagation-evidence.md:9`), so the manual checks are non-blocking (AC-M1).


## Interaction with IronClaude behaviour
<!-- Source: Base (original, modified) — UserPromptSubmit row: Variant A, Interaction table (A:83) per Change #6; Band row and "off footprint" per Change #7 (INV-001); Pragmatic ladder per Change #9 (INV-002); Orca workers bullet: Variant A (A:82) per Change #5; Environment bullet per Change #18 -->
What Ponytail does, read from upstream source today (v5.3.3):

| Component | In `full`/`lite`/`ultra` | In `off` |
|---|---|---|
| SessionStart `ponytail-activate.js` | Writes flag, emits ruleset, codebase map (3 s cap), and once a statusline-setup nudge ending "Proactively offer to fix this for the user on first interaction" when `settings.statusLine` is unset | `clearMode()` then `process.exit(0)`: nothing emitted |
| SubagentStart `ponytail-subagent.js` | Injects the ruleset into every subagent | Exits when mode is absent or `off` |
| UserPromptSubmit `ponytail-mode-tracker.js` | On Claude Code, emits only for `/ponytail ...` commands and deactivation phrases ('stop ponytail', 'normal mode'); per-prompt ruleset re-injection is Qoder-only. No phrase switches the mode on | Injects only for `/ponytail ...` commands |
| Band (`claude-band.json` -> `band/register.tsx`) and ledger CSV | Runs | Runs: the module never checks the level (`readLevel` only labels the band, upstream `band/register.tsx:95-103`). It draws the band unless `~/.claude/.ponytail-band` holds `off` (`:86-91`), runs `git grep` over the repo at session start (`:201-222`), hooks every Edit and Write (`:254-290`), and after every turn writes the ledger row unless the `ledger` option is `false` (`:154-163`, `:292-349`) |

**`off` footprint.** In `off`, Ponytail injects no ruleset, codebase map, statusline offer or subagent context. Its band module still runs in every session, Orca workers included: it draws a band above the prompt, runs `git grep` over the repo at session start, watches every Edit and Write, and after every turn writes a ledger row (`$XDG_CONFIG_HOME/ponytail/band/<project>.csv` when that variable is set, else `~/.config/ponytail/band/<project>.csv`; local only, webhook empty by default). Two controls exist: `/ponytail band off` hides the band (it writes `~/.claude/.ponytail-band`; the `git grep`, the Edit/Write watch and the ledger keep running), and Ponytail's `ledger` userConfig option (`false` stops the CSV row). The IronClaude default for the ledger is the open decision in 3.1a.

Interactions, each with the position taken:

- **Pragmatic ladder** (`pragmatic.md:136-152`, "Stop at the first rung..."): same doctrine as Ponytail's. Running both at `full` states it twice per session and per subagent with different wording, which can conflict on edge cases. In `off` there is one authority: Pragmatic. A user who wants Ponytail's rules on can switch them on with `/ponytail <level>` or persistently (see Opt-out). `/ponytail <level>` switches the mode for every session in that repo, not only the current one (upstream `ponytail-runtime.js:46-66`). Any new session that starts in `off` in that repo (an Orca worker, a resume, `/clear`) switches it back off (`ponytail-activate.js:31-35`). While a level is on, every subagent of every session in the repo gets the ruleset. Bare `/ponytail` switches to `full` (`ponytail-mode-tracker.js:110-118`).
- **Statusline nudge**: the installer never sets `statusLine` (grep of `src/superclaude` finds no `statusLine`), so every fresh workspace would trigger the nudge in a non-`off` mode, and an unattended Orca worker would be told to raise it with a user who is not there. `off` removes it. Rejected: setting `statusLine` ourselves (new settings scope, not asked).
- **Freshness / Edit hooks and rules**: Ponytail registers only SessionStart, SubagentStart and UserPromptSubmit (`hooks/claude-codex-hooks.json`), none on tool use, so it cannot block or reorder Edit-time checks. IronClaude's freshness check is a PreToolUse Edit hook (observed this session: `PreToolUse:Edit hook error: [~/.claude/hooks/freshness-pre-edit.sh]`), a different event, so the two do not touch.
- **`/sc:implement`**: must not depend on Ponytail. The design note recorded in the enrichment (`.dev/tasks/to-do/TASK-WF-mergedOutput-20261024-165151/source.md:208-224`, not re-read here) says it embeds the fix-cost lens and never calls `ponytail-review`. This spec adds no reference to Ponytail in any primitive (FR-008). The only other `src/superclaude` hits for "ponytail" are `sc-pr-submit-protocol/scripts/*.sh` and `sc-implement-protocol/refs/qa.md`; their content was not read, UNVERIFIED, and they are untouched.
- **Orca workers / subagents**: IronClaude already injects two blocks into every subagent (`freshness-subagent-start.sh` and `pragmatic-subagent.js`, `src/superclaude/hooks/hooks.json:110-128`); a non-`off` mode would add a third to every Orca worker and `/sc:*` subagent. In `off` there is zero per-subagent injection; the three hooks still start a `node` process per event (cost UNVERIFIED, each has a 15 s timeout upstream).
- **Environment**: settings `env` reaching spawned subprocesses is documented and observed (`enrichment/env-propagation-evidence.md`); a plugin-hook-specific run is M1b under AC-M1 (non-blocking, and counted only when M1c passes).


## Failure Behaviour
<!-- Source: Base (original, modified) — budget row and clone-size paragraph per Change #2; `node` row and two new rows: Variant A, Failure Behaviour (A:103-104) per Change #13; "No claude CLI" row per Change #15; Offline row clarified in post-merge validation -->
All cases go through code that exists today; none gets new handling.

| Case | Behaviour (verified in `install_plugins`) | Result |
|---|---|---|
| No `claude` CLI | `shutil.which("claude")` is `None` -> `⏭️  Plugins: claude CLI not found; skipped` (`:256-258`). Settings entries are already written by the earlier defaults step, so a later install with `claude` present installs it. Pinned by T5c. | `ok=True` |
| Offline | `claude plugin marketplace add DietrichGebert/ponytail` returns non-zero; the install command also fails. After the FR-005 fix both are reported by name (repo and plugin id); today the failed install is reported as `--scope` (`:303`) | `ok=True`, `⚠️  Plugins: not installed: ...; rerun superclaude install to retry` |
| 30 s shared budget spent | Each command checks `remaining < 2` and is listed as `(time limit)` (`:290-293`); each run is also capped by `timeout=remaining` (`:299`). Orca runs first and may use up to 25 s (`_ORCA_TIMEOUT`, `:34`). | `ok=True`, a rerun resumes where it stopped while some run leaves budget, because installed plugins are skipped (`:283`) |
| `node` missing | Not checked by the installer. The plugin installs; its hooks call `node -e ...` (upstream `claude-codex-hooks.json`) and fail, even in `off`. IronClaude's own SubagentStart hook `pragmatic-subagent.js` already needs `node` (`install_hooks.py:66-68`), so such a workspace is already degraded. Upstream hooks force-exit within 1 s (`ponytail-activate.js:197-201`, `ponytail-mode-tracker.js:216`, `ponytail-subagent.js:94`); with the defaults' `"verbose": true` (`user_settings_defaults.json:6`) each failure shows an error. | Documented prerequisite; opt-out is `false` |
| Marketplace add fails but plugin install is attempted anyway | Existing behaviour (commands are appended unconditionally, `:277-284`); the install fails and is reported | unchanged |
| Malformed `settings.json` | `apply_settings_defaults` returns `ok=False` and leaves the file (`:147-148`); pre-existing, unchanged | unchanged |
| Enabled in settings but not installed (any failure above) | Same state the six existing plugins can already reach. Claude Code may install it in the background (`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`, `enrichment/assumption-evidence.md:19`); UNVERIFIED | unchanged; never fatal |
| Marketplace keyed other than `ponytail` in `known_marketplaces.json` | The add is re-queued on every run because the guard checks only the key (`:277-279`); when the add succeeds, the step still prints `✅ Plugins: installed ...` (`:306-311`) | `ok=True`; caught only by M1a |

Clone size: upstream repo `size` is 13130 KB (about 13 MB, `gh api repos/DietrichGebert/ponytail`, 2026-11-04); actual clone time on a Coder workspace is UNVERIFIED. The three clones plus up to seven installs share one 30 s budget; an earlier run shows the budget can be fully spent (`.dev/codegraph-migration/evidence/P2-layer2.md:358`, environment of that run unknown).


## Opt-out
<!-- Source: Base (original, modified) — item 2 per Change #9 (INV-002); item 3 per Change #7 (INV-001); item 4 path per Change #10 (INV-006); test range per Change #16 -->
No new opt-out mechanism. The documented ones:

1. **Do not want Ponytail at all**: set `"ponytail@ponytail": false` in `~/.claude/settings.json` `enabledPlugins`. `apply_settings_defaults` keeps a present key (`:159`) and `install_plugins` only installs entries that are `True` (`:266`). Do not delete the key (the next run re-adds `true`) and do not only run `claude plugin uninstall` (the next run reinstalls it).
2. **Want Ponytail's always-on rules**: set `env.PONYTAIL_DEFAULT_MODE` to `lite`, `full` or `ultra` in `settings.json`. To switch it on without changing the default, type `/ponytail <level>`: `/ponytail <level>` switches the mode for every session in that repo, not only the current one. Any new session that starts in `off` in that repo (an Orca worker, a resume, `/clear`) switches it back off. While a level is on, every subagent of every session in the repo gets the ruleset. Bare `/ponytail` switches to `full`.
3. **Want to stop the local ledger/band**: `/ponytail band off` hides the band (it writes `~/.claude/.ponytail-band`; the `git grep`, the Edit/Write watch and the ledger keep running). Ponytail's `ledger` userConfig option set to `false` stops the CSV row; the IronClaude default for it is the open decision in 3.1a. To stop the band module entirely, use opt-out 1.
4. The env default beats Ponytail's own `defaultMode` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json` when `XDG_CONFIG_HOME` is unset) (upstream resolution order: env, then file, then `full`; `ponytail-config.js`). So `/ponytail default full` is ignored while our `env` key is `off`. The docs must say this in one sentence (Risk R2).

The existing test pattern (`tests/cli/test_install_user_setup.py:73-98`) already proves a user `False` survives; T3/T4 below extends it to Ponytail and to the env key.


## Visibility (install --list / doctor)
<!-- Source: Base (original, modified) — plugin count removed in post-merge validation -->
Decision: neither command changes in this PR.

- `install --list` prints core, commands, agents, skills, templates, codegraph and retired MCP only (`main.py:86-172`). None of the six existing plugins appears; adding only Ponytail would be inconsistent, adding all of them is a feature.
- `doctor` runs pytest-plugin, agents, skills, configuration, ccsession, codegraph and retired-MCP checks (`doctor.py:27-49`); "plugin" there means the pytest plugin. `update.sh:10` runs `superclaude doctor`, so a new plugin check would also gate updates on network/CLI state, which contradicts "never fatal".
- The install summary line already names what happened: `✅ Plugins: installed ...` or the warning above. That is the visibility this issue needs.
- If wanted later: one backlog issue, "report default-plugin state in doctor (informational, never failing)", per `~/.claude/ISSUE-BACKLOG.md`.


## Docs and CHANGELOG
<!-- Source: Base (original, modified) — installation.md block: Base B:159-172 + Variant A docs paragraph (A:123) + Variant C (C:73,75) — merged per Change #11 (after Changes #7, #9, #10); CHANGELOG block per Change #12 -->
**`docs/getting-started/installation.md:353-360`** (read this session). Replace the count so it cannot drift again, and add one short block:

```text
`superclaude install` also installs the default Claude Code plugins listed in
its settings defaults (including `playwright`, `frontend-design` and `ponytail`)
with `claude plugin install <plugin> --scope user`, skipping any you disabled in
`enabledPlugins`. ... [unchanged budget/retry sentences] ...

`ponytail` (from `DietrichGebert/ponytail`) adds the `ponytail-*` skills and the
`/ponytail` command. It is installed with its always-on mode off:
`env.PONYTAIL_DEFAULT_MODE` is set to `off` unless you already set it. In `off`,
Ponytail injects no ruleset, codebase map, statusline offer or subagent context.
Its band module still runs in every session, Orca workers included: it draws a
band above the prompt, runs `git grep` over the repo at session start, watches
every Edit and Write, and after every turn writes a ledger row to
`$XDG_CONFIG_HOME/ponytail/band/<project>.csv` (or
`~/.config/ponytail/band/<project>.csv` when `XDG_CONFIG_HOME` is unset; local
only, webhook empty by default). `/ponytail band off` hides the band; the
`git grep`, the Edit/Write watch and the ledger keep running.
<LEDGER SENTENCE: per open decision 3.1a.
 Outcome 1: "IronClaude ships the ledger off (Ponytail's `ledger` option is set
 to `false`); set it to `true` to turn it back on."
 Outcome 2: "The ledger is on by default; set Ponytail's `ledger` option to
 `false` to stop it.">

`/ponytail <level>` switches the mode for every session in that repo, not only
the current one. Any new session that starts in `off` in that repo (an Orca
worker, a resume, `/clear`) switches it back off. While a level is on, every
subagent of every session in the repo gets the ruleset. Bare `/ponytail`
switches to `full`. To change your default, set `PONYTAIL_DEFAULT_MODE` to
`lite`, `full` or `ultra`. The variable overrides `/ponytail default <mode>`:
that command prints "PONYTAIL DEFAULT SET" but has no effect while the variable
is set.

To opt out, set `"ponytail@ponytail": false` in `enabledPlugins` in your user
settings (`~/.claude/settings.json`). A project `.claude/settings.json` that
enables it wins over your user value. Do not delete the key: the next install
adds it back as `true`.

Existing workspaces get Ponytail only after the IronClaude package itself is
upgraded: upgrade the package the way you installed it (for a checkout,
`git pull` before `./update.sh`, because `update.sh` reinstalls from the local
checkout), then run `superclaude update` or `superclaude install`.

Its hooks need `node` on your PATH; IronClaude's own SubagentStart hook already
needs it.

On a workspace where Orca's skill install uses the shared 30 s network budget on
every run, the installer may not reach the Ponytail install. Such a workspace
gets Ponytail on a later run that leaves budget, or through Claude Code's own
background install of enabled plugins (UNVERIFIED).
```

The ledger sentence is the only open text in this block; the implementer fills it once the coordinator decides 3.1a.

Also update the "Hook registrations and settings defaults" table row only if it lists plugins (it does not, `:345`), so no change there. `docs/testing/v5.0.0/post-release-manifest.json:28` says "default plugins" without a count: no change.

**`CHANGELOG.md`** (`[Unreleased]` is empty at `:5`; headings follow the `#### Changed (topic)` style used at `:13`):

```text
### Ponytail plugin installed by default (#330)

#### Added (default plugins)

- `superclaude install` and `superclaude update` (and `update.sh`) now install the Ponytail plugin (`ponytail@ponytail`, from `DietrichGebert/ponytail`; verified against upstream v5.3.3). It ships with `env.PONYTAIL_DEFAULT_MODE` set to `off` when you have not set it: its skills and `/ponytail` command are available, and it injects no ruleset, codebase map, statusline offer or subagent context. Its band module still runs in every session, Orca workers included: a band above the prompt, a `git grep` at session start, a watch on every Edit and Write, and a local per-turn ledger row under `$XDG_CONFIG_HOME/ponytail/band/` (or `~/.config/ponytail/band/`); `/ponytail band off` hides the band. <LEDGER SENTENCE per open decision 3.1a. Outcome 1: "The ledger ships off; set Ponytail's `ledger` option to `true` to turn it back on." Outcome 2: "The ledger is on; set Ponytail's `ledger` option to `false` to stop it."> Set `PONYTAIL_DEFAULT_MODE` to `lite`, `full` or `ultra` to turn the always-on mode on. To opt out, set `"ponytail@ponytail": false` in `enabledPlugins` in your user settings; do not delete the key, because the next install adds it back. Existing workspaces get Ponytail after you upgrade the IronClaude package, then run `superclaude update` or `superclaude install`. Needs `node` on the PATH.
- If you already use Ponytail with a default in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`), the new `PONYTAIL_DEFAULT_MODE=off` wins over it, and `/ponytail default <mode>` reports success but has no effect while that variable is set. Set `env.PONYTAIL_DEFAULT_MODE` to your preferred mode instead.

#### Fixed (plugin install report)

- A plugin that fails to install is now listed by its name in the `Plugins: not installed` warning (it printed `--scope`).
```


## Tests and Acceptance Criteria
<!-- Source: Base (original, modified) — T2 per Change #17; T3/T4 per Change #16 (INV-017); T5 per Change #14; T5c: Variant C (C R2 N1) per Change #15; AC-1 grep: Variant C (C:75) per Change #11; AC-M1 M1a/M1b/M1c per Change #18 (Variant A V-1 wording A:91, INV-009, INV-010, INV-029) -->
All in `tests/cli/test_install_user_setup.py` (helpers `_settings`, `_plugin_home`, `fake_run` pattern at `:15,175-209`). Run with `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py -v`.

| ID | Test | Proves |
|---|---|---|
| T1 | New `test_defaults_ship_ponytail`: load the defaults file; assert `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"] == {"source": "github", "repo": "DietrichGebert/ponytail"}`, `env["PONYTAIL_DEFAULT_MODE"] == "off"`; assert every `enabledPlugins` key's marketplace has a `source.repo` (guards every future add) | FR-001..003 |
| T2 | Extend `test_plugins_install_missing_enabled_defaults` (`:182-209`): assert `["plugin","marketplace","add","DietrichGebert/ponytail"]` in calls and `ponytail@ponytail` in installs. Both assertions go next to the existing assertions at `test_install_user_setup.py:205`; the test already iterates every default, so no fixture change | FR-002, FR-004 |
| T3/T4 | Extend `test_settings_defaults_fill_only_missing_values` (`:73-98`) with two legs (one fixture cannot both add a key and keep a user value for that same key). Leg 1 (existing user): settings hold the old six plugins and two marketplaces; after `apply_settings_defaults`, `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]` is present and `env["PONYTAIL_DEFAULT_MODE"] == "off"` (the three keys arrive), the rest is unchanged, and a second run returns `(True, "✅ Settings defaults: already present")`. Leg 2 (user choice kept): `enabledPlugins["ponytail@ponytail"] = False` and `env.PONYTAIL_DEFAULT_MODE = "full"` are unchanged after apply | FR-003, NFR-002, NFR-004, opt-out, existing users |
| T5 | Extend `test_plugin_failures_and_time_limit_never_fail_install` (`:229-242`) using its existing `playwright`-only fixture (the label logic is plugin-agnostic, so no Ponytail fixture). Non-zero-exit leg: `ok is True`; message contains `anthropics/claude-plugins-official` and `playwright@claude-plugins-official`; `"--scope" not in message`. `deadline=0` leg: `ok is True`; message contains `(time limit)` and the same two names; `"--scope" not in message`. Before the fix, both legs fail on `--scope` (`install_user_setup.py:292,303,305`); today's assertions (`:240,242`) pass either way | FR-005, NFR-001 |
| T5c | New `claude`-absent leg: monkeypatch `setup.shutil.which` to return `None`; assert `install_plugins(home=...) == (True, "⏭️  Plugins: claude CLI not found; skipped")` (two spaces after the emoji, as at `install_user_setup.py:258`). No test reaches this branch today: every plugin test patches `which` to `/bin/claude` (`:195,222,233`) | NFR-001 |
| T6 | `test_plugins_skip_already_installed` (`:212-226`) stays green unchanged | NFR-004 |

Update path coverage: `tests/cli/test_update_command.py:24-48,253-289` already stub and assert `install_user_setup` inside `update`; no new test, because `update.sh:8` and `main.py:404` are unchanged and T3/T4 leg 1 covers what `install_user_setup` does for an existing user.

Acceptance criteria:

- **AC-1** With T1..T5 and T5c green, `uv run pytest tests/cli tests/unit/test_cli_install.py` passes, `make lint` is clean, and `grep -rn "six plugins" docs/` returns nothing.
- **AC-2** `git diff --stat` touches only: `user_settings_defaults.json`, `install_user_setup.py` (at most 5 changed lines), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md`, `CHANGELOG.md`. No `update.sh`, `main.py`, `doctor.py`, output style, `.claude/` file.
- **AC-3** `grep -rn 'src/superclaude' ` on files changed adds no installed-primitive hit.
- **AC-M1 (manual, non-blocking)** Three checks, all in one throwaway `HOME` under `/tmp`, never this workspace's `~/.claude`, with network and the real `claude` CLI. Evidence is recorded in the PR. No check blocks the merge (`enrichment/env-propagation-evidence.md:9`).
  - **M1a (install mechanics; non-blocking)**: `~/.claude/plugins/installed_plugins.json` lists `ponytail@ponytail`; `~/.claude/plugins/known_marketplaces.json` has the key `ponytail`; a second `superclaude install` prints exactly `✅ Plugins: already installed` (a key mismatch otherwise hides behind `✅ Plugins: installed ...`); the install finishes with no prompt and no hang under closed stdin. Fail outcome: record the evidence in the PR and open a follow-up issue.
  - **M1b (env reaches the hook; non-blocking)**: with settings `env.PONYTAIL_DEFAULT_MODE = "off"`, a new session shows no Ponytail ruleset and `~/.claude/.ponytail-active` is absent. M1b counts as evidence only if M1c passed in the same HOME (absence alone also appears when the hook never runs). Fail outcome: document `{"defaultMode": "off"}` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json` when `XDG_CONFIG_HOME` is unset) as a user step in the docs, and open a follow-up issue. The installer never writes outside `~/.claude`.
  - **M1c (positive control; non-blocking)**: the plugin's skill files exist under the installed plugin directory in `~/.claude/plugins/`. If a Claude session can be started in that HOME: the `ponytail-*` skills are listed, `/ponytail lite` returns "PONYTAIL MODE CHANGED — level: lite" and `~/.claude/.ponytail-active` appears, then `/ponytail off` clears it. If a session cannot be started there, record M1c as UNVERIFIED in the PR (and M1b therefore as unconfirmed). If the open decision in 3.1a picks outcome 1, also record whether a ledger row is written.
- **AC-M2 (manual)** Set `enabledPlugins["ponytail@ponytail"]` to `false`, rerun install: no Ponytail command runs, the value stays `false`.
- **AC-M3 (manual)** Run install with `PATH` lacking `claude`: exit 0 and the skip line; with the network blocked: exit 0 and the named warning.


## Risks
<!-- Source: Base (original, modified) — R4 per Change #2; R6, R7 per Change #7; R1 path per Change #10; R1, R2 per Change #22; R10 per Change #20 (INV-024); R11 per Change #22 (INV-002); R3 impact aligned in post-merge validation -->
| ID | Risk | Prob. | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Our `env` default overrides a user's own `defaultMode` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json` when `XDG_CONFIG_HOME` is unset) (env has top priority upstream) for someone who already runs Ponytail; `/ponytail default <mode>` prints success but has no effect | Low | Low-Med (their always-on mode silently turns off) | CHANGELOG sentence (above); user fixes with one `env` line. Accepted over adding config-file code |
| R2 | `/ponytail default <mode>` writes `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json` when `XDG_CONFIG_HOME` is unset) and prints "PONYTAIL DEFAULT SET", but has no effect while the env key is set | Med (among Ponytail users) | Low | One docs sentence; in-session `/ponytail <level>` works; fix is editing the env key |
| R3 | `node` absent: hooks fail on each SessionStart, SubagentStart and prompt, even in `off` | Low-Med | Med (noise: an error per hook run, see the Failure Behaviour `node` row) | Docs prerequisite; opt-out `false`; follow-up for a prerequisite check if seen in practice |
| R4 | The 30 s shared budget can starve any install on a fresh workspace: Ponytail's 13 MB clone runs ahead of all six installs. A rerun usually resumes, but not while Orca uses the budget on every run (see Known Limitations and Follow-ups) | Med | Low (reported by name; a rerun resumes while some run leaves budget) | FR-005 naming; documented rerun; Coder Handoff question 3 |
| R5 | Unpinned third-party code runs three hooks every session; upstream `main` can change (v5.3.1-v5.3.3 shipped in Oct 2026) | Low | High | Same trust model as `understand-anything`; only `DietrichGebert/ponytail` allowed (seed constraint); `off` removes rules injection but not code execution; pinning syntax for `claude plugin install` UNVERIFIED, so none proposed |
| R6 | Ponytail's band module runs in every session even in `off`, Orca workers included: a band above the prompt, `git grep` over the repo at session start, a watch on every Edit and Write, and a per-turn ledger row (`$XDG_CONFIG_HOME/ponytail/band/<project>.csv`, or `~/.config/ponytail/band/<project>.csv` when `XDG_CONFIG_HOME` is unset; local, webhook empty by default). Upstream `band/register.tsx` never checks the level | High | Low | Documented in docs and CHANGELOG; `/ponytail band off` hides the band only; the `ledger` userConfig option `false` stops the CSV row (IronClaude default: open decision 3.1a); opt-out 1 stops all of it |
| R7 | Users read "installed but does nothing" as broken | Med | Low | Docs and CHANGELOG say `off` is deliberate, name what `off` still does (the band module), and give the one-line switch |
| R8 | Message-text change (FR-005) breaks a consumer that parses `--scope` | Very low | Low | Repo grep found only the evidence log `.dev/codegraph-migration/evidence/P2-layer2.md`, not code |
| R9 | `PONYTAIL_DEFAULT_MODE=off` value stops being valid upstream | Very low | Low | `off` is a runtime mode in `RUNTIME_MODES` (`ponytail-config.js`); an unknown value falls through to `full`, so a future rename degrades to Ponytail's default, which T1 does not catch; re-check on upstream major bumps |
| R10 | Claude Code installs enabled plugins in the background (`enrichment/assumption-evidence.md:19`), so a session started during workspace boot may clone the same marketplace while the installer does (a race), or may rescue a starved install. Both effects are UNVERIFIED | Low | Low | Never fatal; M1a observes the installer path only |
| R11 | A user switches Ponytail on in one session; another session or Orca worker starting in that repo switches it back off, or the ruleset reaches every subagent in that repo while on | Med (among opt-in users) | Low | The per-repo mode sentence in the docs block and Opt-out item 2 |


## Known Limitations and Follow-ups
<!-- Source: Round 2 consensus (A R2 N4, B R2 Final X-005, C R2 N3) + invariant-probe.md INV-028 orchestrator decision — merged per Change #20 (new section) -->

**Limitation** (verbatim in the docs block and in the PR description): "On a workspace where Orca's skill install uses the shared 30 s network budget on every run, the installer may not reach the Ponytail install. Such a workspace gets Ponytail on a later run that leaves budget, or through Claude Code's own background install of enabled plugins (UNVERIFIED)." Out of scope for this PR.

**Mechanism** (spec only): `_find_orca` probes with a fixed `timeout=10` that ignores the deadline (`install_user_setup.py:190`), then the Orca install gets up to 25 s (`:226`, `_ORCA_TIMEOUT` at `:34`) of a 30 s budget (`:35`), and it retries on every run while an Orca skill is missing (`:213-215`). Orca hit the 25 s limit in both logged runs (`.dev/codegraph-migration/evidence/P2-layer2.md:357,623`).

**Follow-ups** (each a backlog issue from `~/.claude/ISSUE-BACKLOG.md`):

1. Bound the Orca probe by the deadline, or give plugins their own budget.
2. If M1b fails, the `config.json` user-step follow-up (AC-M1).
3. If M1a fails, its follow-up (AC-M1).
4. Report default-plugin state in `doctor`, informational only (Visibility).
5. The ledger default, if the coordinator defers the open decision in 3.1a.


## Out of Scope
<!-- Source: Base (original, modified) — config.json path per Change #10; userConfig exception per Change #8 -->
- Any edit to `update.sh`, `main.py` (`update()`, `install --list`, the install banner at `:233` that omits "plugins"), `doctor.py`.
- A `node` or `claude`-version prerequisite check, a per-plugin "requires" table, version pinning, or a generic plugin framework.
- Reordering or prioritising plugins under the 30 s budget; changing `_NETWORK_BUDGET` or `_ORCA_TIMEOUT`.
- Setting `statusLine`, writing Ponytail's `config.json` (`$XDG_CONFIG_HOME/ponytail/` or `~/.config/ponytail/`), or setting plugin `userConfig` (ledger, webhook), except the ledger default if the open decision in 3.1a picks outcome 1.
- Reworking the Pragmatic ladder, adding Ponytail references to any skill, command or agent, or making `/sc:implement` call `ponytail-review`.
- Any edit in the Coder repo; any run of `superclaude install/update`, `update.sh` or `claude plugin` against the real `~/.claude`.
- Plugin state in `doctor` / `install --list` (backlog candidate).


## Coder Handoff (confirmation only; no Coder repo edits, no Orca link flags)
<!-- Source: Base Coder Handoff (B:239-246) + Variant C (haiku:qa), Coder Handoff (C:114) — merged per Change #19 (INV-027 decision: keep Closes #330) -->
A handoff is needed only as a confirmation, not as a Coder change. The Coder repo was not read (UNVERIFIED); `install_user_setup.py:31-33` records that `superclaude install` runs under a 60 s limit in Coder workspaces, which is why the budget exists. This PR reaches a workspace only when `superclaude install` or `update` runs in it, so "all workspaces" holds only if the template does that. The PR description carries a one-paragraph summary of this section for the Coder owner (no file in the Coder repo, no Orca link flags). Questions:

1. Does the template run `superclaude install` (or `update`) on workspace create and on refresh? If a template pre-writes `~/.claude/settings.json` with its own `enabledPlugins`, entries it omits are still filled (nested fill), but a template that pins `PONYTAIL_DEFAULT_MODE` or sets `"ponytail@ponytail": false` wins by design.
2. Are the `claude` CLI and `node` on PATH before that step runs? Without `claude` the plugin is skipped; without `node` the hooks fail (R3).
3. Is there headroom in the 60 s limit for one more marketplace clone inside the existing 30 s network budget (R4), given the Orca budget limitation in Known Limitations and Follow-ups? If not, the owner can raise the limit or accept a second `superclaude install` run.
4. Does the template install `superclaude` from the fork at its current version rather than a pinned older one? Existing workspaces get Ponytail only after a package upgrade.

No answer blocks this PR. The PR keeps `Closes #330`. If answer 1, 2 or 4 is "no", file a handoff issue from `~/.claude/ISSUE-HANDOFF.md`.

