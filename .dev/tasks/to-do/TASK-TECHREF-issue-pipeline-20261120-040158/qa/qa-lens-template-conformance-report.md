# QA Report - Gate 3 Lens: Template Conformance

QA phase: lens-template-conformance
Lens: template conformance (Gate 3, Step 6.2, N = 23)
Document: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (2369 lines)
Template: /home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md
Date: 2026-11-20

## Verdict: PASS

BLOCKING findings: 0. MINOR findings: 7 (notes only). Fix authorization was false; the document was not modified. Nothing was written under the snapshot.

## Template section presence table

Order check: all 16 template sections appear in template order (headings at lines 183, 224, 364, 444, 655, 1366, 1395, 1401, 1509, 1576, 1648, 1695, 1744, 1856, 2003, 2081 by `grep -n '^#'`).

| Template section | Present yes/no | Line in document | Notes |
|---|---|---|---|
| Frontmatter (31 template fields) | yes | 1-53 | Every template field is present and non-placeholder (`source_references` is an extra field, harmless). Unknowns are written as "Not recorded in the sources" / "None found in the snapshot", not as sentinels. |
| Title, WHAT/WHY/HOW TO USE, Lifecycle table | yes | 55-74 | Lifecycle table adapted truthfully (Product PRD "None found in the snapshot"). Template "Tiered Usage" table omitted (template guidance, not content). |
| Document Information (8 fields) | yes | 78-89 | All 8 fields filled. "Last Verified Against Code" dated 2026-11-20 against 61ac2c2e6, consistent with 15.1. |
| Living Document Contract | yes | 91-98 | Verbatim from template. |
| Completeness Status + Contract Table | yes | 102-134 | 16 section lines + Appendix A/B + links + review. Two unchecked boxes (links, review) are truthful, not placeholders. |
| Table of Contents | yes | 138-179 | See check 5; matches headers (two level-5 headings omitted, F-06). |
| 1. Overview | yes | 183-220 | What it does / Who uses it / Where it lives / statistics present. The single PR 686 sentence is at 218. |
| 2. Architecture | yes | 224-362 | Populated; subsections remapped (F-01). |
| 3. Directory Structure | yes | 364-442 | Populated; 3.1 is a file inventory, not "File Naming Conventions" (F-01). |
| 4. Data Flow | yes | 444-653 | Populated; subsections 4.1-4.6 remapped (F-01). Required trigger table 4.4 and writes-to-GitHub table 4.5 live here. |
| 5. Subsystem Reference (5.1-5.4) | yes | 655-1364 | 5.1 at 657, 5.2 at 990, 5.3 at 1155, 5.4 at 1326. All four present. |
| 6. State Management | yes | 1366-1393 | Populated for on-disk stores (28 lines, under the 150 cap). Columns adapted (F-02). |
| 7. Component Inventory | yes (N/A) | 1395-1399 | "N/A - not a UI feature" with rationale. Matches the required N/A wording. |
| 8. API & Integration Points | yes | 1401-1505 | Populated; subsections 8.1-8.5 differ from template 8.1-8.3 (F-01, F-02). |
| 9. Configuration & Environment | yes | 1509-1572 | Populated; 9.1-9.4 (F-02). |
| 10. Error Handling & Edge Cases | yes | 1576-1644 | Populated; 10.1-10.4 differ from template (F-01). |
| 11. Performance Characteristics | yes | 1648-1691 | Populated; states plainly that no measured values exist. |
| 12. Conventions & Patterns | yes | 1695-1740 | 12.1-12.3 present with template titles. |
| 13. Extension Guide | yes | 1744-1852 | 13.1 and 13.2 present; 13.1 is bullets, not the template table (F-02). |
| 14. Known Limitations & Technical Debt | yes | 1856-1999 | 14.1, 14.2, 14.3 present with template titles; 14.1 and 14.3 table columns match the template exactly. |
| 15. Verification & Accuracy | yes | 2003-2077 | 15.1 log (date 2026-11-20, commit 61ac2c2e6), 15.2 spot-check protocol, 15.4 Evidence Trail. |
| 16. Glossary | yes | 2081-2132 | Term / Definition columns as in the template. |
| Appendix A: Test-Pin Matrix | yes | 2136-2208 | After Section 16. Required title present. |
| Appendix B: Removed on 2026-11-20 | yes | 2212-2355 | After Section 16. Required title present. |
| Document History | yes | 2359-2363 | Last block, as in the template; columns match. |
| Template footer | yes | 2367 | Present. |

## Required content (a)-(g) of the build request

| Item | Present | Where | Evidence |
|---|---|---|---|
| (a) live-versus-switched-off ledger | yes | 2.3, lines 317-343 | 18 rows plus 1b, 7b, 12b. Rows 1-8 are exactly watcher, claim, L1, L2, identity, G2 rule 2, coordinator text, removed package. Status words used: BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED, each with an Evidence column. |
| (b) writes-to-GitHub table | yes | 4.5, lines 585-615 | One table, a row per piece (watcher G1-G7, claim C1-C5, create X1-X3, workers, scripts, hooks, installers, coordinator text, removed package) with exact commands. |
| (c) trigger table | yes | 4.4, lines 558-583 | Columns: Piece, What starts it, Who or what runs it, Frequency, Evidence, Live?. |
| (d) test-pin matrix | yes | Appendix A, lines 2136-2208 | 48 rows (21 + 11 + 9 + 7); I compared every test file named in research-notes.md lines 61-63 (20 watcher files plus fixtures, 9 hooks, 7 skills, 1 command, 2 cli, 3 unit, 1 core) with the matrix: none missing. Columns include Path, Lines, Tests, What it pins. |
| (e) doc-vs-code contradiction table | yes | 14.1.2, lines 1876-1922 (also 5.1.8 at 950-962) | Part A: KW-1..KW-8. Part B: X-1..X-28. |
| (f) Appendix "Removed on 2026-11-20" | yes | lines 2212-2355 | B.1-B.9. |
| (g) exactly one PR 686 / rewrite design sentence | yes, count = 1 | Section 1, line 218 | `grep -in 'PR 686\|#686\|rewrite'` returns: "PR 686" 1 hit (line 218); "rewrite design" 1 hit (line 218, the same sentence). Other "686" hits are line ranges (`685-686`, `654-686`, `669-686`); "Rewrites" at lines 435 and 1264 describe the identity hook. No other description of PR 686 or the rewrite exists. The sentence is "PR 686 and the rewrite design are out of scope for this reference." |

## Findings

| ID | Severity | Location | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| F-01 | MINOR | Sections 2, 3, 4, 6, 8, 9, 10, 11 | Subsection titles differ from the template. Template subsections with no same-titled counterpart: 2.3 Key Design Decisions (As Built), 2.4 Technology Stack, 3.1 File Naming Conventions, 4.2 Data Sources, 4.3 Data Transformations, 6.1-6.4, 8.1 API Endpoints Used, 8.2 Internal Integration Points, 10.1 Error Handling Patterns, 10.2 Known Edge Cases, 10.3 Graceful Degradation, 11.1 Performance Profile. The template's External Service Dependencies table is present but numbered 8.5 (line 1498), not 8.3. The information they carry is present elsewhere: design divergences in 14.1.2, data sources and transformations in 4.1 and 4.5, state in 6 and 5.1.3, edge cases in 10.3 and 14.3.1. Sections 2.3, 4.4, 4.5 and 14.2.1 hold the content the build request requires beyond the template. The Standard tier requires "all numbered sections", which are all present. | Headings from `grep -n '^#'` (lines 228-345, 413, 465-617, 1407-1498, 1578-1637, 1652-1683). | Optional: add a one-line pointer under each remapped section naming where the template's subsection content sits. No fix is needed to pass. |
| F-02 | MINOR | 2.2, 6, 8.1, 8.3, 9.1-9.3, 10.1, 11.1, 12.1, 13.1, 14.2.1 | Table column sets differ from the template where it prescribes them. 2.2 (Component / Path / Role / Depends on / Depended on by vs Subsystem / Purpose / Primary Directory / Key Files); 6 (single table with Writer / Readers vs Store / Library / Scope / Purpose); 8.1 (R/W, Actor, File:line vs Method / Request / Response shape); 9.3 (no "Required" column); 11.1 (Name / Value / Where / Effect vs Metric / Measured Value / Method; the document states no measurements exist, line 1650); 12.1 (adds Where enforced / Pinned by test); 13.1 (bullets vs the Task / Steps / Files / Pitfalls table); 14.2.1 (ID / Capability / Declaring doc / Code evidence / Class / Status word / Note vs Item / Severity / Description / Effort, which the build request's C8 rule requires). Columns match the template exactly in 12.2, 12.3, 13.2, 14.1.1, 14.3, 15.1, 16 and Document History. | Table headers at lines 1370, 1411, 1543, 1654, 1701, 1930; template lines 335, 406, 438, 482, 511, 561. | Optional; no fix needed to pass. |
| F-03 | MINOR | 5.1-5.4 | The template's per-subsystem skeleton (Purpose, Key Files, How It Works, Public Interface, Dependencies, Consumers, Conventions) is only partly followed. 5.1 has a "Dependencies and consumers" paragraph (line 691) but no Public Interface or Conventions block; 5.2-5.4 have Purpose, Key Files, How It Works and Extension points but no Dependencies or Consumers tables. Section 2.2 gives "Depends on / Depended on by" for every component, so the information exists. | Read of lines 655-1364. | Optional. |
| F-04 | MINOR | 5.1 (657-979), 5.4 (1326-1363), whole document | Lens item 9 asked for subsystem sections of 40-200 lines. 5.1 is about 323 lines (template: "candidate for its own separate Technical Reference"); 5.4 is 38 lines (2 under the floor); 5.2 is about 164 and 5.3 about 170 (in range). Section 6 is 28 lines (under 150, passes). The document is 2369 lines against a 2,000-line "code smell" line in the template; the line-budget overshoot is a known, accepted tier decision and is MINOR only. | Heading line numbers from `grep -n '^#'`. | None required (accepted tier decision). |
| F-05 | MINOR | 1 (line 203), 3 (lines 371, 384, 391, 403) | Line 203 says the key statistics are "stated here once; later sections do not repeat them", but several are repeated: the watcher module line counts (cycle 1,406 and so on) appear again in 3.1 (line 417) and 5.1 (line 680); 59 reason words, 19 fixtures, 12 argv elements recur in many sections. The directory tree also carries counts ("nine modules", "10 files", "15 files", "19 test files", "19 JSON files"), which the template's Directory Structure rule says to avoid. A wording and style issue, not a wrong fact. | Lines 203, 207, 371, 384, 391, 403, 417, 680; template lines 686-688. | Reword line 203 to "stated first here". |
| F-06 | MINOR | Table of Contents (138-179) | The ToC lists every numbered heading in order and its links match GitHub slugs (for example `#8-api--integration-points`, `#appendix-b-removed-on-2026-11-20`). It omits two level-5 headings: 5.1.1.1 (line 739) and 5.1.1.2 (line 761). The 13.1.1-13.1.8 entries are bold labels, not headings; the ToC summarises them as a range. | `grep -n '^#'` against ToC lines 140-179. | Optional: add the two entries. |
| F-07 | MINOR | 15.2 (2013-2036), footer (2367) | 15.2 replaces the template's five-step spot-check list with an 18-row command table. The table covers file existence and interface checks but has no step comparing Section 6 state shapes with the store definitions (Section 6 is present, so the template's check 3 applies) and none for Section 12 conventions (template check 5). The footer says "structure followed", which is slightly stronger than the subsection differences in F-01 to F-03 support. | Read of lines 2017-2036 and 2367; template lines 591-595. | Optional: add two rows to 15.2; reword the footer. |

## Checks performed

| # | Lens check | Result | How checked |
|---|---|---|---|
| 1 | All 16 sections present in order, N/A with rationale for Section 7 | PASS | `grep -n '^#'` (all headings); reads of 183-1400; Section 7 at 1395-1399 has "N/A - not a UI feature" and a rationale. |
| 2 | Frontmatter complete; Document Information and Completeness Status present and truthful | PASS | Compared lines 1-53 with template lines 1-42 field by field (all 31 present); Document Information 8 of 8; Completeness Status lines 102-134 agree with the sections that exist; the two unchecked boxes are stated as not done. |
| 3 | Numbering and header text; Section 5 has 5.1-5.4 | PASS (with F-01) | Top-level numbers and titles match the template; 5.1, 5.2, 5.3 and 5.4 headings at 657, 990, 1155, 1326. |
| 4 | Table column structures | PASS with notes (F-02) | Header rows compared with the template for Sections 2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16. |
| 5 | ToC matches headers | PASS with note (F-06) | Order, anchors and entries checked against the heading list; no phantom entries. |
| 6 | Appendix A, Appendix B, Document History after Section 16 | PASS | Headings at 2136, 2212, 2359; Section 16 at 2081. |
| 7 | No placeholders or sentinels | PASS | Two greps: `TODO\|TBD\|FIXME\|PLACEHOLDER\|placeholder\|YYYY\|[FEATURE...` returned only the ToC link text "Subsystem Reference" and quoted `gh issue create --title "[FEATURE] ..."` command text (source text); a second grep for template bracket tokens and `**Status**` found only the two intentional unchecked boxes (lines 123-124). Angle-bracket tokens in the 13.1 skeletons (for example lines 1756, 1799) are intentional illustrations, not template placeholders. |
| 8 | Required content (a)-(g) as structures; PR 686 count | PASS | See the table above; count of "PR 686" = 1 and "rewrite design" = 1, both in the single sentence at line 218. |
| 9 | Subsystem sections 40-200 lines; Section 6 under 150 | PASS with notes (F-04) | Line spans from heading numbers; 5.1 over 200, 5.4 two lines under 40, graded MINOR because the lens severity rule lists only missing required structures, placeholders, a wrong ToC and extra PR 686 sentences as BLOCKING. |
| 10 | Section 15 content | PASS with note (F-07) | 15.1 date 2026-11-20 and commit 61ac2c2e6; 15.2 protocol; 15.4 Evidence Trail. I confirmed every research, synthesis, sandbox, gaps-and-questions and BUILD-REQUEST path in 15.4 exists (Glob of the task folder). |

Counts: 10 lens checks, 10 passed (4 with MINOR notes); BLOCKING 0; MINOR 7.

Confidence: Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for this lens only. Other lenses (facts, cross-section consistency, citations) were not in scope and were not graded.

Tool engagement: Read: 18 (instruction block, template, build request, 12 reads covering all 2369 lines of the document, 2 research-notes reads, own report) | Grep: 7 | Glob: 3 | Bash: 0

Not graded here (out of lens): correctness of cited line numbers, counts and quoted constants; those belong to the evidence-quality, internal-consistency and code-example lenses.

Status: Complete
