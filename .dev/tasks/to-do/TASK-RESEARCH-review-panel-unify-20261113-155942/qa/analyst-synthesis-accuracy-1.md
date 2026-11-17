# Synthesis Quality Review (Partition 1 of 2): synthesis-accuracy lens

**Date:** 2026-11-14
**Analysis type:** synthesis-review, lens = synthesis-accuracy (checklist items 1-5)
**Files reviewed (assigned_files):** synthesis/synth-01-problem-current-state.md, synth-02-target-gaps.md, synth-03-external-findings.md, synth-04-options-conflicts.md
**Task directory:** .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/
[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

**Method:** read all four files in full; recomputed the Section 4 row counts by script; compared every adversarial result in synth-04 with the four `return-contract.yaml` files; traced claims to research files by grep and line read. Research line numbers below are `research/<file>:<line>` of the files as they stand today. E2 is cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only in all four files (checked by regex over all hex ids: no other E2 commit appears).

**Executor notes handled:** (2) the four debates are written back into synth-04 and each states `partial` with the unaddressed HIGH invariants as open items: accepted as legitimate, no finding. (3) the C14 recount: the older claim survives as measured fact in four places across three files, see findings 1-4. (4) the synth-05 `[CONTRADICTION]` about PENDING/exit 12 is outside this partition (synth-05). (5) E2 commit: clean.

## File 1: synth-01-problem-current-state.md

**Sections covered:** `## 1. Problem Statement` (3 bullets: question, why it matters, trigger), `## 2. Current State Analysis` with 2.1 E1, 2.2 E2, 2.3 E3, 2.4 shared package, 2.5 consumers, 2.6 Current State Summary (overlap matrix, 18 rows).

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 1. Problem Statement` (:23), `## 2. Current State Analysis` (:36); template sub-structure present (The question / Why it matters / Trigger; 2.N Current State Summary at :345; Evidence lines per subsection). |
| 2 Tables | PASS | Overlap matrix columns are exactly Component / E1 / E2 / E3 / Same purpose? / Same data contract? / Same code? / Divergent choices / Evidence (:349); 18 rows. |
| 3 No fabrication | FAIL | 17 claims traced (below); one is worded beyond its source and is contradicted by the C14 recount (finding 1). |
| 4 Evidence cited | PASS | Every subsection ends with an Evidence line; table rows carry file:line and R/S/GQ tags. |
| 5 Options | n/a for this file | |

**Traced claims (synth-01)**

| Synth file | Claim | Research source | Supported? |
|---|---|---|---|
| synth-01 §2.1 (:71) | Stage 2 shadow exit FAIL, 13 of 20 runs, EV-1 8/13 = 0.615 vs legacy 3/39 = 0.077 | R07:197, :272, :515; R11:219 | Yes |
| synth-01 §2.1 (:67) | Legacy card conversion 479 of 712 = 67.28% vs 90% target | scope/04:47 (doc-sourced, labelled so in the file) | Yes |
| synth-01 §2.1 (:68) | `cluster_v2` precision 0.84 (21/25), recall 0.95 (21/22), AI-labelled | R03:240 | Yes |
| synth-01 §2.1 (:69-70) | Legacy 0 of 689 numeric per-finding confidences; shadow 142 of 142; blocking mean 0.80 (n=16) vs 0.66 (n=126) | R05:157-158, :180, :187-188 | Yes (sums of the 14-row table re-added: 142) |
| synth-01 §2.1 (:76) | Spike S-ID: self-report matched pin 0 of 3, transcript honoured 2 of 3, haiku pin ran gpt-6.1-sol | scope/04:80-82 | Yes |
| synth-01 §2.1 (:72) | `cluster_agreement` 1.000 mostly the no-blocking-cluster branch: 11 of 14 runs, shadow09 = 0.9328 | GQ:225 (C-05), GQ:142 (D-19) | Yes |
| synth-01 §2.1 (:73) | 38 of 39 non-shadow pre runs selected Tier 2; 35 of them "through the parsed-sparse pre-filter" | R11:412 (39 files, tier 2 in 38, `parsed-sparse` in 35) | Counts yes; "through the pre-filter" NO: R11 counted files that carry the flag, not runs the flag decided; refuted by the C14 recount (`reviews/adversarial/panel-size-cost/adversarial/return-contract.yaml:27`, `diff-analysis.md:41`, `quant_score.py:42` lists this exact phrase as overstated) |
| synth-01 §2.2 (:86) | 62 reviewer-model sets, 71 valid-era rows, 213 row-packages, about 106 scored runs, 16 known defects over 3 packages (10+4+2) | R11:143; scope/00:12, :71 | Yes |
| synth-01 §2.2 (:110) | 80 reviewer cases, 49 blocking lost (24 anchor, 14 anchor2, 10 claim, 1 refs), 3 flips not 4 | R02:329, :128, :307 | Yes |
| synth-01 §2.2 (:109) | 156 of 665 valid-era runs never opened `source.md` | R06:125, :282 | Yes |
| synth-01 §2.2 (:111) | 195 chained rows among 1398 rows, 83 mega-rows | R03:288, :88 | Yes |
| synth-01 §2.4 (:290) | `tests/review` 651 tests in 19 files (131 + 520), `tests/cli/reflect` 353, skill-text 178, total 1182 | R12:19, :26, :58, :67, :72 (131 + 520 = 651; 651 + 353 + 178 = 1182) | Yes |
| synth-01 §2.5 (:319, :321) | rf-qa family: 43 spawning call sites in 11 skill files; the 19-files/521-lines census is a different unit | R10:234, :229 | Yes |
| synth-01 §2.5 (:329) | `ensemble.py` writes a version "1.0" contract with 33 keys, 11 outside the 1.8.0 lists | R13:29, :178 | Yes (the 11 is also stated in synth-02 MS-13) |
| synth-01 §2.5/2.6 (:362) | 23 of 45 recorded briefs depart from the three-section template | R06:87, :96 | Yes |
| synth-01 §1 (:33) | 94 open gap rows, none Critical, 30 Important | GQ:249 | Yes (the log's own scale; synth-02 §4.1 row 15 explains why the gap table has 15 Critical rows) |
| synth-01 §2.1 (:42) | Kernel is master code (d2d8a2d16); branch is three commits ahead | git log in the task context (HEAD 792cf8c52, c2e3347d3, 9874d63fb) | Yes |

**Per-file verdict: FAIL** (one blocking finding: finding 1).

## File 2: synth-02-target-gaps.md

**Sections covered:** `## 3. Target State` (desired behaviour, 5-consumer table, diagram, success criteria SC-1..SC-17, constraints K-1..K-11, 3.1 external context), `## 4. Gap Analysis` (144 rows in groups D, BL, MS, ENS, OPEN, DOC), 4.1 contradictions (15), 4.2 coverage self-check, 4.3 Critical/Important by track.

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 3. Target State` (:18), `## 4. Gap Analysis` (:99); Desired behavior / Success criteria / Constraints present; C8 rule paragraph and its application note present. |
| 2 Tables | FAIL | Column structure is correct (Gap / Current State / Target State / Severity / Notes) but the table is broken into six blocks by blank lines at :125, :149, :173, :185, :221; a script over all four files found five header-less table starts in this file only (:126 BL-01, :150 MS-01, :174 ENS-1, :186 DOC-01, :222 DOC-36). In GFM, 5 of the 6 blocks render as plain text (finding 6). |
| 3 No fabrication | FAIL | 17 claims traced (below); DOC-59 keeps "same conclusion" after the C14 recount (finding 4). The 4.2 self-check counts were recomputed by script over rows `| **` in :107-:260 and all match. |
| 4 Evidence cited | PASS | Each row cites file:line and a log id; C8 rows carry the remediation-note sentence; the 7 distinct C8 gaps are named. |
| 5 Options | n/a for this file | |

**Traced claims (synth-02)**

| Synth file | Claim | Research source | Supported? |
|---|---|---|---|
| synth-02 D1 (:109), SC-2 (:53) | 49 blocking findings lost (24, 14, 10, 1), 3 flipped merges | R02:329, :128 | Yes |
| synth-02 SC-5 (:56) | Suites G8 82 tests and G9 271 tests; 110 + 27 key lists | R12:276-277; R07 (key lists) | Yes |
| synth-02 D4 (:112), SC-10 (:61) | 65 judge-blocking vs 38 real over 71 valid-era rows | R05:310 | Yes |
| synth-02 D6 (:114), SC-6 (:57) | 195 chained among 1398 rows (1398 is all rows), 83 mega-rows | R03:288 | Yes |
| synth-02 DOC-19 (:204) | `cluster_agreement`: 11 of 14 shadow runs 1.0 (no blocking cluster), shadow09 0.9328, shadow02/04 null | GQ:142 (D-19), GQ:225 (C-05) | Yes |
| synth-02 D8 (:116) | 156 of 665 valid-era runs never opened `source.md`; causal link unverified | R06:125, :282 | Yes |
| synth-02 MS-05 (:154) | 22 of 45 recorded briefs follow the template, 23 deviate | R06:87 | Yes |
| synth-02 BL-20, DOC-54 (:145, :240) | 43 spawning call sites in 11 skill files; 521 vs 591 vs 997 are counts in other units | R10:234, :229 | Yes |
| synth-02 MS-13 (:162) | `ensemble.py` contract has 33 keys, 11 in neither lint list; 3 shadow contracts unparseable | R13:178; R07 §7.1 | Yes |
| synth-02 DOC-43 (:229) | `tests/cli/reflect` 37 files, 353 tests; surface 1182 | R12:72, :19 | Yes |
| synth-02 MS-12 (:161), SC-16 | Stage 2 exit FAIL, 13 of 20, EV-1 8/13 = 0.615 vs 3/39 | R07:197, :272 | Yes |
| synth-02 MS-16 (:165) | Legacy 0 of 689, shadow 142 of 142 | R05:157, :180 | Yes |
| synth-02 K-2 (:75), BL/ENS-9 (:182) | `--reviewers` accepts up to 4 against the C11 cap of 3 | GQ:89 (G-67) | Yes |
| synth-02 §4.2 (:283-285) | 144 rows; Critical 15 / Important 65 / Minor 64; tracks M1 56, M2 20, M3 18, M4 16, none 34 | recomputed by script over :107-:260 | Yes, exact |
| synth-02 §4.2 (:285) | 15 Critical rows named by track | script listing: D1 D3 D4 D14 MS-11 MS-14 ENS-1..5 DOC-20 DOC-63..65 | Yes |
| synth-02 §3.1 (:90) | Union voting 82.7% recall, 85.0% FPR vs weighted 37.7% / 35.3% | web-01:22 | Yes |
| synth-02 DOC-59 (:245) | MR:142's 37 of 38 / 34 superseded by the recount 38 of 39, 35 "(same conclusion)" | GQ:182 (D-59, same wording, written before the C14 debate); R11:412 | Counts yes; "same conclusion" NO: the C14 debate overturned the flag-driven conclusion (return-contract.yaml:27, refactor-plan.md:13) |

**Per-file verdict: FAIL** (finding 4 and finding 6 are blocking).

## File 3: synth-03-external-findings.md

**Sections covered:** `## 5. External Research Findings`: reading notes, 5.1 panel aggregation, 5.2 severity, 5.3 judge calibration, 5.4 fingerprinting, 5.5 External Research Summary (takeaways, contradictions, exclusions, gaps, consolidated options).

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS | `## 5. External Research Findings` (:8); 5.N External Research Summary present (:306); the template's Finding / Source / Relevance / Relationship fields are kept as table columns, with an added Date column. |
| 2 Tables | PASS | Every finding table uses Finding / Source / Date / Relevance / Relationship to codebase; tags `[E] [A] [S] [2] [V] [U]` are defined at :17. |
| 3 No fabrication | FAIL | 15 claims traced (below). One statement about E1 calibration is wrong against R05 and contradicts synth-01 (finding 5); it is inherited from web-03:11. |
| 4 Evidence cited | PASS | Each row carries a URL, a verification tag and a research-file relation; excluded or unverified items are listed at :341-353. |
| 5 Options | PASS | 5.1.5, 5.2.5, 5.3.6, 5.4.5 and 5.5.5 give external options labelled "options, not decisions". |

**Traced claims (synth-03)**

| Synth file | Claim | Research source | Supported? |
|---|---|---|---|
| synth-03 5.1.1 (:31) | MultiVer union voting 82.7% recall, 48.8% precision, 85.0% FPR | web-01:22 | Yes |
| synth-03 5.1.1 (:33) | Self-Agg n=10: F1 21.91% (+43.67%), recall +118.83% | web-01:34 | Yes |
| synth-03 5.1.2 (:44) | 294 defects, 56.8% (167 of 294) found by one model, Jaccard 0.29, coverage 47% to 72% | web-01:98 | Yes |
| synth-03 5.1.2 (:41) | Cursor resolution rate 52% to 70% (secondary, self-reported) | web-01:79-80 | Yes |
| synth-03 5.3.1 (:175) | Nine judges: Kish 2.0-2.5, 8-22 points below independent, 11% of gap, phi 0.437/0.435 vs 0.389, 0.603 | web-01:60 | Yes |
| synth-03 5.3.1 (:174) | PoLL kappa 0.763 vs 0.627; GPT-4 0.518 to 0.725 | web-01:54; web-03:92, :108 | Yes |
| synth-03 5.3.1 (:178) | Fuser +47.14% accuracy, -53.73% ECE | web-03:157 | Yes |
| synth-03 5.3.3 (:205) | Xiong: AUROC about 62.7% | web-03:136, :215 | Yes |
| synth-03 5.3.3 (:208) | Ferrer ECE 0.166 vs 0.229, AUC 0.668 | web-03:164-165 | Yes |
| synth-03 5.4.3 (:279) | Closure 64% precision vs 97% pairwise at 0.65; black-hole threshold | web-04:119, :197 | Yes |
| synth-03 5.4.3 (:280) | VL-Dedup: cap off 64 to 598 records; K=5 cut F1 0.998 to 0.299; snippet-only `[S][U]` | web-04:126 | Yes |
| synth-03 5.4.1 (:255) | CodeQL hash: 100 non-space characters, `:n` suffix | web-04:167 | Yes |
| synth-03 5.4.1 (:256) | SARIF limits 1,000 locations per result, 25,000 results per run | web-04:62 | Yes |
| synth-03 5.2.1 (:86) | SARIF `level` has four values, three of them severities | web-02:20-26, :28 | Yes (and consistent with synth-02's "three buckets") |
| synth-03 5.3 intro (:168), 5.3.3 (:205) | "shadow runs recorded 0 numeric per-finding calibrations of 689 findings"; "zero numeric calibrations in shadow runs" | web-03:11 repeats it; R05:155-180 says legacy 0 of 689, shadow 142 of 142 | NO: wrong population (finding 5) |

**Per-file verdict: FAIL** (finding 5 is blocking).

## File 4: synth-04-options-conflicts.md

**Sections covered:** `## 6. Options Analysis (conflict log)`: 6.0 conflict index (C01-C20), C-01 to C-20 blocks (each: effort/position/evidence table, options with Aspect/Assessment tables, evidence list, status, recommended resolution, adversarial result), 6.D defects D1-D16, 6.X overall design options A/B/C, Options Comparison, recommended design.

| Check | Result | Evidence |
|---|---|---|
| 1 Headers | PASS (note) | `## 6. Options Analysis (conflict log)` (:1) carries a suffix not in the template (finding 8, MINOR); `### Options Comparison` (:1441) present. |
| 2 Tables | PASS | Every option has Aspect / Assessment with Effort, Risk, Reuse of existing code, Files/systems affected, Pros, Cons; Options Comparison uses Criterion / Option A / Option B / Option C (:1443). |
| 3 No fabrication | FAIL | 16 claims traced (below). The four adversarial result paragraphs match their `return-contract.yaml` files on scores, convergence, status, invariant ids/counts and unresolved ids. The C14 block contradicts itself (findings 2 and 3). |
| 4 Evidence cited | PASS | Evidence bullets carry research section and file:line, with [E1]/[E2]/[E3] and [CODE-VERIFIED]/[DOC-SOURCED] tags. |
| 5 Options | PASS | C-01..C-20: every conflict has 3 options (C-05 has 5) each with an assessment table; the overall design options A/B/C have tables and a comparison table. Required C01-C14 coverage complete. |

**Option and table coverage for C01-C14 and overall options**

| Conflict | Options with Aspect/Assessment tables | Status text | Adversarial result matches contract? |
|---|---|---|---|
| C-01 | A, B, C | DECIDED | n/a |
| C-02 | A, B, C | DECIDED | n/a |
| C-03 | A, B, C | UNDECIDED, resolved by debate | Yes: winner A, 0.9167 vs 0.8798, margin 3.7%, convergence 0.86 (25 of 29), INV-009/INV-013, unresolved S-007 C-001 C-006 X-003 (return-contract.yaml, model-tier-config) |
| C-04 | A, B, C | DECIDED | n/a |
| C-05 | A, B, C, D, E | UNDECIDED, resolved by debate | Yes: winner B (Option D) by tiebreaker, 0.9091 vs 0.8810, convergence 0.909 (30 of 33), 11 HIGH invariants (INV-001/004/005/011/014/019/020/021/023/024/025), unresolved C-005 C-012 X-002 |
| C-06 | A, B, C | DECIDED | n/a |
| C-07 | A, B, C | DECIDED | n/a |
| C-08 | A, B, C | DECIDED | n/a |
| C-09 | A, B, C | DECIDED | n/a |
| C-10 | A, B, C | DECIDED | n/a |
| C-11 | A, B, C | DECIDED | n/a |
| C-12 | A, B, C | DECIDED | n/a |
| C-13 | A, B, C | UNDECIDED, resolved by debate | Yes: winner B narrowly, 0.9804 vs 0.9724, 14 vs 10 points, convergence 0.89 (33 of 37), 10 HIGH invariants INV-001..010, unresolved S-006 C-013 A-002 A-004 |
| C-14 | A, B, C | UNDECIDED, resolved by debate | Result paragraph yes: winner B, 0.9256 vs 0.9194, 6 to 4, convergence 0.80 (24 of 30), 3 HIGH (INV-009/012/013), unresolved S-002 S-006 C-003 C-010 C-013 C-016. But the same block's evidence and option text contradicts the paragraph (findings 2, 3) |
| 6.X | A, B, C + Options Comparison | n/a | n/a |

**Traced claims (synth-04)**

| Synth file | Claim | Research source | Supported? |
|---|---|---|---|
| synth-04 C-02 (:150, :132) | 49 lost blocking findings, 48 by length (24 + 14 + 10), 1 refs; all dropped: anchor 56, anchor2 18, claim 14 | R02:329 | Yes |
| synth-04 C-03 (:215-216) | `--env gateway` reflect template fails "launch None is not one of sonnet, opus, haiku"; haiku slot served by gpt-6.1-sol | R04:119, :96, :122 | Yes |
| synth-04 C-05 (:311, C-13 :834) | 0 invariant violations over 264 E2 merges | R02:146; R05:297 | Yes |
| synth-04 C-05 (:297, :371) | 65 judge-blocking vs 38 real over 71 rows | R05:310 | Yes |
| synth-04 C-05 (:368, :375) | Convergence 1.0 in 9 of 14 runs; 6 of 14 merges inline; cluster_agreement 1.0 in 10 of 11 | R07:351, :360 | Yes as recorded (denominator differs from synth-01, finding 9) |
| synth-04 C-05 (:326) | B3 found in 95 of 106 runs, I8 76, I2 71 | R11:147 | Yes |
| synth-04 C-06 (:437) | 142 of 142 shadow findings calibrated; 0.80 vs 0.66 (n=16 vs n=126) | R05:180, :187-188 | Yes |
| synth-04 C-10 (:642) | 156 of 665; 23 of 45 briefs depart; 0 of 45 carry the verbatim line | R06:125, :87-88 | Yes |
| synth-04 C-12 (:770) | 195 chained of 1398; 83 mega-rows | R03:288 | Yes |
| synth-04 C-17 (:1096) | 0 of 48 recorded post run directories carry a findings block | R07:376 | Yes |
| synth-04 C-20 (:1290) | Stage 2 exit FAIL, 13 of 20, EV-1 8/13 = 0.615 vs 3/39, 6 parity and 9 lint/manifest failures | R07:197, :272, :515 | Yes |
| synth-04 C-13 (:891) | F5 "empty findings block counts as a valid review" among INV-010 falsifiers; plan reviewer 21 findings | reviews/adversarial/ledger-model/adversarial/round25-fault-finder-raw.md:111; refactor-plan-review.md:149 | Yes |
| synth-04 C-09 (:578) | 6 of 9 tier3-orchestrated pilot runs collapsed to the Sonnet alias; combo A3 collapsed | R04:210-211 | Yes |
| synth-04 C-16 (:1045, :1080) | 26 of 42 MAJOR findings `blocking: false` in 13 shadow runs; 16 `blocking: true` | R05:186-189, :231 | Yes |
| synth-04 C-14 (:926, :941, :944) | "Acts on the measured driver of Tier 2 spend (35 of 39 parsed-sparse)"; "Pays Tier 2 on 38 of 39 plans for an input-format reason"; "mostly for an input-format reason ... [CODE-VERIFIED in data]" | R11:412 counts only | Counts yes; causal claim NO (return-contract.yaml:27; diff-analysis.md:41; refactor-plan.md:13 "must not repeat '35 of 39 escalate because of the flag', '34 by the pre-filter'") |
| synth-04 C-10 (:691) | "Parsed-sparse escalation sends nearly every workflow plan to Tier 2" | R06:98 (mechanism claim); R06:255 marks the count UNVERIFIED; R11:412 counts only | NO as measured fact (finding 3) |

**Per-file verdict: FAIL** (findings 2 and 3 are blocking).

## Findings

CRITICAL and IMPORTANT are blocking; MINOR are notes. The C14 recount facts used for findings 1-4: the parsed-sparse flag was set in 35 of 39 non-shadow runs (34 of the 38 Tier 2 runs) and was decisive in 0 for certain and at most 1; 29 of the 34 flagged Tier 2 runs also have a recorded escalate row 4, 5 or 6 (`reviews/adversarial/panel-size-cost/adversarial/return-contract.yaml:27`; `refactor-plan.md:13` states the only allowed wording; `quant_score.py:42` names "through the parsed-sparse pre-filter" as overstated). `research/11-evaluation-evidence.md:412` supports only the counts (39 files, tier 2 in 38, `parsed-sparse` in 35).

| # | Severity | Synth file | Section | Finding | Proposed fix |
|---|---|---|---|---|---|
| 1 | CRITICAL | synth-01 | 2.1 "Current measurements and state", row "Tier 2 is the typical path" (:73) | Says "35 of them through the parsed-sparse pre-filter". This is the exact phrase the C14 debate marked as overstated; it presents the older claim (Tier 2 driven by the flag) as measured fact, tagged `[CODE-VERIFIED in data]`. R11:412 counted files carrying the flag, not runs the flag decided. | Reword: "38 of 39 non-shadow pre runs selected tier 2; the parsed-sparse flag was set in 35 of 39 and was decisive in 0 for certain and at most 1 (recount 2026-11-13, C14 debate); the data counts runs, not the cause". Keep the strength cell "measured census of counts; cause not established". |
| 2 | CRITICAL | synth-04 | C-14 (:897, :926, :941, :944) | The block contradicts its own "Adversarial result" (:956, which says A's "35 of 39 escalate because of the flag" is overstated). Option B Pros (:926): "Acts on the measured driver of Tier 2 spend (35 of 39 parsed-sparse)"; Option C Cons (:941): "Pays Tier 2 on 38 of 39 plans for an input-format reason, not plan risk"; Evidence bullet 1 (:944): "mostly for an input-format reason ... 35 by the parsed-sparse pre-filter ... same conclusion ... [CODE-VERIFIED in data]"; E1 cell (:897) lists "34 by the pre-filter" with the recount as if it confirmed it. All state the refuted cause as measured. Option B's Con (:927, "those 35 plans") inherits the premise. | Rewrite :926 to "Targets the rubric lever (O-8); the flag was set in 35 of 39 runs but decisive in at most 1, so the saving is unproven (Phase 1 is conditional, see the resolution)". Rewrite :941 to "Pays Tier 2 on 38 of 39 plans; the flag is not shown to be the reason". Rewrite :944 to the figure rule of `refactor-plan.md:13`: "flag set in 35 of 39 runs, decisive in 0 certain and at most 1", drop "same conclusion", change the tag to [CODE-VERIFIED in data] for the counts only. In :897 add "set in 35, not shown decisive" after the recount. Reword :927 to "plans that carry the flag". |
| 3 | CRITICAL | synth-04 | C-10 Evidence bullet 4 (:691) | "Parsed-sparse escalation sends nearly every workflow plan to Tier 2, so the Tier 2 source-exposure rule applies to almost every run (06 §2.3; 11 §12)". Presents the older causal claim as fact; R06:255 itself marks the count behind it UNVERIFIED and R11:412 gives counts only. | Reword to the supportable part: "Tier 2 was selected in 38 of 39 recorded non-shadow pre runs (11 §12), so the Tier 2 brief source-exposure rule applies to nearly every recorded run whatever the cause". |
| 4 | IMPORTANT | synth-02 | 4 Gap table, DOC-59 (:245) | "Superseded by the 2026-11-13 recount: 38 of 39, 35 (same conclusion)". "Same conclusion" re-endorses the flag-driven conclusion that the C14 debate overturned; copied from the log row D-59 (GQ:182), which predates the debate. Rated Minor and `Track: none (drop: recount)`, so no row carries the correction. synth-06 rows V-316, V-366, V-673 already use the corrected wording, so synth-02 is the outlier. | Replace with "Counts superseded by the 2026-11-13 recount (38 of 39 selected Tier 2; flag set in 35, decisive in 0 certain and at most 1). The older 'driven by the flag' conclusion is not carried (C14 debate, synth-04 C-14)". |
| 5 | IMPORTANT | synth-03 | 5.3 intro (:168) and 5.3.3 row 5 (:205) | States that E1 "shadow runs recorded 0 numeric per-finding calibrations of 689 findings" and that "zero numeric calibrations in shadow runs is a small loss of evidence". R05:155-180: the legacy recorded cards carry 0 of 689; the shadow runs carry 142 of 142. synth-01 (:69-70) and synth-04 C-06 (:437) state the correct split, so the synthesis set contradicts itself. The error is inherited from web-03:11, but synth-03 :6 promises code facts "as recorded in research/01 to research/12". | In :168 write "legacy recorded cards carried 0 numeric per-finding calibrations of 689 findings; shadow runs carry 142 of 142 (R05 §5)". In :205 replace "in shadow runs" with "in the recorded legacy cards" and drop the "small loss of evidence" inference or restate it for the legacy cards. |
| 6 | IMPORTANT | synth-02 | 4 Gap Analysis table (:107-:221) | The Gap table is split by blank lines at :125, :149, :173, :185 and :221, leaving five header-less blocks (starts at BL-01, MS-01, ENS-1, DOC-01, DOC-36). The template requires one `Gap / Current State / Target State / Severity / Notes` table; in GFM the 5 later blocks render as plain text, so most of the 144 rows lose table form. Checked by script: no other synth file in this partition has this defect. | Delete the five blank lines (or repeat the header and separator row at each break) so the 144 rows form one table. Do not change row text. |
| 7 | MINOR | synth-04 | 6.X Assessment summary (:1439) | Lists "C01, C02, C04, C07-C12, C15, C16, C18-C20 decided; C03, C05, C13, C14 open". It omits C06 and C17 (both DECIDED-BY-EVIDENCE in 6.0 :20, :31; 14 listed, 16 decided) and calls C03/C05/C13/C14 "open" although 6.0 records them as resolved by debate with status `partial`. | Write "C01, C02, C04, C06-C12, C15-C20 decided by evidence; C03, C05, C13, C14 resolved by adversarial debate (partial, HIGH invariants open)". |
| 8 | MINOR | synth-04 | Header (:1); 6 overall | Header reads `## 6. Options Analysis (conflict log)`; the template and the task text use `## 6. Options Analysis`. Only one Options Comparison table exists (overall options), none per conflict; that matches the template, so this is a note. | Keep the suffix as a subtitle line below a plain `## 6. Options Analysis` header at assembly. |
| 9 | MINOR | synth-04 | C-05 Evidence bullet 5 (:375) | Gives `cluster_agreement` 1.0 "in 10 of 11" (R07:360). synth-01 :72 and synth-02 DOC-19 (:204) give 11 of 14 runs, mostly the no-blocking-cluster branch, with shadow02/04 null and shadow09 0.9328 (GQ:225, :142). Both are traceable; the different denominators are not reconciled and :375 omits the no-blocking-cluster caveat. | Add "(11 of 14 shadow runs per GQ C-05, mostly the no-blocking-cluster branch)" or restate with one denominator. |

Items checked and not defects: the four adversarial result paragraphs in C-03, C-05, C-13, C-14 match their return contracts (scores, convergence, invariant ids and counts, unresolved ids); each states `partial` and the unaddressed HIGH invariants as open, as the executor note allows. The synth-02 note that the gap table has 15 Critical rows while the log has none is flagged explicitly (synth-02 §4.1 row 15), so it is not a silent inconsistency. synth-03's "SARIF level has four values" and synth-02's "three buckets" agree with web-02:20-28. E2 is cited at commit 4a22d742... only.

## Summary

- Files reviewed: 4; files passing: 0; files failing: 4 (synth-01: finding 1; synth-02: findings 4 and 6; synth-03: finding 5; synth-04: findings 2 and 3).
- Findings: CRITICAL 3, IMPORTANT 3, MINOR 3. Blocking: 6.
- Claims traced: 17 (synth-01), 17 (synth-02), 15 (synth-03), 16 (synth-04) = 65; 60 supported, 5 not supported or only partly supported (synth-01 :73, synth-02 DOC-59, synth-03 :168/:205, synth-04 :926/:941/:944, synth-04 :691).
- All blocking findings are wording or formatting fixes; none requires new research. Findings 1-4 should be fixed together with one grep for `parsed-sparse` over synth-01 to synth-04 afterwards.

## Verdict: FAIL

