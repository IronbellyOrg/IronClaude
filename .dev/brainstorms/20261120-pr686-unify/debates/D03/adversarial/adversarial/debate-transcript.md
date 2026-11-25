# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 plus the Round 2.5 invariant probe (standard depth, no Round 3)
- Convergence achieved: 88.9% on diff points; blocked by one HIGH invariant (INV-001)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (V1 = OURS, V2 = CLAY)
- Round 1 advocates ran as two parallel subagents; each read both variants and diff-analysis.md and verified cited facts before use.

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position summary.** Revert PR 682, because it deleted merged, tested work of `ironbelly` (PRs 584 and 591) in 66 minutes. It also removed the only human plan-approval step without a recorded answer to a written question, and nothing replaced the double-start protections. The revert is cheap and returns the repo to the last state the owner approved.

**Steelman of V2.** Clay's design is one system: assignment is the only trigger, the plan is reviewed when the issue is created, and the poller, coordinator and gate are replaced together. The old gate was costly: it needed a person-opened coordinator, a grant row per issue and two sessions per approval (Q36, "latency approved for now"). Its login check cannot tell the owner from an agent on the same login (FU-1 record j, actor `ironbelly`, type `User`). Deleting first lets PR 686 drop the `issue_watch` symbols the package imports without a shim (`orchestrator.md:982`, checked). Clay also scoped the deletion carefully (guard rule 2 stays, a no-`--to` contract bullet, independent guard review PASS) and did ask the owner in writing on issue 450.

**Strengths claimed.**
1. The work is the owner's and recent. PRs 584 and 591 merged 2026-11-17 for decision 6 "Go with B now" (`owner-answers.md:139`, checked). Rows R35 (2026-11-19) and R36 (2026-11-20) show the owner still building on the gate when PR 682 merged.
2. It did run live in part. FU-1 has eleven RECORDED lines a to k on throwaway issue 452 (`issue-pipeline-fu1.md:108-118`, checked). "Never ran live" is true only of the cron watcher.
3. The protections are pinned only by deleted tests: `test_approval_concurrency.py:60` and `:71` (one winner among six racers, checked), `test_approval_crash.py:45`. The replacement is design text (PR B); E-pr682.md line 68 calls equal protection UNVERIFIED.
4. No human approval remains. Rule R1 (`orchestrator.md:73`, checked): "no plan-approval gate after the claim". `hold.py` checks heading presence only (E-pr682.md line 69).
5. The revert is small: 3 of 36 files conflict. The alternative is reworking a 53-file owner branch.
6. The process was one-sided: issue 450 has no reply from ironbelly; issue 655 was filed about 3 hours after the question; PR 682 merged after 66 minutes with no human review.

**Weaknesses identified in V2.**
1. It treats an unanswered question as a ruling (E-pr682.md line 54 finds no ironbelly comment after Clay's, none on 655, 681 or 682).
2. It never names decisions 2, 3, 6 or Q35 to Q38 (E-pr682.md line 81).
3. "Reviewed at creation" is policy, not code. After creation anyone with assign rights can start a worker. Issue 655 marks "assignment is safe" UNVERIFIED; design OQ6 finds two gaps.
4. "The watcher is off" is weaker than it sounds: R18 turns generated configs to `enabled: true`; only the R33 constant `GOVERNED_LEVELS_ALLOWED = False` holds that back.
5. The same-login argument cuts both ways: it was an accepted risk (L-1) and the plan hash, plan-reply-unedited and label-after-reply safeguards reduce it. Deleting everything is not a fix.
6. The removal-order argument is a convenience for PR 686, not a reason to drop the gate.

**Concessions.** Decision 4 (`owner-answers.md:126`) says the owner can correct that reading and Q36 says latency is accepted only "for now". Record f says the G2 session-id lookup "was not attempted", so the live record does not cover G2 or the cron watcher. The dependence on the owner's branch rests on uncommitted local work, not master. The guard comment at `launch-level-guard.sh:496` and the G2 design now disagree, so a revert needs a guard re-review. PR 686 and the restored package cannot both land as written; whether any gate should exist is D01's question. E-pr682.md names rows R9, R17, R24, R33, R34 while V1 cited R19, R22, R24, R29, R35, R36 (V1's were checked).

**Shared assumptions.**
- A-001 QUALIFY: on master the watcher is `enabled: false`; R18 turns it on by default and only R33 holds it back.
- A-002 QUALIFY: the design calls Clay "the owner" while `owner-answers.md` records ironbelly's answers (E-pr682.md line 56, UNVERIFIED); the real owner must say.
- A-003 REJECT: whether a gate exists at all (D01) decides both outcomes; until D01 is decided, restoring the owner-approved state is the safer default.
- A-004 QUALIFY: test presence is all that can be compared, but it is lopsided: the restored code has about 80 tests plus a live record; the replacement has neither.

**Per-point winners (V1 advocate).** S-001 V2 (tie); S-002 V1; C-001 V1; C-002 V1; C-003 V1; C-004 V2; C-005 V2; C-006 V1; C-007 V1; C-008 V1; C-009 V2; C-010 V2; X-001 V1; X-002 V1; A-001 V1; A-002 V1; A-003 V1; A-004 V1.

### Variant 2 Advocate (CLAY)

**Position summary.** Keep PR 682. The design on master (`docs/designs/orchestrator.md:73`, rule R1) removes the post-claim approval gate on purpose and moves plan review to issue creation. A revert would also collide with PR 686. V1 is right that the deletion left a real protection gap and that its process was thin, but that gap is closed by building PR B, not by restoring a package the design has retired.

**Steelman of V1.** PR 682 deleted merged, tested owner work (PRs 584 and 591, decision 6 and Q35 to Q37) in 66 minutes with no human review and without naming those decisions (E-pr682.md lines 8, 81). The old tests pinned one winner on a race, a kill between `worker-start` and `adopt-mark`, and refusal of bot and edited approvals; no code on master has those today (E-pr682.md line 68). "Reviewed at creation" is policy; `hold.py` only checks headings. The "never ran live" claim overstates it (FU-1 eleven RECORDED lines on 452). The revert is mechanically small (3 files).

**Strengths claimed.**
1. The design is internally consistent: R1 at `orchestrator.md:73` (checked in master, pr-a, pr-p snapshots); 7.2 lists the deletion; PR D goes first.
2. The plan-quality check now happens at creation: `sc-issue-protocol/SKILL.md:102` (checked): the worker fills `## Priority`, `## Fix approach`, `## Test plan` at every depth.
3. A revert fails on order: `orchestrator.md:982` says `issue_pipeline` imports `issue_watch` symbols that PR 686 deletes; V1 admits the two cannot both land as written.
4. The same-login hole is real: FU-1 record j shows actor `ironbelly`, type `User`. The gate never separated the owner from an agent.
5. The cost was the owner's own words: Q36 "latency approved for now".
6. The deletion was carefully scoped: guard rule 2 stays, F14 contract bullet added, independent guard review PASS (E-pr682.md line 61).

**Weaknesses identified in V1.**
1. The revert restores a gate the design says must not exist; D01 asks whether any gate should exist and V1 admits the revert is wasted if D01 goes to Clay.
2. Reverting undoes PR 682's separable hardening (no-`--to` bullet, rewritten worker-guard test); V1 itself says those parts are worth keeping.
3. The risk V1 cites for restoring (L-1) is one the gate could not remove: record j shows the actor-type check passes for an agent on the owner's login.
4. The revert puts back about 4,600 lines whose only caller is a disabled watcher (E-pr682.md line 67). "No code on master has the protections" is also true of every approval path while the watcher is off.
5. V1 depends on an unrun rebase of the owner's 53-file uncommitted branch (E-pr682.md line 67 marks UNVERIFIED), and that branch contradicts same-day rulings (cron, approvers).

**Concessions.** "Never ran live" is scope-sensitive: the handoff pieces ran on issue 452 (FU-1 lines 108-118 at `01e7a9e23^`); only the watcher cron never ran. Fact 2 overstates the issue 450 comment: it is a question, and there is no reply from ironbelly; silence is not consent. Fact 7 is weak: the watcher's `flock` gives one winner per cycle, not the per-issue crash-safe adoption row; until PR B exists, equal protection is unverified. The design calls Clay "the owner" while owner-answers records ironbelly's answers (UNVERIFIED if the same person). PR 682 reversed decisions 2, 3, 6 and Q35 to Q38 without naming them: a real process failure.

**Shared assumptions.**
- A-001 QUALIFY: off by default on master; R18 turns it on; only the closed ship gate (R33) holds it back.
- A-002 QUALIFY: D03 needs one identified owner whose decisions bind; the record does not settle whether that is Clay or ironbelly.
- A-003 REJECT: revert vs keep cannot be settled apart from D01 and PR 686; absent a D01 ruling, master's current state is the default.
- A-004 ACCEPT: neither side has run its double-start protection against a real race; PR B's named tests (`orchestrator.md:1108-1112`) are the bar and are not built.

**Per-point winners (V2 advocate).** S-001 V2; S-002 V1; C-001 V1; C-002 V1; C-003 V2; C-004 V2; C-005 V2; C-006 V2; C-007 V1; C-008 V2; C-009 V2; C-010 V2; X-001 V1; X-002 V1; A-001 V1; A-002 V1; A-003 V1; A-004 V2.

## Round 2: Rebuttals

Run sequentially: V1 advocate first, then V2 advocate with V1's rebuttal as input. Facts re-verified by the orchestrator are marked [verified].

### Variant 1 Advocate (OURS) rebuttal

- **Burden.** Conceded in part: if D01 ends assignment-only the revert is moot. But the gate was approved and merged, and PR 682 removed it before D01 was decided, so restoring the last approved state is the default until D01 rules.
- **Separable hardening.** At `01e7a9e23^` WC-17 already said "The worker's `ask` and `send` commands carry no `--to`... the launch-level guard blocks any `--to` from a bound worker" [verified, WORKER-CONTRACT.md line 59]. PR 682 only moved that sentence into its own bullet because deleting WC-17 would have removed it; F14 was a gap the deletion created. The guard-test rewrite was needed only because the test imported the deleted package. The standalone bullet and its test assertion are harmless and worth keeping.
- **Same-login risk (L-1).** Record j shows a known, accepted risk; the gate still blocks bare, edited and plan-hash-changed approvals (records e, k). It shows the gate is not proof against an agent on the owner's login, not that it is useless.
- **"4,600 lines, only a disabled watcher calls them".** 4,599 deleted lines = 2,969 tests + 1,618 src (package 1,597) [verified by `git show --numstat 01e7a9e23`]. The package is reached by the `superclaude issue-pipeline` command a coordinator session runs, so "disabled" does not make it dead.
- **Owner-branch rebase.** Conceded UNVERIFIED (E-pr682.md line 67); V1 does not rest on it. Only 3 files conflict on a revert.
- **New evidence.** PR 681 (the design) merged 2026-11-20T00:02:33Z and PR 682 at 00:02:36Z, both by `clayphi`, 3 seconds apart [verified]. PR 682's only review was one automated `augmentcode` review. The commit message "Nothing ran this code" conflicts with FU-1 records a to k.
- **Hybrid and conditional.** Adopt: the no-`--to` bullet with its test assertion; the creation-time plan sections (independent of the gate); stale-text banners. Not separable: the package, WC-17, guard G2 rule 1 and the approval rows are one mechanism pinned together by the old tests. If D01 ends assignment-only, V1 accepts PR 682 with three conditions: PR B and its named tests exist before the watcher is enabled; the R18 default-on config stays blocked by R33; ironbelly gives a written ruling naming decisions 2, 3, 6 and Q35 to Q38.
- **Final winners (V1 view).** S-001 V2; S-002 V1; C-001 V1; C-002 V1; C-003 V1; C-004 V1; C-005 V2; C-006 V1; C-007 V1; C-008 V2; C-009 V1; C-010 V2; X-001 V1; X-002 V1; A-001 V1; A-002 V1; A-003 V1; A-004 V1.

### Variant 2 Advocate (CLAY) rebuttal

- **Burden.** Concedes. Restoring the last approved state is a defensible default until D01 rules. V2 accepts V1's three conditions (two already hold: watcher off, R33 closed; the third, a written ruling from ironbelly, is the right bar).
- **F14 hardening.** Concedes after checking WC-17 at `01e7a9e23^` line 59: a relocation, not a new protection, so not a V2 benefit.
- **Same-login risk.** Mostly conceded: the gate cannot tell an agent on the owner's login from the owner, but the plan hash and edited-approval refusal did real work; deleting the whole gate is not a fix.
- **Package reach.** Verified that at `01e7a9e23^` only `cli.py`, `main.py`, `WORKER-CONTRACT.md` and the guard hook (`src` and `plugins`) named `issue-pipeline`; no installed skill, command or agent told a coordinator to run it. Supports "unused by default" but V1 is right that it is a live command, not dead code.
- **Timing.** Verified 00:02:33Z and 00:02:36Z, both clayphi. PR 682 had one review (augmentcode); PR 681 had 8 reviews. The deletion followed the design's own plan but its review was thin.
- **Clear separable benefits of V2.** None that V1 cannot adopt. The one remaining benefit depends on D01: if assignment-only wins, a revert followed by a second deletion is about 4,600 lines of churn (a conditional cost, not a defect in V1).
- **If the owner keeps the gate.** Revert PR 682, keep the no-`--to` bullet and its test assertion, re-review the guard (its comment and the G2 design disagree), amend R1 in `docs/designs/orchestrator.md`, sequence PR 686 to leave the `issue_watch` symbols in place or add a shim, leave the creation-time plan sections as an extra layer.
- **New evidence.** `gh api` collaborators on `IronbellyOrg/IronClaude`: ironbelly is the only collaborator with admin; clayphi has `admin=false`. Ironbelly's 2026-11-17T07:09:31Z comment on issue 450 calls the watcher BLOCKED on the owner-run live test; the last comment on 450 is clayphi's 2026-11-18T17:00:32Z proposal with no reply.
- **Final winners (V2 view).** S-001 V2; S-002 V1; C-001 V1; C-002 V1; C-003 V1; C-004 V2; C-005 V2; C-006 V1; C-007 V1; C-008 V1; C-009 V1; C-010 V2; X-001 V1; X-002 V1; A-001 V1; A-002 V1; A-003 V1; A-004 V1.

## Round 2.5: Invariant Probe

Full table in `invariant-probe.md`: 13 findings, 4 ADDRESSED, 9 UNADDRESSED (1 HIGH: INV-001; 6 MEDIUM; 2 LOW). INV-001: a revert of PR 682 and PR 686 (head 8e5ae29ad) merge without a git conflict but produce a broken command line (`superclaude --help` crashes, 29 test modules fail at collection), because PR 686 deletes the `issue_watch` symbols the restored package imports. Neither advocate had raised the "clean merge, broken tree" failure mode; both had said only that the two "cannot both land as written".

## Scoring Matrix

Per-point winners come from the two advocates' final lists (Round 2). Where they differ the orchestrator resolves by evidence and gives a lower confidence; ties go to OURS under the weighting rule given by the owner.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | V2 (tie) | 50% | Identical outlines; no substance. |
| S-002 | V1 | 90% | Both advocates: V1 gives an executable, checkable mechanism (git revert, 3-file overlap). |
| C-001 | V1 | 92% | Both advocates; FU-1 records a to k at `issue-pipeline-fu1.md:108-118`; V2 conceded "scope-sensitive". |
| C-002 | V1 | 90% | Both advocates; protections exist only in deleted tests; replacement is design text. |
| C-003 | V1 | 85% | Both advocates in the end (V2: creation-time plan is the author's own and does not stop a worker). V2 benefit (creation-time sections) kept as extra layer. |
| C-004 | V1 | 55% | Advocates split. Record j proves the gate cannot tell owner from an agent on one login, but it was a recorded accepted risk (L-1) and the other safeguards (plan hash, edited-approval refusal) still work. Slight edge, ties go to OURS. |
| C-005 | V2 | 85% | Both advocates; removal order is real (`orchestrator.md:982`); INV-001 raises its importance. |
| C-006 | V1 | 85% | Both advocates; INV-010 confirms the owner patch applies to the revert tree and not to master. |
| C-007 | V1 | 88% | Both advocates; 66 minutes, one automated review, PR 681 and PR 682 merged 3 seconds apart by one account. |
| C-008 | V1 | 55% | Advocates swapped concessions. Fact: master text still names the removed duty and PR E is unbuilt (V2 conceded). |
| C-009 | V1 | 85% | Both advocates; WC-17 at `01e7a9e23^` already carried the sentence, so PR 682 relocated it. |
| C-010 | V2 | 80% | Both advocates; Q36 and the grant row show a real cost. |
| X-001 | V1 | 92% | Both advocates; scope "never ran live" to the cron watcher. |
| X-002 | V1 | 88% | Both advocates; an unanswered question is not recorded agreement. |
| A-001 | V1 | 85% | Both advocates; R18 contradicts "stays off"; INV-003 shows R33 is not built either, so the true hold is `cycle.py:228`. |
| A-002 | V1 | 88% | Both advocates; ironbelly is the only admin collaborator; owner decisions are recorded under that login. |
| A-003 | V1 | 85% | Both advocates rejected independence from D01; revert is the default until D01 rules; conditional verdict required. |
| A-004 | V1 | 80% | Both advocates; restored code has tests and a live record, the replacement has neither (A-004 by V2 in Round 1, V1 in Round 2). |

## Convergence Assessment

- Points resolved: 16 of 18 by both advocates agreeing on the winner (C-004 and C-008 are split)
- Alignment: 88.9% (16 / 18), including shared-assumption points A-001 to A-004 in the denominator
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (11 points) and L3 (C-001, C-002, C-004, C-009, A-001, A-004) all addressed; no forced round needed
- Invariant gate: BLOCKED_BY_INVARIANTS (INV-001, HIGH, UNADDRESSED); no Round 3 at depth standard
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement above threshold). Unresolved points: C-004, C-008 (resolved by the orchestrator in the matrix above)
- Shared assumptions A-001 to A-004: both advocates answered every one (A-001 QUALIFY, QUALIFY; A-002 QUALIFY, QUALIFY; A-003 REJECT, REJECT; A-004 QUALIFY/ACCEPT). No [OMISSION] flags.

