# B. Open and recently closed issues vs PR #686 (lens: issues)

Read-only. Sources: `gh issue view` on IronbellyOrg/IronClaude (and IronbellyOrg/Coder 515, 516, 477), plus `git grep` on `origin/pr-686`.

## Summary

1. PR #686 is not new work. It is "PR A" of issue #655, named in the #655 body ("PR A the poll core: assignment-only discovery, the repo list and map, ... routing (at most 3 in flight each), the hold with its plan requests, the 62 closed reasons, tier validation"). It builds on the built watcher (#331, PRs #447 and #448) that #450 wanted to roll out.
2. Its parents are #655 (open, clayphi) and the spec `docs/designs/orchestrator.md` (landed by PR #681). It also owes work to the follow-up lists #665 (21 Medium findings) and #675 (54+ findings); those stay open and are not closed by it.
3. #450 (open, "roll out the issue watcher") is superseded: #655 says "Replaces #450" and build step 9 says "Close #450 as replaced by this issue". PR #686 deletes the trigger label, approval and project reads that #450's live test and cron would have switched on. #450 is still open on GitHub.
4. No open issue other than #655 asks for an orchestrator registry, a wake file or a `hold:plan` label. #339's accuracy check only records that "no flag or registry marks a session as the orchestrator". #409 item 9 asks whether the observer should show watcher state; it is open and unbuilt, and PR #686 does not touch `observe`.
5. Real tensions: Coder #515 (cron) and Coder #516 (a `Coordinator` worktree and `COORD-<repo>` session per project) were written for the old design and say "coordinator"; #655 uses an Orca automation and says "orchestrator". Open #689 renames `## Fix approach` to `## Approach`, but `hold.py` in PR #686 accepts only `## Fix approach`.
6. Siblings: PR #690 (PR P, `/sc:issue --plan`) is open; PR D (#682), PR C (#684) and the closeout (#683, issue #668) are merged. PR B (the orchestrator skill) and PR E did not appear in the 25 most recent PRs (UNVERIFIED beyond that list).

## Table

Relation codes: (a) #686 implements it, (b) parent or spec, (c) duplicates, (d) overlaps, different layer, (e) complements, (f) conflicts, (g) unrelated.

| issue | state | author | what it wants | relation to #686 | evidence quote |
|---|---|---|---|---|---|
| #655 | open | clayphi | Issue-polling orchestrator: poll assigned issues, hold ones without a plan, claim, start worker, merge, closeout, audit | (b) parent. #686 implements the PR A slice only | "PR A the poll core: ... the hold with its plan requests, the 62 closed reasons, tier validation" |
| #665 | open | clayphi | Handle 21 Medium review findings of the #655 spec through the plan | (e) follow-up list. M1, M3, M4 (filtered issues, reason table, `origin_mismatch`) land in PR A code; not closed by it | "M1. What happens to an assigned issue that is filtered out ... is undefined" |
| #675 | open | clayphi | Handle 54+ review findings of additions A to E (hold, plan request, wake) | (e) follow-up list. F1 to F5 are about the hold decision table and `plan_requests[]`, which #686 builds | "F1. The decision table of the hold has no row for an issue that passes the check, has no label and still has a `held` entry" |
| #450 | open | ironbelly | Roll out watcher: live test, 24 h shadow run, cron | (f) superseded. #686 removes what #450 would have enabled; cron was dropped | "Replaces #450" (#655); "Dropped on purpose: ... cron (FU-2)" |
| #331 | closed 11-08 | ironbelly | Automated issue watcher and routing service | (b) ancestor. #686 rewrites its code (claim launch, approval, board reads removed) | "starts one Orca claim session (`/sc:issue --claim N`)" is what #686 deletes |
| #668 | closed 11-20 | clayphi | `/sc:closeout` skill for merged PRs | (e) complements; called by PR B wave 8, not by #686 | "The orchestrator of issue #655 calls it in wave 8" |
| #651 | closed 11-19 | clayphi | Priority, Fix approach, Test plan in every create template | (e) feeds #686: its hold check reads those headings | "front-load planning into the issue at filing time" (as #655 cites it) |
| #689 | open | clayphi | `/sc:issue` plans at create; third mode; rename `## Fix approach` to `## Approach` | (f) coupling risk. `hold.py` line 64 has only `("fix_approach", "## Fix approach")` | "`plan-check` ... must accept both headings until existing issues are migrated" |
| #687 | open | clayphi | Daily cleanup of merged worktrees | (g) unrelated, but states the orchestrator never removes worktrees | "This cleanup is never run by the orchestrator" |
| #339 | open | ironbelly | Orchestrator mode: one session manages all sessions of a worktree; sweep, close | (d) parent theme; Phase 1 sweep built. #686 is a different layer (intake and routing) | "no flag or registry marks a session as the orchestrator" (accuracy check) |
| #534 | open | ironbelly | Follow-ups of #339 Phase 1 (read-only sweep) | (g) sweep internals. `_sweep` in `cycle.py` is the poll's own state sweep, not the Orca sweep | "Owner-ruled limitations of Phase 1" |
| #590 | open | ironbelly | Sweep classified 1 of 264 sessions; show cap 50 | (g) | "could classify only 1" |
| #547 | closed 11-14 | ironbelly | sweep `git status` can run repo-configured programs | (g) | "git can run programs named in repository configuration" |
| #409 | open | ironbelly | TUI observer for humans (`superclaude observe`); item 9: show watcher state? | (d)/(e) different layer. Item 9 is open, with no source yet; #686's registry and wake files could become one. #686 does not touch `observe` | "Showing watcher or coordinator state (item 9) is still open and needs a source other than `worker-list`" |
| #606 | closed 11-20 | ironbelly | Observer visual parity with mockups (PR #673 merged) | (g) | observer rendering only |
| #604 | open | ironbelly | Observer R4 remote fleet, backlog | (g) | "Nothing has been built for this" |
| #423 | open | ironbelly | Orchestrator v2: catalogue of what all agents do, cross-agent review | (d) later, different layer; a knowledge catalogue, not a routing registry | "separate future release after the v1 orchestrator (#339)" |
| #431 | closed 11-17 | ironbelly | Orchestrator waits on quiet workers; weak alive checks | (e) rules merged (#434), monitor work moved to #423. #686's ack and retry (3 tries, `ack_not_observed`) is the same concern for wakes | "Monitor work continues under #423" |
| #444 | open | ironbelly | Evaluate sub-orchestrator / `--sub` | (d) possible later conflict: #686 allows several orchestrators per repo, #444 asks about nested ones | "Assess the implications for ... WC-13's worker fan-out restriction" |
| #468 | open | ironbelly | Orchestration check spam from mailbox heartbeats | (e) risk: #686 delivers wakes by mailbox | "You have 1 orchestration message. Run `orca orchestration check`" |
| #507 | closed 11-11 | ironbelly | Coordinators use `--unattended` on worker Command lines | (e) background; #686's new-session delivery should follow it (UNVERIFIED) | names "issue-watch, claim-launched agents" as headless callers |
| #442 | open | ironbelly | Live observations for the launch-level guard | (e) gate: #655 says "gated by #442" before any governed worker; not a #686 blocker | "needs a real Claude Code session and was never run" |
| #678 | open | ironbelly | Guard misses bare `claude <prompt>` | (g) | OB-H1 item 8 |
| #394 | closed 11-17 | ironbelly | Hook enforcing launch level of claim-launched agents | (e) background; the claim launch it governs is removed from the watcher by #686 | "launch level of claim-launched agents" |
| #546 | open | ironbelly | Hook that rejects a launch whose model breaks the policy | (d) different layer: #686 validates tier names in `repos.yaml`; #546 enforces which model may run | "A machine-readable model policy exists ... and is loaded by a hook" |
| #551 | closed 11-17 | ironbelly | Model-policy hook v1 design decisions | (g) follow-up to #546 | design restrictions list |
| #462 | closed 11-17 | ironbelly | Orchestrator-spawned sessions default to Opus | (e) background for tier choice; #686 defaults `worker_tier` to tier2 | "honor the user default model" |
| #384 | closed 11-05 | ironbelly | Primitives use ccsession aliases | (e) #686's tier names follow it (UNVERIFIED, title only) | title only |
| #552 | open | ironbelly | Blocker classifier, fewer review blockers | (g) (PR #688 is its own work) | "Loosen what review gates classify as blocking" |
| #574, #575, #576, #580 | closed | ironbelly | Jev compaction, pruner, local inference node | (g) | evaluations rejected, unrelated |
| Coder #515 | open | ironbelly | cron in the workspace image so the watcher runs on a timer | (f) conflicts: #655 uses an Orca automation, no cron | "Orca's own scheduled automations start an agent session ... not a fit" against #655 "reuses the work-report waker pattern" |
| Coder #516 | open | ironbelly | Every project has a `Coordinator` branch, worktree and `COORD-<repo>` session, restarted when stopped | (d) overlaps: #686 records "an orchestrator must be started" and has a new-session delivery. Two ways of asking who creates the per-repo coordinator | "The watcher's claim sessions start in that same worktree" (stale: #686 removes the claim session) |
| Coder #477 | open | ironbelly | Listener and secure prompt routing per workspace | (g) #655 says it "stays unneeded" | "Coder#477 stays unneeded unless its revisit condition returns" |

## Direct answers to the pointed questions

- **Orchestrator or coordinator registry.** Only #655, and so PR #686 (`.orchestrator/orchestrators.json`), asks for one. #339's accuracy check says none exists. Coder #516 asks for a per-project coordinator session but not a registry. I found no second open issue asking for the same registry.
- **Wake mechanism.** Only #655 (wake file plus mailbox, typed line or new session). Coder #477 asked for a listener that routes prompts to the project orchestrator; #655 rejects it. So two issues asked for "reach the project orchestrator" in two ways, and #655 chose the wake file.
- **`hold:plan` label.** Only #655 (addition A) and #675 F1 to F5. #689 depends on the same plan headings. No other issue.
- **Observer or TUI showing orchestrators.** #409 item 9 only, still open and unresolved. #606 (merged as PR #673) did not cover it.
- **Same thing asked two ways.** (1) Timer: #450 and Coder #515 (cron) against #655 (Orca automation). (2) Per-project coordinator: Coder #516 (`COORD-<repo>`, restarted at boot) against #655 (the poll starts an orchestrator when none has room). (3) Terminology: "coordinator" in Coder #516 and #409 against "orchestrator" in #655, #339 and #444.

## Caveats

- Not read in full: #394, #606, #574, #575 (very long), #322; I used leads and keyword searches. #384, #507, #331 bodies were only grepped or skimmed.
- The #655 body is 64 KB; I read the PR split, models, related-issues sections and the first lines of its comments, not every ruling.
- Whether PR B and PR E exist was taken from `gh pr list` (25 most recent), not searched further.
