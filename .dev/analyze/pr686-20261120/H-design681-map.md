# H: map of the design merged in PR #681 (`docs/designs/orchestrator.md`)

Read 2026-11-20 with `git show origin/master:docs/designs/orchestrator.md` (1,412 lines; cited below as D:line). Read-only; nothing was written to GitHub or Orca.

1. The design says "approved by the owner (Clay)". Every GitHub source I read puts Clay's words and the approval in text posted by the account `clayphi`; none shows `ironbelly` (the repository admin) seeing it.
2. Author, approver of record and merger of #681 are all `clayphi`. No human review, approval, reaction or assignment exists on #681 or #655. UNVERIFIED whether `ironbelly` read it elsewhere (chat, calls).
3. Main collision with the owner's line: the design deletes the approval label, approver list, Project Status gate, Pipeline levels, cron and the per-issue grant row. The owner's zero-setup plan (R19 to R36) is still building those, last amended 2026-11-20.
4. Also contradicted: Q26 coordinator layout (`.dev/coordinators/` in each project), the "coordinator, not orchestrator" naming (Coder 516), the WORKER-CONTRACT person-opened-coordinator and push-on-go rules, and the pr-submit "no-activity reviewer is skipped" rule.
5. Real reuse: the built poller code, `/sc:issue --claim --pipeline none`, `/sc:pr-submit` poll scripts, `/sc:closeout` (#683), ccsession tiers, Orca orchestration verbs, Clay's IronFlow coordinator spec.
6. Silent on `/sc:sweep`, `superclaude observe` (#409), #423 knowledge layer and WC-16. Already being built: #682 (PR D), #683, #684 merged; #686 (PR A) and #690 (PR P) open.

## Who approved it

**Status line (D:3):** "approved by the owner (Clay) on 2026-11-19 with his approval of additions A to E (ruling 37)". D:11 defines "the user" as "the person the orchestrator works for (Clay)". D:1146 and D:1217 mark OD1 to OD15 "Decided" by "Clay's rulings".

**Who is "the owner (Clay)":** the design never names a GitHub login. All 15 comments on #655 (2026-11-18 20:00 to 2026-11-19 22:19 UTC), the issue, #681, #665, #668, #682 to #684, #686, #687, #689 and #690 are by `clayphi`. Several comments say "applied by the orchestrator session", so an agent posted them under that login. `clayphi` has `maintain`; `ironbelly` has `admin` (collaborators API). `ironbelly` wrote #331, #339, #409, #423, #444, #450. Clay's #450 comment of 2026-11-18 17:00 says "@ironbelly my thoughts ... What do you think?", so `clayphi` and `ironbelly` are different accounts and that comment is a proposal. #450 has no later comment from `ironbelly`.

**Rulings** (the design cites 1 to 39; they are kept in `RULINGS.md` of the orchestrator session, which I did not read: UNVERIFIED by number). What GitHub shows:

| Rulings | Where stated | By, date |
|---|---|---|
| R1 to R15 (D:71-87), assignment-only trigger, Orca automation, no approver list, #655 comments 0 to 11 | text on #655 and #450 | `clayphi`, 2026-11-18 |
| 1 to 11 (living report, no session manager, workers never merge, merge method, review hold, hourly check, 3 in flight, bots dropped) | #655 comment 12, 2026-11-19 02:23 | `clayphi`, "Clay's rulings, applied by the orchestrator session" |
| 12 (tiers) | #655 comment 13, 03:14 | `clayphi` |
| 13 to 36, 39 (additions A to E, 13:16 to 13:34 UTC per D:1181) | #655 comment 14, 22:19, summary only | `clayphi` |
| 37 (approval of the spec) | status line, comment 14, PR body | text only; no dated primary source read |
| 38 (clarifies 26) | comment 14 | "GeneralIronFlow"; identity UNVERIFIED |

All came from `clayphi`'s account; none from `ironbelly`.

**Merge data (#681):** opened 2026-11-19 22:32:39, merged 2026-11-20 00:02:33 (about 1.5 hours later) by `clayphi`. Reviews: Codex (comment, 2 P2 findings), Augment (4 findings), six self-replies by `clayphi` ("The owner approved this text byte for byte; recorded for #665"). `reviewDecision` empty, no reviewers requested, no labels, no assignees, no reactions. The PR body says "the owner reviews and merges", yet the author merged it.

**`ironbelly` evidence:** zero comments, reviews or reactions on #655, #665, #668, #681 to #684, #686, #687, #689. Only trace: an `ironbelly` accuracy-check comment on #624 (2026-11-20 00:54) lists #681 among 45 pull requests checked for file history. That is a list, not a review. Not approval.

## Element-by-element map

| Design section | What it decides | Relation | Existing work and evidence |
|---|---|---|---|
| 1.1, 1.4 R1 (D:33-49, 73) | Assignment is the only trigger; no trigger or approval label, no approver list, no plan-approval gate | CONFLICTS | Zero-setup R19: "the approval label plus the issue's state stay the gate", owner 2026-11-18 confirmed; R22 Status allow-list; R36 (2026-11-20) keeps the `Approved` field. Its "Gates that stay manual" says the same. Design D:73 "no approval label ... no plan-approval gate" |
| 1.4 R4, 4.8 (D:76, 343-354) | Orca automation `orchestrator-poll`, no cron | CONFLICTS | Zero-setup R6 "Cron is the scheduler (owner decided 2026-11-18)", R16; Coder 515 (open) installs cron. Clay's own #450 comment asked for Orca automation |
| 1.4 R9 (D:81), 5.3 wave 1 | Claim at `--pipeline none`; the claim's launch levels never used | CONFLICTS | Zero-setup R23/R25: Status picks the command, Pipeline field picks level, owner "launch levels widened 2026-11-19". Builds on `issue.md:48` ("watcher always passes --pipeline none") |
| 1.3 (D:65) | Takes name `/sc:orchestrator`; leaves `--sub` to #444 | OVERLAP | #339 and #444 propose that command; U19 (D:1277) "how #444 joins is UNVERIFIED" |
| 1.3, DQ9 (D:65-67, 119) | No session manager; orchestrator does check-ins, types into terminals, approves permission prompts | OVERLAP, NEW parts | #339: hourly sweep, close or resume sessions; `/sc:sweep` (merged, read-only) and WC-16 "run /sc:sweep on every wake". Design never mentions sweep. Approving prompts for workers is NEW |
| 2 DQ2, 3 wake (D:112, 143-237) | Wake file, mailbox message, typed line, session start | BUILDS ON / DUPLICATE | `waker.py` pattern; D:432 says `wake.py` "duplicates about 100 lines of the IronFlow script". Coder 477 (listener, open) does routing a different way; D:66 and issue-watcher NG-1 reject listeners |
| 2 DQ3 (D:113) | Lease comment on the issue, lowest comment id wins | NEW | Adds a GitHub comment; `/sc:issue --claim` makes re-claim idempotent |
| 2 DQ6 (D:116) | Standing `grants` list in `repos.yaml` | CONFLICTS | Zero-setup: "each issue still needs its own grant row from the owner". Design: "the old per-issue grant row ... retires" |
| 2 DQ7, K12 (D:117, 1234) | Workers started by `worker-start` run with no launch-level guard or L2 hook; `master` unprotected | CONFLICTS (partly) | D:117 says the owner accepted this "for the first test issue" only; #442 observations (owner's #685 runbook) and R33 `GOVERNED_LEVELS_ALLOWED=False` assume the guard governs launches |
| 2 DQ8 (D:118), 5.3 waves 7-8 | Orchestrator merges; closing is its job via closeout | CONFLICTS | WORKER-CONTRACT master: "coordinator ... only when the user's instruction names that action and confirms"; "pushes only on the person's go". D:911 (C13) rewrites coordinator spec FR-13 "human-only list: merges" |
| 2 ADD1 (D:135), 8.1 PR B | New "Orchestrated issue flow": worker runs `/sc:pr-submit`, coordinator "may be started by a script" | CONFLICTS | WC contract (`WORKER-CONTRACT.md:23`, `:244`): `/sc:pr-submit` "never as a worker"; "an Orca coordinator session the person opened" (line 70). Memory "approvals through chat" |
| 2 ADD4 (D:138) | A reviewer with no activity holds the PR | CONFLICTS | Project CLAUDE.md for `/sc:pr-submit`: "a reviewer that shows no activity on the PR is skipped". Design admits it drops that |
| 2 ADD3, 4.4 (D:137, 267-305) | Multi-repo search per org; repo list in `IronbellyOrg/IronOrchestrator` `repos.yaml` | OVERLAP (rival mechanism) | Zero-setup R5/R8/R13/R16: one loop over `orca repo list`, configs in `~/.config/superclaude/issue-watch.d/`. D:87 R15 forbids repo list in IronClaude config |
| 4.1, 4.10 (D:243, 361-434) | Reuse `runner.py`, `record.py`, `audit.py`, budget code; remove approval, Project, GraphQL edit code | BUILDS ON + CONFLICTS | Built watcher (#447, #448, `issue-watcher.md`). Removes what zero-setup R19, R22, R31, R35 are extending on branch `ironbelly/issue-watcher-zero-setup-plan` (edits `predicates.py`, `github.py`, `cycle.py`, `launch.py`) |
| 4.10 line 410, 4.11 (D:410, 436-495) | Poll writes labels `hold:plan` and `hold:backlog`; plan check; plan request after 1 hour | NEW / COMPLEMENT; CONFLICTS with NG-2 | Nothing held plan-less issues (#651 only adds template sections). `issue-watcher.md:76` NG-2 "no GitHub write" |
| 5.3 wave 6-7 (D:528+), 5.10 | PR watch reuses pr-submit poll scripts; `/sc:closeout <PR>` | BUILDS ON | `sc-pr-submit-protocol/scripts`; `/sc:closeout` merged as #683 (adopts Jay Wedgeworth's skill) |
| 5.6 (D:664-696) | Nine-row "what reaches Clay", cap 5 notices a day, typed answers only | COMPLEMENT | Fills a gap beside FR-12 "Needs you". Typed-answer rule fits memory "approvals through chat" |
| 5.7 (D:698-718) | One orchestrator per repo, 3 in flight; ids `<short>-<n>`; state in `.orchestrator/` of another repo; O_EXCL files | OVERLAP / CONFLICTS | Q26 final: "owner's answer of 2026-11-14 settles where coordinators live: a Coordinator branch and worktree and a `.dev/coordinators/` directory in every project"; layout `<kind>-<slug>/<dev>--<N>` with create-once claim files. Q26 also says "It advises; it decides nothing". #444 sub-orchestrator; #339 orchestrator of orchestrators (body read only in part) |
| 5.8 (D:720-734) | Tiers in `repos.yaml`: plan tier1b, worker tier2, orchestrator tier1b | BUILDS ON | ccsession `--tier`, `sc-issue-protocol/refs/tiers.md`; U28 and U29 UNVERIFIED |
| 5.9, 5.11 (D:736, 801) | Closed "may do" list, `refuse(argv)`, audit AU1 to AU8 | NEW | Nothing equivalent on master |
| 6, 6.3 (D:849-932) | Coordinator spec (IronFlow) moves to `IronOrchestrator`, 29 edits; PR C moved `agent-work-report` | BUILDS ON Clay's spec; OVERLAP | #684 merged. The living report is a third view beside `/sc:sweep` reports and the observer (`superclaude observe`, #409 "same facts in the same way"). Design never mentions #409 or #423 |
| 7 (D:951-1005) | Carries FU-3 to FU-12, shadow run, lock and restart tests; drops cron, approvers, FU-9, FU-7 | BUILDS ON / CONFLICTS | `issue-watcher-setup.md`; zero-setup R18, R28 rely on the same checks for the dropped gate |
| 8 (D:1007-1048) | PR D first, then A, P, B, C, E | BUILDS ON ruling 9 only | #682, #683, #684 merged by `clayphi`; #686 and #690 open. #689 (clayphi, 2026-11-20) moves planning into create and sends claim to workflow and implement: same line, not reconciled with D:136 |
| 10 (D:1146-1216) | OD1 to OD15 all "Decided" | Self-attested | Zero decisions by `ironbelly` in any source read. AD-D5 to AD-D7 "stand unless the owner objects" |

## Worth folding in

Strongest case FOR the design: it answers questions the owner's line left open (the watcher could only claim, with a person doing every later step); it adds a plan-before-claim hold nothing else covers; it already reuses the built poller, `/sc:closeout`, ccsession tiers and the pr-submit scripts; it has 62 reasons, tests T1 to T13 and an UNVERIFIED list; its goal of no manual session handling matches #339 ("no sessions should be run interacted with manually"). It is also already half built on master.

Candidates to fold in (each is separable from the contested rules):
- Hold label plus plan check (4.11), since it needs no decision on cron or approval.
- Closeout (#683) and audit AU1 to AU8, as post-merge steps any coordinator can call.
- Nine-row escalation table and the typed-answer check (5.6).
- Tier settings (5.8) and the hand-back loop (wave 8).
- The wake format and the multi-org search (ADD3), as the transport for either design.
- The `plan_check` function and "no GitHub text reaches a typed line" rule.

## Must be reconciled or dropped

1. **Trigger and gate.** R1 against zero-setup R19, R22, R23, R25, R31 to R36. One must win. PR D (#682) already removed `issue_pipeline`, which the owner's branch edits (`brief.py`, `cli.py`, `reads.py`); a merge conflict on that branch is likely (UNVERIFIED).
2. **Scheduler.** Orca automation against cron (R6, Coder 515). Coder 515 and 516 and 477 never mention #655.
3. **Where coordinator state lives.** `IronOrchestrator` and `.orchestrator/` against Q26's in-project `.dev/coordinators/`. The two also disagree on claim locks.
4. **Names.** `/sc:orchestrator` against "coordinator, not orchestrator" (Coder 516, zero-setup R10), and against #444's use of the name.
5. **Authority.** Standing grants, autonomous merge, workers with no guard, a script-started coordinator, against WORKER-CONTRACT lines 23, 70, 239 to 246 and the FR-13 human-only list. Needs the repository owner's own recorded decision, not a relayed one.
6. **Reviewer rule.** ADD4 against the `/sc:pr-submit` skip rule.
7. **NG-2 read-only watcher.** Label writes in `issue_watch/github.py`.
8. **Silent overlaps.** Wire `/sc:sweep`, `superclaude observe` and #409 into wave 5, or say why not; place #423 and #444 explicitly; reconcile #689 with the `--pipeline none` claim.
9. **Process.** Re-ask for `ironbelly`'s explicit approval of #681 before more PRs (B, E) build on it.

## Caveats

Not read: `RULINGS.md`, the IronFlow coordinator spec, #339 body past the first 60 lines, the orchestrator repo; `GeneralIronFlow` and the "owner" in zero-setup rows are not identified in any source.
