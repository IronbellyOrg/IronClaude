# X15 (OA-1): Do both approval gates stay? Final reconciled proposal

Reconciler read A-0, B-0, A-3 and B-3 on 2026-11-22 and checked the key claims against origin/master `2ea524514`. This is a recommendation until the owner says it in chat. Hours are estimates with their basis.

Plain words. START gate: the issue field `Approved` set to Yes and unedited since, plus a Status in the allowed list (Research, Spec, Plan, Debug). PLAN gate: after the claim, the worker writes a plan, the owner approves it in chat, and only then does `release-worker` let the worker edit (rule WC-17, `issue-pipeline check-approval`, `release-worker`).

## 1 Unified proposal
Answer: both gates stay. Clay's PR 700 stands as the restored state. No removal PR. No code change for OA-1.
Order:
1. The owner says the sentence in section 7. Silence is not a yes.
2. An agent records it in local brainstorm files only (section 8).
3. A review happens at the earliest of: 2026-12-22 (a Tuesday), the first live watcher run, or before any launch level above Pipeline None (the claim-only level) is switched on.
4. If the owner says nothing at the review, both gates stay. A date never removes a gate.
5. The review is a chat question with counts (plans asked, approved, refused, wait time). Outcomes: keep both; narrow the plan gate to stages that edit code (needs its own check of the guard's edit and turn classes plus an independent guard review); or remove it through a new PR opened with `/sc:pr-submit --monitor 3`. Remove only on a measured "no protection and real delay".
Docs must call the plan gate a seatbelt against honest mistakes, not a lock, because the owner and agents share one GitHub login (accepted limit).

## 2 Context
OA-1 is the owner-only question on the list. Clay's PR 700 (merged 2026-11-20T15:07:32Z, gh read) rolled back the orchestrator build including PR 682, so the plan-approval package is already back on master without the owner's answer (SPEC Appendix B.3 item 4, line 789, says to answer after the fact). Decision D01: assignment alone never starts work. Decision D03: revert 682 if both stay. SPEC 8.3 (line 505): "only the start gate" now means a new removal PR. Clay's issue 450 comment of 2026-11-18 wants assignment alone as the trigger, so Clay may disagree.

## 3 Implications
Changes: only local records (DECISIONS.md OA-1 line 1237 and X-19 line 1411 become answered; SPEC 8.3 marked "branch not taken"; STATE.md and the S17 go/no-go list gain three lines). FR-31 stands; S6 and S7 stay "done by PR 700".
- Master code: unchanged. Watcher: unchanged (off by default, `cycle.py` line 235; governed levels skipped, line 1036). Coordinator: keeps adopt, plan ask, check-approval, release-worker, complete. Dashboard: shows two approval states per issue.
- Issue 698 (guard reads words, assignee shortcut): stays open and live. STOP line on the S17 list: no launch level above None until the owner has chosen an option in chat. Advice: (b) `release-worker` refuses without an approval row, with tests; (d) docs only is allowed only until the flip.
- Issue 699 (claim worktree has no agent): independent of the gates. Owner chooses before the first live claim. Default: the documented exception, one rule sentence plus one pin test.
- Stays blocked: any launch level above None; any post on issues 450, 698, 699 (a draft reply to Clay waits for the owner's go).

## 4 Benefits
Nothing built is thrown away. The narrow worker level (W, then WA after release) is kept; removal would bind workers wider (F). The decision is in the owner's words and matches decision 6 = B. A later removal needs a reviewed PR with real data. Nothing changes today because nothing runs live.

## 5 Risks and containment
- Friction at the first live run: the review measures it.
- False confidence in a text-based gate: seatbelt wording, ship gate closed, STOP line on 698.
- Two approvals become a rubber stamp: the review counts refusals.
- Clay disagrees: draft reply only; the owner decides.
- The review date lives in a ledger and can be forgotten: backed by the S17 line and the ship-gate trigger.
- The record shows PR 700 acted before the answer: say so plainly in the entry.

## 6 Costs (estimates)
- Owner: about 1 minute (one sentence).
- Agent recording: 0.5 to 1 hour (basis: small edits in DECISIONS, SPEC, STATE and the S17 list).
- Review: 1 to 2 hours (basis: reading counts and one chat answer).
- 698 option (b): 2 to 5 hours (basis: one function, one store lookup, 3 to 4 pin tests). Option (d): near 0.
- 699 exception: about 1 hour (basis: one sentence and one test).
- Branch "only the start gate": 10 to 20 hours plus an independent guard review (basis: PR 682 was 36 files and about 4,600 lines per D03; add moving `complete.py` and a rebase onto an untried tree). SPEC RK-4 puts confidence near 50 percent.

## 7 The sentence the owner says in chat
"OA-1: both approval gates stay. My approval starts the work, and my approval of the plan, given in chat and recorded by the agent, lets the worker edit. PR 700 stands and no removal PR is opened. We review both on 2026-12-22, or after the first live watcher run, or before any launch level above Pipeline None is switched on, whichever comes first. If I say nothing at the review, both gates stay."

## 8 What an agent does after it
Local files only, no GitHub write, nothing for the owner to write.
1. Record the quoted words, date and recorder in DECISIONS.md at OA-1 and X-19; mark both answered; state that PR 700 acted first.
2. Mark SPEC 8.3 "branch not taken" (keep the text); update Appendix B.3 item 4.
3. Add to the S17 list and STATE.md: (a) STOP on 698 as above; (b) 699 chosen before the first live claim; (c) the review held, or its date and triggers not yet reached.
4. Add the seatbelt wording to the docs.
5. Draft, do not post, the reply to Clay on issue 450.

## 9 Consensus
Full. A and B agree on the answer, sentence, triggers, silence rule, review date, hard stop and costs. Residual for OA-1: none. Two later choices are scheduled, not open here, and are asked in chat from the S17 list:
- 698: (b) a real lock against the worker's own mistake, 2 to 5 hours, my pick; (d) free, but the lock rests on text match, so governed levels stay off.
- 699: keep the documented exception (about 1 hour, fastest); or change the claim script to create the worktree with an agent (follows the rule exactly, larger change).
Independent call: I keep all three review triggers. The first-run trigger gives little plan-gate data at level None (plan ask is a wait there, not a lock), so that review can be short.

## 10 Not verified
- Whether the Orca hook sees a script's inner `orca` call (699).
- What the guard's edit and turn classes cover in detail (needed before "narrow the plan gate").
- Whether PR 707 equals the owner's planb branch; whether Clay accepts both gates.
- Whether a second GitHub account for a real lock (698 option c) will be provided.
- The watcher default-off line number on current master was checked (line 235); the D03 citation of line 228 is stale.
Checked by me: `GOVERNED_LEVELS_ALLOWED = False` (launch.py line 48); `release()` tests no approval record (release.py); guard lines 804 to 809 deny edits at W and allow at WA, F, FS; issues 698 and 699 open with no assignee; PR 700 merged; 2026-12-22 is a Tuesday.
