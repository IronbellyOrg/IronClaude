# QA Report - Synthesis Coherence, Partition 1

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only; returned as text for parent persistence because this reviewer is prohibited from writing report files)
**Phase:** synthesis-gate
**Lens:** synthesis-coherence
**Task item:** Step 5.21
**Partition:** 1 of 2
**Fix cycle:** N/A
**Fix authorization:** false
**Governing template:** Project rf-qa-qualitative Output Format (All Phases); tech-research qualitative review template

---

## Overall Verdict: FAIL

## Criteria and Partition Scope
**Assigned files:** `synthesis/synth-01-problem-current-state.md` (report sections 1-2), `synthesis/synth-02-target-gaps.md` (sections 3-4) and `synthesis/synth-03-external-findings.md` (section 5).

**Criteria applied.** These come from Step 5.21's Action and Verify clauses, the synthesis-coherence lens in `/config/.claude/skills/tech-research/SKILL.md:507`, and the legacy 12-item qualitative checklist at `SKILL.md:995-1040`, adapted to synthesis components:
- whether the question matches the findings
- whether the explanation holds together end to end
- whether alternative mechanisms are kept
- whether conclusions are proportionate to evidence strength
- whether the six causal classes are applied faithfully
- whether limits are stated honestly
- whether current and historical evidence stay separate
- whether the external N/A decision is backed by sources
- whether contradictions are resolved by evidence or marked with both sources
- whether raw review statuses and separate count units stay intact
- whether the three files agree with each other
- whether counterevidence is kept
- whether the research-only scope is respected

**Primary sources checked against:**
- `research/evidence-deck.md` (all 900 lines)
- `gaps-and-questions.md` (complete)
- `research/scope-rules.md` (complete)
- `research/web-01-gap-applicability.md` (complete)
- `research/06-session-0690ee9f.md` (complete)
- targeted ranges of cases 01, 02, 03 and 05
- current checkout protocol sources: `qa.md` (complete), `retry.md:136-150`, `ledger.md:134-160`, `managed-workspace.md:38-86`, `sc-workflow-protocol/SKILL.md:46-73` and `quality-gates.md:22-42`
- the task file at lines 64-75, 250-276 and 300-379
- `qa/qa-research-verification-structural.md:88-128`

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Question matches findings | PASS | synth-01:11 asks the six-way disposition question, and the case table at synth-01:60-67 answers it per incident with classification and endpoint. The task overview at TASK:64-75 matches the cited range. |
| 2 | End-to-end explanation and traceable chains | FAIL | Five case chains map failure, then repair, then next review to deck chronologies (deck:176-184, 208-216, 236-245, 275-284, 310-322). The credential chain at synth-01:67 leaves out the first failed follow-up FINAL. See Issue 1. |
| 3 | Alternative mechanisms kept | PASS | synth-01:110-120 separates what each kind of evidence establishes from what it does not. synth-02:67 keeps overlapping mechanisms, including exposure versus creation. Both match deck:594 and deck:657. |
| 4 | Conclusions proportionate to evidence | FAIL | Case-level strength wording matches the deck's Strong and Bounded labels (deck:374-391). The Gap Analysis severity column at synth-02:50-61 rates every gap the same and labels evidence limits inconsistently. See Issue 2. |
| 5 | Six causal classes applied faithfully | PASS | The six classes appear in synth-01:11 and synth-02:20, matching deck:36-45 and deck:413-422. Every class has a case example in synth-01:62-67 (introduced, missed, unresolved, changed criteria, invalid, unknown). "Before/after evidence required" is kept at synth-01:115 and synth-02:20. |
| 6 | Honest limits | PASS | Unknown miss reasons, the rubric updater, confounding, unobserved runtime and non-prevalence are stated at synth-01:52, 104, 168, synth-02:24 and 60-61, and synth-03:19-27. These match gaps:56-59 and deck:831-845. |
| 7 | Current and historical evidence kept separate | PASS | synth-01:75 labels instruction sources as checkout text, not historical loads. I re-read all six cited protocol ranges and they support each row (for example retry.md:144 "Worst case: 5 reviews instead of 2"; ledger.md:142 single writer; managed-workspace.md:85 digest exclusions). The aged seven-pair equality is dated and excluded from ranking evidence (synth-01:132, matching qa-research-verification-structural.md:97-127). |
| 8 | External N/A backed by sources, with correct case attribution | FAIL | The N/A rationale, the provider record (Tavily, Context7, WebSearch and WebFetch not invoked) and the coverage of 15+3 questions all match web-01:20, 28-49 and 99-113. TASK:257-259 permits a reasoned N/A. One applicability row attributes runner-behavior unknowns to the wrong case. See Issue 3. |
| 9 | Contradictions resolved by evidence or marked with both sources | PASS | synth-01:128-130 resolves the 13/3 versus 14/2 count from the detailed checklist (01-session:90-103) and marks the two Orca source contradictions with `[CONTRADICTION: ...]`, citing both the case and the gap register (gaps:33-35). No unmarked contradiction was found between the three files. |
| 10 | Raw review statuses and separate count units intact | PASS | synth-01:23-31 and 39-44 keep separate units for sessions, incidents, reviews, findings and transitions, plus the strict subset, matching deck:22-32 and 51-56. Raw `partial`, `PARTIAL`, `not_ready`, `cannot-verify` and `misunderstood` are preserved. Monitor's 7 verdicts, 5 reviewers and 5 repairs match deck:326 and 551. Overlapping finding inventories (CI 18/16/8) are not added together. |
| 11 | The three files agree with each other | PASS | Strict-subset membership, the 14/2 Orca accounting, seven synthetic exclusions, dated protocol drift and the external N/A are stated the same way in all three (synth-01:41, synth-02:18 and 21, synth-02:36, synth-03:11). |
| 12 | Counterevidence and successful controls kept | PASS | synth-01:69 and synth-02:69 keep the oracle repairs 1-3, monitor Tasks 10/11, the initial credential control and sessions 09/10/17/19. Each matches deck:647-655, including session 17's real restore-basename bug (deck:652). |
| 13 | Research-only scope respected | PASS | No ranking, probability, implementation task or authorization appears (synth-01:169, synth-02:25 and 33, synth-03:83, matching web-01:133). |

## Summary
- Checks passed: 10 / 13
- Checks failed: 3
- Critical issues: 0
- Issues fixed in-place: 0 (report-only, fix_authorization: false)
- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The verdict is FAIL because issues exist, not because of low confidence.
- **Tool engagement:** Read: 23 | Grep: 0 (dedicated tool; content searches ran through Bash grep) | Glob: 0 | Bash: 8. Read + Grep + Glob = 23, which is at least the 13 checklist items.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | synth-01:67, credential row, "Primary transitions" and its evidence ranges | The follow-up chain reads "1215/1230 → 1938 → 1968 → nested second FINAL record 116 → repairs 2015 → pass/archive 2036". It goes straight from the task-QA criterion softening (1215/1230) to the user's "accept and fix" (1938). It leaves out the first failed follow-up FINAL: dispatched at parent 1916, concluded at nested `agent-a9c0c61dd415c2c4d.jsonl` record 135 (06-session:133-139), and given as parent 1932 in deck:350. The cited ranges (06-session:11-32, 64-129, 141-266, ...) also skip 06-session:131-140, where that review is anchored. Only 2 of the incident's 3 review results (deck:156) can be traced from the row. That breaks end-to-end traceability for one of the three strict incidents. | Insert the first FINAL into the chain, for example "1215/1230 → first FINAL issues (dispatch 1916, nested record 135; parent 1932 per deck) → 1938 → 1968 → nested 116 → 2015 → 2036". Extend the evidence range to include 06-session:131-140. |
| 2 | MINOR | synth-02:50-61, Gap Analysis Severity column | All 12 rows are rated "Important", with no discrimination. A single-case guard-label misreading risk (row 58, `head-moved`) gets the same rating as the multi-case repair-interaction mechanism (row 51). The labels also contradict the table's own stated split between defects and inference limits (synth-02:46). Rows 60 and 61 are "Important evidence limit", but row 59 ("Live sources can be mistaken...") is plain "Important", even though its Notes call it a "Research-accounting boundary... not... product defect", which is the same kind of row as 60-61. The template severity scale is Critical/Important/Minor (SKILL.md:842 and 886). | Rate each gap proportionately on the template scale, based on its demonstrated effect. Mark defect versus inference-limit type consistently (in the Notes column or as a label suffix applied to every limit row), so rows 59-61 use the same convention. |
| 3 | MINOR | synth-03:22, section 5.1 row "CI planning weaknesses and live runner behavior" | The row bundles unverified runner "permissions, cancellation or timeout behavior" with the CI planning case. The CI case contains no cancellation, permission or timeout claim (zero matches in 04-session-43582de1.md). These unknowns come from the Orca monitor case (05-session:292-293, "Real GitHub permissions, dispatch expression behavior, runner cancellation behavior... remain unverified"; deck:540, timeout claim not proved on runner). The deck's question at deck:836 is case-neutral. A reader would credit the runner-behavior gap to the wrong incident. | Split the row, or reword it: keep the CI implementation-failure unknown under CI, and attribute the runner permission, cancellation and timeout unknowns to the monitor workflow (citing 05-session:292-293). |

## Actions Taken
None. Report-only review. I made no edits to synthesis files, research files, the stub at `qa/qa-synthesis-qualitative-report-1.md`, the task file or any other file. I spawned no agents and took no test, Git, staging, archive, move, delete or publication action.

## Inherited Structural Verdict - Reliance Audit
No `## Inherited Structural Verdict` block was supplied in the spawn prompt. This reviewer worked standalone and relied on no rf-qa PASS items. The parallel Step 5.17 and 5.19 structure and content reports were not consulted, to keep the review independent.

## Self-Audit
**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was available. Structural items (headings, table schema) were not re-litigated beyond what affects coherence, such as the severity-scale labels in Issue 2.

**(b) Independent semantic checks:**
- Credential review count against the case file: read 06-session:1-388. The first FINAL anchor is at :133-139, the trace supplement at :353-361 lacks a first-FINAL row, and synth-01:67 omits it (Issue 1).
- Runner-behavior attribution: grep counted 0 cancel/permission/timeout matches in 04-session and 3 in 05-session (:154, :292, :293), against synth-03:22 (Issue 3).
- Gap severity labels: read synth-02:44-61 rows 50-61 against SKILL.md:842 and 886 (Issue 2).
- Protocol-row semantics: read qa.md:9-11, 31, 82, 86; retry.md:144-146; ledger.md:142-158; managed-workspace.md:42-85; workflow SKILL.md:56-58; quality-gates.md:24-41. Each synth-01:79-84 claim is supported.
- Protocol-drift dating: qa-research-verification-structural.md:97-127 (17:27:55.147Z seven equal; 18:22:14.768885Z three equal, four different) matches synth-01:132 and gaps:56.
- External N/A completeness: web-01 rows 32-49 (18 rows = 15 deck questions + 3 extra) map one-to-one into synth-03's 9 grouped rows. Provider record web-01:99-113 matches synth-03:35-43.

**Independent factual claims and source files:**
About 60 claims checked. Examples:
- Oracle 67/78 tests and the 291→383→398→450→521→573→668 chain (deck:208-216; 02-session:222-232).
- Monitor 7 verdicts, 5 reviewer identities, 5 repairs and the acceptance at 1250/1261 (deck:310-326, 551; 05-session:223-236, 273-287).
- CI 18 concerns, 5 medium, 11 low, 0 high, partial evidence (deck:277-284).
- Orca 14/2 and the 20-item composition (01-session:90-103).
- `head-moved` from a missing checkpoint (03-session:158-171).
- Control sessions 09/10/17/19 (deck:82-92, 647-655).
- Seven synthetic exclusions (deck:94-103).
- Task Step 4.1 at TASK:257-259.

Files read: the three targets; evidence-deck.md (complete); gaps-and-questions.md; scope-rules.md; web-01-gap-applicability.md; 06-session-0690ee9f.md; ranges of 01, 02, 03 and 05; the six protocol sources; the task file ranges; the QA structural verification range; SKILL.md:495-520 and 990-1080.

**Clean-result justification and external-tool provenance:**
The verdict is not clean (3 issues), so no clean-result justification is needed. No web research was needed or performed; Tavily, WebSearch and WebFetch were not invoked.

Non-defect check: synth-01, 02 and 03 still say "parent persistence pending" in their headers and closing tables, and they carry no in-file Parent Persistence Record, unlike the deck, web-01 and the hypothesis cards. The task log records their exact-text persistence and attribution externally (TASK:651, 655, 657, which say the author's original handoff wording is preserved deliberately). So I did not count this as a defect. I did not open `qa/synthesis-component-intake.md` myself.

## Partition Limits and Evidence Uncertainty
[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

- synth-04, 05 and 06, the five hypothesis cards and the debate artifacts were not reviewed. Consistency between this partition's sections 1-5 and the ranking, plan and evidence sections is unchecked.
- Case files 01, 02, 03 and 05 were checked only at cited or targeted ranges. Case 06 was read in full. Primary JSONL logs were not re-opened; claims were checked against the persisted case reports and the deck.
- Deep line-by-line citation tracing for every anchor belongs to the Step 5.13 and 5.15 lenses. Only a sample of synth-01 research citations was spot-checked here (7 ranges, all supportive).
- The first-FINAL parent record number differs between sources: the deck says 1932, while case 06 anchors the dispatch at 1916 and the nested record at 135. Issue 1's fix should use whichever anchor the fixer verifies in the primary log.

## Recommendations
- Route Issues 1-3 to the Step 5.23 consolidation and the single serialized Step 5.24 fixer. All three are confined to synth-01:67, synth-02:50-61 and synth-03:22, and none of them changes a causal class or hypothesis identity.
- After the fixes, the Step 5.26 content verifier should check that the corrected credential chain shows all three review results and that the severity labels are applied consistently.

## QA Complete
Verdict FAIL. 13 checks: 10 passed, 3 failed. Issues: CRITICAL 0, IMPORTANT 0, MINOR 3. Report returned as text for exact parent persistence at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-qualitative-report-1.md`.

---

| Status | Result |
|---|---|
| DONE | Reviewed synth-01, 02 and 03 for coherence against the primary sources. Verdict FAIL, 3 MINOR issues. No files edited. |
| NEXT | The parent writes this exact report to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-qualitative-report-1.md`, then includes it in the Step 5.23 consolidation. |