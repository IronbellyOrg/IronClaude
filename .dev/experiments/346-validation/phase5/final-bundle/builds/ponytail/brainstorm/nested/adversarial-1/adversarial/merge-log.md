# Merge Log

## Metadata
- Base: Variant B, `variant-2-sonnet-refactorer.md` (sonnet:refactorer, combined score 0.967)
- Executor: merge-executor (claude-opus-5-5)
- Plan: `refactor-plan.md`, changes 1-21 plus change 22 (post-debate correction sent by the coordinator mid-merge; it overrides the in-run placement of changes 2, 9, 18 and 21)
- Changes applied: 22 of 22 handled (18 applied, 2 partial, 2 superseded by change 22, 0 skipped)
- Output: `../merged-output.md` (645 lines, 18 numbered sections, 19 `<!-- Source: -->` tags)
- Status: success, with the partials and executor decisions listed below
- Timestamp: 2026-11-08T15:18:39Z

## Changes

| # | Change | Status | Where in merged output | Provenance tag |
|---|---|---|---|---|
| 1 | Drop the revert channel from every review-3 forecast | applied | s1 prediction, s2.2 first reading bullet, s9.2-9.3, s11, s15.5 | changes 1, 14 |
| 2 | Remove `--apply-audit` and `plan`; row builder inside `apply`; owner approval before S1 | applied | s1, s3.4 step 4, s3.6, s6, s10.1 K11, s12 #3, s15.1 | change 2; consent wording then reshaped by change 22 (`--fix-audit` is the mode flag and the consent; owner approval kept) |
| 3 | Separate `## Fix Audit (review 3 only)` heading, seven bullets byte-identical, no bullet 8 | applied | s1, s3.6, s12 #1(d) and section text, s16.2 T3 | change 3; heading kept literally, its meaning ("fires only in front of review 3") stated in s12 |
| 4 | Brief stored once in `refs/auditor-brief.md`, copied by `prepare` to `D/brief.md` | applied | s3.4 steps 1-2, s4 intro, s12 #4 | change 4, A s5; "the session passes that file's text unchanged" now means: as the Skill argument in the audit session (change 22) |
| 5 | Header lines `auditor:` and `auditor-isolation:` | partial | s4 output block, s5 | change 5; both lines kept, but the isolation value is `own-session` because change 22 removes the subagent and the in-review-session paths that `subagent` and `in-session` described |
| 6 | Upgrades logged `UPGRADE <id>`, ignored | applied | s4 Q1, s6 check.log, s8 step 4, s10.1 K9, s16.1, s16.3 | change 6, A K9 |
| 7 | Rows delete words or restore the aligned baseline span; exact tokens | applied | s4 edit rules, s7 row kinds, s10.1 K10 | change 7 |
| 8 | Naming and accounting; plugin-absent and inline-rubric runs not valid treatment replicates; failures are outcomes | applied | s5, s15.2, s15.3 | change 8, C s1, round2-C O5 |
| 9 | INV-005 review 3 unprimed | partial | s1, s3.1, s3.4, s10.2, s17 #8 | change 9 superseded in part by change 22: INV-005 is solved by the session boundary; kept are the rule that the session reads only exit codes and summary lines (`APPLY_OK reverted=n shrunk=n`, `APPLY_STOP`) and the transcript check, now on the review-3 transcript; "auditor subagent returns only done" not applied (no subagent) |
| 10 | Unattributed hunks kept; no unattributed-revert default, including `--auto-minor` | applied | s4 verdict rules, s6 classes, s10.1 K6, s12 #3, s16.1 | change 10 |
| 11 | Disposition cross-check; no file means no whole revert, `dispositions: none` | applied | s3.4 step 1, s4 header, s6 classes, s7, s16.1 | change 11; executor added the unparsed-`Where` rule (decision D9) |
| 12 | Delete-only keyed on the hunk; restore only in `minor-only` hunks | applied | s4 edit rules, s6 classes, s7, s10.1 K10 | change 12 |
| 13 | Deletions remove only cycle-2 added words | applied | s4 edit rules, s7 delete rows, s10.1 K10, s16.1 | change 13 |
| 14 | Corrected forecasts (P about 3.2, 2.8 to 3.6; (a) 3.1; (b) 3.5; growth 27/26/26%; 427-only P 5.1) | applied | s1, s9.2, s9.3, s11, s15.5 | change 14 |
| 15 | Gate readouts G1-G6 and the falsifier | applied | s15.4 | change 15; G2 matched against fork 2 of change 22 |
| 16 | Paired measurement | applied (reshaped) | s15.1, s15.5, s15.6 F1, s17 cost | changes 16, 22: a fork of the loop folder after the cycle-2 reviser (T08a plus T09 in one, T09 alone in the other) replaces the extra review on `current-before-audit.md` |
| 17 | Baseline sha recorded; must equal saved `spec-v2-after-round1.md` | applied | s3.2, s10.1 K1, s15.3 | change 17 |
| 18 | Bullet-4 exception sentence | superseded | s3.1, s3.6, s12 section text item 1 | change 22: the `--fix-audit` run is not a review run and no review run writes a revised spec, so no exception is needed; s3.6 says so |
| 19 | Early PASS rule | applied | s3.3, s15.3, s16.3 last row | change 19 |
| 20 | Metric definitions (proxy, 427 blocking, reopened findings, no lowering by regrading) | applied | s8 last paragraph, s15.2 | change 20 |
| 21 | Substitution in the review-3 brief only | superseded | s13 | change 22: no review brief changes at all; one inserted Task T08a; s1 and s13 state plainly that a name substitution in T09 cannot work |
| 22 | Audit as its own step (`--fix-audit`), own Task T08a, no subagent, review 3 unchanged, verdict after review 3, forked paired measurement | applied | s1, s3 (all), s4, s5, s6, s8, s10, s12, s13, s15, s16, s17 | change 22 |

## Executor decisions where the plan was silent or a consequence was forced

| Id | Decision | Reason |
|---|---|---|
| D1 | No audit lines in any review report; script-written `D/audit-state.txt` added; K13 compares script-written files and the recorder's sha | change 22 runs T09 verbatim, so no session can add B's report lines |
| D2 | `verdict` writes the `open-blocking:` line itself from review 3's two tables (A s9 parse) and cross-checks it with review 3's verdict line; `--report-rule` (`427` or `any-severity`) reports T09's any-severity line separately | change 22 requires the 427 verdict after review 3 and T09's line reported separately; default keeps B's "never creates a PASS, never lowers a FAIL" |
| D3 | `REVERT_SHARED` id is not closed | A said "still closed as minor"; the base rule (close only when every citing hunk was reverted; INV-023) kept |
| D4 | Reverted text labelled `origin=unchanged`, with the dependent-line caveat | base said "origin=changed minor note"; invariant probe INV-029 marks it a mislabel |
| D5 | Base sentence "passing the original copy as --baseline widens the scope with no code change" dropped | withdrawn in round2-B 1.5; contradicts change 17 |
| D6 | Over-half-unattributed skip guard included | base-selection "From the debate"; round1-B concession 4; change 8 names it |
| D7 | Baseline placeholder renamed `BL` | avoids a clash with variant B and Arm B |
| D8 | A's in-session fallback (no subagent available) not carried | change 22 removes the subagent; the plugin-absent fallback (inline-rubric) is kept |
| D9 | A `Where` cell of a blocking id with no parsable range protects like a missing disposition file | unknowns protect (round2-C s3 item 2); format marked UNVERIFIED (open question 11) |
| D10 | Ablation flag moved to `apply --auto-minor`; the ablation T08a calls the script directly | `plan` removed by change 2; no new command flag |
| D11 | Variant Usage line gains ` [--fix-audit]` | replaces base difference (c) ` [--apply-audit]` |
| D12 | Paired-effect forecast "about minus 0.3 (minus 0.7 to plus 0.1)" | arithmetic from change 14 numbers minus the 3.5 base |
| D13 | Placement (b) defined as triage before the first fix only | round2 convention (round2-B header); base s9 had triage before each reviser |
| D14 | Base s17 "Verification status" not kept as a section | required list has 18 sections; its UNVERIFIED items are marked inline |
| D15 | T08a paths: R2 and baseline from round2-A citations and change 17; spec path left UNVERIFIED | T09 not read in this merge |
| D16 | Section 3 heading made generic ("placement, trigger, steps, consent") | change 22 moves the steps out of the review-3 run |

## Post-merge validation
- **Heading hierarchy:** one H1; H2 sections 1-18 numbered in the required order; H3 subsections numbered within their parents (2.1-2.4, 3.1-3.6, 9.1-9.4, 10.1-10.2, 15.1-15.6, 16.1-16.3); no skipped levels. PASS.
- **Internal references:** every "section N" and "section N.M" reference resolves (checked by grep after the last edit; 2.5 and 16.4 were merged or renumbered and no reference points at them); K1-K13, F1-F5, G1-G6, E1-E12 and Q1-Q12 are all defined where cited. PASS.
- **Tables:** column counts of every pipe table outside code blocks match their header (awk check). PASS.
- **Style:** no em or en dashes (grep count 0); provenance header comments present; every section tagged. PASS.
- **Length:** 645 lines (target 450-650). PASS.
- **New contradictions found (all resolved in the text):**
  1. Change 5 values `subagent|in-session` against change 22 (no subagent): resolved by the value `own-session` (D8, change 5 partial).
  2. Change 2 "no consent flag" against change 22 "invoking `--fix-audit` is the consent": merged; `--fix-audit` is the mode flag and the consent, owner approval still recorded before S1.
  3. Heading "(review 3 only)" against a mode that runs no review: heading kept per change 3, meaning stated in s12.
  4. A's `REVERT_SHARED` closure against the base closing rule: base kept (D3).
  5. "Never lowers a FAIL" against T09's any-severity FAIL: handled by `--report-rule` (D2).
- **Left open, not contradictions:** INV-016 (LOW, a closed id listed open with a PASS) is not in the plan and was not changed; F1 is predicted more likely than not to fire (forecast 3.2 against bar 3), stated in s15.6.

## Summary
- Planned changes: 22 (21 plus change 22)
- Applied: 18 (1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 22)
- Partial: 2 (5, 9)
- Superseded by change 22: 2 (18, 21)
- Skipped: 0
- Executor decisions logged: 16 (D1-D16)
- New contradictions: 5 found, 5 resolved, 0 open
