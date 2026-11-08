---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-enforceTheOwnerP-20261108-031809
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# Every Orca worktree gets an agent: hook enforcement, /sc:issue claim fix, instruction updates

Source: ./source.md
Goal: An agent's Bash call that runs `orca worktree create` without `--agent` is blocked with the exact command to use; `/sc:issue --claim` no longer leaves Orca's plain first tab and `--pipeline none` no longer creates a worktree; the repo and installed instructions state that every worktree gets an agent and that the session creating it owns that agent.

## Constraints

- Owner decisions recorded 2026-11-08 during planning (they refine the source): a session may not create a worktree for its own use; every worktree gets an agent; the session that creates a worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns its agent(s); a human-created worktree also needs an agent. `/sc:issue --pipeline none` now creates no worktree (it stops after the comments, `issue-summary.md` and `next-steps.md`); the default `--pipeline worktree` and `full` keep launching an agent.
- Deviation from the source, approved by the owner on 2026-11-08 after the pre-execution review (`.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md`, Grounding Gap G-1): for `/sc:issue`, the agent does NOT come with the create. The claim must copy `.dev/issues/<N>/` (including `launch-prompt.md`) into the new worktree, pass the repository check and write the launch-level pending record before the agent starts (a failed copy means no agent), so the script keeps create → copy → `agent launch` and closes Orca's plain first tab itself after a successful copy. FO-18 (no `--agent` on the claim's create) therefore stays. The owner also confirmed on 2026-11-08 that the hook and the script change stay (an instruction-only fix was rejected).
- Only the `--agent` requirement is enforced by the hook. "No worktree for your own use", "the creator owns the agent" and "a human-created worktree needs an agent" stay instruction text.
- Accepted consequences, each reported as a warning, never a failed claim: a failed launch (`W-LAUNCH-FAILED`) leaves a worktree with no agent and no tab (re-run the claim); any post-create path that cannot close the tab (unknown create reply, list failure, AMBIGUOUS, row not listed or not on disk, a failed copy, a later reused match) leaves the plain tab with `W-FIRST-TAB-LEFT`.
- Line anchors in this plan are approximate. Re-read `cmd_worktree`, `finish`, `Outcome.as_dict` and every cited test before editing.
- Evidence for every behaviour claim lives in `.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/` (REPORT.md and tier1-observation.md N1, N8, N10, N13, N14). Orca source citations there are from the local IronOrca checkout; do not change Orca.
- Out of scope: `src/superclaude/core/WORKER-CONTRACT.md` (WC-13; a separate sub-orchestrator/coordinator issue covers it), supervised `worker-start` (already creates worktrees with an agent), closing existing empty tabs, any Orca change.
- Keep: Orca-only worktree creation (`CLAUDE.md:307`, `:312`); never pass Orca link flags (`--issue`, `--pr`, `--linear-issue`, `--reference*`, `--gitlab*`) for this repo; never hardcode `src/superclaude/` paths inside installed primitive text; edit `src/superclaude/...` then `make sync-dev` and `make verify-sync`; never stage `.claude/` paths other than `.claude/settings.json`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Use `uv run` for every Python and pytest command.

## Phase 1: Deterministic guard for bare worktree creates

## Task 1: Add the PreToolUse(Bash) hook `require-orca-worktree-agent.sh` and its tests

Create `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (executable), a sibling of `src/superclaude/hooks/scripts/block-bare-python.sh`, with the same decision contract stated in that file's header: allow = exit 0; block = one message on stderr and exit 2; never exit 1; fail open (exit 0) when `jq` or `awk` is missing, the input is not valid JSON, the tool is not Bash, `tool_input.command` is missing or empty, or the scanner errors. Read the command the same way (jq extracts `tool_input.command` and pipes it on stdin to an awk scanner; never through `awk -v` or the environment). Reuse that file's tokenizing approach (quotes, `#` comments, `;`, `&&`, `||`, `|`, newlines, `$( )` and backtick substitutions, subshells, wrappers such as `env`, `sudo`, `command`) rather than a regex over the whole string; do not extract a shared library, because installed hooks are standalone files. That scanner keeps only the command word of each command and exits on its first match (`block-bare-python.sh` sets `need[o] = 0` and returns early for later words), so extend it: collect every word of each simple command, reset the collection at each separator and inside each substitution, and decide per command once its words are complete. Block a simple command whose command word is `orca` (or a path ending in `/orca`) and whose first two non-option arguments are `worktree` and `create`, when none of that command's own words is `--agent` or starts with `--agent=`, and none is `--help` or `-h`. A flag in one command never satisfies another command. In the header, list the known ceilings the way `block-bare-python.sh` does: `bash -c`, `sh -c`, `eval`, `env -S`, `ssh host '…'`, a heredoc piped into a shell, `xargs`, `find -exec`, `claude --bare`, a quoted value equal to `--agent` (for example `--prompt "--agent"`), humans, other agent tools, and scripts that call Orca themselves (such as `orca_worktree.py`, which runs Orca as a subprocess, not through the Bash tool). Do not block `orca worktree list`, `orca worktree create --help`, other `orca` subcommands, text that only mentions the phrase inside a quoted argument (for example `echo "orca worktree create"`), or commands with `--agent`. The block message names the exact form `orca worktree create --name <name> --agent claude --prompt "<task>"`, says the session that creates the worktree becomes its orchestrator and owns that agent, and says supervised workers use `orca orchestration worker-start`. Add `tests/hooks/test_require_orca_worktree_agent.py`, modelled on `tests/hooks/test_block_bare_python.py` (same way of feeding PreToolUse JSON and checking exit code and stderr).

Acceptance criteria:
- `uv run pytest tests/hooks/test_require_orca_worktree_agent.py -v` passes, with cases for: a bare create (exit 2), a create with `--agent claude` (exit 0), `--agent=claude` (exit 0), `orca worktree create --help` and `-h` (exit 0), `orca worktree list` (exit 0), `orca worktree list --name create` (exit 0), a create chained after `cd /x &&` (exit 2), a create inside `$( )` (exit 2), a create inside backticks (exit 2), the phrase inside a quoted `echo` argument (exit 0), `/usr/local/bin/orca worktree create --name x` (exit 2), `env X=1 orca worktree create --name x`, `sudo orca …` and `command orca …` (exit 2), a create after `|` (exit 2), a create on the second line of a multi-line command or after a `#` comment line (exit 2), `orca worktree create --name a --agent claude --prompt t ; orca worktree create --name b` and the reverse order (exit 2 both), `echo --agent ; orca worktree create --name x` (exit 2), an inner bare create inside `$( )` of a command that carries `--agent` (exit 2), invalid JSON (exit 0), a non-Bash tool (exit 0), an empty command and empty stdin (exit 0), and `jq` or `awk` missing from PATH or the scanner failing (exit 0).
- The block case asserts the whole message: the form `orca worktree create --name <name> --agent claude --prompt "<task>"`, the sentence that the creating session becomes its orchestrator and owns the agent, the `orca orchestration worker-start` sentence, all on stderr, with exit 2 and no stdout.
- The script's header states the contract and the fail-open cases; the script runs no Python.
- The pass/fail log of that pytest run is saved to `./artifacts/t1-hook-tests.log`.

## Task 2: Register the hook and its mirror, and update every test that enumerates hooks

Depends on: Task 1

Register `~/.claude/hooks/require-orca-worktree-agent.sh` as a PreToolUse `Bash` hook in `src/superclaude/hooks/hooks.json` with its own registration entry and `"timeout": 3`, next to the `block-bare-python.sh` entry. Add `"require-orca-worktree-agent.sh"` with a one-line comment to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py` (beside `block-bare-python.sh`). Copy the script byte-for-byte and executable to `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, and add the same registration to `plugins/superclaude/hooks/hooks.json`. Update the tests that list hooks: the fake script list in `tests/cli/test_install_hooks.py` (around lines 96-104), the hooks package file list in `tests/unit/test_cli_install.py` (around line 139), and the exact Bash-hook set asserted in `tests/hooks/test_freshness_subagent_start_policy.py` (around lines 104-117). In `tests/cli/test_install_hooks.py` add, next to `test_real_hooks_json_registers_block_bare_python` and `test_block_bare_python_script_is_packaged_listed_and_mirrored` (around lines 760-790), the same two checks for the new hook (registered once under matcher `Bash` with timeout 3 in both trees; listed in `_FRESHNESS_SCRIPTS`; source and mirror executable and byte-identical) and an installed-settings check like `_assert_block_bare_python_installed`. `launch-job-identity.sh` (also a PreToolUse Bash hook) replaces the whole input through `updatedInput` and wraps the original command as a quoted argument, and its header says the rewrite order of other hooks is unspecified. Add a test that feeds the new hook the event a governed session would produce for a bare create (the original command, with launch-level state present) and expects exit 2, and record in the artifact that the live order of the two hooks is unverified.

Acceptance criteria:
- `uv run pytest tests/cli/test_install_hooks.py tests/unit/test_cli_install.py tests/hooks/test_freshness_subagent_start_policy.py tests/hooks/test_block_bare_python.py tests/cli/test_verify_sync_hooks.py -v` passes (run `tests/cli/test_verify_sync_hooks.py` alone, not in parallel with other source-changing work, because it edits files in place).
- `cmp src/superclaude/hooks/scripts/require-orca-worktree-agent.sh plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` reports no difference, and `make verify-sync` exits 0.
- The governed-session test exists and passes; `./artifacts/t2-launch-identity-interaction.md` names it and states that the live hook order is unverified.

## Phase 2: /sc:issue claim follows the rule

## Task 3: Make `orca_worktree.py worktree` close Orca's plain first tab after a new create

Change `cmd_worktree` and `finish` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (create call at about lines 594-613; new-row handling at about lines 614-646; `finish` at about lines 494-532). The close step runs only when the status is `created` (never on the reused path, which also goes through `finish`), only after `finish`'s git-common-dir check passed and the `.dev/issues/<N>/` copy succeeded, and before the command returns (so before any launch):
- Parse the create's `--json` reply, an envelope `{"ok": …, "result": {…}}`. Read `result.setup` and `result.defaultTabs`. If either reports a setup or default tabs, close nothing and warn. If the reply is missing, not JSON, not `ok`, or the create timed out (the code already continues after `created.timed_out`), close nothing and warn: an unknown reply never leads to a close.
- Otherwise run `orca terminal list --worktree path:<path> --json`; if it lists exactly one terminal and that terminal's `agentIdentity` is absent or empty, close that tab with `orca terminal close --terminal <handle> --tab --json`.
- Any list or close failure, malformed list reply, zero or several terminals, or a terminal with an agent is a non-fatal warning (new code `W-FIRST-TAB-LEFT`, reason in `detail`) and never changes `status`. A failed copy keeps the plain tab and reports its existing copy warning; nothing is closed.
- Add `W-FIRST-TAB-LEFT` to `WARNING_ORDER` (lines 198-206) at a stated rank: `Outcome.as_dict` ranks notes with `min(..., key=WARNING_ORDER.index)`, which raises `ValueError` for an unlisted code. Add it with its remedy line ("close the plain tab in Orca by hand") to the worktree-warning list in `src/superclaude/skills/sc-issue-protocol/SKILL.md` (about line 149) and the Wave 7 table in `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, and make the claim's Final output print `worktree_warning` so an unattended run shows it.
- Update the module docstring (lines 20-30) for the two `terminal` calls.

Update `tests/skills/test_issue_orca_worktree.py`: give the fake Orca `terminal list` and `terminal close` responders; add a valid-JSON create reply fixture for the close path (`created_scene()` returns "opaque, not json", so it cannot drive the close); the exact call list in `test_fo18_exact_commands_and_no_forbidden_flag` (around lines 794-820) uses the valid-reply fixture and gains the two `terminal` calls; the opaque-reply FO-11 test (around lines 552-561) now expects `W-FIRST-TAB-LEFT` and no `terminal` call; add tests for setup reported, default tabs reported, a timed-out create, list failure, malformed list reply, zero terminals, two terminals, one terminal with an agent, close failure (status `created`), a failed copy (no close), a new row whose path belongs to another repository (failed, zero `terminal` calls), a reused worktree (no `terminal` call), and `W-FIRST-TAB-LEFT` as the only note and together with `W-WORKTREE-COPY-FAILED` (JSON printed, no exception). `--agent`, `--prompt` and `--surface` stay only in `cmd_launch`, and no flag from `NEVER_FLAGS` or the link flags is used (`tests/skills/test_issue_protocol.py` around lines 336-370).

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v` passes.
- A created-worktree run against the fake Orca with a valid create reply records, in order: `worktree list`, `worktree create`, `worktree list`, `terminal list --worktree path:<wt> --json`, `terminal close --terminal <handle> --tab --json`; the close comes after the copy.
- `WARNING_ORDER`, `SKILL.md` and `refs/claim.md` list `W-FIRST-TAB-LEFT`, the last two with its remedy line.

## Task 4: Make `--pipeline none` create no worktree

Depends on: Task 3

In `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, Wave 7 ("Runs for every `--pipeline` value") now runs only when `--pipeline` is not `none`; Wave 8 is unchanged (already skipped for `none`). For `none`, the claim ends after both comments are posted; `worktree_status` in the final return contract is `not_requested`, and `worktree_path`, `worktree_branch`, `worktree_match_key` and `worktree_warning` are `null` (update the return-contract block in `src/superclaude/skills/sc-issue-protocol/SKILL.md`, about lines 121-136, keeping its ten keys). Also update every other place that says the worktree is made for every value: `SKILL.md` line 17 and line 170 ("create or reuse the Orca worktree"), lines 90-91 (Wave 6 "continue with Wave 7 and Wave 8"; Wave 7 has no `none` exclusion), and `refs/claim.md` line 93 ("run Wave 7, then Wave 8"), line 97 ("Runs for every `--pipeline` value") and lines 131-136 (Final output "Worktree: <path>" and "Open <wt> and run next-steps there": for `none` they say no worktree and point at the main checkout's `.dev/issues/<N>/next-steps.md`). Lines 89, 92 and 150 of `SKILL.md` already handle `none`; leave them. Keep the Wave 0 Orca check for `none` (design rule P1: Orca is a dependency) and say so in the Wave 0 text. In `src/superclaude/commands/issue.md`, update the `--pipeline` row (line 43: "Every value creates the worktree; `none` launches no agent") to say `none` creates no worktree and launches no agent, and update the lines about `none` at about 77, 80, 88 and 111 (the user runs `next-steps.md` from the main checkout's `.dev/issues/<N>/`). Keep the three values and the default `worktree`. No existing pin quotes the old `none` wording (the ST-9 test around lines 431-463 pins only the Wave 8 skip), so add new pins in `tests/skills/test_issue_protocol.py`: `refs/claim.md` skips Wave 7 for `none`; the `none` Final output has no worktree line and points at the main checkout; the four worktree fields are `null` for `none`.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py -v` passes.
- `grep -n "Every value creates the worktree\|Runs for every \`--pipeline\` value" src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol/refs/claim.md` prints nothing, and `grep -n "create or reuse the Orca worktree" src/superclaude/skills/sc-issue-protocol/SKILL.md` shows only lines that exclude `none`.
- `refs/claim.md` Wave 7 states it does not run for `--pipeline none`, and `SKILL.md` shows `worktree_status: not_requested` for `none`.

## Task 5: Record the new decisions in the /sc:issue design docs

Depends on: Task 4

In `docs/designs/sc-issue-claim-pipeline-flag.md`: change the `none` row of the level table (around line 21), P4 (around line 42), the `--pipeline` options row (around line 75), the Wave 7 line (around line 149) and LA-7/ST-9 (around lines 340 and 355) so `none` creates no worktree; add to section 8.3 (around line 184) the first-tab close step from Task 3 and its warning `W-FIRST-TAB-LEFT`; add a dated note to D2 (around line 370) and FO-18 (around line 333) that they stay, and why (the claim must copy files and write the pending record before its agent starts). In `docs/designs/sc-issue-command.md`, update B17 (around line 44) where it says `none` means "worktree only, no agent". Also update the user-facing text: `docs/user-guide/commands.md` lines 367, 379 and 394 (they say `none` creates the worktree and that you run the steps in it), and the `/sc:issue` routing row in `src/superclaude/core/HOW-WE-WORK.md` (line 329); after editing `HOW-WE-WORK.md`, copy it byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` as the project `CLAUDE.md` requires. Cite the owner decisions of 2026-11-08 (including the approval of the first-tab close in place of agent-on-create), `.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/REPORT.md` and the review report `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md`.

Acceptance criteria:
- `grep -n "none" docs/designs/sc-issue-claim-pipeline-flag.md` shows no remaining statement that `none` creates a worktree.
- Section 8.3 names the `terminal list` and `terminal close` calls and `W-FIRST-TAB-LEFT`.
- `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py tests/core/ -v` still passes (no test pins the changed doc lines, or the pins are updated).
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference, and `docs/user-guide/commands.md` no longer says `none` creates a worktree.

## Phase 3: Instructions state the rule

## Task 6: Update the project worktree rule and its example in `CLAUDE.md`

Depends on: Task 2

In `CLAUDE.md`, section "Parallel Development with Git Worktrees" (rule at lines 307-310, bullets from line 312, example block at lines 318-324): state that every Orca worktree is created with an agent (`orca worktree create --name <name> --agent claude --prompt "<task>"`, plus `--repo`, `--base-branch`, `--parent-worktree`/`--no-parent` as needed), that no session creates a worktree for its own use, that the session creating it becomes its orchestrator (or coordinator under another orchestrator) and owns its agent(s), and that a PreToolUse hook blocks a bare create once it is installed. Insert the ownership point as the first list item at line 312. Change the example at line 320 to carry `--agent claude --prompt "<task>"`, since the hook would block the bare example. Also change line 305 ("give each session its own worktree") and the Usage block at lines 333-337, which tell sessions to open their own worktrees: a worktree is created by its orchestrator with an agent in it. Keep the Orca-only rule, the link-flag bullet and the internal-temporary-checkout exception unchanged. Add a test in `tests/core/` that the project `CLAUDE.md` section from `### Parallel Development with Git Worktrees` to the first following `\n## ` contains `--agent claude`, the phrase `every worktree gets an agent`, the phrase `never create a worktree for your own use`, and the words `orchestrator`, `coordinator` and `owns` in the ownership item (case-insensitive), that the example line contains `--agent`, and that the Orca-only rule, link-flag bullet and temporary-checkout exception are still present.

Acceptance criteria:
- The new test passes under `uv run pytest tests/core/ -v`.
- `grep -n "orca worktree create --name pm-agent --base-branch origin/master$" CLAUDE.md` prints nothing.

## Task 7: Add the rule to the installed "Orca session launches" section in both copies

Depends on: Task 6

Append one paragraph after the existing "Orca session launches" paragraph in `src/superclaude/core/CLAUDE.md` (the paragraph ends at line 53, before `## Key Docs` at line 55) and the same paragraph after the matching paragraph in `src/superclaude/skills/ccsession-tag/README.md` (ends at line 237, before `#### The one question rule` at line 239). Do not change the existing lines (45-53 and 228-237). The paragraph says: every Orca worktree gets an agent; create it with `worktree create --agent` (supervised workers use `worker-start`, and a supervised worker follows its worker contract, which forbids it from creating worktrees); never create a worktree for your own use; the session that creates a worktree becomes its orchestrator, or coordinator under another orchestrator, and owns its agent(s); a hook blocks `orca worktree create` without `--agent`. It names no `src/superclaude/` path. In `tests/core/test_orca_session_launch_guidance.py`, add the pinned phrases `Every Orca worktree gets an agent`, `never create a worktree for your own use` and `owns its agent` for both copies, assert the paragraph names both `orchestrator` and `coordinator`, and assert the appended paragraph is identical in both files; the 12 existing phrases stay. Then run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py -v` passes.
- `make verify-sync` exits 0; its output is saved to `./artifacts/t7-verify-sync.log`.
- The appended paragraph in both files contains no `src/superclaude/` text.

## Phase 4: Delivery

## Task 8: Run the affected suites and record delivery steps

Depends on: Task 7

Run `uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/unit/test_cli_install.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py tests/core/ -v` and `make lint`, and fix any failure inside the files these tasks changed. Write `./artifacts/t8-delivery.md` with the operator steps that make the change take effect on a machine: after merge, `superclaude update` (plain `superclaude install` skips existing core files, `src/superclaude/cli/install_core.py:70-72`; `update` forces them), then confirm with `grep -c 'Every Orca worktree gets an agent' ~/.claude/CLAUDE.md` (expect 1) and that `~/.claude/settings.json` lists `~/.claude/hooks/require-orca-worktree-agent.sh` under PreToolUse `Bash`; note that `update` overwrites local edits to `~/.claude/*.md` and that sessions started before the update keep the old instructions until restarted; add a "Not covered" section (the hook's known ceilings from Task 1: humans, other agent tools, `claude --bare`, scripts that call Orca, quoted-execution forms); and list the pending live checks that unit tests cannot cover: a real `/sc:issue --claim` leaves no plain tab and the close runs after the copy; a bare create in a Claude session is blocked; `orca worktree create --agent claude --prompt …` leaves no plain tab, and whether adding `--activate` or setup hooks still seeds one (if it does, the block message and the `CLAUDE.md` example must not combine them).

Acceptance criteria:
- The combined pytest run (with `tests/cli/test_verify_sync_hooks.py` run on its own) and `make lint` pass; their output is saved to `./artifacts/t8-tests.log`.
- `./artifacts/t8-delivery.md` exists with the update, confirm, "Not covered" and pending-live-check sections above.
