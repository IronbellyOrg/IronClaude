## Feature Summary

One issue that replaces #450 and the open parts of #331 and of the coordinator handoff. The orchestrator, a skill named `orchestrator` with the command `/sc:orchestrator` built in IronClaude, polls GitHub for issues assigned to the user and makes sure each has a plan (Priority, Fix approach and Test plan, the format of #651; an issue without one is held, and a plan is created through `/sc:issue --plan`). It claims the issue, hands the work to a supervised worker in the issue's own repo and worktree, watches the worker and its pull request, merges when every condition holds, runs the closeout and an audit (an issue the pull request did not finish goes back for another round), and keeps the work report current. Planning is done once; cheaper models then execute. When nothing is new, no agent starts and no tokens are spent.

The history of #331, #450 and the coordinator handoff, and the full list of what was carried over and dropped, is in a separate comment: [History and carried-over detail](https://github.com/IronbellyOrg/IronClaude/issues/655#issuecomment-6991418475). This body holds the current design and the workflow.

**Body synced with the approved spec (2026-11-19).** The design is the spec `docs/designs/orchestrator.md` on branch `clayphi/issue-655-spec`, approved by Clay together with additions A to E (ruling 37); where this body and the spec differ, the spec wins. **A** the hold and acceptance check (`hold:plan`, `hold:backlog`) and plan creation through `/sc:issue --plan`; **B** what reaches Clay (one nine-row table, on from the start); **C** what the orchestrator may do and may never do; **D** the closeout, its own issue #668 (`/sc:closeout`), and the hand-back of a not-done issue; **E** the audit after a pull request lands, the never-merge rule for `changes_requested` and the merge-safety hold. Rulings 23 to 39 are in section 10.

**Models (Clay, 2026-11-19):** stronger models plan and cheaper models build. The agents the orchestrator starts run on ccsession tiers named in `repos.yaml`, never on model ids, with a per-repo override: `plan_tier` (the plan call, default `tier1b`; it sets the depth of `/sc:issue --plan`), `worker_tier` (default `tier2`) and `orchestrator_tier` (default `tier1b`). A tier the user cannot use falls once to the next allowed tier and is recorded; a tier the gateway refuses is row 9. Spec 5.8.

## Problem Statement

The work to pick up assigned issues automatically is spread over #331 (closed; the built `superclaude issue-watch` poller, never run live), #450 (open, blocked: live test, shadow run, cron) and the coordinator handoff (a plan-approval step after the claim). All of it is built around layers that Clay's 2026-11-18 rulings remove: a trigger label, an approval label and approver list, a Project in the Backlog column, a plan-approval gate after the claim, a separate watcher session, and cron. The watcher also works on one repository only (`REPO` at `src/superclaude/cli/issue_watch/github.py:37`, `ORIGIN_REPO` at `launch.py:50`), and `/sc:issue --claim` resolves its repository from `origin` only. Nothing today holds an issue that has no plan, decides whether a merged pull request finished its issue, or audits how a pull request landed.

## User Story

As an owner who is assigned issues in several repositories, I want one orchestrator that polls on a schedule, holds an issue until it has a plan, claims what is assigned to me, starts the right worker in the right repo and worktree, and carries the work through merge, closeout and, if needed, another round, so that I never start the work by hand and nothing is spent when nothing is new.

## Proposed Solution

### 1. How it works, end to end

1. An Orca automation runs a poll script every 5 minutes (configurable). The schedule reuses the work-report waker pattern from the IronFlow repo (`.claude/skills/agent-work-report/SKILL.md`, Input section; `scripts/waker.py`): the automation runs the script as its precheck and the script exits non-zero, so Orca starts no agent and leaves no terminal. The script routes each new issue to an orchestrator of the issue's repo with a free place (starting one if none) and wakes it only when something is new.
2. The script finds, since the last poll: new issues assigned to the user (only the user's own GitHub login counts); comments that mention the user; issues that could be assigned to the user; and issues and pull requests that affect the user's work. Only assignment triggers a claim; the rest is passed on as information. With nothing new, no agent starts and no tokens are spent. At switch-on the issues already assigned count as seen (an older one is handed over with `/sc:orchestrator --take <repo>#<N>`); an unacknowledged wake is tried up to 3 times.
3. **The hold (addition A).** Before an assigned issue is sent on, the poll checks its body with a script: `## Priority`, `## Fix approach` and `## Test plan` must each be present once and filled in. An issue that fails gets the label `hold:plan` (a label only, never a comment) and is not sent to an orchestrator; when the check passes, the poll removes the label. A person's label `hold:backlog` makes the system do nothing with the issue until it is removed. A hold removed by hand stays removed. After one hour with no plan work elsewhere the poll sends ONE plan request to the repo's orchestrator, which makes the plan through `/sc:issue --plan` (section 5). Assignment stays the only trigger: the hold is a precondition, not an approval.
4. For each assigned issue that passes, the orchestrator runs the workflow of section 2: claim, plan record, report entry, handoff and worker start, watching, pull request watch, merge, closeout and audit, completion.
5. **One orchestrator per repo, at most 3 issues in flight each** (Clay; `max_in_flight` in `repos.yaml`). In flight: from the moment the poll routes the issue until it is closed, dropped or escalated; an open plan request also takes a place. The poll alone routes each issue, under its lock, to an orchestrator of the repo with a free place, or starts another; an idle one ends, a dead one is restarted; the report coordinator stays separate (spec 5.7).
6. The orchestrator reads the repo list and the repo-to-checkout map from the private orchestrator repo `IronbellyOrg/IronOrchestrator`, where the orchestrator sessions run, not from IronClaude configuration. Workers start in the issue's own repo and a worktree there.
7. **The report is a living document** (Clay, 2026-11-19): the daily run no longer touches issue entries; the daily report is being phased out (section 7).

### 2. The orchestrator's runtime workflow

`SKILL.md` carries this as numbered waves. Each wave has a ref (`refs/<name>.md`, loaded only at that wave), its commands, its template and the check that ends it. Escalation can end any wave: the orchestrator fills the escalation template and waits (section 9). Detail: spec 5.3.

| Wave | What it does | Orca and SC commands | Template it fills | Check that ends the wave |
|---|---|---|---|---|
| 0. Intake (`refs/intake.md`) | Loads Orca's `orchestration` skill, binds the Run, reads the wake, checks each issue's repo against the orchestrator repo's list, takes every issue of its own wake (a wake for another orchestrator is refused). For a plan request: reads the issue live, writes the plan record first and the acknowledgment second, calls `/sc:issue --plan` | `orca skills get orchestration`; `orca orchestration run-create` once, `run-use --id <run>` after a restart; `Skill sc:issue-protocol --plan <N> --depth <d>` | None (the wake has a fixed format set by the poll) | Every issue in the wake has a repo, a checkout and a state (new, already claimed, or skipped with a reason); a plan request ends with the body passing the plan check or an escalated failure |
| 1. Claim (`refs/claim.md`) | First re-reads the issue live (a plan must exist, no `hold:backlog`), then runs the claim workflow at `--pipeline none`: assign, accuracy check, summary, next steps, the accuracy-check and "Claimed by" comments | `/sc:issue --claim <N> --pipeline none` (it calls `/sc:recommend` itself) | The claim's own templates (`sc-issue-protocol/templates/`) | The "Claimed by" comment (marker `<!-- sc:issue:claim -->`) exists and the claim reports success; a closed, held or otherwise-assigned issue, or a pull request, stops with no write |
| 2. Plan record (`refs/plan.md`) | Records the sha256 of the body it hands the worker (`body_sha`); starts no agent. In a hand-back round it first updates the plan (wave 8) | `/sc:issue --plan <N> --remaining <file>` in a hand-back round only | None (`plan-check` checks the #651 formats) | `body_sha` is recorded |
| 3. Report entry added (`refs/report.md`) | Adds the issue's entry to the living work report, with the human assignee, the orchestrator and the state not-started | `superclaude orchestrator report-entry` | `templates/report-entry-update.md`, following the work report's `item-template.md` | The entry is in the report with the assignee, a follow-up state and a last-update time |
| 4. Handoff and worker start (`refs/handoff.md`) | Fills the handoff prompt, makes the worktree, creates the Task, starts the supervised worker, links the issue, puts the session link in the entry | `orca orchestration task-create --spec <filled handoff>`; `worker-start --task <id> --worktree path:<worktree> --agent claude` (the worktree is made first by `orca_worktree.py worktree`); `orca reference add`; `worker-show`. The worker then runs `/sc:workflow` if needed, `/sc:implement`, the regression gate and `/sc:pr-submit --monitor 3` | `templates/handoff-prompt.md` (nine sections, section 4); `templates/report-entry-update.md` | `worker-start` reported `ready` and a Dispatch exists; the entry shows the session link and state working. An unknown outcome is checked once and retried once; a second failure is row 9 |
| 5. Watching (`refs/watch.md`) | Handles worker messages, gathers milestones, runs the hourly check-in for each running worker until its `worker_done`, applies the playbook and the permission rules, and does every check-in itself (typing and approvals included) | `orca orchestration check --wait --types "worker_done,escalation,question"`, `reply`, `send`, `ask`, `worker-show`, `worker-read`, `gate-create`, `gate-resolve`; FR-23 and FR-24 | `templates/worker-checkin.md`; `templates/report-entry-update.md`; `templates/escalation.md` | The worker sent a valid `worker_done`, or it was escalated and the human answered; every milestone reached is in the entry |
| 6. Pull request watch (`refs/pr-watch.md`) | Decides readiness the way `/sc:pr-submit --monitor 3` does: CI, the Augment and Codex reviews, open threads, and any open "changes requested" review; an already merged pull request goes straight to wave 8 | The `superclaude.pr_submit` core, `scripts/poll-ci-checks.sh`, `scripts/poll-augment-review.sh`; `superclaude orchestrator merge-gate` (13 closed reasons) | `templates/report-entry-update.md` | On the final head: every check green, every review agent finished, no open thread, no `changes_requested`, no merge-safety hold, and `worker_done` received |
| 7. Merge (`refs/merge.md`) | Merges when wave 6 ended clean; a failing check waits for the human's explicit OK; `changes_requested` is never merged; a merge-safety file change waits for Clay's explicit OK | `gh pr merge --match-head-commit` pinned to the issue's repo, with the repo's own method from `repos.yaml`; `gate-create` | `templates/escalation.md`; `templates/report-entry-update.md` | `gh` shows the pull request merged; the entry says merged |
| 8. Close, closeout, audit, and drop the entry (`refs/close.md`) | Runs `/sc:closeout`, which decides whether the issue is done and closes it only then; runs the audit; updates the entry. A not-done issue is handed back: old worker final, plan updated, new worker started (section 7) | `Skill sc:closeout-protocol <PR>`; `superclaude orchestrator audit`; `report-entry --closed` or `--update`; `superclaude orchestrator handback` | `templates/report-entry-update.md` | The issue is closed and the entry gone; or the issue is handed back and in flight again; or the case is escalated (row 9) |
| 9. Completion accounting (`refs/completion.md`) | Settles the worker (reuse, retain or release its terminal) and prints the return contract | `orca orchestration worker-release` (or `worker-retain`); `worker-list --run <id> --terminal-state reclaimable` | The return contract | `worker-list` shows no reclaimable terminal for the Run, and the return contract is printed |

### 3. Deliverables

- **The orchestrator**: the skill `orchestrator` and the command `/sc:orchestrator`, in IronClaude, with the workflow of section 2, the templates of section 4, the playbook (FR-23) and twelve `superclaude orchestrator` verbs.
- **The poll script** the Orca automation runs, with the safety features carried over (section 11), the hold of addition A and 62 closed reason names.
- **The `/sc:issue --plan` mode** (with `--remaining`), its own small pull request built before the orchestrator skill (section 5).
- **The four templates**, each a file with a test (section 4).
- **The orchestrator repo** (the private `IronbellyOrg/IronOrchestrator`), where the orchestrator sessions run. All skills live in IronClaude; everything the orchestrator keeps while it runs lives there: the coordinator spec, the work report and its state files, the daily run's records, the repo list, the repo-to-checkout map and an overview of each repo.
- **Work report integration** (section 7) and the **defined checks** (section 8).
- **Moves and spec sync:** the coordinator spec and work report state move to the orchestrator repo, the `agent-work-report` skill moves into IronClaude, and the IronFlow copy of the spec is kept updated (FR-13, FR-1, FR-2, FR-19, rows C25 to C29 of spec 6.3).
- **The closeout** is not part of this issue: it is issue #668 (`/sc:closeout`), a dependency that must merge before the live test.
- **How the work is split and ordered** (section 13) and **the tests** (section 14).

### 4. The skill's structure and templates

The command is a thin file, `src/superclaude/commands/orchestrator.md` (Usage: `--wake <wake_id>`, `--hourly`, `--resume`, `--take <owner/repo#N>`). The protocol skill is `src/superclaude/skills/sc-orchestrator-protocol/`, modelled on `sc-issue-protocol`, `sc-pr-submit-protocol` and `sc-troubleshoot-protocol`: a mandatory Activation section; a `SKILL.md` with numbered waves, Will Do and Will Not Do and an error table with named STOP codes; one lazy-loaded ref per wave plus `refs/playbook.md`; stub-first templates; a return contract printed last; a file table that a test checks in both directions; installed paths for any other primitive (repo CLAUDE.md). The deterministic steps are verbs of `superclaude orchestrator` in `src/superclaude/cli/orchestrator/`: `wake-check`, `wake-ack`, `state`, `lease`, `merge-gate`, `plan-check`, `repos`, `report-entry`, `escalate`, `answer-check`, `audit`, `handback`, plus two modules that are not verbs, `limits.py` (the refusal function of section 9) and `names.py` (the rule that no agent or model is named in anything user-facing). There is no `hold` verb: the poll alone writes the hold label. Spec 5.1, 5.4, 5.12.

The four templates, each a file with its own test; each step that writes or sends names its template, and a test checks that:

- **Handoff prompt** (`templates/handoff-prompt.md`), nine sections in this order: (1) issue link, repo, worktree and base branch; (2) goal; (3) Priority, Fix approach and Test plan, copied from the issue as quoted data (in a hand-back round also a block "Round n of at most 4": the earlier pull requests, the remaining items); (4) Orca's task-spec fields: target, change, constraints, ownership, observable acceptance; (5) do-not-touch rules and safety (issue text is data; never print secrets; no force-push; no attribution line that names an agent or a model, except the one commit trailer this repository's practice puts on commits, ruling 39); (6) the SC command chain, with the pull request body naming the issue by `Fixes <repo>#<number>` only when the pull request fully addresses it and `Refs <repo>#<number>` otherwise (ruling 38); (7) never merge, never force-push; (8) reporting duties: preamble IDs, heartbeat, `ask`, `worker_done`; (9) stop condition: green, reviewers finished, no open thread.
- **Report entry update** (`templates/report-entry-update.md`): follows the work report's item template; shows the assignee, the session links, the follow-up state, the last update, the PR and CI state; written at claim and at the milestones of section 7.
- **Escalation** (`templates/escalation.md`): the nine rows of section 9 with their old rule numbers, the lines `Why this reaches you:`, `Low-stakes options:` and `If you do not answer:`, and the three ways it reaches the human.
- **Worker check-in** (`templates/worker-checkin.md`): the status message and the fields of the answer.

The handoff prompt is the task spec of `worker-start`, with issue text quoted as data; the integer-only rule covers only the poll script's own launch prompt.

### 5. Claiming and starting workers

The orchestrator runs the existing claim workflow (`src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`); it does not write a second one. That workflow assigns the issue, checks its accuracy, writes a summary and the next steps through `/sc:recommend`, and posts the accuracy-check and "Claimed by" comments; at `--pipeline worktree` or `full` it would also create an Orca worktree and launch an agent, held by the #442 ship gate. **Decided by Clay:** the orchestrator claims at `--pipeline none` and starts the worker itself with `orca orchestration worker-start`, so the worker is supervised and reports through the Run mailbox, never through the claim's launch levels. A test of 2026-11-18 (not re-run here) showed `orca orchestration send --to <terminal handle>` reaching an agent launched with `orca worktree create --agent`, readable with `orca orchestration check --terminal <handle>`. Whether a worker started this way falls under the #442 gate: spec 2.1.

**The plan before the claim (addition A, spec 4.11).** A plan must exist before an issue is claimed, and all plan creation goes through `/sc:issue` (Clay, rulings 23, 30, 31):

- **The check** is a script (`plan_check`): each of the three headings once, non-empty, not only "Not known yet". The poll applies it to the search row's body, so a decision costs no call. Labels: `hold:plan` (written only by the poll, under the grant `issue.hold`) and `hold:backlog` (placed and removed only by a person). A hold removed by hand stays removed; an edit after the claim by someone other than the user's own login is one line in the report entry and nothing else.
- **The plan request.** After one hour in which nothing changed (the quiet clock moves on any change, a linked branch, pull request or session), the poll sends ONE `plan_requests[]` item to an orchestrator of the repo that has a free place (it takes one of the three places; a new orchestrator is started only when the repo has none). The orchestrator writes the plan record `.orchestrator/issues/plan-<key>.<requested_at>.json` first and the acknowledgment second, so a crash cannot lose the request, then calls `Skill sc:issue-protocol --plan <N> --depth <d>` (`<d>` from `plan_tier`). The issue stays held and unclaimed; the poll lifts the hold when the plan passes the check. A call that fails twice, or a repeated heading, is escalated; a call unfinished after 60 minutes raises the poll reason `plan_stuck`.
- **PR P, the `/sc:issue --plan` mode**, is its own small pull request, built before PR B: it changes `commands/issue.md`, `SKILL.md`, the new `refs/plan.md` and the two issue test files. It appends an absent section, fills an empty one in place, stops on a repeated heading, and makes one marked body edit and no comment. Its `--remaining <file>` option rewrites `## Fix approach` and `## Test plan` to the scope that is left (done items kept) for a hand-back round. Spec 8.3.
- **At the start of wave 1** the orchestrator re-reads the issue live: no `hold:backlog` and a plan that still passes, or nothing is claimed.

### 6. Orca's built-in orchestration

The orchestrator uses Orca's own orchestration layer: `run-create` and `run-use` (one Run per orchestrator, resumed after a restart); `task-create`, `task-update`; `worker-start` (the filled handoff as task spec) and `dispatch`; the mailbox (`send`, `check`, `ask`, `reply`, `inbox`); `gate-create` and `gate-resolve`; `worker-show`, `worker-read`, `worker-release`; `orca reference add` and `find`; `orca worktree ps`. It never runs `worker-stop` or `worker-abandon` (section 9).

Orca ships an `orchestration` skill. The orchestrator skill loads it at run time (`orca skills get orchestration`) instead of copying it, and cites its supervised loop, its task-spec contract and its completion accounting (a valid `worker_done` settles the Task; each settled worker is reused, retained or released). Clay's coordinator spec names FR-8 and FR-9 for the same commands. The handoff also satisfies the brief layout of `src/superclaude/core/WORKER-CONTRACT.md`.

### 7. The work report, and watching the pull request and merging

**One design with Clay's coordinator spec** (`.dev/specs/SPEC-AGENT-WORK-COORDINATOR-20261027.md`, today in the IronFlow repo and moving to the orchestrator repo; FR-1, FR-7, FR-9, FR-19, FR-20, FR-21 cited, not copied). This orchestrator is that spec's `/agent-coordinator`: it sweeps the sources, routes, hands off with a self-contained work package and tracks ownership. There is no session-manager skill, now or later (Clay): the orchestrator does every check-in itself, including typing into a worker's terminal and approving its permission prompts under FR-23 and FR-24; the check-in template and the playbook are part of the skill's one PR. The IronFlow copy of the spec is kept in sync, not the home.

**Report entries.** The entry follows the work report's item template and the follow-up states of FR-9 (working, question, gated, delivered, claimed-missing, stalled, failed, not-started). It shows the human assignee, the orchestrator that holds the issue and the worker's session, the last two as links that open them in Orca. The report is a living document (Clay, 2026-11-19): the entry is added at claim and updated at milestones: plan done, blocked or asking, PR opened, review rounds summarized, PR ready, merged; not on every worker message or CI change, and not hourly for a green PR that is waiting. When the issue closes, the entry leaves the report. Escalations and notices about an orchestrated issue are lines of that issue's own entry (ruling 24).

**Daily run.** The daily run no longer touches issue entries. It covers only ClickUp tasks and messages, direct messages, mentions, items with no issue, sessions not under an orchestrator, and a missed-update sweep. The daily report itself is being phased out. This changes the spec's FR-2 and FR-19 (a dependency).

**Pull request and merge.** The worker pushes its own branch and opens its pull request; it never merges or force-pushes. Only the orchestrator merges, and only when every check is green on the final head, every review agent the repo lists (Augment, Codex) has finished on that head, no review thread is open, no review is left at "changes requested" (a hard refusal that no recorded OK overrides), and the worker has sent `worker_done`. A failing check is never merged without the human's explicit OK. A review agent that does not run or finish holds the pull request and escalates (row 9); `reviewers: none` means no hold. **Merge-safety hold (Clay, ruling 35):** a pull request that changes CI or another file on the repo's `merge_safety_files` list (a `repos.yaml` field; default: workflows, branch protection and ruleset files, CODEOWNERS, and the files the repo's merge gate reads) waits for Clay's explicit OK even when green and reviewed. The OK is tied to the question key `merge_safety:<PR>:<head sha>` (a new push needs a new OK; the OK for a failing check never clears it); the file list is the paginated REST list with old and new paths, and an unreadable list is a hold, never "no match". The merge method is the repo's own (`repos.yaml`: `merge_method`, `release_merge_method`; IronClaude squashes ordinary pull requests and merges a release pull request with a merge commit). Every `gh` call is pinned to the issue's own repo, never to an upstream parent. For THIS build no pull request is merged by the orchestrator session or any worker: each stops at green and the owner does the QA and the merge. Readiness reuses the `superclaude.pr_submit` core and the poll scripts of `/sc:pr-submit --monitor 3`. Clay's spec lists merges as human-only (FR-13); this issue takes merges and closing off that list (spec 6.3).

**Closeout (addition D, issue #668).** After a merge, including a merge made by a person, wave 8 calls `/sc:closeout <PR>`, a separate skill that adopts Jay Wedgeworth's closeout (Clay, rulings 19 to 22; its own issue #668, merged before the live test; PR B's tests use a fake). It decides whether the issue is done by reading the issue's own criteria (Fix approach, Test plan, acceptance criteria, "Done when") against what the pull request and its linked pull requests delivered, never by the words `Fixes`, `Closes` or `Refs` (ruling 32). Done: it closes the issue with one note; the orchestrator no longer runs `gh issue close`. Unclear after investigating: escalated (row 9). Every worker pull request links its issue with `Fixes <repo>#<number>` only when it fully addresses the issue and `Refs <repo>#<number>` otherwise (rulings 26 and 38): GitHub closes an issue on `Fixes`, so a part-done round says `Refs`; a wrongly written `Fixes` still closes the issue and no script checks it (K28).

**Not done: the hand-back (Clay, ruling 36).** A closeout that finds the PR did not finish the issue goes back to the orchestrator to start the work that was not done, by the same workflow. The closeout leaves the issue open with one note, returns the unmet criteria and starts nothing. The orchestrator (not Clay) then records what remains (`round`, `remaining` in the state file; the entry says "merged, the issue is not finished: ... (round n)"), waits until the old worker is final (`worker_done` received; it never stops a worker), releases it, updates the plan through `/sc:issue --plan <N> --remaining <file>`, and starts a new worker on a new branch `issue-<N>-r<n>` in the reused worktree through waves 4 to 9 (the issue stays in flight; the guard looks at tracked changes only). The verb `handback` bounds it: at most 3 hand-backs (4 rounds), and a stop when a round leaves the same unmet criteria; a stop, a failed re-plan or an unusable worktree is row 9 in the issue's own entry. Spec 5.3 wave 8.

**Audit after a pull request lands (addition E, spec 5.11).** `superclaude orchestrator audit` (no model) runs eight checks adapted from Jay's audit on the pull request that landed, whoever merged it: AU1 force push, AU2 review dismissed, AU3 thread resolved with no real reply, AU4 merged over a change request, a pending review request or an unresolved thread, AU5 conflict markers, AU6 baseline or tests loosened, AU7 merge-safety control changed, AU8 a bot fix after a "@codex fix this" style request (a warning only). The result goes into the entry. Only AU4a, AU4c and AU5 reach Clay (row 8); warnings never do; the orchestrator opens no follow-up issue.

### 8. Every check, defined

| Check | What runs | How often | What triggers it |
|---|---|---|---|
| New issues | The poll script, run by the Orca automation; no model unless something is new; it also applies the hold of section 1 | Every 5 minutes (configurable) | The clock |
| Worker messages | The orchestrator reading the Orca mailbox (`worker_done`, `ask`, escalation, heartbeats) | As they arrive | Each message (`orca orchestration check --wait`) |
| Worker status | A status check of every open worker: state read from Orca, a check-in by the orchestrator itself where needed; it also reads the issue (closed, assigned elsewhere, edited by someone else); the entry is updated only at a milestone | Hourly by default and configurable, for each running worker, Monday to Friday, 24 hours a day; it stops for a worker at its `worker_done` | The clock |
| Daily report | The daily run of the work report, covering only what the orchestrator does not (section 7); it no longer touches issue entries and is being phased out | Monday to Friday, default 07:00 local, from FR-2; configurable | The clock |

Two runs never overlap (the run lock of FR-2). How the poll and the spec's waker (FR-25) fit together: see the spec.

### 9. What the orchestrator handles itself and what goes to the human

Cited from Clay's spec: FR-10 (escalation and management of agents), FR-23 (the playbook, a file in the skill) and FR-24 (permission approvals). Detail: spec 5.6 and 5.9.

**The orchestrator handles itself** everything not in the table below, and records what it decided and why in the report entry: sorting each worker into an FR-9 state; unsticking a worker by the FR-23 playbook; answering a worker's question when the sources answer it; approving a permission prompt under FR-24 when the action is not in rows 1 to 7; merging when every merge condition holds; the closeout and the hand-back. Agents may close issues and delete ordinary files as their work needs. When in doubt, a case does not reach Clay.

**What may reach Clay (addition B, Clay's rulings 16 and 24).** One table of nine rows replaces the old eight rules (their numbers survive in "was"). A case reaches him only when it fits one row, and its entry names that row:

| Row | It reaches Clay when it needs | Covers (was rule) |
|---|---|---|
| 1 | his own identity | acting or speaking as him; contact outside Ironbelly (1) |
| 2 | a secret | a key, token or login only he holds; any request to write a secret anywhere |
| 3 | money | spend, pricing, billing (1) |
| 4 | a legal act | a contract, terms, a filing, a signature |
| 5 | something that cannot be undone, or changes shared settings | publishing or tagging a release; deleting a shared branch; a force push; a settings change (1); deleting a skill or an agent the issue does not name (2) |
| 6 | other people's access or data | giving, removing or changing anyone's access; their data |
| 7 | a breaking change | something other people or systems rely on stops working |
| 8 | a decision only he can make | a scope that creeps into peripheral features (4); a question still unanswered after the issue, the code, the docs and a web search (5); a choice that changes what the product does (6); merging over a failing check or a pull request that changes a merge-safety file, which wait for his explicit OK (3) |
| 9 | him because it is stuck and nobody else can unstick it (a stop, not a decision) | a worker the check-in did not unstick the same day (7); a failed handoff (8); a pull request held because a review agent never ran or has a `changes_requested` review, a merge his rights forbid; a closeout that stayed unclear or failed; a hand-back that reached its bound |

- The rules are on from the start: no warn phase, no ladder. `superclaude orchestrator escalate` refuses an entry that names no row. An unanswered question waits and nothing is decided for Clay: the entry says what stays blocked and what continues (`If you do not answer:`). Every answer is checked first (`answer-check`: Clay's own typed input or his ClickUp reply, newer than the entry, for the right question); no tap, click or reaction answers anything. Tagging or publishing a release always needs a recorded human OK. Notices (a ClickUp DM, else the Orca unread mark) are capped at `reach_daily_max` (5 per repo per 24 hours, ruling 39); an entry is never dropped. The ways to reach him: lines of the issue's own entry, an Orca decision gate, and the notice.
- Merging and closing issues are not in the table (ruling 13).

**What the orchestrator may do and may never do (addition C, spec 5.9).** It controls Orca sessions: list, read (at most 200 transcript messages), send work, wait on its own mailbox, answer an approval once, delete the ordinary files its work needs (ruling 25; removal of that line was rejected), tag or publish a release only with a recorded OK. It may interrupt a worker's current turn in ONE case, when a major issue must be escalated to Clay: `escalate --interrupt`, only after the escalation is written; this one send is exempt from the 60-second typing hold (five places of the coordinator spec change, spec 6.3 C25 to C29). Restarting a dead agent stays as FR-23 says (ruling 29). The "may never" list, each line with a test and one refusal function `refuse(argv)` in `limits.py` that every verb's `gh`, `git` and `orca` call passes through: never a permanent "always allow"; never delete a shared branch, another person's data, or a worktree or session it did not start; never change credentials, mint or rotate secrets, or control machine lifecycle (`coder`, `systemctl`, `orca automations create`, `edit`, `remove`, `run`); never tag or publish a release without a recorded OK; never stop a worker (`worker-stop`, `worker-abandon`) apart from that one interrupt; never write outside `grants` or `repos.yaml`.

### 10. Clay's rulings (2026-11-18 and 2026-11-19)

**2026-11-18**

- The only trigger is assignment: no trigger label, no approval label, no approver list, no plan-approval gate after the claim. It is safe because only users with triage or write access can assign an issue (stated by the owner; UNVERIFIED here). The hold of section 1 is a precondition, not a trigger.
- The Backlog column may stay on the board, but nothing may depend on it. An Orca automation runs the schedule, not cron.
- If a launch outcome is unknown, the orchestrator checks for the session itself and retries once; no command is printed for a person. GitHub throttling uses exponential backoff; an unrecognized GitHub error is a login failure until the live test shows the real text.
- The poll sends data to an agent only when something new arrived. The live test uses throwaway issues that are only assigned.

**2026-11-19** (the owner's rulings are kept in `RULINGS.md` of the orchestrator session; the spec cites them by number)

- Report and people: the living report (1); no session manager, ever (2); only the user's own GitHub login counts, no bot list (11); the agent is never named in anything user-facing, people by name (15); plain English, no em or en dashes, no secrets (17).
- Workers and merging: workers push and open PRs, never merge or force-push; only the orchestrator merges (3, 13); the poll starts an orchestrator when none runs (4); merge method per repo (5); review agents that do not run or finish hold the PR (6); worker check Monday to Friday, 24 hours a day (7); one orchestrator per repo, 3 in flight (8); existing issues seen at switch-on, 3 delivery tries, retire the approval code first, repo name IronOrchestrator (9); tiers, never model ids (12).
- Additions: A (23, 30, 31, 33, 39): the hold, one hour, a label and no comment, `hold:backlog`, a hold removed by hand stays removed, plan creation only through `/sc:issue`. B (16, 24, 39): the hard bar (releases, pricing, other people's access and data, deleting shared branches, breaking changes), rules on from the start, an unanswered question waits, a release needs a human OK, 5 notices a day per repo. C (25, 29): interrupt allowed, deleting ordinary files allowed, the restart of a dead agent kept (14 is superseded). D (19 to 22, 26, 32, 36, 38): closeout is issue #668 and adopts Jay's skill; it decides by whether the issue is done; a not-done issue goes back to the orchestrator; `Fixes` only when fully addressed, else `Refs`. E (27, 34, 35): audit findings reach Clay as recommended, `changes_requested` never merged, a bot-fix warning, the merge-safety hold. Naming (28). Removals 1, 3, 4, 5a yes; 2 and 5 rejected (29).
- Order and approval: wait for A to E (20); Clay approved the draft and the spec (37). The owner decisions OD1 to OD15 are in spec section 10.

### 11. Carried over and dropped (summary; full detail in the history comment)

- **Carried over:** reuse of the built `issue-watch` code as the poll step (`runner.py`, `record.py`, `audit.py`, `launch.py`, the budget and rate-limit code in `github.py`; `cycle.py` reshaped) with its safety features (one claim and one worker start per issue, up to 3 delivery tries, a run lock, a call budget, an audit log, a dry-run mode, a validated integer in the launch prompt, an origin check); the live test replacing the `_assumed_shape` fixtures; the shadow run, lock test and restart test; FU-3, FU-4, FU-5, FU-6, FU-8, FU-10, FU-11, FU-12; #442's launch checks; owner questions Q1 to Q4.
- **Dropped on purpose:** the trigger label; the approval label, approver list and FU-9; the Project and Backlog requirement; the plan-approval gate (WC-17, the `issue-pipeline` approval rows and `stage-status`, the approval part of guard G2); cron (FU-2); FU-7. Replaced by the additions: the plan agent of wave 2 (now `/sc:issue --plan`), the orchestrator's own `gh issue close` (the closeout closes), and the eight escalation rules (now the nine-row table).

### 12. Build procedure, with the SC commands and the check for each step

1. **Spec: done.** `/sc:design` produced `docs/designs/orchestrator.md` (branch `clayphi/issue-655-spec`), reviewed in rounds, with additions A to E merged in; Clay approved it (ruling 37). It answers every open question of this issue and gives every carried-over item a disposition and every dropped item a removal plan.
2. **Plan.** `/sc:workflow` on the spec. Check: a tasklist in which every task names its files and an acceptance check, with the PR split below.
3. **PR split** (spec 8.1; the workflow confirms or changes it): **PR D** retire the gate first (Clay): the approval code in `issue_pipeline`, WC-17, the issue pipeline duties of WORKER-CONTRACT and guard G2 rule 1; **PR A** the poll core: assignment-only discovery, the repo list and map, the new-since-last-poll rule, routing (at most 3 in flight each), the hold with its plan requests, the 62 closed reasons, tier validation; **PR P** the `/sc:issue --plan` mode with `--remaining`, after D and before B; **PR B** the orchestrator skill and command as ONE pull request: all ten waves, refs, four templates, the playbook, the verbs, `limits.py`, `names.py`, the "Orchestrated issue flow" section of WORKER-CONTRACT (opened after A and P merge and the local end-to-end tests pass); **PR C** moving `agent-work-report` into IronClaude; **PR E** real fixtures, the live-test record and the rewritten runbook. Outside IronClaude: the orchestrator repo, moving the spec and work report state into it, keeping the IronFlow copy updated. **Issue #668** (the closeout skill) is its own issue and a dependency of wave 8. Check: each PR passes the regression gate on its own and leaves `enabled: false`.
4. **Build.** `/sc:implement` once per PR. Check: each run's ledger shows per-task QA passed.
5. **Regression gate**, per PR: `make test`, `make lint`, `uv run ruff format --check src/ tests/`, `make verify-deps`, `make sync-dev` then `make verify-sync`.
6. **Open each PR** with `/sc:pr-submit --monitor 3 --head <branch>`. Check: Augment and Codex findings of Medium severity or higher are fixed, CI is green, and a PR that touches a gate or validator file carries the "## Generator-Constraint Considered" section. For this build no PR is merged by the orchestrator session or a worker: each stops at green for the owner's QA.
7. **Live test** (owner-run): real `gh` and Orca, throwaway issues that are only assigned. Check: every `_assumed_shape` fixture is replaced by captured output (or has a written reason), `uv run pytest tests/issue_watch/` passes, the record is committed.
8. **Shadow run:** 24 hours in dry-run mode, then the audit log, the two-process lock test and the restart test. Check: every cycle ends with exit 0 or an understood reason, the second process exits 75, the state folder survives a restart.
9. **Switch on:** create the Orca automation, set `enabled: true`, watch the first real cycles. Check: `status` reports a healthy last cycle, one real assigned issue is claimed once and started once, and the 7-day review (FU-10) is scheduled. Close #450 as replaced by this issue.

### 13. What runs in parallel

| Piece | Starts | Waits for |
|---|---|---|
| The spec | done, approved (ruling 37) | nothing; the rows below start after it |
| #651 (issue templates) | now | nothing |
| The orchestrator repo, moving the spec and work report state into it | in parallel with everything | nothing to start; B's local end-to-end tests and PR C need the repo |
| PR D: retire the old approval gate | first | nothing |
| PR A: the poll core | in parallel with D; merges after D | PR D merged; the spec fixes the wake format A and B build against |
| PR P: the `/sc:issue` plan mode | in parallel with A | PR D merged |
| PR B: the orchestrator skill (one PR) | in parallel with A | PR A and PR P merged before its PR is opened (its tests fake the plan call); T1 to T13 pass; the orchestrator repo; #651 at run time only |
| Issue #668 (the closeout skill), not a 655 piece | built in parallel with A and B | its PR merged before the live test; wave 8 does not wait (PR B's tests use a fake closeout) |
| PR C: moving `agent-work-report` into IronClaude | in parallel with A and B | the orchestrator repo, so the daily run keeps working |
| Live test (owner-run), then PR E | after A, B, P and the repo | A, B, P, the repo, #668 merged; #442's launch checks before any governed worker on a real issue |
| Shadow run, then switch-on | last, in that order | the live test and PR E; for the switch-on also PR C, PR D and #651 |

### 14. Testing and design questions for the orchestrator skill

The skill is one pull request and deep work, so it is tested locally, end to end, before its PR is opened: throwaway issues and pull requests in more than one repo across both GitHub orgs the work report covers (IronbellyOrg and IronbellyGroup), with the results in the PR description (spec 9.2).

| Local end-to-end test | What it proves |
|---|---|
| T1 Throwaway issues in two repos, one per org | The poll finds issues across orgs, the origin check runs per repo, each worker starts in its own repo's worktree |
| T2 Which user it polls for | An issue assigned to the user's own login is picked up; one assigned to someone else, or co-assigned, is not |
| T3 An issue for a repo with no local checkout | Never started in the wrong repo: the checkout is set up (FR-8, `orca project setup-clone`) or the case is escalated |
| T4 Two orchestrators or two users see the same issue | Only one claims it (one routing, the assignee check, the "Claimed by" marker, the lease, the dispatch record) |
| T10 Four issues of one repo, at most 3 in flight each | Three go to orchestrator 1, the fourth starts 2; none is claimed twice; a killed one is restarted |
| T5 Restart in the middle of each wave | The Run resumes (`run-use`) with no second claim and no second `worker-start` |
| T6 A worker that dies, stalls or asks | The FR-9 states, the check-in and playbook, `ask` then `reply`, and rows 7 and 9 behave as written |
| T7 An issue with no plan | The plan call appends the three sections with the plan marker; one it cannot fill escalates, body unchanged |
| T8 PR watch and merge on a real throwaway PR | Each merge condition holds back the merge when it fails (failing check, unfinished review, open thread, no `worker_done`, moved head); a clean PR merges |
| T9 The report entry from claim to close | Added at claim, updated at milestones only, shows the assignee and session link, leaves the report at close |
| **T11 The hold lifecycle** | Ten issues: a complete one is woken at once with no label; an incomplete one gets `hold:plan` and no comment, a plan request only after one hour with no change, the plan record first and the acknowledgment second, three kill windows lose nothing, `plan_stuck` after 60 minutes, a hold removed by hand is not put back, `hold:backlog` does nothing, a full orchestrator gets no plan request |
| **T12 The closeout and the hand-back** | Wave 8 after a merge by the orchestrator, by a person while the worker still runs (the hand-back waits for `worker_done`), squash-merged, closed unmerged; `Fixes` (`already_closed`) and `Refs`; a not-done issue handed back and finished in a second round; the cap, the no-progress stop, a failed re-plan, a tracked change in the worktree; kills inside a hand-back |
| **T13 The audit and the merge-safety hold** | The eight checks on throwaway pull requests; a workflow file change is held until Clay's OK for that head, a rename out of a protected path is held, an unreadable file list is a hold, never "no match" |

Design questions: the 13 questions this issue listed (which login, routing, no double claim, a repo with no checkout, restart state, the plan write grant, the #442 gate, the merge method, the cadence, the wake format, how the report is served, information items, several orchestrators) are answered in spec 2.1; what remains open are the spec's UNVERIFIED items (section 12).

## Acceptance Criteria

- [ ] An Orca automation runs the poll script every 5 minutes (configurable) and no cron entry exists. With nothing new a cycle starts no agent and spends no model tokens; with new items one wake per orchestrator carries its share. The closed reason table has exactly 62 names.
- [ ] One orchestrator per repo and at most `max_in_flight` (default 3, in `repos.yaml`) issues in flight for each (an open plan request counts); the poll routes each issue, under its lock, to an orchestrator with a free place or starts another; each wake is addressed to one orchestrator, which refuses any other; an idle one ends and a dead one is restarted.
- [ ] The skill `orchestrator` and the command `/sc:orchestrator` exist in IronClaude in the structure of `sc-issue-protocol`, `sc-pr-submit-protocol` and `sc-troubleshoot-protocol`; `SKILL.md` lists waves 0 to 9 with ref, commands, template and ending check. The skill lands as one pull request after T1 to T13 pass, with their results in its description.
- [ ] The orchestrator runs `/sc:issue --claim` at `--pipeline none` and starts each worker with `worker-start` in a worktree of the issue's own repo, never through the claim's launch levels; each issue is claimed once and its worker started once.
- [ ] **Hold and plan (A):** an assigned issue that fails the plan check gets `hold:plan` (label only, no comment) and is not sent on; `hold:backlog` makes the system do nothing; a hold removed by hand is not put back; after one hour with no change the poll sends ONE plan request; a plan is created only through `/sc:issue --plan` (PR P, with `--remaining`), the plan record written before the acknowledgment; wave 1 re-reads the issue live.
- [ ] The four template files exist, each with a test and used by each step that writes or sends; the handoff has its nine sections in order with the `Fixes` or `Refs` rule; the escalation template holds the nine rows. The skill loads Orca's own `orchestration` skill at run time; each wave names its Orca commands.
- [ ] The report entry follows the item template: added at claim, updated at milestones only, removed at close; it shows the human assignee, the orchestrator and worker as links (or "no live session" with the reason), an FR-9 state and the last update; escalations are lines of the issue's own entry. The daily run no longer touches issue entries (test).
- [ ] The worker status check is hourly by default (only the interval is configurable), runs for each running worker Monday to Friday, 24 hours a day, and stops at its `worker_done`. There is no session-manager skill: the orchestrator does every check-in itself, typing and approvals included, under FR-23 and FR-24 (refused on unsent typing or fresh output, except the one interrupt; "always allow" never sent; tests).
- [ ] The worker pushes its own branch and opens its pull request, never merges, never force-pushes. Only the orchestrator merges, and only when every check is green on the final head, every listed review agent has finished, no thread is open, no review is at "changes requested" and the worker has sent `worker_done`; never over a failing check without the human's explicit OK; a merge-safety file change waits for Clay's OK for that head; a review agent that does not run holds the pull request.
- [ ] **What reaches Clay (B):** the nine-row table decides; `escalate` refuses an entry that names no row; the rules are on from the start; an unanswered question waits; `answer-check` runs before any answer is acted on, typed answers only; a release tag or publish needs a recorded human OK; deleting a skill or an agent needs the issue to name it, ordinary files may be deleted; a scope change escalates only when it creeps into peripheral features; a question only after the issue, code, docs and a web search.
- [ ] **Limits (C):** every line of the "may never" list has a test and passes through `refuse`; the one interrupt is sent only after its escalation is written.
- [ ] **Closeout and hand-back (D):** wave 8 calls `/sc:closeout`, which decides by the issue's own criteria and closes only a done issue; the orchestrator runs no `gh issue close`; #668 is merged before the live test; a not-done issue is handed back (old worker final, re-plan through `--remaining`, new worker on a new branch) at most 3 times, stops when nothing progressed, every stop is row 9.
- [ ] **Audit and merge safety (E):** the audit runs eight checks with no model and no GitHub write; AU4a, AU4c and AU5 reach Clay; `changes_requested` is never merged; an unreadable file list is a hold.
- [ ] All skills live in IronClaude; the coordinator spec and work report state live in the orchestrator repo; the IronFlow copy is kept updated (FR-13, FR-1, FR-2, FR-19, rows C25 to C29).
- [ ] No trigger label, approval label, approver list, Project or Backlog read, or plan-approval gate remains, except where the spec records a reason; the safety features of section 11 still hold and have tests.
- [ ] The live test, shadow run, lock test and restart test pass before `enabled: true`; #442's checks pass before the first worker on a real issue. #450 is closed as replaced.

## Out of Scope

- Creating issues and the Priority, Fix approach and Test plan sections themselves (#651).
- The general orchestrator for all sessions of #339.
- A separate merge agent, a listener, a webhook, a GitHub Action or a hosted service (a pull poller stays; Coder#477 stays unneeded unless its revisit condition returns).
- The closeout skill itself: it is issue #668, with its own spec and pull request; this issue only calls it.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/cli/issue_watch/` (8 modules, about 4,800 lines; `github.py:37` has the `REPO` literal, `launch.py:50` `ORIGIN_REPO`): reshaped; new `wake.py`, `repos.py`, `route.py` and `hold.py`. `src/superclaude/cli/issue_pipeline/` (8 modules): removed (PR D), with WC-17 and "Issue pipeline duties" of `core/WORKER-CONTRACT.md` (which gains an "Orchestrated issue flow" section) and guard G2 rule 1 of `hooks/scripts/launch-level-guard.sh`.
- `docs/designs/issue-watcher*.md`, `issue-pipeline*.md`, `sc-issue-claim-pipeline-flag.md`; `tests/issue_watch/`, `tests/issue_pipeline/`, `tests/hooks/`.
- Used as they are: the claim flow (`sc-issue-protocol`, `scripts/orca_worktree.py`), the installed `orca` commands, `src/superclaude/pr_submit/` and `sc-pr-submit-protocol`. Changed: `/sc:issue` (`commands/issue.md`, `SKILL.md`, new `refs/plan.md`, two test files: PR P).
- Moves: `.claude/skills/agent-work-report/` from IronFlow into IronClaude (PR C); the coordinator spec and `.dev/coordinator/` to the orchestrator repo. New: `commands/orchestrator.md`, `skills/sc-orchestrator-protocol/`, `cli/orchestrator/` (verbs, `limits.py`, `names.py`), the poll script and its setup.

## Related Issues/PRs

- Replaces #450; closes the open parts of #331; depends on #651 and on #668 (the closeout skill); relates to #339; gated by #442. PRs #447, #448, #485, #548, #584 and #591 are in the history comment. Same area, not read in full: #423 and #444 (it mentions a proposed `/sc:orchestrator` command, which the spec reconciles). Follow-up lists of review findings: #665, #674, #675.
- Spec: `docs/designs/orchestrator.md` on branch `clayphi/issue-655-spec`; coordinator spec `SPEC-AGENT-WORK-COORDINATOR-20261027.md` (IronFlow, moving to the orchestrator repo). Reference only: https://simple-with-us.github.io/AI-Fleet-Coordinator/.

## Success Metrics

- Assignment to a started worker takes at most one poll interval plus the claim time, with no human step, for an issue that has a plan.
- Idle cycles start no agent: zero model tokens between assignments.
- Zero duplicate starts for one issue over the shadow run and the first 7 days live (7-day review, FU-10).

## Architecture Impact

- The separate watcher session disappears. The poll becomes a script run by an Orca automation and decisions (claim, plan, handoff, watch, merge, closeout, audit) move into the orchestrator. The poll gains its first GitHub write, the label `hold:plan` (grant `issue.hold`).
- The poll is repo-aware; the repo list and map live in the orchestrator repo; the origin check runs per repo, so a fork's upstream is never touched.
- The handoff prompt is filled from a template and passed as the task spec of `worker-start`. Plan writes go through `/sc:issue --plan`, under the grant `issue.body.append_plan_sections` (a `grants` list in `repos.yaml`; changing `grants`, `reach_daily_max` or `merge_safety_files` needs Clay's recorded word). All skills live in IronClaude; everything kept while running, in the orchestrator repo.

## Dependencies

- #651 for the plan format; #668 for the closeout (before the live test); #442's live checks before any governed worker launch on a real issue.
- Orca with the `automations`, `orchestration`, `reference` and `worktree` commands.
- Today in the IronFlow repo (read access needed): the work-report waker pattern, the daily work report skill and Clay's coordinator spec; moving them and updating the IronFlow copy: FR-13 lists merges and closing issues as human-only; FR-1 places the skills in IronFlow; FR-2 and FR-19 describe a daily run that rebuilds every item; FR-10, FR-23 and the proof table carry the interrupt exception.
- The private orchestrator repo `IronbellyOrg/IronOrchestrator` with `repos.yaml`, the map and the overviews; a `gh` login that can read those repositories.

## Testing Strategy

See the Test plan below. The existing mocked tests keep passing; new mocked tests cover the rules, waves, templates, merge conditions, escalation table and limits; the live test replaces the guessed fixtures; the shadow run, lock test and restart test gate the switch-on.

## Documentation Needs

- The design doc `docs/designs/orchestrator.md` (it replaces `docs/designs/issue-watcher.md` as the source of truth), a rewritten owner runbook (labels, approvers and cron removed; Orca automation and a pointer to the orchestrator repo added), the live-test record, and WORKER-CONTRACT.md with the retired `issue-pipeline` parts marked retired.
- The coordinator spec moved to the orchestrator repo and updated (FR-13, FR-1, FR-2, FR-19 and the interrupt rows), with the IronFlow copy kept in sync.

## Alternatives Considered

Rejected by Clay: a separate watcher session plus the orchestrator; cron or a hosted listener; the approval label and Backlog column as optional extras; a separate session-manager skill; the closeout inside this issue (it is #668). Reasons are in the history comment.

## Impact Analysis (Blast Radius, Integration Impact)

- Blast Radius: the poll and start path of every workspace that enables it; one bad cycle could start many workers, and the orchestrator can merge pull requests, close issues (through the closeout), restart a hand-back round and interrupt a worker in one case. The caps stay: one claim and one worker start per issue, a day cap, a call budget, a lock, a dry-run mode, a bound on hand-backs.
- Integration Impact: `issue-watch` and `issue-pipeline` CLI verbs, the claim flow, `/sc:issue` (a new mode), WORKER-CONTRACT.md, the launch-level guard and its tests, the runbook, the work report skill in IronFlow, issue #668.

## Risks & Mitigation

The spec keeps 28 risks (K1 to K28; K22 to K28 are new) and UNVERIFIED items U1 to U60 (U35 withdrawn), each with its check (spec sections 11 and 12). The main ones:

- Assignment by anyone with triage or write access starts a worker. Mitigation: the intended gate; the launch prompt stays integer-only; the day cap and one claim and one worker start per issue stay. Issue text reaches the worker through the handoff prompt, which quotes it as data.
- Multi-repo work widens the origin check. Mitigation: the repo list comes from the orchestrator repo; the check runs per repository.
- The claim's launch levels and `worker-start` could be mixed. Mitigation: a test fails if the skill launches through the claim's launch levels.
- This issue and the IronFlow coordinator spec could drift. Mitigation: one design, FRs cited by number, copies kept in sync.
- The orchestrator skill is one large pull request (Clay). Mitigation: local end-to-end tests first, and the regression gate.
- The orchestrator can merge, close and restart work. Mitigation: the merge conditions, no merge over a failing check or a `changes_requested` review, the merge-safety hold, every `gh` call pinned to the issue's repo, the "may never" list with `refuse`, the closeout deciding done-ness. The list binds the verbs, not a command the model types itself (K22): `refuse` in every verb, a text scan, a stated limit (U42).
- The hold delays an unfilled issue by an hour plus a few cycles (K24); an unanswered question stops its issue until Clay answers (K25). Both intended; only that issue waits.
- A plan or closeout call is a Skill call from inside a wave, itself UNVERIFIED (K17, K27, U2, U55).
- The hand-back loop costs a worker, a plan update and a merge each round, and a wrongly written `Fixes` still closes the issue at merge (K28). Mitigation: at most 3 hand-backs, a stop when nothing progressed, every stop is row 9.
- The orchestrator repo does not exist in full yet. Mitigation: the spec defines its minimum format and keeper.
- Removing the approval gate removes code that guard G2 relies on. Mitigation: the spec lists each G2 rule and keeps any the guard still needs. Unknown GitHub error text is a login failure until the live test.
- Workers run with no launch-level guard and IronClaude `master` is not protected, so only the worker's prompt holds it back. A recorded risk.
- A wrong count of orchestrator sessions could exceed 3 in flight or leave issues unattended. Mitigation: the count comes from the state files and the poll's own entries; a dead orchestrator is restarted.

## Effort Estimate (hours) and Complexity

- Effort Estimate (hours): about 124 hours of agent and owner work before the additions (spec and review 16, plan 3, the poll PR 17, the orchestrator skill PR 64 including its local end-to-end tests, the skill move and gate retirement 10, live test 5, shadow-run review and switch-on 8, orchestrator repo and spec move 1), plus the 24-hour shadow run. Additions A to E add work to PR A, PR B and PR P and are not re-estimated here: an estimate, not a measurement.
- Complexity: complex. It reshapes a built package, retires another, builds the orchestrator, adds multi-repo support and crosses three repositories.

## Priority

High: #450 is blocked and the coordinator handoff cannot run until this lands; until then every assigned issue is started by hand (#651's rule: High = other work is blocked).

## Fix approach

Repo: `IronbellyOrg/IronClaude`. Base branch: `master`. One feature branch per PR, from `origin/master`; every PR is opened only through `/sc:pr-submit --monitor 3 --head <branch>`.

Commands, in order: `/sc:design` (spec, done and approved), `/sc:workflow` (plan and PR split), then PR D, PR A, PR P, PR B, PR C and PR E (spec 8.2), each with `/sc:implement` and `/sc:pr-submit --monitor 3`; issue #668 is built on its own track. Then the owner-run live test, the shadow run and the switch-on. Steps and checks: section 12; files: Components Affected.

## Test plan

Tests to add or change (spec 9.1 has a row per piece):

- `tests/issue_watch/`: assignment-only discovery, the new-since-last-poll rule, the repo list and map, the per-repo origin check, backoff, the single retry, "nothing new means no wake"; the hold: one test per case of `plan_check` and per row of the decision table, label only, a hold removed by hand never put back, the quiet clock, one plan request per hold sent only to an orchestrator with a free place, `plan_stuck`, exactly 62 closed reasons. Remove the tests of the label, approval, Project and approver rules; keep the property test that only a validated integer reaches the launch prompt; replace `_assumed_shape` fixtures after the live test.
- `tests/issue_pipeline/` and `tests/hooks/`: remove or rewrite the tests of the approval gate and the retired G2 rules.
- `/sc:issue` (PR P): the three failure forms of a plan section, bytes outside the sections written unchanged, one marked write and no comment, each STOP code, `--remaining` (round file, done items kept, marker for a rerun).
- Skill structure (style of `tests/skills/test_issue_protocol.py`): thin command; `SKILL.md` frontmatter, Will Do and Will Not Do, error table, waves 0 to 9; the file table both ways; no `src/superclaude/` path to another primitive; Orca's skill loaded at run time. Each template has its own test (sections in order, placeholders filled, a mutation case); the handoff has its nine sections, quoted issue text and both `Fixes` and `Refs`.
- With fakes: several orchestrators (4 issues give 3 and 1; a wake for another orchestrator is refused), typing and approvals (refused on unsent typing; never "always allow"), Orca orchestration (one `run-create`, one Task and one `worker-start` per issue, each mailbox message handled once, a gate per escalation), the work report (entry at claim, at milestones only, removed at close).
- Merge and close, with fake `gh` and Orca: one failing case for each merge condition, `changes_requested` refused even with a recorded OK, the merge-safety hold (rename out of a protected path, unreadable list, OK tied to the head), the repo's merge method, every `gh` call pinned to the repo, no second copy of the `pr_submit` logic.
- What reaches Clay and the limits: the nine-row table parsed, `escalate` refuses no row, a question without an answer never continues, `answer-check` refuses relayed, old and wrong-question answers; `refuse` has a failing case for every "may never" pattern and a passing one for each ordinary command; the interrupt after its escalation only.
- Closeout, hand-back and audit: wave 8 order (closeout, audit, entry), the `handback` verb (cap, no progress, nothing remaining, idempotent), waiting for a final old worker, the tracked-only worktree guard, the eight audit checks on canned replies.
- Checks: each check of section 8 has its trigger and cadence in configuration; the worker check ends at `worker_done`. Local end-to-end tests T1 to T13 (section 14) run before the skill's PR.

Regression gate (every PR): step 5 of section 12.

How a reviewer verifies: `grep -rn "issue-watch:trigger\|approvers_file\|project_id" src/superclaude/cli` finds nothing except where the spec records a reason; `orca automations list` shows the 5-minute automation and `crontab -l` no issue-watch entry; the shadow run's audit log shows no starts, only decisions (`would_wake` for an assigned test issue); one assigned throwaway issue gives one "Claimed by" comment and one worker session within one poll interval, and with nothing assigned no agent starts (`orca automations runs`).

<!-- sc:issue:create template=issue-feature-complex -->

