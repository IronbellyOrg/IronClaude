# QA Report: Phase 5 Synthesis Coherence Verification

**Topic:** Fresh check of what the synthesis means after the Step 5.24 fixes (cycle 1). It covers synthesis components 01-06, hypothesis cards 01-05 and the actual debate artifacts.
**Date:** 2026-10-24
**Phase:** synthesis-gate verification, Task Step 5.26 (report-qualitative checklist plus the synthesis-coherence lens)
**Lens:** Synthesis coherence and content verification
**Fix cycle:** 1 (of at most 2)
**Fix authorization:** false (report only)
**Governing format:** the Standard QA Report Output Format in `/config/.claude/skills/task/SKILL.md:466-506`, plus the 12-item qualitative checklist in `/config/.claude/skills/tech-research/SKILL.md:1020-1032` and the synthesis-coherence lens at `:507`. The Axis column is left out because this is not a task-qualitative review.
**Intended output:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-verification-content.md`

**Delivery limitation:** the higher-priority rules for this session stop me writing report files. I created no file and edited nothing. This text is the complete report for the parent to save at the path above.

All relative paths resolve under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. `ADV/` means `reviews/adversarial/adversarial/`.

---

## Overall Verdict: FAIL

- **Original PASS now FAIL (checked first):** 0. No check that passed at cycle 0 now fails.
- **Original findings not fully fixed:** 1 (U-1, the remainder of P5-18, MINOR).
- **New findings:** 3 (N-1, N-2, N-3). All are IMPORTANT, because each is a contradiction inside the corrected synthesis.
- **Regression check:** not triggered.
- **Failure-count check:** |F1| = 4 against |F0| = 33. The count shrank, so no halt is triggered.
- **Fix cycles:** this is cycle 1 of 2. One more fix cycle is allowed before the cap.

**Bound targets:** all 11 targets currently hash to the fix log's "After all patches" SHA-256 values (`qa/qa-synthesis-fix-log.md:112-122`, recomputed with `sha256sum`). So I reviewed the exact applied state.

## Items Reviewed

### Check sets, in the order the task requires

**1. Original PASS now FAIL.** None.

I re-checked every protected cycle-0 PASS identity in the meaning-oriented reports against the corrected text:
- qualitative-1: #1, #3, #5, #6, #7, #9, #10, #11, #12, #13
- qualitative-2: #1, #5, #6, #8, #9, #12, #14, #16
- content-1: #8, #12
- content-2: #8, #10, S3, S4, S5
- accuracy-2: synth-04 #1, #2, #5, S3; synth-05 #3, #6, S4; synth-06 S4

Each still holds. The evidence is in the table below and in the Self-Audit.

**2. Original findings not fully fixed:** U-1 (P5-18 remainder).

**3. New findings:** N-1, N-2, N-3.

### Status of the 33 cycle-0 findings

| Group | Corrected state checked against the sources | Result |
|---|---|---|
| P5-01 | All six components now end with a `## Provenance and Delivery Record (not for assembly)` block marked NOT-ASSEMBLED. The status lines and DONE/NEXT tables were moved there unchanged. Each receipt says "states or implies no synthesis-gate verdict". | Resolved |
| P5-02 | synth-03:72 now reads `### 5.5 Evidence and Limits`. | Resolved |
| P5-03 | synth-02:42 states the reason for the uniform rating. That reason matches the template's Critical rule for unwired capabilities (`tech-research/SKILL.md:1374`). Rows 57-59 now use `Important` with "Inference limit." | Resolved |
| P5-04 | synth-01:74 adds the chain "first FINAL issues (dispatch 1916; nested record 135; parent 1932)". This matches `06-session:137-139` and deck:350. | Resolved |
| P5-05, P5-06 | synth-01:12 and :15 now carry the trigger and cite `BUILD-REQUEST.md:12,14`. Those lines were re-read and match. | Resolved |
| P5-07 | synth-01:59 cites deck:105,662. Deck:105 says the sample is "not a measured failure rate". | Resolved |
| P5-08 | synth-03:82 cites task file line 68. That line contains "publish". | Resolved |
| P5-09 | synth-01:72, synth-02:54, :87 and both coverage rows now carry the claims at records 791 and 801, the "16 fixed, 2 partial" figure and the "ready with notes" verdict. These match `04-session:102-104,114-118,240,244`. | Resolved |
| P5-10, P5-11, P5-12 | The added anchors were re-read: deck:312, :350, :505, :558, :596, :244; `06-session:156-175,381`; `03-session:173-178`. Each supports its clause. | Resolved |
| P5-13 | synth-02:55 adds the 13/3 closure error and the condensed verdict, matching deck:858-859 and `01-session:81,253`. All nine deck items at :855-863 now sit in Section 4 or Section 9 (item 7 via Q17). | Resolved |
| P5-14 | synth-05:91-92 add unexecuted rows that need approval. Their bindings were re-read. | Resolved |
| P5-15 | Both control lists are now tables. The original prose (taken from the patch needles) is fully preserved, and every row matches deck:647-655. | Resolved |
| P5-16 | synth-03:20-21 now give the runner unknowns to the monitor case (`05-session:292-293`). | Resolved |
| P5-17 | synth-05:70 adds the monitor input. synth-05:75 adds the order-4 row. synth-04:284 says that Section 7.6 alone sets the order. | Resolved, but see N-3 |
| P5-18 | The controls were added to Options A, B, D and E and to synth-05:87, and synth-04:309 states the exclusions. The deck limits are given for Option A and Option D, but not for Session 10 Task 4 or Session 17 Task 8 in Options B and E, or in synth-05:87. | **Partly fixed (U-1)** |
| P5-19, P5-20, P5-21, P5-22 | Wording and anchors were re-read: transcript lines :168, :379, :381, :384-385 and :425; `refactor-plan.md:32-33`; deck:389,595. The rank positions are unchanged. | Resolved |
| P5-23 | synth-04:62 now says v4 passed the structural gate and was never semantically reviewed (`01-session:85-86`). | Resolved |
| P5-24 | synth-04:65 is supported by `01-session:323` and its hash table at :330-333, which has no comparison target for v3. | Resolved |
| P5-25 | The dated superseding rows are present, and the qa/ count of 204 still matches the current directory. | Resolved, but see N-1 |
| P5-26 | synth-06:176-177 match `plan-review-evidence.md:4-28` and `merge-log.md:161-163`. | Resolved, but see N-1 |
| P5-27 | The three template subsections are present (synth-06:40-56) and the header states the adaptation. | Resolved |
| P5-28 | Each card's chapter 1 has the presentation note. My own exact-once recheck found every non-heading line of `variant-1..5-original.md` once in its card. The only exception is `\|---\|---\|---\|`, which appears twice in every card both before and after the patch. | Resolved |
| P5-29 | Each current-rule citation now names its layer. The pin text is at checkout line 42 and installed line 43, and `qa.md:82` is the same in both layers. | Resolved |
| P5-30 | synth-06:34 cites transcript :49 ("task size is an observed amplifier, not an isolated cause"). | Resolved |
| P5-31 | Option B Scope, Alternatives, the comparison row and the 7.1 override now follow `variant-2-original.md:10,37,54` and transcript :269,272. No card or variant was edited. | Resolved, but see N-2 |
| P5-32 | "only unanimous exact rank position" appears at synth-04:67, :202 and :288. | Resolved |
| P5-33 | synth-04:146 restores the location qualifier. The candidate file exists (1,006 bytes) and is stated as not hash-verified. | Resolved |

### Qualitative checklist (`tech-research/SKILL.md:1020-1032`) and step-specific checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Problem statement matches findings | PASS | synth-01:10-12 states the six-way disposition question. synth-04:6 and 7.1 answer it. The trigger now matches `BUILD-REQUEST.md:14`. |
| 2 | Options are genuinely distinct | PASS | All five card identities survive (my exact-once recheck). P5-31 keeps V2's two outcomes separate, as in `variant-2-original.md:37`. |
| 3 | Recommendation follows from the analysis | PASS | synth-04:195-203: V1 first is the only unanimous placement (transcript :477-484), and the next step is Option A's replay, research-only and approval-bounded. |
| 4 | Implementation plan is actionable and coherent | FAIL | N-3: Section 8's count and its Phase 2 goal contradict the added order-4 row. |
| 5 | Gaps are honestly acknowledged | PASS | Unknown reviewer misses, the unknown rubric updater, the policy/proof confounding and unobserved runtime behavior remain (synth-02:58; synth-06 Q2-Q4, Q8; synth-04 7.3). |
| 6 | No circular reasoning | PASS | The ranking rationale cites only the transcript and the refactor plan. The added controls cite the deck, not the synthesis itself. |
| 7 | Evidence trail is complete and accurate | FAIL | N-1: synth-06:64 misstates which rows are unchanged history. N-2: the synth-04 7.8 reading-limits table contradicts text added at Step 5.24. |
| 8 | Conclusion is proportionate | PASS | synth-04:237-241 keeps the bottom pair "following the smaller side", gives the weakest step and keeps the `partial` status. No probability appears (grep for `%`, "probabilit" and "likel": every hit is a negation or a disclaimer). |
| 9 | External research is put in context | PASS | synth-03:9 and synth-06:36 keep the reasoned N/A with zero queries. |
| 10 | Sections agree with each other | PASS | Gap rows 6 and 9 now map to plan rows synth-05:91-92. The 7.6 orders map to synth-05:70-75. Gap row 8 is covered by synth-05:89. The 7.4 row "V2 within a V1-style family" is consistent with `variant-2-original.md:54` and deck:388. |
| 11 | Technical accuracy | PASS | Every anchor added by the fixes was re-read (Self-Audit). |
| 12 | Depth matches the Deep tier | PASS | Five full assessment tables, the pair tallies, the overlap cautions and a 20-question register. |
| S1 | Each of the 33 corrections is verified against its sources | FAIL | 32 are fully resolved. P5-18 is partial (U-1). |
| S2 | Previously passed meaning checks still hold | PASS | No regression (set 1 above). |
| S3 | Ranking is proportionate to the recorded debate | PASS | The displayed order is V1 > V3 > V2 > V5 > V4, labelled non-consensus (synth-04:197). V3 above V2 has 3 of 5 and V4 above V5 has 3 of 5 (:230-233), matching transcript :486 and `return-contract.md:24`. The displayed bottom step follows the 2-of-5 side (:238). Writing scores are not treated as likelihood (:249; 6.0 table). |
| S4 | Added screened controls do not imply the advocates weighed them, and nothing is re-ranked | PASS | synth-04:309 says so explicitly. A grep of all five variants, the transcript and the merged analysis for Sessions 09/10/13/14/17/19 and "restore-basename" returns nothing. The 7.1 and 7.2 tallies are unchanged. |
| S5 | Overlap, controls and unknowns survive | FAIL | Overlap (7.4) and the unknowns survive. Control limits are missing in two options and in one plan row (U-1, counted once). |
| S6 | Historical classifications are unchanged | PASS | P5-04, P5-13, P5-14 and P5-23 add or correct events without reclassifying them. Consent and checkpoint events stay "not a ranked repeat cause" (synth-04:278; synth-05:91). |
| S7 | Recommendation stays research-only | PASS | synth-04:284; synth-05:75, :91-92 and :102 say UNEXECUTED and that approval or a user scope decision is required. |
| S8 | The fixes introduced no new inconsistency | FAIL | N-1, N-2 and N-3. |

## Summary

- Checks passed: 15 / 20
- Checks failed: 5 (items 4 and 7, and S1, S5 and S8). These cover 4 unique issues.
- Critical issues: 0. IMPORTANT: 3 (N-1, N-2, N-3). MINOR: 1 (U-1).
- Original PASS now FAIL: 0. Not fully fixed: 1. New: 3. |F1| = 4.
- Issues fixed in place: 0 (report only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| U-1 | MINOR | synth-04:83 (Option B Opposition) and :161 (Option E Opposition); synth-05:87 | **P5-18 is only partly fixed.** P5-18 required each control "with its deck anchor and the limit stated there". The fix log says "each with its stated limit" (`qa-synthesis-fix-log.md:50`). Options B and E cite the Session 10 Task 4 and Session 17 Task 8 controls without the deck limits (`evidence-deck.md:650-651`: "Original implementation package absent from searched locations; logs/Edit survive"; "Later PR reviews are separate development work"). synth-05:87 also leaves out those two limits and the Session 17 FINAL limit "Not strict fail-fix-fail" (deck:652). Option A (synth-04:56) does state them, so a reader of B or E sees a stronger control than the deck supports. | Add the two deck limits to the Options B and E Opposition rows, worded as at synth-04:56. Add all three limits to synth-05:87. Do not re-rank. |
| N-1 | IMPORTANT | synth-06:64 versus :176-177 and section 10.2 | **The historical-snapshot statement is now false.** synth-06:64 says every row in 10.1-10.8 that is not marked "Superseding" records the 22:14:30Z observation and "is kept unchanged as historical". But Step 5.24 changed unmarked rows in place: patch 213 (`qa-synthesis-fix-log.md:213`, `"repl": "\n"`) removed the web-01 row from 10.2, and patches 219-220 rewrote the 10.5 plan-review-evidence and merge-log rows (synth-06:176-177). The corrections themselves are right (P5-26, P5-27); the claim about which rows are untouched is what is wrong. | Change the sentence at synth-06:64 to say that three rows were corrected in place at Task Step 5.24 (web-01 moved to Web Research; the 10.5 plan-review-evidence and merge-log rows corrected). Alternatively, mark those rows "Corrected at Task Step 5.24". |
| N-2 | IMPORTANT | synth-04:323-324 versus :85 and :284 | **The reading-limits table contradicts text added by the fixes.** 7.8 says `ADV/variant-*-original.md` were "Not read directly" (:323), yet the corrected Option B Scope cites `ADV/variant-2-original.md:10,37` directly (:85). 7.8 also says synth-05 was read at "Lines 1-40 only; referenced by path, not by step identifiers" (:324), yet the corrected 7.6 says how Section 8's rows are grouped and that order 4 appears there as a user scope decision (:284; the row is at synth-05:75). A reader cannot tell whether those added claims rest on files the component says it did not read. | Add a dated Step 5.24 line to 7.8 recording that the fixer read `ADV/variant-2-original.md` (lines 10, 37), the transcript lines :269 and :272 and synth-05 in full, keeping the producer's original rows. Wording only: no change to the ranking. |
| N-3 | IMPORTANT | synth-05:11, :66, :75, :120 | **Section 8's count and its Phase 2 framing contradict the added row.** synth-05:11 says the section "retains and sharpens the existing five discriminating checks", and the coverage row at :120 says "All five comparisons use its six causal classes". Phase 2 now has six comparison rows (:70-75), and Phase 3 has two new comparison rows (:91-92). Phase 2's goal is to test explanations "using existing counterexamples and retained history", and it depends on Phase 1's evidence binding (:64-66). The added order-4 row says "No existing input" and "outside the current research scope" (:75). | Update :11 and :120 to say there are five original comparisons, one row needing a user scope decision (7.6 order 4) and two Phase 3 separation checks. Then either move the order-4 row into its own "Outside current scope: needs user decision" subsection, or state in Phase 2's Goal and Dependencies that this row is the exception. Keep it UNEXECUTED. |

## Actions Taken

- Read Task Step 5.26 and its neighbouring steps (task file :331-371). Read the governing formats: `task/SKILL.md:466-506` and `tech-research/SKILL.md:995-1032`, :1362-1375 and :507.
- Read in full: the consolidation, the fix log (lines 1-122 and 233-265, including the Parent Application Record), synth-01 through synth-06, `run-evidence.md`, `return-contract.md`, `refactor-plan.md` and `plan-review-evidence.md`.
- Read the header and chapter 1 of each card, plus every card line that refers to the card itself.
- Read the transcript lines that carry the A-001, S-002, C-001 and C-003 rows and the Round 1 and Round 2 critiques (:39-55, :128-130, :166-169, :207-209, :240-310, :333-345, :376-386, :412-489). Read `merge-log.md:159-164`, `merged-root-cause-analysis.md:15-45` and `variant-2-original.md:8-12,35-40,54`.
- Ran one bounded read-only batch over the cited ranges of the evidence deck and case reports (private `mktemp` directory, `BATCH_OK failures=0`, `CLEANUP_OK`). Ran targeted read-only greps, hash checks and the card exact-once check.
- Edited no file and created no file. Ran no agents, tests, Git, staging, archive, move, delete or publication. Sent the team lead one short completion notice with no report body.

## Self-Audit

**(a) Reliance list: rf-qa PASS items I relied on without re-checking structure:**
- No Inherited Structural Verdict was supplied. The Step 5.25 report `qa/qa-synthesis-verification-structural.md` did not exist when I checked (`ls qa/qa-synthesis-verification-*` returned "No such file"). So I relied on no structural PASS and worked standalone.
- I relied on the fix log's statement that patches were applied byte-exactly only after independently recomputing all 11 SHA-256 values.

**(b) Independent semantic checks (at least one required):**
- **Ranking proportionality:** compared synth-04:205-241 with transcript :477-486, `return-contract.md:24`, `run-evidence.md:16` and `refactor-plan.md:27-35`.
- **Controls not weighed by the debate:** grep of the five variants, the transcript and the merged analysis for the screened sessions returned nothing. The deck control rows :647-658 were matched to every placement.
- **P5-31 fidelity:** `variant-2-original.md:10,37,54`; transcript :269, :272, :295 and :379; deck:388.
- **Card identity:** my own line-by-line exact-once check of all five variants against the cards.
- **Corrected claims re-read at their sources:** 01-session :81, :85-86, :90-103, :253 and :323-333; 04-session :102-118 and :240-244; 06-session :129-176 and :381; 03-session :171-178; 05-session :290-294; deck :100-106, :278-282, :310-314, :348-352, :386-407, :503-507, :556-598, :624-632, :643-668, :707-731 and :853-864; both protocol layers for `managed-workspace.md` and `qa.md:82`; `BUILD-REQUEST.md:12,14`; task file :68; the t10 log path.
- **Original control prose:** taken from the P5-15 patch needles and compared with the new tables, so nothing was dropped.
- **Whether the fixes edited historical rows:** read fix-log patches 213, 219 and 220 (basis for N-1).

**Mandatory questions:**
1. **Claims checked independently against sources:** about 95 (all 33 groups, 31 protected PASS identities, the ranking and tally facts, and the anchors).
2. **Files read:** listed under Actions Taken.
3. **Why the result is not a false zero:** four defects were found. Every finding cites lines I read this session.
4. **Web research:** none was performed. No Tavily or fallback call was needed.

**Confidence:** Verified 20/20 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%. A PASS is still impossible because four defects remain.

**Tool engagement:** Read 16 | Grep 0 (greps ran inside Bash) | Glob 0 | Bash 22, including one bounded batch.

## Recommendations

- Step 5.27 should record this FAIL. The regression check is clear (no protected PASS now fails). The failure count shrank from |F0| = 33 to |F1| = 4, so no monotonicity halt. Fix cycle 2 of 2 is the last one allowed.
- In cycle 2, one fixer should apply U-1, N-1, N-2 and N-3 as wording or placement changes only. That means no re-ranking, no card or variant edits and no change to the debate artifacts. Fresh verifiers should then check the result.

## QA Complete

| Status | Result |
|---|---|
| DONE | Checked all 33 corrections, the 31 protected PASS identities, the ranking, the controls, the unknowns and research-only scope against the actual sources and the debate. Verdict FAIL: 0 regressed, 1 not fully fixed (MINOR), 3 new (IMPORTANT). |
| NEXT | The parent saves this exact text at `qa/qa-synthesis-verification-content.md`. Step 5.27 then decides cycle 2, which is the last fix cycle allowed. |