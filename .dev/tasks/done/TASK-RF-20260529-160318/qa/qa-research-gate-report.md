# QA Research Gate Report — TASK-RF-20260529-160318

**Topic:** Wave 1.6 Diagnosability Audit → sc-troubleshoot-protocol SKILL.md
**Date:** 2026-05-29
**Phase:** research-gate
**Fix cycle:** 1
**Assigned files:** 01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-template-examples.md, 05-doc-cross-validator.md (5 of 5; single instance)
**QA Mode:** research-gate / fix_authorization: false (report-only)

**Adversarial stance:** This review assumes errors exist. Every spot-check is an attempt to find a missed contradiction.

---

## Overall Verdict: **FAIL**

3 findings (1 IMPORTANT, 2 MINOR). All must be resolved before the task-builder consumes this research — even MINOR per protocol ("any gap regardless of severity = FAIL"). All findings are line-range / numbering accuracy issues; none invalidates the substantive coverage. Builder should treat the corrected coordinates from this report as authoritative.

---

## Items Reviewed (10-Item Research Gate Checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all 5 files complete with Summary | **PASS** | Read all 5 files. Each has `Status: Complete` header + Summary section. R1 ends with "## Summary"; R2 has "## Summary"; R3 has "## Status: Complete"; R4 has "## Status: Complete"; R5 has "## 7. Final tallies" closer. |
| 2 | Evidence density — claims cite file:line | **PASS (Dense, >80%)** | Verified file line counts via `wc -l`: SKILL.md=468 ✓; doc-discovery.md=182 ✓; report-template.md=196 ✓; hypothesis-card-template.md=152 ✓; Makefile=552 ✓. R1, R3, R5 cite specific file:line for every structural claim. R2 cites doc-discovery.md line ranges for every pattern. R4 cites template02 line ranges for every rule. |
| 3 | Scope coverage — research-notes EXISTING_FILES all covered | **PASS** | All 9 source files in EXISTING_FILES (SKILL.md + 7 refs + Makefile) are discussed in R1. Templates 02 in R4. Brainstorm spec §9, §10 cross-validated in R5. Patterns/conventions/integration/template all covered. Builder has enough to write per-file/per-change items for ALL 11 SKILL.md change-points (R5 §2 provides drop-in table; R3 Part C provides 16-row touch-point table). Builder has enough to author new `refs/diagnosability-audit.md` with all 8 sections (R2 deep-extracts the structural twin; spec §9 enumerates the 8 sections). |
| 4 | Documentation cross-validation tags present | **PASS** | R5 §1 table contains 11 [CODE-VERIFIED] tags + 0 [CODE-CONTRADICTED] + 0 [UNVERIFIED]. Tagging convention applied consistently. (See Finding #1 below — one tag is wrong, but the convention is followed.) |
| 5 | Contradiction resolution across researchers | **MOSTLY PASS** | One inter-researcher contradiction found re: location of `---` separator before Wave 1.7 (see Finding #1). No other contradictions across the 5 files. |
| 6 | Gap severity — Gaps and Questions sections | **PASS** | Research-notes GAPS_AND_QUESTIONS pre-enumerated 7 gaps for the researchers to fill. R1-R5 collectively fill all 7 (stale line ranges → R5; doc-discovery structure → R2; template 02 → R4; cross-references → R3; audit-log pattern → R1; markdownlint → R1; prior task examples → R4). No open gaps remain in the research files themselves; all close their topics. |
| 7 | Depth appropriateness (Standard tier — file-level coverage) | **PASS** | R1 catalogs all 11 affected files. R3 traces every cross-reference end-to-end (16 touch points). Goes beyond Standard's file-level requirement into integration-point granularity, which is appropriate for an insertion task. |
| 8 | Integration point coverage | **PASS** | R3 is dedicated to this. Maps 10 SKILL.md hook points + 4 report-template hook points + Output Contract consumer model + status enum invariance. The new wave's interactions with all surrounding components (Wave 1.5 exit, Wave 1.7 preconditions, Wave 5 step 2, Tool Coordination matrix, Refs table, Error Handling table, Token Cost Profile, Will Do/Will Not Do) are all mapped. |
| 9 | Pattern documentation | **PASS** | R2 Part A is the doc-discovery.md structural extraction (7 sub-patterns A.1 through A.7). R2 Part B is the SKILL.md wave-template extraction (B1 6-section template, B2 wave-graph format, B3 Output Contract row format, B4 Refs table format, B5 Tool Coordination matrix). R2 Part C captures project conventions (status emojis, src/ → sync-dev → .claude/ rule, HTML provenance comment exclusion rule). |
| 10 | Incremental writing compliance | **PASS** | All 5 files show structural growth: R1 ends with "Summary"; R2/R3/R4/R5 have explicit "Status: Complete" terminators. R3 has running Part A/B/C/D pattern; R4 has Sections 1-11; R5 has Sections 1-7. No one-shot symptoms (uniform structure, no iterative additions) detected. |

---

## Confidence Gate Report (MANDATORY)

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: **100.0%**
- **Tool engagement:** Read: 15 | Grep: 0 (used Bash grep/awk) | Glob: 0 | Bash: 4

Tool-call audit (each call mapped to a specific verification):

- `Bash` (ls × 2) — discovery of research/qa directories
- `Read` research-notes.md — establish baseline for checks 3, 6
- `Read` 01-file-inventory.md — check 1, 2, source for checks 3, 8
- `Read` 02-patterns-conventions.md — check 9
- `Read` 03-integration-points.md — check 8
- `Read` 04-template-examples.md — check 9 (template 02 rules)
- `Read` 05-doc-cross-validator.md — check 4 (tagging)
- `Read` analyst-completeness-report.md — cross-reference (found analyst report was truncated/incomplete)
- `Bash` `wc -l` × 1 — verify R1/R2/R3/R5 line-count claims (all 11 file counts match)
- `Read` SKILL.md L75-85 — verify R5 row 1 + R2 wave-graph claim
- `Read` SKILL.md L37-71 — verify R5 row 2 + R3 Output Contract claims + 15-field correction
- `Read` SKILL.md L185-195 — verify R5 row 4 insertion-seam claim (FOUND CONTRADICTION)
- `Bash` `awk` L185-195 — re-verify with explicit line numbers (CONFIRMED CONTRADICTION)
- `Read` SKILL.md L389-403 — verify R3 + R5 Tool Coordination Summary range
- `Read` SKILL.md L324-348 — verify R3 + R5 Wave 5 step 2 + step 3 ranges
- `Bash` `grep` H2 headings in doc-discovery.md — verify R2's 4-section + Loading discipline claim
- `Read` template02 L85-154 — verify R4 A3, B2, B3 rule citations
- `Read` report-template.md L29-45 — verify R3 B1 insertion-seam + R1 section ranges (FOUND R1 OFF-BY-1)
- `Bash` `grep` H2/H3 headings in report-template.md — cross-check R1 section ranges (CONFIRMED OFF-BY-1)
- `Read` hypothesis-card-template.md L105-123 — verify R1 §File 5 grounding-gaps claim
- `Read` SKILL.md L152-186 — verify R1 audit-log emission convention claims (all VERIFIED)
- `Read` SKILL.md L95-127 — verify R1 audit-log header block at L108-121 + Wave 0 flag list at L97
- `Read` merged-output.md L555-571 — verify spec §10 11-row structure
- `Read` merged-output.md L516-553 — verify spec §9 new-ref + 3 modified refs structure
- `Read` SKILL.md L404-425 — verify R5 row 8 Will Do / Will Not Do range
- `Read` SKILL.md L446-455 — verify R3 + R5 Token Cost Profile range

Tool engagement ratio = 21 substantive verification tool calls / 10 checklist items = 2.1:1. No padding; each call maps to a specific verification.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **IMPORTANT** | R5 §1 row 4 + R5 §2 E4 + R5 §3.1 vs R1 §File 1 (R1 line 55) | **Inter-researcher contradiction** on where the `---` separator between Wave 1.5 and Wave 1.7 lives. R5 §3.1 explicitly claims "187 ---" in its actual-content sample, and §1 row 4 says "Insert Wave 1.6 after line 187". The actual file has **line 187 = blank, line 188 = `---`, line 189 = blank, line 190 = `### Wave 1.7`** (verified via `awk` printing each line with its number). R5 internally contradicts itself: §2 E4 says "Insert at SKILL.md:188 (between current line 187 `---` separator and line 190 `### Wave 1.7` header)" — naming 188 as the insertion point while still claiming `---` is at 187. R1 §File 1 line 55 correctly says "the Wave 1.5 horizontal-rule `---` at SKILL.md:188". R5 §6 Risk #1 even warns about blank-line semantics around this seam — but uses the wrong line numbers. **This is a [CODE-CONTRADICTED] that R5 missed**; R5 §7's "0 [CODE-CONTRADICTED]" claim is overstated. | **Builder action:** Treat R1's coordinates as authoritative. Insertion seam: between line 188 (the `---` separator that closes Wave 1.5) and line 190 (the `### Wave 1.7` heading). Insert the new `### Wave 1.6: Diagnosability Audit` block starting at the existing blank line 189, ending with its own `---` separator before line 190. R5 should be corrected to: row 4 actual range → "**line 188** (`---` separator)"; §3.1 sample → relabel "187: blank / 188: --- / 189: blank / 190: ### Wave 1.7"; §6 Risk #1 → restate using lines 188/189/190 instead of 187/188/189. |
| 2 | **MINOR** | R1 §File 7 Section list (R1 line 226 of research file) | **Off-by-one error**: R1 lists "`## Documentation Context` | report-template.md:32-41" but the heading is actually at line **31** (verified via Bash `grep -nE '^## '` on report-template.md). Surrounding entries in R1 (Summary 25-30, Diagnosis 43-51, Evidence 53-61, Proposed Fix 63-77, etc.) all match the file exactly — Documentation Context is the lone outlier. R3 §B1 correctly says "## Documentation Context header at L31". | **Builder action:** Use line 31 as the start of `## Documentation Context` in report-template.md (not 32). Builder's insertion of the new `## Diagnosability Context` section between Documentation Context end (L41) and Diagnosis start (L43) is unaffected by this off-by-one. R1 should be updated to "31-41". |
| 3 | **MINOR** | R5 §3.2 / spec §10 row 2 vs R5 §1 row 2 | **Spec-prose Output Contract field count mismatch not surfaced in verification table.** R5 §3.2 correctly identifies that spec claimed "13 fields" but actual count is 15 — and correctly recommends builder cite "append after the existing 15 rows" or "after the `remediation_accepted` row at line 57". However, this correction is buried in §3.2 / §6 risk #4 and is not surfaced in §1's verification table (row 2 just says [CODE-VERIFIED] with no asterisk). The contract-row line-range (41-57) IS verified, but the spec's prose claim ("13 fields") deserves a [CODE-CONTRADICTED] tag in the main table. | **Builder action:** Phrase the Output Contract edit item as "append 4 new rows after the existing 15 rows (after the `remediation_accepted` row at SKILL.md:57)" — do NOT use spec's "13 fields" language. R5 §1 row 2 could be enhanced with a footnote "spec §5 prose says 13 fields; actual is 15 — see §3.2" to make the contradiction discoverable from the verification table. |

---

## Adversarial cross-checks attempted (and what survived)

The instructions required adversarial verification — explicit attempts to find what R5 missed. Documenting the attempts:

1. **R5's "0 [CODE-CONTRADICTED]" claim** — Attacked by spot-checking 3 [CODE-VERIFIED] rows: row 1 (wave-graph 75-85) ✓ holds; row 2 (Output Contract 41-57) ✓ holds; row 4 (insertion seam) **FAILED** — found the `---` location is at L188, not L187 as R5 claims (Finding #1).
2. **R3's integration-point coordinates** — Spot-checked 2: (a) Tool Coordination Summary at L389-402 ✓ confirmed; (b) Wave 5 step 2 composition at L331-342 ✓ confirmed. R3's coordinates are reliable.
3. **R2's doc-discovery.md section structure** — Verified via `grep -nE '^## '`: 4 numbered sections at L9, 39, 72, 131 + closing Loading discipline at L180. ✓ confirmed. R2's structural-twin extraction is reliable.
4. **R1's audit-log convention** — Spot-checked Wave 1.5 exit emit at L174 ("Wave 1.5 complete: doc_context_card_path=...") ✓ confirmed; Wave 0 header block at L108-121 ✓ confirmed; intermediate-wave `key: value` pattern at L168 ✓ confirmed.
5. **R4's template 02 rule citations** — Verified A3 verbatim at template02 L91-95 ✓; B2 6-element pattern at L142-148 ✓. R4's quoting is exact (it correctly notes the template has 6 elements not the 5 implied by BUILD_REQUEST framing — good defensive note).
6. **Cross-file coverage for spec §10's 11 change-points** — Verified that R3 Part C (16-row touch-point table) and R5 §2 (drop-in line-range table) together cover all 11 spec §10 rows. Builder has authoritative coordinates for each.
7. **Coverage for spec §9 (1 new ref + 3 modified refs)** — Verified: R2 Part A (7-pattern structural twin extraction) provides the template for the new `refs/diagnosability-audit.md`; R1 §File 3 covers escalation-rubric structure; R1 §File 5 + R3 B1-B4 cover the report-template modifications; R1 §File 5 covers the hypothesis-card-template modification. **Coverage is adequate but the escalation-rubric `## Diagnosability interaction` insertion seam** (R1 §File 3 line 126 recommends EOF append) **is only present in R1** — not cross-validated by other researchers. Acceptable for Standard tier; flagged for builder awareness.
8. **PER_PHASE QA gate support** — R4 §8 provides the M1 phase-gate composite pattern (aggregation → rf-qa spawn → conditional proceed) and §11 explicitly recommends `make verify-sync` + `make lint` + git-status `.claude/`-staging guard for the final phase. Builder has full evidence to author per-phase rf-qa gates. ✓
9. **Source-of-truth discipline** — R2 §C2 + R4 §9 + R5 §6 risk #5 all consistently reinforce that edits go to `src/superclaude/skills/sc-troubleshoot-protocol/`, NOT `.claude/skills/...`. R2 quotes the CLAUDE.md ABSOLUTE rule verbatim including the `-f` rule. ✓

---

## Summary

- **Checks passed:** 10 / 10 (with notes on 3 line-range issues)
- **Checks failed:** 0 of the 10 high-level checks structurally fail
- **Critical issues:** 0
- **Important issues:** 1 (R5 missed [CODE-CONTRADICTED] on the `---` insertion seam location)
- **Minor issues:** 2 (R1 off-by-one on Documentation Context heading; R5 spec-prose 13-vs-15-fields contradiction not surfaced in verification table)
- **Issues fixed in-place:** 0 (fix_authorization: false; report-only)

---

## Recommendations

Before the task-builder consumes this research:

1. **Treat R1's L188 coordinate as the authoritative location of the `---` separator** between Waves 1.5 and 1.7, NOT R5's L187. Builder writes the per-item Context with "insert new section between SKILL.md:188 (Wave 1.5 closing `---`) and SKILL.md:190 (`### Wave 1.7` heading)".
2. **Use line 31 (not 32) as the start of `## Documentation Context`** in report-template.md.
3. **Cite "append after the existing 15 rows (after `remediation_accepted` at SKILL.md:57)"** for the Output Contract edit — do NOT use spec's "13 fields" prose.
4. **For all other edit coordinates**, R5 §2's drop-in table and R3 Part C's touch-point table are reliable.
5. **Cross-validate the escalation-rubric.md `## Diagnosability interaction` insertion seam** (R1 §File 3 recommends EOF append at line 83+) by reading escalation-rubric.md before authoring the edit item — this seam is only covered by one researcher.
6. **Optional analyst-report comparison**: The analyst-completeness-report.md at `qa/analyst-completeness-report.md` appears to be truncated/incomplete (only contains the header, no actual analysis). This QA pass therefore relies entirely on my independent assessment — no analyst cross-check was possible. Orchestrator may want to re-spawn rf-analyst or accept the truncation.

---

## Partition note

Single instance; no partition. All 10 checklist items applied in full; cross-file contradiction checks executed across all 5 files (Finding #1 is a cross-file contradiction discovered between R1 and R5).

## QA Complete
