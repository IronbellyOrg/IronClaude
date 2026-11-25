# X14 FINAL: restore the PR 681 design text docs/designs/orchestrator.md? (Appendix B.3 action 2)

Reconciler's note. Written 2026-11-22. Read A-0, B-0, A-3 and B-3. I opened three sources myself (section 10). Every verdict here is a recommendation until the owner says so in chat.

## 1 Unified proposal

Do not restore `docs/designs/orchestrator.md`, as is or amended. Record Appendix B.3 action 2 as "No. Clay's text is archived. The unified design goes in a new file, docs/designs/coordinator.md, written once at stage S10."

Order (each write only after the owner's chat go, one at a time, `--repo IronbellyOrg/IronClaude` on every gh call):
1. One comment on issue 716 (the coordinator backlog issue). It holds the hold sentence: no builder starts PR B (the coordinator skill), PR E (the runbook rewrite), S11 (adapt PR 686) or S13 (coordinator substrate) until coordinator.md exists and the owner has said in chat that it is approved. It also corrects the line "the design doc is on the archive branch only": the text is in master history at commit `c2a139552` and on two branches. It says "approved by the owner (Clay)" inside the file is Clay's wording, not an owner approval.
2. One comment on issue 655 (Clay's issue). It says where the text is kept (commit first, then the branches), why it was not restored (the plan treats it as unapproved source), that 655 stays open and rescoped, and that 716, 717 and 718 carry what 655 proposed beyond the plan. At most one `@clayphi` mention.
3. Optional, last: push a tag `archive/pr-681-orchestrator-design` on `c2a139552` as a findable name. Deleting the tag undoes it.
4. Later, the S10 pull request writes the full `docs/designs/coordinator.md` (binding decisions in plain words, the nine owner-only items each marked open or ruled with its safe default, what was taken from Clay's text, pointers to 716 to 718). It opens only with `/sc:pr-submit --monitor 3`, after the nine items are ruled and the spec is re-reviewed. When it is made, the local SPEC.md rows for FR-68, S10, S11 and S13 are reworded so the gate is "approved by the owner in chat, with a date", because a merge of any file would meet "S10 merged" by the letter.

No status file goes on master now (see section 9).

## 2 Context

PR 681 put Clay's 1412-line coordinator design on master. Clay merged it themself. PR 700 then removed it. The plan (FR-68, S10, D14) wanted a banner plus an owner-reviewed amendment. With the file gone, any restoration is a new owner-reviewed change. Issues 716, 717 and 718 now carry what 655 proposed beyond the plan. The unified spec is local and not pushed, so builders elsewhere cannot read it.

## 3 Implications

- Changes: Appendix B.3 action 2 is recorded as No. Two issue comments appear, posted from the shared ironbelly login. S10 becomes "write coordinator.md" instead of "restore and amend".
- Stays blocked: PR B, PR E, S11 and S13 stay held until the owner says in chat that coordinator.md is approved. The nine owner-only items still need rulings first.
- Stays as is: issue 655 stays open with assignee clayphi. Clay's branch and PRs 686 and 690 are untouched. `docs/designs/sc-closeout.md` keeps its five labelled references (lines 106, 155, 189, 361, 379); no edit.
- Side note for the S10 pull request: four older files (`orchestrator-mode.md` and `orchestrator-mode-review-1.md` to `-3.md`) are on master. The S10 pull request must say what happens to them.

## 4 Benefits

- Master never carries a text that claims an owner approval no owner gave, nor Clay's rule R1 ("no plan-approval gate after the claim"), which contradicts the plan-approval rule PR 700 put back.
- The hold reaches builders where they get work (issue 716) now, at almost no cost.
- Clay's text is kept in three places and credited; nothing of theirs is deleted again.
- The amendment is done once, on the real unified design, not twice.

## 5 Risks and containment

- Clay may read "not restored" as a second erasure. Their reaction is UNVERIFIED. The 655 comment says where the text is and that 716 to 718 mine it.
- A comment is not a lock: master is unprotected and has no CODEOWNERS file, so an agent that ignores the comment is stopped only by the spec gates and the owner's chat sentence. Contain: rewording the spec gates (step 4); the CODEOWNERS and ruleset change (FR-75) should land before the S10 pull request.
- A comment can be edited or hidden by anyone with the shared login. Contain: the optional tag, plus the decision ledger record.
- A builder treats Clay's text as a spec. Contain: the hold sentence and issue 716's existing rows, which say each wave row is re-checked against the verdicts before building.
- The archive branch could be deleted. Contain: the commit is permanent in master history; two branches and the optional tag also hold it.
- S10 drags and S11 and S13 wait. Contain: S10 only writes decisions already ruled; open items stay "open, safe default".

## 6 Costs (all estimates, unmeasured)

- Now: steps 1 to 3 about 30 to 60 agent minutes (basis: two short comments, one ledger record, one check of each). Owner about 10 minutes (one answer).
- S10 pull request later: about 3 to 10 agent hours (A said about 3 to 5, B said 6 to 10; basis: trimming a 790-line spec, up to 3 review rounds) plus 1 to 2 owner hours of reading. This cost belongs to the S10 decision, not to this one.
- Restore-and-amend instead: about 6 to 16 agent hours (basis: about 94 changed lines in A's count, 13 line entries and 11 verdicts in B's), plus a full read of 1412 lines.

## 7 The sentence the owner says in chat

"X14: do not restore the 681 design file. Hold PR B, PR E, S11 and S13 until coordinator.md exists and I have said in chat that it is approved. Post the comments on 716 and 655, comments only, no status file."

## 8 What an agent does after it

1. Records those words in the decision ledger and sets Appendix B.3 action 2 to "No, archived; new file at S10". The owner writes no file.
2. Posts the comment on 716, then on 655, using `gh issue comment N --repo IronbellyOrg/IronClaude`. Reads each back to check it posted.
3. Pushes the tag only if the owner says so. A hook blocking a tag push is UNVERIFIED; the push result says.
4. Rewords the local SPEC rows (FR-68, S10, S11, S13) to the chat-approval gate.
5. Leaves 717 and 718 unchanged (their bodies do not carry the wrong claim).

## 9 Consensus and residual choice

Consensus: partial. Both agents agree on everything above except one point, and each accepts the other's form.

Residual owner decision: do you want a short status file `docs/designs/coordinator.md` (40 to 80 lines, "DRAFT, nothing here is an instruction to build", states that a merge is not approval) on master now?
- Answer "no, comments only" (my recommendation, and A's pick): about 30 to 60 agent minutes, no new text on master, no review loop. The hold is visible only to readers of 716 and 655. A reader of master alone does not see it.
- Answer "yes, add the status file" (B's pick if the S10 pull request is more than about 2 weeks away): adds about 1.5 to 2 agent hours, a 1 to 2 hour review loop and about 20 owner minutes (estimates). The hold becomes findable in `docs/designs/` and survives a deleted comment. It is more unreviewed text on master and binds no more than the comment, since master has no CODEOWNERS and no ruleset.

My reason for "comments only": the file adds no enforcement, and the owner's chat sentence is the real gate either way. If the owner wants a findable pointer, the optional tag is cheaper than a file. Steps 1, 2 and 4 hold in both answers.

## 10 What could not be verified

Checked myself on 2026-11-22 after `git fetch origin`:
- `c2a139552` is an ancestor of origin/master, and `git show c2a139552:docs/designs/orchestrator.md` prints the file; line 3 says "approved by the owner (Clay)".
- `docs/designs/orchestrator.md` is absent on master; the four `orchestrator-mode*` files are present. No CODEOWNERS file exists on master. Tags `archive/pr-682-issue-pipeline-removal` and `archive/pr-684-agent-work-report` exist; the branch `clayphi/archive-orchestrator-655-20261120` head is `d7d645ddd`, the same commit the 684 tag points at.
- Issue 716 is open, has no assignee, and its row S02-F1 says "The design doc is on the archive branch only". Issue 655 is open, assignee clayphi. PR 681 was merged by clayphi; reviews are from the codex and augment bots and clayphi, none from ironbelly.
- SPEC.md FR-68, FR-78 and the S10, S11, S13 rows read as the agents quoted them.

Not verified: Clay's reaction; whether a hook blocks a tag push; whether master branch protection is still off (I relied on both agents' reading of `protected: false`); the D15 line counts (73 and 21, about 94 of 1412) and the 124 conflicting rows (taken from the agents); whose work the four `orchestrator-mode*` files are; DECISIONS.md line 426 "KEEP and RESCOPE" (cited by both agents, not re-read by me).
