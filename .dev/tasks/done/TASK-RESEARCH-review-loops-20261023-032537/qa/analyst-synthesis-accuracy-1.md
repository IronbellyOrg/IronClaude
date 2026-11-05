# Synthesis Quality Review - Accuracy, Partition 1

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only review; returned as text for parent persistence because this reviewer may not write report files)
**Files reviewed:** 3 (`synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`)
**Lens:** synthesis-accuracy
**Task item:** Step 5.13
**Partition:** 1 of 2
**Governing template:** Project rf-analyst Synthesis Quality Review Output Format; tech-research synthesis checklist

## Overall Verdict: FAIL (9 issues: 0 critical, 4 important, 5 minor)

## Per-File Review

### synth-01-problem-current-state.md
**Sections covered:** 1 and 2
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | FAIL | `## 1. Problem Statement` and `## 2. Current State Analysis` match, and so does the 2.1-2.6 plus final 2.7 Current State Summary pattern (`/config/.claude/skills/tech-research/SKILL.md:1330-1352`). But lines 173-176 add a DONE/NEXT status table inside 2.7. It is not report content, and its NEXT row ("Parent persistence at the intended existing destination...") no longer matches disk: the file is persisted and has no Parent Persistence Record (grep count 0). On assembly this table would be pasted into the report's Section 2. |
| 2 | Table column structure correct | PASS | Section 2 has no fixed column schema in the template. Each table has consistent columns and a cited evidence column or evidence line. |
| 3 | No fabricated content | PASS | Spot-traced claims all matched their sources. Population, time and glob (`research/session-manifest.txt:1`). Seven synthetic exclusions plus index 03 (`research/evidence-deck.md:76,94-103`). Orca counts 16/14+2/20, Writes 544/841, targeted 874, 15 edits to v4 (`evidence-deck.md:178-188,466-482`; `research/01-session-ac2cd1fd.md:90-103`). Oracle 67/78 tests and record chain (`evidence-deck.md:210-216,495`). Task 6 and Task 2 chains (`evidence-deck.md:240-256`). CI 18 concerns and 5 medium/11 low/0 high (`evidence-deck.md:277-284`). Monitor 640 lines, 7 verdicts, 5 repairs, 4 literal `fix` replies, 5 reviewer identities (`research/05-session-e002bed2.md:20-24`; `evidence-deck.md:326,551`). Credential eight observations and the T6 compliant line without a ruling (`research/06-session-0690ee9f.md:367-386`). Every Section 2.3 protocol row was re-read in the source: `sc-workflow-protocol/SKILL.md:56-58`, `refs/quality-gates.md:24-41`, `refs/qa.md:9-11,62-68,82,86`, `refs/retry.md:144-146`, `refs/ledger.md:142-158`, `refs/managed-workspace.md:42,48-68,78-85`. |
| 4 | Evidence citations | FAIL | (a) Line 67's credential "Primary transitions" chain leaves out the first failed follow-up FINAL. It runs from task-QA records 1215/1230 straight to acceptance 1938. The first `FINAL: issues` result (parent 1932; nested `agent-a9c0c61dd415c2c4d.jsonl` record 135, per `evidence-deck.md:350` and `06-session-0690ee9f.md:137-139`) has no anchor, although every other row anchors each review result. (b) Line 11 names `/sc:workflow` and `/sc:implement`, but the cited source (task file lines 64-75) names neither. The original question is `BUILD-REQUEST.md:12`, which is not cited, and the template asks for the original question (`SKILL.md:1332`). (c) The line 52 paragraph (family clustering, selection by modification time, no prevalence estimate) has no citation, although support exists at `evidence-deck.md:105,662`. |
| 5 | Options include 2+ options with pros/cons | N/A | Options (Section 6) are in synth-04, which belongs to partition 2. |
| 10 | Key finding coverage | PASS | Section 2.6 maps all nine inputs and gives explicit exclusion reasons. The summary findings of cases 01-06 (case Summary sections; `06-session-0690ee9f.md:343-347`) and the Key Takeaways at `evidence-deck.md:814-823` appear in 2.2-2.7. Case recommendations (for example the 06 durable-evidence advice and the 05 regression-matrix advice) belong to Sections 6-8, which are in partition 2. |

### synth-02-target-gaps.md
**Sections covered:** 3 and 4
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | FAIL | `## 3. Target State` and `## 4. Gap Analysis` match. Lines 91-94 add the same kind of DONE/NEXT table at the end of Section 4. Its claim "No files were written" and its NEXT row "Parent persists this component" are stale against disk, and the file has no Parent Persistence Record (grep count 0). |
| 2 | Table column structure correct | FAIL | The gap table header exactly matches `Gap \| Current State \| Target State \| Severity \| Notes` (`SKILL.md:1370-1372`). But the Severity cells at lines 60-61 read "Important evidence limit", which is outside the template's `Critical/Important/Minor` set. |
| 3 | No fabricated content | PASS | Traced. 14 accepted plus 2 partial amendments (`evidence-deck.md:466-482`). Introduced Orca and CI defects (`:430-433,501-503`). T6 lint softening (`06-session-0690ee9f.md:156-175`). T10 authority overreach (`:218-222`). T6 `complete verdict=compliant` with no Ruling (`:381`). `head-moved` guard (`evidence-deck.md:243,729`). Seven-versus-three/four protocol comparison (`gaps-and-questions.md:56`; `qa/qa-research-verification-structural.md:93-127`). The unwired-capability (C8) disclaimer at line 65 is accurate: no source finding concerns an unwired shipped capability. |
| 4 | Evidence citations | PASS | Every gap row carries a deck, gap-register or web-01 line citation. Sampled ranges contain the stated facts, for example `evidence-deck.md:585-598`, `:564-569`, `:724-729` and `web-01-gap-applicability.md:30-56`. |
| 5 | Options include 2+ options with pros/cons | N/A | Options (Section 6) are in synth-04, partition 2. |
| 10 | Key finding coverage | PASS | The coverage table (lines 77-87) covers all six cases, the deck, the rule map, the external assessment and the gap register, with stated exclusions. Deck controls (`evidence-deck.md:643-668`) are preserved at lines 21 and 69. |

### synth-03-external-findings.md
**Sections covered:** 5
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | FAIL | `## 5. External Research Findings` plus 5.1-5.3 and `### 5.4 External Research Summary` fit the template (`SKILL.md:1378-1389`). But line 73 adds a separate top-level `## Evidence and Limits` heading. The template has no such heading, and on assembly it would become an unnumbered section between Sections 5 and 6. Lines 85-88 also add a DONE/NEXT table whose NEXT row says persistence is pending, and line 5 says "This worker did not modify the existing output file". Both are stale against the persisted file, which has no Parent Persistence Record. |
| 2 | Table column structure correct | PASS | No external findings exist, so the template's Finding/Source/Relevance/Relationship fields are recorded as reasoned N/A (lines 41-42). |
| 3 | No fabricated content | PASS | The N/A decision and provider record match `web-01-gap-applicability.md:14-22,97-115`. The 9-row table in 5.1 covers all 18 rows of the web-01 inventory (`:30-49`), including all 15 deck questions (`evidence-deck.md:831-845`). Only one `web-*` file exists in `research/`. The Step 4.1 N/A permission and the "tier quota" wording match the task file line 259. |
| 4 | Evidence citations | FAIL | Line 83 cites `web-01-gap-applicability.md:127-150` for "does not authorize ... external publication". Those lines cover protocol repair, implementation tasks, proposed checks and production actions, but not external publication. That limit actually comes from the task file's Task Overview (`TASK-RESEARCH-review-loops-20261023-032537.md:69`). |
| 5 | Options include 2+ options with pros/cons | N/A | Not applicable to Section 5. |
| 10 | Key finding coverage | PASS | The web-01 Key Takeaways (`:53-56,91-93`) and the deck conclusions (`evidence-deck.md:814-823`) are in 5.3-5.4. The justified external N/A is explicit and is not presented as a skipped phase or a provider failure. |

## Issues Requiring Fixes
| # | File | Check | Issue | Required Fix |
|---|------|-------|-------|-------------|
| 1 | synth-01 | 1 | IMPORTANT: Lines 173-176, a DONE/NEXT status table inside 2.7, is non-report content with a stale persistence claim. | Remove it from the component, or move the delivery provenance into a clearly non-assembled receipt. Do not let the assembler copy it into Section 2. |
| 2 | synth-02 | 1 | IMPORTANT: Lines 91-94, a DONE/NEXT table at the end of Section 4, says "No files were written" while the file exists, with no persistence receipt. | Same fix as issue 1. |
| 3 | synth-03 | 1 | IMPORTANT: Lines 85-88, a DONE/NEXT table, and the line 5 delivery note are stale against the persisted file. | Same fix as issue 1. Update or relocate the delivery note. |
| 4 | synth-03 | 1 | IMPORTANT: Line 73, a separate top-level `## Evidence and Limits` heading, is outside the template. | Fold it into 5.4 or make it a 5.x subsection, so Section 5 contains no extra top-level heading. |
| 5 | synth-02 | 2 | MINOR: Lines 60-61 use the Severity value "Important evidence limit". | Use `Important` and move "evidence limit" into the Notes column. |
| 6 | synth-01 | 4 | MINOR: The line 67 credential transition chain leaves out the first failed follow-up FINAL. | Insert "→ first FINAL issues, parent 1932 (nested `agent-a9c0c61dd415c2c4d.jsonl` record 135)" between 1215/1230 and 1938. |
| 7 | synth-01 | 4 | MINOR: The line 11 question names the commands, but the cited task lines 64-75 do not name them. | Cite `BUILD-REQUEST.md:12` (the original GOAL), or quote it as the original question. |
| 8 | synth-01 | 4 | MINOR: The line 52 paragraph about clustering and modification-time selection has no citation. | Add `Evidence:` `evidence-deck.md:105,662`. |
| 9 | synth-03 | 4 | MINOR: Line 83's "external publication" limit is attributed to web-01 lines 127-150, which do not contain it. | Add the task file line 69 as the source, or drop "external publication" from the attributed sentence. |

## Summary
- Files passed: 0
- Files failed: 3
- Total issues: 9
- Critical issues (block assembly): 0. Issues 1-4 would put non-report text or an unnumbered heading into the assembled report, so fix them before assembly.

## Self-Audit
I assumed the compression was inaccurate and checked, using tools:
- I fully read the governing template sections: Report Structure, Synthesis Agent Prompt, Synthesis Mapping Table, and the 10-item checklist (`SKILL.md:779-812,1311-1400,1491-1528`).
- I fully read all three target files.
- I fully read the evidence deck (lines 1-900), `scope-rules.md`, `gaps-and-questions.md` and `web-01-gap-applicability.md`.
- I read the cited ranges of all six protocol sources directly.
- I read case 06 at lines 60-386, plus targeted ranges of cases 01 (90-103), 03 (337-362), 04 (66-87), 05 (12-30, 52-76, 223-236, 270-290), the Summary sections of cases 01-05, and grep hits in case 02.
- I checked `qa-research-verification-structural.md:90-128`, the manifest header, `BUILD-REQUEST.md:10-14`, and task file lines 62-76, 253-259 and 313-315.
- I extracted every absolute citation in the three files by grep and confirmed that each cited line range lies inside its file.
- I checked for a persistence receipt with grep.
- Wording I examined and accepted: synth-01 Section 2.3 says operator and escalated reviews use "fresh subagents". `qa.md:86` says "subagents", and the "fresh" part comes from ledger rows P/H/V; I found no contradiction. The 2.6 and Section 4 coverage tables placed inside report sections are a permitted way to meet synthesis rule 11.

## Partition Limits and Evidence Boundaries
[PARTITION NOTE: Cross-file checks are limited to synth-01..03. A full cross-file analysis needs the partition 2 report merged in.]
- I did not review synth-04..06 or the hypothesis cards. So I did not assess checks 5-9, including whether Section 4 gaps are addressed in Section 8 and whether stale-documentation items reach Section 9 (synth-06).
- Verification traced claims to the research layer (case reports, the deck and the rule map) and directly to the protocol sources. I opened no raw session JSONL logs, historical Git objects or package artifacts, so primary-record accuracy rests on the research files.
- I did not read every line of cases 01-05; only the ranges listed in the Self-Audit.
- I edited no file, spawned no agent, ran no tests, and used no Git, web lookup or staging.
