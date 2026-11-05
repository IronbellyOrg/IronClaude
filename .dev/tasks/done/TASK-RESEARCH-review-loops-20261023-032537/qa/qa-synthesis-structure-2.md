# QA Report - Synthesis Structure, Partition 2

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only; returned as text because report writes are prohibited for this reviewer)
**Phase:** synthesis-gate
**Lens:** structure
**Task item:** Step 5.18
**Partition:** 2 of 2
**Fix cycle:** N/A
**Fix authorization:** false
**Governing template:** Project rf-qa Output Format (All Phases); tech-research Synthesis QA Agent Prompt

---

## Overall Verdict: FAIL

## Criteria and Partition Scope

**Assigned targets:**
- `synthesis/synth-04-options-recommendation.md`
- `synthesis/synth-05-implementation-plan.md`
- `synthesis/synth-06-questions-evidence.md`
- `synthesis/hypothesis-01.md` through `hypothesis-05.md`
- The debate artifacts listed in `reviews/adversarial/run-evidence.md`

**Governing criteria (read directly):**
- Task Step 5.18 at `TASK-RESEARCH-review-loops-20261023-032537.md:333-335`.
- R-003 is `/config/.claude/skills/tech-research/SKILL.md`. I read these parts of it:
  - Synthesis QA Agent Prompt, lines 900-942 (checks 1-6 apply to this lens).
  - Synthesis Agent Prompt, lines 779-811. Its rule at line 810 says each section must be written "in the exact format they should appear in the final report".
  - Report Structure, lines 1311-1487.
  - Synthesis Mapping Table, lines 1491-1502.
  - Synthesis Quality Review Checklist, lines 1506-1529.

**Checks applied:**
1. Exact headers and table schemas.
2. No invented assertions.
3. Primary citations resolve and support the claim.
4. At least two comparative options, realized here as the five tested hypotheses.
5. Specific research-only next checks.
6. Complete questions and evidence content.
7. Card-template compliance.
8. Debate artifacts exist.
9. Exactly five ranked causes, with the original identities preserved.
10. No placeholders, no false claims about current state, and no unrequested implementation.

**Excluded from this lens:** checks 7-12 (cross-section consistency, documentation-only claims, stale docs, content rules, completeness, invented paths) belong to Step 5.20. Synthesis files 01-03 belong to partition 1 (Step 5.17).

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match the Report Structure | FAIL | synth-04 has `## 6. Options Analysis`, `### Option A`-`E`, `### Options Comparison`, `## 7. Recommendation` with **Recommended approach** and **Rationale**: PASS. synth-05 has `## 8. Implementation Plan`, `### Phase 1-3`, `### Integration Checklist`: PASS. synth-06 has `## 9. Open Questions` and `## 10. Evidence Trail`, but uses custom subsections 10.1-10.8. The template's `### Web Research` and `### Gaps Log` subsections (SKILL.md:1480-1486) are missing. The web record `web-01-gap-applicability.md` is folded into the 10.2 research table (line 83), and the gaps log appears only in the 10.7 table (line 206). See Issue 1. |
| 2 | Components are in final-report form (SKILL.md:810) | FAIL | Worker handoff tables and stale "persistence pending" lines are embedded in the report bodies: synth-04 lines 4, 7 and 333-337; synth-05 lines 4, 7 and 135-140; synth-06 lines 4, 7 and 229-232. Persistence has actually happened (`qa/synthesis-component-intake.md:59` "Complete updated author returns persisted: 5"; synth-04:339-341). See Issue 2. |
| 3 | Table column schemas | PASS | Option tables use `Aspect / Assessment` with all six template rows: Effort, Risk, Reuse, Files/systems, Pros, Cons (synth-04:54-70, 81-97, 108-124, 135-151, 160-175). The comparison table has the template's five criteria plus extra rows (179-191). The synth-05 phase tables use `Step / Action / Files / Details` (45, 70, 86). The synth-06 Open Questions table uses `# / Question / Impact / Suggested Resolution` (13). Each card's gap table uses `Gap / Current State / Target State / Severity / Notes`, confirmed by grep with one match per card. |
| 4 | No invented assertions | PASS | I re-read about 60 synth-04 debate anchors against `ADV/debate-transcript.md` (lines 49, 128-129, 167, 208, 243, 256-265, 277, 294-304, 316, 333-344, 356, 378-385, 397, 414-426, 438, 449-453, 468-486). Also checked: base-selection 5/150-155/170-171, invariant-probe 18-20/39-44/51-54/72, return-contract 14-31, merged analysis 21/37-43/64/155-165/170/205, diff-analysis 33/69, refactor-plan 9/32, plan-review-evidence 16, and post-merge validation 120. All supported. Every quoted phrase exists in its source. For example, "more direct for its two retained blockers, but narrower overall" is at debate-transcript:265, and "a proven amplifier in two runs" is at hypothesis-03:107. The advocate orders at synth-04:221-225 match debate-transcript:480-484 exactly. No probability or percentage appears. |
| 5 | Primary citations resolve and support the claim | FAIL | Two synth-04 citation defects (Issues 3 and 4). The other checked anchors resolve: evidence-deck 49-58/121-128/376-422/565/585-598/626/643-662/726-731/814-847; scope-rules 32/41/43/45/56/64-96; gaps 11/29-59; web-01 97-148; qa-phase-3-fix-log 95-116; task-phase3-gate 67-103; task-phase4-gate 134-177. The Coder targets in synth-05:58-60 exist and match: plan lines 81-87 is Task 6, t6 log lines 1-3 are the renderer notice, progress.md lines 14-18 cover blocked, halt, ruling, complete and FINAL pass. |
| 6 | At least two options, realized as five tested hypotheses | PASS | synth-04 has five options A-E mapped to V1-V5, each with mechanism, support, opposition, alternatives, scope, falsification, evidence strength, debate record and pros/cons. The comparison table covers all five. Effort and risk are explicitly scoped to the proposed investigation, not to how likely each cause is (synth-04:5, 65-66). |
| 7 | Specific research-only next checks | FAIL | synth-05 Phase 2 has five specific comparisons, each with files, expected observation, and what would strengthen or weaken it (72-76). But synth-04:286 says "Step-level targets are in Section 8" for the 7.6 order, and order 4 (synth-04:293, adding independently selected sessions) has no row in synth-05. See Issue 5. |
| 8 | Card-template compliance | FAIL | All five cards have the ten numbered chapters, a table of contents, the template header fields and the gap table. Sections 3-6 and 8 carry explicit reasons where content is N/A. But no card's `## 1. Problem Statement` contains the template's question / why it matters / trigger bullets (SKILL.md:1334-1336), and none explains why they are absent. Extraction per card and a grep for "research question\|why it matters\|trigger" returned 0 for every card. See Issue 6. |
| 9 | Complete questions and evidence content | FAIL | synth-06's inventory counts are accurate for its stated snapshot. I recomputed: research 23 (16 local Markdown + web-01 + 6 captures), QA 191 (133 + 58 by group arithmetic), reviews 17 (4 + 13), phase-outputs 9, resume-analysis 4. QA now holds 202 files, which is 191 plus 10 gate stubs plus `synthesis-gate-intake.md`. However, the Evidence Trail does not list the existing `synth-04-options-recommendation.md` (it is listed only as "absent", lines 128 and 223), and it still describes the card format as unresolved (lines 126 and 220). See Issue 7. |
| 10 | Debate artifacts exist | PASS | Listed `reviews/adversarial/` (4 files) and `reviews/adversarial/adversarial/` (13 files): diff-analysis, debate-transcript, invariant-probe, base-selection, score-source-manifest.json, refactor-plan, plan-review-evidence, merge-log, variant-1..5-original. These match run-evidence.md:28-30 and synth-06:134-146. |
| 11 | Exactly five ranked causes; original identities preserved | PASS | synth-04 7.1 ranks exactly five causes, consistent with the debate's provisional V1>V3>V2>V5>V4 (`plan-review-evidence.md:16`). The sha256 of variant-1..5-original equals the five `input-manifest.json` hashes (3f39f065..., e62a753c..., f20f7fd3..., fe15dc65..., 1cf685b5...). A mechanical line-by-line check found every non-heading original line present exactly once in its card (V1 35, V2 37, V3 36, V4 36, V5 34 lines including quoted metadata). The only repeats are the generic `\|---\|---\|---\|` separator, which is expected because the added gap and provenance tables reuse it. |
| 12 | No placeholders, false current-state claims or unrequested implementation | PASS | A grep for `RF_PLACEHOLDER\|TODO\|TBD\|FIXME\|[Name]\|[topic]` across synth-04/05/06 and the five cards found no match. synth-05 is explicitly research-only (13, 101, 128-133). synth-04 7.6 requires approval and authorizes nothing (286). Current-rule statements are labeled "source-read only" and the cited skill refs exist (`quality-gates.md`, `qa.md`, `managed-workspace.md`). |

## Summary
- Checks passed: 6 / 12
- Checks failed: 6
- Critical issues: 0
- Issues fixed in-place: 0 (report-only, `fix_authorization: false`)
- Issue count: 7 (CRITICAL 0, IMPORTANT 0, MINOR 7)
- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 0 (literal searches ran inside Bash) | Glob: 0 | Bash: 13 (including 5 bounded read-only batch scripts) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0. Read+Grep+Glob (14) is at least the 12 checklist items.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `synth-06-questions-evidence.md`, section 10 (lines 40-227) | Section 10 does not follow the Report Structure's Evidence Trail subsections (SKILL.md:1475-1486). There is no `### Web Research` table (`File / Topic`) and no `### Gaps Log` subsection. `research/web-01-gap-applicability.md` sits inside the 10.2 research table under an `Agent Type` column (line 83). `gaps-and-questions.md` appears only as a row of the 10.7 gate/dispatch table (line 206). | Add `### Web Research` with a `File / Topic` row for `research/web-01-gap-applicability.md`, labeled as the reasoned-N/A record with zero external findings. Add `### Gaps Log` listing `gaps-and-questions.md`. The custom 10.x subsections can stay as additional content. |
| 2 | MINOR | `synth-04` lines 4, 7, 333-337; `synth-05` lines 4, 7, 135-140; `synth-06` lines 4, 7, 229-232 | The components are not in final-report form (SKILL.md:810). Each ends with the worker's DONE/NEXT handoff table, and synth-05 also has a "Recommended next action: Persist..." line. The NEXT rows and the Status/Persistence header lines say parent persistence is still pending, but all three files are persisted (`qa/synthesis-component-intake.md:59`; synth-04:339-341). If assembled as is, the report would carry stale process instructions inside sections 7, 8 and 10. | Remove the trailing handoff tables and the synth-05 "Recommended next action" line from the report bodies, or move them below a clearly marked non-assembled provenance block. Update the header Status/Persistence lines to the actual persisted state, with attribution to the intake record. |
| 3 | MINOR | `synth-04` line 58 (Option A, Opposition row) | The sentence "The credential proof-only rejection happened while delivery already met the lint criterion" is cited to `synthesis/hypothesis-01.md` section 6 and `research/evidence-deck.md:647-648`. Neither supports it. Card 1 section 6 covers only oracle, monitor and plan/trap counterevidence, and grep finds no credential or lint mention in card 1's body. Evidence-deck 647-648 are the oracle repairs 1-3 and monitor Tasks 10/11 rows. The supporting evidence is at `research/evidence-deck.md:595` ("Delivery criterion held") and `:649`. | Add `research/evidence-deck.md:595,649` (or the credential case section) as the anchor for the credential clause, keeping the existing anchors for the oracle and monitor clauses. |
| 4 | MINOR | `synth-04` line 90 (Option B, Debate record, "Against") | The text attributes the position to "the V3, V4 and V5 advocates" but cites only `:129` (Variant 3 advocate, Round 1, block 105-147), `:343` (Variant 3 advocate, Round 2) and `:425` (Variant 5 advocate, Round 2). The V4 advocate's position has no anchor. | Add the Variant 4 advocate's Round 2 anchors, `ADV/debate-transcript.md:379` ("most later monitor faults preexist repair") and `:385` ("stronger introduction evidence does not alone outrank..."), which lie in the V4 block at 364-404. |
| 5 | MINOR | `synth-04` line 286, with order 4 at line 293; `synth-05` Phase 2 (lines 70-76) | synth-04 says "Step-level targets are in Section 8" for the 7.6 sequence. Orders 1-3 map to synth-05's comparisons, but order 4 (apply the C-001 transition labels to additional, independently selected sessions) has no target row in synth-05. synth-05 covers only the five existing comparisons plus controls (line 13). The nearest content is synth-06 Open Question 1 (line 15). synth-04:326 discloses that its author read only synth-05 lines 1-40. | Either narrow the line 286 statement to "Step-level targets for orders 1-3 are in Section 8; order 4 corresponds to Open Question 1 in Section 9", or add a research-only, approval-gated synth-05 row that specifies the sampling target for order 4. |
| 6 | MINOR | `hypothesis-01.md` through `hypothesis-05.md`, `## 1. Problem Statement` (card 1 lines 27-31; card 2 27-31; card 3 27-31; card 4 27-33; card 5 27-33) | Card-template gap. The Report Structure's Problem Statement requires the question, why it matters and the trigger (SKILL.md:1334-1336). Every card's chapter 1 contains only `### Original Hypothesis`, with no explanation for the omitted elements. Sections 3, 4, 5, 6 and 8 in the same cards do explain their N/A portions, so chapter 1 is the only chapter whose missing template elements are neither present nor justified. | In each card's chapter 1, add a presentation-only N/A note, or the shared research question as already stated in the package (synth-04:8). The verbatim original hypothesis body must stay untouched. |
| 7 | MINOR | `synth-06` lines 51, 126, 128, 220, 223 (sections 10.1, 10.4, 10.8) | The Evidence Trail lists every package file except the existing options/recommendation component. It records `synthesis/synth-04-options-recommendation.md` only as "absent at the snapshot" (128, 223), counts synthesis/ as 10 files (51), and says the cards' ten-section format acceptance is unresolved (126, 220). In fact synth-04 exists (modified 2026-10-24 01:03), and all five cards are now ten-chapter presentations (modified 00:48-00:53, each with a 10.5 persistence record). The snapshot framing is honest, but at this pre-assembly gate the Evidence Trail does not list every synthesis file produced. | Refresh 10.1, 10.4, 10.6 and 10.8 to the current disk state: add the synth-04 row, update the synthesis and QA counts, and record the cards' completed format-only presentation with their 10.5 records. Keep the earlier snapshot as a dated historical note rather than the current inventory. |

## Actions Taken

None. This was a report-only review with `fix_authorization: false`. I edited no target, stub or other file. I ran no agents, tests, Git, staging, archive, move, delete or external lookups. All shell activity was read-only inspection: five bounded batch scripts, each in a private `mktemp` directory under `/tmp` with a cleanup trap, plus individual read-only `grep`/`sed`/`awk`/`ls` calls.

## Self-Audit

The verdict is FAIL with 7 genuine defects. I did not set or meet any quota. Every issue above was confirmed with a direct read or search, not taken from another report.

**Tool-backed checks:**
- **Headers and schemas.** Grepped every heading in the five cards. Read all three synth files in full and compared each table header to the Report Structure lines.
- **Identity preservation.** Recomputed sha256 for all five variants against `input-manifest.json`. Ran a line-by-line exact-once check of every non-heading original line against its card.
- **Debate fidelity.** Printed and compared about 60 cited debate-artifact lines, and attributed each advocate citation to its transcript block using the transcript's own `###` headings. One finding I was about to raise was withdrawn: the quoted phrase "more direct for its two retained blockers, but narrower overall" was verified verbatim at debate-transcript:265.
- **Package citations.** Printed the cited lines in the evidence deck, rule map, gap register, web record, fix log and both gate decisions.
- **External paths.** Confirmed that the three Coder rendering targets, the oracle artifact root and the three installed skill refs exist, and read the cited Coder line ranges.
- **Inventory.** Recounted the research/ (23), qa/ (202 now; 191 + 11 post-snapshot), reviews/ (17), phase-outputs/ (9) and resume-analysis/ (4) inventories, and spot-checked ten grouped QA filenames for existence.
- **Placeholders.** Grepped all eight targets for placeholder tokens.

**Checked and found clean:** the five-option completeness, the ranking tallies, the absence of probabilities, research-only scoping, the existence of debate artifacts, and the table column schemas.

## Partition Limits and Evidence Uncertainty

- `[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]` I did not review synth-01/02/03 (Step 5.17). Cross-section consistency, documentation-only claims, stale-documentation routing, content rules and path checks (checks 7-12) belong to Step 5.20.
- Historical JSONL physical-record anchors (for example oracle 291/383/450, monitor 759-762/1240, credential 332-435) were checked against the case-carrying cards (hypothesis-03 and -05 support tables, hypothesis-04 supporting incidents) and against the case-report section structure. They were not replayed against the original session JSONL logs. That is a primary-log check outside this structure lens.
- I did not read every line of the case reports `research/01`-`06`. Claims about their sections were spot-checked where synth-04 depends on them, for example the CI "four new medium" downgrade at `research/04-session-43582de1.md:16`.
- I read cards 1, 2 and 5 in full. Cards 3 and 4 were checked by heading extraction, the mechanical preservation check, chapter 1 and supporting-incident extraction, N/A and UNEXECUTED counts, and targeted greps, not by a full sequential read.
- Codebase-graph coverage was unavailable for package files, so every conclusion rests on direct reads.
- I observed a defect in the governing source itself: SKILL.md:1523 says "the following 3 items are unique to rf-qa" but numbers them 11-13 against a 12-item checklist. It does not affect the targets and is not counted as a target finding.

## Recommendations

- Route all seven issues to the Step 5.24 single serialized correction pass. Every fix is a targeted citation, label or inventory edit.
- None of the fixes needs a change to the hypothesis arguments, the debate transcript, or the original variants, so a re-debate is not triggered.
- Re-verify the corrected synth-04, synth-06 and card chapter 1 sections in the Phase 5 fix-cycle check before assembly.

## QA Complete

Verdict FAIL; 7 issues (CRITICAL 0, IMPORTANT 0, MINOR 7). Report-only; no files modified. This report was not written to disk because report writes are prohibited for this reviewer. The intended path is `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-structure-2.md`, which the parent should persist exactly.