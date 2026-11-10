# Round 2 (rebuttal), advocate A (variant-1-opus-architect)

## 1. Response to criticisms of A raised in round 1

1. **Revert channel contradicted (B weakness 1).** Conceded in round 1 and kept conceded. The class-A share is 0.17 per run over all six runs (`evidence-attribution.md`, Totals). A's 2.5 is withdrawn; see section 5.
2. **N5 to N12 is class C, not a deletion win (B weakness 2, C weakness 1).** Conceded. Two readers against one. The deletion principle now rests only on the seven class-B remedies, all of which the attribution file names as deletions.
3. **MAJOR may be downgraded and whole-reverted (B weakness 3, C weakness 2).** Conceded and fixed by adopting B's rule (X-002): no whole revert of a hunk that cites a report-blocking id. With that rule, A's `closed_minor` set holds only ids the report itself graded minor, so C's concern (a wrongly downgraded blocking fix hidden from the verdict) can no longer arise through A's verdict formula.
4. **Fixed table columns are fragile (B weakness 4).** Conceded. Take B's `open-blocking:` line as the primary input and A's table parse as a cross-check; if the two disagree, the verdict is FAIL (B's own C-009 merge).
5. **Hunk attribution cannot separate minor from blocking text (C weakness 4).** Partly conceded. `minor-byte-share.md` limits whole-hunk reverts to 6% and 27% of added characters. Counter: the lever the evidence supports does not need that separation. A deletion-shrink row inside a `blocking-involved` hunk only has to (i) delete words and (ii) keep every blocking id on the hunk. Attribution limits reverts, not shrinks.
6. **A reinterprets "never re-reviewed" (C weakness 5).** Partly conceded: under P, review 3 reads the shrunk text, so the edits are seen, though the audit's grades are never regraded. That is an owner call. But the literal reading costs the registered metric (C concession 1) and ships edits nobody read (C concession 4). P is the only placement that runs once and still lets the metric move.

## 2. Updated assessment of B and C

- **B** moved to the right place. Its revised 3.3 drops the revert channel, and its three repairs are good and cheap: the fail-open guard when more than half the hunks are unattributed (B concession 4), letting a shrink row drop a validated-minor id (concession 3), and asking Q2 (is there a smaller fix) before Q1 (concession 6). A adopts all three. B's `--auto-minor` ablation is sound diagnostics but costs two more runs at n = 2; keep it optional. B and A now differ mainly on the shrink rule (O2) and on 0.4 of a finding in forecasts.
- **C** conceded its placement cannot move the raw count, withdrew its numbers, and accepted B's blocking-revert ban. C remains the best source for naming (never call a terminal count "review 3") and for the edge-case test list (U-006); both go into the merge. C's both-cycle ledger and fail-closed plugin rule remain rejected: C itself says the ledger is "not free instrumentation" and may cost more than it saves (C concession 5), and section 3 below shows cycle 1 adds little that a P audit can reach.

## 3. New evidence not presented in round 1

1. **Cycle-1 fixes breed most review-2 blocking findings in the 427 runs.** The review-2 reports tag origin per finding. flg-r1 R2-1 to R2-4 are all "changed" (`exp346-ab-flg-r1/.../review/spec-panel-round2.md:145-148`); flg-r2 N1 to N6 are all "origin=changed" (`exp346-ab-flg-r2/.../spec-panel-round2.md:95-125`); trt-r2 N1 to N7 are all "origin=changed" (`exp346-ab-trt-r2/.../spec-panel-round2.md:174-180`); trt-r1 N1 to N5 are "origin=changed" and F2, F5, F8 are reopened (`exp346-ab-trt-r1/.../spec-panel-round2.md:13,157-161`). Total: 22 of 25 review-2 blocking findings sit on cycle-1-changed lines. The control run ctl-r2 says only N1, N2 and part of N5 were "Introduced by the revision" (`exp346-ab-ctl-r2/.../spec-panel-round2.md:236`). Caveat: "changed" is a location tag, not a smaller-fix judgement. No class-B rate for review 2 has been measured (UNVERIFIED).
2. **Review-3 defects anchor on cycle-2 fixes.** From the tables in `evidence-attribution.md`: 7 of 7 class B and about 10 of 12 class C anchor on cycle-2 fixes. The exceptions are ctl-r2 R3-2 (F7, F4) and trt-r2 R3-3 (partly F8, F1).
3. **Class C scales with the number of cycle-2 blocking fixes.** Cycle-2 blocking rows per run are 9, 7, 8, 7, 4, 6 (41 in total; `evidence-attribution.md`, cycle-2 lines). R3 class B plus C per run is 5, 3, 4, 3, 3, 1 (19). That is about 0.46 R3 blocking findings per cycle-2 blocking fix, and 0.4 in the flg arm (4 of 10, over critical+major). This is the only route by which any audit touches class C: fewer review-2 blocking findings mean fewer cycle-2 fixes.
4. **All seven class-B remedies pass a word-subsequence test or are a revert to v2 text.** "delete the attribution and the word 'documented'", "delete two clauses", "delete 'only'", "delete the closed allow-list", "delete 'report goes there too'" are pure deletions. trt-r1 R3-4 reads "drop the resume exception or keep v2 wording", which is a deletion or a baseline revert. ctl-r2 R3-1 "drop guard case (1)" may leave a numbering or plural word that a strict subsequence check rejects; that row would SKIP (fail open), not corrupt.

## 4. Positions on the three open points

**O1. Placement to run. Winner: merge: run P now (A and B); pre-register (a) as the next run, triggered if P's mean exceeds 3.**
The attribution file is right that class C (2.0 per run, the largest class) is out of reach of P: a necessary fix cannot be shrunk away. But (a) does not reach it directly either. It reaches C only by shrinking cycle-1 fixes so that review 2 raises fewer blocking findings and cycle 2 makes fewer fixes. Evidence item 1 shows the pool is real (22 of 25 review-2 blocking findings on cycle-1 text), but the share a smaller cycle-1 fix would avoid is unmeasured. If it matches review 3's 25% and the audit captures half, the flg arm loses about 0.6 review-2 blocking findings and therefore about 0.2 review-3 findings (section 5). That gain is below the two-replicate spread (Arm B: 6 and 1). Against that, (a) breaks both parts of the owner's goal: it runs twice, and audit 1's edits are reviewed by review 2. P keeps the goal, isolates the shrink channel so the next decision is readable, and in A's architecture (a) is a one-condition change in bullet 8 with the same script, so nothing is lost by sequencing.

**O2. Shrink rule. Winner: A (deletion-only: new text is a word subsequence of old), plus restoring baseline spans, which are already reverts.**
Deletion-only reaches all seven class-B remedies (evidence item 4), so it gives up none of the measured lever. It is also the safer rule. A free shorter rewrite can write a new claim, and a new claim written by a fix is exactly the class-C mechanism that dominates review 3. A deletion can still change meaning (removing "only" widens a rule), and review 3 reads it, but it cannot introduce a fact nobody checked. It is also script-checkable in a few lines (compare words, ignoring case and punctuation), where "shorter" leaves the content judgement to the model. A row that fails the test SKIPs, so the worst case is plain 427 for that hunk.

**O3. Scope. Winner: A and B (cycle-2 only for P).**
Under P, cycle-1 text has already passed review 2. Cycle-1 minor-only hunks are 6% of cycle-1 added characters, about 1.3 growth points (776 of 57,763 bytes, `minor-byte-share.md`), and no class-B anchor sits on a cycle-1 fix (evidence item 2). Widening scope would add review-3 surface for almost no reachable gain. Architect note: define scope as "fixes since the last audit". Under P that is cycle 2; under (a) each audit covers its own cycle, so both cycles are covered with no new parameter and no ledger.

## 5. Final predicted numbers (Arm B base: R3 critical+major mean 3.5, growth 30.0%)

| Placement | R3 critical+major mean | Growth after two cycles |
|---|---|---|
| P | 2.9 (2.5 to 3.4) | 26% (24 to 28) |
| (a) | 2.7 (2.2 to 3.2) | 23% (20 to 26) |
| (b) | 3.4 (2.9 to 4.0) | 26% (23 to 28) |

- **P, R3:** 3.5 minus 0.25 (half of the 0.5 class A, reverted when its hunk is minor-only) minus 0.5 (half of the 1.0 class B, by deletion-shrink) plus 0.15 new surface (lower than round 1's 0.3 because deletions add no claims) = 2.9.
- **P, growth:** 30.0 minus 3.0 (cycle-2 minor-only hunks, measured in flg-r2) minus 1.0 (deletion-shrinks of blocking text) = 26.
- **(a), R3:** P minus 0.6 fewer review-2 blocking findings (5 per run x 25% assumed avoidable x 50% captured) x 0.3 marginal R3 per cycle-2 blocking fix once the second audit has taken its share of B = 2.7.
- **(a), growth:** P minus 1.3 (cycle-1 minor-only hunks) minus 1.0 (cycle-1 shrinks) minus 0.8 (0.6 fewer cycle-2 fixes at about 760 characters each) = 23.
- **(b), R3:** triage prevents cycle-1 minor fixes, which anchor 0 of the flg arm's review-3 critical+major findings and 1 of 28 overall, and leaves cycle 2 alone: 3.5 minus 0.1 = 3.4.
- **(b), growth:** cycle-1 minor text is between 6% (minor-only hunks) and about 40% (equal-bytes estimate) of the 19.6-point cycle-1 increment; at about 20%, 30.0 minus 4 = 26.

Chance P meets the mean bar of 3: about 50%. Every number rests on n = 2 and on judged classes, and assumes reviewers do not find replacement findings (UNVERIFIED).
