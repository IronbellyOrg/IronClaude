## Template-Conformance QA Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Lens:** Template-Conformance (report-lens-template-conformance)
**Date:** 2026-11-07
**Fix authorization:** false (report not modified)

**Template:** Report Structure in `~/.claude/skills/tech-research/SKILL.md:1311-1487`
**Method:** report read in full (lines 1-1651, Reads of 150 lines or fewer); every header grepped; marker grep for `TODO|TBD|FIXME|XXX|[CONTRADICTION|Assembler note|this file)|not yet written|(synth-0N`. Lines :390-395 sit inside a code fence and were not treated as headers.

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | S7 (:1078-1080) | (c) An unresolved assembler sentinel remains: `[CONTRADICTION: ... Both versions presented for QA resolution.]`. It cites the HOW-WE-WORK "Other commands" table as `:314-337` (synth-04) or `:318-337` (synth-01/02). The report uses both: `:314` at :935 and :1075, `:318` at :237, :433 and :1214. A developer cannot tell which line range is right. | Read `src/superclaude/core/HOW-WE-WORK.md`, choose the correct range, correct every citation, and delete the marker (or turn it into a numbered S9 row). |
| 2 | IMPORTANT | S9 (:1507-1509) | (c) A second unresolved `[CONTRADICTION ... Both versions presented for QA resolution.]` sentinel. S9 row 21 (:1461) pins `Bash(superclaude sweep:*)` (colon form), while synth-02 3.1 and S8 step 1.15 use `Bash(superclaude sweep *)` (space form). Neither form is chosen, so the `allowed-tools` line that step 1.15 writes is undecided. | Check the `allowed-tools` form used by existing command files, choose one form, align row 21, step 1.15 and 3.1, and replace the marker with a resolved row or an Open Question row. |
| 3 | IMPORTANT | S10 (:1639-1642) | (c) Stale self-reference copied from synth-06: `synth-05-implementation-plan.md (planned; not yet written when this file was produced)` and `synth-06-questions-evidence.md (this file)`. Both are false in the assembled report (synth-05 exists and is the source of S8; "this file" is the report, not synth-06). An "Assembler note" at :1642 contradicts the list instead of correcting it. | List the six synthesis files as they are now (synth-05, 310 lines), remove "(this file)", and delete the assembler note. |
| 4 | IMPORTANT | S4.9 (:604-617), S7.1 (:1096-1111), S8.2 (:1324-1342) | (b) Open Questions are merged into three other sections, each with its own local `OQ-N` numbers (synth-02, synth-04 and synth-05 numbering, stated in "Assembler note" :606 and :1326). Cross-references such as "OQ-11" (:1205, :1252-1253), "OQ-1" (:1227, :1259) and "OQ-6" (:1217) are therefore ambiguous: the same id means different questions in S4, S7 and S8. | Move every open question into S9 with one numbering; replace local `OQ-N` references with S9 row numbers; remove 4.9, 7.1 and 8.2 or reduce each to a pointer to S9. |
| 5 | IMPORTANT | S7 (:1066-1094) | (b) S7 merges S8 and S5 content: an "Implementation steps" table (:1066-1076) duplicates the S8 plan, and an "External context" block (:1082-1094) repeats S5. The duplicated steps disagree with S8 (HOW-WE-WORK `:314` at :1075 versus `:318` in step 1.21 at :1214). | Reduce S7 to the `**Recommended approach:**` and `**Rationale:**` template, with pointers to S8 for steps and S5 for external context. |
| 6 | MINOR | S7 (:1033-1037) | The label `**Recommended option: A1.**` replaces the template's `**Recommended approach:**`; the rationale is a `### Rationale (from the comparison)` heading with a table instead of a `**Rationale:**` paragraph. | Use the template labels. |
| 7 | MINOR | S6 (:868-1031) | Options are named A1-A4 instead of Option A/B/C; there is an extra "Constraints every option must meet" subsection (:870); A4 uses "How it would work" and "Why it is rejected" instead of the Description / How it works / Aspect table; the comparison table adds a "Meets K-1..K-6" row. | Follow the Option A/B/C block and the five-criterion comparison; move constraints into S3.3. |
| 8 | MINOR | S5 (:645-797) | The finding fields do not match the template: `**[EXTERNAL] Finding:**` with non-bold nested "Source:", "Relevance:" and "Relationship:" (not "Relationship to codebase"); an extra "WC-10 / read-only" field; "Relevance: LOW for Phase 1" (:664) and "Finding (context only)" (:749) break the HIGH/MEDIUM/LOW enum and the label. | Use `**Finding:**` / `**Source:**` / `**Relevance:** HIGH/MEDIUM/LOW` / `**Relationship to codebase:**`. |
| 9 | MINOR | S5 (:641) | The section repeats the research-question text from the header (:9), which is synth-03 header text carried over. | Remove the repeat. |
| 10 | MINOR | S3.3 (:458-471) | An "External context" table (S5 content) is merged into Target State constraints. | Move it to S5 or replace it with a pointer. |
| 11 | MINOR | S8 (:1129-1240) | Phase 1 is split into `#### 1A`-`1F` sub-phases; later phases are a one-line table instead of Phase 2..N blocks; `**Goal.**` / `**Dependencies.**` use periods, and Dependencies is a table; the Integration Checklist (:1404) comes after 8.1-8.5 instead of directly after the phases. | Use the Phase N / Goal / Dependencies / step-table form and place the Integration Checklist directly after the phases. |
| 12 | MINOR | S8.1-8.5 (:1241-1402) | Non-template subsections: 8.3 repeats S5 external context; 8.4 repeats S4.8 and S9.4 contradictions under a fourth id scheme (X-1..X-12); 8.5 is a process coverage table. | Keep the plan and checklist; move or point the rest to S4, S5 and S9. |
| 13 | MINOR | S4 (:477-633) | The template's single Gap table (Gap / Current State / Target State / Severity / Notes) is split into ten subsections, including a severity-rules list (4.1), resolved rows (4.5), contradictions (4.8, which duplicates 9.4) and coverage (4.10). Rows in 4.6 are keyed by citations (for example "scope-02 `:146`") rather than gap names. | Use one gap table with named gaps; move resolved rows, contradictions and coverage to S9 and S10. |
| 14 | MINOR | S1 (:34-40) | Labels use periods (`**The question.**`, `**Why it matters.**`, `**Trigger.**`) instead of the template's colon form. | Use `**The question:**`, `**Why it matters:**`, `**Trigger:**`. |
| 15 | MINOR | Header (:7-13) | Non-template header fields: Task folder, Research question, Evidence labels and "NB-4 fix in effect". Judged under this lens, the NB-4 research-gate-by-exception record is consistent everywhere it appears (:13, 9.6 :1583, S10 :1646 and :1651) and is not a conformance defect; only its placement as a header field departs from the template. | Keep the Date/Depth/Research files/Scope header; move the labels and the NB-4 record into S10 (Gaps Log / QA reports). |
| 16 | MINOR | Body (:164, :245, :265, :606, :1096, :1113, :1156, :1241, :1326, :1642) | (c) Assembly and synthesis process text remains in the body: "Assembler note" (:606, :1326, :1642); header suffixes "(local numbering from synth-04 ...)" (:1096), "(synth-04)" (:1113), "(synth-02 Section 4)" (:1241); "Nothing in this synthesis builds on A4" (:164); "Tally from scope-03/scope-04" (:245, :265); "SC-1 to SC-16 in synth-02 3.2" (:1156). | Remove synthesis-file references from headers and prose; cite report sections instead. |
| 17 | MINOR | 4.10, 7.2, 8.5, 9.7, :1603 | Four non-template "coverage of assigned files" tables plus the sentence "A file without a Key Takeaways list is not a defect and is not listed as one" (:1603) are aimed at QA, not at readers of the report. | Remove them or fold one evidence map into S10. |
| 18 | MINOR | 4.1, 4.6, 5.9, 5.10, 6, 8.4 | Id collisions: external "C1, C2" (5.9 :814-815) versus codebase C1-C15 (4.6), and ":729 (5.9, C1)"; A4 risks R-1..R-4 (:1004-1007) versus severity rules R-1..R-3 (4.1) versus R1-R9 (5.10); constraints K-1..K-6 versus gaps K1-K4; X-1..X-12 in 8.4. | Give each id family its own prefix. |
| 19 | MINOR | ToC (:22-29) | (d) The ToC is not generated from the headers; subsection labels are lowercased paraphrases: "2.6 summary" (header "2.6 Current State Summary"), "4.9 open questions" (header "Open Questions ([UNVERIFIED], not stated as fact)"), "8.2 open questions" ("Open Questions carried by the plan"), "8.3 external context" ("External context used by the plan"), "9.6 resolved rows" ("Resolved rows and where they were resolved"). | Regenerate the ToC from the actual header text. |
| 20 | MINOR | ToC (:19-30) | (d) Hierarchy is flattened: only the ten top-level sections are linked (their anchors such as `#1-problem-statement` resolve); subsections are unlinked plain text, and the `####` sub-phases 1A-1F (:1170-1219) are missing. | List subsections as nested, linked entries, including 1A-1F. |
| 21 | MINOR | ToC (:19) | The ToC is a four-column table with an extra "Source" column (synth file per section): process metadata the template does not have. | Use the template's ToC list; keep source mapping in S10. |
| 22 | MINOR | S9 (:1474, :1561) | Non-integer row ids "33a" and "98a" were inserted into the numbered list. | Renumber the S9 rows sequentially. |
| 23 | MINOR | S9 (:1431-1603) | S9 is split into seven subsections. 9.6 (GQ rows / Where resolved) and 9.7 (File / Gaps entries / Covered by) do not use the # / Question / Impact / Suggested Resolution columns. 9.5 rows 99-109 only point to other rows (for example "GQ-60"), which duplicates entries. | Keep one Question/Impact/Suggested Resolution table; move resolved rows and coverage to S10; merge AMBIGUITY pointer rows into their GQ rows. |
| 24 | MINOR | S9 (:1501-1502) | (c) Rows leave process instructions that cannot apply to an assembled report: row 60 says "Correct the wording in the final report", but this is the final report; row 61 says "Re-cite at the Phase 5 synthesis gate", a gate that has already passed. | Apply or drop the instruction and state the outcome. |
| 25 | MINOR | S10 (:1611-1651) | The Agent Type column holds descriptions ("Phase 2 codebase research agent") instead of agent types; non-template "Synthesis files" and "QA reports" subsections; the Web Research File cells carry line counts and an `[EXTERNAL]` tag. The header count "8 codebase + 2 web" (:5) matches S10 (8 + 2), so that part conforms. | Use agent type names; keep only File/Topic in the web table. |
| 26 | MINOR | 2.3, 3.3, 4.6, 5.9, 6, 8, 9 | The A4 rejection is restated in at least eight places (:164, :456, :569, :819, the S6 A4 block, :1133, :1455, :1491). | State it once in S6 and point to it elsewhere. |
| 27 | MINOR | S2/S3 boundary (:320-321) | A double blank line before the `---` separator. | Collapse it to one blank line. |

### Checklist results

| Check | Result | Evidence |
|-------|--------|----------|
| (a) All 10 sections present, or N/A with rationale | PASS | Header grep: `## 1.` :34, `## 2.` :42, `## 3.` :324, `## 4.` :477, `## 5.` :635, `## 6.` :868, `## 7.` :1033, `## 8.` :1129, `## 9.` :1431, `## 10.` :1607. None is marked N/A. |
| (b) Order matches the template, no merged sections | FAIL | Order 1-10 is correct, but Open Questions are merged into S4, S7 and S8 (findings 4, 5, 10, 12, 13). |
| (c) No placeholder, sentinel or TODO text | FAIL | No TODO/TBD/FIXME/XXX; two unresolved `[CONTRADICTION]` sentinels (:1078, :1507), a stale "(planned; not yet written)" / "(this file)" entry (:1639-1640), and assembler notes (findings 1-3, 16, 24). |
| (d) ToC matches headers and hierarchy | FAIL (minor only) | Top-level anchors resolve; subsection labels are paraphrased, unlinked and incomplete (findings 19-21). |

### Summary

- Total findings: 27
- Critical: 0
- Important: 5 (findings 1-5)
- Minor: 22 (findings 6-27; notes only, they do not fail the review)
- The two `[CONTRADICTION]` markers and the NB-4 record were judged in place and not removed (report not modified).
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 15 | Grep: 5 | Glob: 0 | Bash: 0 (no web research)

**Verdict: FAIL**
