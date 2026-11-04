235bb29732e5681bbc6e23842700f369c166175e
Review one task for spec compliance.

Task brief: ## Task 3: Rewrite the default-plugin paragraph and add the Ponytail lite section in `docs/getting-started/installation.md`

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

AC ids: T3.AC1,T3.AC2,T3.AC3,T3.AC4 (in the order of the Acceptance criteria bullets)
Global constraints: ## Constraints

- Change only `src/superclaude/cli/user_settings_defaults.json`, `src/superclaude/cli/install_user_setup.py` (at most 5 changed lines, failure label only), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md` and `CHANGELOG.md`. No change to `main.py`, `update.sh`, `doctor.py`, output styles, rules, hooks, any skill, command or agent, or any `.claude/` file.
- Never run `superclaude install`, `superclaude update`, `./update.sh` or `claude plugin ...` against this workspace's `~/.claude`; any manual proof uses a throwaway `HOME` under `/tmp` that is removed afterwards.
- No `pluginConfigs` entry, no `statusLine` setting, no write outside `~/.claude`, no version pin, no new module, constant, flag or CLI option.
- A user's existing `enabledPlugins`, `env` and marketplace values are never changed.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); never stage `.claude/` paths.
- The superseded package `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/` and `.dev/reflect/pre-closeIronbellyOr-20261104084538/` stay on disk untouched.
Start sha: 235bb29732e5681bbc6e23842700f369c166175e
Diff against the start snapshot: diff --git a/docs/getting-started/installation.md b/docs/getting-started/installation.md
index 551f022a..13ae732c 100644
--- a/docs/getting-started/installation.md
+++ b/docs/getting-started/installation.md
@@ -351,14 +351,85 @@ registered, and only the verbose output shows that line.
 </div>
 
 `superclaude install` also installs the default Claude Code plugins listed in
-its settings defaults (six plugins, including `playwright` and `frontend-design`)
+its settings defaults (including `playwright`, `frontend-design` and `ponytail`)
 with `claude plugin install <plugin> --scope user`, skipping any you disabled in
 `enabledPlugins`. This step downloads over the network within a shared 30-second
 budget (with the Orca skills step); a plugin that fails or runs out of time is
-reported, and the step never makes `superclaude install` fail. Rerun
+reported by name, and the step never makes `superclaude install` fail. Rerun
 `superclaude install` to retry. When the Orca CLI is installed, the same step
 asks it to install its own skills (`computer-use`, `orca-cli`, `orchestration`).
 
+**Ponytail.** `ponytail` (from `DietrichGebert/ponytail`) adds the `ponytail-*`
+skills and the `/ponytail` command, and runs in its always-on `lite` mode: the
+installer sets `PONYTAIL_DEFAULT_MODE` to `lite` under `env` in
+`~/.claude/settings.json` unless you already set it. The behaviour below was
+checked against Ponytail v5.3.3; the plugin is not pinned to a version, so a
+later release may differ.
+
+In `lite`, every session start:
+
+- injects Ponytail's rules at the lite level ("Build what was asked. Name the
+  smaller option in one line and let the user pick."). The rules include the
+  rest of Ponytail's guidance too, for example ending each reply with one or two
+  lines on what was skipped and any risk;
+- appends a short map of the codebase (set `PONYTAIL_MAP=0` to turn the map off);
+- records the mode in `~/.claude/.ponytail-active`.
+
+Every subagent gets the same rules. `PONYTAIL_SUBAGENT_MATCHER`, a
+case-insensitive regular expression on the agent type, limits which subagents
+get them; it is best-effort and injects anyway when the expression is invalid.
+
+If your user settings have no `statusLine`, the first session on the workspace
+gets a one-time note asking Claude to offer to set up Ponytail's statusline
+badge. Ponytail copies `ponytail-statusline.sh` into `~/.claude` and writes
+`~/.claude/.ponytail-statusline-nudged`, so the note is not repeated. The first
+session can be an unattended Orca worker or a headless `claude -p` run: a worker
+sees the note in its context and may mention the offer in its reply. The
+installer never sets `statusLine`; to skip the note, set your own `statusLine`
+or create that file before the first session.
+
+Ponytail's band module runs in every mode: it draws a band above the prompt,
+runs `git grep` over the repo at session start, watches every Edit and Write,
+and after every turn writes a ledger row to
+`$XDG_CONFIG_HOME/ponytail/band/<project>.csv` (or
+`~/.config/ponytail/band/<project>.csv` when `XDG_CONFIG_HOME` is unset). The
+ledger stays local unless you set Ponytail's webhook option. `/ponytail band off`
+hides the band; the `git grep`, the Edit/Write watch and the ledger keep
+running. The ledger is on by default: set Ponytail's `ledger` option to off in
+`/config` to stop it.
+
+To change the mode for the current project, type `/ponytail off`,
+`/ponytail lite`, `/ponytail full` or `/ponytail ultra`; a message that is
+exactly "stop ponytail" or "normal mode" also turns it off. The level is stored
+per project directory, so each worktree has its own, and any new session,
+`/clear` or resume in that directory sets it back to the default. Bare
+`/ponytail` reports the level when Ponytail is on, and switches it on at the
+default level when it is off (`full` when the default is `off`). To change the
+default, set `PONYTAIL_DEFAULT_MODE` under `env` in `~/.claude/settings.json` to
+`off`, `lite`, `full` or `ultra`. The variable overrides Ponytail's own
+`/ponytail default <mode>`, which prints "PONYTAIL DEFAULT SET" but has no
+effect while the variable is set.
+
+To opt out, set `"ponytail@ponytail": false` under `enabledPlugins` in
+`~/.claude/settings.json`. Do not delete the key: the next install adds it back
+as `true`.
+
+Ponytail keeps its files under `CLAUDE_CONFIG_DIR` when that variable is set,
+while the installer always writes to `$HOME/.claude` (see the note below). Its
+hooks need `node` on your PATH; IronClaude's own SubagentStart hook already
+needs it. Existing workspaces get Ponytail only after the IronClaude package
+itself is upgraded: upgrade the package the way you installed it (for a
+checkout, `git pull` before `./update.sh`, because `update.sh` reinstalls from
+the local checkout), then run `superclaude update` or `superclaude install`.
+
+On a workspace where Orca's skill install uses the shared 30 s network budget on
+every run, the installer may not reach the Ponytail install. Such a workspace
+gets Ponytail on a later run that leaves budget, or through Claude Code's own
+background install of enabled plugins (UNVERIFIED). Every marketplace is added
+before any plugin is installed, so the extra Ponytail download can also push
+the other default plugins past the budget on a fresh workspace; they are
+reported by name and installed on a later run.
+
 > **`CLAUDE_CONFIG_DIR`.** The installer always writes its files under
 > `$HOME/.claude/`. If you set `CLAUDE_CONFIG_DIR`, it is used only to find
 > `.claude.json` when reading MCP registrations. An empty

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
