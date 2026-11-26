# Round 2 findings: issue #810 (W2) One plan request from the poll after one quiet hour

Checked 2026-11-24 on master `f2894fc44`. Issue state: OPEN, no comments. Parent: umbrella #717. `<P>` = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify`. `<R>` = `/home/coder/workspaces/worktrees/IronClaude/Coordinator/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. Analyze check: `.dev/issuecleanup/b/8/analyze/810/analyze-report.md` (target `src/superclaude/cli/issue_watch`).

Defect in the issue text: the body is 164 lines and carries the full text of W3 to W15 after W2 (`gh issue view 810 --json body`, lines 35 and 152), which belongs to #811 to #823. Any edit of W2 must cut it.

## Alignment with architectural decisions

- **R38 (A)** (`<R>:64`, owner 2026-11-21): work starts only on assignment plus trigger label plus `Approved` field plus an allowed Status; "his plan check, `hold:plan` and `hold:backlog` are not adopted". W2 fires when an assigned issue "has failed the plan check for one hour". **In conflict.** The plan check is what R38 rejects.
- **R38 (C)** (`<R>:64`): "in-flight cap, idle end, wake file with acknowledgment ... are not adopted". W2 writes a wake-file item and counts the open request in the in-flight count (S05-F21). **In conflict.**
- **PR #729** (merged 2026-11-23): records R38 and says uncovered features remain in #716 to #718; it does not re-adopt the wake file.
- **D15 A4** (`<P>/debates/D15/VERDICT.md:44`; `SPEC.md:442`; `DECISIONS.md:567`): "Plan request after one hour: Defer ... Not built now; if built, ids only and after D07 settles who plans". W2 asks to build it now. **In conflict with the Defer**; and D07 is overtaken by R38 (C).
- **D09** (`<P>/debates/D09/VERDICT.md:64`): "Defer the one-hour plan request and the lease comment" to D07. **In conflict** (same reason).
- **D10 item 5** (`<P>/debates/D10/VERDICT.md:18`) and **FR-13** (`<P>/spec/SPEC.md:203`), **SEC-16** (`:305`): wake items carry `repo`, `number`, `url` only, no title; no GitHub text reaches a prompt. W2's own text keeps ids only. **Aligned** on that point; the 655 title variant (S01-F16) is correctly rejected.
- **D01 item 5** (`<P>/debates/D01/VERDICT.md:16`; FR-04 `SPEC.md:194`): a plan written after approval voids the approval, so a plan request must finish before approval. **Aligned and a live trap**: R19 and R37 (`<R>` rows R19, R37) keep "a body edit after approval voids it"; a plan request that edits the body after approval is refused as `edited_after_approval` (`src/superclaude/cli/issue_watch/audit.py:71`). W2 cannot meet its purpose for approved issues.
- **FR-05 plan check** (`SPEC.md:195`) and **A1** (`SPEC.md:441`): the plan check was adopted with change in the unification spec but is voided by R38 (A); PR 686 (the only code) is CLOSED. **Conflict.**
- **WORKER-CONTRACT** (`~/.claude/WORKER-CONTRACT.md:290-303`, WC-17 `:59`): the coordinator adopts claims from `dispatch.json` and the issue folder; no wake file is read; plan approval is the reply to the worker's own ask (WC-17). **Conflict**: W2's consumer path does not exist and the contract has a different plan route.
- **NG-2** (poll writes nothing to GitHub; `DECISIONS.md:386-390`): W2 writes only the wake file. **Aligned**.
- Master (analyze report): 0 hits in `issue_watch` for plan_requests, plan_stuck, held_incomplete, plan_check, wake, max_in_flight, coordinator_full; `audit.py:71-84` has no `plan_stuck`.
- Searched DECISIONS.md, SPEC.md, FOLLOW-UPS.md and the verdicts for: plan request, plan_requests, plan_stuck, hold:plan, held_incomplete, quiet hour, in-flight.

## Complementary issues

- **#716** (umbrella) and its closed sub-item **C15 (#796)**: C15 was the consumer of W2's wake item. The owner closed #796 NOT_PLANNED on 2026-11-24T22:10Z saying R38 rejects the plan check and the wake file, PR 690 was closed, and "the sibling item W2 (#810) has the same base. If plan-less issues should still be filled automatically, a new, smaller item against the merged claim and plan-approval flow (WC-17) is the way, decided together with #810". So W2 has no consumer left.
- **#770** (watcher hands each claim to the coordinator and results come back): the one watcher-to-coordinator channel. Whatever replaces W2's wake file must use it. Interface: one item format and one wake path.
- **#757** (sweep outside the session, wake only on change): a candidate transport.
- **#772** (stage flow: Research, Spec, Plan, Debug; what Pipeline Full means): who moves an issue into the Plan stage.
- **#775** (a comment on an approved issue silently cancels approval): the same voiding rule that makes a post-approval plan edit fail.
- **#761** (18 gaps) and **#777** (map the chain): where "plan-less issues" would be decided.

## Closest overlap

**#770**, "The watcher hands each claim to the coordinator, and results come back to it" (open). Shared: a watcher-to-coordinator message path and the question "what does the coordinator learn, and when". W2's transport half (wake file, ids only, one item per issue) is the same problem. I estimate about 25 percent of W2's done-when (the delivery of an ids-only item to the coordinator, not the quiet clock, the plan-check trigger, the in-flight count or `plan_stuck`). Next two closest: **#772** (about 15 percent: who starts the Plan stage) and **#757** (about 10 percent: a possible wake transport).

## Standalone or merge

**Verdict: close (do not keep as standalone; do not merge as written).** Tested against #770:
- Owner: #770 is the question of the watcher's hand-off; W2 is a watcher feature that needs it. Same owner decision (the owner's note on #796 says "decided together with #810").
- Acceptance test: W2 = quiet clock, one request at 60 minutes, none at 59, in-flight count; #770 = coordinator learns of a claim and a result, one live run. Different.
- Files touched: W2 = `cycle.py`, `record.py`, `audit.py`, a new wake module; #770 = `issue_pipeline/cli.py`, WORKER-CONTRACT, sweep. Different.
- Build phase: W2 is "watcher first part" in the #717 order; #770 is a prerequisite. W2 cannot start before #770 settles.
- Risk if merged into #770: the plan-check trigger, which R38 rejects, would ride into a P1 item; risk if kept as is: someone builds a wake file R38 rejects.
Plainly: merging the transport idea into #770 would be right, and the surviving idea ("plan-less approved issues get a plan automatically") belongs as one note on #772 or a new smaller item built on WC-17. The coordinator posts that only after the owner's go.

## Closed issues and merged PRs checked

- **#796 (C15)** closed NOT_PLANNED 2026-11-24: the consumer; closing note above.
- **#809 (W1)** closed NOT_PLANNED 2026-11-24 (merged into #716): the baseline half is covered by `approval_before_init` (`predicates.py:268`).
- **#813 (W5)** closed NOT_PLANNED 2026-11-24.
- **#450** (closed COMPLETED): watcher rollout; live operation reported.
- **#651 and PR #661** (merged 2026-11-19): every `/sc:issue --create` template now requires Priority, Fix approach and Test plan at every depth, so issues made through the command arrive with their plan sections. This removes most of W2's premise (a plan-less assigned issue).
- **#689** (closed NOT_PLANNED by Clay 2026-11-23): "plan everything at creation"; supports the same direction.
- **PR #686, #690** (CLOSED unmerged): the only code for plan check, wake file and `plan_requests`.
- **PR #707** (merged): the actual watcher; no plan check.
- **PR #729** (merged): R38.
- **PR #759** (merged 2026-11-24): first-run retry; not a plan request.

## Updated recommendation

**Close** (as not planned), because R38 (A) and (C) reject its base, D15 A4 defers it, its only consumer #796 was closed by the owner, and #661 removed most plan-less issues; the owner's note on #796 says to decide together with #810. If the owner keeps it open instead: keep open with changes (rewrite on top of #770 and WC-17, cut the W3 to W15 text from the body), priority **P3**, complexity **complex**, size **L**. Changed from round 1 (keep open with changes, P3, complex L): the action. Why: round 1 had not seen the closing of #796, #809 and #813 (22:10Z) and the owner's note that W2 shares #796's base; complexity, size and priority are unchanged.

## Scan record

Read in full: open-issues.tsv (133 rows), closed-issues.tsv (156), merged-prs.tsv (507), titles only. Search terms: plan, quiet, wake, hold, in-flight, hand, claim, coordinator, stage, approval, watcher, poll, template, priority, fix approach. Opened in full: open #716 (body, 3 comments), #717 (body, 2 comments), #770, #772, #757, #775, #777, #761, #795; closed #796, #809, #813, #450, #651, #689; PRs #707, #729, #661, #686, #690, #759. Plan files: SPEC.md, DECISIONS.md, FOLLOW-UPS.md and the D01, D07, D09, D10, D15 verdicts; `<R>` R38. Master: grep over `issue_watch` (0 hits) and `audit.py`. UNVERIFIED: whether the owner will accept a smaller replacement item; #776 and #773 not read; PR #690 read by body only.
