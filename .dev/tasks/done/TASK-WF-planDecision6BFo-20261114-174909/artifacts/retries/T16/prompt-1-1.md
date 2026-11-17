eb0413194054445cfb98a30a3bcf345a291786b7
Review one task for spec compliance.

Task brief: ## Task 16: Remove the plain `approved` route from every worktree-level claim

Remove the way a person or an agent releases a governed worktree-level agent by typing `approved`. The owner decided this on 2026-11-14 (Q39, restated that day): it applies to every worktree-level claim, now, and replaces the earlier default of keeping it for person-run claims until G2 exists. The task has no dependency on the first live test, on a coordinator, on G2 or on any other task of this plan.

The mechanism lives in two places, and both change:
- The guard hook `src/superclaude/hooks/scripts/launch-level-guard.sh` and its plugin copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh`. At level worktree it accepts a whole prompt `approved`, `approved.` or `approved!` (trimmed and lower-cased) as the release, by writing the session's `.ok` file (lines 349-354, the match at line 353; the comment at lines 341-346 describes it). That match is removed. The other accepted form stays: a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` (the regex at line 347).
- The launch prompt template `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md`, worktree block, line 23: "A human approves by replying `approved` in this session or by running the printed implement command." becomes a sentence that a human approves only by running the printed implement command in this session, a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`.

After the change a governed worktree-level agent is released only by a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`. Typing `approved` does nothing.

Wording that repeats the old route changes with it: the LL-IMPL hint in the guard (line 45, "or reply approved, in this session"); `src/superclaude/skills/sc-issue-protocol/refs/claim.md` line 140 (final output: "reply `approved` in its tab to let it continue"); and the sentences that describe the route in `docs/designs/sc-issue-claim-pipeline-flag.md` (lines 162 and 232), `docs/designs/sc-issue-launch-level-hook.md` (line 236, the LL-IMPL row), `docs/user-guide/commands.md` (line 377) and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (line 320). These stay as they are: the `.ok` state label `worktree (approved)` (guard line 117) and the tests that block `approved` text sent through `CronCreate`, `SendMessage`, `tmux` or `orca terminal send` (the LL-TURN and LL-ESCAPE cases), because they are other blocks, not the release.

Tests and fixtures that pin the old wording, all changed in the same commit (line numbers are at base d4d1662a8 and are found again after any rebase):
- `tests/hooks/test_launch_level_guard.py`, the approval cases from line 3673 on: the accepted list at lines 3685-3689 (`approved`, `Approved.`, `approved\n` and `\t\r\napproved!\r\n`) becomes a rejected list; the rejected list at 3703-3711 stays rejected; the `.ok` check at 3723-3729, the parametrized cases at 3741 and 3750 and the cases at 3760-3764 lose the `approved` value and keep `/sc:implement x` and `/task y`.
- `tests/hooks/test_launch_level_guard_l2_tokens.py` (lines 149-151), which requires the plugin copy to be byte-identical to the source guard.
- The fixture `tests/hooks/fixtures/launch_level/ob_h1/item5-monitor-approved-line.json` and its row in `tests/hooks/fixtures/launch_level/ob_h1/README.md` (line 15): the prompt `approved` stays a valid input, and a test now asserts it releases nothing.
- A new test in `tests/skills/test_issue_orca_worktree.py` renders the launch prompt for level worktree and fails if it tells the agent to wait for a reply of `approved`.

Risks, stated in the touched texts and in the pull request description:
- A person with no coordinator can no longer release a governed agent by typing `approved`. They type `/sc:implement <plan path>`, `/sc:task` or `/task` themselves, or later use the coordinator route of Tasks 14 and 15, which this task does not wait for.
- A governed worktree-level agent already waiting for `approved` when the installed guard is refreshed with `superclaude install` can then be released only by one of those three prompts. Before installing, check `ls ~/.claude/state/launch-level/sessions/` for sessions in flight.
- A session that already has its `.ok` file stays released.
- The guard is a security hook, so this change gets its own independent review before merge (Task 13 states the same rule for G2). Tasks 14 and 15 later edit the same guard file and its plugin copy, so whichever lands second rebases onto the other.

Runs first in this plan, on its own branch from origin/master, with its own pull request later (opened only on the owner's go, through `/sc:pr-submit --monitor 3`). Start condition: can start now; it does not wait for the first live test, a coordinator, Plan B Task 13, or Plan B Tasks 14 and 15.

Acceptance criteria:
- After the change no template, guard match, guard hint or final-output line tells a person or an agent that typing `approved` lets the agent proceed, at any worktree-level claim; a search for the word `approved` in the two guard copies, the launch prompt template and `refs/claim.md` finds only the `worktree (approved)` label and the unrelated LL-TURN and LL-ESCAPE text.
- A hook test shows that at level worktree the prompts `approved`, `Approved.` and `approved!` write no `.ok` file and a later `/sc:implement` skill call is still blocked with LL-IMPL, and that a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` writes the `.ok` file and then allows `/sc:implement`.
- `uv run pytest tests/hooks/ tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py -v` passes with the old-route cases changed as listed, and `make sync-dev` followed by `make verify-sync` passes with no staged `.claude/` path.

AC ids: T16.AC1 = first acceptance bullet, T16.AC2 = second, T16.AC3 = third (in source order).
Global constraints: ## Constraints

- Plan only. The owner approved this plan with fixes on 2026-11-15 and asked for the review changes on the same day; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- This is Plan A of two. It holds only work that can run now, in this file order: Task 16 first (its own branch from origin/master, its own pull request later), then Tasks 1, 2, 8 (a document only), 3, 4, 5, 6, 7 and 19. Task numbers are stable across both plans, so they are not contiguous here. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so the order of the items is the gate. A `Depends on` line names only a task that appears earlier in this file. Plan B lives in its own package folder, `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909-planB/plan-b-gated-tasks.md` (Tasks 20, 9, 10, 11, 12, 13, 14, 15, 17, 18). It opens with an owner-run gate item, the first live test recorded in docs/designs/issue-pipeline-fu1.md, and is not run from this file.
- Archive. Plan B sits in its own package folder, so archiving this plan's folder when it completes does not move Plan B.
- Owner input O-1 (not chosen by this plan): the number of one GitHub issue that the owner wrote, which Task 4 records real GitHub responses for. It is written by the owner into `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` as one line `ISSUE: <number>`. An executor that finds no such line stops at Task 4 and never picks an issue.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Plan B Tasks 13 to 15).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.
Start sha: eb0413194054445cfb98a30a3bcf345a291786b7
Diff against the start snapshot: diff --git a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
--- a/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
+++ b/docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md
@@ -317,7 +317,7 @@ There is no TDD for supervised orchestration as a whole. The "TDD Divergence" co
 | 3 | Unattended mode is selected only by the `--unattended` flag | 31 command files carry `## Unattended mode`; no command detects Orca, its preamble or its environment; the flag counts only as a standalone unquoted argument token; person-mode flags are refused by the command text; a worker-side "brief guard" checks every `Command:` line. No parser or guard executable exists (grep of `src` for "brief guard"/"guard refused" hits only `WORKER-CONTRACT.md`). NORMATIVE for the guard; CHECKOUT for the 31 sections (`research/01` B.2) | D1: `--unattended` is the only switch, plus the worker-session brief guard (`APPROVED.md:8`); `WORKER-CONTRACT.md:12` | None recorded. Note an internal inconsistency kept open as owner question C2 (Section 14.3.1): `WORKER-CONTRACT.md:14` lists `--monitor 1` (pr-submit) as refused, yet `/sc:pr-submit` has no unattended section and is on the never-as-worker list (`:23`) |
 | 4 | Workers never act outward; the coordinator does every push, PR, comment, install and paid run | WC-9 (`WORKER-CONTRACT.md:41-45`): no brief turns outward action on; the only git write a brief may authorize is an end-of-Task local commit under the three conditions listed in Section 5.1 (How It Works, item 3); the coordinator stages `.dev/tasks`. 8 command names are on the never-as-worker list (`:23`, pinned by the `NEVER_AS_WORKER` tuple, `tests/skills/test_worker_contract.py:382-391`). No IronClaude hook enforces it for a person-opened coordinator or a supervised worker (both are ungoverned sessions to the launch-level guard; `research/02` 6.3) | D4 (no worker acts outward) and D3 (`/sc:pr-submit` never an Orca worker) (`APPROVED.md:10-11`) | None recorded |
 | 5 | The only machine check on Orca worktree creation is a lexical `--agent` test | PreToolUse(Bash) hook `require-orca-worktree-agent.sh` (timeout 3 s, `hooks.json:105-114`). A call is blocked when its command word's basename is `orca` (or the word starts with `$`), its first two non-option arguments are `worktree` and `create`, and none of its own words is `--agent`, `--agent=...`, `--help` or `-h` (`:30-33,145`). Exit 2 with a message on stderr; fail-open (exit 0) for missing `jq` or `awk`, non-JSON, non-Bash tools, no command, or any scanner error (`:10-15`, `:342-349`). Header lists known ceilings: `bash -c`/`eval`/`env -S`/`ssh` strings, `xargs orca`, heredoc into a shell, built command words, `claude --bare`, humans and subprocess callers such as `orca_worktree.py` (`:39-61`). The hook also does not block raw `git worktree add`, paths under `.dev/worktrees/`, `--setup run`, or removal of a worktree that holds unmerged work (no match for these in the script, grep 2026-11-12; `research/02` 5.4), although the project rule says never to create a worktree that way; those parts of `WORKER-CONTRACT.md:220-225` are text only (Section 5.2 table D). "No worktree for your own use" and "the creator owns the agent" are instruction text (`:7-8`). Registered only at user level: the project `.claude/settings.json` has no entry, so the guard runs only where `superclaude install` registered it (`research/03` B.1) | Make "every Orca worktree gets an agent" mechanically checkable at the cost of a bounded text scan that never blocks what it cannot judge (header `:10-15`) | None recorded against a design doc. The header's claim that its tokenizer is "copied" from `block-bare-python.sh` is [CODE-CONTRADICTED] (a derivative, 25 changed lines; `research/03` A.5) |
-| 6 | **DEFECT (launch-level guard) and documented ceiling (worktree gate):** both IronClaude hook scripts recognize the Orca CLI only under the command word `orca` | The two predicates are `require-orca-worktree-agent.sh:145` and `launch-level-guard.sh:458`. The hook is a documented ceiling (every statement of its reach names the literal `orca worktree create`); the guard is the DEFECT because its approval-forgery guarantee (`docs/designs/sc-issue-launch-level-hook.md:193`) holds only for the name `orca`. **Not fixed.** The statement, the probes, the owner confirmation and the remediation-plan link: Section 8.2 | The scripts were written against the bare name; the design lists accepted limits for built or obfuscated names (O-7, R1), a hostile agent (R12) and another session typing `approved` (R15), none of which covers a literal installed name | DEFECT against `docs/designs/sc-issue-launch-level-hook.md:193` (design guarantee vs code). Live effect on approval forgery was not observed; issue #442 (live observations) is OPEN |
+| 6 | **DEFECT (launch-level guard) and documented ceiling (worktree gate):** both IronClaude hook scripts recognize the Orca CLI only under the command word `orca` | The two predicates are `require-orca-worktree-agent.sh:145` and `launch-level-guard.sh:458`. The hook is a documented ceiling (every statement of its reach names the literal `orca worktree create`); the guard is the DEFECT because its approval-forgery guarantee (`docs/designs/sc-issue-launch-level-hook.md:193`) holds only for the name `orca`. **Not fixed.** The statement, the probes, the owner confirmation and the remediation-plan link: Section 8.2 | The scripts were written against the bare name; the design lists accepted limits for built or obfuscated names (O-7, R1), a hostile agent (R12) and another session typing a release prompt (R15), none of which covers a literal installed name | DEFECT against `docs/designs/sc-issue-launch-level-hook.md:193` (design guarantee vs code). Live effect on approval forgery was not observed; issue #442 (live observations) is OPEN |
 | 7 | The launch-level guard is a separate, text-level control for claim-launched sessions | `launch-level-guard.sh` governs only a session whose `session_id` has a binding file; classifies Bash/Monitor text, Skill names, Edit/Write paths and MCP tools; unbound sessions are never blocked. Fail-closed only for its own failure paths (EXIT trap maps internal failure to LL-BROKEN or LL-NOBIND for a governed session); identity loss (no valid `session_id`) allows a tool call silently and a prompt only when it carries no launch marker (detail by event in Section 5.3, Failure behavior; qualifier stated once in Section 10.3). Registered on UserPromptSubmit and PreToolUse, timeout 5 s (`hooks.json:63-71,115-124`), no `onFailure` key. A hook stopped at its timeout lets the call go ahead: the design records "hook killed at timeout \| call goes ahead (V8, R2)" (`sc-issue-launch-level-hook.md:216,440`) and a probe showed TERM/KILL produce exit 143/137 with no deny (`research/gap-P3-G06.md` section 3, single runs). DOCUMENTED: a PreToolUse command hook that reaches its timeout is canceled and does not block unless `"onFailure": "block"` is set (Claude Code v2.1.295 or later) (https://code.claude.com/docs/en/hooks, read 2026-11-11; `research/web-01` Q1); the host's actual behavior and signal are [UNVERIFIED]. Text-level accepted leaks are pinned by tests (`tests/hooks/test_launch_level_guard.py:3602-3622`). The identity helper's `identify` mode has no runtime consumer in this checkout (its consumer, the L2 pre-push hook, exists only on ORIGIN/MASTER) | Limit what an unattended claim agent can do (commit, push, merge, escape through other sessions) without blocking ungoverned sessions; `onFailure: "block"` was rejected because a broken hook would then block every ungoverned session (`.dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md:98,694,701`, via `gap-P3-G06.md` section 2) | Design vs code and tests: (a) design table says T-SPD-5 "under 1 s each, asserted", but the test asserts 3.5 s per run and keeps 1 s as a reported target (`tests/hooks/test_launch_level_guard.py:996-1021`, decision 2026-11-08; `gap-P3-G06.md` section 6); (b) design IR-7 says the claim should refuse without an L2 layer, the HEAD claim script warns only (`orca_worktree.py:800-805`: "IR-7 ... says refuse; this plan builds no L2 layer"); `origin/master` adds an owned L2 pre-push hook, refusal still off (`research/04` F5, not read in full). The guard's ship gate (OB-H1 item 1, OB-H2, OB-H3) is a usage rule that the claim script does not check (`research/03` GAP-7) |
 | 8 | `/sc:issue --claim` creates the worktree without `--agent` | `orca_worktree.py:666-682` runs `orca worktree create --repo ... --name issue-<N> --base-branch ... --no-parent --comment ... --json` with no `--agent`; after copying the issue files it closes Orca's plain first terminal tab only if exactly one agent-less terminal is listed; the agent is started later by `orca agent launch` (`:1351-1355`) after an enforcement preflight and a one-time pending record (`research/04` F1) | The claim must copy files, pass the repository check and write the launch record before an agent starts, so a failed copy means no agent (`docs/designs/sc-issue-claim-pipeline-flag.md:11,194,380`; commit `24d79b7fa` body, per `research/04` F4 B3) | An accepted exception, not a defect: owner decision recorded 2026-11-08 in the design document, but the unqualified rule text `core/CLAUDE.md:55` ("Every Orca worktree gets an agent") and project `CLAUDE.md:312` do not name it (owner question C1 open). The approval is a sentence in a design doc, not a primary owner message |
 | 9 | The worker result is a file written by an LLM and read by an LLM | `<report-dir>/return-contract.yaml` with `worker_contract_version`, `worker_status` (`succeeded`/`partial`/`failed`/`blocked`), `command`, `report_path`, `artifacts`, `blocked_question`, `reason` (`WORKER-CONTRACT.md:32-39`). Orca's `worker_done --report-path` carries the path and "does not check the file". No schema, validator or parser exists; no executable under `src/` mentions the worker fields (two greps, zero non-markdown hits). Four file layouts coexist across commands, of which the contract names two (`research/gap-P3-G04.md` 3.3). The package contract of an archived plan is a different file with a different vocabulary and is read by code (`archive_workspace.py:325-334`) | Orca carries a pointer, so the coordinator opens the file itself (`:39`); the fall-back for a missing or invalid file is `--outcome failed` (`:59`) | None recorded. Contract text speaks of an `/sc:implement` producer that does not exist (row 14) |
diff --git a/docs/designs/sc-issue-claim-pipeline-flag.md b/docs/designs/sc-issue-claim-pipeline-flag.md
--- a/docs/designs/sc-issue-claim-pipeline-flag.md
+++ b/docs/designs/sc-issue-claim-pipeline-flag.md
@@ -130,7 +130,7 @@ The hook must read the level from state the launched agent cannot edit. Anything
 | Re-claim | a new nonce and a new session for every launch, never `--resume` (a re-claim that finds a `launch` entry launches nothing; the user removes the entry to launch again) | IR-5 |
 | `pipeline.json` | not written (section 3) | IR-3 |
 
-The word-to-level map the hook applies: `worktree` = W (planning only, `WA` after a person approves), `full` = F, `full-submit` = FS. The approval step of level `worktree` is the hook's (a person types `approved` or `/sc:implement` in the session). This design adds nothing for it. The hook enforces the stop; when the guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent, no launch record), so no level runs as a prompt-only instruction.
+The word-to-level map the hook applies: `worktree` = W (planning only, `WA` after a person approves), `full` = F, `full-submit` = FS. The approval step of level `worktree` is the hook's (a person types `/sc:implement`, `/sc:task` or `/task` in the session; a plain `approved` no longer releases). This design adds nothing for it. The hook enforces the stop; when the guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent, no launch record), so no level runs as a prompt-only instruction.
 
 `enforcement_hook` (contract field) reports the IR-4 preflight `enforcement_preflight()` in `orca_worktree.py` (`jq`, `uv`, the commands the guard calls, the installed guard, effective registration, `CLAUDE_CONFIG_DIR`): `installed` means the whole preflight passed (also when the launch then failed), `missing` means it failed and the launch was refused with `W-ENFORCEMENT-ABSENT`, and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). The IR-7 check `l2_status()` only warns with `W-L2-ABSENT` while `IR7_REFUSE` is `False` (#441).
 
@@ -159,7 +159,7 @@ Run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --sourc
 
 1. The `next-steps.md` path, then `Worktree: <wt>` (status, `match_key`; on key `basename` or `branch` the line "reused a worktree not created by /sc:issue").
 2. The "untracked, do not stage" line (MR 2.4) when it applies, and "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive (MR 5 step 2).
-3. Launch result: `launched` -> "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." (`full` -> "It runs every step and stops after implementation." `full --submit` -> "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges.") `already_launched` -> "agent already launched at <time>; remove the `launch` entry of <D>/worktree.json to launch again". `none` -> no `Worktree:` line, and "No worktree created and no agent launched. Open .dev/issues/<N>/next-steps.md in this checkout and run its commands in your own session."
+3. Launch result: `launched` -> "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; run the printed implement command (`/sc:implement <plan path>`) in its tab to let it continue." (`full` -> "It runs every step and stops after implementation." `full --submit` -> "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges.") `already_launched` -> "agent already launched at <time>; remove the `launch` entry of <D>/worktree.json to launch again". `none` -> no `Worktree:` line, and "No worktree created and no agent launched. Open .dev/issues/<N>/next-steps.md in this checkout and run its commands in your own session."
 4. Every warning with its remedy line (section 11), the worktree warning first.
 5. The return contract (section 10) and STOP. The claim `status` stays `success` through any Wave 7 or Wave 8 failure: the assignment and comments cannot be undone (AD 4.5, FR-10, FR-29).
 
@@ -229,7 +229,7 @@ Arguments `--number <N> --source <D> --level worktree|full [--submit]`. Output `
 | Block | Required statements |
 |---|---|
 | `common` | You were started by `/sc:issue --claim <N>`. Read `.dev/issues/<N>/issue-summary.md` and `.dev/issues/<N>/next-steps.md`. Run each step of `next-steps.md` in order by invoking its command through the Skill tool in this session, never by reading a command file and never inside a subagent. `next-steps.md` names the model tier it was written for; if this session runs on a lower one, say so in your first message. Never merge anything and never push to `master` or `main`. |
-| `worktree` | Follow the steps up to the `Plan boundary` line of `next-steps.md`. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`. When the plan exists, print its path and `Waiting for approval`, then wait. A human approves by replying `approved` or by running the printed implement command; after that, run the remaining steps, still with no commit, push or `/sc:pr-submit`. |
+| `worktree` | Follow the steps up to the `Plan boundary` line of `next-steps.md`. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`. When the plan exists, print its path and `Waiting for approval`, then wait. A human approves only by running the printed implement command (a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`); after that, run the remaining steps, still with no commit, push or `/sc:pr-submit`. |
 | `full` | Run every step through the last one. Leave the changes in the working tree, stage nothing, and finish by printing `git status --short`. |
 | `submit` | The owner asked for the commit and push by passing `--submit`. After the last step: check that no PR is already open or merged for this branch; commit with a conventional-commit message, staging `.dev/tasks` and the changed files, never anything under `.claude/` and never `.dev/issues/`; push the current feature branch to `origin` (never `master`); run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`. Never merge. |
 
diff --git a/docs/designs/sc-issue-launch-level-hook.md b/docs/designs/sc-issue-launch-level-hook.md
--- a/docs/designs/sc-issue-launch-level-hook.md
+++ b/docs/designs/sc-issue-launch-level-hook.md
@@ -55,7 +55,7 @@ first prompt (UserPromptSubmit)    consume nonce; publish sid without replacemen
   v
 each matched call (PreToolUse)     no bound id: exit 0 | jq -> level -> classes -> grid -> exit 0 or 2  FR-L-10
   v
-typed prompt (UserPromptSubmit)    "approved" or /sc:implement /sc:task /task at W: touch <sid>.ok  FR-L-15
+typed prompt (UserPromptSubmit)    /sc:implement /sc:task /task at W: touch <sid>.ok  FR-L-15
   v
 release                            a person runs rm sessions/<sid> sessions/<sid>.ok  FR-L-07
 ```
@@ -186,7 +186,7 @@ No match: PUSHFORM. Match: destination is capture 5, else 3, minus one `refs/hea
 ## 6. Human approval and human versus agent
 
 - **Event:** UserPromptSubmit only (O-4).
-- **Match (FR-L-16):** whole prompt trimmed and lower-cased matches `^approved[.!]?$`, or first line matches `^/(sc:implement|sc:task|task)([[:space:]]|$)`. `/task-builder`, `/tasks`, `/sc:implement-protocol`, `please approved`, `approved, but`, `/sc:pr-submit` do not.
+- **Match (FR-L-16):** only the first line matching `^/(sc:implement|sc:task|task)([[:space:]]|$)` releases. `/task-builder`, `/tasks`, `/sc:implement-protocol`, `approved`, `please approved`, `approved, but`, `/sc:pr-submit` do not. Amended: the plain `approved` route (a whole prompt `approved`, `approved.` or `approved!`) was removed for every worktree-level claim (owner decision Q39).
 - **Where (FR-L-15):** bound session, no `agent_id`, level `worktree` (or invalid word). Nothing at `F`, `FS`.
 - **Effect (FR-L-17):** `touch .ok`; `W` becomes `WA`. It unlocks IMPL (the grid also allows TURN at `WA`), never COMMIT, PUSH, SUBMIT or MERGE. A failed `touch` shows later as LL-IMPL. Lasts until a person deletes the files (O-6).
 - **Order (FR-L-18):** the prompt event runs before expansion, so `.ok` exists before Skill `sc:implement-protocol`. OB-H1 item 4 checks; fallback is UserPromptExpansion with exact `command_name`.
@@ -233,7 +233,7 @@ To stderr, then exit 2. Header: `Launch-level guard: this session was started by
 
 | Id | Blocked: | Why: | You can: |
 |---|---|---|---|
-| LL-IMPL | starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills). | At the worktree level the agent stops at a plan until a person approves it. | Read the plan, then type /sc:implement or /task, or reply approved, in this session. |
+| LL-IMPL | starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills). | At the worktree level the agent stops at a plan until a person approves it. | Read the plan, then type /sc:implement or /task in this session. |
 | LL-COMMIT | creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref). | Only a launch with --pipeline full --submit lets the agent commit. | Review the changes and commit them yourself, or claim the issue again with --pipeline full --submit. |
 | LL-PUSH | a git push. | Only a launch with --pipeline full --submit lets the agent push. | Push the branch yourself after review, or claim the issue again with --pipeline full --submit. |
 | LL-PUSH-FORM | a push that is not one plain git push command, or a command that names git and push together. | The guard can check a push only when the whole command is git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it; other forms (force, --all, another remote, variables, backticks, line continuations, chained or piped commands) can reach another remote or the main branch. | Run the push as its own command, exactly: git push origin <branch> or git push -u origin <branch>, with the branch name written out. |
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -374,7 +374,7 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 
 | Level | What the launched agent does | Commit, push, PR |
 |-------|------------------------------|------------------|
-| `worktree` (default) | Runs the steps of `next-steps.md` up to the plan boundary, prints the plan path and `Waiting for approval`, then waits until you reply `approved` (or run the printed implement command) | No |
+| `worktree` (default) | Runs the steps of `next-steps.md` up to the plan boundary, prints the plan path and `Waiting for approval`, then waits until you run the printed implement command (a plain `approved` reply no longer releases it) | No |
 | `full` | Runs every step, implementation included, and leaves the changes in the working tree, nothing staged | No |
 | `full` with `--submit` | Does the same, then commits, pushes a feature branch to `origin` and opens a PR through `/sc:pr-submit --monitor 3` | Yes; never merges |
 | `none` | Stops after the comments: no worktree, no agent. You run `.dev/issues/<N>/next-steps.md` yourself from this checkout | No |
diff --git a/plugins/superclaude/hooks/scripts/launch-level-guard.sh b/plugins/superclaude/hooks/scripts/launch-level-guard.sh
--- a/plugins/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/plugins/superclaude/hooks/scripts/launch-level-guard.sh
@@ -42,7 +42,7 @@ ll_say() {
     LL-IMPL)
         b='starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills).'
         w='At the worktree level the agent stops at a plan until a person approves it.'
-        y='Read the plan, then type /sc:implement or /task, or reply approved, in this session.' ;;
+        y='Read the plan, then type /sc:implement or /task in this session.' ;;
     LL-COMMIT)
         b='creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref).'
         w='Only a launch with --pipeline full --submit lets the agent commit.'
@@ -338,19 +338,16 @@ if [ "$LL_BRANCH" = prompt ]; then
     if [ "$LL_GOVERNED" = 1 ]; then
         # B8: already bound; the level never changes, a supplied record is consumed.
         [ "$LL_USABLE" = 1 ] && rm -f -- "$LL_PEND/$LL_NONCE" 2>/dev/null
-        # Approval (FR-L-15 to FR-L-17): only at worktree (an invalid word
-        # included), never at full or full-submit. The whole prompt trimmed and
-        # lower-cased is approved, approved. or approved!; or the first line,
-        # leading whitespace removed, starts /sc:implement, /sc:task or /task
-        # as a whole word. The [[:space:]] after the command name also matches
-        # the newline that ends the first line.
+        # Release (FR-L-15 to FR-L-17): only at worktree (an invalid word
+        # included), never at full or full-submit. Only a first line, leading
+        # whitespace removed, that starts /sc:implement, /sc:task or /task as a
+        # whole word releases; a plain typed word no longer does. The
+        # [[:space:]] after the command name also matches the newline that ends
+        # the first line.
         LL_RE_APR='^[[:space:]]*/(sc:implement|sc:task|task)([[:space:]]|$)'
         LL_APR=0
         if [ "$LL_LEVEL" = W ]; then
             [[ $LL_PROMPT =~ $LL_RE_APR ]] && LL_APR=1
-            LL_P=${LL_PROMPT#"${LL_PROMPT%%[![:space:]]*}"}
-            LL_P=${LL_P%"${LL_P##*[![:space:]]}"}
-            [[ ${LL_P,,} =~ ^approved[.!]?$ ]] && LL_APR=1
         fi
         if [ "$LL_APR" = 1 ]; then
             # No-replace create of a regular file in the owned sessions
diff --git a/src/superclaude/hooks/scripts/launch-level-guard.sh b/src/superclaude/hooks/scripts/launch-level-guard.sh
--- a/src/superclaude/hooks/scripts/launch-level-guard.sh
+++ b/src/superclaude/hooks/scripts/launch-level-guard.sh
@@ -42,7 +42,7 @@ ll_say() {
     LL-IMPL)
         b='starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills).'
         w='At the worktree level the agent stops at a plan until a person approves it.'
-        y='Read the plan, then type /sc:implement or /task, or reply approved, in this session.' ;;
+        y='Read the plan, then type /sc:implement or /task in this session.' ;;
     LL-COMMIT)
         b='creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref).'
         w='Only a launch with --pipeline full --submit lets the agent commit.'
@@ -338,19 +338,16 @@ if [ "$LL_BRANCH" = prompt ]; then
     if [ "$LL_GOVERNED" = 1 ]; then
         # B8: already bound; the level never changes, a supplied record is consumed.
         [ "$LL_USABLE" = 1 ] && rm -f -- "$LL_PEND/$LL_NONCE" 2>/dev/null
-        # Approval (FR-L-15 to FR-L-17): only at worktree (an invalid word
-        # included), never at full or full-submit. The whole prompt trimmed and
-        # lower-cased is approved, approved. or approved!; or the first line,
-        # leading whitespace removed, starts /sc:implement, /sc:task or /task
-        # as a whole word. The [[:space:]] after the command name also matches
-        # the newline that ends the first line.
+        # Release (FR-L-15 to FR-L-17): only at worktree (an invalid word
+        # included), never at full or full-submit. Only a first line, leading
+        # whitespace removed, that starts /sc:implement, /sc:task or /task as a
+        # whole word releases; a plain typed word no longer does. The
+        # [[:space:]] after the command name also matches the newline that ends
+        # the first line.
         LL_RE_APR='^[[:space:]]*/(sc:implement|sc:task|task)([[:space:]]|$)'
         LL_APR=0
         if [ "$LL_LEVEL" = W ]; then
             [[ $LL_PROMPT =~ $LL_RE_APR ]] && LL_APR=1
-            LL_P=${LL_PROMPT#"${LL_PROMPT%%[![:space:]]*}"}
-            LL_P=${LL_P%"${LL_P##*[![:space:]]}"}
-            [[ ${LL_P,,} =~ ^approved[.!]?$ ]] && LL_APR=1
         fi
         if [ "$LL_APR" = 1 ]; then
             # No-replace create of a regular file in the owned sessions
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -137,7 +137,7 @@ Print, in this order:
 1. The `next-steps.md` path. For `--pipeline none` print no `Worktree:` line (none was created), skip item 2 and print only the `--pipeline none` line of item 3. Otherwise print `Worktree: <path> (<status>)`, adding `, matched by <match_key>` when `match_key` is not null (a newly created worktree has none). For `match_key` `basename` or `branch` add "reused a worktree not created by /sc:issue". For `record` after `W-ORCA-LIST-FAILED` add "unverified: Orca could not be listed".
 2. "`.dev/issues/<N>/` in the worktree is untracked: do not stage it" only when `tracked_known` is true and `tracked_files` is empty. When `tracked_known` is false, print nothing about tracking. Add "run `make sync-dev` there first" when `<wt>/.claude/` is absent and a step of `next-steps.md` needs a primitive that is not synced into the worktree.
 3. The launch result:
-   - `launched`: "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." For `full`: "It runs every step and stops after implementation." For `full` with `--submit`: "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges." Then print the JSON's `release` line and the two `layers` lines (`L1 guard` first, then `L2 pre-push`) verbatim.
+   - `launched`: "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; run the printed implement command (`/sc:implement <plan path>`) in its tab to let it continue." For `full`: "It runs every step and stops after implementation." For `full` with `--submit`: "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges." Then print the JSON's `release` line and the two `layers` lines (`L1 guard` first, then `L2 pre-push`) verbatim.
    - `already_launched`: "agent already launched at <launched_at>" plus the script's `detail`, which names the two files that hold the `launch` entry (`<D>/worktree.json` and a file in the worktree's git directory); the user removes the entry from both to launch again.
    - `--pipeline none`: "No worktree created and no agent launched. Open .dev/issues/<N>/next-steps.md in this checkout and run its commands in your own session."
 4. Every warning, the worktree one first (print the Wave 7 `warning` as `worktree_warning: <code>`, so an unattended run shows it): the code, its `detail`, and its remedy line from the two tables above. For `W-LAUNCH-FAILED`, also print the launch JSON's `hand_command` when it is not null (the remedy line promises it), and tell the user that an agent started by hand is not governed by the enforcement hook.
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md b/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md
--- a/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md
+++ b/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md
@@ -20,7 +20,7 @@ Never merge anything, and never push to `master` or `main`.
 <!-- block:worktree -->
 Level: worktree. Follow the steps of `next-steps.md` up to the line `Plan boundary: after step <K>` (the number after `after step` is the last step you may run before a human approves). If the line reads `Plan boundary: before step 1`, there is nothing to run yet. Do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.
 
-When the plan exists, print its path and the words `Waiting for approval`, then wait. A human approves by replying `approved` in this session or by running the printed implement command. After that, run the remaining steps, still with no commit, no push and no `/sc:pr-submit`.
+When the plan exists, print its path and the words `Waiting for approval`, then wait. A human approves only by running the printed implement command in this session, a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`. After that, run the remaining steps, still with no commit, no push and no `/sc:pr-submit`.
 
 <!-- block:full -->
 Level: full. Run every step of `next-steps.md` through the last one; the `Plan boundary` line does not apply. Leave all changes in the working tree and stage nothing. Make no commit, push no branch and open no pull request, by any command or skill; if a step would do any of these, skip that part and say so. Finish by printing `git status --short`.
diff --git a/tests/hooks/fixtures/launch_level/ob_h1/README.md b/tests/hooks/fixtures/launch_level/ob_h1/README.md
--- a/tests/hooks/fixtures/launch_level/ob_h1/README.md
+++ b/tests/hooks/fixtures/launch_level/ob_h1/README.md
@@ -12,7 +12,7 @@ What a real observation must capture, per item (design section 11, OB-H1):
 | 2 | item2-skill-keys.json | the input keys of a Skill call and the form of the skill name (`skill` or `name`, with or without `sc:`) |
 | 3 | item3-agent-isolation.json | the tool name for an Agent or Task call and the `isolation` key |
 | 4 | item4-typed-implement-prompt.json | the exact prompt of a typed `/sc:implement x`, and whether the prompt event runs before expansion |
-| 5 | item5-monitor-approved-line.json | the exact prompt of a Monitor line `approved` and of background-Bash and background-subagent notices |
+| 5 | item5-monitor-approved-line.json | the exact prompt of a Monitor line `approved` and of background-Bash and background-subagent notices. The prompt `approved` stays a valid input; since the plain `approved` route was removed, `test_apr_ob_h1_item5_fixture_releases_nothing` asserts it releases nothing |
 | 6 | item6-taskcreate.json | whether `TaskCreate` matches the anchored tool matcher |
 | 7 | item7-sendmessage-mcp.json | the tool names of SendMessage and of MCP tools |
 | 8 | item8-claude-no-p.json | a `claude` command without `-p` |
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -3681,12 +3681,6 @@ def _approve(tmp_path: Path, text: str, **extra):
 
 
 APPROVING = [
-    # T-APR-1: the whole prompt, trimmed and lower-cased.
-    "approved",
-    "Approved.",
-    "  APPROVED!  ",
-    "approved\n",
-    "\t\r\napproved!\r\n",
     # T-APR-2: the first line, leading whitespace removed (case-sensitive).
     "/sc:implement x",
     "/task",
@@ -3698,6 +3692,14 @@ APPROVING = [
     "/task\nsecond line",
 ]
 NOT_APPROVING = [
+    # T-APR-1 (removed route, owner decision Q39): a plain "approved" releases
+    # nothing, whatever its case, trailing mark or surrounding whitespace.
+    "approved",
+    "Approved.",
+    "approved!",
+    "  APPROVED!  ",
+    "approved\n",
+    "\t\r\napproved!\r\n",
     # T-APR-4
     "please approved",
     "approved, but",
@@ -3738,7 +3740,7 @@ def test_apr_exact_form_needed(tmp_path, text):
 
 
 @pytest.mark.parametrize("agent_id", ["agent-1", "a"])
-@pytest.mark.parametrize("text", ["approved", "/sc:implement x"])
+@pytest.mark.parametrize("text", ["/sc:implement x", "/task y"])
 def test_apr_ignored_with_agent_id(tmp_path, text, agent_id):
     # T-APR-3: a subagent prompt never approves (B5, U17).
     _bind(tmp_path, "worktree")
@@ -3747,7 +3749,7 @@ def test_apr_ignored_with_agent_id(tmp_path, text, agent_id):
 
 
 @pytest.mark.parametrize("word", ["full", "full-submit"])
-@pytest.mark.parametrize("text", ["approved", "/sc:implement x", "/task y"])
+@pytest.mark.parametrize("text", ["/sc:implement x", "/task y"])
 def test_apr_ok_written_only_at_worktree(tmp_path, word, text):
     # T-APR-6: FR-L-15, nothing is written at F and FS.
     _bind(tmp_path, word)
@@ -3757,11 +3759,11 @@ def test_apr_ok_written_only_at_worktree(tmp_path, word, text):
 
 def test_apr_unbound_session_cannot_approve(tmp_path):
     # T-APR-7: an unbound id writes nothing, with an empty or a nonempty store.
-    _approve(tmp_path, "approved")
+    _approve(tmp_path, "/sc:implement x")
     assert not _store(tmp_path / "home").exists()
     _bind(tmp_path, "worktree")
-    _approve(tmp_path, "approved", sid="other-session")
-    _approve(tmp_path, "approved", sid=None)
+    _approve(tmp_path, "/sc:implement x", sid="other-session")
+    _approve(tmp_path, "/sc:implement x", sid=None)
     assert _session_files(tmp_path) == [SID]
 
 
@@ -3776,12 +3778,34 @@ def test_apr_degraded_session_can_approve(tmp_path, word):
         "W",
         note=word not in ("worktree\n",),
     )
-    _approve(tmp_path, "approved")
+    _approve(tmp_path, "/sc:implement x")
+    assert _ok_path(tmp_path).is_file()
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")
+
+
+@pytest.mark.parametrize("text", ["approved", "Approved.", "approved!"])
+def test_apr_plain_approved_releases_nothing(tmp_path, text):
+    # Q39: the plain word writes no .ok, so a later /sc:implement call is still
+    # blocked with LL-IMPL; a typed /sc:implement line then releases it.
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, text)
+    assert not _ok_path(tmp_path).exists()
+    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
+    _approve(tmp_path, "/sc:implement x")
     assert _ok_path(tmp_path).is_file()
     _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, None, "WA")
 
 
-@pytest.mark.parametrize("text", ["/sc:implement x", "/task y", "approved"])
+def test_apr_ob_h1_item5_fixture_releases_nothing(tmp_path):
+    # The OB-H1 item 5 fixture (a Monitor line "approved") stays a valid input.
+    fixture = Path(__file__).parent / "fixtures/launch_level/ob_h1/item5-monitor-approved-line.json"
+    prompt = json.loads(fixture.read_text())["prompt"]
+    _bind(tmp_path, "worktree")
+    _approve(tmp_path, prompt)
+    assert _session_files(tmp_path) == [SID]
+
+
+@pytest.mark.parametrize("text", ["/sc:implement x", "/task y"])
 def test_apr_typed_implement_then_skill_call_allowed(tmp_path, text):
     # T-APR-9: FR-L-18, in order: the Skill call is blocked before the prompt,
     # the prompt event writes .ok, then the expanded Skill call is allowed.
@@ -3812,7 +3836,7 @@ APR_STILL_BLOCKED = [
 def test_apr_approval_never_unlocks_commit_push_submit(tmp_path, payload, msg_id):
     # T-APR-5: FR-L-17, the typed approval gives WA, which unlocks IMPL only.
     _bind(tmp_path, "worktree")
-    _approve(tmp_path, "approved")
+    _approve(tmp_path, "/sc:implement x")
     result = _run(payload, tmp_path)
     _assert_decision(result, tmp_path, msg_id, "WA", text=_text_note(payload, msg_id))
 
@@ -3824,7 +3848,6 @@ def test_apr_failed_write_shows_later_as_impl(tmp_path):
     sessions = _bind(tmp_path, "worktree")
     sessions.chmod(0o500)
     try:
-        _approve(tmp_path, "approved")
         _approve(tmp_path, "/sc:implement x")
         assert sorted(p.name for p in sessions.iterdir()) == [SID]
         result = _run(_skill("sc:implement"), tmp_path)
@@ -3839,7 +3862,7 @@ def test_apr_existing_ok_link_never_followed(tmp_path):
     _bind(tmp_path, "worktree")
     target = tmp_path / "elsewhere"
     _ok_path(tmp_path).symlink_to(target)
-    _approve(tmp_path, "approved")
+    _approve(tmp_path, "/sc:implement x")
     assert not target.exists() and _ok_path(tmp_path).is_symlink()
     _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
 
@@ -3847,7 +3870,7 @@ def test_apr_existing_ok_link_never_followed(tmp_path):
 def test_apr_lasts_until_a_person_deletes_the_files(tmp_path):
     # O-6: later prompts and calls never remove the approval.
     _bind(tmp_path, "worktree")
-    _approve(tmp_path, "approved")
+    _approve(tmp_path, "/sc:implement x")
     for text in ("please approved", "/sc:pr-submit", "approved", "anything"):
         _approve(tmp_path, text)
     assert _session_files(tmp_path) == [SID, f"{SID}.ok"]
@@ -3882,7 +3905,7 @@ def test_apr_prompt_runs_no_sed_or_tr(tmp_path):
     # Trimming and lower-casing are bash string operations.
     log = _counting_bin(tmp_path)
     _bind(tmp_path, "worktree")
-    _approve(tmp_path, "  APPROVED!  ")
+    _approve(tmp_path, "  /sc:implement x")
     _approve(tmp_path, "please approved " * 1000)
     assert _ok_path(tmp_path).is_file()
     assert not log.exists()
@@ -3894,7 +3917,7 @@ def test_trn_turn_blocked_before_and_allowed_after_typed_approval(tmp_path, tool
     _bind(tmp_path, "worktree")
     payload = _tool(tool, prompt="approved")
     _assert_decision(_run(payload, tmp_path), tmp_path, "LL-TURN", "W")
-    _approve(tmp_path, "approved")
+    _approve(tmp_path, "/sc:implement x")
     _assert_decision(_run(payload, tmp_path), tmp_path, None, "WA")
 
 
diff --git a/tests/skills/test_issue_orca_worktree.py b/tests/skills/test_issue_orca_worktree.py
--- a/tests/skills/test_issue_orca_worktree.py
+++ b/tests/skills/test_issue_orca_worktree.py
@@ -1167,6 +1167,15 @@ def test_pr4_prompt_no_pr_tokens_outside_the_worktree_prohibition_and_submit(
         assert token not in common, token
 
 
+def test_pr16_worktree_prompt_never_tells_the_agent_to_wait_for_approved(
+    tmp_path: Path,
+) -> None:
+    # Q39: the plain `approved` reply no longer releases a worktree-level agent.
+    worktree = render(tmp_path, "worktree")[1].read_text()
+    assert "`approved`" not in worktree and "replying approved" not in worktree
+    assert "only by running the printed implement command" in worktree
+
+
 def test_prompt_unusable_template_is_reported_not_raised(tmp_path: Path) -> None:
     proc, out = render(tmp_path, "full", template=tmp_path / "missing.md")
     data = json.loads(proc.stdout)


Codegraph context
index_state: fresh
checked_at: 2026-11-16T21:51:31Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: ran on the Grep/Read floor (the guard is a shell script; its dependents are the tests and docs in the diff).

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
