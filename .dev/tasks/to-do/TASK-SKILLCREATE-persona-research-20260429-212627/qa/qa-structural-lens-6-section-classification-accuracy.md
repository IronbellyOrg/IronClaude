# QA Report — Section Classification Accuracy Lens (Lens 6 of 6)

**Topic:** sc-persona-research-protocol SKILL.md
**Date:** 2026-04-30
**Phase:** skillcreate-section-classification-accuracy
**Fix authorization:** false (REPORT ONLY)

## Overall Verdict: FAIL

Multiple cross-section contradictions, internal inconsistency between Phase 7 references, folder-name inconsistencies across S4/S9/S20.

## Items Reviewed

| # | Check | Result |
|---|-------|--------|
| 1 | Phase structure coherence (S10 ↔ A.7) | PARTIAL FAIL — internal consistency S10↔A.7 PASSES (matching L0/L1/L1/L4/L2/L0/L4); checklist's prescribed L0/L1/L4/L2/L4/L6/L0 mismatch. |
| 2 | Nesting logic correctness (AGENT_FILES gate, no rf- prefix, sequential, error handling) | FAIL — AGENT_FILES not referenced in Phase 7 of A.7. Phase 7 in this skill is "Optional Validator", not agent-creator nesting. Critical Rule 3 boilerplate leak. |
| 3 | Cross-section consistency | FAIL — multiple agent roster + folder name contradictions. |
| 4 | Section label verification (COPY/SUBSTITUTE/GENERATE) | PARTIAL FAIL — GENERATE sections have substantive content; numbering style inconsistent. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | S14 (line 312-319) ↔ S20 (lines 620, 693, 736, 858, 950, 1018) | Agent roster mismatch. S14 lists Approval Gate as agent type; S20 has Archetype Matcher prompt instead. Approval Gate is a halt point not a spawned agent. | Reconcile rosters: add Archetype Matcher to S14 table and remove Approval Gate (it's a phase, not an agent). |
| 2 | CRITICAL | S20 Aggregator (lines 956-957) vs S4 (line 41) vs S9 (lines 171, 177) | Folder name contradiction: S4 declares `synthesis/`, S20 Aggregator output is `aggregation/`. | Standardize: pick one folder name and use uniformly across S4, S9, S20. |
| 3 | CRITICAL | S4 (line 46) vs S9 (line 176) vs S20 Discovery Worker (line 865) vs S28 (line 1820) | Three different archetype folder names: `archetypes/`, `archetype-proposals/`, and `archetype_store.local_path`. | Standardize on one (recommend `archetype-proposals/`); update all references. |
| 4 | IMPORTANT | S10 phase table (lines 209-216) vs checklist's expected L-level | Checklist expects `L0/L1/L4/L2/L4/L6/L0`; document encodes `L0/L1/L1/L4/L2/L0/L4`. | Resolve with orchestrator: correct document L-levels to match checklist OR update checklist's expected mapping. |
| 5 | IMPORTANT | Critical Rule 3 (line 1740) | "Phase 7 agent-creator nests are sequential (interactive)" — leftover skill-creator boilerplate. Phase 7 in this skill is "Optional Validator". | Remove agent-creator reference from Rule 3 or replace with persona-research-Validator-specific guidance. |
| 6 | IMPORTANT | Lines 14, 54, 144 (unnumbered) vs lines 1415, 1486 (numbered) | Inconsistent section numbering. S2-S20 unnumbered, S21-S29 numbered. | Renumber S1-S20 to match `## N.` pattern OR update S25.3 SECTION_COUNT_29 check. |
| 7 | IMPORTANT | S20 Identity Verifier (line 691) vs §5.2 contract (lines 808-847) | Identity Verifier output schema includes `ethics_screen` field; §5.2 worker contract `identity_verification` block omits it. | Reconcile: add `ethics_screen` to §5.2 OR remove from Identity Verifier output. |
| 8 | MINOR | S25.3 line 1654 | ETHICS_DISCLAIMER_VERBATIM count exactly 3 — tight; future deletion would break. | Consider relaxing threshold to "≥2 times" or making locations explicit. |
| 9 | MINOR | S16 (lines 390-412) | Classified COPY but content has persona-research-specific items (ethics attestation, Guard G1/G4) — SUBSTITUTE-grade. | Reclassify S16 as SUBSTITUTE (matches reality). |

## Confidence: 100% | Tool engagement: Read=5, Grep=1, Bash=2

## QA Complete
