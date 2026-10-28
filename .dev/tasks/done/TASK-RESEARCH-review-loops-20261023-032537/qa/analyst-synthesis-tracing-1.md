# Synthesis Quality Review - Source Tracing, Partition 1

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only review; text returned to the parent for persistence because this reviewer is not permitted to write report files)
**Files reviewed:** 3 (`synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`)
**Lens:** source-tracing
**Task item:** Step 5.15
**Partition:** 1 of 2
**Governing template:** Project rf-analyst Synthesis Quality Review Output Format; tech-research synthesis checklist

## Overall Verdict: FAIL (6 issues: 1 important, 5 minor, 0 critical)

## Per-File Review

### synth-01-problem-current-state.md
**Sections covered:** 1 and 2
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | Not in this lens | Belongs to Steps 5.13 and 5.17. Headings were only read here to locate claims. |
| 2 | Table column structure | Not in this lens | Belongs to Steps 5.13 and 5.17. |
| 3 | No content fabricated beyond research | FAIL | All six case-history rows match the cited case files and the evidence deck: counts 16/14/2/20, 67/78 tests, 18 then 5 medium/11 low, 7 verdicts/5 reviewers/5 repairs, raw records 499-946, 291-668, 188-234, 430-527, 623-1084, 585-1261, 390-2036. No fabricated event was found. However, the research question in section 1 (line 11) names `/sc:workflow` and `/sc:implement`, and neither cited anchor contains those names (Issue 1). |
| 4 | Citations actually substantiate statements | FAIL | Two defects. Issue 1: the line 15 anchors do not support the command names. Issue 2: the credential-incident primary transition chain (line 67) gives no anchor for the incident's first failed FINAL review. All other anchors were spot-checked against the cited lines and support their statements, including all ten section 2.3 protocol-source anchors re-read in the current checkout. |
| 5 | Options with pros/cons | N/A | Outside sections 1-2. Covered by partition 2. |
| 6 | Implementation plan specificity | N/A | Outside sections 1-2. Section 8 is in partition 2. |
| 7 | Cross-section consistency | PASS | Sections 2.1, 2.2, 2.5 and 2.7 agree with each other and with synth-02 sections 3-4: strict subset of three, one rendering blocker, two planning sequences, seven synthetic exclusions, 14/2 Orca closure, and observation-scoped seven-pair agreement versus later three equal/four different. |
| 8 | No doc-only current architecture | PASS | Section 2.3 is labeled as checkout instruction source, not runtime proof. Every row cites `src/superclaude/skills/...` lines, and I re-read each one: SKILL.md:48-72, quality-gates.md:24-41, qa.md:9-17/25-52/62-68/80-90, retry.md:142-146, ledger.md:138-158/142, managed-workspace.md:42-68/78-85. The working tree for those paths is clean, and their SHA-256 values equal the original hashes in `qa/qa-research-verification-structural.md:115-121`. |
| 9 | Stale/contradicted sources surfaced | PASS | Both `[CONTRADICTION: ...]` markers from `gaps-and-questions.md:33-35` appear in section 2.5 with both versions kept. The aged seven-pair equality, the omitted ledger FINAL, the relocated documentation evidence, `head-moved` and historical positions are all surfaced. No `[CODE-CONTRADICTED]` or `[STALE DOC]` tags exist in the research inputs (grep found none). |
| 10 | Key Takeaway coverage | FAIL | The section 2.6 matrix covers most case takeaways. It omits the CI case's intermediate-assessment and premature-completion findings without an exclusion rationale (Issue 3). |
| B | Historical/current boundary | PASS | Present protocol text is never projected onto historical runs (lines 75, 102, 167). The monitor and CI continuation windows are kept separate (line 48). The execution-time protocol comparison is excluded from ranking evidence (line 132). |

### synth-02-target-gaps.md
**Sections covered:** 3 and 4
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | Not in this lens | Belongs to Steps 5.13 and 5.17. |
| 2 | Table column structure | Not in this lens | Belongs to Steps 5.13 and 5.17. |
| 3 | No content fabricated beyond research | PASS | Every success criterion, constraint and gap statement traces to case files, the deck, the rule map, the gap register or web-01. Examples: 14 accepted and 2 partial (deck:465-482); "retains a compliant completion" (06:381); documentation wrong-task rejection (deck:244, 03:173-178); credential softening (06:156-175). Nothing invented was found. |
| 4 | Citations actually substantiate statements | FAIL | In three Gap-table rows the row-specific anchors cover only some of the factual clauses: row 1 (Issue 4), row 3 (Issue 5), row 6 (Issue 6). Rows 2, 4, 5 and 7-12 were checked clause by clause against their cited ranges and pass. |
| 5 | Options with pros/cons | N/A | Partition 2. |
| 6 | Implementation plan specificity | N/A | Partition 2. |
| 7 | Cross-section consistency | PASS | Target criteria agree with synth-01 sections 2.1-2.2. The gap inventory matches synth-01 section 2.4. The constraint on instruction freshness matches synth-01 section 2.5 and synth-03 section 5.4. Severity is stated as non-likelihood (line 44), consistent with synth-01's no-ranking scope. |
| 8 | No doc-only current architecture | PASS | Section 4 frames every row as a historical delivery, process or evidence gap or as an explicit inference limit (lines 44-46, 63-65). No present component is claimed missing or unwired. |
| 9 | Stale/contradicted sources surfaced | PASS | Gap rows 3, 8, 9 and 10 carry the source contradictions, ledger omission, checkpoint-label misreading and live-source drift. The constraints row on line 36 carries the protocol-copy drift. |
| 10 | Key Takeaway coverage | FAIL | The CI row of the Key Takeaway table (line 82) has the same omission as synth-01 (Issue 3). The other eight topic rows were checked against the case and deck takeaway sections and pass. |
| B | Historical/current boundary | PASS | Lines 23, 35-36 and 59 keep historical loads, observation windows and current instruction text separate. |

### synth-03-external-findings.md
**Sections covered:** 5
**Verdict:** PASS

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | Not in this lens | Belongs to Steps 5.13 and 5.17. |
| 2 | Table column structure | Not in this lens | Belongs to Steps 5.13 and 5.17. |
| 3 | No content fabricated beyond research | PASS | The N/A decision, the zero queries, sources and findings, the providers NOT invoked and "availability not tested" all match `web-01-gap-applicability.md:14-22, 97-115`. "No additional external-research Markdown file" matches the actual `research/` listing (only `web-01-*` exists). |
| 4 | Citations actually substantiate statements | PASS | Anchors re-read and confirmed: task file :253-259 (Step 4.1 allows a justified N/A), web-01 :14-22/:26-56/:60-94/:97-115/:127-150/:180-182, deck :643-668/:733-737/:814-823/:827-847/:884-890, gaps :29-59/:55-59. "All fifteen evidence-deck questions" is correct: deck rows 831-845 are 15, and web-01 rows 32-49 are those 15 plus 3 extra limits. All 15 are distributed across the nine section 5.1 rows. |
| 5 | Options with pros/cons | N/A | Partition 2. |
| 6 | Implementation plan specificity | N/A | Partition 2. |
| 7 | Cross-section consistency | PASS | Section 5.3 restates the deck's overall Key Takeaways (814-823) consistently with synth-01 section 2.7 and synth-02 section 4. Protocol freshness (line 81) matches synth-01 section 2.5 and synth-02 line 36. |
| 8 | No doc-only current architecture | PASS | Describes no current component. Line 81 explicitly disclaims any certification of runtime or helper behavior. |
| 9 | Stale/contradicted sources surfaced | PASS | Row 3 of section 5.1 preserves both Orca contradictions. The web-01 "not persisted" wording is explained as delivery state, not approval (line 47). |
| 10 | Key Takeaway coverage | PASS | Section 5.3 maps the deck's overall takeaways. Section 5.4 maps web-01's takeaways (web-01:53-56, 91-93). The deck chronology is explicitly excluded with a rationale (line 65). |
| B | Historical/current boundary | PASS | Lines 25, 27 and 81 keep fingerprints, membership and dated protocol observations at their actual scope. |

## Claim and Key-Takeaway Source Bindings

| Claim group (target:line) | Primary binding verified | Result |
|---|---|---|
| synth-01:11 research question names `/sc:workflow` and `/sc:implement` | Cited task file :64-75 says "planning and task-execution reviews". Deck :14-64 says nothing about commands. Actual source: `BUILD-REQUEST.md:12` | Unsupported by cited anchors (Issue 1) |
| synth-01:21-35 population, units, exclusions | deck:14-45, 74-105 (indexes 21-24 and 28-30 = seven synthetic), manifest | Supported |
| synth-01:41-46 strict subset, planning statuses | deck:49-58, 145-156 | Supported |
| synth-01:48 window boundaries | 05:315-355, 387-411; 04:66-87, 275-309 | Supported |
| synth-01:62 Orca row | 01:59-103, 110-198, 286-340, 375-442; 15 v4 edits at 01:84; source hash at 01:328, 340 | Supported |
| synth-01:63 oracle row | 02:77-102, 184-275; deck:208-216, 495 | Supported |
| synth-01:64 documentation row | 03:45-111, 144-188, 190-258 | Supported |
| synth-01:65 CI row | 04:120-248, 275-309, 334-361, 511-610 | Supported, but key takeaways omitted (Issue 3) |
| synth-01:66 monitor row | 05:12-27, 52-71, 81-103, 113-254, 387-411, 487-502 | Supported |
| synth-01:67 credential row | 06:11-32, 64-129, 131-266, 268-319, 367-387 | Supported, but the first follow-up FINAL issues record (parent 1932, deck:350, 390) is missing from the chain (Issue 2) |
| synth-01:69-71 controls | deck:643-668 (rows 647-654) | Supported |
| synth-01:79-84 current protocol rows | Re-read in the current checkout; hashes match the original recorded source hashes | Supported |
| synth-01:104-106 historical policy changes | 05:223-236; 06:238-266; scope-rules:64-77 | Supported |
| synth-01:110-122 what checks establish | 02:222-248; 05:52-75, 193-221, 238-250; 06:238-309; deck:608-668 | Supported |
| synth-01:126-135 exceptions | 01:90-103, 217, 255-267, 294-301, 342-350; gaps:29-35, 53-59; 03:341-362; qa-structural:93-127; 06:189-236; 05:273-287, 413-438 | Supported |
| synth-02:18-25 success criteria | deck:14-64, 74-105, 130-164, 461-484, 643-668 | Supported |
| synth-02:33-38 constraints | scope-rules:29-58, 64-88; gaps:53-59; web-01:26-56 | Supported |
| synth-02:50 gap row 1 | deck:585-598 covers Orca and oracle only | Partially unsupported (Issue 4) |
| synth-02:51, 53, 54, 56-61 gap rows 2, 4, 5, 7-12 | Cited ranges checked clause by clause | Supported |
| synth-02:52 gap row 3 | gaps:29-35, 57-59 and scope-rules:64-77 do not cover the credential task-QA softening | Partially unsupported (Issue 5) |
| synth-02:55 gap row 6 | deck:564-569 does not cover "compliant completion" or the documentation wrong-task rejection | Partially unsupported (Issue 6) |
| synth-03:11-29 N/A decision and inventory | task :253-259; web-01:14-56; deck:827-847; gaps:29-59 | Supported |
| synth-03:33-47 provider record | web-01:97-115, 180-182 | Supported |
| synth-03:53-71 retained local findings | deck:643-668, 733-737, 814-823, 884-890; web-01:60-94 | Supported |

| Research Key Takeaway source | Represented in partition-1 synthesis | Result |
|---|---|---|
| 01 Orca (sections 2, 3, 4, 5, 6, 7 and supplements) | synth-01 sections 2.2, 2.4, 2.5, 2.6; synth-02 rows 1-3, 7 | Covered |
| 02 Oracle (sections 3-7) | synth-01 sections 2.2, 2.4, 2.6; synth-02 rows 1, 5 | Covered |
| 03 Documentation (sections 2-7, current location) | synth-01 sections 2.2, 2.5, 2.6; synth-02 rows 4, 5, 9 | Covered |
| 04 CI, section 4 bullets 2-3 ("16 fixed, 2 partial" was one reviewer's intermediate assessment, later corrected); section 8 mechanisms 3 and 5 (regeneration declared complete before finding-by-finding verification; initial "ready with notes") | Not represented and not excluded with a rationale | Missing (Issue 3) |
| 04 CI, other takeaways | synth-01 sections 2.2, 2.6; synth-02 rows 1, 2, 7 | Covered |
| 05 Monitor (sections 1-8, continuation, identity) | synth-01 sections 2.2-2.6; synth-02 rows 1, 2, 3, 8 | Covered |
| 06 Credential (sections 1-8, eight observations) | synth-01 sections 2.2, 2.4, 2.5, 2.6; synth-02 rows 3, 4, 6, 8 | Covered |
| Evidence deck (all section takeaways and overall takeaways) | synth-01 sections 2.1-2.7; synth-03 section 5.3 | Covered |
| scope-rules, gaps register, web-01 | synth-01 sections 2.3, 2.5, 2.6; synth-02 constraints; synth-03 sections 5.1-5.4 | Covered |

## Issues Requiring Fixes

| # | File | Check | Issue | Required Fix |
|---|------|-------|-------|-------------|
| 1 | synth-01 | 3, 4 (MINOR) | Section 1, line 11, names the investigated commands as `/sc:workflow` and `/sc:implement`. The line 15 evidence anchors (task file :64-75; evidence-deck :14-64) contain neither name; the task overview says only "planning and task-execution reviews". The real source, `BUILD-REQUEST.md:12`, is not cited. This is a reference match without semantic support. | Add `BUILD-REQUEST.md:12` to the section 1 evidence line. Alternatively, reword the question to match the cited task overview. |
| 2 | synth-01 | 4 (MINOR) | Section 2.2 credential row, line 67. The primary transition chain for the strict follow-up incident ("1215/1230 → 1938 → 1968 → nested second FINAL record 116 → repairs 2015 → pass/archive 2036") never anchors the first of its three FINAL results. That result is parent record 1932, `FINAL: issues`, 2026-10-22T20:20:36.570Z, recorded at evidence-deck.md:350, 390; I confirmed it read-only in the original JSONL. Its nested conclusion is `agent-a9c0c61dd415c2c4d.jsonl` record 135 (06:137-139). Every other incident row anchors each review result. | Insert the first-FINAL anchor (1932, or nested record 135) between 1215/1230 and 1938. |
| 3 | synth-01, synth-02 | 10 (IMPORTANT) | CI-case takeaways are dropped without an exclusion rationale. The orchestrator declared every review note applied (record 791) before the calibrator reported that the 18 prior findings were not individually checked (801). Reviewer 1's "16 fixed, 2 partial" and initial "ready with notes" were intermediate assessments that debate corrected. Sources: 04:102-104, 114-118 (section 4 Key takeaways), 04:240, 244 (section 8 mechanisms 3 and 5), evidence-deck.md:280. The synth-01 section 2.6 CI row (line 148) and the synth-02 Key Takeaway CI row (line 82) present CI coverage as complete. The analogous Orca "13 fixed, 3 partial" summary correction is retained, so the omission is asymmetric. It drops one of the case's five stated reasons review did not converge. | Represent these findings in synth-01 section 2.2 (CI row) and/or synth-02 gap row 7 with citations 04:102-104, 114-118, 240, 244 and deck:280, and list them in both coverage matrices. Otherwise, add an explicit exclusion with rationale to both matrices. |
| 4 | synth-02 | 4 (MINOR) | Gap row 1, line 50, cites only evidence-deck.md:585-598. That range supports the Orca coverage-credit and oracle label/count clauses. It does not support "CI presence checks admit semantically wrong edits" (support: deck:505; 04:405-435) or "Monitor structural checks do not cover the later behavioral counterexamples" (support: deck:312; 05:58-75). | Add deck:505 (or 04:405-435) and deck:312 (or 05:58-75) to the row's Notes. |
| 5 | synth-02 | 4 (MINOR) | Gap row 3, line 52, states that "Credential task QA softens a known literal lint condition before acceptance; FINAL applies the literal condition." The cited gaps-and-questions.md:29-35, 57-59 (Orca contradictions; evidence and policy confounding) and scope-rules.md:64-77 (rubric loads; monitor migration) do not substantiate the softening. Support exists at evidence-deck.md:350, 558, 596 and 06:156-175. | Add deck:558/596 or 06:156-175 to the row's citations. |
| 6 | synth-02 | 4 (MINOR) | Gap row 6, line 55, cites only evidence-deck.md:564-569. Deck:569 records the acceptance artifact without a ruling line, but not that the ledger "retains a compliant completion" (support: 06:381). The row's documentation wrong-task rejection clause also has no anchor (support: deck:244; 03:173-178). | Add 06:381 and deck:244 (or 03:173-178) to the row's Notes. |

## Summary
- Files passed: 1 (synth-03)
- Files failed: 2 (synth-01, synth-02)
- Total issues: 6 (1 important, 5 minor)
- Critical issues (block assembly): 0

## Self-Audit

Applies to the clean synth-03 verdict and to the checks that passed in the failed files.

- **Tools and reads:** I read all three targets in full; the Step 5.15 text (task file :321-323); the tech-research checklist (`/config/.claude/skills/tech-research/SKILL.md:1506-1529`); and the prepared stub. Inputs read in full: evidence deck (900 lines), case 05, case 06, gaps register, web-01, scope-rules. Inputs read at every cited range: case 01 :50-442, case 02 :68-315, case 03 :30-362, case 04 :60-609. Other reads: task file :60-77 and :250-261, `qa/qa-research-verification-structural.md:88-129`, all six cited current protocol sources at the cited lines.
- **Mechanical checks:**
  - Current checkout SHA-256 of the six protocol sources equals the original recorded hashes, and `git status` is clean for those paths.
  - Parent JSONL records 1916, 1932 and 1935 were inspected read-only for timestamp and `FINAL:` tokens.
  - Grep found no `[CODE-CONTRADICTED]`, `[STALE DOC]` or `[UNVERIFIED]` tags in the research inputs; `[CONTRADICTION` appears only in the gap register and synth-01.
  - Grep confirmed the CI premature-completion and intermediate-count terms are absent from synth-01..03.
  - Current synth-01..03 SHA-256 values (`fcbaedde…`, `f7fd5451…`, `4a352d1e…`) each appear in `qa/synthesis-component-intake.md`.
- **Why synth-03 is clean:**
  - Every factual sentence maps to an anchor I re-read.
  - The fifteen-question claim was counted row by row (deck 831-845) and mapped onto the nine section 5.1 rows.
  - The provider fields match web-01 :97-115 exactly, and the "no other external file" claim matches the directory listing.
  - The N/A decision is justified by task line 259, not asserted as a skipped phase.
- **Considered and not counted:**
  - The "parent persistence pending" headers and NEXT rows in synth-01..03 are the producers' original transport state. Current bytes are bound to recorded deliveries in `qa/synthesis-component-intake.md`, and task log :657 states the wording is the author's original stage. This is a delivery receipt elsewhere, not a false content claim.
  - synth-01 2.3 "fresh subagents" for per-task re-run reviews: qa.md:86 says "always subagents" and the ledger.md resume rows say "fresh". Treated as supported.
  - The 2.7 summary rows restate earlier-cited content, so their broad evidence line was not scored as an anchor defect.
- **No finding quota was applied.** Each of the six issues is a concrete statement-to-anchor or takeaway-coverage defect, cited to exact lines.

## Partition Limits and Evidence Boundaries

- [PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.] This partition covers synth-01, synth-02 and synth-03 only. Not reviewed here: synth-04..06, the five hypothesis cards, the adversarial artifacts and the immutable `reviews/adversarial/adversarial/variant-1..5-original.md` identities (Step 5.16).
- Case recommended actions (05:463; 06:347) and the CI renumbering proposal are recommendation-level content for sections 6-8. Their representation was not judged here beyond confirming that partition-1 files do not claim them as executed.
- Primary-source depth: claims were traced to the research layer (case files, deck, rule map, gap register, web-01) and their cited lines. Original JSONL logs were opened only for parent records 1916, 1932 and 1935. Historical plan and source bytes in the Coder and ci-followup worktrees, nested reviewer transcripts and `source.md` files were not re-read. The case analysts' primary-byte findings are therefore inherited, not re-verified.
- Out-of-scope observations, logged for follow-up and not scored (they are in research inputs, not assigned targets):
  - Case 06 never lists parent record 1932 (the first follow-up `FINAL: issues`). The deck's use of 1932 is correct per the JSONL check above.
  - Case 01:296-297 cites `Source:402` for two different requirements (named up-to-date state; self-check before any upstream call). I did not verify this against the Orca `source.md`.
- No target or other file was edited. No agents, tests, Git operations, staging, archive, move, deletion or external lookup were performed. This report is returned as text for parent persistence at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/analyst-synthesis-tracing-1.md`.