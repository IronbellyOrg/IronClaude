# Evidence attribution: which fixes produced the review-3 blocking findings (issue 346)

Read-only analysis of six recorded loops of scenario S1 (spec reviewed by /sc:spec-panel 3 times, 2 fix cycles).
Runs: ctl-r1, ctl-r2 (control, pre-427 text); trt-r1, trt-r2 (427 text); flg-r1, flg-r2 (427 + re-review flags).
Sources per run: `<run>/.dev/orca-command-refactor/review/*.md`, `specs/history/*.md`,
`<run>/.dev/experiments/346-validation/phase4/<short>/metrics.json`. Nothing in the run folders was edited.

Conventions:
- "R3 blocking" = review-3 findings graded CRITICAL or MAJOR, or marked blocking. In control runs blocking = MAJOR.
  In flg runs the reports grade blocking separately, so CRITICAL+MAJOR can exceed blocking; both are given.
- A = anchored on a fix of a MINOR finding; B = anchored on a fix of a BLOCKING finding where a smaller fix would
  have avoided it; C = anchored on a blocking fix where a smaller fix would not have avoided it; D = unchanged or older text.
- "Revert" = would the R3 anchor text disappear if the earlier fix were reverted to its pre-fix text.
- Every A/B/C/D assignment, revert answer and smaller-fix answer is a JUDGEMENT unless the report's own text states it.
- UNVERIFIED marks a point the files do not settle.

Method: the metrics numbers were copied with jq. The row-level attribution was done by one read-only reader per run,
which compared the cited v3 lines against v2 and v1 with grep (no full diffs) and matched them to the disposition
"Where" column. v1 for the control and trt runs is taken as identical to `exp346-ab-flg-r1/.../spec-v1-draft.md`.
The metrics give 57,763 bytes as every run's v1 size. The sha256 match is recorded only for ctl-r2, flg-r1 and flg-r2.

## ctl-r1 (control)
- Metrics: R3 `rounds[2].M2.critical_plus_major` = 8 (= `blocking` 8). Growth `rounds[0].M4.growth_percent_this_round` 23.83
  (57,763 -> 71,528 B), `rounds[1].M4.growth_percent_this_round` 27.37 (-> 91,102 B), cumulative
  `spec_sizes.growth_percent_vs_v1.after_round2` 57.72.
- Cycle 1: 19 rows, 11 blocking (#1-11), 8 minor (#12-19), 8/8 minor applied (disposition.md:14-32).
- Cycle 2: 17 rows (N1-N9 blocking, M1-M6 minor, plus citation rows C-14 and C-40 graded minor). 8/8 minor rows applied (disposition-round2.md:17-33).

| R3 id | origin | earlier fix (grade) | revert removes anchor? | smaller fix avoids? | class |
|---|---|---|---|---|---|
| R3-1 | changed (2.4 table, "is total" claim v3:64,78 new) | N1 (blocking) | yes | no: recommend's `clarification_needed`/`degraded` stay unmapped; rows needed to be added | C |
| R3-2 | changed (v3:88,333 attribution to "tasklist's reflect gate") | N2 (blocking) | yes | yes: delete the attribution and the word "documented" (the review's own remedy, round3:174) | B |
| R3-3 | changed (`find -newer` v3:227) | N3 (blocking) | yes | no: N3 required catching gitignored writes; needs an allow-list | C |
| R3-4 | unchanged (AC-2.2 text identical v1:200, v2:211, v3:245) | none | no | n/a | D |
| R3-5 | changed (verbatim block, P0 sentence v3:75,179) | N6 (blocking) | yes | no: dropping the block loses the Skill-call duty AC-0.4 needs | C |
| R3-6 | changed (D6, "only confirms", v3:175,179) | N7 (blocking) | yes | yes: delete two clauses, keep section 9's 0-3 gate | B |
| R3-8 | unchanged (`master...HEAD` in v1:176,193) | none (N8 kept it) | no | n/a | D |
| R3-9 | older text (v1:194 "existing report file") | #12 (minor) extended it into step 3 | no | n/a | D (alt. A) |

- Summary: R3 blocking 8 = A 0 + B 2 + C 3 + D 3 (A 1 + D 2 if R3-9 is read as anchored on #12). All classes are judgements.
- UNVERIFIED: v3:179 is listed under both N6 and N7, so which fix wrote the "only confirms" clause is not settled.

## ctl-r2 (control)
- Metrics: R3 `rounds[2].M2.critical_plus_major` = 4 (1 CRITICAL + 3 MAJOR). Growth `growth_summary_for_D6b.step_growth_percent`
  R1_revise 31.9 (-> 76,214 B), R2_revise 28.3 (-> 97,814 B); cumulative
  `growth_summary_for_D6b.this_arm_growth_after_two_fix_cycles_percent_bytes` 69.3.
- Cycle 1: 21 rows, 12 blocking (F1-F12), 9 minor (F13-F21), 9/9 minor applied (disposition.md:25-45).
- Cycle 2: 17 findings (N1 CRITICAL, N2-N7 MAJOR, N8-N17 minor) + 4 citation rows. 10/10 minor applied, and the citation rows were applied with N15/N5/N2/N16.
  One sub-point inside N5 was not adopted (disposition-round2.md:24-50,57).

| R3 id | origin | earlier fix (grade) | revert removes anchor? | smaller fix avoids? | class |
|---|---|---|---|---|---|
| R3-1 CRIT | changed; report: "Introduced by the N4 fix" (round3:190) | N4 (blocking); clashes with F4's AC-0.4 (blocking) | yes | yes: drop guard case (1) and the 2.3 "exactly when" coupling | B |
| R3-2 | report: "Not raised before ... pre-dates both revisions" (:191,198); reader: master counts first appear in v2:82,92-93 | F7 (blocking); AC-1.1 clause from F4 (blocking) | partly | no: the defect is a missing fact (31 commands already converted) | C (D by report tag) |
| R3-3 | mostly unchanged; report: "Residual of N6" (:192); holes exist in v1:185 | N6 (blocking); commit half leans on N10 (minor) | no | no: the holes come from text that was never written | D |
| R3-7 | changed; report: "Introduced by the N4 fix" (:196) | N4 (blocking) | yes | no: closing it needs skill-file coverage added | C |

- Summary: R3 blocking 4 = A 0 + B 1 + C 2 + D 1 (C 1 + D 2 by the report's own tag on R3-2). Judgements.
- UNVERIFIED: the R3-2 origin. The report's "pre-dates both revisions" disagrees with v1 having no master text.

## trt-r1 (427 text)
- Metrics: R3 `rounds[2].M2.critical_plus_major` = 6. Growth `rounds[0].M4.growth_percent_this_round` 11.64 (-> 64,488 B),
  `rounds[1].M4.growth_percent_this_round` 10.27 (-> 71,113 B); cumulative
  `growth_summary_for_D6b.this_worktree_growth_after_two_fix_cycles_percent` 23.11.
- Cycle 1: 17 rows (F9 is a pointer merged into F1), 9 blocking (F1-F8, F10), 7 minor (F11-F17), 7/7 minor applied (disposition.md:20-36,46).
- Cycle 2: 15 rows: N1-N5 and the reopened F2, F5, F8 (8 blocking); N6-N9 and F14 (5 minor); citation rows C9 and C2.
  5/5 minor applied (disposition-round2.md:22-36,54). The report says minor notes "do not require changes" (round2:190).

| R3 id | origin | earlier fix (grade) | revert removes anchor? | smaller fix avoids? | class |
|---|---|---|---|---|---|
| R3-1 | changed (report tag; round3:37 ties R3-1..5 to fixes) | N1, F5 (cycle 2), F2 (all blocking) | yes, partly | no: step 3 was never updated, and deletion undoes N1/F5 | C |
| R3-2 | changed ("only the output argument" v3:64,73) | N2 (blocking) | yes | yes: delete "only"; N2 stays fixed | B |
| R3-3 | changed (AC-1.2 v3:209) | F2 reopened (blocking) | yes for the AC anchor | no: needs an added shape (d) | C (D defensible) |
| R3-4 | changed (v3:62 "no other worker writes there") | F5 + N2 resume exception (blocking) | yes | yes: drop the resume exception or keep v2 wording | B |
| R3-5 | changed (own-worktree rule v3:73, step 6 v3:198) | F14 (minor) | yes (F14's false failure returns) | no: needed one more edit to step 1 | A |
| R3-6 | effectively unchanged (AC-0.4 pass column word-for-word v1:194) | F1 sharpened WC-5 (blocking) | no | no | D |

- Summary: R3 blocking 6 = A 1 + B 2 + C 2 + D 1. Judgements. R3-6 has no source fix named in the report.

## trt-r2 (427 text)
- Metrics: R3 `rounds[2].M2.critical_plus_major` = 5 (MAJOR). Bytes from `rounds[i].M4`: 57,763 -> 71,244 -> 78,715. Step growth
  23.34 % and 10.49 % (re-derived here; the file stores no per-step percent). Cumulative
  `growth_summary_for_D6b.treatment_growth_after_two_fix_cycles_percent_bytes` 36.27.
- Cycle 1: 16 rows, 9 blocking (F1-F9: 3 CRITICAL + 6 MAJOR), 7 minor (F10-F16), 7/7 minor applied (disposition.md:49-64,79).
- Cycle 2: 18 rows: N1-N7 blocking; N8-N16 minor plus citation rows C4 and C15 (11). 9 minor applied; N9 and C15 rejected
  (disposition-round2.md:44-61,93-94).

| R3 id | origin | earlier fix (grade) | revert removes anchor? | smaller fix avoids? | class |
|---|---|---|---|---|---|
| R3-1 | tag changed; the faulty `master...HEAD` range is unchanged since v1:176,193 | N4 (blocking), kept the range | no | no: the fault is in kept text | D (C by tag) |
| R3-2 | tag changed; the flag-led gap is in the narrower v1:172 pattern | N5 widened it; F3 self-test (blocking) | no | no: N5 was too narrow, not too large | D (C by tag) |
| R3-3 | changed (WC-6 path insertion v2:64; 2.4 row v2:80) | F8, F1, N2 (blocking) | yes | no: post-release `--output` still nested | C |
| R3-4 | changed (WC-2 refusal, AC-2.2a new in v3) | N7 (blocking) | yes | no: dropping AC-2.2a leaves the rule unchecked | C |
| R3-5 | changed (bounded `ask` v3:61; v2:61 matched Orca) | N6 (blocking) | yes | no: deleting the bound reopens N6 | C |

- Summary: R3 blocking 5 = A 0 + B 0 + C 3 + D 2 (C 5 + D 0 if classed by the report's tags). Judgements.
- UNVERIFIED: round 3 grades R3-5 "minor" in Part 1 (round3:29) but blocking in its findings list (:179,198). Blocking is used here.

## flg-r1 (427 + re-review flags)
- Metrics: R3 `rounds[2].M2.critical_plus_major` = 6, `rounds[2].M2.blocking` = 4. Growth `spec_sizes.v2.growth_pct_bytes_vs_v1`
  17.53 (-> 67,886 B), v2->v3 8.72 (re-derived), cumulative `spec_sizes.v3.growth_pct_bytes_vs_v1` 27.78.
- Cycle 1: 22 rows, 11 blocking (#1-11), 11 minor (#12-22), 10 minor applied (#19 rejected) (disposition.md:16-37).
  The report told the reviser to fix 1-11 only. The reviser applied the minor ones because the Task brief said so (metrics `rounds[0].revise`).
- Cycle 2: 14 rows: R2-1..R2-4 blocking; R2-5..R2-12 minor (R2-7 is MAJOR severity but non-blocking); citation rows C5 and C26.
  10/10 minor and citation rows applied (disposition-round2.md:17-30).

| R3 id | sev / blocking | origin tag | earlier fix (grade) | revert removes anchor? | smaller fix avoids? | class |
|---|---|---|---|---|---|---|
| R3-1 | MAJOR / y | changed | R2-2 (blocking), on R1 #8 | yes (the defect returns in a stricter form) | yes: delete the closed allow-list, keep the forbidden list (round3:197) | B |
| R3-2 | MAJOR / y | changed | R2-3, R1 #9 (blocking) | no: ignored paths are already missing in v1:185 | no | D |
| R3-3 | MAJOR / y | changed | R2-1 (blocking); "P1 commands" ambiguity already in v1:159 | partly | no: `--report-dir` is needed for the WC-13 refusal | C |
| R3-4 | MAJOR / y | changed | R2-1 (blocking); `<report-dir>` from R1 #2 | yes | yes, partly: delete "report goes there too" | B |
| R3-7 | MAJOR / n | changed | R2-7 (non-blocking) | yes | no: the whole fix is the tick rule | A |
| R3-8 | MAJOR / n | changed | gap from R1 #2 (blocking); R2-4 adjacent | no | n/a | D |

- Summary: R3 blocking 4 = A 0 + B 2 + C 1 + D 1. Over CRITICAL+MAJOR 6: A 1 + B 2 + C 1 + D 2. Judgements.
- The report tags all 10 findings changed (round3:192). Here R3-2 and R3-8 are classed D because the problem predates v2.

## flg-r2 (427 + re-review flags)
- Metrics: R3 `rounds[2].M2.critical_plus_major` = 1 (= blocking). Growth `spec_sizes.growth_percent_bytes.v1_to_v2` 21.63
  (-> 70,255 B), `v2_to_v3` 8.64 (-> 76,328 B), cumulative `v1_to_final_cumulative` 32.14.
- Cycle 1: 22 rows, 13 blocking (1 CRITICAL + 12 MAJOR), 9 non-blocking (4 MAJOR + 5 MINOR; spec-panel.md:236). 8 of the 9 non-blocking
  applied (F16 rejected) (disposition.md:16-39).
- Cycle 2: 15 rows: N1-N6 blocking; N7-N11 and 4 citation notes (9 non-blocking). All applied (disposition-round2.md:19-35).

| R3 id | sev / blocking | origin | earlier fix (grade) | revert removes anchor? | smaller fix avoids? | class |
|---|---|---|---|---|---|---|
| N12 | MAJOR / y (Nygard wanted minor, round3:144) | changed (round3:84,159) | N5 (blocking), named at round3:35,85 | yes | no: both halves of N5 are defective; dropping both reopens N5 | C |

- Minor R3 findings: N14 is anchored on the N9 fix (minor), and a smaller fix would avoid it (class A at minor grade).
  C-R3-15 (citation note) comes from the N11 fix (minor). N13 and N15 are D (pre-existing).
- Summary: R3 blocking 1 = A 0 + B 0 + C 1 + D 0.
- UNVERIFIED: whether a transcript can show the pre-launch question. The report infers it and did not read a transcript (round3:86).

## Totals and implied predictions
All A/B/C/D counts are judgements by the per-run readers, reviewed here for consistency, not re-derived.

| run | R3 blocking | A | B | C | D | alternative reading |
|---|---|---|---|---|---|---|
| ctl-r1 | 8 | 0 | 2 | 3 | 3 | A 1 / D 2 (R3-9) |
| ctl-r2 | 4 | 0 | 1 | 2 | 1 | C 1 / D 2 (report tag R3-2) |
| trt-r1 | 6 | 1 | 2 | 2 | 1 | - |
| trt-r2 | 5 | 0 | 0 | 3 | 2 | C 5 / D 0 (report tags) |
| flg-r1 | 4 | 0 | 2 | 1 | 1 | over all 6 CRIT+MAJOR: A 1, D 2 |
| flg-r2 | 1 | 0 | 0 | 1 | 0 | - |

Per-arm means (main reading):

| arm | R3 blocking | A | B | C | D | (i) minus A | (ii) minus A and B |
|---|---|---|---|---|---|---|---|
| control | 6.0 | 0.0 | 1.5 | 2.5 | 2.0 | 6.0 | 4.5 |
| trt | 5.5 | 0.5 | 1.0 | 2.5 | 1.5 | 5.0 | 4.0 |
| flg | 2.5 | 0.0 | 1.0 | 1.0 | 0.5 | 2.5 | 1.5 |
| all 6 | 4.67 | 0.17 | 1.17 | 2.00 | 1.33 | 4.50 | 3.33 |

Reading of the totals:
- Only 1 of 28 R3 blocking findings (trt-r1 R3-5) is anchored on a fix of a minor finding (2 of 28 under the alternative
  ctl-r1 reading). Fixes of minor findings do show up at minor or non-blocking grade: flg-r1 R3-7, flg-r2 N14 and C-R3-15.
  Reverting every minor fix (i) is therefore predicted to cut R3 blocking by about 0.2 per run, which is negligible.
- Shrinking over-sized blocking fixes (ii) removes another 1.17 per run (about 25 %). The largest class is C: 12 of 28
  are new defects that a necessary blocking fix brought in. D (8 of 28) is older text that the reviewers only reached in round 3.
- Caveats (judgement): the predictions assume a revert does not bring back the earlier finding. trt-r1 R3-5 would trade
  for F14's minor false failure, and every B/C revert reopens a blocking finding. They also assume reviewers would not find
  replacement findings elsewhere (UNVERIFIED; the reviews appear to look for new issues each round). With n = 2 per arm,
  the arm differences are not separable from run-to-run noise.

Growth if fixes of minor findings had not been applied (ESTIMATE):
- Method: the dispositions state only whole-cycle sizes (for example flg-r1 disposition.md:42, trt-r1 disposition.md:15),
  which match the metrics bytes. No per-row byte cost is recorded. Assumption: each applied row adds equal bytes. For each cycle,
  minor share = applied minor findings / applied findings (citation rows excluded; flg runs count non-blocking as minor).
  Estimated v3 = v3 bytes - sum over cycles of (cycle growth x minor share). This is UNVERIFIED: minor fixes may be smaller
  than blocking ones, so the equal-bytes assumption probably overstates their share.

| run | cycle 1 minor share | cycle 2 minor share | bytes removed (c1 + c2) | actual growth % | estimated growth % without minor fixes |
|---|---|---|---|---|---|
| ctl-r1 | 8/19 | 6/15 | 5,796 + 7,830 | 57.72 | 34.1 |
| ctl-r2 | 9/21 | 10/17 | 7,908 + 12,706 | 69.34 | 33.7 |
| trt-r1 | 7/16 | 5/13 | 2,942 + 2,548 | 23.11 | 13.6 |
| trt-r2 | 7/16 | 8/15 | 5,898 + 3,985 | 36.27 | 19.2 |
| flg-r1 | 10/21 | 8/12 | 4,820 + 3,947 | 27.78 | 12.6 |
| flg-r2 | 8/21 | 5/11 | 4,759 + 2,760 | 32.14 | 19.1 |

- Arm means: control 63.5 % -> about 33.9 %; trt 29.7 % -> about 16.4 %; flg 30.0 % -> about 15.9 %. On this method, minor-fix
  rows account for roughly 40-55 % of all growth, while they anchor almost none of the R3 blocking findings (see above).
- The estimate ignores that later blocking fixes may build on text that a minor fix added (judgement; not measured).
