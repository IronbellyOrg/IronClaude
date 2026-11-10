# Round 2 (rebuttal), advocate B (variant-2-sonnet-refactorer)

Convention: P = the owner's single audit after cycle 2 and before review 3. (a) = an audit after every fix cycle. (b) = triage of findings before the first fix cycle (A's round-2 meaning). Arm B base = flg arm: review-3 critical+major mean 3.5 (runs 6 and 1), growth 30.0%.

## 1. Response to criticisms of B

1. **B's forecast rested on the revert channel (A, C).** Conceded in round 1 and kept. The channel is worth about 0.2 per run (`evidence-attribution.md`, Totals). B's 2.4 stays withdrawn; section 5 has new numbers.
2. **The audit has almost no say in the verdict (A weakness 2).** Counter: that is the design, not a defect. A script that can neither create a PASS nor lower a FAIL cannot ship a false PASS, and the attribution file warns that "every B/C revert reopens a blocking finding". A has now adopted the same rule (A round 2, 1.3). Keep.
3. **More surface than A: `plan` step, `--apply-audit`, three report lines, K5 severity parse (A weakness 3).** Conceded in part. `--apply-audit` goes (O4). `plan` folds into `apply` (the row builder is a function, not a subcommand). The report lines shrink to `open-blocking:` and `audit:`. K5 is rewritten after the format finding in section 3 (item 2).
4. **"Cannot corrupt the spec" is too strong (C weakness 3).** Conceded as worded. The true claim is narrower: the script cannot change any text outside the rows it lists, and every row is checked mechanically. A valid but wrong shrink is still possible, and review 3 is the net for it. I will say that in the design text.
5. **Cumulative-baseline shortcut does not recover cycle-1 attribution (C weakness 6).** Conceded, and it is worse than C said. My round 1 claim that passing the original copy as `--baseline` widens scope "with no code change" is wrong: the script reads severity from the review-2 report only, so cycle-1 ids are `foreign-id` hunks and stay protected. Widening needs report 1 as a second input. Withdrawn.
6. **"Never re-reviewed" is reinterpreted (C weakness 5, A round 2 item 6).** Not a factual dispute. Under P review 3 reads the shrunk text, so no edit ships unread. Whether that satisfies the owner's words is the owner's call; I flag it in O1.
7. **`--auto-minor` ablation costs two more runs at n = 2 (A round 2, 2).** Accepted: optional, run only if P misses. It has no auditor call, so it is the cheaper of the two follow-ups.

## 2. Updated assessment of A and C

- **A** has converged on most of B: no whole revert of report-blocking hunks, the `open-blocking:` line, the fail-open guard, Q2 before Q1. What remains is the deletion-only rule (O2) and the capture rate for class B. A's P figure of 2.9 assumes an auditor finds half of the class-B defects. The seven class-B remedies are the review-3 reviewers' own words, written after they saw the defect. A pre-review-3 auditor has no such text. I use 35%, not 50% (section 3, item 4).
- **C** conceded placement, numbers, ledgers, and the FR-8/FR-9 override. Two things remain worth taking: the naming rule (never call an audit-computed count "review 3") and the U-006 edge-case table as the test list for `apply`. C's both-cycle ledger and fail-closed plugin rule stay rejected.

## 3. New evidence, and checks of A's round-2 items 1-4

New measurements (my own re-run of `enrichment/minor_share.py`'s method on cycle 2, v2 to v3, read-only on each run's `specs/history/`; id sets per run from `evidence-attribution.md`; the id regex is crude and nothing was hand-checked, so treat as indication):

| run | added chars | minor-only | blocking-involved | untagged |
|---|---|---|---|---|
| flg-r1 | 6,950 | 2,285 (33%) | 4,217 (61%) | 448 (6%) |
| flg-r2 | 6,301 | 1,726 (27%) | 4,575 (73%) | 0 |
| trt-r1 | 6,847 | 660 (10%) | 6,156 (90%) | 31 |
| trt-r2 | 8,064 | 842 (10%) | 7,222 (90%) | 0 |
| ctl-r1 / ctl-r2 | 20,544 / 22,126 | 0 | 0 / 1,359 | 28 of 28 and 29 of 30 hunks untagged |

1. **flg-r1 is attributable in cycle 2.** `disposition.md` uses bare numbers, but cycle 2 cites `R2-n` in the text, and only 5 of 20 hunks (6% of bytes) are untagged. This settles A-002 for the cycle P works on. The flg mean minor-only share is 30%, which is 3.96 and 2.99 growth points, mean 3.5. That is above the 3.0 every round-1 note used.
2. **Severity is written four ways in four 427 reports.** flg-r1 uses table cells `| MAJOR | blocking |` (`spec-panel-round2.md` near line 145), flg-r2 uses prose `CRITICAL, blocking, origin=changed` (near line 95), trt-r1 `Severity MAJOR, blocking (guard GAP G4)`, trt-r2 `MAJOR, B, origin=changed` with a grade key. One regex will not do. Repair for K5: a tolerant per-line token search, and any id whose grade cannot be read is treated as blocking (protected, never reverted). Log the unknown rate; test on the four formats.
3. **The fail-open guard is not hypothetical.** The control runs cite no ids at all, so the "more than half unattributed, skip" guard fires on both. They are free fixtures for that test (the controls are not the Arm B base).
4. **trt arms: the revert channel is only 10% of cycle-2 bytes.** Without the re-review flags, minor fixes are fewer, so the audit pays less. This supports building for the flg base only.

Checks of A's round-2 items:

- **A1 (22 of 25 review-2 blocking findings on cycle-1 changed lines): holds as a count, fails as a cause.** I read the flg-r1 table, flg-r2 N1-N6, trt-r1 N1-N5 and trt-r2 N1-N7: all tagged `origin=changed`. But the tag means "a line the revision touched". ctl-r2 round 2 (line 236) lists only N1, N2, N12, N15-N17 and part of N5 as introduced by the revision and says "the rest pre-date it". trt-r1 N4 and trt-r2 N4 (the `grep -E '^-[^-]'` filter) are v1 text that moved. So it is a pool of touched lines, not a pool a smaller fix would have avoided.
- **A2 (7 of 7 class B and about 10 of 12 class C on cycle-2 fixes): holds.** I recounted from the tables; the two C exceptions are ctl-r2 R3-2 and trt-r2 R3-3.
- **A3 (41 cycle-2 blocking rows, 19 R3 B+C, 0.46 per row; flg 0.4): arithmetic holds, weak as a rate.** Per run it runs from 0.17 (flg-r2, 1 of 6) to 0.75 (flg-r1, 3 of 4), and four of six runs are control or pre-flag text. It cannot fix a marginal figure for (a).
- **A4 (class-B remedies pass a word-subsequence test): mostly holds, with a gap.** Five of seven are named deletions in the attribution file. trt-r1 R3-4 says "keep v2 wording", which is a restore, not a subsequence. ctl-r2 R3-1 may fail the test (A says so). And the test shows a deletion fixes it, not that an auditor would nominate it before review 3.

## 4. Positions on the open points

**O1. Placement to run. Winner: merge: run P now; pre-register (a), but trigger it on an anchor readout, not on the mean alone.**
P is the owner's single audit and the only placement that runs once and lets the registered metric move. (a) does not reach class C (2.0 per run, the largest) except through fewer cycle-2 fixes, and that gain (about 0.1) is far below the Arm B spread of 5 between its two runs. A mean test of "exceeds 3" will fire about 60% of the time on noise alone given my P forecast of 3.1. So: run (a) next only if the same A/B/C/D reader finds that at least a third of P's leftover critical+major anchor on cycle-1 text; otherwise run the no-model ablation. The owner should decide whether "review 3 reads the shrunk text" meets "never re-reviewed"; the audit's own grades are never re-graded.

**O2. Shrink rule. Winner: merge: a row may only delete words, or restore a span of the baseline text.**
Deletion-only (A) is right that a free rewrite can write a new claim, which is how class C is made. But it cannot express "keep v2 wording" (trt-r1 R3-4) and it cannot undo a minor fix that changed a word inside a mixed line, which is where the byte-share evidence says the remaining 70%-plus of minor bytes sit. A baseline span adds no claim: a reviewer already read it in review 2. Both checks are mechanical (word subsequence, or exact substring of the baseline). A row whose old text holds a report-blocking id may only delete, and must keep that id. A failed check SKIPs the row, so the floor is plain 427.

**O3. Scope. Winner: A and B, cycle 2 only.**
All seven class-B anchors are cycle-2 fix text, cycle-1 minor-only hunks are 776 chars (1.3 growth points), and severity for cycle-1 ids is not in report 2 (section 1, item 5). Widening needs a second report input for almost no reachable gain. Under (a) each audit covers its own cycle, so no scope parameter is needed.

**O4. Consent flag. Winner: A (pure one-line name substitution; drop `--apply-audit`).**
The coordinator that writes `/sc:spec-panel-ponytail --re-review` has already chosen a command whose documented job is the audit. A flag repeats that choice, changes Arm B's bytes by two tokens, and adds a no-flag dry-run branch the experiment never exercises. Safeguards stay without it: the pre-audit copy is saved, the sha guard holds, edits are limited to diff hunks, and `apply-log.md` records what ran. This depends on the owner accepting that choosing the command is consent (my round-1 Q1); if the owner says no, the flag returns.

## 5. Final predicted numbers (Arm B base: 3.5 and 30.0%)

| Placement | R3 critical+major mean | Growth after two cycles |
|---|---|---|
| P | 3.1 (2.6 to 3.7) | 27% (25 to 29) |
| (a) | 3.0 (2.5 to 3.7) | 26% (24 to 28) |
| (b) | 3.4 (2.9 to 4.0) | 26% (23 to 28) |

- **P, R3:** 3.5, minus 0.3 (class A 0.5 times 60% of those hunks being minor-only and reverted), minus 0.35 (class B 1.0 times 35% nominated in advance), plus 0.25 (deletions that change meaning, restored baseline text, replacement findings) = 3.1. Chance the mean is 3 or lower: about 40%. Per run, r1 stays near 5 and r2 near 1.
- **P, growth:** 30.0, minus 2.5 (70% of the measured 3.5-point mean minor-only share actually reverted), minus 0.8 (deletion shrinks of blocking text, unmeasured) = 26.7, so 27%.
- **(a), R3:** P minus 0.13 (5 review-2 blocking findings times 25% times 35% capture, times 0.3 R3 per cycle-2 fix) = 3.0. Replacement findings in review 2 are ignored, so this is the upper edge of the benefit.
- **(a), growth:** P minus 0.9 (cycle-1 minor-only 1.3 points times 70%) minus 0.4 (cycle-1 shrinks) = 25.7, so 26%.
- **(b), R3:** triage stops cycle-1 minor fixes, which anchor 0 of the flg arm's critical+major findings and 1 of 28 overall, and leaves cycle 2 alone: 3.5 minus 0.1 = 3.4.
- **(b), growth:** cycle-1 minor share taken at 20% (between 6% by hunk and about 43% by row count) of the 19.6-point cycle-1 increment = 3.9, minus 0.4 knock-on = 25.7, so 26%.

All numbers rest on n = 2 per arm, judged A/B/C/D classes, and the unverified assumption that reviewers do not find replacement findings. The ordering P below 3.5 is more reliable than the size of any gap between P, (a) and (b).
