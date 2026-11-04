# Manual install proof (issue #330, Task 4; non-blocking)

Run: 2026-11-04, Claude Code 2.1.318, worktree venv python. Script: a throwaway-HOME driver (`mktemp -d /tmp/ponytail-home*`, removed on exit by a trap). Every step ran under
`env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME -u PONYTAIL_DEFAULT_MODE -u PONYTAIL_MAP -u PONYTAIL_SUBAGENT_MATCHER` (plus the parent session's messaging/session variables) `HOME=<throwaway>`.
Scope note: the proof drives the installer's settings-defaults and plugin steps (`apply_settings_defaults`, then `install_plugins` with the 30 s budget), not the whole `superclaude install`, so the Orca skills step (Orca was on PATH) did not run and did not use budget; its time is therefore 0 here.

| Check | Result | Evidence (log lines below) |
|---|---|---|
| Isolation: no CLAUDE_CONFIG_DIR / XDG_CONFIG_HOME / PONYTAIL_* inside | PASS | "isolation check ... (end)" with no lines |
| M1a install: `installed_plugins.json` lists `ponytail@ponytail`; `known_marketplaces.json` has key `ponytail` | PASS | "installed ponytail@ponytail: True" (version 5.3.3, gitCommitSha 96608e07); "known marketplace key ponytail: True"; first run installed all seven defaults in 18.7 s of the 30 s budget |
| M1a second run prints exactly `✅ Plugins: already installed` | PASS | runs 2 and 3 |
| M1a no prompt / no hang under closed stdin | PASS | every run returned (stdin is DEVNULL in `install_plugins`) |
| M1c skill files under the installed plugin directory | PASS | second throwaway run: `cache/ponytail/ponytail/5.3.3/skills/{ponytail,ponytail-audit,ponytail-debt,ponytail-gain,ponytail-help,ponytail-review}/SKILL.md` |
| M1b (lite): a new session shows the ruleset at level lite; `~/.claude/.ponytail-active` holds `lite` | PASS | `claude -p` in a throwaway git repo answered that its context holds `PONYTAIL MODE ACTIVE — level: lite`; `.ponytail-active: lite` |
| Statusline note (lite, no statusLine set) | observed | the same session reported a `STATUSLINE SETUP NEEDED` line; `.ponytail-statusline-nudged` present; `ponytail-statusline.sh` copied |
| Ledger on by default | observed | `~/.config/ponytail/band/proj.csv` and `board.html` written in the throwaway HOME |
| AC-M2: `"ponytail@ponytail": false` → no Ponytail command runs, value stays `false` | PASS | fake `claude` logged 0 ponytail commands; "value kept: False" |
| AC-M3: no `claude` on PATH → exit 0 and the skip line | PASS | `(True, '⏭️  Plugins: claude CLI not found; skipped')`, rc=0 |
| Real `~/.claude` untouched | PASS | settings.json, installed_plugins.json, known_marketplaces.json hashes identical before/after; real `.ponytail-active` absent |
| Throwaway HOMEs removed | PASS | "cleanup done ... removed" |

Side observation (not part of #330): in a fresh HOME with the IronClaude defaults, `claude -p` printed `[claude-code:unrecognized_model] {"model":"gpt-6.1-sol"}`, from the defaults' `modelSettings` keys; harmless here.

Note on the first log's M1c listing: its `find -path '*ponytail*'` matched every file because the throwaway directory name contains "ponytail", so it listed dropbox skills; the second run lists Ponytail's own skill files.

## Log 1 (full proof)

```text
== real ~/.claude before
5711b646dfb93d13 /home/coder/.claude/settings.json
55a39037ff3fcc56 /home/coder/.claude/plugins/installed_plugins.json
6805f6e8293b74a2 /home/coder/.claude/plugins/known_marketplaces.json
real .ponytail-active absent
== isolation check inside the throwaway env (expect no lines)
(end)
== orca on PATH: /home/coder/.config/orca/linux-orca-cli-shim/orca (the Orca skills step is not run; only the plugin step)
== claude 2.1.318 (Claude Code)
== M1a run 1 (shared 30 s budget, as superclaude install uses)
defaults: ✅ Settings defaults: added 25 (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, env.CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, env.PONYTAIL_DEFAULT_MODE, modelSettings.gpt-6-astra, modelSettings.gpt-6.1-sol, modelSettings.gpt-6-sol, modelSettings.gpt-5.6-sol, enabledPlugins.frontend-design@claude-plugins-official, enabledPlugins.playwright@claude-plugins-official, enabledPlugins.notion@claude-plugins-official, enabledPlugins.dropbox@claude-plugins-official, enabledPlugins.google-cloud-storage@claude-plugins-official, enabledPlugins.understand-anything@understand-anything, enabledPlugins.ponytail@ponytail, extraKnownMarketplaces.claude-plugins-official, extraKnownMarketplaces.understand-anything, extraKnownMarketplaces.ponytail)
plugins: (True, '✅ Plugins: installed frontend-design@claude-plugins-official, playwright@claude-plugins-official, notion@claude-plugins-official, dropbox@claude-plugins-official, google-cloud-storage@claude-plugins-official, understand-anything@understand-anything, ponytail@ponytail') elapsed=18.7s budget=30.0s
== M1a run 2 (30 s)
defaults: ✅ Settings defaults: already present
plugins: (True, '✅ Plugins: already installed') elapsed=0.0s budget=30.0s
== M1a run 3 (30 s; expect already installed)
defaults: ✅ Settings defaults: already present
plugins: (True, '✅ Plugins: already installed') elapsed=0.0s budget=30.0s
== M1a records
installed ponytail@ponytail: True [{"scope": "user", "installPath": "/tmp/ponytail-home.AlWvBt/.claude/plugins/cache/ponytail/ponytail/5.3.3", "version": "5.3.3", "installedAt": "2026-11-04T13:41:05.325Z", "lastUpdated": "2026-11-04T13:41:05.325Z", "gitCommitSha": "96608e078b2d5ea607c5c3b8b5a54d1c1fba6846"}]
known marketplace key ponytail: True
== settings env/enabled in throwaway HOME
lite True
== M1c skill files
$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/clean-up-dropbox-content/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/collect-files-with-request/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/find-dropbox-content/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/inspect-dropbox-file/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/organize-dropbox-folder/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/share-dropbox-content/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/clean-up-dropbox-content/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/collect-files-with-request/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/find-dropbox-content/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/inspect-dropbox-file/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/organize-dropbox-folder/SKILL.md
$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/share-dropbox-content/SKILL.md
== M1b session in a throwaway git repo (claude -p, lite expected)
[claude-code:unrecognized_model] {"model":"gpt-6.1-sol","query_source":"sdk"}
1) No. The line is `SessionStart:startup hook success: PONYTAIL MODE ACTIVE — level: lite`, which has a prefix.
2) Yes.
rc=0
.ponytail-active: lite
.ponytail-statusline-nudged: present
ponytail-statusline.sh copied: yes
ledger csv: board.html
proj.csv
== AC-M2 (opt-out kept): fresh HOME with ponytail false, fake claude logging commands
defaults: ✅ Settings defaults: added 24 (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, env.CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, env.PONYTAIL_DEFAULT_MODE, modelSettings.gpt-6-astra, modelSettings.gpt-6.1-sol, modelSettings.gpt-6-sol, modelSettings.gpt-5.6-sol, enabledPlugins.frontend-design@claude-plugins-official, enabledPlugins.playwright@claude-plugins-official, enabledPlugins.notion@claude-plugins-official, enabledPlugins.dropbox@claude-plugins-official, enabledPlugins.google-cloud-storage@claude-plugins-official, enabledPlugins.understand-anything@understand-anything, extraKnownMarketplaces.claude-plugins-official, extraKnownMarketplaces.understand-anything, extraKnownMarketplaces.ponytail)
plugins: (True, '✅ Plugins: installed frontend-design@claude-plugins-official, playwright@claude-plugins-official, notion@claude-plugins-official, dropbox@claude-plugins-official, google-cloud-storage@claude-plugins-official, understand-anything@understand-anything') elapsed=0.0s budget=30.0s
ponytail commands run: 0
0
value kept: False
== AC-M3 (no claude on PATH)
defaults: ✅ Settings defaults: added 25 (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, env.CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, env.PONYTAIL_DEFAULT_MODE, modelSettings.gpt-6-astra, modelSettings.gpt-6.1-sol, modelSettings.gpt-6-sol, modelSettings.gpt-5.6-sol, enabledPlugins.frontend-design@claude-plugins-official, enabledPlugins.playwright@claude-plugins-official, enabledPlugins.notion@claude-plugins-official, enabledPlugins.dropbox@claude-plugins-official, enabledPlugins.google-cloud-storage@claude-plugins-official, enabledPlugins.understand-anything@understand-anything, enabledPlugins.ponytail@ponytail, extraKnownMarketplaces.claude-plugins-official, extraKnownMarketplaces.understand-anything, extraKnownMarketplaces.ponytail)
plugins: (True, '⏭️  Plugins: claude CLI not found; skipped') elapsed=0.0s budget=30.0s
rc=0
== real ~/.claude after
5711b646dfb93d13 /home/coder/.claude/settings.json
55a39037ff3fcc56 /home/coder/.claude/plugins/installed_plugins.json
6805f6e8293b74a2 /home/coder/.claude/plugins/known_marketplaces.json
real .ponytail-active absent
cleanup done: /tmp/ponytail-home.AlWvBt /tmp/ponytail-home2.VVJqpe /tmp/ponytail-home3.5hbbkC removed
```

## Log 2 (Ponytail-only reinstall to list skill files)

```text
(True, '✅ Plugins: installed ponytail@ponytail')
./5.3.3/.openclaw/skills/ponytail-audit/SKILL.md
./5.3.3/.openclaw/skills/ponytail-debt/SKILL.md
./5.3.3/.openclaw/skills/ponytail-gain/SKILL.md
./5.3.3/.openclaw/skills/ponytail-help/SKILL.md
./5.3.3/.openclaw/skills/ponytail-review/SKILL.md
./5.3.3/.openclaw/skills/ponytail/SKILL.md
./5.3.3/skills/ponytail-audit/SKILL.md
./5.3.3/skills/ponytail-debt/SKILL.md
./5.3.3/skills/ponytail-gain/SKILL.md
./5.3.3/skills/ponytail-help/SKILL.md
./5.3.3/skills/ponytail-review/SKILL.md
./5.3.3/skills/ponytail/SKILL.md
removed /tmp/pt-skills.RBVTrz
```
