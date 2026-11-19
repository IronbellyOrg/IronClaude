---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-scriptThe442Obse-20261108-061618
version: "2"
priority: Medium
created_date: "2026-11-08"
---

# Script the issue 442 observation runbook and run it on the disposable issues

Source: ./source.md
Goal: The runbook `.dev/issues/442/observation-runbook.md` becomes a set of scripts under `.dev/issues/442/scripts/` that an agent runs end to end: setup, an Orca terminal driver that types each session's prompts and waits for each turn to end, an evidence script that drafts `.dev/issues/442/observation-results.md` for the 12 items (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX), and a cleanup script. The plan ends with one live run on the four disposable issues T1 to T4 and its cleanup.

## Constraints

- Owner authorization (2026-11-08, this session): an agent may start Claude sessions for the observations and run governed claims on the four disposable issues T1 to T4 only. Creating those four issues (Task 5) and the one disposable pull request (session `e`), both on `IronbellyOrg/IronClaude`, is inside this authorization; the owner's execution order of 2026-11-09 confirmed it. No claim, launch or comment on any other issue. The runbook's section 3 gate still holds: no governed claim on a real issue, whatever the results.
- GitHub: every `gh` call passes `--repo IronbellyOrg/IronClaude`; every `gh api` path spells `repos/IronbellyOrg/IronClaude/...`. Nothing ever targets `SuperClaude-Org/SuperClaude_Framework`. No Orca `--issue` or `--pr` flag. Never `gh pr merge`.
- Python only through `uv run`. Worktrees only through Orca (the claim creates them; cleanup removes them with `orca worktree rm`).
- Safety list of runbook section 5.1 (lines 773-783) applies to every script: no probe in the real `~/.claude/settings.json`; no prompt starting with `[sc-launch:v1:`; a marker inside a prompt only at the LL-NOBIND step of session A; no `superclaude install` during the run; the claim session starts with `env -u CLICKUP_API_TOKEN claude`; no script prints or logs `env` output or a token.
- Settings, hook, git config and launch-store changes are made by the scripts from the driving agent's own shell, never by a prompt typed into an observed Claude session (LL-TAMPER).
- Terminal injection is representative: a prompt sent with `orca terminal send` reaches the hook as the same UserPromptSubmit payload as a typed one (hook payloads carry no origin field, design V6). An agent sending `approved` is therefore the R15 risk the design names; it is allowed here only because the owner authorized it for T1 to T4.
- Orchestration skill: investigated and not used. Evidence from the version-matched guide (`orca skills get orchestration`, read 2026-11-08): `worker-start` injects a lifecycle preamble as the first prompt and obliges heartbeats and `worker_done`, which would change the very UserPromptSubmit and PreToolUse payloads under observation and, in a governed session, add Bash calls the guard judges; governed sessions must come from the claim's own `orca agent launch --surface terminal` with a leading marker (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` docstring line 46), and a second launch path would not test it; the guide's own routing sends terminal control, lightweight prompts and reading or waiting on terminals to `orca-cli`; and this session is a settled dispatched worker whose lifecycle IDs must not be reused (guide lines 100-101). The independent check of each task is already the `/sc:implement` reviewer, so a supervised Orca reviewer would add nothing. The driver uses plain `orca terminal create|send|read|wait|list|close`.
- Every script: bash, `set -u -o pipefail`, `umask 077`, and every external call bounded by `timeout`. An item without evidence is `pending`, never PASS.
- Scripts live in `.dev/issues/442/scripts/` of this checkout; scratch state stays under `/tmp/ob` as the runbook defines. No change to `src/` or `tests/`.

## Phase 1: Shared helpers and isolated setup

## Task 1: Write the shared helper library and the self-test harness

Create `.dev/issues/442/scripts/lib.sh`, sourced by every other script, and `.dev/issues/442/scripts/selftest.sh`.

`lib.sh` holds: the paths of runbook sections 1.2 and 1.3 (`OB=/tmp/ob`, `/tmp/ob/bin`, `/tmp/ob/logs`, `/tmp/ob/home`, the baseline files); a state file `/tmp/ob/state.env` that records T1 to T4, `WT_T1` to `WT_T4`, each session's terminal handle and governed session id (`GSID`), and the pull request URL, written by appending `KEY=value` lines and read back without `eval`; a `gh_fork` wrapper that adds `--repo IronbellyOrg/IronClaude` (or checks that a `gh api` path starts with `repos/IronbellyOrg/IronClaude/`) and refuses any argument matching `superclaude-org` case-insensitively; a `step` function that prints `BEGIN <id>` and one of `OK`, `SKIP`, `FAIL`, `PENDING` per step; and `main_checkout`, which reads the main checkout path from the first `worktree` line of `git worktree list --porcelain`.

`selftest.sh` puts stub `orca` and `gh` commands first on `PATH` (stubs that log their arguments to a temp file and print canned JSON), sets `OB` to a temp directory, and runs each script's test cases; later tasks add their cases to it.

Acceptance criteria:
- `bash -n` passes on both files, and `bash .dev/issues/442/scripts/selftest.sh` prints `SELFTEST_OK` and exits 0.
- A self-test case shows `gh_fork issue list` calling the stub with `--repo IronbellyOrg/IronClaude`, and `gh_fork api repos/SuperClaude-Org/x` exiting non-zero without calling the stub.
- A self-test case writes and reads back the state file, including a value containing spaces, with no `eval`.

## Task 2: Write the precondition, baseline and session A setup script

Depends on: Task 1

Create `.dev/issues/442/scripts/setup.sh`. It runs the checks P1 to P8 of runbook section 1.1 (lines 19-28) and records each command's output to `/tmp/ob/preconditions.txt`; writes the baseline files of section 1.2 (lines 34-39); and builds session A's isolated HOME exactly as section 1.3 (lines 43-169) says, including `/tmp/ob/bin/ob-probe.sh`, `/tmp/ob/bin/ob-tree.sh`, the guard copy, the copied commands, skills and agents, and the session A and A2 settings files written there. It refuses to run if `/tmp/ob` already exists, unless `--resume` is given, and never writes under the real `~/.claude`.

It then runs one login check in the isolated HOME (open item 5 of `.dev/issues/442/handoff-runbook.md`): `HOME=/tmp/ob/home CLAUDE_CONFIG_DIR=/tmp/ob/home/.claude timeout 120 claude -p "Reply with the word ok"`. If that fails for authentication, the script prints `BLOCKED login-isolated-home` and exits 3; it never copies credential files.

Acceptance criteria:
- With stub commands, the self-test shows the script creating the section 1.3 layout under the test `OB` directory, and refusing a second run without `--resume`.
- A self-test case confirms the script writes nothing outside `OB` (it compares a listing of a fake `HOME/.claude` before and after).
- The script's probe files match the text of runbook section 1.3 byte for byte (a self-test case diffs them against the blocks extracted from the runbook).

## Phase 2: Orca terminal driver and the session scripts

## Task 3: Write the Orca terminal driver

Depends on: Task 1

Create `.dev/issues/442/scripts/driver.sh` with these subcommands:
- `start <name> <worktree-selector> <command>`: `orca terminal create --worktree <selector> --title ob-442-<name> --command <command> --json`; it stores the returned handle in the state file.
- `send <name> <text> <label> [timeout-s]`: it sends one prompt with `orca terminal send --terminal <handle> --text <text> --enter --json`, then waits for the turn to end.
- `screen <name> <file>`: it saves `orca terminal read --terminal <handle> --screen --json` to a file.
- `adopt <name> <handle>`: it records a terminal the claim launched.
- `answer <name> <key> <reason>`: it answers a permission dialog by sending the single key (for example `y` or `1`) with the same `orca terminal send` call, after the same `[sc-launch:v1:` refusal as `send`, and appends one line (name, key, reason) to `./artifacts/t10-run-log.md`.
- `stop <name>`.

`send` stops waiting when the first of these happens:
- a new `Stop` event appears in `/tmp/ob/logs/<label>.jsonl` (the event count is taken before the send);
- the screen shows a `Blocked:` line (the count of `Blocked:` lines is taken before the send; only an increase is a new block, so an old block left on screen cannot end the next turn);
- `orca terminal wait --terminal <handle> --for tui-idle --timeout-ms <ms>` returns.

`send <name> <text> <label> [timeout-s] [wait-notice]`: the optional `wait-notice` flag adds a notice wait. After the turn's `Stop` event appears, it keeps waiting, bounded by the same timeout, until the background-completion notice has arrived and been answered: the log shows a prompt event after the Stop (a `<task-notification>`-wrapped prompt) followed by another Stop. Only then does it print `TURN_END stop`; on timeout it prints `TURN_END timeout` and records the step `PENDING`, because the completion evidence is missing. Every prompt the runbook marks "wait until the notice arrives and Claude has answered it" (OB-H1 item 5, runbook:302) passes this flag.

It then saves the screen to `/tmp/ob/screens/<name>-<n>.json`, and prints `TURN_END stop|blocked|idle|timeout`. When the screen shows a permission dialog or a login screen, it prints `NEEDS_INPUT <file>` and sends nothing. Every wait is bounded; the default is 600 seconds, and a session can pass a longer one.

Before writing it, confirm each flag with `orca terminal <sub> --help`. The `--for exit|tui-idle` flag and the `create` flags were confirmed on 2026-11-08. `send`, `read` and `list` are as recorded in the runbook appendix.

Acceptance criteria:
- With a stub `orca` whose `read --screen` output is scripted, the self-test shows each of the four outcomes of `send` (`stop`, `blocked`, `idle`, `timeout`), and `NEEDS_INPUT` for a screen holding a permission dialog.
- The self-test shows that `send` refuses a text starting with `[sc-launch:v1:` and exits non-zero without calling `orca`.
- The self-test shows two blocked prompts in a row: the second send does not report `blocked` from the first send's still-visible `Blocked:` line; it ends on its own new block or its Stop event.
- The self-test shows `wait-notice`: a scripted log where the Stop event precedes the `<task-notification>` prompt keeps `send` waiting until the notice and its answer (a further Stop) appear, and times out to `PENDING` when they never do.
- The self-test shows `answer` refusing a key line starting with `[sc-launch:v1:`, appending its line to the run log, and sending nothing else.
- The help output of the real `orca` for `terminal send`, `read`, `wait`, `create` and `list` is saved to `./artifacts/t3-orca-help.txt`.

## Task 4: Write the session A and A2 scripts

Depends on: Task 2, Task 3

Create `.dev/issues/442/scripts/session-a.sh` and `.dev/issues/442/scripts/session-a2.sh`.

Prompts and steps:
- Prompt files go in `.dev/issues/442/scripts/prompts/`, one file per prompt. Each is copied byte for byte from the runbook's `text` blocks.
- Session A (section 2.1, lines 228-439): item 1 (block at line 234), item 3 (line 253), item 4 (lines 268-281), item 2 (line 286), item 5 (lines 304, 308 and 312), item 6 (line 330), item 9 (line 349), item 8 (line 366), the LL-NOBIND prompt (line 385) and OB-CTX part 1 (lines 401, 405, 409, 413 and 417). The prompts are sent in the runbook's order, and the three item-5 prompts go through the driver's `wait-notice` flag.
- Session A2 (section 2.1b, lines 440-472): the prompts at lines 444 and 457.
- Shell steps that the runbook places between prompts run from the script's own shell, never as prompts. One example is the `MAIN=` session id read at line 225.

Session start:
- The runbook starts both sessions in `/tmp/ob/repo-a` (runbook:163,452), which `setup.sh` created with plain `git init` (runbook:146), so it is not an Orca worktree. `driver.sh start` therefore uses the main checkout's worktree selector and sets the directory with the working-directory form confirmed from `orca terminal create --help` (saved by Task 3); when `create` supports no directory flag, the command string becomes `cd /tmp/ob/repo-a && HOME=... claude`, run by the shell inside the terminal. The chosen form is recorded in the script's comment, and a Task 3 self-test case asserts the created terminal's working directory is `/tmp/ob/repo-a`.
- Session A then runs `HOME=/tmp/ob/home CLAUDE_CONFIG_DIR=/tmp/ob/home/.claude claude` there, with `/tmp/ob/logs/h1.jsonl` as the label log.
- Session A2 starts as runbook section 2.1b says (`claude --settings /tmp/ob/settings-a2.json`), in the same directory.

Each script saves the screen after every prompt and stops at the first `NEEDS_INPUT` or `timeout`. In that case it records the step as `PENDING` with the screen file.

Acceptance criteria:
- A self-test case extracts every `text` block in runbook lines 228-472 and diffs it against the prompt files: no missing prompt and no changed byte.
- With the stub driver, the self-test shows session A sending the prompts in runbook order, and stopping with `PENDING` at a scripted `NEEDS_INPUT`.
- No prompt file starts with `[sc-launch:v1:`. The only file holding the marker is the LL-NOBIND prompt file (a self-test grep).

## Task 5: Write the disposable GitHub and claim setup script

Depends on: Task 3

Create `.dev/issues/442/scripts/setup-github.sh` for runbook section 1.4 (lines 170-200).

Issues:
- For T1 to T4, it copies `~/.claude/ISSUE-HANDOFF.md` to a temp file and fills every section with the runbook's title and body text for that issue (line 177 and line 178). It then runs `gh_fork issue create --title ... --body-file <copy>` and records each number in the state file.
- It refuses to create issues when the state file already holds numbers.

Claim session:
- It starts the claim session in the main checkout with the driver: `start claim path:<main checkout> "env -u CLICKUP_API_TOKEN claude"`.
- For each issue it sends `/sc:issue --claim <T> --pipeline none`, then reads `Worktree: <path> (created)` from the screen and records it as `WT_T1` to `WT_T4`.

Probe settings:
- It writes each worktree's `.claude/settings.local.json` with the generator at line 197, with labels `h2-T1` to `h2-T4`.
- When that file already exists it stops with `EXISTS: merge by hand`; it never overwrites it.

Acceptance criteria:
- With the stub `gh`, the self-test shows four `issue create` calls, each carrying `--repo IronbellyOrg/IronClaude` and a `--body-file`, and no second set on a rerun.
- The self-test shows the generated `settings.local.json` equal to the output of the runbook's line 197 generator, and the script refusing to overwrite an existing file.
- The worktree paths are read from the claim screen, not guessed. A self-test case with a scripted screen records `WT_T1`.

## Task 6: Write the governed session scripts B to E

Depends on: Task 5

Create `.dev/issues/442/scripts/session-gov.sh` with subcommands `b`, `c`, `d` and `e`. Each subcommand follows its runbook section in order, and its prompt files go in `.dev/issues/442/scripts/prompts/`, copied byte for byte.

Session `b` (section 2.2.1, lines 536-642):
- Step 1 first makes the backup itself: `cp "$WT_T1/.claude/settings.local.json" /tmp/ob/t1-local.json` (runbook:541); it refuses to continue when that copy is missing or empty. Then it runs the two preflight refusals: it writes the bad JSON and then `disableAllHooks` into `$WT_T1/.claude/settings.local.json` from its own shell, sends the claim to the claim session, and runs the three checks at lines 549-551 after each refusal. It then restores the file from `/tmp/ob/t1-local.json`; the restore never runs when the backup step failed. A self-test asserts the restored file is byte-equal to the backup.
- The real claim follows. The governed terminal handle is the `terminal` key of the claim result, set from the recursive `handle` search (`orca_worktree.py` lines 49, 1031-1046, 1289, 1313), read from the claim output or the `launch` record of `.dev/issues/<T1>/worktree.json`, and recorded with `driver.sh adopt`. Fallback: when the claim output lacks `terminal`, the script records the whole record in the run log and stops for the operator.
- `GSID` is read from the probe log.
- Step 3 sends the prompts at lines 586, 592 and 598, then repeats the commit prompt.
- Step 4 sends the prompts at lines 606, 610, `/clear` and 625, and runs the `identify` checks at lines 616-620 and 629-633. It then follows the runbook's mid-step order exactly: the guarded release `rm` for this run's recorded `GSID` runs at line 635, before the final `identify` at line 638 on `sleep 241`, which must print `ordinary` with reason `released`. OB-CTX needs that case recorded (line 641); without it the item can never reach PASS.

Session `c` (section 2.2.2): it sends the `/sc:implement <plan path>` prompt, using the plan path read from the screen, and then the commit prompt.

Session `d` (section 2.2.3): it sends the claim with `--pipeline full`. It waits up to 90 minutes for the agent's final `git status --short`, then sends the commit prompt.

Session `e` (section 2.2.4, lines 657-697):
- It sends the claim with `--pipeline full --submit`. It checks that the pull request URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`, and stops with `FAIL misrouted-pr` if it does not.
- For O-10, during monitoring, it changes `ob-442/T4.txt` on the pull request branch with `gh_fork api -X PUT repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt`. This stands in for the web UI edit; whether `/sc:pr-submit` reacts the same way is UNVERIFIED, and the step's result says so.
- O-10 edit trigger: the `gh_fork api -X PUT` fires once the pull request URL first appears in the governed session's screen or its `h2-T4` log, and only then. Cycle end: the cycle counts as ended only after a `Stop` event follows the `/sc:pr-submit` final report in that log, bounded by a timeout that leaves the O-10 count `pending` on expiry.
- Before the push setup it records `worktreeConfigPre=true|unset` in the state file, reading `git -C "$WT_T4" config --get extensions.worktreeConfig` first, so cleanup step 3 unsets the key only when this run set it.
- After the cycle it runs the push URL commands at lines 668-672. It sends the push prompt (line 678) only after re-checking inline, immediately before the send, that `git remote get-url --push origin` in `$WT_T4` prints `/tmp/ob/bare-push.git` (a run-time check in the script, not only a self-test case), then sends the merge prompt (line 684) and runs the restore at lines 690-691.

Release:
- Subcommands `c`, `d` and `e` end by running the claim's printed `release` `rm` line from the script's shell; session `b` releases mid-step 4 at runbook line 635, as its step 4 says. Release is idempotent: an `rm` whose target is already absent counts as released, never as an error.
- It runs that line only when the path is `~/.claude/state/launch-level/sessions/<GSID>` or `<GSID>.ok` for this run's recorded `GSID`.

Stop rules: every subcommand (`b`, `c`, `d` and `e`) at entry reads OB-H1 item 5 from the results file and refuses to launch unless it is PASS; `d` and `e` also require item 1 PASS (runbook section 3.3, lines 720-726).

Acceptance criteria:
- With the stub `orca` and `gh` and scripted screens, the self-test shows session `e` refusing the push prompt when the push URL is not `/tmp/ob/bare-push.git`, and refusing a pull request URL outside `IronbellyOrg/IronClaude`.
- The self-test shows the release step refusing an `rm` path that is not this run's `GSID` or its `.ok` file, and treating an already-absent target as released.
- The self-test shows `b` and `c` refusing to start when item 5 is not PASS, and `d` refusing when item 1 is not PASS.
- Every prompt file matches its runbook `text` block byte for byte (a self-test diff over lines 536-697).

## Phase 3: Evidence

## Task 7: Write the evidence script that drafts the results file

Depends on: Task 4, Task 6

Create `.dev/issues/442/scripts/evidence.sh <item|all>`. It runs each item's evidence command from the runbook against `/tmp/ob/logs`:
- session A items: section 2.1, lines 230-439;
- item 7: section 2.1b;
- filters F1 to F8: section 2.2.0, lines 475-535;
- OB-H2, OB-H3 and OB-CTX: the rules at lines 582, 641 and 696.

It writes `.dev/issues/442/observation-results.md` in the template of section 4.1 (lines 734-758), filling one block for each of the 12 items: OB-H1 items 1 to 9, OB-H2, OB-H3 and OB-CTX. Each block gets:
- the exact command;
- the trimmed deciding lines;
- the log file and line;
- the screen file for block messages;
- a Result of PASS, FAIL or pending, following the item's PASS rule.

Parts that need a reading are marked `needs reading`, and their item stays pending until that reading is recorded: the F7 and F8 retry judgement, the visibility of a block message in the tab (U20), and the AC-7 message text. The header fields come from `/tmp/ob/preconditions.txt` and the state file. A rerun replaces the file and never appends a duplicate block.

It also writes `$PKG_ART/ob-logs/`: a copy of `/tmp/ob/logs`, `/tmp/ob/screens` and the state file, made only after a scan finds no line matching `gh[pousr]_[A-Za-z0-9]{20,}`, `github_pat_`, `sk-[A-Za-z0-9]`, `CLICKUP_API_TOKEN=`, `Bearer `, `Authorization:`, `-----BEGIN`, `_TOKEN=` or `_KEY=`. `$PKG_ART` is defined once in `lib.sh` as the absolute path of this package's `artifacts/` directory (never the project-root `artifacts/`, which is never staged). A match stops the copy and lists the file and line number, never the matched text.

Acceptance criteria:
- With a synthetic log built from `tests/hooks/fixtures/launch_level/ob_h1/*.json`, the self-test produces a results file with exactly 12 item blocks. An item whose log is missing reads `Result: pending`.
- The self-test classifies synthetic evidence, not only structure: a fixture-variant log where the self-started turn carries a bare `Approved!` yields FAIL for item 5, and a payload whose parent session id is missing or wrong yields FAIL for item 1; neither can produce PASS.
- The self-test shows each F1 to F8 filter in the script equal to its runbook text (a diff against the extracted block).
- The self-test shows the secret scan stopping the copy for a planted `ghp_` line and for a planted `Bearer ` line, and the report not containing the planted value.
- Running the script twice yields the same file (a `cmp` of two runs).

## Phase 4: Cleanup

## Task 8: Write the cleanup script

Depends on: Task 1

Create `.dev/issues/442/scripts/cleanup.sh`. It does steps 1 to 8 of runbook section 5.2 (lines 785-835) in that order: worktrees are removed before the pull request is closed with `--delete-branch`.

By default it prints the plan of every removal and deletes nothing. With `--apply` it does each step and prints one line per step.

What `--apply` removes, following every step of section 5.2 (lines 785-835):
- In step 1, the leftover background jobs: `pgrep -af 'sleep 24[123]$'` first, then `pkill -xf` for `sleep 241`, `sleep 242` and `sleep 243` (runbook:789-794).
- In step 2, only the store entries that are new against the baseline and are one of this run's recorded `GSID` values or their `.ok` files. Right after step 2 and again immediately before step 7, the script itself runs both diffs of runbook:799-800 (`sessions` against `baseline-sessions.txt`, `pending` against `baseline-pending.txt`), prints each result, and refuses to run step 7 while any line marked `>` remains. Leftover entries in `jobs/` and `requests/` are listed, not removed.
- In step 3, it undoes the session E push setup: it reads `worktreeConfigPre` from the state file, and only when this run set the key (state says `unset`) does it unset `extensions.worktreeConfig` and the worktree `pushurl` (runbook:806); when the state says `true` or is absent, it lists the current values and changes nothing.
- In step 4, the worktrees with `orca worktree rm --worktree path:<WT>`. `--force` is used only when `git -C <WT> status --short` shows nothing but files the run created.
- In step 5, the pull request (with `--delete-branch`) and the issues with `gh_fork`, only when they were created: the state file's PR URL and issue numbers decide, and each absent one is listed as `SKIP` instead of called.
- In step 6, nothing: it leaves `.dev/issues/<T1>/` to `.dev/issues/<T4>/` in the main checkout in place and lists them for the owner.
- In step 7, `/tmp/ob`, only after `$PKG_ART/ob-logs/` exists and the second store diff (above) found no `>` line.
- In step 8, it lists the runbook's named scratch folders (`/tmp/ob-test.*`, `/tmp/ob-nobind.*` and the rest at runbook:835) without deleting them; they belong to the earlier verification worker.

It refuses `--apply` while `.dev/issues/442/observation-results.md` is missing.

Acceptance criteria:
- With the stub commands, the self-test shows the default run calling no `rm`, `pkill`, `orca worktree rm` or `gh` write command, and the `--apply` run calling them in the section 5.2 order.
- The self-test shows step 2 skipping a new store entry that is not a recorded `GSID`, and step 7 refusing while `$PKG_ART/ob-logs/` is missing and while the pre-step-7 diff still shows a `>` line.
- The self-test shows step 3 unsetting `extensions.worktreeConfig` only when the state recorded `worktreeConfigPre=unset`, and step 5 listing `SKIP` for a pull request and issues the state file does not record.
- A self-test case covers the gated run: issues and worktrees recorded, no PR URL in the state, no governed launch; cleanup still completes every step, skipping step 5's PR close and reporting step 2 as nothing to remove.
- Every `gh` call in the stub log carries `--repo IronbellyOrg/IronClaude`.

## Phase 5: Runbook update

## Task 9: Update the runbook and its handoff for the scripted path

Depends on: Task 7, Task 8

Edit `.dev/issues/442/observation-runbook.md`:
- Replace the two wrong statements: prompts are not representative of typed ones (runbook:765) and the claim's release `rm` must be run by a person (runbook:769). Prompts sent with `orca terminal send` reach the hooks as the same payload as typed ones, so injected prompts are representative. The LL-TAMPER block applies only to a governed session, so the claim's release `rm` is run from the driving agent's own shell.
- Update the neighbouring statements the scripted path makes partly false: the web-UI-only edit at runbook:767 (the script uses `gh_fork api -X PUT`) and any remaining person-only wording in lines 764-769.
- Change the "Starting the sessions" bullet (runbook:764) to record the owner's authorization of 2026-11-08 for T1 to T4.
- Add a section `## 6. Scripted path` that names each script in `.dev/issues/442/scripts/`, the order to run them in, the `--apply` rule of the cleanup, and the `NEEDS_INPUT` and `BLOCKED login-isolated-home` stops.

Add a short paragraph to `.dev/issues/442/handoff-runbook.md` under "What is left": the scripts exist, and the live run is this plan's Task 10.

Acceptance criteria:
- The old wording is gone: `grep -n 'not representative' .dev/issues/442/observation-runbook.md` prints nothing (it also prints nothing before the edit, so the real check follows), `grep -n 'must be.*typed by a person' .dev/issues/442/observation-runbook.md` prints nothing, and `grep -c 'orca terminal send' .dev/issues/442/observation-runbook.md` is at least 1; the last two fail before the edit, so the check cannot pass vacuously. Section 6 names every script file that exists in `.dev/issues/442/scripts/` (a self-test case compares the two lists).
- `bash .dev/issues/442/scripts/selftest.sh` still prints `SELFTEST_OK` after the edit, because the prompt and filter diffs read the edited runbook.

## Phase 6: Live run on the disposable issues

## Task 10: Run the observations in the runbook order and record the results

Depends on: Task 9

Run the scripts against the real Orca and GitHub, in the order of runbook section 3.1 (lines 700-710): `setup.sh`, `session-a.sh`, `session-a2.sh`, `evidence.sh all`, then `setup-github.sh` and `session-gov.sh b`, `c`, `d` and `e`, and `evidence.sh all` after each session. Follow the stop rules of section 3.3 as the scripts enforce them. A gated skip is a valid recorded outcome: when the stop rules skip session `d` or `e`, or any session ends FAIL, record that outcome in the results file, do not run the remaining governed sessions, and go to Task 11 cleanup with the resources that exist; a pull request then never exists and later PR assertions apply only when one was created.

At each `NEEDS_INPUT`, read the saved screen and answer with `driver.sh answer <name> <key> <reason>`:
- answer a tool permission dialog only for a command whose target is this run's disposable set (the T1 to T4 issues, their worktrees and branches, the plan's own scripts, or `/tmp/ob`);
- answer nothing else;
- record every answer in `./artifacts/t10-run-log.md`.

`BLOCKED login-isolated-home` is the owner's decision: stop session A and ask. For each `needs reading` mark, record the reading and the screen file it is based on in the results file. Record the version and hash header fields from `/tmp/ob/preconditions.txt`.

Acceptance criteria:
- `.dev/issues/442/observation-results.md` has 12 item blocks. Each Result is PASS, FAIL or pending with its evidence lines, and no PASS lacks an evidence command and a log line or screen file.
- `$PKG_ART/ob-logs/` exists and passed the secret scan. `./artifacts/t10-run-log.md` lists every script run with its exit code and every `answer` call with its reason.
- The disposable pull request URL in the results file starts with `https://github.com/IronbellyOrg/IronClaude/pull/`, when a pull request was created; when the gates skipped session `e`, the results file records that skip instead. No issue other than T1 to T4 was claimed or commented on: `gh_fork issue list --search "ob-442 disposable"` lists exactly four issues, and the claim session screens show no other issue number.
- Any FAIL in OB-H2, OB-H3 or OB-CTX is stated at the top of the results file, with the section 3 consequence: no governed claim on a real issue.

## Task 11: Clean up the run and stage the package

Depends on: Task 10

Run `cleanup.sh` without `--apply` and save its plan to `./artifacts/t11-cleanup-plan.txt`. Then run it with `--apply` and save the output to `./artifacts/t11-cleanup.txt`. The owner reviews `$PKG_ART/ob-logs/` before any commit; staging is not committing. Then stage the package with `git add .dev/tasks` (staging only, no commit).

Acceptance criteria:
- `./artifacts/t11-cleanup.txt` shows every step of runbook section 5.2 as done or listed; step 5's pull-request lines read `SKIP` when no pull request was created.
- `/tmp/ob` is gone. The pre-step-7 store diff printed by `cleanup.sh` itself (both `sessions` and `pending`) showed no line marked `>`.
- `gh_fork pr view <url> --json state -q .state` prints `CLOSED` when a pull request was created, and each of T1 to T4 prints `CLOSED` with `gh_fork issue view <n> --json state -q .state`.
- `orca worktree list` shows none of `WT_T1` to `WT_T4`.
- `git status --short .dev/tasks` shows the package staged.
