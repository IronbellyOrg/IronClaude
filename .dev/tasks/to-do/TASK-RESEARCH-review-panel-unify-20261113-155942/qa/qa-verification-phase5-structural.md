# QA Report: Phase 5 Synthesis Gate, Fix Verification (structural)

**Topic:** unified Review Panel investigation (TASK-RESEARCH-review-panel-unify-20261113-155942)
**Date:** 2026-11-14
**Phase:** synthesis-gate (verification)
**Fix cycle:** 1
**Fix authorization:** false (report only)

Report is written incrementally; sections follow below.

Required contents (from the task file Execution Context, line 111): (a) overlap matrix = synth-01 2.6; (b) value inventory = synth-06 8.1; (c) conflict log = synth-04 Section 6; (d) target architecture = synth-05 7.1; (e) future-use-case check = synth-05 7.2.

## Section A: scripted executor checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| S1 | synth-02 Section 4 is one contiguous table | PASS | Python scan of lines between `## 4. Gap Analysis` and `### 4.1`: exactly 1 pipe-row block (starts at line 107, 146 lines = header + separator + 144 rows); no blank line inside it. |
| S2 | every table row in synth-06 8.1 has the header's column count | PASS | Same scan of `### 8.1` to `### 8.2`: 2 pipe blocks (a 2-column block of 11 lines and the 7-column inventory of 693 lines = 691 rows); 700 data rows, 0 with a different cell count (unescaped-pipe counting, `\|` excluded). Whole file synth-06: 11 tables, 0 bad rows. V-231 and V-497 now parse as 7 cells. |
| S3 | synth-06 G9 command collects the count it states | PASS | Ran the G9 command's pytest selection (`tests/cli/reflect` + the four `--ignore` flags) with `uv run pytest --collect-only -qq -p no:cacheprovider`: `271 tests collected`; those tests sit in 34 files. Same call without `--ignore`: 353; the four G8 files alone: 82; `ls tests/cli/reflect/test_*.py` = 38. G9 text (271, 34 of 38, 353 = 271 + 82) matches. |
| S4 | synth-07 9.1 lists G-01 to G-94 exactly once; every new Section 9 row indexed | PASS | Scan of lines 64-127: 94 distinct G ids, 0 missing, 0 duplicates, 0 outside 1-94. Q-01 to Q-57 each appear once as a first-column row of Section 9 and once in the 9.1 index (57 and 57; no id missing in either). Rows Q-45 to Q-57 are marked "none" for gap ids as the 9.1 intro says. |
| S5 | grep for `parsed-sparse`, `input-format`, `same conclusion`, `driver of Tier`, `37 of 38` finds no sentence presenting the older claim as measured fact | PASS (see detail) | Every hit in synth-01 to 07 read in context (lines synth-01:73; synth-02:217,240,273; synth-04:28,691,897,917,941,944,954,956; synth-05:18,31,51,286,292,294; synth-06:11,346,363,396,399,429,435,548,587,703,767; synth-07:54). Each is the recount wording, a quote marked superseded or "not carried", or a source's own claim whose Reason cell carries the correction. `same conclusion` and `driver of Tier` have 0 hits. `input-format` has 1 hit (synth-06 V-333, "input-format compliance is a brief problem": a different meaning, not the C14 claim). synth-06 V-399 keeps "34 of 38 pre runs parsed-sparse" as the source's item with the recount in the Reason cell. |
| S6 | no debate winner changed in synth-04 or synth-05 | PASS | Compared the four `return-contract.yaml` files with synth-04 index rows C03/C05/C13/C14 (lines 33, 35, 43-44) and the synth-05 open-risk table: C03 `base_variant A`, status partial, 2 HIGH (INV-013, INV-009), 4 unresolved, convergence 0.86; C05 `base_variant B (Option D)`, partial, 11 HIGH, 3 unresolved, 0.909; C13 `base_variant B`, partial, 10 HIGH INV-001..010, 4 unresolved, 0.89; C14 `base_variant variant-2 (B)`, partial, 3 HIGH (INV-009, -012, -013), 6 unresolved, 0.80. All match; scores and margins quoted match the contracts. |
| S7 | E2 cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | PASS | Grep of every hex token in synth-01..07: E2 appears as the full SHA 16 times and as the prefix `4a22d742` 4 times (same commit, synth-01:84 heading and 3 others). Other SHAs are `9874d63fb`, `c2e3347d3`, `792cf8c52`, `d2d8a2d16` (E1 branch), `9163bd1c7`, `5d9a0ae70`, `77e0a7029` (E3 PRs, read in context), `e8db2fe6` (base-run id) and URL hashes. No second E2 commit. |
| S8 | table integrity elsewhere (extra scan; the S7 sha scan also confirmed `4a22d742` is a prefix of the full SHA) | NOTE | 27+11+29+90+13+11+12 tables scanned. Non-separator blocks are ASCII diagrams in code fences (synth-01:125-237, synth-04:1380-1384, synth-05:89-99; synth-05 diagram edited by P5-B22 is intact). Two real broken rows remain: synth-01:260 (11 cells under a 4-column header) and synth-04:769 (8 cells under 3), both unescaped pipes inside code spans. The fix log records them as pre-existing and not among the 25 findings; see Minor notes. |

## Section B: the 25 blocking findings (check (a))

Each row was checked by opening the named synth file at the named place and, where the fix cites a source, the source (debate return contracts, `proposal-merged.md`, `invariant-probe.md`, research files, `SKILL.md`, `ledger.py`, the test file, pytest).

| Finding ID | Fixed? (yes/no) | Evidence |
|---|---|---|
| P5-B1 | yes | synth-04 C-14: E1 evidence row (:897) now says 38 of 39 selected Tier 2, flag set in 35 of 39 (34 of 38 Tier 2 runs), decisive in 0 for certain and at most 1, "cost driver is not established"; Option B description (:917) calls the rubric edit "a hypothesis"; pros/cons (:940-941) and first Evidence bullet (:944) carry the recount; Status "Original reason" is marked as pre-recount; Recommended resolution (:954) = Step A audit keys, pre-filter unchanged unless CI-1, Step B D-1 owner-gated, Step C H-A, and states "fix the rubric first" is not carried. Cross-checked against `panel-size-cost/proposal-merged.md` (CI-1 at :350, the 0.68 E-6 run at :73,:137,:145) and `return-contract.yaml:27`. synth-05 7.4.3 (:292) replaced "Overridden: none" with the list of corrected sentences. No `same conclusion`, `driver of Tier`, `measured driver` left. Winner B unchanged. |
| P5-B2 | yes | synth-04:691 now reads "Tier 2 was selected in 38 of 39 recorded non-shadow pre runs ... the flag was set in 35 of 39 and was not shown to be the cause (decisive in 0 for certain and at most 1); R06 marks its own count UNVERIFIED". |
| P5-B3 | yes | synth-01:73 row "Tier 2 is the typical path": 38 of 39; flag set in 35 of 39 (34 of 38); decisive 0 / at most 1; "counts only, cause not established"; Strength cell "measured census of counts; cause not established". |
| P5-B4 | yes | synth-02:240 DOC-59 rewritten ("Counts superseded ... older 'driven by the flag' conclusion is not carried"); 4.1 row 16 added (:273) naming `return-contract.yaml` and `recount_tier_decision.py` (present in the debate folder) with "stronger finding: the recount" and the model-written-fields caveat. |
| P5-B5 | yes | synth-03:168 "legacy recorded cards held 0 ... of 689 findings, while shadow runs hold 142 of 142 (research/05 section 5; web-03 line 11 states the shadow figure as 0 of 689, a slip not carried here)"; :205 restated; :215 Platt row restated ("a fit is not currently possible"). Source: `research/05-blocking-calibration.md:155,180,193-194` (legacy 0/689, shadow 142/142); `research/web-03-judge-calibration.md:11` does carry the slip. |
| P5-B6 | yes | Script S1: synth-02 Section 4 is one pipe block of 146 lines (header, separator, 144 rows); matches the 144 stated in 4.2. |
| P5-B7 | yes | synth-01:33 now carries the scale sentence ("gap-log rating; synth-02 Section 4 re-rates 15 rows Critical because control C8 ... see 4.1 row 15"). synth-02 4.1 row 15 exists and 4.2 says Critical 15. |
| P5-B8 | yes | synth-04 C-05 Option E Cons and Evidence now say the equality "shows nothing either way" because `cluster_agreement` is mostly the no-blocking-cluster default (11 of 14, two null, shadow09 0.9328); the "10 of 11" figure is dropped with a note on the two populations. Agrees with synth-02 DOC-19 (:200) and `research/03-clustering.md:125-126`. Winner D unchanged. |
| P5-B9 | yes | synth-04 C-04 Status is now a split decision (silent re-admission and per-slot distinctness decided by code evidence; declared replicas a design option resting on one of 28 uncorrected p-values); Recommended resolution and an Evidence multiplicity caveat added; synth-02 D11 row carries the same caveat ("a hypothesis for replication, not a basis for the design"); synth-05 C-04 row and 7.1.3 Panel resolution row, synth-06 M1-09 and V-497 are consistent. (Index-row label left as DECIDED-BY-EVIDENCE: minor note m3.) |
| P5-B10 | yes (synth-04); see new defect N-1 for the twin sentence in synth-05 | synth-04 6.X (:1375 and the Assessment summary) lists C03 (launch adapters, O-2), C05, C13, C14 (D-1) as the dependencies, lists C06 and C17 as decided, and states A and B are two stages of one path with C the only alternative. |
| P5-B11 | yes | Numbering compared with `ledger-model/adversarial/invariant-probe.md:9-18` and the contract: INV-001 `defer`, INV-002 atomic vs bounded, INV-003 `prior` open, INV-004 valid reviewer undefined, INV-005 would-be PASS uncleared row, INV-006 second `ledger revise`, INV-007 quorum denominator, INV-008 spanless row, INV-009 `evidence` on `prior`, INV-010 sufficiency. synth-06 M1-07 (:740) uses exactly this; V-118 and V-432 say INV-006; V-431 says INV-008; synth-05 risk row and synth-04 C-13 result match. |
| P5-B12 | yes | Script S3 (pytest collect-only with the G9 command): 271 tests in 34 files; 353 in the directory; 82 for G8; 38 test files. synth-06 G9 (:938) "remaining 34 of the 38 test files", four `--ignore` flags, 353 = 271 + 82; V-558 "353 in 38"; V-612 closed ("38 files ... G9 covers 34"); V-054 "59 runs with extra modelUsage keys, 57 of them an auxiliary call" = `research/08:307`. |
| P5-B13 | yes | synth-06 V-405 Reason: the source's "37/38" is superseded by the recount; "the rubric-first lever (O-8) is not supported by that count"; keeps the ceiling point only. |
| P5-B14 | yes | Script S2: V-231 (`seed\|slot\|i` escaped) and V-497 now parse as 7 cells; whole synth-06 has 0 rows with a cell count different from the header. |
| P5-B15 | yes | synth-07 9.5 (:242-258) holds Q-47 to Q-57: D-1, task-builder POST gate a/b, tripwire numbers, H-A owner and count-rule parameters, C05 16 owner decisions, C13 OD-1 to OD-11 (OD-6, OD-8, `refusals[]`), C03 flip shape and the undebated INV-009 split, core verdict vocabulary `[CONTRADICTION]`, brainstorm `tasklist` hand-off, EV-1 presence-only gap, the HIGH-invariant tally (2, 11, 10, 3) matching the four contracts. Spot-checked numbers against the proposals (26 of 38 and 14 manifests against 91 directories in `panel-size-cost/proposal-merged.md:55,236`; C05 16-row owner table at `who-judges-blocking/proposal-merged.md:729-750`). Each row has Impact and Suggested Resolution; 9.1 indexes them (script S4); Inputs line names `reviews/adversarial/`; synth-05 7.4.3, synth-06 8.5 last row and 8.6 last checkbox point to 9.5. |
| P5-B16 | yes | Q-13, Q-16, Q-17, Q-19, Q-20, Q-22, Q-23 relabelled "decided in synth-04 C-NN ... owner confirmation only" with the residual open part stated; Q-30 "partly decided by M2-01" with the hash versus `origin/master` mechanism open. |
| P5-B17 | yes | synth-07 Section 10: "planned" wording gone; Synthesis Files table complete; "Adversarial Debate Outputs" is a table of the four folders with status, merged-proposal path and return-contract path plus the `conflict-index.md` pointer; QA Reports table lists the Phase 5 reports; header date 2026-11-14. |
| P5-B18 | yes | synth-07 9.4 D-59 row (:229) and Q-38 impact cell (:54) carry the recount with the 29-of-34 escalate-row figure and "the 'driven by the flag' claim is not carried". |
| P5-B19 | yes | synth-05 Rationale 6 (:~30) and the C-14 row (:51) now follow the merged design; synth-06 M2-07 (:767) names the Step A keys (`matching_rows`, `calibrated_C_t1`, `S_domains_basis`, `tier_without_flag`, `sparse_flag_decisive`, `escalation_path`; telemetry `reviewers_requested/resolved/source`), the `SKILL.md` §5.4 edit site (verified: `### 5.4 tier_decision.yaml audit artifact` at SKILL.md:447; §5.4 is in the C6 allowed list), the recompute check and the three pinned H-A arms; V-366, V-518 (R06's wording marked), V-557 reworded. The CI-1 "at least three runs" trigger matches `proposal-merged.md:350`. |
| P5-B20 | yes | synth-06 M1-06 (:739) adds `ledger.py:191,199,207-238` (verified: `first["category"]`, `first["claim"]` at :191,:199) and "taken from the highest-confidence member and recomputed on re-find"; G1 (:930) and G2 (:931) gain `test_review_findings.py:235-317` and `test_review_ledger.py:139-150` with replacement assertions marked "proposed wording, not read from the test bodies". Both ranges match synth-04 6.D row D6 (:1361). |
| P5-B21 | yes | Headings of `src/superclaude/skills/sc-reflect-protocol/SKILL.md`: `### 4.3a` at :309 (so :344,:346 are inside), `## 8.` at :677 (:714 inside, outside the allowed list), `## 17.6` at :1920 (:1955,:1958 inside, outside). `tests/cli/reflect/test_shadow_skill_contract.py:65` allows only 3.1, 4.3a, 5.4, 9.2. synth-06 M2-02 (:762), M2-09 (:769), G8 (:937) and synth-05 7.4.1 (:258) now say the `:714`, `:1955`, `:1958` edits change the C6 allowed list in the same change. |
| P5-B22 | yes | synth-05 7.1.3 "Merge and verdict" (:160) and "Built-in run audits" (:161) are split into a **core part** (machine verdict and generic writer interface; check-plugin interface with manifest-derived checks) and a named **reflect module part** (1.8.0 contract writer, EV-1, `panel_lint`, verdict replay, shadow-exit checks); the 7.1.1 diagram ends with "reflect module side (not core): 1.8.0 contract writer, EV-1, panel_lint, verdict replay" and its box rows say "writer iface". M2-02 keeps the writer module-side. |
| P5-B23 | **no** | synth-05 7.1.3 (:160), synth-06 M2-02 (:762), synth-07 Q-56 and synth-04 C-11 Option A "How it works" now say EV-1 remains an on-disk presence check and list what the writer verifies. But synth-04:720, the Pros cell of the same C-11 Option A, still reads "fixes three unparseable shadow contracts and the self-attested EV-1". That is the unsupported claim the finding targeted, and it contradicts the option's own text four lines above it, synth-06 V-271 ("EV-1 is still self-attested") and Q-56. See N-2. |
| P5-B24 | yes | synth-06 V-415, V-416, V-420, V-426 changed from DROP to "Round model (ledger), deferred to O-1" with the not-read reasons (`research/scope/05:184` lists `diffgate.py` and the fix-audit scripts as not read); the unread scripts and bundle design docs are added to synth-07 Q-01 and the G-25 item of Q-34. |
| P5-B25 | yes | synth-06 M1-08 (:741): grader "built as a shadow-only component", promotion conditional on O-1 (M1-18), "Closes gaps" now D4, MS-03, G-01, G-02 (MS-19 and G-91 named as staying with M1-18 and O-1); M1-18 (:751) still holds MS-19, G-91; V-155, V-421, synth-05 decider-hook row (:158) and synth-07 Q-01 say the same. |

Result: 24 of 25 fixed; 1 not fully fixed (P5-B23).

## Section C: new blocking defects introduced or left by the fixes (check (b))

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N-1 | IMPORTANT | synth-05 Rationale 2 (line 27) against synth-04 6.X Assessment summary (line 1439) | The P5-B10 fix made synth-04 correct: Option B depends on C03 (launch adapters, O-2), C05, C13 and C14 (template and count defaults, D-1). synth-05 Rationale 2 still says "No part of B depends on the four open conflicts except which decider (C-05) and which round model (C-13) the registry carries". synth-05 therefore now contradicts the corrected synth-04 and its own open-risk table (C-03 row: the launch adapters and class-launch core; C-14 row: D-1 and the template defaults), while 7.4.3 says it follows synth-04. This is the same false dependency claim P5-B10 removed from synth-04; it is a cross-file inconsistency between synth-04 and synth-05 (check (b)). The gate had recorded the synth-05 side as minor note M-23 only because synth-04 and synth-05 agreed; the fix split them. | In synth-05 Rationale 2 replace the sentence with: B's launch adapters and class-launch grammar depend on C-03 (O-2), the decider on C-05, the round model on C-13 and the template and reviewer-count defaults on C-14 (D-1); the architecture leaves all four as declared hooks or owner-gated items. |
| N-2 (P5-B23 still open) | IMPORTANT | synth-04 C-11 Option A, Pros cell (line 720) | Says Option A "fixes three unparseable shadow contracts and the self-attested EV-1". The writer only reads `merge_method` and checks artifact presence; EV-1 stays a presence check (the same option's "How it works" two lines above, synth-05 7.1.3, synth-06 M2-02, V-271 and Q-56 all say so). The finding's required fix was to remove the "EV-1 stops being self-attested" claim; it was removed from synth-05 and the Recommended resolution but survives in this Pros cell. A reader of the options table sees a claim the report's own Section 9.5 Q-56 says is not established. | Reword the Pros cell to "fixes three unparseable shadow contracts and narrows the self-attestation of EV-1 (it remains an on-disk presence check, Q-56)". |

Open blocking findings after cycle 1: N-1 and N-2 (= P5-B23). |F_2| = 2 against |F_1| = 25, so the count shrinks strictly. No finding that passed at a prior cycle has regressed (this is the first verification cycle).

## Section D: check (c), required contents (a) to (e) still present

| Required content | Location | Result | Evidence |
|---|---|---|---|
| (a) overlap matrix | synth-01 2.6 | PRESENT | Heading and 18 numbered component rows (`grep -cE '^\| [0-9]+\. '` = 18, as the section text says). |
| (b) value inventory | synth-06 8.1 | PRESENT | 691 `V-` rows, 7-column table, 0 malformed rows (script S2). Rows V-415, V-416, V-420, V-426 changed from DROP to a destination, which adds content. |
| (c) conflict log | synth-04 Section 6 | PRESENT | 20 conflict blocks `### C-01` to `### C-20`, 65 option blocks, the 6.0 index with all 20 rows, 6.D defects, 6.X overall options and Options Comparison; C-03, C-05, C-13, C-14 adversarial results intact and matching the four return contracts (S6). |
| (d) target architecture | synth-05 7.1 | PRESENT | 7.1.1 diagram (box intact after P5-B22), 7.1.2 data flow, 7.1.3 component table (Merge and verdict, Built-in run audits now split core and module), 7.1.4 per-use-case rows. |
| (e) future-use-case check | synth-05 7.2 | PRESENT | Exposure table with 23 rows, unchanged by the fixes. |
| Section 9 / Section 10 | synth-07 | PRESENT | 9.1 to 9.5, Evidence Trail with debate and QA tables. |

No removed required content found. No broken table introduced by the fixes (S1, S2); no new uncited claim found in the new 9.5 rows, M2-07, G9 or the C-04 split (each was traced to `proposal-merged.md`, a return contract, `invariant-probe.md`, `SKILL.md`, the test file, or the pytest run). The cross-file check between synth-04, synth-05 and synth-06 found the two inconsistencies N-1 and N-2 above; synth-06 agrees with synth-04 and synth-05 on C-04, C-11, C-13, C-14 numbering and the C6 section list.

## Minor notes (do not fail the gate, are not rechecked)

| # | Location | Note |
|---|---|---|
| m1 | synth-01:260 and synth-04:769 | Two table rows with unescaped pipes inside code spans (11 cells under 4 columns; 8 under 3). The fix log reported them as outside the 25 findings; they were not introduced by the fixes. Escape as `\|`. |
| m2 | synth-02:263 (4.1 row 6), synth-01:290, synth-06:687 (V-657) | Still say "37 or 38" files and "stays unresolved" while synth-06 G9, V-558 and V-612 now state 38 (M-04 of the consolidated file). |
| m3 | synth-04 6.0 index row C04 | Status column still reads DECIDED-BY-EVIDENCE although the C-04 block is now a split decision. |
| m4 | synth-04 6.0 index row C14, E1 cell (line 28) | Quotes the source's "37 of 38 ... (MR:142; recount 38 of 39)": attributed and corrected in place, so not a measured-fact presentation. |
| m5 | synth-06 V-399 (line 429) | Keeps "34 of 38 pre runs parsed-sparse" as the source's item; the Reason cell carries the recount. Acceptable. |
| m6 | synth-06 M1-06 cites `cluster_v2` `:302-378` | Consolidated note M-01 (range is `_components`/`_cluster`; `cluster_v2` starts at `:381`); unchanged by the fixes. |
| m7 | synth-01:80, synth-02:159, synth-07 Q-31, synth-06 V-271 | These describe EV-1 as "self-attested" (the gap, not a fix) and are consistent with Q-56; only the synth-04:720 Pros cell is wrong (N-2). |

## Summary

- Findings fixed: 24 / 25 (every finding except P5-B23, which is only partly fixed).
- Scripted executor checks S1 to S7: 7 / 7 PASS (S8 note only).
- New or residual blocking defects: 2 (N-1 IMPORTANT, N-2 IMPORTANT = P5-B23 residual). Critical: 0.
- Minor notes: 7.
- Required contents (a) to (e): all present.
- Issues fixed in place: 0 (fix authorization false).
- Confidence: Verified: 35/35 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist = 7 scripted checks + 25 findings + checks (b) and (c) + S8; the 100% is coverage of the checklist, not a claim that the synthesis is correct).
- Tool engagement (approximate): Read: 5 | Grep: 14 | Glob: 0 | Bash: 38. No web research; no Tavily or web fallback used.

## Overall Verdict: FAIL

Two blocking findings remain open: N-1 (synth-05 Rationale 2 contradicts the corrected synth-04 dependency sentence) and N-2 (synth-04:720 still says the writer fixes the self-attested EV-1, so P5-B23 is not fixed). Both are one-sentence edits. 24 of the 25 original findings are fixed and verified. Next step: fix cycle 2 limited to N-1 and N-2, then one more verification (the last allowed review).

## QA Complete
