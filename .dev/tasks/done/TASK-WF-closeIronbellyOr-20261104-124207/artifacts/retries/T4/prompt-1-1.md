68b48ccb40439194b11344ce2cb7c162dd96fc5e
Review one task for spec compliance.

Task brief: ## Task 4: Add the `[Unreleased]` entry for #330 to `CHANGELOG.md`

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

AC ids: T4.AC1,T4.AC2,T4.AC3,T4.AC4 (in the order of the Acceptance criteria bullets)
Global constraints: ## Constraints

- Change only `src/superclaude/cli/user_settings_defaults.json`, `src/superclaude/cli/install_user_setup.py` (at most 5 changed lines, failure label only), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md` and `CHANGELOG.md`. No change to `main.py`, `update.sh`, `doctor.py`, output styles, rules, hooks, any skill, command or agent, or any `.claude/` file.
- Never run `superclaude install`, `superclaude update`, `./update.sh` or `claude plugin ...` against this workspace's `~/.claude`; any manual proof uses a throwaway `HOME` under `/tmp` that is removed afterwards.
- No `pluginConfigs` entry, no `statusLine` setting, no write outside `~/.claude`, no version pin, no new module, constant, flag or CLI option.
- A user's existing `enabledPlugins`, `env` and marketplace values are never changed.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); never stage `.claude/` paths.
- The superseded package `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/` and `.dev/reflect/pre-closeIronbellyOr-20261104084538/` stay on disk untouched.
Start sha: 68b48ccb40439194b11344ce2cb7c162dd96fc5e
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index e18e86ad..a3dcb564 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,17 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### Ponytail plugin installed by default (#330)
+
+#### Added (default plugins)
+
+- `superclaude install`, `superclaude update` and `update.sh` now install the Ponytail plugin (`ponytail@ponytail`, from `DietrichGebert/ponytail`; checked against upstream v5.3.3) and set `PONYTAIL_DEFAULT_MODE` to `lite` under `env` in `~/.claude/settings.json` when you have not set it. In `lite`, every session start injects Ponytail's rules at the lite level ("Build what was asked. Name the smaller option in one line and let the user pick.") plus a short codebase map, and every subagent gets the same rules. On a workspace whose user settings have no `statusLine`, the first session gets a one-time note asking Claude to offer to set up Ponytail's statusline badge; that session can be an unattended Orca worker, which then sees the note and may mention the offer. Ponytail's band module runs in every mode (a band above the prompt, a `git grep` at session start, a watch on every Edit and Write, and a local per-turn ledger row under `$XDG_CONFIG_HOME/ponytail/band/` or `~/.config/ponytail/band/`). The ledger is on; set Ponytail's `ledger` option to `false` to stop it. Change the mode with `/ponytail off|lite|full|ultra` for the current project, or set `PONYTAIL_DEFAULT_MODE` to `off`, `lite`, `full` or `ultra` to change the default. To opt out, set `"ponytail@ponytail": false` in `enabledPlugins` in your user settings; do not delete the key, because the next install adds it back. Existing workspaces get Ponytail after you upgrade the IronClaude package, then run `superclaude update` or `superclaude install`. Needs `node` on the PATH. See [the installation guide](docs/getting-started/installation.md).
+- If you already use Ponytail with a `defaultMode` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`), the new `PONYTAIL_DEFAULT_MODE=lite` wins over it, and `/ponytail default <mode>` has no effect while that variable is set. Set `PONYTAIL_DEFAULT_MODE` under `env` to your preferred mode instead.
+
+#### Fixed (plugin install report)
+
+- A plugin that fails to install is now listed by its name in the `Plugins: not installed` warning (it printed `--scope`).
+
 ## [5.0.0] - 2026-11-02
 
 Major release: codegraph replaces codebase-memory-mcp and Serena, and several commands, flags and core files are removed. Read the [5.0.0 release notes](docs/releases/v5.0.0.md) for the breaking changes and upgrade steps. This is the first versioned section of this changelog; it covers every change since the package version was set to 4.3.5 (2026-06-04), which was never tagged.
diff --git a/.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/m1-install-proof.md b/.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/m1-install-proof.md
new file mode 100644
index 00000000..06e40a2a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/m1-install-proof.md
@@ -0,0 +1,110 @@
+# Manual install proof (issue #330, Task 4; non-blocking)
+
+Run: 2026-11-04, Claude Code 2.1.318, worktree venv python. Script: a throwaway-HOME driver (`mktemp -d /tmp/ponytail-home*`, removed on exit by a trap). Every step ran under
+`env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME -u PONYTAIL_DEFAULT_MODE -u PONYTAIL_MAP -u PONYTAIL_SUBAGENT_MATCHER` (plus the parent session's messaging/session variables) `HOME=<throwaway>`.
+Scope note: the proof drives the installer's settings-defaults and plugin steps (`apply_settings_defaults`, then `install_plugins` with the 30 s budget), not the whole `superclaude install`, so the Orca skills step (Orca was on PATH) did not run and did not use budget; its time is therefore 0 here.
+
+| Check | Result | Evidence (log lines below) |
+|---|---|---|
+| Isolation: no CLAUDE_CONFIG_DIR / XDG_CONFIG_HOME / PONYTAIL_* inside | PASS | "isolation check ... (end)" with no lines |
+| M1a install: `installed_plugins.json` lists `ponytail@ponytail`; `known_marketplaces.json` has key `ponytail` | PASS | "installed ponytail@ponytail: True" (version 5.3.3, gitCommitSha 96608e07); "known marketplace key ponytail: True"; first run installed all seven defaults in 18.7 s of the 30 s budget |
+| M1a second run prints exactly `✅ Plugins: already installed` | PASS | runs 2 and 3 |
+| M1a no prompt / no hang under closed stdin | PASS | every run returned (stdin is DEVNULL in `install_plugins`) |
+| M1c skill files under the installed plugin directory | PASS | second throwaway run: `cache/ponytail/ponytail/5.3.3/skills/{ponytail,ponytail-audit,ponytail-debt,ponytail-gain,ponytail-help,ponytail-review}/SKILL.md` |
+| M1b (lite): a new session shows the ruleset at level lite; `~/.claude/.ponytail-active` holds `lite` | PASS | `claude -p` in a throwaway git repo answered that its context holds `PONYTAIL MODE ACTIVE — level: lite`; `.ponytail-active: lite` |
+| Statusline note (lite, no statusLine set) | observed | the same session reported a `STATUSLINE SETUP NEEDED` line; `.ponytail-statusline-nudged` present; `ponytail-statusline.sh` copied |
+| Ledger on by default | observed | `~/.config/ponytail/band/proj.csv` and `board.html` written in the throwaway HOME |
+| AC-M2: `"ponytail@ponytail": false` → no Ponytail command runs, value stays `false` | PASS | fake `claude` logged 0 ponytail commands; "value kept: False" |
+| AC-M3: no `claude` on PATH → exit 0 and the skip line | PASS | `(True, '⏭️  Plugins: claude CLI not found; skipped')`, rc=0 |
+| Real `~/.claude` untouched | PASS | settings.json, installed_plugins.json, known_marketplaces.json hashes identical before/after; real `.ponytail-active` absent |
+| Throwaway HOMEs removed | PASS | "cleanup done ... removed" |
+
+Side observation (not part of #330): in a fresh HOME with the IronClaude defaults, `claude -p` printed `[claude-code:unrecognized_model] {"model":"gpt-6.1-sol"}`, from the defaults' `modelSettings` keys; harmless here.
+
+Note on the first log's M1c listing: its `find -path '*ponytail*'` matched every file because the throwaway directory name contains "ponytail", so it listed dropbox skills; the second run lists Ponytail's own skill files.
+
+## Log 1 (full proof)
+
+```text
+== real ~/.claude before
+5711b646dfb93d13 /home/coder/.claude/settings.json
+55a39037ff3fcc56 /home/coder/.claude/plugins/installed_plugins.json
+6805f6e8293b74a2 /home/coder/.claude/plugins/known_marketplaces.json
+real .ponytail-active absent
+== isolation check inside the throwaway env (expect no lines)
+(end)
+== orca on PATH: /home/coder/.config/orca/linux-orca-cli-shim/orca (the Orca skills step is not run; only the plugin step)
+== claude 2.1.318 (Claude Code)
+== M1a run 1 (shared 30 s budget, as superclaude install uses)
+defaults: ✅ Settings defaults: added 25 (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, env.CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, env.PONYTAIL_DEFAULT_MODE, modelSettings.gpt-6-astra, modelSettings.gpt-6.1-sol, modelSettings.gpt-6-sol, modelSettings.gpt-5.6-sol, enabledPlugins.frontend-design@claude-plugins-official, enabledPlugins.playwright@claude-plugins-official, enabledPlugins.notion@claude-plugins-official, enabledPlugins.dropbox@claude-plugins-official, enabledPlugins.google-cloud-storage@claude-plugins-official, enabledPlugins.understand-anything@understand-anything, enabledPlugins.ponytail@ponytail, extraKnownMarketplaces.claude-plugins-official, extraKnownMarketplaces.understand-anything, extraKnownMarketplaces.ponytail)
+plugins: (True, '✅ Plugins: installed frontend-design@claude-plugins-official, playwright@claude-plugins-official, notion@claude-plugins-official, dropbox@claude-plugins-official, google-cloud-storage@claude-plugins-official, understand-anything@understand-anything, ponytail@ponytail') elapsed=18.7s budget=30.0s
+== M1a run 2 (30 s)
+defaults: ✅ Settings defaults: already present
+plugins: (True, '✅ Plugins: already installed') elapsed=0.0s budget=30.0s
+== M1a run 3 (30 s; expect already installed)
+defaults: ✅ Settings defaults: already present
+plugins: (True, '✅ Plugins: already installed') elapsed=0.0s budget=30.0s
+== M1a records
+installed ponytail@ponytail: True [{"scope": "user", "installPath": "/tmp/ponytail-home.AlWvBt/.claude/plugins/cache/ponytail/ponytail/5.3.3", "version": "5.3.3", "installedAt": "2026-11-04T13:41:05.325Z", "lastUpdated": "2026-11-04T13:41:05.325Z", "gitCommitSha": "96608e078b2d5ea607c5c3b8b5a54d1c1fba6846"}]
+known marketplace key ponytail: True
+== settings env/enabled in throwaway HOME
+lite True
+== M1c skill files
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/clean-up-dropbox-content/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/collect-files-with-request/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/find-dropbox-content/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/inspect-dropbox-file/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/organize-dropbox-folder/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/078f0ca36df4-c857d09d/skills/share-dropbox-content/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/clean-up-dropbox-content/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/collect-files-with-request/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/find-dropbox-content/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/inspect-dropbox-file/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/organize-dropbox-folder/SKILL.md
+$H/.claude/plugins/cache/claude-plugins-official/dropbox/1.0.1/skills/share-dropbox-content/SKILL.md
+== M1b session in a throwaway git repo (claude -p, lite expected)
+[claude-code:unrecognized_model] {"model":"gpt-6.1-sol","query_source":"sdk"}
+1) No. The line is `SessionStart:startup hook success: PONYTAIL MODE ACTIVE — level: lite`, which has a prefix.
+2) Yes.
+rc=0
+.ponytail-active: lite
+.ponytail-statusline-nudged: present
+ponytail-statusline.sh copied: yes
+ledger csv: board.html
+proj.csv
+== AC-M2 (opt-out kept): fresh HOME with ponytail false, fake claude logging commands
+defaults: ✅ Settings defaults: added 24 (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, env.CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, env.PONYTAIL_DEFAULT_MODE, modelSettings.gpt-6-astra, modelSettings.gpt-6.1-sol, modelSettings.gpt-6-sol, modelSettings.gpt-5.6-sol, enabledPlugins.frontend-design@claude-plugins-official, enabledPlugins.playwright@claude-plugins-official, enabledPlugins.notion@claude-plugins-official, enabledPlugins.dropbox@claude-plugins-official, enabledPlugins.google-cloud-storage@claude-plugins-official, enabledPlugins.understand-anything@understand-anything, extraKnownMarketplaces.claude-plugins-official, extraKnownMarketplaces.understand-anything, extraKnownMarketplaces.ponytail)
+plugins: (True, '✅ Plugins: installed frontend-design@claude-plugins-official, playwright@claude-plugins-official, notion@claude-plugins-official, dropbox@claude-plugins-official, google-cloud-storage@claude-plugins-official, understand-anything@understand-anything') elapsed=0.0s budget=30.0s
+ponytail commands run: 0
+0
+value kept: False
+== AC-M3 (no claude on PATH)
+defaults: ✅ Settings defaults: added 25 (outputStyle, model, effortLevel, alwaysThinkingEnabled, verbose, teammateMode, agentPushNotifEnabled, skipDangerousModePermissionPrompt, env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS, env.CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION, env.PONYTAIL_DEFAULT_MODE, modelSettings.gpt-6-astra, modelSettings.gpt-6.1-sol, modelSettings.gpt-6-sol, modelSettings.gpt-5.6-sol, enabledPlugins.frontend-design@claude-plugins-official, enabledPlugins.playwright@claude-plugins-official, enabledPlugins.notion@claude-plugins-official, enabledPlugins.dropbox@claude-plugins-official, enabledPlugins.google-cloud-storage@claude-plugins-official, enabledPlugins.understand-anything@understand-anything, enabledPlugins.ponytail@ponytail, extraKnownMarketplaces.claude-plugins-official, extraKnownMarketplaces.understand-anything, extraKnownMarketplaces.ponytail)
+plugins: (True, '⏭️  Plugins: claude CLI not found; skipped') elapsed=0.0s budget=30.0s
+rc=0
+== real ~/.claude after
+5711b646dfb93d13 /home/coder/.claude/settings.json
+55a39037ff3fcc56 /home/coder/.claude/plugins/installed_plugins.json
+6805f6e8293b74a2 /home/coder/.claude/plugins/known_marketplaces.json
+real .ponytail-active absent
+cleanup done: /tmp/ponytail-home.AlWvBt /tmp/ponytail-home2.VVJqpe /tmp/ponytail-home3.5hbbkC removed
+```
+
+## Log 2 (Ponytail-only reinstall to list skill files)
+
+```text
+(True, '✅ Plugins: installed ponytail@ponytail')
+./5.3.3/.openclaw/skills/ponytail-audit/SKILL.md
+./5.3.3/.openclaw/skills/ponytail-debt/SKILL.md
+./5.3.3/.openclaw/skills/ponytail-gain/SKILL.md
+./5.3.3/.openclaw/skills/ponytail-help/SKILL.md
+./5.3.3/.openclaw/skills/ponytail-review/SKILL.md
+./5.3.3/.openclaw/skills/ponytail/SKILL.md
+./5.3.3/skills/ponytail-audit/SKILL.md
+./5.3.3/skills/ponytail-debt/SKILL.md
+./5.3.3/skills/ponytail-gain/SKILL.md
+./5.3.3/skills/ponytail-help/SKILL.md
+./5.3.3/skills/ponytail-review/SKILL.md
+./5.3.3/skills/ponytail/SKILL.md
+removed /tmp/pt-skills.RBVTrz
+```
diff --git a/.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/t4-checks.log b/.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/t4-checks.log
new file mode 100644
index 00000000..44d342a8
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/t4-checks.log
@@ -0,0 +1,20 @@
+$ make verify-sync
+✅ All components in sync.
+rc=0
+$ git diff --stat HEAD   (HEAD = branch base = origin/master 119622e3; local master is stale)
+ CHANGELOG.md                                    | 11 +++
+ docs/getting-started/installation.md            | 80 +++++++++++++++++++++-
+ src/superclaude/cli/install_user_setup.py       |  7 +-
+ src/superclaude/cli/user_settings_defaults.json | 12 +++-
+ tests/cli/test_install_user_setup.py            | 89 +++++++++++++++++++++++++
+ 5 files changed, 192 insertions(+), 7 deletions(-)
+$ git status --short | grep "^??"   (only .dev/ packages untracked)
+?? .dev/brainstorms/20261104-063430-ponytail-plugin-install/
+?? .dev/reflect/pre-closeIronbellyOr-20261104084538/
+?? .dev/reflect/pre-closeIronbellyOr-20261104124503/
+?? .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/
+?? .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/
+$ grep -n "to `lite`\|option to `false`" CHANGELOG.md
+11:- `superclaude install`, `superclaude update` and `update
+$ git diff HEAD -- CHANGELOG.md | removed lines (0 = no existing section changed)
+0

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty):

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
