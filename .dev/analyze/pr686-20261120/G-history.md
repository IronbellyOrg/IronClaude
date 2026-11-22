# G-history: events that led to PR #686, PR #681 and issue #655

All times UTC. `ironbelly` is a login shared by the owner and every session on this host (owner-answers, 2026-11-14 tenth batch), so a GitHub action by it does not show which person acted. #655 comments 12 and 14 say "applied by the orchestrator session" but post as `clayphi`.

## Summary

1. Two lines of work ran at the same time on the same package, `src/superclaude/cli/issue_watch/`. The owner line: #331, #447/#448, #450, #584/#591, then a local zero-setup plan (cron, approval label, Project Status). The Clay line: a comment on #450 on 2026-11-18 17:00, then #651, #655, spec PR #681 and PRs #682 to #690.
2. The one recorded contact is Clay's #450 comment (17:00:32, to `@ironbelly`, eight points, ends "What do you think?"). I found no reply, reaction, review or comment by `ironbelly` after it on #450, #655, #651, #668, #665, #675 or PRs #681 to #690.
3. In #655 and `docs/designs/orchestrator.md`, "the owner" means Clay ("approved by the owner (Clay)"). Rulings 1 to 39 are Clay's, kept in `RULINGS.md` of the orchestrator session (unread: UNVERIFIED). No source shows `ironbelly` giving a ruling.
4. The same day the owner line recorded the opposite on four points: cron, the approval label plus Status gate, "coordinator" not "orchestrator", one `COORD-<Repo>` per project. They sit in an unpushed local file, memory files and Coder #515/#516; #655 cites none of them.
5. #655 cites #331, #450, #447, #448, #485, #548, #584, #591, #339, #423, #444, #442. It does not cite #409, #431, #539, #587 to #589, #613, #636, Coder 515/516 or the zero-setup plan. PRs #681 to #690 cite none of #331, #450, #584, #591.
6. A duplicate search exists only at `/sc:issue --create` (lists, never stops); no claim-time or template check exists; no sign it ran for #655. #290 (rules for proposing new skills) is open, assigned to Clay.

## Timeline

| Date and hour | Who | What | Source |
|---|---|---|---|
| 10-23 18:05 | clayphi | Files #289, #290 (rules for worktrees; for proposing primitives) | gh |
| 10-27 | Clay (per #655) | `SPEC-AGENT-WORK-COORDINATOR-20261027.md`, IronFlow repo `.dev/specs/`; date from the file name. UNVERIFIED: not on this host | #655 body |
| 10-29 08:31-08:53 | ironbelly | Answers #289/#290: "only file issues until we have an eval framework"; hands #290 to clayphi | #290 |
| 10-30 14:39 | ironbelly | #331 created. Then #339 (11-01), #409 (11-06; `ironbelly` login assigns clayphi 17:37), Coder #477, #423, #431 (11-07) | gh |
| 11-08 04:58 | ironbelly | #444 created; names a proposed `/sc:orchestrator` command | #444 |
| 11-08 06:27-07:32 | ironbelly | #447, #448 merged; #450 created 07:03:49; #331 closed 07:03:52. #485 merged 11-10 06:10 | gh |
| 11-11 14:47 | clayphi | Comment on #409 (reply to a ClickUp DM): the only other Clay comment on these issues before 11-18 | #409 |
| 11-14 17:41-17:42 | ironbelly | #539 (sweep), #548 (option 3) merged. Q35 "B1b": watcher claims `--pipeline none`, a coordinator starts the worker | owner-answers |
| 11-17 04:00 / 17:28 | ironbelly | #584 (Plan A), #591 (Plan B) merged; #587 06:04; status reviews 07:09 (#450 BLOCKED) | gh |
| 11-18 17:00:32 | clayphi | Comment on #450 to `@ironbelly`: no trigger or approval label, no Backlog, orchestrator polls and claims, Orca automation not cron, plan first, one issue replaces #331/#450/handoff | #450 comment 3 |
| 11-18 17:09-17:14 | owner line | Local debate files (single or per-project watcher). Requirements rows say "Owner 2026-11-18": label plus Status gate (R19, R22), "coordinator, not orchestrator" (R10) | `requirements.md` |
| 11-18 18:25:35 | clayphi | #651 filed; says "#450 ... same area, explicitly out of scope" and "No duplicate found" | #651 |
| 11-18 18:26:56 / 18:40:16 | ironbelly | Coder #515 (install cron), #516 (one coordinator per project); decisions posted 18:45. Chat: "Yes take on those duties" (WC-17) | Coder; memory |
| 11-18 19:55:24 | clayphi | #655 filed "replaces #450" (cross-reference on #450 and #331 at 19:55:25). Nine "body updated" comments 20:00-21:22; history comment 20:57; self-assigned 21:24; accuracy check (35 claims vs code) and claim 21:32:41 | #655 |
| 11-18 23:35 to 11-19 14:39 | owner line | Plan folders `TASK-WF-requirements-` `20261118-233559`, `20261119-010910`, `-012839`, `-140750` (review), `-143917` (superseded) | local |
| 11-19 01:25 to 21:15 | Clay | Rulings 3 (01:25), 12 tiers (03:09), 23 to 35 (13:16-13:34), 36 (20:59), 38 (21:15, "GeneralIronFlow's clarification of ruling 26") | spec section 10 |
| 11-19 15:29-15:32 | owner line | Commit "R1-R34 and plan v5"; `/sc:implement` ledger starts for `...143917-2`; T1 to T25 edit `issue_watch/` (predicates, github, cycle, cli, dispatch). Branch `ironbelly/issue-watcher-zero-setup-plan`: no PR, not on remote | `progress.md`, gh |
| 11-19 22:19-23:31 | clayphi | #655 body synced "approved by Clay ... (ruling 37)"; PRs #681 to #684 opened | #655, gh |
| 11-20 00:02:33 / :36 | clayphi | clayphi merged #681 and #682; #682 deletes `issue_pipeline/` and WC-17, the code of #584/#591 | PR data |
| 11-20 00:25 to 02:01 | clayphi | #686 (PR A), #687, #689, #690 (PR P) opened; #683 merged 01:16, #684 merged 02:01 | gh |
| 11-20 01:50 | owner line | R36 "Yes, withdraw" R31; approval is the `Approved` issue field | `requirements.md` |

Satellites: #665 (11-19 01:23), #668 (03:36), #674, #675 (15:21). The owner-answers record ends at 11-17; later owner decisions are in `requirements.md` and the two memory files. The named `issue-339-orchestrator-mode/...` path does not exist; I read the copy in `blocker-classification-stage3c/`.

Rulings cited in #655 and the spec (2026-11-19): 1 to 12 (living report, no session manager, workers push, one orchestrator per repo, tiers), 19 to 22 (closeout), 23 to 35 (holds, `/sc:issue --plan`, audit), 36 (hand-back), 37 (approval of spec and A to E), 38, 39. Each is Clay's, or a session's for Clay; none is `ironbelly`'s.

## Scheduler decision: cron or Orca automation

| Date and hour | Who | What | Source |
|---|---|---|---|
| 11-08 07:03:49 | ironbelly | #450 "Done when" 3: "FU-2: the cron entry (`0 */5 * * * *`, six fields) is installed" | #450 |
| 11-18, hour not recorded; on disk by 17:09:03 | ironbelly | R6 "Cron is the scheduler (owner decided 2026-11-18)". Findings line 18: Orca automations start "an agent session with a prompt on each run". Position papers dated 17:09:03 and 17:09:05 cite R6 | `requirements.md`, `debate/` |
| 11-18 17:00:32 | clayphi | Point 5: "Use an Orca automation, not cron" | #450 comment 3 |
| 11-18 18:26:56 | ironbelly | Coder #515: "Orca's own scheduled automations start an agent session on each run, so they are not a fit for a plain command"; "Decision already made by the owner: use cron (not systemd, not Orca automations)" | Coder #515 |
| 11-18 20:57:06 | clayphi | First #655 comment naming it: "Cron (FU-2 ...): an Orca automation replaces it"; "rejected (Clay's ruling ...)". The 19:55 body is overwritten: UNVERIFIED | #655 comment 6 |
| 11-19 22:19; 11-20 00:02:33 | clayphi | Body section 10 "An Orca automation runs the schedule, not cron"; spec 1.4 R4 "(Clay, 2026-11-18)", 4.8: precheck "is the pattern of `waker.py` (evidence E130)", merged in #681 | #655, spec |

First: Clay's comment (17:00:32) is the earliest timestamp. The owner's cron decision has no hour; R6 is cited 8m31s later, so the order is UNVERIFIED. Cron as the plan dates from 11-08.

Citations: #655, the #681 body and the spec contain no "515", "516" or "zero-setup". They name cron only as #450's FU-2; the owner's 11-18 decision is not cited. `debate/` covers single versus per-project watcher (R5, R16) and assumes cron ("R6 needs a timer in every workspace and the host has no crontab"); no record debates automation versus cron. The owner's stated reason (an automation starts an agent) is answered only by spec 4.8 and the waker reference; UNVERIFIED that the owner saw it.

## Where the two lines could have met

1. **#450 comment, 11-18 17:00:32.** It mentions `@ironbelly` (mention event 17:00:34), who is #450's assignee. No answer exists on GitHub. #655 later calls it "Clay's 2026-11-18 comment on #450" and rests the removals on "Clay's 2026-11-18 rulings". Whether the owner answered in chat or a DM is UNVERIFIED.
2. **Cross-references.** #651 (18:25:36) and #655 (19:55:25) appear on #450's timeline, #655 on #331's. Whether the owner saw them: UNVERIFIED.
3. **Owner posts after the comment.** Coder #515 and #516 (1h26m and 1h40m later) and `requirements.md` say cron and a label gate were decided. None mentions #651, #655 or the comment.
4. **Assignment.** #655 was self-assigned (21:24) and never assigns or mentions `ironbelly`. #450 stays open, assigned to `ironbelly`.
5. **Clay read the owner's work.** The history comment names #584, #591 and `docs/designs/issue-watcher.md` section 2.1; of #423 and #444 it says "Same area, not read in full".
6. **Names.** #444 (11-08) already proposes `/sc:orchestrator` with `--sub`; the spec gives that name to the poll orchestrator. The owner's R10 and #516 say "coordinator" everywhere.
7. **Same code.** Owner T1 to T25 and #686 both rewrite `issue_watch/`. No cross-reference found; the owner branch is unpushed.
8. **Deleting owner code.** #682 removes the code of #584/#591 and WC-17; its body cites only #655. Owner memory still says the coordinator holds those duties.
9. **A channel existed:** ClickUp DMs (#409, 11-11); content unreadable.

## Process rules that existed

- Repo `CLAUDE.md`: "Confidence-First Implementation: Check confidence BEFORE starting"; "Auggie first". Neither names a search of open issues or PRs.
- `/home/coder/workspaces/IronClaude/src/superclaude/core/HOW-WE-WORK.md` (checked-out branch, near lines 280-284): "When unsure which tool to use, run `/sc:recommend` ... or ask your lead before starting anything large." No duplicate or issue-search rule.
- `CONTRIBUTING.md` "Claiming and filing issues", `.github/ISSUE_TEMPLATE/feature_request.yml` and `PULL_REQUEST_TEMPLATE.md`: no duplicate rule or checkbox. `docs/developer-guide/contributing-code.md` line 410, "Don't duplicate existing functionality", is about code.
- `~/.claude/skills/sc-issue-protocol/refs/create.md` Wave 1: `gh issue list --repo <R> --state all --search "<keywords>" ... --limit 10` into `scout.md` "Possible duplicates". "Possible duplicates do not stop the run; they go into the body's related-issues section." Issues only, one repo, ten rows. Claim mode has no duplicate section (`templates/scout-report.md`); its accuracy check compares issue text to code.
- `confidence-check` skill (line 58): "No Duplicate Implementations? (25%)", about code. UNVERIFIED that it ran.
- #290: the onboarding rule (issue first, `/sc:recommend --plugin` before building) is not in HOW-WE-WORK; the 11-17 status review: "clayphi to add the primitive-change rules". #655 adds a new skill and command.
- For #655: no scout or duplicate comment. Its body lacks the template header comment that #665, #668, #675, #687, #689 carry, so whether `--create` made it is UNVERIFIED. The body itself says "Replaces #450", so the overlap was known; none of these checks would have stopped it.

## Issues and PRs that should have been referenced first

Precedence is the owner's call; the reasons are what the sources say.

| # | Date | Why it mattered | #655 cites it? |
|---|---|---|---|
| #331 | 10-30 | Owner's watcher issue; #655 closes its open parts | Yes: "closes the open parts of #331" |
| #450 | 11-08 | Open, assigned `ironbelly`, BLOCKED 11-17; Clay's question sits on it unanswered | Yes: "Replaces #450" |
| #447, #448, #485, #548 | 11-08 to 11-14 | The built poller whose code #686 reshapes; #548 is the option-3 decision | Yes: "PRs #447, #448, #485, #548, #584 and #591 are in the history comment" |
| #584, #591 | 11-17 | Plan A/B claim handoff, WC-17; #682 deletes them | Yes, same sentence; not cited in #681 to #690 |
| Owner-answers record (Q35 "B1b", Q36, Q20), via #587 to #589 | 11-14 to 11-17 | Who claims, who starts workers, who owns the watcher | No |
| Zero-setup `requirements.md` R1 to R36, plan folders (local, unpushed) | 11-18 to 11-20 | Opposite choices on cron, label gate, naming; build running in `issue_watch/` | No; not visible on GitHub |
| Coder #515, #516 | 11-18 | Owner's cron and per-project coordinator work, filed after Clay's comment | No |
| #339 | 11-01 | Owner's orchestrator umbrella; sweep is Phase 1 | Partly: "relates to #339"; "The general orchestrator for all sessions of #339" is out of scope |
| #444 and #423 | 11-08, 11-07 | #444 proposes `/sc:orchestrator`; #423 is Orchestrator v2 | Yes: "Same area, not read in full: #423 and #444" |
| #409 | 11-06 | Observer; assigned to Clay | No |
| #539 | 11-14 | `/sc:sweep`, WC-16 coordinator loop | No (spec says "sweep" 8 times, not WC-16) |
| #431 | 11-07 | Worker liveness; #655 wave 5 watches workers | No |
| #613, #636 | 11-17, 11-18 | Claim flow that wave 1 runs; #689 plans to change it | No |
| #442, Coder #477 | | Launch-level guard gate; listener | Yes: "gated by #442"; "Coder#477 stays unneeded unless its revisit condition returns" |
| #290 | 10-23 | Rule for proposing new skills; assigned to Clay | No |

Caveats: IronFlow spec and `RULINGS.md` unread; DM and chat content unread; notification state not checked; local `origin/master` may lag.
