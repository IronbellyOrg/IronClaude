# QA Report — Internal Consistency Lens (Lens 2 of 6)

**Topic:** sc-persona-research-protocol SKILL.md
**Date:** 2026-04-30
**Phase:** skillcreate-internal-consistency
**Fix authorization:** false (REPORT ONLY)

## Overall Verdict: FAIL

Inconsistent with section classification table at multiple structural levels. Most critical: only 9 of 29 sections (S21-S29) carry canonical numbered headers; S1-S20 use unnumbered topical headers. S19 (COPY) has heading drift. S18 (A.8) is missing entirely.

## Items Reviewed (19 checks)

- Checks passed: 13 / 19
- Checks failed: 6
- CRITICAL: 2 | IMPORTANT: 4 | MINOR: 0

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Lines 6-1413 (S1-S20) | 20 of 29 sections lack canonical numbered headers. Only S21-S29 (lines 1415, 1486, 1546, 1569, 1606, 1691, 1732, 1798, 1825) are numbered. SECTION_COUNT_29 self-check (line 1661) requires 29 — actual 9. | Renumber every section header from S1 through S29 to match canonical `## N. SectionName` pattern. |
| 2 | CRITICAL | Between line 513 and 515 | S18 (A.8 Receive & Verify Task File) classified COPY is missing as standalone section. Tech-research has A.8 at lines 450-461. Persona-research jumps directly from A.7 close (line 513) to Stage B header (line 515). §22.1 mapping (line 1507) enumerates "S18 Stage A Output | tech-research S18 boilerplate | COPY" — unfulfilled. | Insert A.8 (Receive & Verify the Task File) block from tech-research/SKILL.md L450-461 verbatim between L513 and L515 with persona-research-specific verification points. |
| 3 | IMPORTANT | Line 515 | S19 header has suffix `(Delegation Protocol)` not in tech-research line 465. Line 517 inserts a preamble paragraph not in tech-research. | Remove `(Delegation Protocol)` suffix; remove or relocate preamble paragraph at line 517. |
| 4 | IMPORTANT | Lines 390-412 (A.5) | S16 classified COPY but body criteria are persona-research-specific (SUBJECT_ROSTER, ARCHETYPE_RESOLUTION_STRATEGY, ETHICS_ATTESTATION, Guard G1/G4) — SUBSTITUTE-level customization mislabeled as COPY. | Reclassify S16 as SUBSTITUTE in 12-section-classification.md OR restore tech-research's generic 6-criteria body. Recommend reclassify. |
| 5 | IMPORTANT | Line 218 | "(per skill-creator architecture):" — bare reference-skill noun in body prose of §10 (GENERATE). Flagged by skill's own Source-Fidelity rule (line 1401). | Replace with citation form, e.g., "(per RF 3-gate QA architecture)". |
| 6 | IMPORTANT | Frontmatter | No `allowed-tools` field. S1 classification requires tightly scoped per guide line 79. Critical Rule 14 also calls for it. | Add `allowed-tools` listing only tools needed (Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch, MCP Tavily). |

## Confidence: 100% | Tool engagement: Read=9, Grep=4, Bash=4

## QA Complete
