# QA Report — Skillcreate Template-Conformance (Lens 1 of 6)

**Topic:** sc-persona-research-protocol SKILL.md template conformance
**Date:** 2026-04-30
**Phase:** skillcreate-template-conformance
**Lens:** template-conformance
**Fix authorization:** false (REPORT ONLY)

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result |
|---|-------|--------|
| 1 | Section presence and ordering | FAIL — section-naming convention switches mid-document; S1-S20 use plain canonical names, S21-S29 use numeric S-prefix. Canonical reference (tech-research) uses pure section names throughout. |
| 2 | YAML frontmatter validity | PASS-WITH-CAVEAT — frontmatter parses; trigger phrases embedded in description. `allowed-tools` field absent (canonical also omits). |
| 3 | Template comment removal | PASS — zero HTML comments remain. |
| 4 | Content rules compliance | FAIL — S21.1 schema block at lines 1428-1456 lists `## 1.` through `## 29.` but document does not have those literal headers. Schema-as-described diverges from schema-as-implemented. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Lines 1415-1825 (S21-S29) | Numeric S-prefix headers ("## 21. Output Structure" through "## 29.") inconsistent with canonical (no numeric prefix). S1-S20 use plain names. | Either remove numeric prefix from S21-S29 OR add numeric prefixes to S1-S20. Canonical pattern is plain names. |
| 2 | IMPORTANT | S25.3 self-validation (line 1651) | Skill's own SECTION_COUNT_29 check (`grep -c '^## [0-9]\+\. '` should return 29) cannot be satisfied; only 9 numbered headers exist. | Revise S25.3 to drop the regex (use level-2 + level-3 count) OR restructure document to have 29 numbered headers. |
| 3 | MINOR | Lines 1419-1457 (S21.1 schema block) | Schema lists 29 sections as `## 1.` through `## 29.`, but document doesn't have "## 1. Skill Overview". Self-contradiction. | Revise schema to match actual section names, OR clarify schema is logical mapping not literal headers. |
| 4 | MINOR | Frontmatter | No `allowed-tools` field. Critical Rule 14 calls for tightly-scoped allowed-tools. | Add `allowed-tools` listing only tools actually used. |

## Confidence: 100% | Tool engagement: Read=6, Grep/Bash=7

## QA Complete
