# Round 2 findings: issue #799 (C18) Hand-back rounds: fresh branch in the reused worktree and named stops

Checked 2026-11-24 against master `f2894fc44f6e68a7dd6a78c75f59683cb0b5acb9` (worktree `/home/coder/workspaces/worktrees/IronClaude/Realign`). Live state: OPEN, label `enhancement`, no comments, sub-issue of umbrella #716 (read in full with its 2026-11-22 to 2026-11-24 comments, including the closing backlog review and the owner's 2026-11-24T20:53Z comment "Determine the current full handoff process before anything else is adopted"). Round 1 findings read: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/6/799/findings.md`. Static command: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/6/analyze` (report `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/6/analyze/analyze-report.md`). Plan files read-only from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`).

## Alignment with architectural decisions

| Decision or rule | Verdict | Evidence |
|---|---|---|
| **R38** (owner, 2026-11-21; `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): merged watcher is the design; Clay's rows "not adopted"; it "supersedes the 'Clay strengths adopted' rows of the unification spec (section 7 and the HYBRID rows of section 2)" | **Partly in conflict (round 1 missed this link)** | The hand-back loop is Clay's design decision D18, and the spec lists it in section 7 as "D18 hand-back ... ADOPT+CHANGE" (SPEC:463, section 7 header SPEC:435). QG1 calls the loop bounds "one separable Clay benefit set" (`debates/QG1/VERDICT.md:13`, `:52`). That row is inside what R38 supersedes. R38 does not name hand-back, so whether the owner still wants a coordinator hand-back loop is UNVERIFIED. `design-comparison-655.md:3` says the recommendations that adopt Clay's parts are void. |
| **FR-35 / OD-2 / R-6** (SPEC:237, :98, :600; QG1 VERDICT:24): round 2 re-plans, the person re-approves, a NEW wake id, the whole start gate repeats | **Partly aligned** | The issue's "starts the new worker on a fresh branch ... only after the old worker is final" matches FR-35's "old worker final first". It says nothing about the re-plan or re-approval, so read literally it starts round n without the gate FR-35 requires. It also relies on `/sc:issue --plan --remaining`, now closed with the whole C15 (#796, "no longer relevant", 2026-11-24T22:10Z) and PR #690 closed unmerged. |
| **OD-13 / FR-33** (SPEC:109, :235; DEC:957-959): a waiting hand-back is not counted in `max_in_flight`; carrier `escalated` is "a recommendation with checks" (DEC:959) | **In conflict for the counting part** | R38(C) rejects the "in-flight cap". `escalated` as carrier for a waiting round is UNVERIFIED (DEC:959; `debates/QG1/VERDICT.md:35`). The issue's named stop for an unusable worktree would reuse that carrier. |
| **D07 VERDICT** (`debates/D07/VERDICT.md:22`, `:67`, `:77`): one worktree holds one live agent; claim worktree sharing is a defect of the owner's own plan | **Aligned** | The item's done-when "no second live worker in the worktree" is the same rule. Interacts with open #699 (claim worktree made without an agent) and with the "never left without an agent" sentence at `src/superclaude/core/WORKER-CONTRACT.md:299`. |
| **WORKER-CONTRACT.md:299** ("Worktree, then worker": the claim script creates or reuses the worktree, `worker-start --worktree path:<exact path>` follows at once) | **Aligned** | Reuse of the issue worktree is the contract's own route. A round-n worker is a new Task, not a relaunch. |
| **WORKER-CONTRACT.md:303** ("Never ... relaunch a dead worker by itself") and **:183-191** (never act on silence: no release, no retry Task) | **Aligned if stated** | The item must say a round is started only from a settled, handled `worker_done`/`not_done`, never from silence. It does not say so; round 1 asked for the same sentence. |
| **WORKER-CONTRACT.md:237-238** (never remove a worktree or branch holding unmerged commits, an open PR or uncommitted changes) | **Aligned** | A fresh branch `issue-<N>-r<n>` leaves the old branch untouched, which the done-when tests. |
| **FR-39 and PR #711 rules** (SPEC:241; `scripts/worktree_cleanup.py`): a worktree is removed only when every related issue is closed and its own PR merged | **Aligned (complementary)** | A hand-back issue stays open, so the cleanup keeps the worktree the next round reuses (PR #711 body, eight rules). |
| **`/sc:closeout` boundary** (`src/superclaude/commands/closeout.md:76-77`): it never releases a worker, never starts the missing work and never counts rounds; it only returns `issue.handback: remaining` (`skills/sc-closeout-protocol/refs/result.md:40-47`) | **Aligned** | The round-starting duty is left to the coordinator, which is exactly this item. Who receives `handback` is still open in #771. |
| **R38(D) / WC-17** (a person's typed go for every push and merge; plan approval row before the plan boundary, `WORKER-CONTRACT.md:300`) | **Aligned if the re-approval step is added** | See FR-35 row. |
| **Owner comment on #716, 2026-11-24T20:53:53Z** ("Determine the current full handoff process before anything else is adopted"; the watcher only hands information to the coordinator) | **Gate** | No hand-back mechanism should be built before the owner confirms the handoff process; this is why the item cannot be scheduled now. |
| Existing code: `orca_worktree.py:388` matches branches with `^issue-{number}(-|$)`, so a worktree on `issue-<N>-r2` is still found by claim reuse; `:703` creates `issue-<N>` | **Aligned (fact for the build)** | A `-r<n>` suffix does not break duplicate detection. |

Searched DECISIONS.md, SPEC.md and the verdicts for `hand-back`, `handback`, `HANDBACK`, `-r<n>`, `r<n>`: hits are FR-26, FR-35, OD-2, OD-13, OA-14, R-6, X-16, D18 and QG1 only. No decision names the branch pattern `issue-<N>-r<n>` (the branch-per-round part is in no plan file).

## Complementary issues

- **#771** (open): decides who receives the closeout `handback: remaining` and what they do. #799 is the mechanism behind one of #771's options ("the coordinator starts the missing work as a new Task"). Interface: closeout result `issue.handback`, `remaining_file`, `remaining` (closeout `refs/result.md:40-47`) in, a round-n Task out.
- **#800** (open, C19): releases the old worker's terminal; #799's "old worker is final and its terminal released" is #800's output. Orca's `worker-release` closes the settled worker's terminal and keeps an output archive (`worker-release --help`, read 2026-11-24).
- **#788** (open, C7): the `orca worktree ps` check before `worker-start` is the "no second live worker" rule. One implementation must serve both; that check only passes once #800 has released the old terminal.
- **#790** (open, C9): its round-2 prompt block (round number, earlier PRs, remaining list) is the worker side of this item.
- **#793** (open, C12): a restart of a dead worker (a distinct duty) versus a new round.
- **#699 / #698** (open): shared-worktree and one-agent-per-worktree rules the round start must obey; no conflict.
- **#786** (open, C5): the Run must be bound before any `worker-start` of round n.

## Closest overlap

**#771** "Wire /sc:closeout and /sc:worktrees into the coordinator's finish, and give a 'not done' result somewhere to go". Shared: the hand-back path (what happens after closeout leaves an issue open with `handback: remaining`) and the same file (`src/superclaude/core/WORKER-CONTRACT.md`, "Issue pipeline duties", `:292-303`). Share of #799's done-when it covers: about 10 percent (it decides the recipient and trigger #799 assumes; it contains none of #799's three tests: branch name, tracked-only start check, failing re-plan and missing-worktree stops). Next closest: **#788** (about 10 percent, the live-agent worktree check) and **#790** (about 5 percent, the round-2 prompt block).

## Standalone or merge

**Verdict: stand alone, sequenced after #771's recipient decision.** Test against #771:
- *Owner*: both are coordinator-duty items under #716's author; #771 is asked by Clay and needs the owner's three answers, #799 needs the owner's handoff-process decision.
- *Acceptance test*: #771's are rule-text tests in `tests/skills/test_worker_contract.py` plus a read-only walkthrough; #799's are executable fixtures (branch name, worktree path, tracked-only start refusal, fault injection of a failing re-plan and a missing worktree).
- *Files touched*: #771 edits contract text and maybe `worktrees.md`; #799 needs a new verb and a start-time check (reusable: `scripts/worktree_cleanup.py:936-985` already splits tracked from untracked changes in `classify_status`; round 1 found no such check, that parser is the nearest one).
- *Build phase*: #771 is unscheduled and owner-gated; #799 is Phase 3 in #716's order.
- *Risk if merged*: a complex item (L) with fault-injection tests would be tied to a medium contract-text decision item, and #771 would carry the unresolved R38 question for D18 inside an item that only needs a recipient.

When merging or closing would be right: if the owner answers #771 with "a person always decides and starts each round", #799 has nothing to build and should be closed, not merged. If the owner rules that the hand-back loop is a rejected Clay design (R38), close it with the same reasoning the owner used on #796 and #804 on 2026-11-24 (rejected architecture).

## Closed issues and merged PRs checked

- **#796** (C15, closed not planned 2026-11-24): the `/sc:issue --plan <N> --remaining` re-plan route is gone, so the failing-`--plan --remaining` test names a call nobody will build (supersedes part of #799's done-when).
- **#798** (C17, merged into #797) and **#804**, **#806**, **#809** (closed 2026-11-24): show the owner's pattern of folding or closing items that rest on R38-rejected architecture; context for the R38 row above.
- **#668 / PR #683** (merged): `/sc:closeout` returns the hand-back and starts nothing; delivers the input of this item.
- **#687 / PR #711** (merged): cleanup keeps a worktree whose issue is open; delivers the safe lifetime for a reused worktree.
- **PR #700** (merged): rolled back Clay's orchestrator design (PRs 681, 682, 684); the hand-back wave (design D18) now exists only on the archive branch `clayphi/archive-orchestrator-655-20261120`, not on master.
- **PR #729** (merged): records R38; says uncovered features stay tracked in #716-#718.
- **PR #591 / #584** (merged): the adoption rows and `Worktree, then worker` step this item extends.
- **PR #724, #735, #736** (merged): owner records in chat; one coordinator per project, a script-started coordinator is valid; none touches rounds.
- **PR #432 / #469** (merged): launch-level guard; no hand-back or branch rule.
- **#444** (closed not planned): sub-orchestrator evaluation; no bearing.

## Updated recommendation

**Keep open with changes, P3, complex, size L. Unchanged from round 1 on action, priority, complexity and size; what changed is the reason and two additions.**
Changes: (1) add the re-plan and re-approval step before any round-n worker (FR-35, OD-2, WC-17). (2) The `/sc:issue --plan --remaining` re-plan route is closed (#796): the item must name a different re-plan route or drop the failing-re-plan test until the owner decides. (3) Replace "one escalation line in the issue's entry": the report entry is parked (#716 comment 2026-11-22, #720, #719). (4) For the "tracked changes only" check, reuse the `classify_status` parser in `scripts/worktree_cleanup.py:936-985` instead of a new check, or drop it. (5) New: before any build, the owner confirms that a coordinator hand-back loop (Clay's D18, superseded by R38 unless re-adopted) is wanted at all, together with #771's recipient decision and the "handoff process first" comment. The owner decides.

## Scan record

- Lists read in full: open-issues.tsv 134 of 134 lines, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508 (`/home/coder/workspaces/worktrees/IronClaude/Coordinator/.dev/issuecleanup/realign-inputs/`).
- Search terms: hand-back, handback, round, worktree, branch, reuse, release, terminal, settle, worker, re-plan, plan, closeout, finish, worktrees, cleanup, claim, one agent, coordinator, C1x numbers.
- Opened in full with `gh issue view` / `gh pr view --repo IronbellyOrg/IronClaude` (read-only): open issues #716, #771, #788, #790, #793, #800, #801, #787, #786, #792, #699, #698, #770, #755 (14); closed issues #796, #798, #809, #804, #806, #668, #687, #444 (8); merged PRs #683, #700, #711, #729, #591, #584, #724, #735, #736, #707, #432, #469 (12). Skimmed from the scan list only: the rest.
- Plan files read: SPEC lines 62, 98, 109, 228, 235, 237, 435-463, 600; DEC 957-959, 504; QG1 and D07 VERDICTs; R38; `design-comparison-655.md`. UNVERIFIED: the unread remainder of the plan files; whether the owner still wants D18 hand-back (no record found); live behaviour of `escalated` as carrier.
