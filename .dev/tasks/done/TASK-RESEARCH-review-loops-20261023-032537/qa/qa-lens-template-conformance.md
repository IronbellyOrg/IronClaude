## Template-Conformance QA Report

**Report reviewed:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md (1,263 lines)
**Lens:** Template-Conformance (Task Step 6.2, report-validation, `fix_authorization: false`)
**Date:** 2026-10-24
**Intended output path (parent to persist):** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-template-conformance.md
**Delivery note:** This reviewer's agent rules forbid writing report files, so this complete report is returned as text for the parent to save. No file was edited.
**Governing sources read:** `/config/.claude/skills/tech-research/SKILL.md:1042-1151` (Lens-Specific QA Agent Prompt Template, Template-Conformance Checklist a-d, output format), `:1241-1307` (Assembly Agent Prompt and assembly rules), `:1311-1487` (Report Structure); `BUILD-REQUEST.md:1-57`; task file Step 6.2 (`TASK-RESEARCH-review-loops-20261023-032537.md:381-383`).

---

### Overall Verdict: FAIL

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|-------------|
| 1 | IMPORTANT | Sections 1, 2, 3, 4, 5, 6, 7, 8, 10 (throughout) | The assembled report still talks about itself as if it were one synthesis piece ("this component", "this synthesis", "these sections", "this worker"), and three of those passages say the document contains no ranking even though Section 7.1 contains one. L87: "separates the observed mechanisms before any subsequent debate or ranking of five candidate causes. These sections describe the evidence, not the eventual ranking." The debate is finished and the ranking is in Section 7. L284: "This component assigns neither ranking nor causal probability". L436: "This component adds no case, hypothesis ranking, probability estimate". Other unadapted self-references, found by grep: L196, L237, L245, L247, L263, L328, L343, L347, L353, L390, L396, L400, L424, L448, L716, L745, L801, L817, L828, L1033, L1056 ("This complete return is its assigned replacement content"), L1152 ("this worker made no task edits"), L1164. In a single report, "this component" has no meaning, and L87/L284/L436 contradict Section 7. The cause is in 10.10 (L1263): Sections 1-10.8 were kept byte-identical to the component text. The Assembly Agent Prompt allows "minimal transitional text where needed for coherence" (`SKILL.md:1304`). | Rewrite each listed passage at report level. Name the section ("Sections 1-2", "Section 5"), say "this report", or name the actual producer. Change L87, L284 and L436 so they send the reader to Section 7 for the ranking instead of denying that one exists. Change L1056 and L1152 so they name the synth-06 worker explicitly. |
| 2 | MINOR | Section 7.6 (L720); Section 8 Integration Checklist (L910) | Some cross-references point to synthesis files when they should point to report sections. L720: "Step-level targets are in Section 8 (`synthesis/synth-05-implementation-plan.md`)" and "corresponds to Open Question 1 (`synthesis/synth-06-questions-evidence.md`, Question 1)". L910: the "Component review" row sends the reader to "the non-assembled Provenance and Delivery Record at the end of `synthesis/synth-05-implementation-plan.md`". That is component-delivery metadata inside the template's Integration Checklist. | At L720, cite "Section 8, Phase 2, last row" and "Section 9, Question 1". Remove the L910 row, or move it to Section 10 as provenance. |
| 3 | MINOR | Section 7.8 (L756-775) | Section 7 is meant to hold the Recommendation (Recommended approach plus Rationale, `SKILL.md:1426-1431`). Section 7.8 is instead the synth-04 producer's personal reading log: "Task file Step 5.12 and neighbors / Read (lines 250-359)", "`synthesis/synth-05-implementation-plan.md` / Lines 1-40 only", "`research/web-01-gap-applicability.md` / Not read directly" (L768), plus "Graph coverage was unavailable for package files" (L773). Inside the final report this reads as a limitation of the report itself, yet Section 5 of the same report is built on `web-01-gap-applicability.md`. | Move 7.8 into Section 10, labelled "synth-04 producer read record", or drop it. Section 7 should keep only recommendation and rationale material. Update TOC line 55. |
| 4 | MINOR | Section 5 (L420-436) | The template ends Section 5 with "5.N External Research Summary" (`SKILL.md:1388-1389`). The report puts "5.5 Evidence and Limits" (L426) after "5.4 External Research Summary" (L420), so the summary is not last. | Swap them: 5.4 Evidence and Limits, then 5.5 External Research Summary. Update TOC lines 37-38. |
| 5 | MINOR | Section 8 Step tables (L819-822, L844-851, L861-868) | The Step/Action/Files/Details template expects numbered steps (1.1, 1.2) and file paths in Files (`SKILL.md:1443-1446`). Here the Step column holds descriptive titles with no IDs. The Files column holds aliases, and L821 ("Relevant case file; evidence deck; gap register") names no specific case file. Section 7.6 (L720) points readers to "Step-level targets ... in Section 8", but there is no step ID to cite; L769 itself admits it is "referenced by path, not by step identifiers". | Add IDs (1.1-1.2, 2.1-2.6, 3.1-3.6) and keep the titles as a prefix to the action. At L821, name the six case aliases from the Phase 1 input table. Change 7.6 to cite the new IDs. |

### Summary
- Total findings: 5
- Critical: 0
- Important: 1
- Minor: 4
- Verdict: FAIL (any finding of any severity fails)

### Checks performed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | All 10 sections present in order, or N/A with reasons | PASS | Heading scan: `## 1.` (L82) through `## 10.` (L947) in template order, with `---` separators between every pair. Section 5 is N/A with stated reasons (L363-365) and keeps the template's subsection pattern. |
| b | Section ordering and subsection hierarchy match the template | FAIL (Finding 4) | Sections 2 and 6-10 keep the template's subsection order; extra subsections are inserted, not reordered. Section 5 puts 5.5 after the Summary. |
| c | No placeholders, sentinels or TODO markers | PASS | Grep for `{{`, `RF_PLACEHOLDER`, `TODO`, `TBD`, `FIXME`, `PLACEHOLDER`, `<!--`: 0 hits. Bracket-token scan finds only the two `[CONTRADICTION: ...]` markers (L223-224), which assembly rule 6 requires (`SKILL.md:1291`), and one verification tag (L169). |
| d | Table of Contents matches headings (names and hierarchy) | PASS | Script compared the 61 TOC entries (L18-78) with the 61 level-2/3 headings: text, GitHub anchor and indent level all match, 0 mismatches. The two level-4 headings (L799, L826) are left out, consistent with a depth-3 TOC. |
| e | Required table columns | FAIL (Finding 5) | S4 `Gap/Current State/Target State/Severity/Notes` (L309) matches. S6 option aspect rows Effort/Risk/Reuse/Files/Pros/Cons are present for all five options (L499-504, 526-531, 553-558, 580-585, 604-609). S6 comparison has Effort/Risk/Maintainability/Integration complexity/Reuse potential (L621-625). S9 `#/Question/Impact/Suggested Resolution` (L918) matches. S10 `File/Topic/Agent Type` and `File/Topic` (L953, L961) match. S8 has the column names but not the step IDs or file paths in the cells. |
| f | Template header fields | PASS | Title, Date, Depth, Research files, Scope (L1-8). "16 + 1 web + 6 captures = 23" checked: `ls research | wc -l` = 23, `ls research/*.md` = 17. Synthesis "11 files" checked: `ls synthesis | wc -l` = 11. |
| g | Section content is real report content (no leftover component scaffolding) | FAIL (Findings 1, 2, 3) | Self-reference grep listed in Finding 1; L720, L910, L756-775 read directly. |

### Self-Audit (clean checks)
- Option blocks: each of Options A-E has `**Description:**` and `**How it works:**` (L480/482, 508/510, 535/537, 562/564, 589/591). The adaptation of options to causal candidates is disclosed at L444. The cited SKILL line ranges at L444 and L761 were checked against my own reads of `SKILL.md`.
- Section 7 keeps the template's `**Recommended approach:**` (L631) and `**Rationale:**` (L637) labels.
- Section 3 keeps `**Desired behavior:**` (L271). Success criteria and Constraints appear as tables. I treated that as an acceptable "tables over prose" adaptation, not a defect.
- Section 8 Integration Checklist is a table of N/A items with reasons instead of `- [ ]` items. Under checklist item a (N/A with stated reasons) I accepted this as an adaptation to research-only scope.
- Section 10 starts with the template's Codebase Research, Web Research and Gaps Log subsections (L951-967) before the custom 10.1-10.10.
- Not counted as a finding: the status lines at L5, L1192 and L1213 ("NOT yet validated", "Phase 6 ... have not run") are accurate today. They will become false the moment the Phase 6 gates finish and must be refreshed then.

### Confidence and tool engagement
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 0 (pattern searches ran through Bash) | Glob: 0 | Bash: 7 (one of them the TOC and anchor comparison script). No web research.
- **Scope note:** I checked only the template-conformance lens. Findings 1 and 2 overlap with the internal-consistency lens (Step 6.3); I reported them here because they are leftover component text in the section content this lens covers.

## QA Complete

| Status | Result |
|---|---|
| DONE | Reviewed the full 1,263-line report against the template. Verdict FAIL: 5 findings (1 important, 4 minor). |
| NEXT | Parent saves this text to /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-template-conformance.md and adds these findings to the Phase 6 consolidation. |