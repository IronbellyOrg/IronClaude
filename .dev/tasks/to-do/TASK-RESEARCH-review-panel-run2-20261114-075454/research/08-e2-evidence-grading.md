# Research: E2 evidence, graded (tasklist review-panel study)
**Investigation type:** Pattern Investigator
**Scope:** E2 study `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` at E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` (git show / git ls-tree only); scope slices 01-04 in `research/scope/`
**Status:** Complete
**Date:** 2026-11-14
---

Conventions. `T` = `6c0984326cbb8fb06c4a36065de58b171d3f8175`; `A1` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`; `CR` = `A1/COMBO-REPORT.md`; `PR` = `A1/PILOT-REPORT.md`; every citation is `git show T:<path>` line numbers. Strength grades: **S3** = recomputed here from committed data and robust; **S2** = recomputed, but small n, one judge, or exploratory; **S1** = anecdote or single run; **S0** = retracted, contradicted or not re-checkable. Tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED] (also [RECOMPUTED] = re-derived here by the quoted command). Scratch: the study tree was extracted with `git archive T <A1> | tar -x -C /tmp/review-panel-run2-2.08/tree` (9,312 files, 54 MB) and is deleted before return.

## 1. Item (a) part 1: pilot cells recomputed (arms A/B/C, 3 packages)

Command: for the 3 packages `git show T:A1/arms/scoring/<pkg>/arm-key.json`, `.../<pkg>/ground-truth.json` and the 9 `arms/scoring/<pkg>/{X,Y,Z}/score.json`, piped into `uv run python -c` (stdin only). Arm keys (from `arm-key.json`): designSpec A=Y B=X C=Z; alias A=Y B=Z C=X; design (control) A=X B=Z C=Y.

| Pkg (GT items / blocking-in-implement) | Arm | any | judge-blocking | real blocking | ledger rows (blocking) | wrong blockers |
|---|---|---|---|---|---|---|
| designSpec (10 / 5) | A | 1 (GT3) | 0 | 0 | 4 (0) | 0 |
| designSpec | B | 1 (GT3) | 0 | 0 | 9 (0) | 0 |
| designSpec | C | 2 (GT3, GT7) | 0 | 0 | 13 (1) | 1 |
| alias (4 / 3) | A | 0 | 0 | 0 | 4 (0) | 0 |
| alias | B | 0 | 0 | 0 | 7 (1) | 1 |
| alias | C | 0 | 0 | 0 | 6 (2) | 2 |
| design control (2 / 0) | A | 1 (GT1) | 1 | 0 | 1 (1) | 0 |
| design control | B | 2 (GT1, GT2) | 2 | 0 | 2 (1) | 0 |
| design control | C | 2 (GT1, GT2) | 2 | 0 | 2 (1) | 0 |

Totals [RECOMPUTED]: any/16 A 2, B 3, C 4; real blocking 0 in every arm (0/8 on the defect-rich packages); wrong blockers A 0, B 1, C 3; defect-rich any/14 A 1, B 1, C 2. All 9 cells and the totals equal `PR:46-50` and the per-arm table `PR:18-40`. The control's "GT blocking" cells in PR are judge-blocking: the control GT has 0 `blocking_in_implement` items, so real blocking there is 0 (same judge-semantics flaw as audit F, see section 4).
- Unit of the PR "Wall s" column [RECOMPUTED from `reviews/*.meta.json`]: the SUM of reviewer walls, not elapsed time. designSpec arm C = 260 (sonnet) + 132 (spark) + 16 (terra) + 805 (glm) + 185 (haiku) + 957 (grok) = 2,355 s = the PR value; designSpec B = 260+132+805 = 1,197 s. Any pilot wall ratio therefore assumes serial runs; the later COMBO-REPORT "elapsed" is a different unit (sum over packages of the slowest reviewer, audit-F flags L54 per slice 04, [UNVERIFIED] here).
- Arms B and C excluded the Qwen3.8-max slots but kept luna slots (alias C = 2,785 s needs a 148 s luna run; design C = 3,367 s needs a 61 s luna run; those luna `t4-2` files now sit in `quarantine-pre-src-luna/TASK-WF-design-20261108-041415/_pilot/t4-2.*`). `combos/SPEC.md:102-103` says luna "refused to review without source.md (25/25 empty on affected packages)": arm C may therefore have carried an empty luna reviewer on two of three packages [UNVERIFIED that the quarantined pilot luna reports are empty; not opened]. Pilot arms are pre-`source.md` era (`CR:373`).

**Key Takeaways (pilot)**
- S3 (arithmetic): the PR table is reproducible exactly from committed score files.
- S1 (inference): n=3 packages, 1 judge per cell, no replicates; the decision rule "C passes exactly (2 >= 2x1)" rests on ONE defect (GT7 on designSpec).
- The pilot wall column is a sum of reviewer walls; panels B and C are not the nominal `@default`/`@live7` (Qwen removed, luna maybe empty).

## 2. Item (e): counts whose sources disagree, re-derived with `git ls-tree`

| Figure | Claims in sources | Re-derived (command) | Verdict |
|---|---|---|---|
| `combos/` size | 106 scored runs vs 96 directories vs 97 tracked entries vs "107 entries" | `git ls-tree -d --name-only T A1/combos/ \| wc -l` = **96** directories (3 are `n2-sol-contaminated-20261111`, `n2-terra-contaminated-20261111`, `r2-sonnet-superseded-20261112`); `git ls-tree --name-only T A1/combos/ \| wc -l` = **97** entries (96 dirs + `combos/SPEC.md`, the only non-tree entry). Scored runs: 319 `score.json*` paths under `arms/scoring/` = 9 pilot + 309 combo (103 rows x 3 packages; all 103 rows have all 3 packages) + 1 `score.json.invalid-apierror`. **106 = 3 pilot arms + 103 scored rows** (`CR:431`), reproduced by grouping the scores per run (106 runs: ARM-A/B/C + 103 rows). "107 entries" is not reproduced by any count run here | 96 dirs / 97 entries / 106 scored runs are each right in their own unit; "106 row folders" (run-2 hand-off, per slice 01) is [CODE-CONTRADICTED] (96); "107 entries" [UNVERIFIED] |
| `RESULT.md` files | 19 vs 29 | `git ls-tree -r --name-only T A1/ \| grep -c '/RESULT.md$'` = **29**; restricted to `A1/combos/` = **19**; the other 10 are `A1/quarantine-pre-src-luna/_combos/<row>/RESULT.md` | both right: 19 under `combos/`, 29 in the study |
| quarantine files | 428 vs 417 | `git ls-tree -r --name-only T A1/quarantine-pre-src-luna/ \| wc -l` = **417** tracked files (92 `*.md`, 64 `meta.json`, 64 `cost.json`, 62 `attempt1.md`, 62 `attempt1.err`, 60 other `.json`, 10 `RESULT.md`, 1 catfix, 1 `attempt2.md`, 1 `attempt2.err`); 10 `_combos/<row>` dirs. `SPEC.md:102-103` and `CR:107` say "428 reviewer files": 428 exceeds the total tracked count, so it is not a count of tracked files; its basis is unknown (plausibly the original machine incl. untracked raw `attempt*.json`, `RAW-TRANSCRIPTS-NOT-COMMITTED.md:2`). `SPEC.md:103` "9 luna-bearing combo rows" vs `CR:107` "10 combo-row merge sets": tree has **10** | 417 verified; 428 [UNVERIFIED] (cannot be reconciled); "9 rows" [CODE-CONTRADICTED] by the tree, 10 is right |
| Qwen reviewer count | 3 (`PR:12`) vs 4 (`SPEC.md:3`: "3 of 4 runs") | `*.meta.json` of pilot reviewers [RECOMPUTED]: 3 timed-out Qwen3.8-max runs (`attempt` 2, `wall_s` 3000, `model_ok` false, empty `observed_model`): designSpec `t3-2`, alias `t3-1`, design `t2-1`; plus a 4th Qwen run `design/reviews/live7-t3-1/t3-1` (`observed_model` qwen3.8-max, `model_ok` true, `wall_s` 2913, 93,701 output tokens per its `cost.json`) that completed. `resolution-default.json` has 1 Qwen slot per package (3), `resolution-live7.json` has 1+1+2 = 4 | both right: 3 timeouts out of 4 Qwen runs. The owner's disqualification rested on 3 timeouts plus a 4th run that finished at 97% of the timeout; arm C excluded all of them |

**Key Takeaways (counts)**
- 96/97/106/103 and 19/29 are each correct in one unit; 428 and "107 entries" are not reproducible and must not be carried.
- Qwen: 3 timeouts out of 4 runs, not "all slots timed out" in the sense of every Qwen run.

## 3. Item (e) first part: alias numbering (run-1 "alias GT3 found once")

Command [RECOMPUTED]: stream all 319 `arms/scoring/**/score.json*` blobs with `git cat-file --batch`, group by run (arm via `arm-key.json`, rows by dir name), map B1..B8/I1..I8 per the `CR:401-417` legend (B1-B5 designSpec GT1-5, B6-B8 alias GT1-3, I1-I5 designSpec GT6-10, I6 alias GT4, I7-I8 control GT1-2). Result over 106 runs (found at any severity / credited through a blocking row): B1 0/0, B2 0/0, B3 95/26, B4 3/3, B5 4/1, B6 1/1, B7 28/25, B8 2/1, I1 4/2, I2 71/33, I3 2/0, I4 4/0, I5 0/0, I6 0/0, I7 16/15, I8 76/37. The "found" column equals `CR:497` cell for cell. Alias GT1 (= B6) was found by exactly one run, `b4-terra-luna-muse` (terra + luna + wonder, matches `CR:503` "luna+terra+wonder"); alias GT3 (= B8) by two runs (`g2-sonnet-ember-r3`, `n2-muse-haiku-grok`); alias GT2 (= B7) by 28; alias GT4 (= I6) by none. Never found: B1, B2, I5, I6 (`CR:501`, reproduced).
- Verdict: the run-1 claim "alias GT3 found once" is [CODE-CONTRADICTED] (GT3 found twice; the once-found defect is alias GT1). The run-2 wording "B6 found once" is right. Grade S3.
- Concentration [RECOMPUTED]: 306 catches in 106 runs; the control (I7+I8) holds 92; the defect-rich 214 catches include B3+I2+B7 = 194 (91%). The "/14" metric is a measure of three easy defects. S3.

**Key Takeaways (numbering)**: alias GT1 once, GT3 twice, GT2 28 times, GT4 never; the defect-rich score is carried by 3 of 14 defects.

## 4. Item (a) part 2: `final-table.py` and `three-way.py` re-run

Method: `git archive T A1 | tar -x` into `/tmp/review-panel-run2-2.08/tree`; the two scripts were piped through `sed` to replace the hard-coded `E = "/home/coder/.../eval-tasklist-review-panel/..."` path, the `/tmp/audit-{k}/flags.tsv` reads, the `/tmp/final-table.py` exec and the three `/tmp/final-*` outputs by scratch paths; nothing else changed; run with `PYTHONDONTWRITEBYTECODE=1 uv run python`. Hard-coded paths: `analysis/final-table.py:7` (E), `:23` (`/tmp/audit-{k}/flags.tsv`), `:80-83` (outputs), `analysis/three-way.py:4` (`exec(open("/tmp/final-table.py")...)`), `:48`, `:52` [CODE-VERIFIED by `git show T:... | cat -n`].
- `final-table.py` output header: `valid-era rows: 71; row-packages scored: 213; row-packages carrying an audit EXCLUDE flag (A,B incomplete/short,D,E,F): 69`; the written `final-table.md` is byte-identical to the committed `A1/analysis/final-table.md` (`diff` printed IDENTICAL) [RECOMPUTED, S3].
- `three-way.py` reproduces the `CR:375-383`/`CR:421-428` figures [RECOMPUTED]: sonnet + 2x luna (n=6: `b4-sonnet-luna2` + `j1-sonnet-luna2-r1..r5`): found 2.33 (sd 0.94, range 1-4), real blocking 0.33, wrong blockers 1.83, control found 1.33, tokens 139,113, elapsed 821 s. ember + 2x luna (n=6): 1.83 / 0.17 / 1.83 / 0.83 / 63,644 / 348 s. sonnet + luna + ember (n=5): 2.20 / 0.20 / 2.00 / 0.80 / 138,551 / 676 s. h2 (n=4): 2.25 / 0.25 / 3.50 / 1.50 / 189,325 / 738 s. Permutation p (20,000 shuffles, seed 1): sonnet+2x luna vs ember+2x luna found 0.512, real blocking 1.000, wrong blockers 1.000, control 0.276, tokens 0.003, elapsed 0.003; vs h2 wrong blockers 0.072, tokens 0.005. Reviewer-level: luna dropped/nosrc 4/9 of 36 in ember+2x luna vs 1/1 of 36 in sonnet+2x luna (the j1 rows are in no audit, so their counts are from audits of 1 row only).
- Defect in `final-table.py` [CODE-VERIFIED + RECOMPUTED]: `fullpkg()` (`final-table.py:15-18`) returns `TASK-WF-designSpec-20261107-075614` for the control package id `TASK-WF-design-20261108-041415` (prints above); the exclusion map therefore counts 41 designSpec / 25 alias / 3 control row-packages (`Counter` printed) instead of the right split, so the AUDIT-CLEAN table (`CR:339-359`) is wrong; AS-SCORED is unaffected (no exclusion). S3 for the defect; conclusion direction unchanged (the slice's corrected clean table is [UNVERIFIED] here, not recomputed).
- `three-way.py:19` prints `p[:8]` = `TASK-WF-` as the flagged package name (visible in the `['TASK-WF-']` cells above), so the flagged-package column is unreadable.

**Key Takeaways (reproducibility)**
- S3: the committed AS-SCORED table and the three-way figures are reproducible from committed `score.json` + ledgers + audit flags, but only after patching 5 hard-coded environment paths; the AUDIT-CLEAN table is wrong by a package-mapping bug.
- Nothing about the JUDGE or the reviewer sessions is reproducible: `git ls-tree -r T A1/ | grep -Ec '/judge\.json$|\.attempt[0-9]+\.json$'` = 0 (raw transcripts not committed, `A1/analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md:2`).

## 5. Item (b): the unit behind "92 / 80 / 49" and the two `CR:292` claims

Source line `CR:292` (read through `git show T:A1/COMBO-REPORT.md | sed -n 292p`): "...anchors over 200 characters (56), anchor2 over 200 (18), claims over 300 (14), bad severity, bad refs are discarded with no error. 80 reviewer-level cases, 49 blocking findings lost; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet 0, terra 0, sol 0. Four verdicts flipped FAIL->PASS (g3 alias, g5 alias, n5-sonnet-ember control, plus total-loss merges)."

Recomputed from `A1/analysis/audits/audit-D/flags.tsv` and `audit2.json` (`uv run python`, scratch copy) [RECOMPUTED]:

| Figure | Unit | Recount |
|---|---|---|
| **92** | findings (every finding line rejected by a validity rule, blocking or not, all rows incl. stale) | `audit2.json` `drop_model` values sum to **92**: luna 30, wonder 14, haiku 7, ember 33, grok 1, glm 7 = exactly the "by model" list in `CR:292`. By reason (`audit-D/summary.md`): anchor>200 56, anchor2>200 18, claim>300 14, bad severity 3, refs-bad 1 = 92 |
| **80** | reviewer-package runs with `block ok false` | 80 `2-blockok` rows, all EXCLUDE, 80 unique (row, package, reviewer); in those 80 runs raw findings 335 vs ledger members 229, i.e. 106 findings missing (not 92) |
| **49** | findings that were BLOCKING (subset of the dropped findings) | 49 `3-dropped-blocking` rows, 49 unique (row, package, reviewer, finding), spread over 44 reviewer-runs; reasons anchor>200 24, anchor2>200 14, claim>300 10, refs-bad 1 (sum 49) |
| 111 / 109 | net findings missing by conservation (raw minus ledger members) | `3-conserve`: 88 rows, 83 with `dropped N`, sum 111; 5 rows are fid mismatches or "members 10 > raw 8" (so net = 109 per slice 04; not re-derived here). 111/109 minus 92 = 17-19 findings dropped with no rule-based reason (haiku 23 net vs 7 explained, per slice 04): [UNVERIFIED cause; hypothesis D15 of slice 04 (audit.py and audit2.py parse different blocks)] |

- Resolution of the unit: **92 findings dropped (all severities) > 49 of them blocking; 80 is a count of reviewer runs, not findings; the per-model list in `CR:292` (luna 30, ember 33, ...) sums to 92 and is NOT the breakdown of the 49 blocking findings** (the report's sentence order invites that reading; slice 01 C15 flags the same mislabel in both hand-offs). 49 / 92 = 53% of dropped findings were blocking. Grade S3 for the numbers, S0 for the by-model attribution of the 49.
- **"Four verdict flips" is [CODE-CONTRADICTED].** `audit2.json` `verdict_flip` has 3 entries (4 findings in 3 row-packages): `g3-sonnet-luna-ember-r3`/alias t4-1 F1, `g5-ember2-luna-r2`/alias t4-1 F1, `n5-sonnet-ember`/design t4-1 F1+F2. Their `ledger.json` last-round verdicts are PASS/PASS/PASS with empty `brief_ids` [RECOMPUTED]; the "total-loss" merges (`g1-ember-luna2-r4`/alias, `g7-haiku-luna2-r4`/designSpec, `n4-sonnet-ember`/design) are verdict FAIL / REVISE with non-empty `brief_ids` (L5, L1, L1): they did not flip. `audit-D/summary.md` itself lists three flips and the total-loss merges as "also". Correct figure: 3 flips (S3).
- **"discarded with no error" is [CODE-CONTRADICTED].** Code at HEAD (`src/superclaude/cli/review/ledger.py:122-134`; identical at the E2 tip per slice 04, `git diff --stat` empty) appends one warning per reviewer: `"{id}: findings block problem ({n} error(s)), first: {msg}"`; `findings.py:90-121` `_check_finding` returns the error for the line and `parse_block` drops it. Committed evidence: `combos/b4-sonnet-luna2/TASK-WF-makeTheAliasOnly-.../merge-stdout.txt` has `"warnings": ["t4-1: findings block problem (1 error(s)), first: anchor must have at most 200 characters"]` and `merged-1.md:6` prints `t4-1: report ..., block ok false`; the same pattern in `j1-sonnet-luna2-r3` and `r5` designSpec (`anchor2 must have at most 200 characters`). What is true: the error text names only the FIRST error, the dropped ids/count are not listed, the merged report shows only `block ok false`, 45 merges have no `merge-stdout.txt` (`audit-D/flags.tsv` 8-nostdout), and `merge` exits 0. Wording to use: "dropped with a one-line first-error warning, not an itemised error". [CODE-VERIFIED at HEAD ledger.py:122-134 and findings.py:79-121]
- "16 empty terra reviews" is [CODE-CONTRADICTED] (`CR:294`): `audit-B/flags.tsv` `1-incomplete` = 51 (sol 12, terra 26, haiku 11, luna 2); valid-era (`final-table.py:11-13` predicate): terra 14 + luna 2 = 16 (`e1-grok-ember-luna` designSpec t4-1 and `g7-haiku-luna2-r4` designSpec t3-1) [RECOMPUTED].
- The corrected sentence for the report: "merge dropped 92 findings (49 blocking) in 80 reviewer runs, flipping 3 verdicts from FAIL to PASS, with a first-error warning".

**Key Takeaways (92/80/49)**: units are findings / reviewer-runs / blocking findings; flips are 3; the by-model list is the 92, not the 49; no kernel can be called "silent" in code, but it is silent in practice (itemised drop list absent).

## 6. Item (c): does batch j1 (in no audit) invalidate "not confirmed" (`CR:428`)?

Facts [RECOMPUTED]: `cat audit-*/flags.tsv | grep -c 'j1-'` = 0; `audit-D/summary.md:3` examined 89 rows; j1 (5 rows x 3 packages, 45 reviewer runs) post-dates audit A's snapshot (`audit-A/summary.md:1`, slice 04 A12).
Audit-equivalent checks applied by hand to the 45 j1 reviewer runs (from `*.meta.json`, reports, `merge-stdout.txt`): model identity `model_ok` and `expected == observed` hold in all 45; no run under 1,000 output tokens; no attempt>1. Merge: 2 of the 15 j1 package-merges have a luna `block ok false` (`j1-r3` designSpec t4-1, `j1-r5` designSpec t4-1; the third luna drop in the family, `b4-sonnet-luna2` alias t4-1, is the batch-4 row): in j1 each dropped line is the reviewer's only finding and non-blocking (`F1` MAJOR, `blocking: false`; anchor>200, or anchor2>200 plus claim>300), so no blocking finding was dropped in j1 and no verdict flipped because of a drop. This matches `CR:427` ("2 of the 30 luna runs' findings blocks were dropped at merge, sonnet 0 of 15") [RECOMPUTED for the drops; the "3 of 30 luna never opened source.md" in `CR:427` is [UNVERIFIED] here, it needs raw JSON]. Two luna reports are INCOMPLETE refusals ("Status: INCOMPLETE ... that file is missing from the checkout", empty findings block, `verdict: FAIL`): `j1-sonnet-luna2-r2` designSpec t4-1 and `j1-sonnet-luna2-r4` designSpec t4-1; audit B's `1-incomplete` EXCLUDE rule would flag both. Two more luna designSpec reports (`j1-r1` t4-1, `j1-r5` t3-1) are legitimate empty-block PASS reports with 5,456 and 5,009 output tokens.
Sensitivity (script `sens.py` over the same scratch tree, per-package means summed over the two defect-rich packages, as `final-table.py`):

| Scenario | n (DS/AL/ctl) | found /14 | real blocking /8 | wrong blockers | control /2 | tokens |
|---|---|---|---|---|---|---|
| ember + 2x luna (comparator) | 6/6/6 | 1.83 | 0.17 | 1.83 | 0.83 | 63,644 |
| S0 sonnet+2x luna as scored (b4 + j1) | 6/6/6 | 2.33 | 0.33 | 1.83 | 1.33 | 139,113 |
| S1 j1 dropped (b4 only) | 1/1/1 | 4.00 | 0 | 3 | 2 | 139,660 |
| S2 j1 only | 5/5/5 | 2.00 | 0.40 | 1.60 | 1.20 | 139,004 |
| S3 as scored minus the 2 incomplete-luna designSpec row-packages | 4/6/6 | 2.83 | 0.33 | 1.75 | 1.33 | 141,204 |
| S4 j1 only minus those 2 | 3/5/5 | 2.40 | 0.40 | 1.40 | 1.20 | 141,153 |

Permutation p vs ember + 2x luna (run-level, 20,000 shuffles, seed 1): S2 found 1.000, real blocking 0.546, wrong blockers 0.671; S0 found 0.512, real blocking 1.000, wrong blockers 1.000. Control GT1 (I7) hits [RECOMPUTED]: sonnet+2x luna 3/6, ember+2x luna 0/6, sonnet+luna+ember 0/5, h2 2/4; sonnet-bearing (3+2) 5/10 vs 0/11, Fisher two-sided p = 0.0124, exactly the `CR:426` figure, but one of 16 issues examined post hoc (Bonferroni x16 = 0.20, not significant).
- Decision: j1 being unaudited does NOT invalidate "not confirmed". Under every scenario above the sonnet + 2x luna family is not distinguishable from ember + 2x luna on found, real blocking, wrong blockers (all p >= 0.5) while tokens and elapsed differ (p 0.003); the two unaudited defects found in j1 (2 incomplete luna refusals) would, if excluded, RAISE the sonnet+2x luna found mean (2.33 to 2.83), so the audit gap does not bias against the family. But "not confirmed" is a power statement, not an equivalence statement: n=5-6, permutation p floor, 3 packages reused, so "indistinguishable" must not be read as "equal"; the single decisive piece of evidence against the update is that the original 4/14 was an outlier (S2: j1 runs 2,1,3,2,2). The more important j1 finding is new: 2 of the 10 luna designSpec runs in j1 refused because `source.md` names a requirements input missing from the sandbox, i.e. the input-delivery gap survives the source.md fix for designSpec. Grade: S2.

**Key Takeaways (j1)**: keep "not confirmed" but label it exploratory; audit j1 only for completeness (2 refusals) before citing j1 reliability numbers; the control GT1 sonnet effect is S1 (post hoc, p 0.012 uncorrected).

## 7. Item (d): graded E2 findings

Grades: S3 recomputed and robust; S2 recomputed but small n/one judge/exploratory; S1 anecdote; S0 retracted or not checkable. Citations: `git show T:<path>`.

| # | Finding | Grade | Tag | Citation |
|---|---|---|---|---|
| G1 | Pilot arms: A 2/16, B 3/16, C 4/16; real blocking 0/8 in all arms; wrong blockers 0/1/3 | S3 arithmetic, S1 as evidence (n=3 packages, one judge, Qwen removed, luna maybe empty, pre-source.md) | [RECOMPUTED] | `PR:46-50`; `arms/scoring/<pkg>/{X,Y,Z}/score.json` |
| G2 | Ceiling: no valid-era row above 4/14; 43 of 71 rows at exactly 2/14; distribution (0:3, 1:9, 2:43, 3:12, 4:4); 147 defect-rich catches | S3 | [RECOMPUTED] (`v71.py` over `valid()`) | `analysis/untried.out:35` (slice 04); `CR:274` |
| G3 | The "/14" metric is dominated by three easy defects: designSpec GT3 63 + GT7 50 + alias GT2 18 = 131 of 147 (89%); designSpec GT1, GT2, GT10 and alias GT4 never caught in 106 runs | S3 | [RECOMPUTED] | `CR:497-501`; `analysis/allsets/allsets-table.md:65-66` |
| G4 | Judge-blocking overstates blocking: 65 judge-blocking catches vs 38 real blocking over 71 valid rows (defect-rich) | S3 | [RECOMPUTED] (`v71.py`: 65 / 38) | `CR:291`; `analysis/audits/audit-F/presence.txt:11` (slice 04) |
| G5 | Merge drop: 92 findings, 49 blocking, 80 runs, 3 verdict flips | S3 for the counts, S0 for "four flips", "no error" and the by-model attribution of the 49 | see section 5 | `audit-D/summary.md`; `audit2.json`; `ledger.py:122-134` HEAD |
| G6 | `source.md` never referenced in 156 of 665 valid-era runs (ember 81/209, luna 49/222, haiku 15/75, grok 4/24, wonder 6/25, sonnet 1/63, terra 0/44, sol 0/3) | S2: aggregation recomputed from `audit-C/runs.json` (665, 156 reproduced); the detection reads raw `attempt*.json` that are not committed; cause is stated as UNVERIFIED inference by `CR:373` | [RECOMPUTED] aggregation, [UNVERIFIED] detection | `CR:373`; `audit-C/runs.json`, `audit-C/flags.tsv` (`2-nosrc` 156) |
| G7 | Refusals: 51 `1-incomplete` runs; valid-era 16 = 14 terra + 2 luna; luna anchor fidelity 91.4% | S3 for counts | [RECOMPUTED] | `audit-B/flags.tsv`; `CR:294` |
| G8 | Replicated family means (n=4-6): ember+luna 2.25 (n=4), ember+2x luna 1.83, haiku+2x luna 2.20, sonnet+ember 2.50 etc. | S2 (replicates reuse the same 3 packages: pseudo-replication; 48 tests, perm p floor 0.029, `audit-F/flags.tsv:56` per slice 04) | [RECOMPUTED] for the sonnet/ember families (section 4), others [UNVERIFIED here] | `analysis/final-table.md`; `CR:303-337` |
| G9 | Surviving significant effects: second luna raises control found (+0.83, perm p 0.048); 2x luna + 2x ember has 2.75-3.25 more wrong blockers; ember+terra worse (-1.75, p 0.029) | S2 exploratory (6 of 48 tests p<0.05, 2-3 false positives expected) | [UNVERIFIED here] (read from `CR:298`, `audit-F/stats.tsv` via slice 04) | `CR:298` |
| G10 | Default `ember + 2x luna` (64k tokens, 1.83/14, 0.17 real blocking, control 0.83) | S2: replicated n=6 but ember skipped `source.md` in 9 of 18 runs and dropped 2 findings blocks, so its measured quality is partly source-blind and the recommendation may shift once the harness is fixed (`CR:371`) | [RECOMPUTED] (three-way reviewer-level table) | `CR:363-371`, `CR:428` |
| G11 | sonnet + 2x luna as optional tier; reached control GT1 in 5/10 sonnet-bearing runs vs 0/11 | S1 (post hoc, one of 16 issues, uncorrected p 0.012) | [RECOMPUTED] | `CR:426-428` |
| G12 | Single-run leaders (grok+haiku+haiku+sonnet 4.00/14 594k tokens; haiku+sonnet+wonder 4.00) | S1 anecdotes; `CR:361` says only rows with 4+ runs support a ranking; sonnet+2x luna's 4/14 is now known to be an outlier (S2) | [RECOMPUTED] for sonnet+2x luna | `CR:306-307`, `CR:370` |
| G13 | Merge defects measured by the audit: 195 of 1,398 multi-member rows are chains, 83 rows with >=8 members or >=4 sections, 46 span-null rows (13 blocking) | S2: replay is a COPY of `findings.py` logic (`audit2.py` L40) that the slice verified line-by-line against the kernel; counts printed to console only | [UNVERIFIED] here (`audit2.json` `chain_rows` has 195 entries, recomputed: 195); the 1,398 denominator and 46/13 not re-derived | `audit-D/summary.md` X1/X2; `audit2.json` |
| G14 | Model identity: 2 `b4-muse-luna2` "wonder" runs served terra; no other mismatch; gateway identity bleed under load | S2: derived from `meta.json` (recomputable) and raw JSON (not committed); the harness `expected_model` overwrite flaw means a silent fallback could hide in checks run before the batch-9 fix | [UNVERIFIED] for the raw-JSON part | `audit-A/summary.md:6-12`; `tools/run-reviewer.sh` (`:57-87` per slice 03) |
| G15 | Blind-judge reliability: 294 judge outputs "clean", blind re-judge of 12 rows 12/12 exact, 19/19 catches confirmed, GT8 borderline | S0 for the re-judge: `git ls-tree -r T A1/ | grep -ciE 'rejudge|re-judge'` = 0, no artifact committed; the 294 clean claim rests on audit E (no summary; `check2.py` console output not committed) | [UNVERIFIED] | `CR:296`; `audit-E/` |
| G16 | Retracted/non-reusable: n2-sonnet-src 8/14, 5/8 (corrupted judge); "second run adds nothing" (`attrib.py`, `doubles.py` attribution flaw); "ember weaker than wonder"; ember x r2 composition; the earlier "0/8 blocking everywhere" | S0 | n/a | `CR:146-148`, `CR:170-174`, `CR:195-200` |

What the study does NOT show (each point verified from the committed tree or quoted source unless tagged):
1. **No product-panel result.** All runs used raw model ids through `tools/run-reviewer.sh` (`claude -p`), not `superclaude review panel` dispatch (`manifest.md:11` per slice 03); only the pilot arms B/C approximate `@default`/`@live7`, and those dropped the Qwen slots.
2. **Ground truth is 16 defects in 3 packages** (designSpec 10 items / 5 `blocking_in_implement`, alias 4 / 3, control 2 / 0; recomputed from `ground-truth.json`: 10/5, 4/3, 2/0). GT items are defects that surfaced during implementation (`evidence` fields cite `.dev/tasks/done/.../progress.md`); a true novel defect scores as a wrong blocker (`PR:79`). No held-out package; 4 of 16 never caught; 3 of 16 carry 89% of catches. S3.
3. **No gate-accuracy measurement**: the metrics are GT coverage and "blocking-flagged row" coverage, not PASS/FAIL agreement with the implementation outcome; real-blocking recall is at most 3 of 8 for any family and 0/8 in the pilot (S3 for pilot).
4. **No multi-round loop evidence**: every ledger is round 1 only (`audit-D/summary.md` X4); the "find once, verify" path of the #346 variants is never exercised (see E3 research).
5. **One judge**: single Opus pass per (row, package); judge variance unmeasured except the unverifiable 12-row re-judge (G15); the judge's "blocking" notion is mis-defined (G4); one known failed judge left a plausible score (`score.json.invalid-apierror`, `CR:146-148`).
6. **No audited-clean evidence for the final recommendation**: AUDIT-CLEAN is buggy (section 4), j1 unaudited (section 6), audits B, C, E, F have no summary (`ls A1/analysis/audits/audit-*/summary.md` = 2 files).
7. **No dollar or input-token cost**: tokens are reviewer OUTPUT tokens (`final-table.py:36` `total_output_tokens_all`), include retried attempts and an auxiliary ~512-token client call (`audit-A/summary.md:22`, 57 claimed vs 54 flags per slice 04 [UNVERIFIED here]); `elapsed` assumes full parallelism.
8. **Reviewer isolation not auditable**: judge and reviewer sessions are not re-runnable from the commit (0 raw transcripts); the sandbox excluded `.dev/tasks/done` etc. (`manifest.md:10`), old-era runs browsed sibling plan packages (25 `X-sibling` WARN, audit C flags).
9. **No test of the proposed harness fixes** (raise the anchor limit; name `source.md` in the brief): `CR:371` lists them as prerequisites; none implemented in `src` at HEAD (`findings.py` limits intact, brief unchanged per slice 01); and j1 shows luna still refuses when a nested input is missing.

**Key Takeaways (grading)**: S3: counts, reproducibility, merge-drop magnitude, judge-blocking inflation. S2: panel ranking among replicated families, default recommendation, source.md non-use. S1: pilot as decision evidence, single-run leaders, control GT1 sonnet effect. S0: re-judge, retracted claims.

## 8. Audits A-F and ground-truth/judge evidence, graded

| Evidence | Committed? | Re-derivable here | Grade |
|---|---|---|---|
| Ground truth (3 `ground-truth.json` + drafts, sha256 in `manifest.md:13-16`) | yes | GT sizes and blocking counts recomputed (10/5, 4/3, 2/0); sha256 not re-computed [UNVERIFIED] | S2 (small, implementation-derived) |
| Blind judge scores (319 `score.json*`, `merged-anon.md`, `label-key.json`) | yes | all 319 parse; 103 rows x 3 packages complete; per-issue counts reproduce `CR:497` | S3 for the data, S2 for the judging (one judge) |
| Judge sessions (`judge.json`) and reviewer raw JSON | no (2,916 files, 1.48 GB left on the original machine) | no | S0 |
| Audit A identity (summary yes) | derived data yes | `E2` flag count 54 vs the summary's "59 WARN", `E11` 1 vs "9" (re-counted with `grep -c`): [CODE-CONTRADICTED] by its own `flags.tsv`; the summary also quotes "930 runs" against "890" | S2 |
| Audit B report validity (no summary) | flags yes | 51 `1-incomplete` and the valid-era 14+2 recomputed | S2 |
| Audit C inputs (no summary) | `runs.json` (890 records) | aggregation 156 of 665 recomputed; detection needs raw JSON | S2 |
| Audit D merges (summary yes) | yes | 80 / 49 / 92 / 3 flips recomputed; 111 vs 92 gap unexplained | S3 for counts |
| Audit E scoring (no summary) | rows.json, flags | the 12-row re-judge has no artifact (0 grep hits); 294 = non-j1 rows (309-15) | S1 |
| Audit F aggregation/statistics (no summary) | `stats.tsv`, `fam.tsv` | not re-run here; `fullpkg()` bug in `final-table.py` found | S2 |

**Key Takeaways (audits)**: only A and D have summaries; D's counts are the only audit result fully recomputable here; E's re-judge is the weakest link in the "scoring is reliable" claim.

## Gaps and Questions

1. [UNVERIFIED] `CR:107`/`SPEC.md:102-103` "428 reviewer files": not a tracked-file count (417 total); the basis is unknown. Question: was 428 counted before the raw transcripts were left out?
2. [UNVERIFIED] "107 entries" for `combos/`: no command here yields 107 (96 dirs, 97 entries, 106 scored runs, 103 scored rows); likely a miscount.
3. [UNVERIFIED] the 17-19 findings dropped with no validity-rule reason (`3-conserve` 111 vs 92; haiku 23 vs 7): not explained here; hypothesis in slice 04 (audit.py and audit2.py parse different blocks) not tested.
4. [UNVERIFIED] the blind re-judge of 12 rows (`CR:296`) and the `check2.py` outputs (judge model identity per score): no artifact; confirm whether any judge other than `claude-opus-5-5` was used.
5. [UNVERIFIED] pilot arm C composition: luna `t4-2` runs for alias and design sit in `quarantine-pre-src-luna/.../_pilot/`; whether they were empty refusals is not opened here. If empty, arm C was a 5-reviewer panel with one empty slot on two packages.
6. [UNVERIFIED] the slice-04 corrected AUDIT-CLEAN table (after fixing `fullpkg()`): I confirmed the bug and the 41/25/3 split but did not recompute the corrected clean table.
7. [UNVERIFIED] `CR:298` statistics (stats.tsv, 48 tests) and the unaudited second-hand audit conclusions (B, C, E, F summaries absent) are read through slice 04 only.
8. [UNVERIFIED] total tokens and the PR token columns (not re-derived here; only walls were), and `audit-A/summary.md:22` "57" vs 54.
9. Question: should the central design treat the E2 recommendation (`ember + 2x luna`) as evidence at all, given that ember skips `source.md` in about half the runs? Answered only partly (G10): a rerun after the harness fixes is the only clean test.
10. Question: is the "NOT CONFIRMED" verdict acceptable with 2 unaudited luna refusals in j1? Yes for the verdict, no for any j1 reliability number (section 6).

## Stale Documentation Found

- **[STALE DOC]** `A1/manifest.md:5` "Worktree branch ... (local, never pushed)": the branch exists on origin at the tip (slice 03; not re-run here).
- **[STALE DOC]** `A1/COMBO-REPORT.md` lines 1-288 still print retracted figures (n2-sonnet-src 8/14 and 5/8, "ember is weaker than wonder", "second run adds nothing", luna pre-source.md results); `CR:289` declares the final section authoritative.
- **[CODE-CONTRADICTED]** `CR:292` "discarded with no error" (code emits a first-error warning; `merge-stdout.txt` shows it), "four verdicts flipped" (3), per-model numbers presented as the 49 blocking findings (they sum to 92); `CR:294` "16 empty terra reviews" (14 terra + 2 luna); `SPEC.md:103` "9 luna-bearing combo rows" (10 in the tree); run-1 hand-off "alias GT3 found once" (alias GT1 found once; GT3 twice); `audit-A/summary.md:22,30` counts (54 and 1 in its own `flags.tsv`); `three-way.py:19` flagged-package output; `final-table.py` `fullpkg()` mapping of the control package.
- **[UNVERIFIED]** `PR:12` "all 3 slots timed out" read as "every Qwen run": a 4th Qwen run finished (2,913 s).

## Summary

The E2 study is strong on counts and weak on inference. Pilot cells, the per-issue table (106 runs), the 71-row distribution, the judge-versus-real blocking gap (65 vs 38), the merge-drop magnitude (92 findings, 49 blocking, 80 reviewer runs, 3 verdict flips) and the committed final table were all re-derived from committed data, with the "92 / 80 / 49" figures resolving to findings, reviewer runs and blocking findings respectively, and with "four flips", "no error" and "16 empty terra" corrected. The panel conclusions are weaker: 3 packages, 16 defects of which 3 carry 89% of the catches, one unrepeatable judge, replicates on the same packages, a buggy AUDIT-CLEAN table, an unaudited batch j1 that does not change the "not confirmed" decision but contains 2 new luna refusals, and nothing that touches the product panel code, multi-round loops or gate accuracy. A central panel design may therefore rely on E2 for the defect list (no silent drops, itemised rejects, refusals as a status, source delivery, real-versus-judge blocking, identity checks) and as a regression fixture, but not for the choice of the default model combination.

