# QA Report - Template Conformance (lens-template-conformance)

**Status:** Complete
**Topic:** Observer, sweep and dashboard technical reference
**Date:** 2026-11-20
**Phase:** lens-template-conformance (Gate 3 structural lens)
**Fix cycle:** N/A (fix_authorization: false, report only)
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Template:** /home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md

---

## Checklist (lens: template conformance)

All line numbers refer to the assembled document unless marked "T:" (template). Document read in full by Read for lines 1-410 and 1108-1698; lines 410-1108 (Section 5) were checked structurally by Grep of headings and bold sub-headers and by line-span measurement; Section 5 content accuracy is out of this lens.

| # | Checklist item | Result | Evidence |
|---|----------------|--------|----------|
| 1 | All 16 sections present, or N/A with rationale (6 and 7 expected N/A) | PASS | `## 1.` to `## 16.` all present as top-level headings (Grep: lines 161, 183, 269, 336, 402, 1112, 1137, 1143, 1229, 1270, 1309, 1354, 1411, 1474, 1618, 1639). Section 6 (1112-1135) and Section 7 (1137-1139) are N/A with stated rationale, repeated in Completeness Status (lines 110-111). |
| 2 | Frontmatter has every template field | PASS | Bash diff of key sets, template lines 2-42 versus document lines 2-48: "IDENTICAL key set" (31 keys incl. nested `review_info`). No template field missing. Values are filled (N/A where not applicable). |
| 3 | Section ordering and numbering match template | PASS | Top-level order: Document Information, Completeness Status, Table of Contents, 1-16, Appendices, Document History = template order (T:68, 92, 126, 147-599, 609, 617). No section out of order. |
| 4 | Subsection structure matches template | PASS (with additive items) | Bash `comm` of `### N.M` headings: template headings missing from the document are only 6.1-6.4 and 7.1-7.3 (Sections 6 and 7 are N/A, expected). Present: 2.1-2.4, 3.1, 4.1-4.3, 8.1-8.3, 9.1-9.3, 10.1-10.3, 11.1-11.3, 12.1-12.3, 13.1-13.2, 14.1-14.3, 15.1-15.2. Additive only: 2.5, 5.3-5.6 (template 5.2/5.N repeat), 14.4-14.6. Each of 5.1-5.6 carries Purpose, Key Files, How It Works, Public Interface, Dependencies, Consumers, Conventions & Patterns (Grep of bold sub-headers; 5.6 Purpose is on the long line 1029). |
| 5 | Table column structures match template | FAIL (1 blocking, minor notes) | Match: 2.2, 2.4, 3.1, 4.2, 4.3, 8.2, 8.3, 9.1, 9.2, 9.3, 10.1, 10.2, 10.3, 11.2, 11.3, 12.2, 12.3, 13.1, 13.2, 14.1, 14.3, 15.1. Differ: 14.2 (line 1502) drops Severity and Effort to Fix (BLOCKING, finding B-2); 8.1 (1149), 12.1 (1358), 11.1 (1315), 2.3 (225) adapted or renamed (minor notes m-1 to m-3). 5.1-5.5 Dependencies and Consumers are tables matching the template (lines 507, 515, 628, 636, 747, 755, 864, 873, 1001, 1009); 5.6 uses prose (minor m-5). |
| 6 | Document Information table, Completeness Status checklist, Contract table present and reflect reality | PASS (minor tension) | Document Information 78-89 (all 8 template fields), Living Document Contract 91-98, Completeness Status 102-122 (18 items as template; Section 6 and 7 marked N/A with reason; "All links verified" left unchecked and "Reviewed" pending, which is honest), Contract table 124-132. Minor tension recorded as m-6. |
| 7 | Table of Contents matches actual headers | PASS | TOC lines 138-155: 16 numbered entries with anchors equal to the `## N.` headings; two additive entries `#appendix-a-document-provenance` and `#document-history` match headers at 1665 and 1692. |
| 8 | No leftover placeholders or sentinel text | PASS | Grep (case-insensitive) for `[Feature Name]`, `[Subsystem`, TODO, TBD, PLACEHOLDER, YYYY, FIXME, `[Name]`, `[Date]`, `[Team`, `[Path]`: hits only at lines 142 (TOC "Subsystem Reference"), 324 and 825 (the literal filename pattern `YYYYMMDD-HHMMSS-sweep`), 954, 1420 and 1625 (the word "placeholders" describing a gate check and allowlist tokens). All legitimate; no template placeholder remains. |
| 9 | Total line count within Standard budget 800-1,200 (more than 1,400 is blocking) | FAIL (blocking) | `wc -l` = 1,698 lines (371 blank, 1,327 non-blank); T:627-634 sets Standard 800-1,200 and says an over-ceiling document "needs editing"; the document's own Document History (line 1696) admits "about 1,700 lines ... exceeds the Standard ceiling". 1,698 is 498 over the ceiling and 298 over the 1,400 blocking threshold; this is not a modest overrun. Finding B-1. |
| 10 | No subsystem section over 200 lines | PASS | Heading-to-heading spans: 5.1 410-530 (about 120), 5.2 531-651 (about 120), 5.3 656-771 (about 115), 5.4 772-891 (about 119), 5.5 896-1026 (about 130), 5.6 1027-1108 (about 82). Largest is 5.5 at about 130 lines. (Whole Section 5 is 710 lines, 42% of the document; it is the main driver of B-1 but is not a per-subsystem breach.) |
| 11 | Section 6 under 150 lines if included | PASS | Section 6 spans 1112-1135 = 25 lines (awk span 25). |
| 12 | Document History and Appendix (Document Provenance) present | PASS | `## Appendices` (1663) with `### Appendix A: Document Provenance` (1665, source table plus assembly map); `## Document History` (1692-1696) with the 1.0 row in the template's four-column format. |

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. ("Verified" means checked with tool evidence; items 5 and 9 are verified as FAIL.)
- **Tool engagement:** Read: 5 (task item line 357, template, document 1-410, 1108-1477, 1474-1703) | Grep: 3 (all headings; section-5 bold sub-headers and rules; placeholder scan) | Glob: 0 | Bash: 4 (line counts and QA dir listing; long-line inspection of 954, 1029, 1420 and the stray separators; blank-line, span and Dependencies/Consumers format measures; frontmatter-key and subsection-heading diffs against the template). Read+Grep+Glob = 8, below the 12 checklist items; flagged as the protocol requires. The shortfall is covered by the 4 Bash verification calls (mapped to items 8, 9-11, 2 and 4) and each Read covered several items at once.
- Web research: none performed (no external claim in this lens). tavily: 0 | fallback: 0.
- Limitation, stated honestly: lines 410-1108 (Section 5 bodies) were not read line by line; only their structure (headings, bold sub-headers, table headers, span lengths) was checked. Content accuracy there belongs to the other Gate 3 lenses.

---

## Verdict: FAIL

Two blocking findings (B-1 line count, B-2 Section 14.2 columns). Everything else in the lens passes; six minor notes follow and never fail the review.

## Findings

### Blocking

**B-1. Document is 1,698 lines, over the 1,400-line blocking threshold (Standard budget 800-1,200)**
- Location: whole document; self-declared Tier "Standard" at line 60; admission at Document History line 1696.
- Evidence: `wc -l` = 1,698 (1,327 non-blank, 371 blank). Template T:627-634: Standard = 800-1,200, "If a document exceeds the tier ceiling, it needs editing - not a larger tier". Four subjects justify a modest overrun (the prompt's upper-end note), not +498 lines. Section spans: Section 5 = 710 lines (42%), Section 14 = 144, Section 2 = 86, Section 8 = 86. Document History line 1696 says the overrun "is known and accepted for now, no content was cut during assembly" and that duplicates were deliberately kept: the path/tag note blocks before Sections 1, 3, 5, 6 and 12 (lines 159, 267, 404-406, 654, 894, 1110, 1352) and the C8 pointers in 2.5 (lines 260-263) versus the table in 14.5 (1598-1608).
- Required fix: cut at least 298 lines to reach 1,400, ideally toward 1,200. Candidates with evidence of duplication or low value in a reference: (a) remove the seven repeated "Notes for ..." / path-convention blocks (159, 267, 404-406, 654, 894, 1110, 1352), keeping the single path convention at line 159; (b) delete the C8 pointer list in 2.5 (260-263) and point to 14.5; (c) fold 14.4 C "Open gaps and Gate 1 corrections" (1574-1585) into 14.4 A/B or drop the rows that restate the register; (d) delete the Appendix A assembly map (1678-1688) and the second 15.1 verification row (1625); (e) trim Section 5 (710 lines), where the largest saving must come from, by moving per-subsystem narrative that Sections 8-12 already carry (Orca verbs 8.1, caps 11.2, error handling 10.1, conventions 12.1) out of 5.1-5.5. Re-count with `wc -l` after the edit. Alternatively the owner may decide to accept the overrun, but under the stated rule that is a decision for the owner, not a pass.

**B-2. Section 14.2 Technical Debt table drops the template's Severity and Effort to Fix columns**
- Location: lines 1498-1514 (header line 1502 `| Item | Research label | Description | Evidence |`); template T:561-563 (`Item | Severity | Description | Effort to Fix`).
- Evidence: line 1500 states "No research file rates severity or effort, so those template columns are not invented; the research label is shown instead." The substitute columns (Research label, Evidence) are not equivalents: "dead code", "untested risk", "fact" are not High/Medium/Low, and no T-shirt size appears anywhere in the table. The omission is disclosed and honest, but the lens rule counts a table that loses required columns as blocking.
- Required fix (needs no invented data): restore the template header `Item | Severity | Description | Effort to Fix` and put the literal text "not rated" in Severity and Effort for each row; move "Research label" and "Evidence" into the Description cell (for example "dead code. Evidence: view.py:331, 402"). Keep the line-1500 sentence.

### Minor (notes only; never fail the review)

- **m-1. 8.1 column structure adapted (line 1149).** Template T:406 has `Endpoint | Method | Purpose | Request Shape | Response Shape`; the document uses `Tool | Binary | Verb and argv template | Purpose | Status | Source` because these are CLI verbs, not HTTP endpoints. Equivalent content for request shape (argv template) is present; response shape is covered in 5.1 and the 8.2 "File formats" table. A one-line note under the heading saying the columns are adapted for CLI verbs would remove the doubt.
- **m-2. 12.1 uses `Evidence` instead of `Example` (line 1358).** Template T:511 `Convention | Description | Example`. Citations are given, examples are mostly inside Description. Cosmetic.
- **m-3. Header wording.** 11.1 uses `Value` for template `Measured Value` (line 1315); 2.3 appends "(design or docs)" to `TDD Divergence` (line 225). Cosmetic.
- **m-4. Template header block "Tiered Usage" table is not carried (grep count 0).** Document Lifecycle Position is present (68-74) and the tier is stated once at line 60. Cosmetic.
- **m-5. 5.6 Dependencies and Consumers are prose (lines 1097, 1099) where 5.1-5.5 use the template tables.** Minor inconsistency inside Section 5.
- **m-6. Two tensions between header claims and the log.** Document Information line 88 says "Last Verified Against Code: 2026-11-20" while 15.1 line 1625 says the assembly pass did no source re-read and QA is pending (line 122). The scaffolding note blocks (159, 267, 404-406, 654, 894, 1110, 1352) and Section 15/Appendix text refer to "research 0N", "GF-n", "synthesis brief", "Line budget: the synthesis brief asked for about 160 lines" (line 1352) which a reader of the finished reference does not have; the template's content rule "state key numbers once in Section 1" (T:645) is also not followed (counts recur in 2.2, 2.5, 3.1, 11.3). Also note: the file name `OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md` is upper-case while the template's naming comment (T:650-655) wants lowercase kebab-case; the path is dictated by OUTPUT_PATH, so no finding.

## Summary

- Checks passed: 10 / 12 (items 1, 2, 3, 4, 6, 7, 8, 10, 11, 12)
- Checks failed: 2 (items 5 and 9)
- Blocking findings: 2 (B-1, B-2). Minor notes: 6 (m-1 to m-6).
- Issues fixed in place: 0 (fix_authorization: false; the document was not modified).

## Recommendations

1. Cut the document by at least 298 lines (B-1) before the next review round; the quickest large wins are the repeated note blocks, the duplicate C8 pointers, 14.4 C and the Appendix assembly map, then Section 5 overlap with Sections 8-12.
2. Restore the Severity and Effort to Fix columns in 14.2 with "not rated" values (B-2).
3. Minor notes m-1 to m-6 may be fixed in the same pass but are not rechecked.

## QA Complete

