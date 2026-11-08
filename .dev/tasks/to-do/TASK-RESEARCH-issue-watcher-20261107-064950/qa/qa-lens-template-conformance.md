# QA Report - report-lens-template-conformance

**Topic:** GitHub issue watcher research (issue #331)
**Status:** Complete
**Date:** 2026-11-07
**Phase:** report-lens-template-conformance (report validation, lens: template-conformance only)
**Fix authorization:** false (report only; the document is not modified)

---

## template-conformance QA Report

Report reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md`
Lens: template-conformance
Date: 2026-11-07

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | Section 2.3, report line 336 | An unresolved assembly sentinel is left in the final report: `[CONTRADICTION: Component A (synthesis 01 ...) ... Component B (synthesis 02 ...) ... Both versions presented for QA resolution.]`. The report body still holds both conflicting statements: line 334 says whether `gh issue list --json` exposes a native issue-type field is [UNVERIFIED]; Section 5.5 line 807 says the official manual lists issue type and project items and that this "closes part of Gaps #11". Checklist item c forbids sentinel or unfilled markers anywhere in the document. | Resolve the conflict (state one version in 2.3 or reword it to match 5.5, keeping the `projectItems` Status schema [UNVERIFIED]) and delete the bracketed block. |
| 2 | IMPORTANT | Section 5.13, report line 908 | Second unresolved `[CONTRADICTION: Component A (synthesis 02) ... Component B (synthesis 03) ... Both versions presented for QA resolution.]` block. It admits that Sections 5.1 and 5.13 use the web files' option lettering ("alternative C-lite", OIDC "fits C ... not B"), which is the opposite of the binding lettering used in Sections 6 to 9 (B = Action plus listener, C = central microservice). The report leaves the wrong letters "as written" (lines 763, 894, 904), so the same option letter means different things in different sections. | Re-letter 5.1 and 5.13 (OIDC row, comparison table line 904) by description and delete the bracketed block. |
| 3 | IMPORTANT | Section 6 Revisit conditions, report line 1326 | Third unresolved `[CONTRADICTION ... Both versions presented for QA resolution.]` block. The report contains two different nine-item revisit lists: Section 5.15 lines 955-965 (#7 event-time reaction, #8 change history, #9 shared ledger, no "cannot run a poller" item) versus Section 6 lines 1312-1322, repeated in Section 8 lines 1794-1804 (#7 Status change or who moved it, #8 ledger, #9 workspaces cannot run a poller). Sections 7.8 and 9.1 D6 say "nine revisit conditions" without saying which list. | Keep one canonical list (Section 6), make 5.15 point to it or match it item by item, and delete the bracketed block. |
| 4 | MINOR | Report header, lines 3-6 | The template header uses bold labels (`**Date:**`, `**Depth:**`, `**Research files:**`, `**Scope:**`). The report uses plain `Date:` lines. No line has a trailing double space or blank line between them (grep for lines ending in two spaces returned 0 matches), so the four fields render as one run-on paragraph. | Use `**Date:**` etc. and separate the lines with two trailing spaces or blank lines. |
| 5 | MINOR | Sections 1, 3, 6, 8 preambles, lines 104-112, 577-585, 991-1006, 1442-1457 | Synthesis-file working preambles survive in the assembled report ("Sources (task folder ...)", "Context and tag legend for Sections 3 to 5", "Research question context", "Sources synthesized", "Source key and evidence tags"). Line 580 adds a second stray `Date: 2026-11-07` in the middle of Section 3. None of this is in the Report Structure template. | Move the source keys and tag legend into one short "Conventions" note after the ToC, or delete the per-section copies; drop the stray `Date:` line. |
| 6 | MINOR | Section 5.10, line 860 | The paragraph "Sweep-style bots were not researched ..." follows the last table row with no blank line (a scripted scan for a non-table line directly after a table row found only this one). GitHub-flavoured Markdown will render it as a table row instead of a paragraph. | Insert a blank line before line 860. |
| 7 | MINOR | Section 10 Synthesis files table, line 1928 | The row for `synth-04-plan-questions-evidence.md` has an empty third cell ("Used by the synthesis"), and its second cell carries a prose parenthetical. An empty table cell is an unfilled value. | Fill the cell (for example "Implementation steps, open questions, evidence trail") and move the parenthetical out. |
| 8 | MINOR | Section 10, line 1930 | The template has a `### Gaps Log` subsection with a bullet for the gaps file. The report has an unheaded paragraph "Gaps Log: ..." after the Synthesis files table, so the template subsection and its ToC entry are missing. | Add `### Gaps Log` with the path as a bullet and add it to the ToC. |
| 9 | MINOR | Appendix A (lines 1987-2167) | A section that is not in the 10-section template, made of synthesis working notes (the text says "kept here unchanged"). It reuses Q-numbers (A.2 Q1 to Q19, A.1 and A.3 item numbers) that mean different things from Section 9's Q1 to Q33; for example A.2 Q4 is "Coder workspace facts" while Section 9 Q4 is the intended-owner rule. The appendix says the numbers are local, but two ID spaces in one document invite wrong cross-references. | Delete Appendix A (Section 9 is declared canonical), or rename its IDs (for example A2-1) so they cannot be confused with Section 9 IDs. |
| 10 | MINOR | Section 7, lines 1332-1436 | The template Section 7 is "**Recommended approach:** [Option X]" plus "**Rationale:**". The report has no such labels; the rationale is a table (7.2) and Section 7 grows seven more subsections (7.3 to 7.9). 7.9 is a 15-row open-items table that duplicates Section 9 instead of pointing to it. | Add the two labelled lines at the top of 7.1/7.2; move 7.3 to 7.6 into Section 6 or 8 if the structure is to match; replace 7.9 with a pointer to Section 9.2. |
| 11 | MINOR | Section 6, lines 1094-1103, 1255, 1291, 1308 | Assessment tables use the headings "Criterion / Rating and justification", the template says "Aspect / Assessment"; Pros and Cons are single prose cells, the template asks for bullet lists. Requirement Scoring, Options Comparison and Revisit conditions are unnumbered `###` headings between numbered 6.0 to 6.4 headings. | Rename the column headings, split Pros/Cons into bullets, number the three trailing headings (6.5 to 6.7). |
| 12 | MINOR | Section 5.13 line 901, 5.15 lines 930-965 | Template Section 5 gives every finding Source, Relevance (HIGH/MEDIUM/LOW) and Relationship (supports/extends/contradicts). The 5.13 comparison table, the 5.15 response-code table and the 5.15 revisit table have none of these columns, and most response-code rows have no URL. | Mark them as derived proposals in a separate subsection, or add the missing columns. |
| 13 | MINOR | Table of Contents, lines 10-98 | The ToC headings match the document exactly (87 of 87 entries, same names and levels, checked with a script), but the entries are plain bullets, not links, so the "every entry links to a section" check cannot pass. The `####` headings of Appendix A and Section 10 are not listed. | Make entries anchor links; list or drop the `####` levels consistently. |
| 14 | MINOR | Lines 96-98, 336, 340, 711, 738, 908, 1326, 1934, 1991, 2025, 2027, 2084, 2088 | Task-process language appears in the report body: "synthesis 01/02/03", "fix cycle 1", "research alignment check", "assigned research files". It describes how the report was built, not the topic. | Reword to cite the research file or the evidence directly. |
| 15 | MINOR | Section 4.2 and G28, lines 714-722 and 710 | The template's C8 control requires a cited on-record scope decision, or a Critical/High severity with a linked remediation task, for an unwired capability. Row G16 and the guard script cite owner decision Q2. `launch-job-identity.sh` (registered in packaged `hooks.json`, dormant because nothing creates `sessions/<sid>`, not installed on the host) is recorded as Minor in G28 with no cited scope decision. Content judgement, so graded minor. | Add one sentence to row G28 and the 4.2 row citing why this capability is out of scope (claim-only owner decision Q2) or raise the severity. |

### Checklist Results

| Item | Check | Result | Evidence |
|---|---|---|---|
| a | All 10 sections present or marked N/A | PASS | `grep -nE '^#{1,6} '` heading list: `## 1. Problem Statement` (102), 2 (151), 3 (575), 4 (675), 5 (751), 6 (989), 7 (1330), 8 (1440), 9 (1827), 10 (1900). None marked N/A. Template subsections that are missing or reshaped are in findings 7, 8, 10, 11. |
| b | Section order matches template; no merges | PASS (notes) | Order 1 to 10 equals the Report Structure template at `~/.claude/skills/tech-research/SKILL.md:1311-1487`. One extra section follows Section 10 (Appendix A, finding 9). Inside Section 6 the three trailing headings are unnumbered (finding 11). |
| c | No placeholder text or sentinel markers | FAIL | Case-sensitive grep for the uppercase to-do and to-be-determined tokens and FIXME: 0 matches. Three `[CONTRADICTION ... for QA resolution]` blocks remain (lines 336, 908, 1326; findings 1 to 3). Empty table cell at line 1928 (finding 7). |
| d | ToC matches headings | PASS (notes) | Script compared 87 ToC entries with 87 `##`/`###` headings: 0 mismatches in name or level. Entries are not links (finding 13). |

### Summary

- Total findings: 15
- Critical: 0
- Important: 3 (findings 1, 2, 3; each is an unresolved assembly sentinel that also leaves two conflicting versions of the same fact in the document)
- Minor: 12 (findings 4 to 15; recorded as notes)
- Adversarial target was at least 21 findings (2,167 lines / 100). 15 were found in this lens. The remaining checks found no defect: ToC names and levels (87 of 87), section order, code-fence balance (16 fences, even), the 10 section headings, phase Goal and Dependencies lines in all 7 phases, Gap table columns and severity on all 30 rows, Open Questions columns. This lens has no further defects to report beyond those listed.
- Confidence: Verified: 4/4 checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 14 | Grep: 9 | Glob: 0 | Bash: 2
- Scope note: only template conformance was reviewed. Factual accuracy, citations, internal consistency of claims and plan quality were left to other lenses; the contradictions in findings 1 to 3 are reported only as unresolved markers.

Verdict: FAIL (3 important findings open: unresolved `[CONTRADICTION]` blocks at lines 336, 908 and 1326; minor findings 4 to 15 are notes)

VERDICT: FAIL

**Status:** Complete
