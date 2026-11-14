# QA Report: Phase 5 Synthesis Gate, Fix Verification (structural, cycle 2)

**Topic:** unified Review Panel investigation (TASK-RESEARCH-review-panel-unify-20261113-155942)
**Date:** 2026-11-14
**Phase:** synthesis-gate (verification)
**Fix cycle:** 2
**Fix authorization:** false (report only)

Written incrementally; sections follow below.

Method: read the cycle-2 section of `qa/qa-consolidated-findings-phase5.md` (4 findings) and of `qa/qa-fix-log-phase5.md`, the two cycle-1 verifier reports, then opened every place those reports named in the synth files. `git diff -U0` of `synthesis/` against the index (which holds the cycle-1 state) was used to bound the cycle-2 edits: 5 files, 23 changed lines (synth-01 :260; synth-02 :38, :68, :153; synth-04 :18, :720, :769, :1366; synth-05 :27, :29, :101, :149, :232; synth-06 :63, :105, :154, :173, :228, :237, :301, :520, :529, :742). That list equals the fix log's file list.

## Section A: scripted executor checks (re-run this cycle)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| S1 | Column-count scan over all seven synth files, outside code fences, unescaped pipes only, per-table header count | PASS (0 bad rows) | Own script (not the fix agent's): synth-01 157 pipe rows, synth-02 241, synth-03 255, synth-04 669, synth-05 160, synth-06 923, synth-07 275; bad rows 0 in each, TOTAL BAD 0. Scanner sanity: a sample row with unescaped pipes inside a code span counts 5 cells, the same row escaped counts 3. |
| S2 | synth-02 Section 4 is one contiguous table | PASS | Between `## 4. Gap Analysis` and `### 4.1`: 1 pipe block, starts at line 107, 146 rows (header, separator, 144 rows), no blank line inside; header `Gap / Current State / Target State / Severity / Notes`. |
| S3 | synth-06 G9 command collects 271 | PASS | Took the command text from synth-06 :938 and ran it with `uv run pytest --collect-only -qq -p no:cacheprovider`: `271 tests collected`. The command has the four `--ignore` flags for the G8 files. |
| S4 | synth-07 9.1 lists G-01 to G-94 once and Q-01 to Q-57 once | PASS | Lines 64-127: 94 distinct G ids, 0 duplicate, 0 missing, none outside 1-94. First-column Q rows in 9.1: 57 rows, 57 distinct. Q-01 to Q-57 each also appear once as a first-column row of Section 9. (A looser regex flags Q-01, Q-45, Q-57 more than once only because the 9.1 intro sentence says "Q-01 to Q-57" and "Q-45 to Q-57".) |
| S5 | No debate winner changed against the four `reviews/adversarial/*/adversarial/return-contract.yaml` | PASS | C03 `base_variant: "A"`, partial, convergence 0.86, 2 HIGH; C05 `base_variant: "B (Option D ...)"`, partial, 0.909, 11 HIGH; C13 `base_variant: "B ..."`, partial, 0.89, 10 HIGH; C14 `base_variant: "variant-2 (Proposal B, Option B ...)"`, partial, 0.80, 3 HIGH. synth-04 index rows C03, C05, C13, C14 and the Adversarial result blocks (:226, :382, :891) read winner A, B (Option D), B (narrowly), B as merged. The cycle-2 diff touches none of those rows or blocks; the C-14 block (:897-:956) is not in the diff. |
| S6 | E2 cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | PASS | Every 40-hex token in synth-01..07: one distinct value, `4a22d74213f93837d00c2c314075dd967b9a98e3` (16 hits). Short form `4a22d742` 4 hits (prefix of the same commit). No other 40-hex SHA and no second E2 commit. |
| S7 | Required contents (a) to (e) present | PASS | (a) synth-01 `### 2.6 ... component overlap matrix (a)` at :345, 18 numbered rows. (b) synth-06 8.1: 691 `V-` rows, 0 duplicate ids. (c) synth-04 `## 6` with 6.0 index, 20 `### C-NN` blocks, 65 `#### Option` blocks, 6.D, 6.X. (d) synth-05 `### 7.1` at :79 with 7.1.1 to 7.1.4; the 7.1.1 box (lines 98-109) has the same per-line widths as in the index (91 91 91 91 91 91 90 91 91 89 91 91), so the cycle-2 edit at :101 did not break it. (e) synth-05 `### 7.2` at :177, 23 rows. |

## Section B: the four cycle-2 findings (check (a))

| Finding ID | Fixed? (yes/no) | Evidence |
|---|---|---|
| P5-B9-r | yes | synth-04 index row C04 (:18) resolution cell now reads "Declared per-slot distinctness and no silent re-admission (decided); intended replicas an optional design option resting on one uncorrected E2 p-value" (the required wording). synth-06 V-033 (:63) Reason: "it is the only support for the optional `replicas` field, one of 28 uncorrected p-values (C-04: replicas are a design option; the per-slot distinctness policy is decided by code evidence alone)". V-075 (:105) "(replicas: design option)"; V-143 (:173) "(replicas: design option)"; V-198 (:228) "`replicas`: design option". The fix agent also caveated further hits; I read each changed line: synth-04 D11 row (:1366) "Decided (C04)" now covers policy only and says replicas are an optional design option; synth-05 :29, :41, :101, :149, :232; synth-02 :38, :68, :119, :153; synth-06 V-124, V-207, V-490, V-499, M1-09 (:742); synth-07 Q-16 (:32). All agree with the C-04 Status split at synth-04 :286-:288 (decided: no silent re-admission, per-slot distinctness; design option: replicas, one of 28 uncorrected p-values). A grep for `replica` across the seven files (all hits read) finds no sentence that presents replicas as part of a decided outcome. synth-01 :34, :100, :104, :115 use "replicated" for repeated E2 panels, a different meaning. |
| P5-B10-r | yes | synth-05 Rationale 2 (:27) now reads: B's "launch adapters and class-launch grammar depend on C-03 (owner item O-2, the target environment), the decider on C-05, the round model on C-13, and the template and reviewer-count defaults on C-14 (Decision D-1). The architecture below leaves all four as declared hooks or owner-gated items". That equals synth-04 6.X (:1439: launch adapters and class-launch grammar on C03 / O-2, decider on C05, ledger rounds model on C13, template and reviewer-count defaults on C14 / D-1) and synth-05 Rationale 6 and the open-risk table. Rationale 4 (:29) heading is "Decided conflicts are built as written; the four debate-resolved ones are staged behind hooks, gates or owner items"; its count "sixteen of the twenty" equals C-01, C-02, C-04 (3) + C-06 to C-12 (7) + C-15 to C-20 (6) = 16. Grep for "No part of B", "only decided", "depend only", "does not depend" over all seven files: 0 hits. |
| P5-B14-r | yes | synth-01 :260 row "Fingerprint" now has `v1\|section\|refs` and `v2\|role\|path\|section\|refs\|class` with escaped pipes (4 cells under the 4-column header). synth-04 :769 row E1 has `v2\|role\|path\|\|refs\|class` escaped (3 cells under 3). Script S1: 0 bad rows in all seven files, including these two rows. |
| P5-B23-r | yes | synth-04 :720 Pros cell: "fixes three unparseable shadow contracts and narrows the self-attested EV-1 (it stays an on-disk presence check, Q-56)"; it now agrees with :712 ("narrows the self-attestation but EV-1 remains an on-disk presence check ... open item Q-56"), synth-05 7.1.3, synth-06 M2-02 and synth-07 Q-56. synth-06 V-271 (:301) Reason: "EV-1 is self-attested today (GQ:G-13); the C-11 design has the merge step write the verdict file with its own `merge_method`, which narrows the self-attestation but EV-1 stays an on-disk presence check (Q-56)". Grep for `self-attest`, `stops being`, `ends the self` over the seven files: every hit either states the current gap (synth-01 :80, synth-02 :159, synth-07 :47) or the narrowed, presence-check wording (synth-04 :712, :720, synth-06 :301); synth-06 :774 "blocking post gate stops being a false green" is about the tasklist post gate. No sentence says EV-1 stops being self-attested. |

Result: 4 of 4 fixed.

## Section C: regression spot-check of the 21 findings cycle 1 passed (check (b))

Spot-checked P5-B1, B3, B4, B11, B12, B15, B19, B21 against their cycle-1 evidence. None of these locations is in the cycle-2 diff except where noted, and each still holds.

| Finding | Still fixed? | Evidence (re-read this cycle) |
|---|---|---|
| P5-B1 | yes | Grep for `measured driver`, `same conclusion`, `driver of Tier`, `input-format reason`, `forcing Tier`: 3 hits, all acceptable: synth-04 :917 "As drafted for the debate: stop the parsed-sparse pre-filter from forcing Tier 2" (Option B description, labelled as drafted, and followed by the hypothesis wording), synth-05 :292 (the list of corrected sentences), synth-06 :587 V-557 (source's claim with correction in the same row). synth-04 :897 still says 38 of 39, flag set in 35 of 39 (34 of 38), decisive in 0 for certain and at most 1, "cost driver is not established"; :954 still Step A, CI-1, D-1, H-A. Winner B unchanged (S5). |
| P5-B3 | yes | synth-01 :73: "38 of 39 ... flag was set in 35 of 39 runs (34 of the 38 Tier 2 runs) and was decisive in 0 for certain, at most 1 ... counts only, cause not established"; Strength cell "measured census of counts; cause not established". |
| P5-B4 | yes | synth-02 :240 DOC-59 "Counts superseded by the 2026-11-13 recount ... not carried"; 4.1 row 16 (:273) present with the recount and the model-written-fields caveat. |
| P5-B11 | yes | synth-06 M1-07 uses the probe numbering INV-001 to INV-010 (`defer`, atomic vs bounded refusal, `prior` open, undefined valid reviewer, would-be PASS, second `ledger revise` = INV-006, quorum denominator, spanless row = INV-008, `evidence` on `prior`, sufficiency); V-118 and V-432 say INV-006, V-431 says INV-008. |
| P5-B12 | yes | G9 collects 271 (S3); G9 text says "the remaining 34 of the 38 test files" and 353 = 271 + 82; V-558 "353 in 38 `tests/cli/reflect` files"; V-612 "resolved: 38 files ... G9 covers 34 files"; V-054 "59 runs with extra `modelUsage` keys, 57 of them an auxiliary ... call (R08 :307)". |
| P5-B15 | yes | synth-07 Section 9.5 (:242) still holds rows Q-47 to Q-57 (first-column scan: Q-01 to Q-57 each once in Section 9 and once in the 9.1 index, S4); the Inputs line (:7) still names `reviews/adversarial/`. |
| P5-B19 | yes | synth-06 M2-07 still names `matching_rows`, `calibrated_C_t1`, `S_domains_basis`, `tier_without_flag`, `sparse_flag_decisive`, `escalation_path`, `reviewers_requested`, `reviewers_resolved`, `reviewers_source` and `reflect_tier_recompute`; synth-05 Rationale 6 (:31) and the C-14 row (:51) keep the same Step A / CI-1 / Step B / Step C wording. |
| P5-B21 | yes | synth-06 M2-02, M2-09 and G8 still say `:344,:346` are in 4.3a and `:714` (section 8) and `:1955,:1958` (17.6) are outside the C6 allowed sections 3.1, 4.3a, 5.4, 9.2, so the allowed list changes in the same change. |

Other regression checks: the cycle-2 diff changed only table rows or single sentences (no row was added or removed; synth-06 V rows still 691, 0 duplicate ids; synth-04 still 20 conflict blocks and 65 option blocks); S1 shows no broken table anywhere; the C-14 block and the four adversarial-result blocks are untouched. No finding that passed at cycle 1 regressed.

## Section D: new blocking defects (check (b))

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| none | | | No new CRITICAL or IMPORTANT defect found. Checked: broken tables (S1), removed required content (S7), new uncited claims (every changed line read; each new caveat is sourced to the C-04 Status at synth-04 :286-:288, synth-01 :94 for the 28 p-values, or Q-56), cross-file inconsistency between synth-04, synth-05 and synth-06 on C-04, C-11 and the Option B dependency sentence (consistent), debate winners (S5), E2 commit (S6). | n/a |

## Minor notes (do not fail the gate, not rechecked)

| # | Location | Note |
|---|---|---|
| m1 | synth-04 index row C04 | The Status column still reads DECIDED-BY-EVIDENCE; the resolution cell now states the split, so the row is not misleading. |
| m2 | synth-04 :288 (C-04 Recommended resolution) | Ends with "choose strict for reflect finders and allow replicas for evaluation panels", slightly stronger than "optional design option" in the same cell; the cell also says no replica is enabled by default. |
| m3 | synth-05 7.1.1 box, lines 104 and 107 | Two box rows are 1 to 2 characters narrower than the rest (90 and 89 against 91); the widths are identical to the cycle-1 state, so not introduced by cycle 2. |
| m4 | Cycle-1 minor notes M-01 to M-23 and the cycle-1 verifier notes (synth-02 :263 "37 vs 38", `cluster_v2` range, garbled sentence at synth-04 :368, V-399 wording, Q-31/Q-32 phrasing) | Not fixed, not rechecked, per the severity rule. |

## Summary

- Findings fixed: 4 / 4 (P5-B9-r, P5-B10-r, P5-B14-r, P5-B23-r).
- Scripted checks S1 to S7: 7 / 7 PASS.
- Regression spot-check of P5-B1, B3, B4, B11, B12, B15, B19, B21: 8 / 8 still fixed; no regression of the 21 findings passed at cycle 1.
- New blocking defects: 0 (CRITICAL 0, IMPORTANT 0). Open blocking findings after this cycle: 0, so |F_3| = 0 < |F_2| = 4 and the monotonicity guard does not fire.
- Minor notes: 4.
- Required contents (a) to (e): all present.
- Issues fixed in place: 0 (fix authorization false; only this report was written).
- Confidence: Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist = 4 findings + 8 regression spot-checks + 7 scripted checks + new-defect check + required-contents check + cross-file consistency check + diff-scope check; the 100% is coverage of the checklist, not a claim that the synthesis is error-free).
- Tool engagement (approximate): Read: 7 | Grep: 3 | Glob: 0 | Bash: 17. No web research; no Tavily or web fallback used.

## Overall Verdict: PASS

All four cycle-2 findings are fixed in every place the cycle-1 verifiers named, no fix regressed an earlier pass, no new blocking defect was found, and the required contents (a) to (e) and all scripted invariants hold.

## QA Complete

Required contents (task file Execution Context): (a) overlap matrix = synth-01 2.6; (b) value inventory = synth-06 8.1; (c) conflict log = synth-04 Section 6; (d) target architecture = synth-05 7.1; (e) future-use-case check = synth-05 7.2.
