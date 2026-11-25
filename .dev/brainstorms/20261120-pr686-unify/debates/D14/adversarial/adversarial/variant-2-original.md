# D14 position: CLAY (Clay line)

Question: what is the final disposition of PR 686 (Clay's rewrite of the watcher, head 8e5ae29ad), PR 690 (branch issue-655-pr-p), issues 687 and 689, the merged design doc (PR 681), the merged deletion (PR 682), PRs 683 and 684, issue 655 and issue 450?

"Dnn" = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Dnn/VERDICT.md`. "The poll" = the unattended watcher job. `enabled: false` means the poll is switched off in shipped config.

## Claim

The stack is built, reviewed and green, and it runs nothing live. Merge it in the order the design set (681 done, 682 done, 684 done, then 686, then 690), and treat every verdict adaptation as a small follow-up PR on top, because each adaptation is cheaper after the stack is on master than before. Keep issue 655 as the tracking issue; close issue 450 into it. Do not revert PR 682.

## Mechanism

- The design (PR 681) chose the order: PR D (delete the old gate), PR A (the poll), PR C (report), PR P (`/sc:issue --plan`), then B and E. Landing out of that order makes later PRs wait on rework (design section 7, D:978-1030 as cited by D03 Strongest points CLAY 1).
- Because the poll ships `enabled: false`, merging PR 686 changes no live behaviour. The owner's cron, live test and shadow run (issue 450) are still required before anything runs, so a fix-forward period costs nothing in production.
- Nothing is lost by landing: the verdicts adopt Clay's pieces in all thirteen topics, so the code ends up on master anyway.

## Cited facts

1. PR 686 is open, mergeable, and all six CI checks pass; it went through 12 review-fix rounds (27 Augment, 24 Codex and 64 Clay comments); the last two rounds touched only `cycle.py` and tests. Source: `gh pr view 686 --repo IronbellyOrg/IronClaude` (MERGEABLE, headRefOid 8e5ae29ad); inventory/clay-prs.md section 4.
2. Nothing ran the removed code: PR 682's body says "Nothing runs this code ... `enabled: false`"; the watcher built in PRs 447 and 448 has never run live. Source: inventory table 2A; FULL-REPORT.md section 3 "The case for the deletion".
3. The old plan-approval gate had a documented cost and limit: one login serves the owner and the agents (accepted risk L-1), and it needed two sessions and a grant row per approval, accepted only "for now" (Q36). Source: D03 VERDICT.md Strongest points CLAY 2.
4. Reverting 682 is a 4,599-line change (2,969 test lines); D03 itself puts confidence at about 50 percent for the revert if the gate is dropped, because then it is churn. Source: D03 VERDICT.md Confidence.
5. Clay gave notice: a comment on the owner's issue 450 on 2026-11-18 17:00:32 UTC addressed to `@ironbelly` ending "What do you think?", then issue 655 stated what it replaces and what it carries over. The owner's own decisions of 11-18 and 11-19 sit in an unpushed local plan that nobody on GitHub could see. Source: FULL-REPORT.md section 1 points 2 and 4, section 9, section 7 line 98.
6. The owner's own alignment records (PRs 587 to 589) mark the watcher-to-orchestrator handoff DEFERRED, not rejected, with the chain watcher, then orchestrator, then dashboard. Source: FULL-REPORT.md section 9.
7. Clay's design carries controls the owner's line lacks and the verdicts adopt: `plan_check`, `hold:backlog` (D01), the merge gate, `answer-check`, `E-NO-GRANT`, audit AU1 to AU8 (D05, D06), acknowledged wake with three deliveries (D10), in-flight cap and guarded restart (D07), living report (D11), `/sc:issue --plan` (D12), closeout (D13). Source: the named verdicts, "Clay strengths to adopt" sections.
8. PR 690 (`/sc:issue --plan` and `--remaining`) is independent in code from PR 686, passed three review rounds, and D12 rates it KEEP-ADAPT with four small fixes, not a rewrite. PR 683 already points to `/sc:issue --plan`, which only lands in 690. Source: D12 VERDICT.md; D13 VERDICT.md Implications.
9. Several verdict conditions can be met as follow-ups: the rename of persisted names (a grep-and-replace; `wake.py:46-47`, tests), M1 and M2 (small order and re-target rules), the registry removal. Clay's design already names K11, K14, K16 as accepted risks with live tests planned. Source: D08 VERDICT.md action 8; D10 VERDICT.md items 10, 11; D10 Clay strengths (honest register).

## What it gets right

- Speed and momentum: a green, reviewed, mergeable PR ends the twelve-round cycle.
- It respects that the poll is off, so the harm of an imperfect first landing is bounded.
- The design's reuse table (runner, audit log, lock, call budget of PR 447) shows the work builds on the owner's code, not a copy.
- It keeps one design as the single source for PRs A to E, which avoids a second plan.

## What it costs

- It asks the owner to accept a design written and approved by Clay as the base, with ten contested rows, and amend afterwards.
- Follow-up PRs must reverse parts of PR 686 (re-add approval and trigger code) and rename wire strings that will already be on master.
- Planb (225 entries, six shared files) conflicts in a modify/delete way on rebase (UNVERIFIED, not tried).

## What it risks

- Landing the combined state of PR 686 and any revert of PR 682 breaks `superclaude --help` (D03 INV-001), so the revert option is closed off once 686 lands unless 686 is revised.
- Wire names with "orchestrator" in them and a registry shape become public on master (D08 action 8; D07).
- No owner review exists on any PR of the stack; `master` is unprotected, so a merge is final in practice.
- The M1 and M2 defects in the wake transport ship on master, though the transport is off.

