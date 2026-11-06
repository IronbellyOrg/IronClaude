# Changelog

All notable changes to IronClaude are documented in this file.

## [Unreleased]

### ccsession: a shim never forwards to another shim

#### Fixed (ccsession shim upstream)

- Every ccsession launch in a Coder workspace failed with `API Error: 502 ccsession: gateway unreachable: [Errno 111] Connection refused` while the gateway was up. The 4013 shim's upstream was `http://127.0.0.1:4114`, the address of a shim that had stopped. The installer's `seed-env.py` copied the shell's `ANTHROPIC_BASE_URL` into `~/.claude/ccsession.env`; run inside a ccsession session, that value is the session's shim. ccsession sources that file after the inherited environment, so the saved address overrode the right one on every launch, and the health check kept reusing the broken shim because its upstream matched.
- The installer no longer saves the gateway address. Orca terminals, the Coder terminal and `coder ssh` all receive it from the workspace (Coder `llm-env.tf`), so the reason for saving it (Orca terminals started from a cleared environment) no longer holds. `seed-env.py` is replaced by `unseed-env.py`: `superclaude install` and `install.sh` put a file that is exactly the example plus the installer's marker and one address line back to the example. A file you edited is never touched.
- A shim session exports `CCSESSION_GATEWAY_URL` (the gateway) beside `CCSESSION_SHIM_URL` (its own address). A `ccsession` started inside it forwards to the gateway, not to the parent shim.
- ccsession refuses to start or reuse a shim whose upstream is a loopback address on a port a ccsession shim can take (the base port, base + 1 to 97, and the same 101 apart, six times; `models.py shim-upstream-check`). The check needs no network, so it also catches a shim that has stopped. A local gateway such as `http://127.0.0.1:4000/cli` is still allowed. The shim itself refuses its own address as upstream.
- The shim's 502 names its upstream (`ccsession: gateway unreachable at <upstream>: ...`). Claude Code shows only the shim's address, which hid the cause.
- A Ctrl+C at the session-name question (`ccsession --ask`, which `ccsession-orca` asks) that arrived just after the question appeared could wait out the whole time limit (30 s by default) before taking effect: bash had not started reading yet, so the INT trap only ran when the one long `read -t` returned. The question now reads in one-second slices, so a Ctrl+C takes effect within a second; the time limit and typed lines are unchanged. This was the intermittent `test_ask_prints_only_the_name_on_stdout` timeout in the parallel Python 3.10 CI job (1 in 12 runs under load before, 0 in 24 after).
- A workspace already affected needs the address in `~/.claude/ccsession.env` fixed (or `superclaude install` run again with this version, for a file the installer owns) and the broken shim stopped.

#### Added (ccsession shim upstream)

- Tests: `test_unseed_resets_an_installer_owned_file_to_the_example`, `test_unseed_leaves_edited_files_alone`, `test_installers_no_longer_save_the_gateway_address`, `test_shim_upstream_check_flags_only_shim_addresses` (a local gateway on 4000 allowed), `test_launch_refuses_a_shim_address_as_upstream` (inherited and env-file cases, nothing listening on the shim address), `test_nested_launch_forwards_to_the_gateway_not_the_parent_shim`, `test_shim_refuses_its_own_address_as_upstream`, and the upstream named in `test_unreachable_gateway_is_not_a_switch`.

### ccsession: status lines go to standard error (#389)

#### Fixed (ccsession output streams)

- Every informational `[ccsession]` line (shim, profile and tier, session start and resume, the model cache and model list notes, and the Orca reopen notices) now goes to standard error. A scripted `claude --version`, `claude mcp list` or `claude -p ... --output-format stream-json` that runs through `ccsession-orca` gets only Claude's own output on standard output. This unblocks IronbellyOrg/Coder PR 458.
- `superclaude eval` therefore reads the real Claude version. Before, the launcher's lines came first and the version check took `127.0.0` from the shim address `127.0.0.1:<port>`, because its probe reads standard output first.
- The lines still show in a terminal. Redirecting `ccsession` standard output to a file no longer collects them.
- The values printed by `--ask`, `--auto-name`, `--list`, `--rm`, `--refresh-models` and `--models-status`, and the `models.py` output the launcher captures, stay on standard output.
- The fix reaches a workspace only after `superclaude install` is run again.

#### Added (ccsession output streams)

- Tests that pin the streams: a replay of `ccsession-orca --version` with a stand-in Claude (`test_version_through_orca_keeps_stdout_clean`), `test_launch_status_lines_are_on_stderr_only` (six launch variants), `test_model_list_update_note_goes_to_stderr_at_launch`, `test_refresh_models_report_stays_on_stdout`, a source guard for the lines a launch test cannot reach (`test_status_lines_in_launcher_scripts_go_to_stderr`), and three version-parsing tests in `tests/cli/eval/test_doctor_version.py`.

### ccsession: start Claude without the permission bypass (#390)

#### Added (ccsession permissions)

- `CCSESSION_PERMISSIONS=default`: `ccsession` starts Claude without `--dangerously-skip-permissions`. Only `--allowedTools=Grep` is added, so Grep and Glob stay available. The shim and tier-model routing are unchanged, and unset or empty behaves as before. Set it in the shell environment that starts `ccsession`: it is read before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file (a value exported there is undone, so Claude and a nested `ccsession` see what the shell set), and it stays exported to nested launches. Any other non-empty value (for example `Default` or `bypass`) exits with status 2 on every `ccsession` call, `--help` included, so a typo never falls back to the bypass. A non-empty `CC_CLAUDE_FLAGS` (from the shell or the env file) still replaces the default flags, an empty one still takes the default, and flags the caller passes to Claude (such as Orca's default `--dangerously-skip-permissions` option) still apply. Callers such as the Coder `claude` wrapper opt in themselves; `superclaude reflect` is not changed. It is documented in `ccsession --help`, the skill README and `ccsession.env.example`, and two v5.0.0 testing guides mention it.

### onboarding deck: a 15-slide page for new team members, built from the routing guide

#### Added (onboarding deck)

- `docs/onboarding/ironclaude-onboarding.html`: a single-page onboarding deck (15 slides, 6 inline diagrams, light and dark themes, prints one slide per page) that explains why IronClaude exists, how a command and its skill are built, how to pick a process level, the two planners, the path from idea to pull request, review and shipping with the four `--monitor` ceilings, where work is saved, how to resume, and the common traps. It follows `src/superclaude/core/HOW-WE-WORK.md` at commit adaa28d9 and links to it for every command; stories from the onboarding meeting are marked as such. A comment at the top of the file says to update the deck in the same PR when the guide changes in a way a slide depends on.
- `tests/docs/test_onboarding_deck.py`: checks that every command and flag the deck shows (in code and inside its diagrams) appears in the guide, with `--plugin` checked against `src/superclaude/commands/recommend.md`, and that the deck keeps its "Built from HOW-WE-WORK.md at commit" footer.
### ccsession: agents no longer get stuck at the session name question (#315)

#### Fixed (ccsession name question)

- An agent or worker started through `ccsession-orca` with a task could stop at `Session name (...)` and wait for a person. The question is now asked only when Claude starts with no task, no name and no resume. A prompt, `--prefill`, `--session-id`, `-p`, `CCSESSION_NAME`, Claude's own `--name`/`-n`, and `--resume`/`--continue`/`--fork-session`/`--from-pr` all skip it.
- `--fork-session` and `--from-pr` now skip the question like `--resume`. The README said `--fork-session` did; the code still asked.
- `ccsession --ask` waited for ever unless its caller set `CCSESSION_ASK_TIMEOUT`, and only `ccsession-orca` did (30 seconds). The default now lives in the question itself for every caller: `CCSESSION_ASK_TIMEOUT` seconds, default 30. `0`, or a value that is not a whole number of seconds (such as `1.5` or `30s`), waits for ever. While a limit is set, the default question and a hint containing `@LIMIT@` show it; a caller's own hint without `@LIMIT@` does not, but the limit applies. A caller that relied on the old no-limit default, such as a terminal-start hook that calls `ccsession --ask`, now gives up after 30 seconds unless it sets `CCSESSION_ASK_TIMEOUT=0`.
- Ctrl+C at the question now ends `ccsession-orca` with status 130 and starts no Claude (it used to start an untagged session). `ccsession --ask` also restores the terminal when Ctrl+C arrives while it collects pasted text.
- The tab-reopen path of `ccsession-orca` no longer passes `CCSESSION_NAME` or `CCSESSION_ASK_TIMEOUT` on to Claude Code.

#### Added (ccsession automatic names)

- A `ccsession-orca` launch that starts a new session without a name (not a resume, not print mode, not `CCSESSION_AUTOSTART=0`, not `--version` or a subcommand) gets a valid automatic one: Enter at the question, no answer within the limit, keys typed ahead, no terminal, and every launch that carries a task. The label is `<folder>-<up to four words of the task>-<MMDD-HHMMSS>-<4 hex>`, only letters, digits and hyphens, checked against the saved names, and it appears in `ccsession --here` once the session starts. If the name list cannot be written, Claude starts untagged instead of stopping.
- `ccsession --auto-name [<task text>]` prints such a label; `ccsession --check-name <name>` exits 0 for a valid name.
- `CCSESSION_NAME=<name>` in the environment names a session without a prompt (for orchestrators). An invalid value is dropped with a warning and Claude still starts; a value equal to a saved label resumes that session (while its conversation is still saved), loudly. A valid value is passed as `--name` even with `-p`, `--version`, a subcommand or `CCSESSION_AUTOSTART=0`, so set it only on a launch that starts a new session; with `--resume <id>` and a name that is also a saved label, Claude would get two `--resume` arguments.
- `ccsession --ask` exits 3 and prints the text as typed when the line cannot be a name (a control character among other text, too long to save, or several lines pasted after a first line that is not blank; a pasted block that starts with a blank line is read as an empty answer); `ccsession-orca` passes that text to Claude as its first message and auto-names the launch. A normal line, spaces included, stays a name. A hint may contain `@LIMIT@`, replaced by the time limit in seconds; with no limit, the hint is cut at the first `; ` that has `@LIMIT@` after it, and a hint without such a `; ` keeps `@LIMIT@` as written.

#### Changed (ccsession name question)

- The question in `ccsession-orca` reads `Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):`. Enter and the time limit start an automatically named session; they no longer start an untagged one. Print mode (`-p`), `--version`, `--help` and Claude subcommands (`mcp`, `doctor`...) start untagged and ask nothing; on a terminal they used to ask first. `CCSESSION_AUTOSTART=0` still starts untagged and asks nothing. A valid `CCSESSION_NAME` names any of these launches.
- The README describes the one question rule, the launch paths and the one documented exception: Claude Agent Teams starts its teammates itself, without `ccsession-orca`, so those sessions are not named (follow-up). Orchestrators should always pass the task or a name. `docs/testing/v5.0.0/user/D08-ccsession.md` tests the question, the automatic names and the launch paths by hand and notes the exception.

### Models: primitives use the plain aliases `opus`, `sonnet` and `haiku`, with a documented ccsession tier mapping (#384)

#### Added (model aliases)

- New reference page `docs/reference/model-aliases.md`: what `tests/skills/test_model_alias_policy.py` checks and its allow-list (the three issue-worker agents pin picker ids on purpose), the owner decision of 2026-11-05 for a ccsession tier workspace (`opus` to `claude-gw-tier1a`, `sonnet` to `claude-gw-tier1b`, `haiku` to `claude-gw-tier2`, through `ANTHROPIC_DEFAULT_*_MODEL`), why aliases and not picker ids, and the known consequences. The launcher sets these variables in tier mode through the follow-up change in the next entry (specified in `.dev/issues/384/launcher-followup.md` with its failing-first test). The workspace defaults file exports real model ids for the same three variables, and the launcher export replaces the ones for tiers the owner may use inside a tier workspace.
- New test file `tests/skills/test_model_alias_policy.py` (frontmatter `model:` values, `claude-gw-tier` text, full model ids in Python constants and in `--model` flags, and the fixes below) and four tests that record how the sprint alternate-model suggestion and the reflect alias count behave while the variables hold tier ids.

#### Changed (model aliases)

- `superclaude reflect run` now falls back to the alias `opus` when `ANTHROPIC_MODEL` is not set, instead of the dated id `claude-opus-4-8`. The D12 manual test expects `--model opus`.
- The `/sc:issue` next-step chains no longer pass `--models opus,sonnet` to `/sc:brainstorm`; the brainstorm defaults (`opus,sonnet,haiku`) apply. `refs/tiers.md` no longer states that `haiku` is `glm-5.3`.
- The cleanup-audit skill, command and report template say that the Pass 1 scanner runs on Sonnet, as `audit-scanner` already did, and drop the 50-70% cost claim that was specific to Haiku.
- The implement retry ladder (`refs/retry.md`, `refs/ledger.md`) names the slot variables the workspace exports (`T3Model01`, `T2Model01`, `T2Model02`, `T1Model01`, `T1Model02`) instead of spellings with an underscore that no workspace exports. In a workspace that sets the four rung variables the primary ladder now replaces the alias fallback ladder, which changes which models the retry advisers use.

### ccsession: tier mode sets the model aliases (#384 launcher follow-up)

#### Changed (ccsession tier mode)

- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (`src/superclaude/skills/ccsession-tag/ccsession`), each one only when the workspace owner may use its tier, so the plain aliases `opus`, `sonnet` and `haiku` in agent frontmatter and `--model` resolve to the tiers (the probes did not exercise the Agent-call `model` parameter). "May use" is read with the `tiers` command of `models.py`, the rule the shim applies, without running the shim. A variable whose tier the owner may not use, or every variable when the list cannot be read, keeps its inherited value: an owner limited to tier2 and tier3 gets only the haiku variable and keeps the inherited opus and sonnet values. Outside tier mode the launcher sets none of them. Inside a tier workspace the exported values replace the real model ids that the workspace defaults file exports for the same variables.
- The pages that said the launcher would set the variables later now say that it does: `docs/reference/model-aliases.md`, `docs/user-guide/brainstorm.md`, `docs/user-guide/commands.md`, `refs/tiers.md` and `refs/chains.md` of the `/sc:issue` protocol, a comment in `src/superclaude/cli/reflect/commands.py` and the docstring of `tests/skills/test_model_alias_policy.py`.

#### Added (tier alias tests and probe)

- Five tests in `tests/unit/test_ccsession_tiers.py`: `test_tier_launch_exports_the_alias_variables` (an unrestricted owner gets all three; it failed before the launcher edit), `test_non_tier_launch_leaves_the_alias_variables_unset`, `test_limited_owner_gets_only_the_haiku_alias_variable`, `test_limited_owner_keeps_inherited_alias_values` and `test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers`, with three keys added to the fake Claude of `_launch_env`.
- Probe record `.dev/issues/384/analysis/probe-sonnet-alias.md`: `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` makes `--model sonnet` and `model: sonnet` run on that tier. In that probe a subagent whose alias is in the main session's own model family stayed on the main session's model.

### Install: harden the pinned-plugin install (#360 follow-ups)

#### Fixed (plugin install)

- A registered `ironclaude` marketplace whose path cannot be resolved (a symlink loop, which raises on Python 3.10 to 3.12, or a path holding a NUL byte) no longer aborts `superclaude install`. The registration is refused like one from another source, and the other plugins still install.
- The pinned-commit check now looks only at the user-scope copy of a plugin, the copy `superclaude install` installs and updates. A project-scope copy at the pin no longer hides a user-scope copy on another commit, and a plugin installed only at project scope, or listed with no user-scope record, is now installed at user scope.
- Every `claude plugin` command the installer runs now acts on `$HOME/.claude`, the profile whose plugin records it checks and where it writes its own files (rules, settings, commands, skills, agents, hooks). Before, the commands inherited `CLAUDE_CONFIG_DIR`, so the marketplace check and the commands could use different profiles and a foreign `ironclaude` marketplace in the `CLAUDE_CONFIG_DIR` profile could be used. If you run Claude Code with `CLAUDE_CONFIG_DIR`, the default plugins are now installed into `$HOME/.claude`, not into that profile. The codegraph MCP registration is unchanged: it still follows `CLAUDE_CONFIG_DIR`.

### Hooks: block bare python, python3, pip and pip3 in Bash calls (#357)

#### Added (UV-only Bash hook)

- New PreToolUse `Bash` hook `block-bare-python.sh`. A Bash tool call whose command runs bare `python`, `python3`, `pip` or `pip3` as a command word is blocked (exit 2), and the message tells the agent to use `uv run python` (or `uv pip`, `uvx`) instead, or `jq` to parse JSON. It also fires for subagent Bash calls. The "use UV for all Python" rule was text-only until now, and agents and helper subagents kept breaking it.
- Allowed: `uv run python`, `uv pip`, `uvx`, and commands that only mention python in arguments, paths, patterns, quoted text, comments or heredoc text, such as `grep -rn python3 src/`, `echo "python3 -c 1"`, `command -v python3` or a multi-line `git commit -m "$(cat <<'EOF' ...)"` message. Commands chained with `&&`, `||`, `;`, `|` or `&`, wrapped in `sudo`, `env`, `timeout`, `nice`, `nohup`, `time`, `exec` or `command`, or nested in `$(...)`, backticks (also inside double quotes or `$(( ))` arithmetic), subshells or process substitution (also as a redirect target, `< <(...) python3`) are checked word by word. Wrapper options that take a value are skipped with their value, in short (`-u U`, `-Eu U`), long (`--user U`, `--signal TERM`) and abbreviated (`--sig TERM`) form. Quoted command words (`"python3" x.py`), `$'...'` escapes (`$'\160ython3'`) and paths (`.venv/bin/python`) count as bare. Words inside `[[ ... ]]` tests, such as `=~ ^(python|pip)$` patterns, are not commands; as in bash, a quoted or escaped `[[` (or other keyword) is an ordinary command word. A function definition named `python3` or `pip` (`python3() { uv run python "$@"; }`) is not a call, though its body is checked, and redirections with a named descriptor (`{fd}>/dev/null python3`) are skipped like `2>`.
- It fails open (allows the command) when it cannot judge it: `jq` or `awk` missing, input that is not valid JSON, a tool other than Bash, or an empty command. The hook needs `jq`; on a host without `jq` it allows every command.
- Known limits, commands it does not catch: string arguments to another interpreter (`bash -c "python3 x"`, `eval`, `env -S`), commands started by another program (`xargs python3`, `find -exec python3`), a heredoc piped into a shell (`cat <<'EOF' | bash`), `${...}` parameter expansions, nested backticks written with `\``, versioned names such as `python3.12`, wrapper options that take a value but are not in the hook's option tables, shell commands run by tools other than Bash, and `claude --bare` sessions, which skip settings hooks.
- `superclaude install` copies the hook to `~/.claude/hooks/` and registers it in `~/.claude/settings.json`; the plugin mirror registers it too.
- `sc:troubleshoot`'s read/parse probe pack (`refs/probe-packs/read-parse.md`) now runs its seek probe with `uv run --no-project python` instead of bare `python3`.

### Ponytail plugin installed by default (#330)

#### Added (default plugins)

- `superclaude install`, `superclaude update` and `update.sh` now install the Ponytail plugin (`ponytail@ironclaude`: upstream `DietrichGebert/ponytail` v5.3.3, pinned to commit `7801d061243d7b753bad0e0b3c057cd250b11755`) and set `PONYTAIL_DEFAULT_MODE` to `lite` under `env` in `~/.claude/settings.json` when you have not set it. In `lite`, every session start injects Ponytail's rules at the lite level ("Build what was asked. Name the smaller option in one line and let the user pick.") plus a short codebase map, and every subagent gets the same rules. On a workspace whose user settings have no `statusLine`, the first session gets a one-time note asking Claude to offer to set up Ponytail's statusline badge; that session can be an unattended Orca worker, which then sees the note and may mention the offer. Ponytail's band module runs in every mode (a band above the prompt, a `git grep` at session start, a watch on every Edit and Write, and a local per-turn ledger row under `$XDG_CONFIG_HOME/ponytail/band/` or `~/.config/ponytail/band/`). The ledger is on; set Ponytail's `ledger` option to `false` to stop it. Change the mode for the rest of the session with `/ponytail off|lite|full|ultra` (the next session start in that project directory resets it to the default), or set `PONYTAIL_DEFAULT_MODE` to `off`, `lite`, `full` or `ultra` to change the default. To opt out, set `"ponytail@ironclaude": false` in `enabledPlugins` in your user settings; do not delete the key, because the next install adds it back. An earlier opt-out with `"ponytail@ponytail": false` carries over: the installer adds `"ponytail@ironclaude": false` when that key is missing. Existing workspaces get Ponytail after you upgrade the IronClaude package, then run `superclaude update` or `superclaude install`. Needs `node` on the PATH. See [the installation guide](docs/getting-started/installation.md).
- If you already use Ponytail with a `defaultMode` in `$XDG_CONFIG_HOME/ponytail/config.json` (or `~/.config/ponytail/config.json`), the new `PONYTAIL_DEFAULT_MODE=lite` wins over it, and `/ponytail default <mode>` has no effect while that variable is set. Set `PONYTAIL_DEFAULT_MODE` under `env` to your preferred mode instead.
- Ponytail is fetched only at the pinned commit, through IronClaude's own marketplace `ironclaude`: every install writes the catalog `~/.claude/ironclaude-marketplace/.claude-plugin/marketplace.json` from the package defaults and adds it with `claude plugin marketplace add`. A marketplace already registered as `ironclaude` from any other source is never used (the warning says how to point the name at IronClaude's catalog), and a failed marketplace add or update skips that marketplace's plugins for the run. Ponytail's hooks run with your permissions, so an upstream change reaches you only when an IronClaude release moves the pin; the next `superclaude install` or `superclaude update` then updates the installed plugin to the new commit. Maintainers bump the pin by changing `ref` and `sha` under `ironclaudeMarketplace` in `src/superclaude/cli/user_settings_defaults.json` and `PONYTAIL_SHA` in `tests/cli/test_install_user_setup.py`. To run a newer Ponytail, set `"ponytail@ironclaude": false` and install upstream yourself with `claude plugin marketplace add DietrichGebert/ponytail` and `claude plugin install ponytail@ponytail --scope user` (unpinned; it follows upstream).
- Master from #358 (commit `9b9497e6`) until this fix shipped Ponytail unpinned as `ponytail@ponytail` from the `DietrichGebert/ponytail` marketplace. On a workspace installed from it, or where you installed `ponytail@ponytail` yourself, the next install adds the pinned `ponytail@ironclaude` beside it, so both are enabled (an old `false` carries over instead); the installer leaves `ponytail@ponytail` alone because its entries look exactly like ones you add yourself. To keep only the pinned copy, run `claude plugin marketplace remove ponytail` (it uninstalls `ponytail@ponytail`, removes its `enabledPlugins` entry and deletes its saved options; later installs do not add it back). To keep upstream Ponytail instead, set `"ponytail@ironclaude": false`.

#### Fixed (plugin install report)

- A plugin that fails to install is now listed by its name in the `Plugins: not installed` warning (it printed `--scope`).

### sc:pr-submit: merge-conflict detection and resolution (#305)

#### Added (pr-submit conflicts)

- At `--monitor 1` and above, the end of Wave 0 checks for a git operation in progress (halts `foreign_op_in_progress`), reads GitHub's `mergeable`, and only on a conflict runs a read-only local probe (`git merge-tree --write-tree`) that classifies every conflicted path into a tier and prints the plan before any edit.
- Tier 1 (opt-in with `--conflict-max-tier 1`, because `uv lock` can run the PR's build code): a conflicted root `uv.lock` is regenerated with `uv lock` at Wave 8 entry and published as one merge commit of the recorded base tip, pushed fast-forward (never forced). It spends no review round, re-triggers no reviewer, is counted in the new `sync_push_count`, and the CI wait then expects checks on the new head (`expect_checks`), so an empty check list right after the push is no longer read as clean.
- Tier 2 (off by default): text and tree conflicts resolved by stated intent before the first review, with a per-file resolution record, an `evidence-validator` grounding check, full tests, a reviewer re-trigger and one round. Enable with `--conflict-max-tier 2`.
- Tier 3 (submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, anything unclassifiable) halts at the end of Wave 0 at L3 with nothing touched, and is reported at L1 and L2.
- New flag `--conflict-max-tier {0,1,2}` (default 0); 0 detects and reports only, so no conflict is resolved unless you pass 1 or 2.
- New core module `superclaude.pr_submit.conflicts`, refs `conflict-mechanical.md` and `conflict-intent.md`, scripts `probe-merge.sh`, `finish-merge.sh` and `collect-conflict-evidence.sh`, and `poll-ci-checks.sh --evidence-sha`.

#### Changed (pr-submit conflicts)

- At `--monitor 1` and above the create path no longer rebases or halts when the branch is behind its base; it reports how many commits behind. `--monitor 0` is unchanged.
- Every push record carries a `kind` (`fix`, `merge`, `sync`, `ci`); `--resume` uses it, so a crashed CI or sync push resumes into the CI wait instead of the review re-trigger path. Old run-logs read as `fix`.
- `push_count` counts fix, CI and Tier 2 merge pushes; Tier 1 sync pushes are in `sync_push_count`. The documented bound is `push_count <= max_rounds + 1`.
- The run-log event enum has 43 members (`sync_started`, `sync_concluded`).
- A PR that is still conflicting at Wave 8 with nothing pushed skips the CI wait (`pr_conflicting`) and ends `terminal_halted` instead of waiting for checks that GitHub will not run; a run that saw a conflict re-reads `mergeable` before claiming clean. Late re-sync during the CI wait is #361.

## [5.0.0] - 2026-11-02

Major release: codegraph replaces codebase-memory-mcp and Serena, and several commands, flags and core files are removed. Read the [5.0.0 release notes](docs/releases/v5.0.0.md) for the breaking changes and upgrade steps. This is the first versioned section of this changelog; it covers every change since the package version was set to 4.3.5 (2026-06-04), which was never tagged.

### ccsession: the session list follows the worktree (#347)

#### Changed (ccsession list per worktree)

- `ccsession --here` and the session-name question (`ccsession --ask`, used by `ccsession-orca`) list the sessions started in this worktree, then, in a section of their own, the sessions whose worktree was removed (with the folder they were started in), and only count the sessions of the repo's other worktrees or copies that still exist. `ccsession --here --all`, or `*` at the question, lists every worktree's sessions. Claude Code continues a resumed conversation in the folder it is started in, so picking another worktree's session put its edits and commits in this worktree. A session's folder is the one Claude Code named its transcript folder after (the folder it was started in), as Claude Code's own `/resume` picker groups sessions; the `cwd` a transcript records follows the shell's `cd`, so it is used only to recover the real path.
- Resuming a session by name that was started in another worktree that still exists works as before, with a warning naming that worktree.

### ccsession: shim survives its launching terminal (#341)

#### Fixed (ccsession shim survives its terminal)

- The shared gateway shim was started inside the terminal that first launched it, so closing that terminal (Orca kills its descendants) cut every other session's reply and refused new ones until a later launch started a new shim. ccsession now starts it from a subshell and the shim starts its own session, so it keeps running until stopped (`pkill -f local-gateway-alias-proxy.py`). A shim already running keeps the old behaviour until it is stopped and a launch starts a new one.
### Reviews: minor findings never fail a review; review loops capped at 2 fix cycles

User decision (release blocker for 5.0.0; evidence: the QA-loop investigation `FINDINGS.md`, bundle A).

#### Changed (review severity)

- The Pragmatic output style (`output-styles/pragmatic.md`) replaces "any issue of ANY severity fails" with five rules: grade every finding blocking or minor; only blocking findings fail a review, and minor findings are recorded as notes, are not rechecked and never trigger a fix pass; a review loop runs at most 2 fix cycles (3 reviews), then escalates to the user with the open blocking findings; a protocol with its own severity model, such as `/sc:implement`, keeps it; findings are graded by definition, and on a CRITICAL / IMPORTANT / MINOR scale CRITICAL and IMPORTANT are blocking and MINOR is minor.
- The rf-qa, rf-qa-qualitative, rf-analyst and rf-team-lead agents, the QA agent and skill templates, both MDTM task templates, the prd, tdd, tech-reference, tech-research, readme, operational-guide, task and task-builder skills, the prd CLI prompts and the legacy QA rule prompts follow the same rule: PASS allows minor findings as notes, FAIL needs a CRITICAL or IMPORTANT finding, and fix agents receive, apply and recheck blocking findings only.
- At the cap, every loop now HALTs and escalates the open blocking findings to the user instead of turning them into Open Questions and proceeding. This covers task-builder's post-execution reflect gate (open Regression or Drift deviations) and sc:tasklist's patch loop, which no longer patches Low findings or ships open blocking findings "logged for human review".
- Every review-loop cap above 2 is lowered to 2 fix cycles. The prd CLI's research fix cycles default to 2; cli-portify's convergence engine and its `--max-convergence` flag default to 1 iteration (2 review passes per iteration).
- `/sc:implement` drops its second A2 in-place repair (one repair per attempt; attempts A3-A5, the halt contract and FINAL are unchanged).

#### Added (review severity)

- `tests/skills/test_review_severity_rule.py` fails CI if any wording of the old rule, a fix-cycle cap above 2, an Open Questions at-cap rule, or a fix loop that sends minor findings to a fix pass comes back, and checks the S1-S5 rules against `pragmatic.md`.

### GitHub issue body files and a CLAUDE.md rule line

#### Added (issue body files)

- `superclaude install` now also copies `ISSUE-HANDOFF.md` and `ISSUE-BACKLOG.md` to `~/.claude/` (core files, so a plain install skips them if they already exist, as for every core file). Each holds four `##` sections to fill: Handoff has What was tried, Relevant files and links, Done when, Who it is for; Backlog has the same first three, then Pick-up note.
- The distributed `CLAUDE.md` gains Core Rules item 10: before filing a GitHub issue, copy the matching template to a temporary file, fill every section in the copy, then run `gh issue create --title "<title>" --body-file <the copy>`. It never edits the installed template. As for every core file, a plain `superclaude install` leaves an existing `~/.claude/CLAUDE.md` alone; `--force` or `superclaude update` replaces it.
- No `sc:issue` skill or command is added, and the repository's own `.github/ISSUE_TEMPLATE` forms are unchanged.

### /sc:pr-submit: Codex reviews

- Codex support: review threads from the Codex connector (`chatgpt-codex-connector[bot]`) go through the same path as Augment's (re-grade, verify, troubleshoot, then fix, push, reply and resolve within the `--monitor` ceiling).
- Fail-open reviewer detection: a reviewer with no activity on the PR is recorded `reviewer_absent` and ignored. Augment-only PRs behave as before apart from that event, and Codex-only PRs now work. A present reviewer that does not complete by `--timeout` is recorded `reviewer_incomplete` when the other reviewer completed, and the other reviewer's result is used. If no reviewer completes and at least one showed activity, the run ends `terminal_timeout`; if no configured reviewer shows activity, it ends `terminal_augment_no_response`.
- P0-P3 mapping: a Codex finding's priority badge becomes its severity hint (P0 Critical, P1 High, P2 Medium, P3 Low), which the existing re-grade and routing then use; a missing or malformed badge falls back to Medium.
- Dedup: findings on the same path and line are routed at the group's highest tier and fixed once, and every verified member's thread is replied to and resolved.
- Per-reviewer re-trigger: after a push that fixes review findings (when the cycle applied edits), one re-trigger comment per present reviewer (`auggie review`, `@codex review`), each with its own watermark; a CI-fix push posts no re-trigger, and the decline fallback posts no second one.
- UNVERIFIED: whether Codex updates its summary marker after `@codex review` has not been observed. If it does not, the Codex re-review ends incomplete at `--timeout`; the other reviewer's result is used when it completed, otherwise the run ends `terminal_timeout`.

### ccsession: one session name for ccsession, Claude Code and Orca (#325)

#### Added (ccsession one name)

- `ccsession <name>` also gives Claude Code that name (`--name`), so the prompt box, the `/resume` picker, ccsession's list and the Orca tab show the same name.
- Claude Code's built-in `/rename <name>` names or renames a session for ccsession too, at no token cost. A new `hooks/session-name.sh` (UserPromptSubmit and SessionEnd; `session-start.sh` hands it SessionStart) copies the name into the repo's list: the session is then listed once, under its new name, and `ccsession <name>` reopens it. Claude Code runs no hook at a rename itself, so the list picks it up at the next message, or when the session ends. Only names someone gave are listed, never Claude Code's automatic ones.
- In an Orca tab whose title ccsession owns, a `/rename` sets the tab to `<name> · Claude Code` (`orca terminal rename`) at the next message. Leaving Claude Code (or, after a crash, the next ccsession launch in that tab) takes that title off again, only while the tab still shows it, so a title a person typed since stays.
- `ccsession --name <name>` takes any name, one starting with `-` too; `ccsession-orca` passes the answer to its question that way, so the question now accepts such a name.
- `superclaude install` (`ccsession --migrate-names`) adds, once per machine, the names given with `/rename` before ccsession kept them.
- `superclaude doctor` reports a missing UserPromptSubmit or SessionEnd ccsession hook; `install.sh` registers both.

#### Changed (ccsession one name)

- Session names may contain spaces and any other character except control characters (`ccsession "my work"`), up to 245 bytes of name file. In the name file, `%`, `/` and a leading `.` are written `%25`, `%2F` and `%2E` (so each counts as 3 bytes); a label an older version saved with a leading `.` is moved to that name at install, before the per-folder lists are copied, and copied to its repo's list when its old list was copied already. A name another saved session already has gets `-2`, `-3`... in the list; a lock on each list keeps two sessions renamed at the same moment from overwriting each other's entry.
- The `/ccsession-tag` command is retired: use `/rename`. Its `SKILL.md` stays, with `user-invocable: false` and `disable-model-invocation: true`, because `superclaude install` installs a skill folder only when it has one.

#### Fixed (ccsession one name)

- A `claude` started inside a ccsession session (for example a pipeline's `claude -p`) no longer takes over its name, even in the same folder, and never changes its Orca tab. ccsession replaces itself with Claude Code, so the launched Claude Code has the process id that starts `CCSESSION_LAUNCH_ID`; the hooks act for the launch only when that process runs them, `/clear` and resume included. A `ccsession` run from inside Claude Code leaves the Orca tab alone, and an untagged one no longer inherits the session's label.
- `superclaude install` over an older ccsession skill folder adds the new hook script, so the registered UserPromptSubmit and SessionEnd hooks never point at a missing file; `superclaude doctor` checks for it. The hook installer treats the standalone `install.sh` form of either ccsession hook as the same hook, so neither is registered twice.
- Renaming a session no longer leaves the old name behind in the list.

### MCP installer: LiteLLM gateway entry

- `superclaude mcp --servers litellm` registers the LiteLLM MCP gateway (`http://ibcore:4000/mcp/`) as an HTTP server with an `x-litellm-api-key: Bearer ${LITELLM_API_KEY}` header. The key stays a literal placeholder that Claude Code reads from the environment, so no key is stored. The entry is opt-in: the "all servers" choice skips it. The installer now supports HTTP entries, and compares URL and headers (not a command) to decide whether a registration is already up to date.

### Added: codegraph in commands, skills and agents; `/sc:impact` and `/sc:graph` (#323)

- New `/sc:impact <symbol>...` (or `--diff <base>`) lists what depends on the named symbols or on a diff: production and test dependents with shown/total counts, call sites checked by reading the code, and, with `--tests`, an advisory test list. It writes `impact.md` and `return-contract.yaml` and never stops its caller. `/sc:implement`, `/sc:pr-submit`, `/sc:troubleshoot --fix`, `/sc:auggie-review`, `/sc:task` (STRICT) and `/sc:reflect` call it for warnings and context only; no gate, severity or verdict changes.
- New `/sc:graph` reports whether this worktree's code-graph index is ready (version, pin, index state, worktree relation, counts). `/sc:graph init` is the manual indexing path for a worktree the session-start hook did not index; no skill or agent runs it.
- New shared guide `~/.claude/CODEGRAPH.md` (installed with the core files) holds the readiness check, the closed `graph:*` token list and the rules every primitive follows: codegraph answers are leads that are Read before they are cited, and the Grep/Read fallback always stays. Troubleshoot, reflect, validate-roadmap, brainstorm, cleanup-audit, auggie-review, task, tasklist and four agents now use codegraph above that fallback; `/sc:explain` gains a one-hop callers/callees view and `/sc:load` points to `/sc:graph status`.
- `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switches off codegraph use in commands, skills and agents only (they fall back to Grep/Read); `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` still switches off only the session-start index hook.

### Added: codegraph installed by default (#323)

- `superclaude install` (and so `./update.sh`) now has a required codegraph phase. It reuses a codegraph `1.6.2` already on `PATH` or in `~/.local/bin`; otherwise it downloads the pinned `v1.6.2` release for Linux or macOS (x64 or arm64), checks its SHA-256 against the value pinned in the source, and installs it under `~/.codegraph/versions/v1.6.2/`. It never runs upstream's installer. A failure keeps the rest of the install and exits 1, naming the failed stage.
- It registers codegraph at user scope with telemetry and update checks off and `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`, which lists seven narrow tools and hides `codegraph_explore` (about 1,861 extra tokens per session in four headless runs; the 2,000-token limit is still a proposal). An entry IronClaude wrote is repaired; one you changed is kept.
- A `SessionStart` (startup) hook starts one background `codegraph init --yes` in a git checkout that has no `.codegraph/codegraph.db`, so each clone and worktree is indexed on its first session. Costs: about 70 KB per indexed file and up to about 1 GB of memory during the first init. `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` turns off this hook only (recommended for CI and headless pipelines).
- `superclaude install --list` prints a codegraph block (executable, owner, registration, `Ready for Serena retirement`), and `superclaude doctor` gains a "codegraph MCP registration" check that fails only when the registered command no longer exists. Remove codegraph with `claude mcp remove codegraph --scope user` and delete the paths `install --list` prints as owned. `.codegraph/` is now git-ignored in this repository.
- Once codegraph is registered and usable, the same `superclaude install` run also removes the Serena launcher registrations (`serena` and any renamed launcher except `serena-local`, with `env` and `headers` absent or empty) and the `~/.local/bin/codebase-memory-mcp` registration; the binary and its client companions stay. Register Serena as `serena-local` to keep it.
- Guidance for agents is in the core `CLAUDE.md` (a `codegraph` row and a block between `SUPERCLAUDE_CODEGRAPH_BEGIN` and `SUPERCLAUDE_CODEGRAPH_END`). See the [MCP installation guide](docs/user-guide/mcp-installation.md#default-setup-codegraph).

### Breaking: codebase-memory-mcp and Serena removed; session memory moves to `.superclaude/memory/` files (#323)

#### Removed (codebase-memory-mcp and Serena)

- `superclaude install` no longer installs codebase-memory-mcp (no download, no native setup, no required phase, no exit 1 for it). The installer module is deleted.
- `superclaude mcp` loses `--uninstall` and `--yes`. Its menu is now "1. Install MCP servers (default)" and "2. Cancel". `codebase-memory-mcp` and `serena` are no longer registry servers: `superclaude mcp --servers serena` now says "Unknown MCP server selection: serena".
- Serena is gone from the MCP registry, the package assets, the freshness hook matcher and the primitives' tool steps. Every command, skill and agent that used Serena symbol, reference, diagnostics or memory tools now uses a native Grep/Read floor.
- Serena session memory is replaced by plain markdown files under `<project>/.superclaude/memory/` (one store per worktree). `/sc:save`, `/sc:load`, `/sc:pm` and the PM agent read and write those files. For one release `/sc:load` still reads an existing project `.serena/memories/<key>.md` when the matching `.superclaude/memory/` file is absent; it never writes there and tells you that folder is read-only history.
- `/sc:reflect` loses `--onboard` and `--with-hierarchy`.

#### Added (retire step)

- At its end, `superclaude install` runs a bounded, non-fatal retire step (10 seconds per `claude` call, 15 seconds for the whole step; no outcome changes the install exit code). It removes only **user-scope** registrations of `codebase-memory-mcp` and `serena` that IronClaude can prove it wrote, plus IronClaude's own receipt and marker files (`~/.local/bin/.superclaude-codebase-memory.json` and `.pending`) once their binary is gone.
- It keeps every shape it cannot prove (for example a registration Coder's bundle also writes) and prints the reason it was kept; for the legacy Serena launcher registration it also prints the exact `claude mcp remove serena --scope user` command. Local-scope and project `.mcp.json` entries are never touched.
- It never touches binaries, uv tools, indexes, caches or memories.
- The current-pin Serena registration (`uvx --from serena-agent==1.7.0 ...`) is not kept for good: it is kept, with the removal command printed on each install, only until the first `superclaude install` run in which the codegraph tools are installed and ready; that run removes it.
- `superclaude install --list` shows one line per retired name (absent, will be removed, or kept with the reason). `superclaude doctor` warns, never fails, when something removable is left. `superclaude update` only prints "legacy registration present: run `superclaude install`".
- After a removal, restart running Claude sessions: a running session can write the entry back. Check with `superclaude install --list`.

#### Manual cleanup (IronClaude does not do these)

To keep using Serena yourself, register it under the name `serena-local`, which the installer never removes:

```bash
claude mcp add --scope user serena-local -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false
```

For a codebase-memory you or IronClaude installed under `~/.local/bin` (this removes its own client companions and keeps its indexes; use the absolute path, because a bare command could resolve to Coder's copy):

```bash
"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"
```

If you installed Serena as a uv tool yourself (Coder workspaces reinstall it at start):

```bash
uv tool uninstall serena-agent
```

To remove a registration the retire step kept:

```bash
claude mcp remove codebase-memory-mcp --scope user
claude mcp remove serena --scope user
```

Delete the data only if you no longer need it; IronClaude never deletes it:

```bash
rm -rf ~/.cache/codebase-memory-mcp   # codebase-memory indexes
rm -rf ~/.serena                      # Serena's user data; project .serena/ folders are yours to delete
```

### ccsession: tiers by Coder role, letter tier names, and the new tier layout

#### Added (ccsession tier rules)

- `CCSESSION_TIER_RULES` in the workspace env file: space-separated `<who>=<start tier>[:<tier>,...][+models]` entries, where `<who>` is a Coder username, `role:<coder role>` (for example `role:auditor`) or `*` for everyone else, including a terminal that does not know its owner. A username entry wins, then the first matching role entry, then `*`. Roles come from `CODER_WORKSPACE_OWNER_ROLES` (comma-separated, set by the Coder template). `+models` also lists each model of the owner's tiers in `/model`, ordered by the new `CCSESSION_MODEL_ORDER` setting. The line follows the same one-line rule as `CCSESSION_ACCESS`; a broken entry that applies to the owner stops the launch rather than opening every tier.
- Tier names may end in a letter: `tier1a`, `tier1b` (env names `T1a_WINDOW`, `T1aModel01`, picker id `claude-gw-tier1a`). `--tier 1A` works.

#### Changed (ccsession tier rules)

- `ccsession-models.json` (2026-10-28.1) defines the owner's layout: Tier 0, Tier 1a (Opus 5.5, Sonnet 5.5), Tier 1b (Sonnet 5.5, GPT-6.1 Sol, Muse Wonder Full), Tier 2 (GPT-6.1 Sol, GLM-5.3, Grok 4.7, Qwen3.8 Max, Muse Wonder, Muse Spark), Tier 3 (GPT-6.1 Terra, then Tier 2's other five) and Tier 4 (GPT-6 Luna). The models and windows themselves stay in the workspace env file. Older ccsession rejects this data (it cannot read letter tier names) and keeps its own copy, so it keeps working with an env file that still has the old `T1Model0N` slots.
- `CCSESSION_ACCESS` is now the older form, read only when the env file has no `CCSESSION_TIER_RULES` line. Older ccsession reads only `CCSESSION_ACCESS` and ignores the new settings.
- The workspace owner's roles are part of the shim settings, so owners with different roles never share a shim.
- The ccsession tests clear the workspace owner and access settings, so they also pass inside a Coder workspace.

#### Fixed (ccsession tier rules)

- A model launched by name (`--model`) takes its window from the first tier slot that names it, in tier order, the same window `/model` uses. Before, it took the first matching slot in name order, so the old `T1Model0N` slots kept in the env file for older ccsession could give `--model claude-opus-5-5` a different window from `/model`.
- The docs say a plain member's Coder roles are `member` (not none), and that older ccsession understands only username entries in `CCSESSION_ACCESS`, so `role:` and `*` entries belong in `CCSESSION_TIER_RULES`.

### ccsession: session names belong to the repo, not the folder

#### Changed (ccsession names per repo)

- Session names are shared by every worktree, branch and copy of a repo. A name started in one worktree is listed and resumed from any other, and a fresh copy of the repo (for example Orca adding the project again as a new folder) still sees its names. Names stay where they always were (`~/.claude/projects/<key>/topics/<name>.txt`) and the key is made by the same function (`/` becomes `-`); only its input changed: the repo's network `origin` as host and path (credentials, port, query, host case and a trailing `.git` ignored, for example `github.com-IronbellyOrg-IronClaude`), else the main worktree's folder for a repo without a network origin (none, or a local-path or relative origin; for a separate or bare git folder, that folder), else the current folder outside git (unchanged). `ccsession`, `--here`, `--rm`, the session-name question, the SessionStart hook and `/ccsession-tag` all use it, and listings find each conversation under whichever folder it ran in. Claude Code already resumes a session from any folder.
- The SessionStart hook saves a name only for the Claude that ccsession started in its own folder, so a Claude started elsewhere that inherits the label (for example a pipeline in another worktree of the same repo) no longer takes the name over.

#### Added (ccsession names per repo)

- `ccsession --key` prints the name-list key for the current folder; the SessionStart hook and `/ccsession-tag` use it so all three agree.
- `ccsession --migrate-names` copies names that older versions saved per folder into their repo's list, once per old list (each copied list is marked, so a name removed with `--rm` stays removed). It runs by itself on first use; `superclaude install` and the skill's `install.sh` run it too, which retries only lists that failed. Copies only: the old files stay but drop out of `--list`, nothing is overwritten, the most recently used folder keeps a shared name, another session with that name is copied as `<name>-<folder>` (then `-2`, `-3`), and lists whose folder no longer exists are skipped. A repo's own list is never treated as an old one.

### ccsession — per-user start tier and tier list (`CCSESSION_ACCESS`)

#### Added (ccsession)

- In Coder workspaces, `CCSESSION_ACCESS` in the workspace env file (`defaults.sh`) sets, per Coder username, the tier ccsession starts on and the tiers it offers: space-separated `<username>=<start tier>[:<tier>,<tier>,...]` entries, no tier list meaning every tier. The owner is read from `CODER_WORKSPACE_OWNER_NAME` (set by the Coder agent). A user who is not listed starts on `CCSESSION_DEFAULT_TIER` with every tier, as before. For a limited user, `--help`, the shim's `/model` list and the shim's tier routing cover only their tiers, and `--tier` / `--model` refuse anything outside them. A broken or repeated entry for the current user stops the launch with the reason; a piece of the value that is not a `name=...` entry, a `${...}` value, or the name on any line other than that one export (comments included) stops every launch that has an owner name. `ccsession --models-status` shows the owner's access, and a launch notes when `CCSESSION_ACCESS` is set but the owner is unknown. Each owner name gets its own shim. The env file reader now also drops a trailing ` # comment` after a value, splits lines at newlines only, and no longer discards the whole file for a byte that is not UTF-8, as bash does. The limit is advisory: the owner can undo it from their own environment or call a model with their gateway key; only a gateway key limited to those models enforces it.

### ccsession: sessions stay listed in Orca Web and on phones

#### Fixed (ccsession Orca title)

- In an Orca terminal (`ORCA_PANE_KEY` set), ccsession now sets the tab title to `<label> · Claude Code`, or `Claude Code` for an untagged session, and starts Claude Code with `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` so Claude Code keeps that title. Orca's web and mobile server decides that a pane still runs Claude by reading the word "claude" in its title. Claude Code's own title is its AI conversation name, without a ✳ in Orca, so a resumed session that already had a name dropped out of the Orca Web sidebar and the phone at once (or showed an unclickable row), and a new one dropped after any answer that used no tool. The Orca desktop app reads Claude's status directly and was never affected. Other terminals keep Claude Code's own titles. A `claude --resume` started without ccsession is not covered.

### ccsession: Orca's Claude launches go through ccsession and ask for a session name

#### Added (ccsession Orca launch)

- `ccsession-orca`, installed and linked into `~/.local/bin/ccsession-orca` next to `ccsession` (by `superclaude install` and by the skill's `install.sh`). Set it as Orca's **Settings > Agents > Claude > Command** so picking Claude directly in Orca starts through ccsession (shim, tier model settings, one credential) instead of bare `claude`. It lists this folder's saved sessions and asks `Session name (Enter or Ctrl+C = untagged; untagged after 30s):`; a name runs `ccsession <name> --shim`, Enter, Ctrl+C or no answer within `CCSESSION_ASK_TIMEOUT` seconds (default 30, `0` for no limit) runs `ccsession --shim`. The limit keeps Orca's supervised workers starting: Orca launches them with the same command and fails one whose Claude is not ready within 60 seconds. It does not ask when Orca resumes or continues a session (`--resume`, `--fork-session`, `--continue`), without a terminal, when keys were already typed into the tab, or with `CCSESSION_AUTOSTART=0`. Orca's prompt, `--prefill <text>` and resume flags reach Claude Code unchanged. If an older ccsession skill is still installed, `superclaude install` wires `ccsession` as before and warns that `superclaude update` adds `ccsession-orca`; `superclaude doctor` checks the new link.
- `ccsession --ask [<hint>]`: the session-name question as one command, for `ccsession-orca` and the Coder New Terminal hook. It prints the saved-session list and the question on the terminal and only the chosen name on standard output (empty for untagged), asks again after an invalid name, and exits 1 when it did not ask, got no answer within `CCSESSION_ASK_TIMEOUT` seconds (unset or `0`: no limit) or input ended, 130 on Ctrl+C.
- `ccsession ... --claude-args <claude args>`: everything after `--claude-args` goes to Claude Code exactly as given, after any label, and is never read as a label or a ccsession option. A plain `--` is still passed on to Claude Code as before.

#### Changed (ccsession Orca launch)

- `/ccsession-tag` and the session-name question no longer accept a name that starts with `-`. `ccsession -name` always read such a name as an option, so it could never be resumed. `ccsession --rm` still removes an existing one.

### pr-submit — origin-first target, `--pr`, dead hook references and `--yes` removed

#### Fixed (pr-submit cleanup)

- `/sc:pr-submit` now takes the target repo from the `origin` remote before anything is created, uses `gh repo view` only when origin has no URL, and reads the base branch with `gh repo view "$REPO"`. Before, it asked `gh repo view` first, which prefers an `upstream` remote, so a PR could be opened on the public parent before the post-create check caught it. The four helper scripts (`poll-augment-review.sh`, `poll-ci-checks.sh`, `reply-resolve-thread.sh`, `retrigger-review.sh`) resolve the repo in the same order when called without `--repo`.
- `/sc:pr-submit` accepts `--pr <N>` to attach to an existing PR. `superclaude reflect contract-status` already printed `/sc:pr-submit --monitor 3 --pr <N>`, which the parser used to reject.
- At `--monitor 1` and above, `/sc:pr-submit` now checks that your checkout is the PR's head before it monitors, edits or pushes, on both the `--head` create path and the `--pr` attach path. It reads `headRefName`/`headRefOid` from the PR and halts on a mismatch, with steps to fix it. Both pushes (review fixes and CI fixes) go to that PR branch. A guard halts before each push, including a push re-driven after a crash, if the PR head moved during the run, or if the commit to push is not exactly one commit on top of the PR head, so a push never publishes unreviewed local commits along with the fix. Before, the push branch was never taken from the PR. `--pr` never rebases the already-published PR head, at any level, and force-pushing is explicitly forbidden. New pure checks: `pr_head_ok`, `pr_branch_ok` and `push_parent_ok` in `superclaude.pr_submit.fsm`. `--monitor 0` is unchanged.

#### Removed (pr-submit cleanup)

- References to the `offer-pr-review.sh` PR-creation hook, which no longer exists: the activation paths in `/sc:pr-submit` and `/sc:auggie-review`, the auggie-review hook example, a comment in `install_hooks.py`, and the leftover `tests/pr_submit/test_hook_update.py` helper.
- The `--yes` flag of `/sc:pr-submit`. It was accepted but never read.

### pr-submit — default monitor level 3; every PR instruction uses `--monitor 3`

#### Changed (pr-submit)

- `/sc:pr-submit` with no `--monitor` now runs level 3 (`DEFAULT_MONITOR = 3` in `superclaude.pr_submit.fsm`). A bare `/sc:pr-submit` now fixes the confirmed review findings of Medium severity or higher (lower ones are only reported) and failing CI checks, pushes the fixes to your branch without asking, and replies to and resolves the review comments it fixed. Use `--monitor 2` to make the fixes locally and stop before pushing, or `--monitor 0` to only open the PR. The command file had already said "default 3" since `2165ae25`; the code, the skill and the options table now agree.
- The repository `CLAUDE.md`, the routing guide (`HOW-WE-WORK.md`, review-pr row and section 3.11), the PRD and TDD release guides, and `docs/developer-guide/contributing-code.md` now say to open PRs with `/sc:pr-submit --monitor 3` (the guides previously said `--monitor 1`). `gh pr create --repo IronbellyOrg/IronClaude ...` remains as the fallback when `/sc:pr-submit` cannot run. `docs/user-guide/commands.md` now states the level-3 default.
- `CLAUDE.md` adds a pre-PR check that `gh repo view` reports `IronbellyOrg/IronClaude`, because gh prefers an `upstream` remote over `origin`.
- The routing guide's "Never push without approval" rule now names the one exception: after the approved push, `/sc:pr-submit --monitor 3` pushes its review and CI fixes without asking again (`--monitor 2` stops before pushing).
- `refs/state-machine.md` §5.3 no longer describes a one-time confirmation before the first push: no wave ever performed it.
- The pull request template now asks for `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude` and a rebase onto `origin/master`, instead of an upstream PR and `upstream/main`.
- The routing guide's mandated per-step flags are called "required flags" instead of "safe flags" (`CLAUDE.md`, `/sc:help`, `docs/user-guide/how-we-work.md`, and the routing-table test), since `--monitor 3` is not a propose-only setting.
- `superclaude reflect contract-status` now suggests `/sc:pr-submit --monitor 3` as the next command once the detection contract is ready.

### routing — one "how we work" guide for which tool to use when; retired unused core files

#### Added (routing)

- `HOW-WE-WORK.md`, the single guide for which command or skill to use for each kind of work, in what order, and with which safe flags. `superclaude install` and `superclaude update` copy it to `~/.claude/HOW-WE-WORK.md`. The plugin source tree `plugins/superclaude/` now also carries it inside the `sc-recommend` skill (`skills/sc-recommend/refs/HOW-WE-WORK.md`) for the next plugin build; the plugin that can be installed today (the repository-root `.claude-plugin/`) does not include it, and `make build-plugin` also needs `plugins/superclaude/manifest/metadata.json`, which is missing. Until a plugin build ships it, get the guide with `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install`. It ends with a machine-readable routing table that `/sc:recommend` reads; `/sc:help` prints its six-level table. It is never `@`-imported, so it costs no context until something reads it.
- `docs/user-guide/how-we-work.md`, a short page pointing to the guide.
- The `sc-recommend` skill and up-to-date `help` and `recommend` commands in the Claude Code plugin source tree (`plugins/superclaude/`), for the next plugin build.

#### Changed (routing)

- `~/.claude/CLAUDE.md` gains a short routing block: the six levels, the hard limit on unplanned changes, and the rule that a `/sc:<name>` message whose command file names a skill must load that skill first (commands whose file names no skill run from their own file). It no longer contains the persona table, the "Skills & Commands" section with its wave-strategies claim, the Key Docs pointers to `PLANNING.md`, `TASK.md` and `KNOWLEDGE.md`, or the IronClaude-contributor sections (Project Structure, Dev Commands, Component Sync, and the "Component edits" core rule); the repository's own `CLAUDE.md` covers the contributor material. A plain `superclaude install` never overwrites a file that already exists in `~/.claude/`: it adds `HOW-WE-WORK.md` the first time, but it does not replace an existing `CLAUDE.md`, and it does not refresh `HOW-WE-WORK.md` in later releases. Run `superclaude update` (or `superclaude install --force`) to get the new `CLAUDE.md` and the latest guide. Warning: both overwrite every file they ship, including an edited `~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, keep no backup, and delete and re-copy each shipped skill folder in `~/.claude/skills/`, so files you added inside one are lost. Back up any file you changed or added first (for example `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`), then re-apply your changes.
- `/sc:help` lists the commands and skills that are actually installed, read live, prints the guide's level table, and points to the guide and `/sc:recommend`. Its flag reference moved to `docs/user-guide/flags.md`.
- `/sc:recommend` reads the guide first. When the goal matches a row of the routing table it returns that row's steps in order, with every flag the guide makes mandatory. It also searches `~/.claude/` and the project's `.claude/` folder, not only an IronClaude checkout's `src/`, and it skips its cache step outside an IronClaude checkout: the `superclaude recommend` CLI is installed everywhere, but the cache fingerprint is computed over a checkout's `src/superclaude/` (plus the installed and project command, skill and agent folders, so installing a command invalidates old answers) and the cache lives in that project's `.claude/cache/`.
- `RULES.md` no longer claims the PM agent activates on its own; it runs only when you invoke `/sc:pm` or delegate to it.
- The `/sc:recommend` classifier key `tasklist-generation` is renamed `task-file-generation`; old cache rows for it are discarded once.
- `docs/user-guide/commands.md` is now a per-command reference only, with a "Changes files?" column; `docs/getting-started/quick-start.md` now points to the guide.
- `commands/README.md` is no longer installed, so new installs no longer show a `/sc:README` command. An existing `~/.claude/commands/sc/README.md` is left in place; delete it yourself if you like.

#### Removed (routing)

- Core files no longer shipped: `ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md`, `MCP.md`, and the plugin copy of `FLAGS.md`. The shipped `CLAUDE.md` has not imported any of them since 2026-03-16; their routing content now lives in the guide. `BUSINESS_SYMBOLS.md` is unchanged (decision 5). Copies of the retired files already in your `~/.claude/` are left in place; nothing loads them, so you can delete them yourself.
- Docs superseded by the guide: `docs/reference/examples-cookbook.md`, `basic-examples.md`, `advanced-workflows.md`, `advanced-patterns.md`, `integration-patterns.md`, `commands-list.md`, `suggested-commands.md`, `comprehensive-features.md`; `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (a duplicate of the copy kept in `docs/developer-guide/`); `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`.

### remediation routing — sc:workflow/sc:implement by default; task-builder//task only with `--depth deep`

#### Changed

- `sc:troubleshoot --fix`, `sc:reflect --remediate`, and the `sc:auggie-review` remediation offer now build a phased tasklist through `sc:workflow` (`--handoff none`), which writes it as a managed `.dev/tasks/to-do/<id>/<id>.md` package and reuses its own built-in advisory `/sc:reflect --mode pre` review (no separate reflect call on the plan), and surface a user-run `/sc:implement <id>.md`. The `task-builder` → `/task` chain is used only with `--depth deep` (`--fix --depth deep` / `--remediate --depth deep` / review `--depth deep`). Nothing auto-executes.
- `sc:troubleshoot --diagnosability-handoff` packages the diagnosability tasklist via `sc:workflow` instead of `task-builder`.
- reflect return contract bumped **`1.7.0 → 1.8.0`** (additive): new `remediation_plan_path` (plan-route sibling of `remediation_task_path`).
- `superclaude reflect run --fix`: the auto-fix loop applies `/sc:implement <remediation_plan_path>` on the plan route and `/task <remediation_task_path>` on the MDTM route (`--depth deep`); the MDTM pointer wins if both are set.
- `sc:workflow` source files built by remediation handoffs flatten numbered/checkbox lines (the workflow gate rejects them).

### reflect — D13 coverage hardening: inference-assisted extraction + parse-density guard (contract 1.5.0)

#### Added (reflect skill)

- Two-pass requirement extraction (`sc-reflect-protocol` SKILL.md Step 1B.0): Pass 1 stays deterministic/LLM-free (regex ID extraction + range-notation expansion, e.g. `SPEC-001..021` → 21 IDs); Pass 2 reads the full spec body and enumerates requirement-shaped content Pass 1 missed, emitting synthetic `INF-NNN` rows that each MUST carry a verbatim quote + `file:line` citation (an inferred row missing either is dropped at emission and never enters the matrix).
- Parse-density guard (Step 1B.2b): when `inferred_count > parsed_count` (sparse labeling relative to requirement content), emits `coverage_degraded: parsed-sparse` and forbids the Tier-1 stop — a table-wide §5.3 pre-filter routing to Tier 2 (explicit `--tier 1` / `--depth quick` pins still override, with a loud WARN).
- Wave-5 evidence-validator now polices inferred rows identically: an `INF-NNN` row whose quote does not match its cited spec lines is dropped, counted in `citations_dropped`, and `coverage_pct_union` / `unmapped_requirements_union` / `S_dev_density` are recomputed over the surviving union before the report finalizes.

#### Changed (reflect skill)

- Return contract bumped **`1.4.0 → 1.5.0`** (§9.4 additive-only): NEW fields `coverage_pct_union`, `unmapped_requirements_union`, `coverage_degraded`. `coverage_pct` and `unmapped_requirements` KEEP pre-D13 parsed-only semantics, so existing consumers need no change (major-only CLI validator tolerates the minor bump).

### reflect — audit-only wrapper → bounded auto-fix engine (contract 1.4.0)

#### Added (reflect CLI)

- `--fix/--no-fix` flag on `superclaude reflect run` (Click default **`--no-fix`**, i.e. audit-only; the O1/O2 gate callers pass `--fix` explicitly — "gate default --fix" refers to the gate-invocation convention, not the bare-CLI default). When `--fix`, the audit runs with `--remediate` so reflect *authors* (never runs) a Tier-3 corrective MDTM file; on an AUTO-FIXABLE verdict with a present `remediation_task_path`, the wrapper auto-executes `/task <path>` as its own top-level `claude --print` subprocess, then re-runs the audit to verify. Reflect stays read-only; the wrapper is the sole mutator-orchestrator.
- `--max-fix-iterations N` flag (default **2**): bounds the audit→apply→re-verify loop. After N apply→verify cycles without convergence to PASS, terminal HALT (exit 10), no promote; the sidecar records `fix_iterations` and `fix_converged: bool`.
- `--base <ref>` flag (highest precedence). Resolution chain in `config.py`: **explicit `--base` > frontmatter `start_commit` > `git merge-base HEAD master`**. A phase-N gate passes `--base <phase-N-start-sha>` to audit only phase-N work. The F3 de-range is preserved: `--diff <BASE>` is a SINGLE ref vs the working tree, never a `<BASE>..HEAD` commit range.
- `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion breaker: the wrapper exports `=1` into every child it spawns inside the fix subtree (the reflect audit subprocess AND every auto-run `/task`). The primary breaker lives in the `reflect` **group callback**, which runs during Click parsing — so a nested `superclaude reflect run` immediately **exits 0** ("nested gate suppressed") BEFORE the `run` subcommand's `exists=True` tasklist-arg validation, even when the file has since moved. Truthiness is exactly the string `"1"`.
- Pure `classify_fix` carve-out (`contract.py`) off existing contract fields only: **AUTO-FIXABLE** ⇔ HALTED caused solely by `drift>0` and/or `necessary`-class items with no `regression_present`, `needs_human_decision`, `user_decision_required`, or grounding-gaps; **HUMAN-REQUIRED** ⇔ any of those triggers (or a `degraded`/`blocked` verdict). Auto-fix applies to the AUTO-FIXABLE path only.
- `remediation_task_path` contract field — reflect's Wave 6 emits the absolute path of the MDTM file `rf-task-builder` wrote (null when none authored) into `return-contract.yaml`; the wrapper reads it to auto-execute rather than guessing the newest `TASK-RF-*` dir. Skill `sc-reflect-protocol` contract bumped **`1.3.0 → 1.4.0`**.
- Headless `--remediate` auto-authoring: under `--print` (wrapper) mode there is no human to "accept" a Tier-3 offer, so `--remediate` authors the corrective file non-interactively and sets `remediation_task_path`. A HUMAN-REQUIRED deviation set still authors nothing auto-runnable (BUILD_REQUEST with `needs_human_decision: true`) and the wrapper HALTs.

#### Changed (reflect CLI)

- `--promote/--no-promote` default flipped **`False → True`** (FR-5): promote-by-default. The wrapper never force-sets `--no-promote` — it has no O2-detection surface, so the **generator** passes `--no-promote` explicitly on its O2 per-phase gate calls; a defaulted O2 promote is a harmless no-op (reflect's Wave-7 finds no per-phase adapter and safely skips `adapter-unresolved`), never a mis-promote.
- `_build_inner_command` now forwards `--promote/--no-promote` **and** `--base` explicitly under `--tmux`, so a `--tmux + --no-promote` (or `--tmux + --base`) outer call does not silently default to promote-on or lose the base ref in the inner foreground reinvocation.

#### Guarantees (reflect CLI)

- Fail-closed: DEGRADED and BLOCKED verdicts are never auto-fixed; a failed `/task` apply HALTs (never silently passes); thinness holds (no `cli.sprint`/`cli.roadmap` import, no `async`, `ClaudeProcess`-only launch). Test suite: **75 passed / 1 justified xfail**.

### Sprint CLI — wire the per-task execution path + runner-owned typed handoff (Stages 0-3, TASK-RF-SPRINTCLI-WIRE-DEAD-20260603-024610)

#### Added (sprint CLI)

- `--handoff/--no-handoff` flag on `superclaude sprint run` (default: **enabled**). When enabled, the per-task execution path writes one typed `HandoffRecord` JSON per task and a `task_complete` ledger event; `--no-handoff` reproduces legacy behavior exactly (no handoff records, no `task_complete` events). Threaded through all three layers (`commands.py` click option → `load_sprint_config` → `SprintConfig.handoff_enabled`).
- `--resume <task_id>` flag on `superclaude sprint run`: resumes a per-task sprint by skipping *validated-successful* tasks (handoff record with `status == "pass"` AND a successful gate outcome). The argument is a `T<PP>.<TT>` task id; it composes with the phase-granular `--start/--end` (those bound the phase range, the validated-success skip suppresses already-done tasks within it). Resuming against a pre-Stage-1 `release_dir` (no `handoff/` directory) degrades gracefully to phase-granular behavior. Non-success tasks (`FAIL_*`/`INCOMPLETE`/`SKIPPED`, PASS-with-gate-fail) are never skipped.
- `handoff/` results subdirectory: per-task handoff records are persisted to `<results_dir>/handoff/phase-{N}-task-{task_id}.json` (phase-qualified key, since the bare `T<PP>.<TT>` id is not sprint-unique). Written via an atomic temp+replace `FileHandoffStore` (`src/superclaude/cli/sprint/handoff.py`).
- `task_complete` execution-log JSONL event — the first-run sibling of `task_rerun_complete`, with the identical field set `{event, phase, task_id, status, turns, duration_sec, timestamp}` (discriminator: `task_complete` = first run, `task_rerun_complete` = rerun).
- Typed, schema-versioned `HandoffRecord` dataclass (`models.py`) constructed by the runner from each finalized `TaskResult` plus `produced_artifacts[]`/`consumed_upstreams[]`; forward-compatible (`from_dict` tolerates unknown keys).
- `--task-parallelism K` flag on `superclaude sprint run` (default: **1 = sequential**). `K > 1` executes up to `K` tasks concurrently per dependency wave (topological order built on the existing `rerun_tasks` dependency-edge shape; cycles surfaced, not dropped). Concurrency is made safe by a lock-guarded `SprintLogger._jsonl`, a lock-guarded `TurnLedger` with an atomic `try_launch` (prevents budget over-commit), and per-task atomic handoff-file writes. `K = 1` preserves byte-identical legacy behavior.

#### Changed (sprint CLI)

- Per-task subprocesses now receive full per-task isolation env (own `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR` under `<results_dir>/.isolation`), and the per-phase fallback path additionally seeds the two settings/plugin keys while keeping its phase-scoped `CLAUDE_WORK_DIR`.
- Per-task `turns_consumed` is now parsed from the stream-json terminal `result` event's `num_turns` (previously hard-coded `0`).
- Prior-task context (`build_task_context`) is now injected into each per-task prompt.
- The per-task heading router emits a warn-only near-miss diagnostic when a phase file has headings that look like `### T<PP>.<TT>` but miss the strict format (it never reclassifies the phase).

### sprint — auto-resume as the default for `run` / `rerun-tasks` (v4.3.5, TASK-RF-20260602-sprint-auto-resume)

#### Behavior change (READ THIS if you script `superclaude sprint`)

- **`superclaude sprint run <index>` with no `--start/--end` now AUTO-RESUMES.** An interrupted sprint is detected from on-disk state (the atomic `phase-N-result.json` is the truth anchor) and resumes at the boundary phase, re-running only the unfinished task on the task-level path. Before proceeding it prints the resume plan + drift + integrity report and (interactively) asks for confirmation.
- **`superclaude sprint rerun-tasks <index>` with no `--phase/--tasks/--from-reflect-report` now AUTO-DETECTS** the boundary phase and its recoverable failed-task set, then runs exactly as if those flags had been supplied (identical result to the explicit invocation).
- **Opt-out / explicit control is unchanged.** An explicit `--start`/`--end` (run) or `--phase`/`--tasks` (rerun-tasks) — *including `--start 1`* — disables auto-detection and preserves today's exact behavior (detected via Click parameter source, not value comparison). `--fresh` (alias `--restart`) ignores prior on-disk state and runs clean from phase 1.
- **CI / non-interactive:** pass `--yes` (or set `SUPERCLAUDE_SPRINT_ASSUME_YES=1` / `CI=1`) to skip the confirmation prompt. A non-interactive session without assent stops with guidance rather than hanging.

#### Added (sprint auto-resume)

- New read-first package `src/superclaude/cli/sprint/resume/`:
  - `planner.py` (`ResumePlanner`) — pure-read reconstruction of the resume plan from `execution-log.jsonl` + `phase-N-result.json` + transcripts. `result.json` presence with a PASS-family status is the authoritative phase-completion signal (a torn/dropped ledger line cannot demote it). Flags ambiguous state (multiple plausible release dirs / interleaved ledger / unreadable core files) and refuses to auto-pick.
  - `drift.py` (`DriftAssessor`) — tiered safety-of-resume scoring. Tier 0 exact normalized-content hash match; Tier 1 whitespace-insensitive cosmetic + structural task-ID diff (only the 0.8 confidence boundary gates resume); Tier 2 additive `git diff` annotation behind a capability check.
  - `integrity.py` (`BoundaryIntegrityGate`) — the resume-seam safety gate. Doubly-validates the last-completed task (persisted status ∧ transcript re-derivation ∧ artifact existence), surfaces next-unfinished partial work, and offers opt-in reversible copy-to-quarantine. The gate verdict is a pure function of deterministic signals; an advisory coherence read can annotate but never change it.
  - `models.py` — `ResumePlan`, `BoundaryReport`, `DriftAssessment`, `BoundaryTask`, `Granularity`, `ResumeDecision`.
- `--fresh` / `--restart`, `--yes` / `-y` flags on both `sprint run` and `sprint rerun-tasks`.
- `phase-N-result.json` now records `tasklist_sha256` (normalized-content hash of the per-phase tasklist) so a later resume can detect drift. Backward-compatible: result files written before v4.3.5 simply lack the key and resume falls back to structural drift scoring.

#### Safety properties

- **Non-destructive by default (NFR-1):** the integrity gate performs zero `results/` mutation unless cleanup is opted into; quarantine is a `shutil.copy2` (originals untouched), lock-guarded, audit-logged, and reversible by the existing `rerun-tasks --restore` (`restore_from_bundle`).
- **LLM is advisory-only (NFR-3):** the coherence read is CI-safe (empty verdict when `claude` is absent/times out) and can never flip the gate verdict.

#### Validated (sprint auto-resume)

- 17 deterministic unit/integration tests (`tests/sprint/test_resume.py`) mapping 1:1 to AC-1..AC-9 + the validator-corrected invariants (INV-001 same-fn hash, FR-2.5 non-destructive/reversible quarantine, DD-2 advisory-only coherence) + a mutation-proved hard-STOP guard.
- 3 real-`claude`-subprocess e2e tests (`tests/sprint/e2e_real/test_e2e_resume.py`) proving bare `rerun-tasks` auto-detect, bare `sprint run` task-level auto-resume, and hard-crash phase-level re-run end-to-end.
- Five in-band phase-gate `rf-qa` reviews (adversarial, fix-authorized) + Phase-4 caught a runtime-only dispatch defect (missing `run_rerun_tasks` kwargs) that mocked tests had hidden.

### sc:cleanup-audit — bake hidden + BMAD scope exclusions into defaults (TASK-RF-20260529-162751)

#### Added (sc:cleanup-audit)

- `DEFAULT_EXCLUDES` regex floor in `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`: hidden paths (any leading-`.` or `/.` segment), BMAD directories (`_bmad/`, `_bmad-output/`, `_planning-input/`), and audit output (`.claude-audit/`). Applied to BOTH the `git ls-files` branch and the `find` fallback branch via a shared `apply_scope()` filter — every downstream artifact (type distribution, domain classification, batch assignments, summary) inherits the filter automatically.
- Per-project override mechanism: `.claude-audit/SCOPE.md` lines of the form `EXCLUDE: <regex>` are added to the exclusion set. Default exclusions cannot be removed — they are a floor, not a ceiling. Override file path is configurable via `SCOPE_FILE` env var.
- `=== ACTIVE SCOPE RULES ===` diagnostic block emitted at the top of `repo-inventory.sh` output so operators can see what was excluded without re-deriving the regex.
- "Default scope exclusions" paragraph under the Discover step + "Scope Floor" Key Patterns bullet in `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` documenting the new floor + per-project override semantics.
- "Scope rule (inherited from `repo-inventory.sh`)" defense-in-depth section in `rules/pass{1,2,3}-*.md` so audit-scanner / audit-analyzer / audit-comparator subagents don't classify out-of-scope paths even if a leaked path appears in a grep result.
- `In-scope after default excludes:` line in the `## Repository Context` block of `src/superclaude/commands/cleanup-audit.md` (alongside the renamed `Total tracked files:`) using the same regex byte-for-byte. **Three-site lockstep** between `scripts/repo-inventory.sh:20`, `commands/cleanup-audit.md:16`, and `SKILL.md:38` — any future regex change must update all three.

#### Changed (sc:cleanup-audit)

- `commands/cleanup-audit.md` Repository Context: `Total files:` relabeled to `Total tracked files:` (clearer, since `git ls-files` only lists tracked files).
- `templates/pass-summary.md` Coverage Metrics "Exclusions applied" item now enumerates the three exclusion layers (Default / Find-fallback / Project) separately so generated reports are accurate post-default-excludes.
- `templates/final-report.md` Exclusions block updated analogously.

#### Validated

- TUIBBS smoke (post-edit): `Total files: 389` matches `progress.json:current_scope.in_scope_paths` from the 2026-05-29 TUIBBS audit (the manually-derived in-scope count) — defaults reproduce the prior hand-authored scope with zero per-project setup.
- 0 hidden/BMAD paths leak into any batch assignment.
- Per-project override fixture (`EXCLUDE: ^vendor/`) tightens scope correctly (3 files → 2 files).
- `sh -n` clean on `repo-inventory.sh`; POSIX-sh compatibility preserved.
- 7 in-band QA reports (5 phase-gate `rf-qa` + post-completion `rf-qa` structural + `rf-qa-qualitative` operational, all PASS-after-fixes) + post-execution `/sc:reflect --mode post` (T1, calibrated 0.88, 0 regressions, 5 deviations classified under §10 taxonomy).

### cliEval — Phase 5+6 remediation (TASK-RF-20260522-153212)

#### Added (cliEval)

- `src/superclaude/cli/eval/exit_codes.py` with exactly 4 canonical exit codes (`SUCCESS=0`, `FAILURES=1`, `USAGE_ERROR=2`, `INTERRUPTED=3`). All 11 `*_EXIT_CODE` constants in the eval module re-export from here via top-of-file `from . import exit_codes as _exit_codes` + local `NAME: int = _exit_codes.VALUE` assignments (CC2 / OQ-2).
- `orchestrator.allocate_session_id(*, run_id, eval_id)` helper — the canonical session-id allocator; `commands.py::_run_one_spec` now threads `run_id` through and calls the helper instead of constructing `f"sess-{spec.id}"` ad-hoc (M5).
- `eval doctor --output-dir` Click option now carries `file_okay=False`, symmetric with `eval run --output-dir` (M6).
- Stderr WARNING emitted at the `_NullLifecycleExecutor` call site on every `eval run` until the production executor lands (M2 / CC3): `eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.`
- User-facing operator guide at `docs/user-guide/eval-pipeline.md` covering all four subcommands, exit codes, output layout, and the AC12 scratch-root policy.

#### Changed (cliEval)

- `eval run --output-dir <X>` is now the OUTPUT ROOT: artifacts land at `<X>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (anchored via `compose_run_dir`) instead of a flat layout under `<X>` (H1 / FR-G4).
- `_format_run_summary_line` renders the full DM-012 taxonomy `P/F/S/E/I/T` (passed/failed/skipped/errored/interrupted/timeout) instead of eliding `ERRORED`/`INTERRUPTED`/`TIMEOUT` (H3).
- FR-G5 coverage gate now fails closed (`CoverageResult(passed=False, parse_error=...)`) on corrupt `~/.claude/settings.json` instead of silently passing (H2).
- `resolve_scratch_root("/tmp/eval-runs")` (bare allowlist prefix with no sub-path) now raises `ScratchRootViolation`; only strict sub-paths are accepted (H4 / AC12). Closes the AC12 tautology where the check would silently accept the prefix as a "match" of itself.
- Runtime allowlist extension now happens **before** any `mkdir(parents=True)` at both `commands.py::eval_run` and `isolation.py::HomeIsolation.setup` call sites (H5a, H5b / OPS-002 / NFR-SEC2). No filesystem write before allowlist validation.
- `EVAL_ID_PATTERN` (the FR-SCH2 schema regex) is now the single source of truth in `artifact_layout.py`; `loader.EVAL_ID_REGEX` is preserved as an import alias for backward-compat. The previously-private `_EVAL_ID_RE` (the path-safety regex) was renamed to `_EVAL_ID_PATH_SAFETY_PATTERN` to disambiguate the defense-in-depth layers (CC1 / OQ-1).
- Both `Reporter.write` and `write_aggregated_report` now emit `summary.yaml` alongside `summary.md` / `summary.json` via the shared `_write_artifact_set` helper (M4 — closes the previous +1 yaml divergence between the two writers).
- `RunTotals` keys derived from `EVAL_STATUSES` partitions in `models.py` (no hardcoded literals). New module-level constants: `PASSED_STATUSES`, `FAILED_STATUSES`, `SKIPPED_STATUSES` (M3).

#### Fixed (cliEval)

- The previously-blocking `NameError: '_new_run_id' is not defined` from `eval run` was already closed at PR #66 (`dce3c3cb`); the Phase 5+6 remediation confirmed the helpers (`_new_run_id` at `commands.py:1326`, `_default_output_dir` at `:1339`) are present and layered the canonical exit-code module, `orchestrator.allocate_session_id`, and the FR-G4 `compose_run_dir` anchoring on top. **B1 follow-up resolved.**
- Documentation drift across `docs/eval/{validation-commands,release-checklist,retention,runtime,retry,scratch-roots}.md` corrected per `.dev/audit-reports/docs-audit-2026-05-22.md`.

#### Notes (cliEval)

- `INTERRUPTED` canonical exit code is **`3`** (matches `signal_handler.EXIT_INTERRUPTED` + `tests/cli/eval/test_exit_codes.py` design-spec §4 docstring), not the POSIX `signal+128 = 130` convention. CI scripts keying off the SIGINT exit code should match `3` exactly. Rationale documented inline in `exit_codes.py`.
- AC matrix at `.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/reports/06-ac-matrix.md` maps every H/M/CC finding ID to its remediation step, test, and verification evidence. PG-FINAL composite task-integrity gate verdict: PASS at cycle 1 (22/22 spec rows + 6/6 auxiliary VALIDATION_REQUIREMENTS checks).

---

### Added

- **Context Freshness System** (`src/superclaude/hooks/scripts/freshness-*.sh`) — seven active shell hooks plus `install_hooks.py` that:
  - Inject a `<session-context>` envelope on every user prompt (turn counter, Δ-since-last-prompt, dirty-git probe, background-agent count).
  - Block `Edit` / `Write` / `mcp__serena__replace_*` / `mcp__serena__insert_*_symbol` against files that have not been Read in the last 30 minutes.
  - Track every Read into `~/.claude/state/reads.jsonl`.
  - Emit telemetry to `~/.claude/logs/freshness-hook.jsonl` for week-1 tuning.
- New `superclaude install` step (`install_hooks`) — atomically copies hook scripts to `~/.claude/hooks/` and additively merges hook registrations into `~/.claude/settings.json` (existing user hooks preserved; backup at `~/.claude/settings.json.bak.<ISO-8601>` before any write).
- `make sync-dev` now also syncs `src/superclaude/hooks/scripts/*.sh` and `src/superclaude/scripts/session-init.sh` into `.claude/hooks/` for local development.
- Context freshness discipline section appended to `src/superclaude/core/CLAUDE.md` — codifies the five content-signal triggers (S1–S5) for citations that hooks cannot catch.

### Fixed

- `src/superclaude/hooks/hooks.json` `session-init.sh` command path changed from the fragile relative `./scripts/session-init.sh` to `~/.claude/hooks/session-init.sh` (Option B from `docs/analysis/hooks-json-relative-path-issue.md`).
- `src/superclaude/hooks/scripts/freshness-pre-edit.sh` now allows `Write` to nonexistent paths via a new `create_allowed` decision (Proposal A from `freshness-hook-fix-debate.md`). Resolves the catch-22 where the gate blocked new-file creation because there was no prior `Read`, and the `Read` itself failed because the file did not exist. `Edit` and `Write` against existing-but-unread files continue to block (`no_prior_read`). New telemetry reason `create_allowed` appears in `~/.claude/logs/freshness-hook.jsonl`. Defense-in-depth regression guard added: `tests/cli/test_install_hooks.py::test_real_hooks_json_gates_write_in_pre_tool_use` pins the matcher.

### Known v1 limitation

- **External-modification detection is not active in v1.** The design called for a `FileChanged` hook to populate `~/.claude/state/changes.jsonl` and feed the `external_change` block reason in the freshness gate. Live probing in T05.01 revealed that Claude Code's `FileChanged` matcher only accepts pipe-separated literal filenames (not regex, not "watch all"), so the design's `matcher: ".*"` registration silently watched nothing. The FileChanged registration has been removed from v1; the `freshness-file-changed.sh` script remains in `src/` for v1.5 re-implementation. The `freshness-pre-edit.sh` gate still blocks on `no_prior_read` and `read_too_old`, which cover the two highest-impact stale-fact scenarios.
- **`Write` to nonexistent files is blocked.** The freshness gate fires on any `Write` target with no prior Read tracker, which is correct per the design (the gate doesn't check file existence). For fresh-session new-file creation, use Bash heredocs (`cat > new_file <<'EOF'…EOF`). v1.5 may add a "Write to nonexistent path → allow" branch.

### v1.5 work items (freshness-system)

- **FileChanged redesign.** Two viable approaches: (a) static per-project watch list via `|`-separated literal filenames in `matcher`; (b) dynamic via `hookSpecificOutput.watchPaths` returned from `PostToolUse(Read)` — needs a fresh probe to confirm Claude Code accepts watchPaths from non-FileChanged events. After redesign, re-run Test 1 to verify `external_change` block reason fires correctly.
- **`Write`-to-new-file refinement.** Add a "if target path does not exist on disk, allow" branch to `freshness-pre-edit.sh`. Verify the change doesn't introduce a false-allow path (e.g., for race conditions where file was deleted between Read and Write).
- **`install_hooks --no-orphans` flag.** Exclude scripts from the copy list that aren't currently registered in `src/superclaude/hooks/hooks.json`. Cleaner for strict-only deployments; preserves current v1 behavior by default. Today the package copies `freshness-file-changed.sh` even though it's unregistered.
- **`reads.jsonl` rotation.** File grows unbounded; PreToolUse gate scans it on every Edit. Design §2.1 calls for keeping the oldest 3 sessions; implement before users accumulate >10K rows.
- **`session_id` sanitization.** Hook scripts interpolate `session_id` into filenames without a regex check. `validate_session_id()` helper exists in `install_hooks.py` but isn't called by the hook scripts themselves. Defense-in-depth hardening; low priority since Claude Code session_ids are platform-generated UUIDs.

### Notes

- Hooks are user-scope only (`~/.claude/settings.json`). Repo-local hooks are silently bypassed when `--add-dir` is used. To opt out, remove the relevant entries from `~/.claude/settings.json` and delete the corresponding scripts from `~/.claude/hooks/`. See [docs/user-guide/freshness-hooks.md](docs/user-guide/freshness-hooks.md).
