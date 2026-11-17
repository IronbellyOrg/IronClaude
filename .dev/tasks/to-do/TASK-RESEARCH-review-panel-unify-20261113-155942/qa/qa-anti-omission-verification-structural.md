# QA Report: Anti-Omission Verification (structural role)

**Topic:** Unified Review Panel research report, anti-omission recoveries (Gate 5, cycle 1)
**Date:** 2026-11-14
**Phase:** fix-cycle (verification of recoveries by an agent that did not add them)
**Fix cycle:** 1
**Fix authorization:** false (report only; no file other than this report was edited)
**Report checked:** `RESEARCH-REPORT-review-panel-unification.md` (4476 lines)
**Inputs:** `qa/qa-anti-omission-consolidated-findings.md` (529 F5 rows, all IMPORTANT, all RECOVER), `qa/qa-anti-omission-fix-log.md` (529 rows, all `Fixed`), `qa/qa-anti-omission-report-3.md`, the four `reviews/adversarial/*/adversarial/return-contract.yaml`, the earlier gate files `qa-consolidated-findings-phase6.md` and `qa-fidelity-consolidated-findings.md`.
**Method:** the id, table, Table of Contents and citation checks were run by script (`/tmp/ao-ver/a.py` to `e.py`, throwaway, not part of the task directory); the wording checks were run by grep and by reading the cited lines.

---

## Overall Verdict: PASS

No CRITICAL or IMPORTANT defect found. Three MINOR notes (below) do not fail the gate.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a1 | Every one of the 529 F5 ids appears in the fix log exactly once | PASS | Consolidated findings: 529 rows, 529 distinct ids, all type Omitted/IMPORTANT. Fix log: 529 rows, 529 distinct ids, 0 duplicates, 0 missing, 0 extra; every row has 5 cells and status `Fixed`. |
| a2 | Every AO3 id named in a 6.E row, a V-692+ row or the fix log exists in `qa-anti-omission-report-3.md` | PASS | AO3 holds 5203 item rows (`| <id> |`, including the `M3-A-nnn` and `M3-B-nnn` forms). The ids named by 155 6.E rows (522 ids), by V-692 to V-698 (7 ids) and by the fix log (529 ids) all exist there: 0 unknown ids. |
| a3 | Every one of the 529 ids is named in some 6.E row, V-692+ row, existing named report item (dedup) or priority correction | PASS | 522 ids are named in the `AO3 ids` column of 6.E rows (L1 182 in 6.E.1, P 88 in 6.E.2, W 152 in 6.E.3, M 100 in 6.E.4) and 7 in V-692 to V-698 (A01-075, A02-033, A02-099, A03-076, A05-014, A05-097, A05-121); 522 + 7 = 529; ids not named anywhere: 0. No id was left to a "dedup against an existing item" or "scope rule" justification; the 11 `M3-A-nnn` and `M3-B-025` ids are named too. |
| a4 | Fix-log row and report row agree | PASS | For all 522 fix-log rows in 6.E, the `Row Cxx-nn` label in the fix log exists in the report, the report row names that id in its `AO3 ids` cell, the sub-table matches the id's partition (L to 6.E.1 C13, P to 6.E.2 C14, W to 6.E.3 C05, M to 6.E.4 C03) and the row title matches. 0 mismatches. 6.E ids not in the fix log: 0. |
| b1 | Every 6.E sub-table row has the header's cell count (pipes escaped) | PASS | All four sub-tables have a 5-cell header; 155 data rows, all 5 cells when split on unescaped pipes; 0 bad rows. Item codes run in order with no gap or duplicate (C13-01 to C13-46, C14-01 to C14-32, C05-01 to C05-43, C03-01 to C03-34). Kind values are all inside the stated 8-value set (38 residual risk, 34 decision, 26 rule, 23 open item, 16 invariant closure, 10 test pin, 6 coupled edit site, 2 script). |
| b2 | Every Section 8.1 row has the header's cell count | PASS | Header (L3121) has 7 cells; all 698 `V-nnn` rows have 7 cells; V ids run 1 to 698 with no gap or duplicate. The new rows V-692 to V-698 use known Kind and Effort values and known destinations (V-693 "Severity scale and per-consumer mapping" is the 7.1.3 component name that the 8.1 conventions table (L3117) lists). |
| b3 | Table of Contents matches the headings including 6.E | PASS | ToC: 73 entries. Report headings at level 2 and 3 after the ToC: 73. Same order, same text, same level; every anchor equals the heading slug. `6.E Detail carried from the four adversarial debates` is in the ToC under Section 6, after `Options Comparison` (ToC lines 11-89). The `####` headings (6.E.1 to 6.E.4, like every other `####`) are not in the ToC, which is the report's existing convention. |
| b4 | Section 8.1 row total and any total the additions changed are consistent | PASS | The report states no total for the Section 8.1 row count (grep for `691`, `698`, `V-1 to`, "rows" outside table rows: no hit). The gap-table total of 145 rows (L760) is a different table and was not touched. The numbers the new text restates (invariant counts 10, 11, 3, 2 HIGH; status `partial`; convergence 0.89, 0.909, 0.80, 0.86) match the four return contracts and the Section 7 and Section 8 preambles. |
| b5 | Section 9.1 still lists G-01 to G-94 once | PASS | Section 9.1 (L4183 to L4250): 94 distinct `G-nn`, none missing, none extra, none repeated. |
| b6 | Section 10 Adversarial Debate Outputs points to 6.E | PASS | L4456: "...are carried in Section 6.E (6.E.1 C-13, 6.E.2 C-14, 6.E.3 C-05, 6.E.4 C-03), one row per item or tight group with the debate file and line as citation." The four-row folder table above it is unchanged. |
| c1 | S1 (muse-ember-1.0, old L3040 and V-407) corrected in place | PASS | The old L3040 is now V-102 (L3224; the insertion of 6.E shifted lines by 184) and the old V-407 L3345 is now L3529. Both now say the model "is set live as `T4Model04=muse-ember-1.0` (debate A-004 REJECT, EV-14; 'absent from the environment' is false)", absent from packaged data, serving unknown. Matches `reviews/adversarial/model-tier-config/adversarial/diff-analysis.md:89` and `merge-log.md:177`. The phrase "absent from the 2026-11-13 gateway list" is still used, but only as the dated gateway-list fact, which the debate itself keeps (EV-14); it is no longer given as "absent from the environment" (see note N1). |
| c2 | S2 ("E2's best panels cannot be expressed" in C-03) corrected in place | PASS | grep for `cannot be expressed` and `cannot express` gives 0 hits for this claim. C-03 Option A cons (L1339) now says E2's best real-blocking panel (haiku + 2x luna) "has the shape of combination E and is expressible by class binding (debate EV-10, 6.E.4; `muse-ember-1.0` as a class value is untested, EV-9)". Row C03-20 carries it. The only remaining `cannot express` (L2238) is about severity-scale options, not this claim. |
| c3 | S3 ("adds blockers with each added reviewer" in C-05) corrected in place | PASS | L1469 (C-05 Option A cons): "the claim that it adds blockers with each added reviewer is not supported: the who-judges-blocking debate (EC2) found E2 neither supports nor refutes a panel-size effect ...". The phrase appears only inside the denial (note N2). The flat per-size figures (1.00, 1.27, 1.05, 1.33, 0.89) match `adversarial/refactor-plan.md:104`. |
| d1 | No debate winner changed | PASS | Return contracts: ledger-model base B (0.9804 against 0.9724), model-tier-config base A, panel-size-cost base B (variant 2, Option B), who-judges-blocking base B (Option D); all four `status: partial`, convergence 0.89 / 0.86 / 0.80 / 0.909, HIGH invariants 10 / 2 / 3 / 11. The C-03, C-05, C-13, C-14 "Adversarial result" lines, the Section 7 table (L2865-2867) and the Section 10 table state the same; 6.E opens with "the four debates stay `partial` and no winner changes" and contains no text that overturns a winner. |
| d2 | The only `[CONTRADICTION` text is the Section 7 flag and its echoes | PASS | 13 lines contain `[CONTRADICTION`: L2961 (7.1.3 Merge and verdict row, the flag), and the echoes at L3095, L3103, L3555, L3824, L3840, L3841, L3849, L3891, L4082, L4112, L4120, L4379; all are about the core verdict vocabulary. 0 hits in 6.E (L2624-2807) and in V-692 to V-698. |
| d3 | No roadmap | PASS | Every `roadmap` hit is a negation or the existing scope note ("report only; no roadmap", "not a roadmap", "later roadmap"); 6.E and V-692 to V-698 contain none; no dates, sprint or ordering commitments in the new text (the one `sprint` hit, C03-17, is the path `cli/sprint/aienv.py`). |
| d4 | E2 cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | PASS | In the new text the only E2 commit reference is the full hash (C03-20); V-695 cites `E2:CR:426,428`, the report's existing `E2:` convention (L3119) that is pinned to that hash. No other commit hash appears in the new text. |
| d5 | Parsed-sparse counts only | PASS | Row C14-23 and C14-22 state counts only (39 files, 38 Tier 2, 35 flagged, 34 flagged and Tier 2; rule 4 = 18, rule 6 = 9, rule 5 = 2, row 8 = 1, row 0 = 1, none = 3; 29 of 34 outside its influence; decisive in 0 for certain, at most 1 of 39) and mark the older "35 of 39" as wrong. They match `panel-size-cost/adversarial/return-contract.yaml:27` (`escalation_figure_after_check`) and Section 8 binding fact (3) (L3103). No causal "driven by" claim was added. |
| e1 | No regression of P6-B1 | PASS | V-037 (L3159): "30 findings lost at merge (all dropped findings, not only blocking ones; E2's blocking-lost total is 49)"; no assembler flag. |
| e2 | No regression of P6-B12 | PASS | SC-18 to SC-23 exist (L543-548): MS-14, ENS-2, ENS-3, ENS-4, ENS-5 each have a criterion and test. |
| e3 | No regression of P6-B18 | PASS | SC-16 (L541) states the route meant (a reflect-side code writer derives `merge_method` and writes `merged-verdict.yaml`; the installed `sc-adversarial-protocol` writes none). |
| e4 | No regression of P6-B34 | PASS | The `plugins/` mirror is named in the rows M1-11, M3-01, M3-08 and G10 (4 of 4 rows contain `plugins/`). |
| e5 | No regression of F4-B1 | PASS | 0 hits for "at most one model per tier" and "every `fallbacks` list is empty" as a general claim; K-10 (L563) and C-03 (L1338) carry the narrowed `t1a-1` statement. |
| e6 | No regression of F4-B3 | PASS | 0 hits for "add the v1 block rules the docstring claims"; L356, MS-01 and DOC-02 (L664) carry "line-level claim ... [STALE DOC, incomplete rather than false]". |
| e7 | No regression of F4-B4 | PASS | 0 hits for "always `degraded`" or "calibrator is always". |
| c-new | New citations resolve (structural role: citations) | PASS | 869 `file:line` references in the 6.E Source cells (16 short names, all defined in the "Source cells" paragraph at L2628) were checked against the line count of the cited debate file: 0 out of range, 0 unknown short names, 0 rows without a source. Content spot-checks of cited lines: ML:182-183 and PM:364 (C13-01 probe totals), DA:89 and ML:177 (C03-21), DA:136-140 and DT:93 (C14-23), DT:76 (C05-25) say what the rows say. The code citations of V-693 resolve in `src/superclaude/pr_submit/models.py:168-194` (`Finding` has `in_diff` but no affected-callsite or pre-existing field) and `severity_router.py:178-197`; the rubric lines resolve in `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md:94-96`; V-696 `ensemble.py:364-390` and V-697 `swarm/merge.py` exist. |

## Row verification table

Method for the table: each row id of the 529 is checked by script against the fix log, the report row that names it and AO3 (checks a1 to a4). "Recovered correctly" here is the structural judgement (the row exists, names the id, sits in the right sub-table, has the right cell count and resolvable citations); the judgement of meaning is the content role's. The last column names the report row and its line.

| Row ID | Recovered or justified correctly? | Evidence |
|---|---|---|
| F5-A01-075 | Yes (recovered, structure) | 8.1 row V-692, report L3814; 7 cells; id named in its Reason cell; source cell resolves |
| F5-A02-033 | Yes (recovered, structure) | 8.1 row V-693, report L3815; 7 cells; id named in its Reason cell; source cell resolves |
| F5-A02-099 | Yes (recovered, structure) | 8.1 row V-694, report L3816; 7 cells; id named in its Reason cell; source cell resolves |
| F5-A03-076 | Yes (recovered, structure) | 8.1 row V-695, report L3817; 7 cells; id named in its Reason cell; source cell resolves |
| F5-A05-014 | Yes (recovered, structure) | 8.1 row V-696, report L3818; 7 cells; id named in its Reason cell; source cell resolves |
| F5-A05-097 | Yes (recovered, structure) | 8.1 row V-697, report L3819; 7 cells; id named in its Reason cell; source cell resolves |
| F5-A05-121 | Yes (recovered, structure) | 8.1 row V-698, report L3820; 7 cells; id named in its Reason cell; source cell resolves |
| F5-L1-022 | Yes (recovered, structure) | 6.E.1 row C13-01, report L2636; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-023 | Yes (recovered, structure) | 6.E.1 row C13-02, report L2637; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-028 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-031 | Yes (recovered, structure) | 6.E.1 row C13-19, report L2654; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-038 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-042 | Yes (recovered, structure) | 6.E.1 row C13-22, report L2657; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-048 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-049 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-050 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-057 | Yes (recovered, structure) | 6.E.1 row C13-06, report L2641; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-058 | Yes (recovered, structure) | 6.E.1 row C13-06, report L2641; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-061 | Yes (recovered, structure) | 6.E.1 row C13-07, report L2642; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-062 | Yes (recovered, structure) | 6.E.1 row C13-07, report L2642; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-065 | Yes (recovered, structure) | 6.E.1 row C13-24, report L2659; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-070 | Yes (recovered, structure) | 6.E.1 row C13-29, report L2664; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-073 | Yes (recovered, structure) | 6.E.1 row C13-19, report L2654; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-074 | Yes (recovered, structure) | 6.E.1 row C13-25, report L2660; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-076 | Yes (recovered, structure) | 6.E.1 row C13-26, report L2661; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-078 | Yes (recovered, structure) | 6.E.1 row C13-27, report L2662; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-080 | Yes (recovered, structure) | 6.E.1 row C13-27, report L2662; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-082 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-083 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-084 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-085 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-088 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-090 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-099 | Yes (recovered, structure) | 6.E.1 row C13-33, report L2668; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-102 | Yes (recovered, structure) | 6.E.1 row C13-25, report L2660; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-109 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-113 | Yes (recovered, structure) | 6.E.1 row C13-32, report L2667; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-119 | Yes (recovered, structure) | 6.E.1 row C13-31, report L2666; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-124 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-139 | Yes (recovered, structure) | 6.E.1 row C13-15, report L2650; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-142 | Yes (recovered, structure) | 6.E.1 row C13-16, report L2651; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-143 | Yes (recovered, structure) | 6.E.1 row C13-16, report L2651; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-153 | Yes (recovered, structure) | 6.E.1 row C13-36, report L2671; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-170 | Yes (recovered, structure) | 6.E.1 row C13-17, report L2652; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-173 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-177 | Yes (recovered, structure) | 6.E.1 row C13-04, report L2639; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-178 | Yes (recovered, structure) | 6.E.1 row C13-04, report L2639; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-183 | Yes (recovered, structure) | 6.E.1 row C13-03, report L2638; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-188 | Yes (recovered, structure) | 6.E.1 row C13-04, report L2639; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-189 | Yes (recovered, structure) | 6.E.1 row C13-08, report L2643; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-190 | Yes (recovered, structure) | 6.E.1 row C13-09, report L2644; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-191 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-195 | Yes (recovered, structure) | 6.E.1 row C13-30, report L2665; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-199 | Yes (recovered, structure) | 6.E.1 row C13-02, report L2637; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-201 | Yes (recovered, structure) | 6.E.1 row C13-05, report L2640; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-203 | Yes (recovered, structure) | 6.E.1 row C13-05, report L2640; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-204 | Yes (recovered, structure) | 6.E.1 row C13-17, report L2652; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-207 | Yes (recovered, structure) | 6.E.1 row C13-41, report L2676; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-209 | Yes (recovered, structure) | 6.E.1 row C13-20, report L2655; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-210 | Yes (recovered, structure) | 6.E.1 row C13-41, report L2676; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-215 | Yes (recovered, structure) | 6.E.1 row C13-41, report L2676; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-222 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-225 | Yes (recovered, structure) | 6.E.1 row C13-39, report L2674; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-228 | Yes (recovered, structure) | 6.E.1 row C13-39, report L2674; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-236 | Yes (recovered, structure) | 6.E.1 row C13-25, report L2660; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-240 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-242 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-249 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-254 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-255 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-256 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-258 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-266 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-281 | Yes (recovered, structure) | 6.E.1 row C13-19, report L2654; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-283 | Yes (recovered, structure) | 6.E.1 row C13-21, report L2656; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-284 | Yes (recovered, structure) | 6.E.1 row C13-21, report L2656; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-287 | Yes (recovered, structure) | 6.E.1 row C13-38, report L2673; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-288 | Yes (recovered, structure) | 6.E.1 row C13-38, report L2673; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-290 | Yes (recovered, structure) | 6.E.1 row C13-38, report L2673; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-292 | Yes (recovered, structure) | 6.E.1 row C13-38, report L2673; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-300 | Yes (recovered, structure) | 6.E.1 row C13-34, report L2669; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-301 | Yes (recovered, structure) | 6.E.1 row C13-35, report L2670; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-302 | Yes (recovered, structure) | 6.E.1 row C13-36, report L2671; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L1-313 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-012 | Yes (recovered, structure) | 6.E.1 row C13-07, report L2642; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-015 | Yes (recovered, structure) | 6.E.1 row C13-08, report L2643; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-019 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-021 | Yes (recovered, structure) | 6.E.1 row C13-30, report L2665; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-022 | Yes (recovered, structure) | 6.E.1 row C13-26, report L2661; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-025 | Yes (recovered, structure) | 6.E.1 row C13-24, report L2659; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-030 | Yes (recovered, structure) | 6.E.1 row C13-27, report L2662; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-035 | Yes (recovered, structure) | 6.E.1 row C13-06, report L2641; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-038 | Yes (recovered, structure) | 6.E.1 row C13-04, report L2639; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-061 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-065 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-068 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-070 | Yes (recovered, structure) | 6.E.1 row C13-19, report L2654; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-071 | Yes (recovered, structure) | 6.E.1 row C13-17, report L2652; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-072 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-073 | Yes (recovered, structure) | 6.E.1 row C13-25, report L2660; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-089 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-090 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-097 | Yes (recovered, structure) | 6.E.1 row C13-08, report L2643; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-103 | Yes (recovered, structure) | 6.E.1 row C13-08, report L2643; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L2-107 | Yes (recovered, structure) | 6.E.1 row C13-42, report L2677; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-035 | Yes (recovered, structure) | 6.E.1 row C13-46, report L2681; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-042 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-064 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-096 | Yes (recovered, structure) | 6.E.1 row C13-18, report L2653; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-110 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-127 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-135 | Yes (recovered, structure) | 6.E.1 row C13-18, report L2653; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-142 | Yes (recovered, structure) | 6.E.1 row C13-15, report L2650; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-144 | Yes (recovered, structure) | 6.E.1 row C13-16, report L2651; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-145 | Yes (recovered, structure) | 6.E.1 row C13-16, report L2651; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-160 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-165 | Yes (recovered, structure) | 6.E.1 row C13-41, report L2676; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L3-167 | Yes (recovered, structure) | 6.E.1 row C13-20, report L2655; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-025 | Yes (recovered, structure) | 6.E.1 row C13-36, report L2671; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-030 | Yes (recovered, structure) | 6.E.1 row C13-37, report L2672; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-038 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-040 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-042 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-043 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-047 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-049 | Yes (recovered, structure) | 6.E.1 row C13-15, report L2650; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-050 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-067 | Yes (recovered, structure) | 6.E.1 row C13-33, report L2668; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-068 | Yes (recovered, structure) | 6.E.1 row C13-34, report L2669; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-069 | Yes (recovered, structure) | 6.E.1 row C13-35, report L2670; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-070 | Yes (recovered, structure) | 6.E.1 row C13-35, report L2670; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-088 | Yes (recovered, structure) | 6.E.1 row C13-43, report L2678; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-102 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-125 | Yes (recovered, structure) | 6.E.1 row C13-22, report L2657; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-129 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-132 | Yes (recovered, structure) | 6.E.1 row C13-07, report L2642; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-135 | Yes (recovered, structure) | 6.E.1 row C13-24, report L2659; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-139 | Yes (recovered, structure) | 6.E.1 row C13-44, report L2679; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-141 | Yes (recovered, structure) | 6.E.1 row C13-26, report L2661; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-144 | Yes (recovered, structure) | 6.E.1 row C13-27, report L2662; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-145 | Yes (recovered, structure) | 6.E.1 row C13-27, report L2662; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-146 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-147 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-148 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-149 | Yes (recovered, structure) | 6.E.1 row C13-12, report L2647; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-153 | Yes (recovered, structure) | 6.E.1 row C13-40, report L2675; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-154 | Yes (recovered, structure) | 6.E.1 row C13-39, report L2674; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-155 | Yes (recovered, structure) | 6.E.1 row C13-38, report L2673; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-156 | Yes (recovered, structure) | 6.E.1 row C13-38, report L2673; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-162 | Yes (recovered, structure) | 6.E.1 row C13-01, report L2636; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-163 | Yes (recovered, structure) | 6.E.1 row C13-05, report L2640; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-164 | Yes (recovered, structure) | 6.E.1 row C13-02, report L2637; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-165 | Yes (recovered, structure) | 6.E.1 row C13-05, report L2640; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-169 | Yes (recovered, structure) | 6.E.1 row C13-39, report L2674; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L4-235 | Yes (recovered, structure) | 6.E.1 row C13-45, report L2680; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-010 | Yes (recovered, structure) | 6.E.1 row C13-01, report L2636; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-014 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-022 | Yes (recovered, structure) | 6.E.1 row C13-06, report L2641; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-023 | Yes (recovered, structure) | 6.E.1 row C13-07, report L2642; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-044 | Yes (recovered, structure) | 6.E.1 row C13-27, report L2662; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-062 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-063 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-074 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-075 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-077 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-078 | Yes (recovered, structure) | 6.E.1 row C13-15, report L2650; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-101 | Yes (recovered, structure) | 6.E.1 row C13-43, report L2678; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-132 | Yes (recovered, structure) | 6.E.1 row C13-04, report L2639; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L5-136 | Yes (recovered, structure) | 6.E.1 row C13-02, report L2637; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-015 | Yes (recovered, structure) | 6.E.1 row C13-13, report L2648; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-019 | Yes (recovered, structure) | 6.E.1 row C13-14, report L2649; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-021 | Yes (recovered, structure) | 6.E.1 row C13-17, report L2652; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-023 | Yes (recovered, structure) | 6.E.1 row C13-10, report L2645; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-034 | Yes (recovered, structure) | 6.E.1 row C13-24, report L2659; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-036 | Yes (recovered, structure) | 6.E.1 row C13-34, report L2669; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-068 | Yes (recovered, structure) | 6.E.1 row C13-08, report L2643; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-069 | Yes (recovered, structure) | 6.E.1 row C13-11, report L2646; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-087 | Yes (recovered, structure) | 6.E.1 row C13-03, report L2638; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-094 | Yes (recovered, structure) | 6.E.1 row C13-15, report L2650; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-138 | Yes (recovered, structure) | 6.E.1 row C13-03, report L2638; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-142 | Yes (recovered, structure) | 6.E.1 row C13-06, report L2641; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-144 | Yes (recovered, structure) | 6.E.1 row C13-29, report L2664; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-147 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-148 | Yes (recovered, structure) | 6.E.1 row C13-28, report L2663; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-151 | Yes (recovered, structure) | 6.E.1 row C13-05, report L2640; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-163 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-164 | Yes (recovered, structure) | 6.E.1 row C13-23, report L2658; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-167 | Yes (recovered, structure) | 6.E.1 row C13-07, report L2642; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-L6-191 | Yes (recovered, structure) | 6.E.1 row C13-43, report L2678; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-021 | Yes (recovered, structure) | 6.E.2 row C14-01, report L2687; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-025 | Yes (recovered, structure) | 6.E.2 row C14-15, report L2701; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-048 | Yes (recovered, structure) | 6.E.2 row C14-05, report L2691; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-069 | Yes (recovered, structure) | 6.E.2 row C14-06, report L2692; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-083 | Yes (recovered, structure) | 6.E.2 row C14-04, report L2690; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-089 | Yes (recovered, structure) | 6.E.2 row C14-07, report L2693; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-109 | Yes (recovered, structure) | 6.E.2 row C14-03, report L2689; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-124 | Yes (recovered, structure) | 6.E.2 row C14-08, report L2694; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-126 | Yes (recovered, structure) | 6.E.2 row C14-09, report L2695; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-139 | Yes (recovered, structure) | 6.E.2 row C14-12, report L2698; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-145 | Yes (recovered, structure) | 6.E.2 row C14-13, report L2699; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-153 | Yes (recovered, structure) | 6.E.2 row C14-14, report L2700; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-164 | Yes (recovered, structure) | 6.E.2 row C14-16, report L2702; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P1-166 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-092 | Yes (recovered, structure) | 6.E.2 row C14-01, report L2687; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-095 | Yes (recovered, structure) | 6.E.2 row C14-04, report L2690; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-096 | Yes (recovered, structure) | 6.E.2 row C14-03, report L2689; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-062 | Yes (recovered, structure) | 6.E.2 row C14-02, report L2688; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-063 | Yes (recovered, structure) | 6.E.2 row C14-02, report L2688; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-064 | Yes (recovered, structure) | 6.E.2 row C14-04, report L2690; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-099 | Yes (recovered, structure) | 6.E.2 row C14-08, report L2694; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-101 | Yes (recovered, structure) | 6.E.2 row C14-09, report L2695; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-105 | Yes (recovered, structure) | 6.E.2 row C14-11, report L2697; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-072 | Yes (recovered, structure) | 6.E.2 row C14-22, report L2708; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-066 | Yes (recovered, structure) | 6.E.2 row C14-26, report L2712; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-024 | Yes (recovered, structure) | 6.E.2 row C14-27, report L2713; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-037 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-056 | Yes (recovered, structure) | 6.E.2 row C14-06, report L2692; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P2-083 | Yes (recovered, structure) | 6.E.2 row C14-21, report L2707; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-005 | Yes (recovered, structure) | 6.E.2 row C14-07, report L2693; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-006 | Yes (recovered, structure) | 6.E.2 row C14-07, report L2693; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-074 | Yes (recovered, structure) | 6.E.2 row C14-07, report L2693; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-078 | Yes (recovered, structure) | 6.E.2 row C14-29, report L2715; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-081 | Yes (recovered, structure) | 6.E.2 row C14-28, report L2714; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-082 | Yes (recovered, structure) | 6.E.2 row C14-28, report L2714; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-120 | Yes (recovered, structure) | 6.E.2 row C14-13, report L2699; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-145 | Yes (recovered, structure) | 6.E.2 row C14-22, report L2708; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-146 | Yes (recovered, structure) | 6.E.2 row C14-24, report L2710; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P3-148 | Yes (recovered, structure) | 6.E.2 row C14-06, report L2692; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-011 | Yes (recovered, structure) | 6.E.2 row C14-28, report L2714; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-016 | Yes (recovered, structure) | 6.E.2 row C14-07, report L2693; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-021 | Yes (recovered, structure) | 6.E.2 row C14-30, report L2716; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-023 | Yes (recovered, structure) | 6.E.2 row C14-22, report L2708; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-024 | Yes (recovered, structure) | 6.E.2 row C14-06, report L2692; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-038 | Yes (recovered, structure) | 6.E.2 row C14-25, report L2711; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-040 | Yes (recovered, structure) | 6.E.2 row C14-22, report L2708; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-055 | Yes (recovered, structure) | 6.E.2 row C14-23, report L2709; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-084 | Yes (recovered, structure) | 6.E.2 row C14-04, report L2690; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-120 | Yes (recovered, structure) | 6.E.2 row C14-16, report L2702; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-123 | Yes (recovered, structure) | 6.E.2 row C14-03, report L2689; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-128 | Yes (recovered, structure) | 6.E.2 row C14-20, report L2706; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-129 | Yes (recovered, structure) | 6.E.2 row C14-10, report L2696; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-138 | Yes (recovered, structure) | 6.E.2 row C14-32, report L2718; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-139 | Yes (recovered, structure) | 6.E.2 row C14-32, report L2718; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-141 | Yes (recovered, structure) | 6.E.2 row C14-32, report L2718; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-153 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-154 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-155 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-156 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-157 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-159 | Yes (recovered, structure) | 6.E.2 row C14-18, report L2704; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-161 | Yes (recovered, structure) | 6.E.2 row C14-19, report L2705; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-163 | Yes (recovered, structure) | 6.E.2 row C14-19, report L2705; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P4-182 | Yes (recovered, structure) | 6.E.2 row C14-02, report L2688; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-042 | Yes (recovered, structure) | 6.E.2 row C14-02, report L2688; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-043 | Yes (recovered, structure) | 6.E.2 row C14-01, report L2687; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-044 | Yes (recovered, structure) | 6.E.2 row C14-01, report L2687; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-047 | Yes (recovered, structure) | 6.E.2 row C14-04, report L2690; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-048 | Yes (recovered, structure) | 6.E.2 row C14-03, report L2689; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-057 | Yes (recovered, structure) | 6.E.2 row C14-10, report L2696; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-061 | Yes (recovered, structure) | 6.E.2 row C14-20, report L2706; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-077 | Yes (recovered, structure) | 6.E.2 row C14-32, report L2718; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-085 | Yes (recovered, structure) | 6.E.2 row C14-32, report L2718; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-093 | Yes (recovered, structure) | 6.E.2 row C14-26, report L2712; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-095 | Yes (recovered, structure) | 6.E.2 row C14-08, report L2694; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-096 | Yes (recovered, structure) | 6.E.2 row C14-10, report L2696; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-098 | Yes (recovered, structure) | 6.E.2 row C14-09, report L2695; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-100 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-101 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-103 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-104 | Yes (recovered, structure) | 6.E.2 row C14-17, report L2703; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-108 | Yes (recovered, structure) | 6.E.2 row C14-18, report L2704; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-120 | Yes (recovered, structure) | 6.E.2 row C14-31, report L2717; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-123 | Yes (recovered, structure) | 6.E.2 row C14-07, report L2693; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-143 | Yes (recovered, structure) | 6.E.2 row C14-16, report L2702; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-146 | Yes (recovered, structure) | 6.E.2 row C14-16, report L2702; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-147 | Yes (recovered, structure) | 6.E.2 row C14-16, report L2702; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-P5-148 | Yes (recovered, structure) | 6.E.2 row C14-16, report L2702; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-014 | Yes (recovered, structure) | 6.E.3 row C05-01, report L2724; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-013 | Yes (recovered, structure) | 6.E.3 row C05-02, report L2725; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-015 | Yes (recovered, structure) | 6.E.3 row C05-05, report L2728; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-033 | Yes (recovered, structure) | 6.E.3 row C05-07, report L2730; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-046 | Yes (recovered, structure) | 6.E.3 row C05-03, report L2726; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-048 | Yes (recovered, structure) | 6.E.3 row C05-36, report L2759; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-051 | Yes (recovered, structure) | 6.E.3 row C05-08, report L2731; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-052 | Yes (recovered, structure) | 6.E.3 row C05-08, report L2731; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-055 | Yes (recovered, structure) | 6.E.3 row C05-09, report L2732; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-061 | Yes (recovered, structure) | 6.E.3 row C05-10, report L2733; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-063 | Yes (recovered, structure) | 6.E.3 row C05-06, report L2729; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-064 | Yes (recovered, structure) | 6.E.3 row C05-11, report L2734; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-069 | Yes (recovered, structure) | 6.E.3 row C05-12, report L2735; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-094 | Yes (recovered, structure) | 6.E.3 row C05-13, report L2736; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-096 | Yes (recovered, structure) | 6.E.3 row C05-13, report L2736; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-097 | Yes (recovered, structure) | 6.E.3 row C05-13, report L2736; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-098 | Yes (recovered, structure) | 6.E.3 row C05-18, report L2741; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-102 | Yes (recovered, structure) | 6.E.3 row C05-14, report L2737; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-104 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-105 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-106 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-107 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-109 | Yes (recovered, structure) | 6.E.3 row C05-20, report L2743; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-115 | Yes (recovered, structure) | 6.E.3 row C05-17, report L2740; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-116 | Yes (recovered, structure) | 6.E.3 row C05-15, report L2738; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-117 | Yes (recovered, structure) | 6.E.3 row C05-17, report L2740; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-122 | Yes (recovered, structure) | 6.E.3 row C05-21, report L2744; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-123 | Yes (recovered, structure) | 6.E.3 row C05-22, report L2745; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-141 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-142 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-150 | Yes (recovered, structure) | 6.E.3 row C05-41, report L2764; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-179 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-180 | Yes (recovered, structure) | 6.E.3 row C05-23, report L2746; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-184 | Yes (recovered, structure) | 6.E.3 row C05-26, report L2749; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-185 | Yes (recovered, structure) | 6.E.3 row C05-26, report L2749; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-187 | Yes (recovered, structure) | 6.E.3 row C05-33, report L2756; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-189 | Yes (recovered, structure) | 6.E.3 row C05-23, report L2746; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-192 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-199 | Yes (recovered, structure) | 6.E.3 row C05-17, report L2740; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-200 | Yes (recovered, structure) | 6.E.3 row C05-16, report L2739; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-203 | Yes (recovered, structure) | 6.E.3 row C05-34, report L2757; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-218 | Yes (recovered, structure) | 6.E.3 row C05-29, report L2752; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-225 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-227 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-229 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-231 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-234 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-241 | Yes (recovered, structure) | 6.E.3 row C05-28, report L2751; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-242 | Yes (recovered, structure) | 6.E.3 row C05-28, report L2751; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-248 | Yes (recovered, structure) | 6.E.3 row C05-31, report L2754; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-249 | Yes (recovered, structure) | 6.E.3 row C05-31, report L2754; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W1-263 | Yes (recovered, structure) | 6.E.3 row C05-42, report L2765; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-015 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-017 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-018 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-019 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-021 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-023 | Yes (recovered, structure) | 6.E.3 row C05-01, report L2724; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-028 | Yes (recovered, structure) | 6.E.3 row C05-12, report L2735; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-031 | Yes (recovered, structure) | 6.E.3 row C05-18, report L2741; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-032 | Yes (recovered, structure) | 6.E.3 row C05-14, report L2737; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-036 | Yes (recovered, structure) | 6.E.3 row C05-21, report L2744; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-043 | Yes (recovered, structure) | 6.E.3 row C05-02, report L2725; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-056 | Yes (recovered, structure) | 6.E.3 row C05-09, report L2732; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-065 | Yes (recovered, structure) | 6.E.3 row C05-29, report L2752; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-078 | Yes (recovered, structure) | 6.E.3 row C05-10, report L2733; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-079 | Yes (recovered, structure) | 6.E.3 row C05-10, report L2733; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-080 | Yes (recovered, structure) | 6.E.3 row C05-03, report L2726; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-082 | Yes (recovered, structure) | 6.E.3 row C05-36, report L2759; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-084 | Yes (recovered, structure) | 6.E.3 row C05-20, report L2743; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-087 | Yes (recovered, structure) | 6.E.3 row C05-06, report L2729; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W2-098 | Yes (recovered, structure) | 6.E.3 row C05-04, report L2727; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-028 | Yes (recovered, structure) | 6.E.3 row C05-27, report L2750; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-088 | Yes (recovered, structure) | 6.E.3 row C05-28, report L2751; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-094 | Yes (recovered, structure) | 6.E.3 row C05-27, report L2750; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-102 | Yes (recovered, structure) | 6.E.3 row C05-08, report L2731; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-116 | Yes (recovered, structure) | 6.E.3 row C05-35, report L2758; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-135 | Yes (recovered, structure) | 6.E.3 row C05-32, report L2755; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-136 | Yes (recovered, structure) | 6.E.3 row C05-21, report L2744; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-199 | Yes (recovered, structure) | 6.E.3 row C05-34, report L2757; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-209 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W3-218 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-008 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-011 | Yes (recovered, structure) | 6.E.3 row C05-43, report L2766; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-015 | Yes (recovered, structure) | 6.E.3 row C05-02, report L2725; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-018 | Yes (recovered, structure) | 6.E.3 row C05-08, report L2731; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-022 | Yes (recovered, structure) | 6.E.3 row C05-01, report L2724; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-029 | Yes (recovered, structure) | 6.E.3 row C05-18, report L2741; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-033 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-034 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-035 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-036 | Yes (recovered, structure) | 6.E.3 row C05-20, report L2743; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-042 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-048 | Yes (recovered, structure) | 6.E.3 row C05-23, report L2746; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-049 | Yes (recovered, structure) | 6.E.3 row C05-22, report L2745; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-053 | Yes (recovered, structure) | 6.E.3 row C05-37, report L2760; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-054 | Yes (recovered, structure) | 6.E.3 row C05-37, report L2760; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-061 | Yes (recovered, structure) | 6.E.3 row C05-12, report L2735; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-064 | Yes (recovered, structure) | 6.E.3 row C05-29, report L2752; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-065 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-066 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-067 | Yes (recovered, structure) | 6.E.3 row C05-30, report L2753; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-072 | Yes (recovered, structure) | 6.E.3 row C05-28, report L2751; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-077 | Yes (recovered, structure) | 6.E.3 row C05-16, report L2739; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-078 | Yes (recovered, structure) | 6.E.3 row C05-15, report L2738; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-081 | Yes (recovered, structure) | 6.E.3 row C05-05, report L2728; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-083 | Yes (recovered, structure) | 6.E.3 row C05-13, report L2736; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-086 | Yes (recovered, structure) | 6.E.3 row C05-14, report L2737; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-092 | Yes (recovered, structure) | 6.E.3 row C05-38, report L2761; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-149 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-150 | Yes (recovered, structure) | 6.E.3 row C05-21, report L2744; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-158 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-159 | Yes (recovered, structure) | 6.E.3 row C05-27, report L2750; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-163 | Yes (recovered, structure) | 6.E.3 row C05-16, report L2739; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-166 | Yes (recovered, structure) | 6.E.3 row C05-07, report L2730; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-170 | Yes (recovered, structure) | 6.E.3 row C05-01, report L2724; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-175 | Yes (recovered, structure) | 6.E.3 row C05-23, report L2746; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-189 | Yes (recovered, structure) | 6.E.3 row C05-40, report L2763; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-191 | Yes (recovered, structure) | 6.E.3 row C05-09, report L2732; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-195 | Yes (recovered, structure) | 6.E.3 row C05-40, report L2763; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W4-200 | Yes (recovered, structure) | 6.E.3 row C05-38, report L2761; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-005 | Yes (recovered, structure) | 6.E.3 row C05-23, report L2746; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-006 | Yes (recovered, structure) | 6.E.3 row C05-28, report L2751; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-017 | Yes (recovered, structure) | 6.E.3 row C05-03, report L2726; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-018 | Yes (recovered, structure) | 6.E.3 row C05-04, report L2727; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-020 | Yes (recovered, structure) | 6.E.3 row C05-01, report L2724; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-021 | Yes (recovered, structure) | 6.E.3 row C05-01, report L2724; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-022 | Yes (recovered, structure) | 6.E.3 row C05-05, report L2728; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-023 | Yes (recovered, structure) | 6.E.3 row C05-06, report L2729; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-024 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-025 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-026 | Yes (recovered, structure) | 6.E.3 row C05-24, report L2747; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-043 | Yes (recovered, structure) | 6.E.3 row C05-08, report L2731; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-045 | Yes (recovered, structure) | 6.E.3 row C05-21, report L2744; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-053 | Yes (recovered, structure) | 6.E.3 row C05-09, report L2732; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-054 | Yes (recovered, structure) | 6.E.3 row C05-18, report L2741; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-055 | Yes (recovered, structure) | 6.E.3 row C05-18, report L2741; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-057 | Yes (recovered, structure) | 6.E.3 row C05-10, report L2733; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-058 | Yes (recovered, structure) | 6.E.3 row C05-10, report L2733; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-063 | Yes (recovered, structure) | 6.E.3 row C05-19, report L2742; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-066 | Yes (recovered, structure) | 6.E.3 row C05-20, report L2743; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-069 | Yes (recovered, structure) | 6.E.3 row C05-39, report L2762; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-070 | Yes (recovered, structure) | 6.E.3 row C05-39, report L2762; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-072 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-075 | Yes (recovered, structure) | 6.E.3 row C05-25, report L2748; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-088 | Yes (recovered, structure) | 6.E.3 row C05-36, report L2759; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-095 | Yes (recovered, structure) | 6.E.3 row C05-31, report L2754; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-097 | Yes (recovered, structure) | 6.E.3 row C05-16, report L2739; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-098 | Yes (recovered, structure) | 6.E.3 row C05-15, report L2738; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-103 | Yes (recovered, structure) | 6.E.3 row C05-13, report L2736; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-108 | Yes (recovered, structure) | 6.E.3 row C05-14, report L2737; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-W5-110 | Yes (recovered, structure) | 6.E.3 row C05-40, report L2763; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-023 | Yes (recovered, structure) | 6.E.4 row C03-01, report L2772; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-024 | Yes (recovered, structure) | 6.E.4 row C03-02, report L2773; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-025 | Yes (recovered, structure) | 6.E.4 row C03-05, report L2776; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-026 | Yes (recovered, structure) | 6.E.4 row C03-04, report L2775; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-029 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-032 | Yes (recovered, structure) | 6.E.4 row C03-07, report L2778; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-037 | Yes (recovered, structure) | 6.E.4 row C03-03, report L2774; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-041 | Yes (recovered, structure) | 6.E.4 row C03-08, report L2779; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-046 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-051 | Yes (recovered, structure) | 6.E.4 row C03-12, report L2783; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-055 | Yes (recovered, structure) | 6.E.4 row C03-14, report L2785; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-072 | Yes (recovered, structure) | 6.E.4 row C03-17, report L2788; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-077 | Yes (recovered, structure) | 6.E.4 row C03-18, report L2789; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-081 | Yes (recovered, structure) | 6.E.4 row C03-19, report L2790; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-082 | Yes (recovered, structure) | 6.E.4 row C03-20, report L2791; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-086 | Yes (recovered, structure) | 6.E.4 row C03-21, report L2792; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-095 | Yes (recovered, structure) | 6.E.4 row C03-16, report L2787; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-098 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-099 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-100 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-118 | Yes (recovered, structure) | 6.E.4 row C03-09, report L2780; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-121 | Yes (recovered, structure) | 6.E.4 row C03-24, report L2795; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-122 | Yes (recovered, structure) | 6.E.4 row C03-15, report L2786; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-124 | Yes (recovered, structure) | 6.E.4 row C03-25, report L2796; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-125 | Yes (recovered, structure) | 6.E.4 row C03-25, report L2796; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-131 | Yes (recovered, structure) | 6.E.4 row C03-26, report L2797; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-132 | Yes (recovered, structure) | 6.E.4 row C03-26, report L2797; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-133 | Yes (recovered, structure) | 6.E.4 row C03-26, report L2797; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-135 | Yes (recovered, structure) | 6.E.4 row C03-27, report L2798; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-139 | Yes (recovered, structure) | 6.E.4 row C03-28, report L2799; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-143 | Yes (recovered, structure) | 6.E.4 row C03-30, report L2801; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M1-144 | Yes (recovered, structure) | 6.E.4 row C03-30, report L2801; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-030 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-054 | Yes (recovered, structure) | 6.E.4 row C03-16, report L2787; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-077 | Yes (recovered, structure) | 6.E.4 row C03-17, report L2788; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-014 | Yes (recovered, structure) | 6.E.4 row C03-21, report L2792; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-013 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-076 | Yes (recovered, structure) | 6.E.4 row C03-31, report L2802; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-090 | Yes (recovered, structure) | 6.E.4 row C03-33, report L2804; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-103 | Yes (recovered, structure) | 6.E.4 row C03-34, report L2805; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-104 | Yes (recovered, structure) | 6.E.4 row C03-01, report L2772; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-106 | Yes (recovered, structure) | 6.E.4 row C03-02, report L2773; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-107 | Yes (recovered, structure) | 6.E.4 row C03-04, report L2775; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-109 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-084 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-086 | Yes (recovered, structure) | 6.E.4 row C03-08, report L2779; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-115 | Yes (recovered, structure) | 6.E.4 row C03-10, report L2781; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M2-121 | Yes (recovered, structure) | 6.E.4 row C03-07, report L2778; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-031 | Yes (recovered, structure) | 6.E.4 row C03-19, report L2790; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-032 | Yes (recovered, structure) | 6.E.4 row C03-20, report L2791; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-044 | Yes (recovered, structure) | 6.E.4 row C03-09, report L2780; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-058 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-063 | Yes (recovered, structure) | 6.E.4 row C03-09, report L2780; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-067 | Yes (recovered, structure) | 6.E.4 row C03-15, report L2786; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-069 | Yes (recovered, structure) | 6.E.4 row C03-25, report L2796; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-070 | Yes (recovered, structure) | 6.E.4 row C03-25, report L2796; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-074 | Yes (recovered, structure) | 6.E.4 row C03-26, report L2797; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-A-075 | Yes (recovered, structure) | 6.E.4 row C03-26, report L2797; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M3-B-025 | Yes (recovered, structure) | 6.E.4 row C03-29, report L2800; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-008 | Yes (recovered, structure) | 6.E.4 row C03-12, report L2783; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-010 | Yes (recovered, structure) | 6.E.4 row C03-25, report L2796; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-014 | Yes (recovered, structure) | 6.E.4 row C03-21, report L2792; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-023 | Yes (recovered, structure) | 6.E.4 row C03-31, report L2802; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-035 | Yes (recovered, structure) | 6.E.4 row C03-25, report L2796; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-041 | Yes (recovered, structure) | 6.E.4 row C03-32, report L2803; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-047 | Yes (recovered, structure) | 6.E.4 row C03-26, report L2797; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-048 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-050 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-051 | Yes (recovered, structure) | 6.E.4 row C03-18, report L2789; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-055 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-059 | Yes (recovered, structure) | 6.E.4 row C03-31, report L2802; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-064 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-065 | Yes (recovered, structure) | 6.E.4 row C03-23, report L2794; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-066 | Yes (recovered, structure) | 6.E.4 row C03-21, report L2792; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-095 | Yes (recovered, structure) | 6.E.4 row C03-33, report L2804; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-097 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-101 | Yes (recovered, structure) | 6.E.4 row C03-31, report L2802; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-107 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-114 | Yes (recovered, structure) | 6.E.4 row C03-31, report L2802; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-120 | Yes (recovered, structure) | 6.E.4 row C03-05, report L2776; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-121 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-130 | Yes (recovered, structure) | 6.E.4 row C03-12, report L2783; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-135 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-136 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-139 | Yes (recovered, structure) | 6.E.4 row C03-04, report L2775; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-141 | Yes (recovered, structure) | 6.E.4 row C03-13, report L2784; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-144 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-145 | Yes (recovered, structure) | 6.E.4 row C03-23, report L2794; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-146 | Yes (recovered, structure) | 6.E.4 row C03-21, report L2792; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-148 | Yes (recovered, structure) | 6.E.4 row C03-14, report L2785; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M4-152 | Yes (recovered, structure) | 6.E.4 row C03-32, report L2803; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-008 | Yes (recovered, structure) | 6.E.4 row C03-05, report L2776; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-012 | Yes (recovered, structure) | 6.E.4 row C03-11, report L2782; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-018 | Yes (recovered, structure) | 6.E.4 row C03-16, report L2787; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-048 | Yes (recovered, structure) | 6.E.4 row C03-07, report L2778; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-051 | Yes (recovered, structure) | 6.E.4 row C03-08, report L2779; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-053 | Yes (recovered, structure) | 6.E.4 row C03-06, report L2777; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-055 | Yes (recovered, structure) | 6.E.4 row C03-04, report L2775; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-060 | Yes (recovered, structure) | 6.E.4 row C03-22, report L2793; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |
| F5-M5-062 | Yes (recovered, structure) | 6.E.4 row C03-21, report L2792; 5 cells; id in its `AO3 ids` cell; Source cell lines in range |

## New-defects table

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| - | - | - | No new CRITICAL or IMPORTANT defect found in the recovered content (tables, totals, ToC, citations, scope). | none |
| N1 | MINOR (note) | L3224 (V-102), L3529 (V-407), L2792 (C03-21) | The phrase "absent from the 2026-11-13 gateway list" remains next to the correction. It is the dated gateway-list fact that the debate itself keeps (`diff-analysis.md:89`, EV-14); the stale claim "absent from the environment" is now written as false. A reader who stops at the V-407 Item cell sees only the old wording; the Reason cell carries the correction. | Optional: add "(but set live as `T4Model04`)" to the V-407 Item cell. Not required. |
| N2 | MINOR (note) | L1469 (C-05 Option A cons) | The stale phrase "adds blockers with each added reviewer" still appears, but only inside the sentence that says it is not supported. A literal grep for the old phrase therefore still hits once. | None. |
| N3 | MINOR (note) | 6.E (L2624-2807) | Rows are long (one cell of C13-xx and C05-xx rows runs several hundred words) although the 6.E preface calls them "short form". Readability only. | None. |

Prior-cycle items: this is cycle 1 of the anti-omission gate; there is no earlier verification report to compare with. No blocking count to monitor for monotonicity (|F_1| = 0).

## Summary

- Checks passed: 26 / 26 (rows a1 to a4, b1 to b6, c1 to c3, c-new, d1 to d5, e1 to e7)
- Checks failed: 0
- Critical issues: 0; Important issues: 0; Minor notes: 3 (N1 to N3)
- Issues fixed in place: 0 (fix authorization is false; no file other than this report was written)
- Row table: 529 of 529 ids verified structurally; 0 rows flagged

## Limits of this structural check

- Judging whether each recovered detail faithfully carries its debate source in meaning is the content role's check (`qa-anti-omission-verification-content.md`). Here, meaning was spot-checked on 8 rows only (C13-01, C03-21, C14-22, C14-23, C05-25, V-693, V-696, V-697) and the source line citations were checked by range for all 869 references.
- Line numbers in this report are the report's lines at the time of reading (4476 lines).

## Actions Taken

None on the report or any task file. The only file written is this report; scratch scripts live in `/tmp/ao-ver/` outside the task directory.

## Recommendations

- Proceed to the next item of the task file; the structural verification of the anti-omission recoveries found nothing to fix.

## Confidence Gate

- **Confidence:** Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 (grep run through Bash, 9 calls) | Glob: 0 | Bash: 27 (of which 5 were Python check scripts: id coverage, ToC and heading slugs, citation bounds, fix-log to report row cross-check, V-row vocabulary). Read + Grep + Glob (1) is below the 26 items, so by the engagement rule this review is flagged; each item above names the script output or grep result that supports it, and the table, ToC, G-index and citation checks are exhaustive by script rather than sampled.
- Web research: none (not needed; all claims are local).
- Unchecked items: none. Unverifiable items: none.

## Verdict

**Verdict: PASS**

## QA Complete
