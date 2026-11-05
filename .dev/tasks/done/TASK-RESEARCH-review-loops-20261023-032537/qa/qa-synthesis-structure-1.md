# QA Report - Synthesis Structure, Partition 1

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete
**Phase:** synthesis-gate
**Lens:** structure
**Task item:** Step 5.17
**Partition:** 1 of 2
**Fix cycle:** N/A
**Fix authorization:** false
**Governing template:** Project rf-qa Output Format (All Phases); tech-research Synthesis QA Agent Prompt

---

## Overall Verdict: FAIL

## Criteria and Partition Scope

**Assigned files:**
- `synthesis/synth-01-problem-current-state.md` (175 lines, SHA-256 `fcbaedde…6c93`). It supplies report sections 1 and 2.
- `synthesis/synth-02-target-gaps.md` (93 lines, `f7fd5451…005b`). It supplies sections 3 and 4.
- `synthesis/synth-03-external-findings.md` (87 lines, `4a352d1e…db83a`). It supplies section 5.

All three hashes match the latest rows in `qa/synthesis-component-intake.md`, so the files reviewed here are the recorded persisted components.

**Criteria applied:** The first six items of the Synthesis QA Agent Prompt (`/config/.claude/skills/tech-research/SKILL.md:925-931`), plus the Step 5.17 check that every assigned section is populated or justified N/A. Each check was measured against the Report Structure (`SKILL.md:1311-1487`), the Synthesis Agent Prompt rules (`SKILL.md:789-800`) and the producing Steps 5.1-5.3 (task file lines 263-276).

**Mapping to this partition:**
- Checks 5 (options) and 6 (implementation plan) are tested only as routing. They pass if these files contain no options or plan content made up here, because sections 6-8 belong to partition 2.
- Checks 7-12 belong to Step 5.19 and are not applied, except where a structural defect overlaps them.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers and template fields match the Report Structure | FAIL | Listed every H1-H3 heading with grep. Headings `## 1.`, `## 2.`, `### 2.1-2.7` (2.7 is the "Current State Summary"), `## 3.`, `## 4.`, `## 5.`, `### 5.1-5.4` (5.4 is the "External Research Summary") all conform. Two defects: synth-03:73 adds an unnumbered H2 `## Evidence and Limits` (issue 1), and synth-01:13 renames and repurposes the template's Trigger field (issue 10). |
| 2 | Table column structures | FAIL | The Gap Analysis table header at synth-02:48 is exactly Gap / Current State / Target State / Severity / Notes. But the Severity cells at synth-02:60-61 say "Important evidence limit", which is not one of the allowed values Critical/Important/Minor (`SKILL.md:1372`) (issue 3). The other tables are freeform and are not governed by a template schema. |
| 3 | No fabrication (semantic trace to research) | PASS (traced sample; see Limits) | About 60 discrete facts were traced to research text, with no invented fact found. Examples: the population time 03:25:59Z (manifest:1); seven synthetic exclusions (deck:94-103); Orca's 16 findings, 14 accepted / 2 partial, 15 edits, same source hash and records 499-946 (01:68-86, 90-103, 340); oracle 67/78 tests, four defects and records 291-668 (02:84-99, 228); documentation records 430/433-434/443/450/506/527 and 188/204/217/234 (03:59-62, 177-180, 199-204); CI's 18 concerns, 5 medium/11 low/0 high and records 623/627/1003/1084 (04:97-99, 283, 319-327); monitor's 640 lines, four `fix` replies, five reviewers and seven verdicts (05:20, 56, 84-103, 491-501); credential records 390/435/1215/1230/1938/1968/2015/2028/2036 (06:75-80, 160-222, 260); protocol timestamps (qa-research-verification-structural:101, 106); fifteen deck questions (deck:831-845); provider record (web-01:97-115). Where a cited anchor fails to support its claim, that is logged under check 4. |
| 4 | Evidence citations use real paths that actually support each claim | FAIL | All 21 distinct cited paths exist and every cited line range is within the file's length (batch `test -e` plus `wc -l`). The protocol-source rows at synth-01:79-84 were re-read and are supported (`qa.md:9-17,80-90`; `managed-workspace.md:42-68,78-85`; `sc-workflow-protocol/SKILL.md:56-58`; `quality-gates.md:24-41`; `retry.md:144-146`; `ledger.md:142-158`). However, six claims cite anchors that do not contain them, or are uncited or unanchored (issues 4-9). |
| 5 | Options content correctly routed (none invented in this partition) | PASS | synth-01:6,169, synth-02:7,25,67 and synth-03:83 explicitly withhold ranking and options. No Option/Comparison table or recommendation appears in any of the three files (heading list plus a full read). |
| 6 | Implementation plan content correctly routed | PASS | No Step/Action/Files/Details table or implementation step appears. synth-02:33 and synth-03:83 keep follow-ups unexecuted and outside these sections. synth-02:65 explicitly declines to authorize a remediation task. |
| 7 | Every assigned section populated or justified N/A; no placeholder accepted as content | FAIL | Sections 1-5 are populated. Section 5's N/A is reasoned and matches web-01:14-22 and 97-115. The research directory holds only one `web-*.md` file. A grep for `RF_PLACEHOLDER`/TODO/TBD/FIXME/template brackets found nothing. But all three components end with producer transport tables whose NEXT rows say persistence is still pending, and those tables sit inside the section bodies (issue 2). |

## Summary

- Checks passed: 3 / 7
- Checks failed: 4
- Critical issues: 0 (Important: 1, Minor: 9; 10 issues total)
- Issues fixed in-place: 0 (`fix_authorization: false`)
- **Confidence:** Verified: 6/7 | Unverifiable: 0 | Unchecked: 0 | Partially verified: 1 (check 3: traced sample, not every subclause) | Confidence: 85.7%. That is below the 95% needed for PASS; the verdict is FAIL on its own findings in any case.
- **Tool engagement:** Read: 22 | Grep: 0 (dedicated tool) | Glob: 0 | Bash: 19 (read-only grep, sed, sha256sum, wc, test). No web research was performed: tavily_search 0, tavily_extract 0, web_search_fallback 0, web_fetch_fallback 0.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | synth-03:73-83 | `## Evidence and Limits` is an unnumbered H2 inside the section 5 component. The Report Structure allows only `### 5.1…5.N` subsections under `## 5.` (`SKILL.md:1378-1389`). Assembled as written, the report would gain a stray top-level section between 5 and 6, which breaks the numbered structure and the table of contents. | Demote it to `### 5.5 Evidence and Limits`, or merge its source table and the paragraphs at :81-83 into 5.4. Alternatively, move the source-role table to the Evidence Trail (section 10, partition 2). |
| 2 | MINOR | synth-01:173-176 (and Status at :4, destination at :7); synth-02:91-94 (and :5, :8); synth-03:85-88 (and :4-6) | Each component ends with a DONE/NEXT transport table that is not part of the Report Structure, sitting inside the section 2, 4 and 5 bodies. Each NEXT row says persistence or QA is still pending, e.g. synth-03:88 "Parent persists the component…". Persistence is actually recorded externally, in `qa/synthesis-component-intake.md` (current hashes) and the task log at lines 655-657. Unlike `evidence-deck.md:898-900`, `web-01-gap-applicability.md:180-182` and `synth-04-options-recommendation.md:339`, none of these files carries a receipt resolving its NEXT row. A mechanical assembly would carry stale process text into the report. | Remove the DONE/NEXT tables and the stale persistence-pending status lines from the assemblable body. Or append a clearly labelled non-assemblable Parent Persistence Record that resolves each NEXT row, and mark the trailing tables for exclusion at assembly. |
| 3 | MINOR | synth-02:60, synth-02:61 | The Severity column uses "Important evidence limit". Allowed values are Critical/Important/Minor (`SKILL.md:1372`). | Set Severity to `Important` and move the "evidence limit" qualifier into the Notes cell. |
| 4 | MINOR | synth-02:50 (gap row 1) | The claim that "CI presence checks admit semantically wrong edits" is cited only to `evidence-deck.md:585-598`. That range covers Orca, oracle, documentation, CI search/exemption, monitor and credential mechanisms, but not CI presence checks admitting wrong edits. The support is at `evidence-deck.md:505` ("Half-edited advisory meaning passes"). | Add `evidence-deck.md:505` (or `:505,514`) to the row's Notes citation. |
| 5 | MINOR | synth-02:52 (gap row 3) | The claim that "Credential task QA softens a known literal lint condition before acceptance; FINAL applies the literal condition" is cited to `gaps-and-questions.md:29-35,57-59` and `scope-rules.md:64-77`. Neither range states the softening or that FINAL applied the literal rule. The support is at `evidence-deck.md:558,596` and `06-session-0690ee9f.md:160-175`. | Add `evidence-deck.md:558` and `06-session-0690ee9f.md:160-175` to the row citation. |
| 6 | MINOR | synth-02:55 (gap row 6) | The claim that the ledger "retains a compliant completion" is cited to `evidence-deck.md:564-569`, which records the missing ruling line but not the compliant completion. The support is at `06-session-0690ee9f.md:381` (`T6: complete verdict=compliant`, no `T6: Ruling:`). | Add `06-session-0690ee9f.md:381` to the citation. |
| 7 | MINOR | synth-01:11 and :15 | "The question" names `/sc:workflow` and `/sc:implement`, but its Evidence line cites only task file :64-75 and deck :14-64. Neither names those commands (a grep of the task file finds no `sc:workflow` or `sc:implement`). The original wording is at `BUILD-REQUEST.md:12`. | Add `BUILD-REQUEST.md:12-14` to the section 1 Evidence line. |
| 8 | MINOR | synth-01:52 | This paragraph states that the sample clusters in a few work families, was selected by modification time and is not a prevalence estimate, with no citation. The nearest Evidence line (:50) cites only the case 05 and 04 observation windows. The support is at `evidence-deck.md:105,662`. | Add `**Evidence:** evidence-deck.md:105,662` after :52. |
| 9 | MINOR | synth-01:67 (credential "Primary transitions") | The strict fail-fix-fail-fix-pass chain anchors the second FINAL (nested record 116) and the pass (2036) but omits the first follow-up `FINAL: issues`. That review was dispatched at parent 1916, concluded at nested `agent-a9c0c61dd415c2c4d.jsonl` record 135 (`06-session-0690ee9f.md:133-137`), and is shown as parent 1932 at `evidence-deck.md:350,390`. As written, the chain runs from task QA 1215/1230 straight to acceptance 1938. | Insert the first-FINAL anchor (`first FINAL issues 1916/nested 135, parent 1932`) between 1230 and 1938. |
| 10 | MINOR | synth-01:13 | The template field `**Trigger:** [what prompted this research]` (`SKILL.md:1336`) is renamed "Trigger and deliverable" and filled with method and deliverable text. The actual trigger, the user's report that fixes lead to more failures and their request for causal analysis (`BUILD-REQUEST.md:14`), does not appear in section 1. | Restore the `**Trigger:**` label, state the user-reported trigger with that citation, and keep the method/deliverable sentence separately (for example under "Why it matters", or as a following line). |

## Actions Taken

None. This was a report-only review (`fix_authorization: false`). No synthesis, research, task or QA file was edited. No agents, tests, Git, staging, archive, move, delete or external lookups were used.

## Self-Audit

This is not a zero-issue result. The checks behind the passed items, and behind the claims judged sound, were:

- **Fabrication (check 3):** facts were re-read in primary research text, not only matched by citation ID. Examples: the Orca 14/2 correction at 01:90-103, the documentation `head-moved` category at 03:158-171, the monitor migration at 05:223-236, the ledger omissions at 05:273-287, the Orca contradictions at 01:217 and :267, and the deferred Task 14 tests at 05:58 and 05:64.
- **Current-protocol rows:** re-read against the checkout sources, not against scope-rules summaries.
- **Section 5 N/A:** checked against web-01's provider table and the research-directory listing.
- **Routing (checks 5 and 6):** confirmed by the full heading list and a full read of all three files.
- **Provenance:** confirmed by matching the current SHA-256 hashes to the intake record.

## Partition Limits and Evidence Uncertainty

- PARTITION NOTE: Cross-file checks are limited to synth-01..03. Cross-section consistency with sections 6-10 (partition 2) and checks 7-12 (Step 5.19) were not assessed.
- Check 3 traced a broad sample of about 60 facts covering every table row's main claim. Dense multi-clause rows were traced at row level against the deck and case sections rather than each subclause separately: synth-01 2.2 and 2.6, and synth-02's Key Takeaway table. Undetected secondary-clause mismatches like issues 4-6 may exist in those rows.
- Physical JSONL session logs were not opened. The record numbers were checked against the case-file transcriptions, which are themselves main-session persistence of analyst text.
- Graph coverage was unavailable for these files (hook: `coverage_unavailable`), so all conclusions come from direct reads.

## Recommendations

- Route all 10 issues to the Step 5.23 consolidation and the single serialized Step 5.24 fixer. All are edits confined to the synthesis files, and none changes a hypothesis or debate claim.
- Fix issue 1 and the stale NEXT rows (issue 2) before assembly, because both would otherwise propagate into the report structure.

## QA Complete

| Status | Result |
|---|---|
| DONE | Step 5.17 structure review of synth-01..03: binary FAIL, 10 issues (1 Important, 9 Minor), no targets edited. |
| NEXT | Parent persists this report at `qa/qa-synthesis-structure-1.md`. Findings feed Step 5.23 consolidation. |