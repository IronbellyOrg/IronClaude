Read-only reviewer. Audit the supplied hunks and matrix; you may Read/Grep/Glob the repo. Run nothing. Return findings only.

You are reviewer 1 of 2 in a Tier-2 reflect ensemble (UC-1, pre-execution), persona analyzer. The subject is a workflow plan that scripts the #442 live-observation runbook. Audit the plan for coverage of its spec and for correctness, deviation and risk in what it prescribes. Ground every finding in a `file:line` citation taken from the hunks below or from your own Reads of the two files named in the file map.

## T1 card excerpt

# T1 reflection card (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/source.md` (1 line)
- Tasklist: `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md` (266 lines, 6 phases, 11 tasks)
- Card author: inline orchestrator

## Coverage section

- Pass 1: 0 parsed IDs. Pass 2: 6 quote-pinned rows INF-001 to INF-006 (`artifacts/inferred-requirements.json`), all citing source.md:1.
- All 6 covered (`artifacts/coverage-matrix.json`): setup by Tasks 1, 2, 5 (plan:31-55, plan:107-128); driver by Tasks 3, 4, 6 (plan:59-82); evidence by Task 7 (plan:166-191); cleanup by Tasks 8, 11 (plan:195-215, plan:255-266); authorization by Constraints (plan:19) and Task 10 (plan:236-253); orchestration investigated and rejected with reasons (plan:25).
- `coverage_pct: null` (parsed-only, 0 parsed), `coverage_pct_union: 1.0`, `S_dev_density: 0.0`, `coverage_degraded: parsed-sparse` (Tier-1 stop forbidden).

## Deviation / risk section

- T1-F1 (gap): Task 11 requires the store diff `ls -A ~/.claude/state/launch-level/sessions | diff /tmp/ob/baseline-sessions.txt -` to run before step 7 deletes `/tmp/ob` (plan:263), but Task 8 does not build that check into `cleanup.sh` (plan:199-210) and `--apply` runs every step in one call (plan:201), so the operator has no point to run it in between.
- T1-F2 (authorization ambiguity): Task 5 creates four GitHub issues (plan:114) and session `e` opens a pull request and writes repository contents with `gh api -X PUT` (plan:148-149). The authorization line (plan:19) names "governed claims on the four disposable issues"; it does not say in words that the agent may create the issues and the pull request. Creation is implied by the source (source.md:1) but is outward-facing.
- T1-F3 (risk, acknowledged): Task 10 lets the agent answer tool permission dialogs "only for a command the runbook prompt itself asked for" (plan:243). That is a judgement step and the R15 risk the plan names (plan:24).
- T1-F4 (unstated source): session `b` restores `$WT_T1/.claude/settings.local.json` from `/tmp/ob/t1-local.json` (plan:137), but no task says which step writes that backup.
- T1-F5 (minor): Task 11 stages `./artifacts/ob-logs/` (plan:185, plan:259), which holds full screen captures; the secret scan covers four token patterns only.
- Honest UNVERIFIED labels: governed handle field (plan:138), O-10 web-edit equivalence (plan:149).

## Structural section

- 6 phases, 11 tasks numbered 1 to 11; every `Depends on` names a lower task; acceptance criteria present on every task.
- Line-number extraction: prompts (lines 228-697) and setup blocks (43-169) sit before the Task 9 edit at runbook:764, so the edit does not shift them.

## Self-reported confidence

0.80 (not used by the rubric).

## Grounding hunks

codegraph run state: index_state=current checked_at=2026-11-08T06:25:20Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook

File map (paths relative to the worktree root): `plan` = `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md`; `runbook` = `.dev/issues/442/observation-runbook.md`; `spec` = `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/source.md`. You may Read either file for more context, at most 150 lines per Read.

### spec, complete (source.md:1)

Script the #442 observation runbook (.dev/issues/442/observation-runbook.md): setup, Orca terminal driver, evidence, cleanup. The owner has authorized an agent to start Claude sessions and run governed claims on the four disposable issues. Investigate whether the /orchestration skill (~/.claude/skills/orchestration/SKILL.md) is appropriate to use in this plan, and include it only if it fits.

### plan: Goal and Constraints (plan:15-27)

Goal: The runbook `.dev/issues/442/observation-runbook.md` becomes a set of scripts under `.dev/issues/442/scripts/` that an agent runs end to end: setup, an Orca terminal driver that types each session's prompts and waits for each turn to end, an evidence script that drafts `.dev/issues/442/observation-results.md` for the 12 items (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX), and a cleanup script. The plan ends with one live run on the four disposable issues T1 to T4 and its cleanup.

## Constraints

- Owner authorization (2026-11-08, this session): an agent may start Claude sessions for the observations and run governed claims on the four disposable issues T1 to T4 only. No claim, launch or comment on any other issue. The runbook's section 3 gate still holds: no governed claim on a real issue, whatever the results.
- GitHub: every `gh` call passes `--repo IronbellyOrg/IronClaude`; every `gh api` path spells `repos/IronbellyOrg/IronClaude/...`. Nothing ever targets `SuperClaude-Org/SuperClaude_Framework`. No Orca `--issue` or `--pr` flag. Never `gh pr merge`.
- Python only through `uv run`. Worktrees only through Orca (the claim creates them; cleanup removes them with `orca worktree rm`).
- Safety list of runbook section 5.1 (lines 773-783) applies to every script: no probe in the real `~/.claude/settings.json`; no prompt starting with `[sc-launch:v1:`; a marker inside a prompt only at the LL-NOBIND step of session A; no `superclaude install` during the run; the claim session starts with `env -u CLICKUP_API_TOKEN claude`; no script prints or logs `env` output or a token.
- Settings, hook, git config and launch-store changes are made by the scripts from the driving agent's own shell, never by a prompt typed into an observed Claude session (LL-TAMPER).
- Terminal injection is representative: a prompt sent with `orca terminal send` reaches the hook as the same UserPromptSubmit payload as a typed one (hook payloads carry no origin field, design V6). An agent sending `approved` is therefore the R15 risk the design names; it is allowed here only because the owner authorized it for T1 to T4.
- Orchestration skill: investigated and not used. Evidence from the version-matched guide (`orca skills get orchestration`, read 2026-11-08): `worker-start` injects a lifecycle preamble as the first prompt and obliges heartbeats and `worker_done`, which would change the very UserPromptSubmit and PreToolUse payloads under observation and, in a governed session, add Bash calls the guard judges; governed sessions must come from the claim's own `orca agent launch --surface terminal` with a leading marker (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` docstring line 46), and a second launch path would not test it; the guide's own routing sends terminal control, lightweight prompts and reading or waiting on terminals to `orca-cli`; and this session is a settled dispatched worker whose lifecycle IDs must not be reused (guide lines 100-101). The independent check of each task is already the `/sc:implement` reviewer, so a supervised Orca reviewer would add nothing. The driver uses plain `orca terminal create|send|read|wait|list|close`.
- Every script: bash, `set -u -o pipefail`, `umask 077`, and every external call bounded by `timeout`. An item without evidence is `pending`, never PASS.
- Scripts live in `.dev/issues/442/scripts/` of this checkout; scratch state stays under `/tmp/ob` as the runbook defines. No change to `src/` or `tests/`.

### plan: Tasks 5 to 8 (plan:107-215)

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
- Step 1 runs the two preflight refusals. The script writes the bad JSON and then `disableAllHooks` into `$WT_T1/.claude/settings.local.json` from its own shell, sends the claim to the claim session, and runs the three checks at lines 549-551 after each refusal. It then restores the file from `/tmp/ob/t1-local.json`.
- The real claim follows. The governed terminal handle is read from the claim output or the `launch` record of `.dev/issues/<T1>/worktree.json`, and recorded with `driver.sh adopt`. Which field holds the handle is UNVERIFIED: confirm it on the first launch and record it in the script's comment.
- `GSID` is read from the probe log.
- Step 3 sends the prompts at lines 586, 592 and 598, then repeats the commit prompt.
- Step 4 sends the prompts at lines 606, 610, `/clear` and 625, and runs the `identify` checks at lines 616-620 and 629-633.

Session `c` (section 2.2.2): it sends the `/sc:implement <plan path>` prompt, using the plan path read from the screen, and then the commit prompt.

Session `d` (section 2.2.3): it sends the claim with `--pipeline full`. It waits up to 90 minutes for the agent's final `git status --short`, then sends the commit prompt.

Session `e` (section 2.2.4, lines 657-697):
- It sends the claim with `--pipeline full --submit`. It checks that the pull request URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`, and stops with `FAIL misrouted-pr` if it does not.
- For O-10, during monitoring, it changes `ob-442/T4.txt` on the pull request branch with `gh_fork api -X PUT repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt`. This stands in for the web UI edit; whether `/sc:pr-submit` reacts the same way is UNVERIFIED, and the step's result says so.
- After the cycle it runs the push URL commands at lines 668-672. It sends the push prompt (line 678) only when `git remote get-url --push origin` in `$WT_T4` prints `/tmp/ob/bare-push.git`, then sends the merge prompt (line 684) and runs the restore at lines 690-691.

Release:
- Each subcommand ends by running the claim's printed `release` `rm` line from the script's shell.
- It runs that line only when the path is `~/.claude/state/launch-level/sessions/<GSID>` or `<GSID>.ok` for this run's recorded `GSID`.

Stop rules: before `b` the script reads OB-H1 item 5 from the results file and refuses unless it is PASS. Before `d` and `e` it also requires item 1 PASS (runbook section 3.3, lines 720-726).

Acceptance criteria:
- With the stub `orca` and `gh` and scripted screens, the self-test shows session `e` refusing the push prompt when the push URL is not `/tmp/ob/bare-push.git`, and refusing a pull request URL outside `IronbellyOrg/IronClaude`.
- The self-test shows the release step refusing an `rm` path that is not this run's `GSID` or its `.ok` file.
- The self-test shows `b` refusing to start when item 5 is not PASS, and `d` refusing when item 1 is not PASS.
- Every prompt file matches its runbook `text` block byte for byte (a self-test diff over lines 536-697).

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

It also writes `./artifacts/ob-logs/`: a copy of `/tmp/ob/logs`, `/tmp/ob/screens` and the state file, made only after a scan finds no line matching `gh[pousr]_[A-Za-z0-9]{20,}`, `github_pat_`, `sk-[A-Za-z0-9]` or `CLICKUP_API_TOKEN=`. A match stops the copy and lists the file and line number, never the matched text.

Acceptance criteria:
- With a synthetic log built from `tests/hooks/fixtures/launch_level/ob_h1/*.json`, the self-test produces a results file with exactly 12 item blocks. An item whose log is missing reads `Result: pending`.
- The self-test shows each F1 to F8 filter in the script equal to its runbook text (a diff against the extracted block).
- The self-test shows the secret scan stopping the copy for a planted `ghp_` line, and the report not containing the planted value.
- Running the script twice yields the same file (a `cmp` of two runs).

## Task 8: Write the cleanup script

Depends on: Task 1

Create `.dev/issues/442/scripts/cleanup.sh`. It does steps 1 to 8 of runbook section 5.2 (lines 785-835) in that order: worktrees are removed before the pull request is closed with `--delete-branch`.

By default it prints the plan of every removal and deletes nothing. With `--apply` it does each step and prints one line per step.

What `--apply` removes:
- In step 2, only the store entries that are new against the baseline and are one of this run's recorded `GSID` values or their `.ok` files. Leftover entries in `jobs/` and `requests/` are listed, not removed.
- In step 4, the worktrees with `orca worktree rm --worktree path:<WT>`. `--force` is used only when `git -C <WT> status --short` shows nothing but files the run created.
- In step 5, the pull request and the issues with `gh_fork`.
- In step 6, nothing: it leaves `.dev/issues/<T1>/` to `.dev/issues/<T4>/` in the main checkout in place and lists them for the owner.
- In step 7, `/tmp/ob`, only after `./artifacts/ob-logs/` exists.

It refuses `--apply` while `.dev/issues/442/observation-results.md` is missing.

Acceptance criteria:
- With the stub commands, the self-test shows the default run calling no `rm`, `orca worktree rm` or `gh` write command, and the `--apply` run calling them in the section 5.2 order.
- The self-test shows step 2 skipping a new store entry that is not a recorded `GSID`, and step 7 refusing while `./artifacts/ob-logs/` is missing.
- Every `gh` call in the stub log carries `--repo IronbellyOrg/IronClaude`.

### plan: Tasks 9 to 11 (plan:216-266)

## Task 9: Update the runbook and its handoff for the scripted path

Depends on: Task 7, Task 8

Edit `.dev/issues/442/observation-runbook.md`:
- Replace the two wrong statements in section 4.2 (lines 764-765). Prompts sent with `orca terminal send` reach the hooks as the same payload as typed ones, so injected prompts are representative. The LL-TAMPER block applies only to a governed session, so the claim's release `rm` is run from the driving agent's own shell.
- Change the "Starting the sessions" bullet to record the owner's authorization of 2026-11-08 for T1 to T4.
- Add a section `## 6. Scripted path` that names each script in `.dev/issues/442/scripts/`, the order to run them in, the `--apply` rule of the cleanup, and the `NEEDS_INPUT` and `BLOCKED login-isolated-home` stops.

Add a short paragraph to `.dev/issues/442/handoff-runbook.md` under "What is left": the scripts exist, and the live run is this plan's Task 10.

Acceptance criteria:
- `grep -n 'not representative' .dev/issues/442/observation-runbook.md` prints nothing, and section 6 names every script file that exists in `.dev/issues/442/scripts/` (a self-test case compares the two lists).
- `bash .dev/issues/442/scripts/selftest.sh` still prints `SELFTEST_OK` after the edit, because the prompt and filter diffs read the edited runbook.

## Task 10: Run the observations in the runbook order and record the results

Depends on: Task 9

Run the scripts against the real Orca and GitHub, in the order of runbook section 3.1 (lines 700-710): `setup.sh`, `session-a.sh`, `session-a2.sh`, `evidence.sh all`, then `setup-github.sh` and `session-gov.sh b`, `c`, `d` and `e`, and `evidence.sh all` after each session. Follow the stop rules of section 3.3 as the scripts enforce them.

At each `NEEDS_INPUT`, read the saved screen:
- answer a tool permission dialog only for a command the runbook prompt itself asked for;
- answer nothing else;
- record every answer in `./artifacts/t10-run-log.md`.

`BLOCKED login-isolated-home` is the owner's decision: stop session A and ask. For each `needs reading` mark, record the reading and the screen file it is based on in the results file. Record the version and hash header fields from `/tmp/ob/preconditions.txt`.

Acceptance criteria:
- `.dev/issues/442/observation-results.md` has 12 item blocks. Each Result is PASS, FAIL or pending with its evidence lines, and no PASS lacks an evidence command and a log line or screen file.
- `./artifacts/ob-logs/` exists and passed the secret scan. `./artifacts/t10-run-log.md` lists every script run with its exit code and every `NEEDS_INPUT` answer.
- The disposable pull request URL in the results file starts with `https://github.com/IronbellyOrg/IronClaude/pull/`. No issue other than T1 to T4 was claimed or commented on: `gh_fork issue list --search "ob-442 disposable"` lists exactly four issues, and the claim session screens show no other issue number.
- Any FAIL in OB-H2, OB-H3 or OB-CTX is stated at the top of the results file, with the section 3 consequence: no governed claim on a real issue.

## Task 11: Clean up the run and stage the package

Depends on: Task 10

Run `cleanup.sh` without `--apply` and save its plan to `./artifacts/t11-cleanup-plan.txt`. Then run it with `--apply` and save the output to `./artifacts/t11-cleanup.txt`. Then stage the package with `git add .dev/tasks` (staging only, no commit).

Acceptance criteria:
- `./artifacts/t11-cleanup.txt` shows every step of runbook section 5.2 as done or listed.
- `/tmp/ob` is gone. `ls -A ~/.claude/state/launch-level/sessions | diff /tmp/ob/baseline-sessions.txt -` was run before step 7 and showed no line marked `>`.
- `gh_fork pr view <url> --json state -q .state` prints `CLOSED`, and each of T1 to T4 prints `CLOSED` with `gh_fork issue view <n> --json state -q .state`.
- `orca worktree list` shows none of `WT_T1` to `WT_T4`.
- `git status --short .dev/tasks` shows the package staged.

### runbook: section 3 order and gate (runbook:698-726)

## 3. Required order and the gate before a governed claim on a real issue

### 3.1 Order

Run the observations in this order. Each step starts only when the one before it is recorded.

1. **OB-CTX part 1** (session A, section 2.1). The design makes OB-CTX the first blocking feasibility check: §14 item 0, and line 318 ("OB-CTX is the first blocking feasibility check described in §19.1").
2. **OB-H1 items 1 to 9** (sessions A and A2). The design's stop rules apply here (§14 item 1): "item 1 fails, stop (O-9); item 5 bare, apply O-17 alternative". Identity loss stops deployment too: a missing or invalid top-level `session_id` on a governed call (design line 81, "otherwise deployment stops").
3. **OB-H2** (session B, steps 1 and 2, plus the LL-NOBIND result from session A).
4. **OB-H3** (session B step 3, then sessions C, D and E).
5. **OB-CTX part 2** (session B step 4). It needs a governed launch, so it can only run after OB-H2's launch. Its result completes OB-CTX.

The design's §14 item 8 says: "Gate: no real governed launch until both pass." Here "both" are OB-H2 and OB-H3, and "real" means a real issue. Sessions B to E launch only on the disposable issues T1 to T4.

### 3.3 What each kind of claim needs

| Claim | Must have passed first |
|---|---|
| Any governed claim on a disposable test issue (sessions B to E) | OB-H1 item 5 |
| `--pipeline full` or `--pipeline full --submit` on a disposable test issue (sessions D, E) | OB-H1 items 1 and 5 |
| `--pipeline worktree` or `--pipeline full` (with or without `--submit`) on a real issue | OB-H1 items 1 and 5, OB-H2, OB-H3 |

If item 5 is FAIL or pending, do not run sessions B to E at all. If item 1 is FAIL or pending, skip sessions D and E. Any FAIL in OB-H2, OB-H3 or OB-CTX means no governed claim on a real issue. Report it instead.

## Coverage slice

Parsed requirements: 0. Inferred rows (all cite source.md:1, `coverage_degraded: parsed-sparse`, `coverage_pct_union: 1.0`):

| ID | Quote (verbatim) | Plan tasks | Grounding |
|---|---|---|---|
| INF-001 | "Script the #442 observation runbook (.dev/issues/442/observation-runbook.md): setup" | Tasks 1, 2, 5 | plan:31-55, plan:107-128 |
| INF-002 | "Orca terminal driver" | Tasks 3, 4, 6 | plan:59-82 |
| INF-003 | "evidence" | Task 7 | plan:166-191 |
| INF-004 | "cleanup" | Tasks 8, 11 | plan:195-215, plan:255-266 |
| INF-005 | "The owner has authorized an agent to start Claude sessions and run governed claims on the four disposable issues." | Constraints, Tasks 4, 6, 10 | plan:19, plan:236-253 |
| INF-006 | "Investigate whether the /orchestration skill (~/.claude/skills/orchestration/SKILL.md) is appropriate to use in this plan, and include it only if it fits." | Constraints | plan:25 |

Return your findings as YAML in your final message (write no files):
findings: [{id, category: authorized-expansion|necessary-deviation|drift|regression|gap|risk, severity: blocking|minor, claim, citation: <path:line>, recommendation}]
verdict: PASS|FAIL
self_audit: <what you actively checked when your finding count is low>
