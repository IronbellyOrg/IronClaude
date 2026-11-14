# QA Report - Synthesis Gate, structure lens (Partition 1 of 2)

**Topic:** Unified central Review Panel (E1 reflect Tier 2 panel, E2 tasklist review-panel study at 4a22d74213f93837d00c2c314075dd967b9a98e3, E3 #346 review loop)
**Date:** 2026-11-14
**Phase:** synthesis-gate (structure lens, items 1-6 plus required-content check)
**Fix cycle:** N/A (first review)
**Assigned files:** synth-01-problem-current-state.md, synth-02-target-gaps.md, synth-03-external-findings.md, synth-04-options-conflicts.md
**Fix authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

Three blocking findings (all IMPORTANT) are open: B-1 (the older "Tier 2 driven by the parsed-sparse flag" claim is still stated as measured fact in synth-01, synth-02 and synth-04), B-2 (the Gap Analysis table in synth-02 is cut into six pieces, five of them without a header row), B-3 (synth-03 says shadow runs recorded 0 of 689 per-finding calibrations; the research and synth-01 say legacy runs 0 of 689 and shadow runs 142 of 142). Everything else in the lens passed. Minor notes N-1 to N-7 are recorded and never fail the gate.

## Required-content result (blocking if missing)

| Required item | Result | Evidence |
|---|---|---|
| (a) Overlap matrix in synth-01 Section 2.6 with all eighteen component rows | PRESENT, 18 of 18 | Rows 1-18 at synth-01 lines 351-368: finding contract, severity scale, parser limits, clustering, merge and ledger, verdict and blocking, calibration, panel templates, tier and class config, identity check, dispatch, brief and input contract, run manifest, telemetry, audits, shadow harness, evaluation harness, tests. Columns: E1, E2, E3, same purpose, same data contract, same code, divergent choices, evidence (matches BUILD-REQUEST line 14). |
| (c) Conflict log in synth-04 with C01-C14 at minimum | PRESENT, C01-C20 (20 of 20) | `grep -c '^| C[0-9][0-9] |'` = 20 index rows; `grep -c '^### C-[0-9]*:'` = 20 sections. |
| (c) Per conflict: 2 or more options, evidence, ONE Status marker, a recommended resolution | PRESENT for all 20 | Script counts: 20 `**Status:**`, 20 `**Recommended resolution:**`, 20 `**Adversarial result:**`; options per conflict = 3 (C-05 = 5), each with an Aspect/Assessment table holding Effort, Risk, Reuse, Files, Pros and Cons rows (Pros and Cons row counts equal the option count in every conflict). |
| (c) D1-D16 in Section 6.D | PRESENT, 16 of 16 | `grep -c '^| D[0-9]* '` = 16 rows with columns Defect, Current behaviour, Options, Recommended fix, Tests that must change, Status. |
| The four debates (C03, C05, C13, C14) written back, open items stated as open | PRESENT and honest | Each Status line reads "UNDECIDED-BY-EVIDENCE, resolved by adversarial debate (partial ...)"; each "Adversarial result" lists the unresolved diff points and unaddressed HIGH invariants. Numbers match the four `return-contract.yaml` files (C03 0.86, 25 of 29, 4 unresolved, 2 HIGH; C05 0.909, 30 of 33, 3 unresolved, 11 HIGH with the same eleven INV ids; C13 0.89, 33 of 37, 4 unresolved, 10 HIGH; C14 0.80, 24 of 30, 6 unresolved, 3 HIGH). |
| E2 cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | HOLDS | Hash scan of the four files shows only that E2 hash (and the `4a22d742` short form); no other E2 commit. |

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match the Report Structure template | PASS | Template read at `~/.claude/skills/tech-research/SKILL.md:1336-1493`. synth-01 has `## 1. Problem Statement` (bullets The question / Why it matters / Trigger) and `## 2. Current State Analysis` with `### 2.1`-`2.5` each ending in an `**Evidence:**` line and `### 2.6 Current State Summary` (template `2.N`). synth-02 has `## 3. Target State` (Desired behavior / Success criteria / Constraints) and `## 4. Gap Analysis`. synth-03 has `## 5. External Research Findings` and `### 5.5 External Research Summary` (template `5.N`). synth-04 has `## 6. Options Analysis (conflict log)`, per-option `#### Option` blocks and `### Options Comparison`. Extra sub-numbering (6.0, 6.D, 6.X, 3.1, 4.1-4.3) is additive. |
| 2 | Table column structures | FAIL | Gap table header `Gap / Current State / Target State / Severity / Notes` is correct, and Options Comparison is `Criterion / Option A / Option B / Option C` (plus two extra rows), and every option table is `Aspect / Assessment`. BUT the Gap table is broken by blank lines at synth-02 lines 125, 149, 173, 185 and 221 (script: blank line followed by a pipe row at those five places); the pieces after each blank line have no header and no separator row, so 128 of 144 gap rows do not form a table (finding B-2). |
| 3 | No fabrication (trace at least 8 claims per file) | FAIL | More than 60 claims traced, at least 10 per file (detail in the next section). Every traced claim matched the research file or the code at HEAD 792cf8c52 except two groups: B-1 (the stale causal claim about the parsed-sparse flag) and B-3 (a calibration count attributed to the wrong run set). |
| 4 | Evidence citations use real paths (parent directory exists) | PASS | Script extracted 143 backticked path tokens from the four files; every token that is a real path resolved (repo file, `~/.claude` file, task-dir file, or E2 tree file via `git ls-tree` at 4a22d742; glob and placeholder tokens containing `*`, `{` or `<` were skipped by design). The 24 tokens that did not resolve are not file paths: shorthand (`AD/...`, `COMBO/PLAN.md`, `shadow01/reviewer-2.md` = run-dir shorthand, `research/12`, `research/13`), branch names (`ironbelly/shadow-runs`, `origin/master`, `feat/review-panel`), repo slugs, schema ids (`review-ledger/1` and similar), and ellipsis placeholders. Directories confirmed: `.dev/reflect/pre-...-shadow01`, `.dev/reflect/pre-...-shadow09`, `.dev/experiments/346-validation/phase5/final-bundle/`, `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py`. |
| 5 | Options analysis: every conflict and the overall design has 2 or more options with pros/cons tables; an Options Comparison table exists | PASS | Script: C-01 to C-20 each have 3 options (C-05 has 5) with Pros and Cons rows; section 6.X has Options A-C with Pros/Cons; `### Options Comparison` table at synth-04 lines 1441-1451 with Effort, Risk, Maintainability, Integration complexity, Reuse potential and two future-consumer rows. 6.D gives per-defect Options and Recommended fix. |
| 6 | Implementation-relevant fixes are specific (file paths, not generic steps) | PASS | 6.D rows name `file:line` for current behaviour and name the tests to change (for example D2 `test_review_ledger.py:376-385`, D11 two golden fixtures); option tables list "Files/systems affected" by file name; gap rows D1-D16 carry file:line plus the test pins. No generic "create a service" style step found. |
| R-a | Overlap matrix, 18 rows | PASS | See required-content table. |
| R-c | Conflict log C01-C14+, options, evidence, one Status, recommended resolution; D1-D16 | PASS | See required-content table. |

---

## Check 3 trace detail (claims verified per file)

Worktree HEAD is `792cf8c52` on `ironbelly/shadow-runs`, the same commit the synthesis cites.

**synth-01 (13 groups traced, all hold except B-1).**
1. 94 open gaps, 0 Critical, 30 Important, 64 Minor: `gaps-and-questions.md:249` matches.
2. 651 tests in 19 files (131 + 520), 353 reflect tests, 178 skill-text tests, 1182 total: `research/12:19,32,58`; `ls tests/review/test_*.py` = 19 (file count of `tests/cli/reflect` differs, see N-2).
3. 23 of 45 recorded briefs depart from the three-section shape: `research/06:87`.
4. Legacy per-finding calibration 0 of 689, shadow 142 of 142: `research/05` section 5 heading and 5.1.
5. Line counts of fifteen `cli/review` and `cli/reflect` files, `scripts/reflect_shadow_exit.py` (410), `spec-panel.md` (490), the rules prompts file (74), reflect `SKILL.md` (2033), `reviewer-spec.md` (116): `wc -l` matches every figure.
6. Definition lines: `findings_v2.check_finding` 84 and `parse_block` 215; `cluster.annotate` 126, `same_defect_v2` 161, `cluster_v2` 381, `clusters_kept` 447; `contract.derive_verdict` 138, `_degraded_reason` 263, `_halted_reason` 361; `ledger.merge_round` 107, `apply_revision` 301, `defer` 350, `verdict` 363, `capture` 375, `render_merged_report` 408: all match.
7. E2 file sizes at 4a22d742 (`run-reviewer.sh` 87, `judge-one.sh` 31, `final-table.py` 83, `three-way.py` 63, `COMBO-REPORT.md` 506, audit A summary 34 and `audit.py` 171, audit D summary 90 and `audit.py` 239) and the six audit directories: `git show` / `git ls-tree` match. `run-reviewer.sh:48` (deny list under bypassPermissions), `:58` (expected_model written), `:76` (overwritten on fallback), `:87` (cost glob): match.
8. Installed experiment variants: `spec-panel-ledger.md` 475, `-stoprule` 481, `-diffgate` 481, `-ponytail` 483, `-armb` 472, `review_ledger.py` 2668, `stoprule.py` 2050, `finding-grader.md` 35, `sc-review-ledger/SKILL.md` 118: match.
9. E2 report claims: 65 judge-blocking vs 38 real over 71 rows (`COMBO-REPORT.md:291`), 80 reviewer-level cases and 49 blocking findings lost (`:292`), 156 of 665 runs never opened `source.md` (`:373`): match.
10. `runner.py:538-545` (`run_tier2_ensemble(config)` then `rc = 0` at 544-545), `ensemble.py:773` (merge_method from reviewer count), `:74` (`REFLECT_CONTRACT_VERSION = "1.0"`), `:894` (`yaml.safe_dump`), `commands.py:255` (`Choice(["standard","deep"])`): match.
11. Tier counts re-run over `.dev/reflect/pre-*/artifacts/tier_decision.yaml` excluding shadow dirs: 39 files, `selected_tier: 2` in 38, `parsed-sparse` present in 35. The numbers hold; the causal wording does not (B-1).
12. Commit facts: d2d8a2d16, 9874d63fb, c2e3347d3, 792cf8c52, 9163bd1c7, 5d9a0ae70, 77e0a7029 exist with the cited subjects; `git diff --stat d2d8a2d16 HEAD -- src/superclaude/cli/review tests/review` and `git diff --stat origin/master HEAD -- src/superclaude/cli/review` are empty; `d2d8a2d16..c2e3347d3` touches exactly four files (SKILL.md, reviewer-spec.md, two reflect tests).
13. `reviewers.py:41` `REVIEWERS = ("augment", "codex")`: matches. Arithmetic checks: 479/712 = 67.28%, 21/25 = 0.84, 21/22 = 0.95, 8/13 = 0.615, 3/39 = 0.077, 16 + 126 = 142: all correct.

**synth-02 (14 groups traced, all hold except B-1 in DOC-59).**
1. D2: clearing loop `ledger.py:254-258` never reads `block_ok`; docstring `:112` says the opposite; `test_review_ledger.py:376-385` ends with the `resolved` assertion at 385.
2. D3: `ledger.py:150-152` raises only when no reviewer block is valid; `:273-274` `verdict = "FAIL" if brief else "PASS"`.
3. D7: `findings.py:29` `_REF_TOKEN` and `telemetry.py:23` `_ID_TOKEN` (`:22` is `_TS`, `:24` is `_ID_RE`, as DOC-16 says).
4. D11: `panel.py:536-543` (`pool = candidates` at 543 when not hard); D12: `select_env` `panel.py:485-494` reads `$T3Model01`.
5. D13: `__init__.py:19-36`, names `lint_cmd` and `estimate_cmd` at lines 24-25, swallow at 30-35.
6. D15: `STRATA = (` at `telemetry.py:112`, check at `:267`.
7. `findings_v2.py:107-108` (MINOR cannot be blocking) and `:161-162` (label rule with `reflect_category`); `findings.py:14,104,108,118` limits.
8. BL-14: `reviewers.py:41`; BL-16/17: `severity_router.py:174-175` (low confidence drops a tier), `:191-193` (`if deep:` drops a tier); `fsm.py:941` `verify: Callable[[Finding], bool]`.
9. ENS-1/ENS-6: `runner.py:538-545`, `ensemble.py:773`; K-2: `config.py:335` clamps reviewers to 2..4.
10. BL-19: `rf-qa.md:41` ("A QA pass that finds zero issues is suspect") against `:92` ("no minimum count"); BL-03 `rf-qa.md:111`; BL-11 `rf-qa.md:403-418` halts.
11. MS-11/DOC-20: `SKILL.md:348` step 9 names `identity_source: observed`; `SKILL.md:87` rejects `--t2-engine panel`; `SKILL.md:338,340` shadow steps.
12. `reflect-reviewer.md:5-8` (read-only tool list, `model: sonnet` at 6, `permissionMode: plan` at 8).
13. Table arithmetic recomputed by script: 144 gap rows (D 16, BL 23, MS 23, ENS 9, OPEN 2, DOC 70 + 1 combined row), Critical 15, Important 65, Minor 64; the Section 4.3 per-track lists add up to 65 Important and the 15 Critical.
14. `rf-qa.md:84,86` synthetic-dnsp HIGH; `rf-qa.md:450` issues table format: match.

Not independently re-traced in synth-02: the K-row constraints (K-1 to K-11) and the SC-row test names, which I read for consistency with synth-01 and synth-04 only.

**synth-03 (27 numeric or named claims traced against `research/web-01` to `web-04`, all hold except B-3).** 82.7% recall and 48.8% precision (web-01), 56.8% and 167 of 294 (web-01), GPT-4o 98.2% against 59.1% (web-01), 2.8% minority-veto error (web-01), Kish ESS and phi 0.437 (web-01), 37,448 pairs and 89.6% (web-03), 26% ownership bias (web-03), AUROC 62.7% (web-03), ECE 0.166 (web-03), fuser +47.14% (web-03), 598 records and F1 0.299 (web-04), 64% precision (web-04), `primaryLocationLineHash` (web-04), 1,000 locations and 25,000 results (web-04), SonarQube 10.2 mapping and "not ideal" (web-02), CodeRabbit Quiet profile (web-02), Star Chamber (web-01), arXiv 2602.02219 (web-03), SureA11y issue (web-04). SARIF "four values" (synth-03) against "three buckets" (synth-02) is consistent: `web-02:18-28` says "four values, three of them severities". The calibration sentence at synth-03 lines 168 and 205 does NOT match research (B-3).

**synth-04 (14 groups traced, all hold except B-1 inside C-10 and C-14).**
1. Debate write-backs for C03, C05, C13, C14 against the four `return-contract.yaml` files: all scores, convergence values, agreed-point counts, unresolved-diff ids and HIGH-invariant counts match (see required-content table).
2. `panel.py:73` `_REFLECT_MAX_REVIEWERS = 3`; `panel.py:485-494`, `:536-543`.
3. `ledger.py:112`, `:150-157`, `:254-258`, `:273-274`; `merge_cmd.py:40-41` (`IntRange(min=1)`, help "1, 2 or 3") and `:101-104` (`--cap` only on round 1).
4. `card_convert.py:199-201` truncation without a counter; `contract.py:380-381` drift halts at any severity.
5. `cluster.py:64` imports `refs_norm`; `cluster.py:407-408` `elif not blocking: agreement = 1.0` (the no-blocking-cluster branch behind the 1.000 figure).
6. `findings.py:104,108,118` (200/200/300 limits); `findings_v2.py:107-108,161-162`.
7. `reflect-reviewer.md:6` `model: sonnet`; `document_review_loop_prompts.md:70` text matches the C-13 and C-10 descriptions.
8. `COMBO-REPORT.md:291-292,373` figures quoted in C-02, C-05, C-10; 24 + 14 + 10 + 1 = 49 and 24 + 14 + 10 = 48 (D1 row) add up.
9. `rf-qa.md:403-418` halts quoted in C-19.
10. Recount of tier decisions: 39 / 38 / 35 (numbers right; B-1 is about the wording).
11. Index-to-section consistency for all 20 conflicts (status, winner, invariant counts).
12. 6.D rows D1-D16 against the same code lines.
13. Installed-variant citations in C-05, C-13 and C-19: `review_ledger.py:41-59` (`PROFILES`, `_blocking_spec_panel`), `:63` (`VERDICT_EXIT` PASS 0, CONTINUE 10, ESCALATE 11, PENDING 12), `:65` (`ANSWER_ACTIONS`), `:851` (`check_anchors`), `:1300-1302` (cap check); `stoprule.py:8` (exit codes 0/3/4/5/6) and `:1185-1189` ("silence never passes"): match.
14. Section 6.X options and the Options Comparison read against the C01, C02, C04, C07-C12, C15-C16, C18-C20 resolutions: consistent (only the omission in N-1).

---

## Issues Found

Findings table in the format requested by the task prompt. B = blocking (IMPORTANT), N = minor note.

| # | Severity | Synth file | Section | Finding | Required fix |
|---|---|---|---|---|---|
| B-1 | IMPORTANT (blocking) | synth-01, synth-02, synth-04 | synth-01 Section 2.1 table row "Tier 2 is the typical path" (line 73); synth-02 DOC-59 (line 245); synth-04 C-10 Evidence bullet (line 691), C-14 E1 position row (line 897), C-14 Option B Pros (line 926) and Cons (line 927), C-14 Option C Cons (line 941), C-14 Evidence first bullet (line 944) | The older claim "Tier 2 was driven by the parsed-sparse flag" is still presented as measured fact, although the C14 debate recount (its own script over the 39 `tier_decision.yaml` files, synth-04 line 956; I re-ran the counts: 39 files, 38 Tier 2, 35 flagged) found the flag SET in 35 of 39 non-shadow runs (34 of the 38 Tier 2 runs) and DECISIVE in 0 for certain, at most 1. Specific wording: synth-01 line 73 "35 of them through the parsed-sparse pre-filter" with strength "measured census" (also wrong denominator: 34 of the 38 Tier 2 runs, 35 of the 39 runs); DOC-59 says the recount gives "the same conclusion"; C-10 line 691 "Parsed-sparse escalation sends nearly every workflow plan to Tier 2"; C-14 line 926 "the measured driver of Tier 2 spend (35 of 39 parsed-sparse)"; line 927 "those 35 plans"; line 941 "for an input-format reason, not plan risk"; line 944 "mostly for an input-format reason ... 35 by the parsed-sparse pre-filter ... with the same conclusion" labelled `[CODE-VERIFIED in data]`. Section C-14 therefore contradicts its own Adversarial result (line 956). | Replace with the recount wording used in synth-06 V-316 / V-366: "38 of 39 non-shadow pre runs selected Tier 2; the parsed-sparse flag was set in 35 of 39 (34 of the 38 Tier 2 runs) and was decisive in 0 for certain and at most 1; the 'driven by the flag' claim is not supported". Concretely: synth-01 line 73 row value and strength; synth-02 DOC-59 "Superseded by the 2026-11-13 recount: 38 of 39 selected Tier 2, flag set in 35 (34 of 38), decisive in at most 1; the older conclusion is NOT carried"; synth-04 line 691 say "the flag is set in most workflow plans and most plans reach Tier 2"; line 897 change "34 by the parsed-sparse pre-filter" to "flag set in 34", keep MR:142 marked doc-sourced and superseded; line 926 "Acts on the largest flagged group (35 of 39 flagged); the flag was decisive in at most 1, so the saving is unmeasured"; line 927 "How many of the flagged plans would then be wrongly stopped at Tier 1 is not measured"; line 941 "Pays Tier 2 on 38 of 39 plans; the flag is set in 35 of them but was decisive in at most 1"; line 944 rewrite to the same recount and drop "mostly for an input-format reason" and "same conclusion". |
| B-2 | IMPORTANT (blocking) | synth-02 | Section 4 Gap Analysis table, blank lines at lines 125, 149, 173, 185, 221 | Table shape: the single Gap table is split into six pieces. Only the first piece (D1-D16) has the header and separator row; the pieces starting at `BL-01`, `MS-01`, `ENS-1`, `DOC-01`, `DOC-36` have neither, so 128 of 144 gap rows render as plain pipe text, not table rows. The assembler copies this file into the report, so the defect propagates. | Delete the five blank lines so the 144 rows are one contiguous table under the one header, or put a header and separator row at the top of each group. Keep the group labels in the "Row groups" paragraph or as bold text above the table, not between rows. |
| B-3 | IMPORTANT (blocking) | synth-03 | Section 5.3 opening paragraph (line 168) and 5.3.3 row "Verbalised confidence is overconfident" (line 205) | False claim copied from `research/web-03-judge-calibration.md:11`: "shadow runs recorded 0 numeric per-finding calibrations of 689 findings" and "zero numeric calibrations in shadow runs". `research/05` section 5 ("legacy 0/689; shadow 142/142"), synth-01 lines 69-70 and synth-04 C-06 all say the opposite: the 0 of 689 belongs to the legacy recorded cards; shadow runs hold 142 of 142. The sentence is used as evidence ("a small loss of evidence"), so the report would contradict itself between Sections 2 and 5. | Line 168: replace "shadow runs recorded 0 numeric per-finding calibrations of 689 findings" with "legacy recorded cards held 0 numeric per-finding calibrations of 689 findings, and shadow runs 142 of 142 (research/05 section 5)". Line 205: replace "zero numeric calibrations in shadow runs is a small loss of evidence" with "the 0 of 689 legacy per-finding numbers is a small loss of evidence; the 142 of 142 shadow numbers carry no ground truth". Also note in the row that the source file `web-03:11` has the same slip. |
| N-1 | MINOR | synth-04 | "Assessment summary" under 6.X (line 1439) | The sentence lists decided conflicts as "C01, C02, C04, C07-C12, C15, C16, C18-C20" and omits C06 and C17, both DECIDED-BY-EVIDENCE in the index. | Add C06 and C17 to the list (or write "all other conflicts"). |
| N-2 | MINOR | synth-01 (and synth-02 DOC-43) | Section 2.4 "Test surface" | States "`tests/cli/reflect` has 37 files"; `ls tests/cli/reflect/test_*.py` gives 38 (the QA note in DOC-43 already records 38 and leaves the difference open). | Say "37 or 38 test files (353 collected tests)" or state the verified 38. |
| N-3 | MINOR | synth-01, synth-02 | citation shorthand | `CR`, `AD`, `HO`, `PR` are defined only in synth-04's header (line 5) and `MR` only inside C-11; synth-02 uses `CR:373`, `AD/summary.md`, `HO:105`, `MR:142` without definition, and synth-01's citation key does not define them. In the assembled report Sections 2 and 4 come before Section 6. | Add the five abbreviations to the synth-01 citation key. |
| N-4 | MINOR | synth-02 | "Row groups" paragraph (line 105) and Section 4.2 | Group order stated as (v) DOC then (vi) OPEN, but OPEN-01/02 rows come before the DOC rows; row ids written `ENS-1`..`ENS-9` in the table and `ENS-01`..`ENS-09` in 4.2. | Align the group letters and the id format. |
| N-5 | MINOR | synth-01 | Section 1 "Why it matters" last bullet (line 33) | "94 open rows, none Critical, 30 Important" is on the gaps-log scale; synth-02 Section 4 lists 15 Critical rows under the C8 rule. The reconciliation exists only in synth-02 Section 4.1 row 15, so a reader of Section 1 sees a conflict. | Add "on the log's scale; Section 4 re-rates 15 as Critical under control C8". |
| N-6 | MINOR | synth-01, synth-02, synth-03 | file preambles | Each file opens with an H1 title and metadata block (`# Synthesis 01: ...`, task, scope, citation key, conventions) before the report section; copied verbatim they add stray H1 headings and duplicate scope text to the report. | Assembler strips the H1 and the metadata lines but keeps the citation key and conventions tables where the report needs them. |
| N-7 | MINOR | synth-02 | Section 4 intro and the C8 rows | The template's Gap Analysis rule says a C8 row MUST carry or link an MDTM remediation task; the file instead states "none created in this run (owner scope: report only)". The reason is stated and cited to the 2026-11-13 owner scope change, so it is an on-record scope decision, not a silent downgrade. | None needed; the assembler should keep that sentence in the report. |

---

## Cross-file note for the merge of partition reports

[PARTITION NOTE: Cross-file checks limited to assigned subset.] Executor note (4): synth-05 raises a `[CONTRADICTION]` about the core verdict vocabulary (PENDING, exit 12). In my partition the same topic appears in synth-04 C-19 (Option A: "PASS/REVISE/ESCALATE as today, with an optional PENDING"; the experiment ledger "CONTINUE and PENDING with exit 0/10/11/12", line 1228) and synth-02 BL-13. Neither file contradicts the other and neither claims a settled vocabulary, so I found no silent inconsistency on my side. I did not verify synth-05's flag; that belongs to partition 2.

---

## Summary

- Checks passed: 6 of 8 (checks 1, 4, 5, 6, R-a, R-c)
- Checks failed: 2 (check 2 table structure, check 3 no fabrication)
- Blocking findings: 3 (CRITICAL 0, IMPORTANT 3: B-1, B-2, B-3)
- Minor notes: 7 (N-1 to N-7), never fail the gate
- Issues fixed in place: 0 (fix authorization is false)

## Actions Taken

None on the synthesis files (report only). Only this report file was written.

## Recommendations

1. Fix B-1 in all three files in one pass (synth-01 line 73, synth-02 line 245, synth-04 lines 691, 897, 926, 927, 941, 944), using the recount wording that synth-06 V-316 and V-366 and synth-05 already use. After the fix, grep the four files for `parsed-sparse`, `input-format`, `same conclusion` and `35 plans` to confirm no sentence presents the flag as the driver.
2. Fix B-2 by removing the five blank lines in synth-02 (lines 125, 149, 173, 185, 221). Re-run the check: no pipe row may follow a blank line that follows a pipe row.
3. Fix B-3 at synth-03 lines 168 and 205.
4. The minor notes can be applied in the same pass or left; they are not rechecked.
5. The four debates ending `partial` with open HIGH invariants are stated as open in synth-04 (Status and Adversarial result lines); they are not defects and need no change.

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 21 (plus 1 rejected for size) | Grep: 7 | Glob: 0 | Bash: about 30 (read-only inspections; the batched scripts ran from private `/tmp/ironclaude-batch.*` directories and were removed on exit; one script failed on an unbound variable and was rerun, one `sed` batch was rerun after a quoting slip). Tavily and web tools: not used, because every claim checked was internal (research files, code, git objects); `tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0`.
- Read plus Grep plus Glob calls (28) exceed the 8 checklist items.
- Unchecked items: none. Unverifiable items: none. Items not independently re-traced (listed for honesty, none is a checklist item): the K-row and SC-row details of synth-02 beyond the code lines named above, and the external URLs inside synth-03, which were compared with the research files only (the research files are the source of record for web content; no live web fetch was made).

## QA Complete
