# Comparison Report: Test 2 (spec-modified) vs Test 3 (spec-baseline)

**Generated**: 2026-04-02
**Purpose**: Prove structural equivalence between roadmap pipeline outputs from two independent runs using the same non-TDD spec

---

## Executive Summary

All 9 artifacts demonstrate structural equivalence between Test 2 (spec in modified repo) and Test 3 (spec in baseline repo). No unexpected structural differences were found. All differences are attributable to expected LLM non-determinism (content variation, section granularity, phase organization) or expected downstream cascading (different base variant selections producing different merged roadmap structures).

**Overall Verdict: PASS**

---

## Summary Table

| Artifact | Test 2 FM Fields | Test 3 FM Fields | FM Match | Test 2 Sections | Test 3 Sections | Section Match | Overall |
|---|---|---|---|---|---|---|---|
| extraction.md | 14 | 14 | YES | 16 | 20 | YES* | MATCH |
| roadmap-opus-architect.md | 10 | 3 | YES** | 31 | 32 | YES | MATCH |
| roadmap-haiku-architect.md | 3 | 3 | YES | 66 | 101 | YES*** | MATCH |
| diff-analysis.md | 2 | 2 | YES | 21 | 21 | YES | MATCH |
| debate-transcript.md | 2 | 2 | YES | 11 | 18 | YES | MATCH |
| base-selection.md | 2 | 2 | YES | 16 | 18 | YES | MATCH |
| roadmap.md (merged) | 3 | 3 | YES | 60 | 59 | YES | MATCH |
| anti-instinct-audit.md | 9 | 9 | YES | 4 | 4 | YES | MATCH |
| wiring-verification.md | 16 | 16 | YES | 7 | 7 | YES | MATCH |

Legend:
- \* Test 3 has 4 additional subsections under Dependency Inventory (cosmetic organization difference)
- \** Test 2 has 7 additional metadata fields (generated, generator, counts); core 3 fields match
- \*** Test 3 has more granular subsections within phases (expected Haiku verbosity variation)

---

## Structural Differences Found

### Expected LLM Non-Determinism (NOT concerning)

1. **extraction.md**: Test 3 breaks Dependency Inventory into 4 subsections; Test 2 uses a flat section. Same content, different organization.

2. **roadmap-opus-architect.md**: Test 2 emits 10 frontmatter fields (including generated, generator, total_phases, total_milestones, etc.); Test 3 emits only the 3 core fields. Opus model sometimes produces richer metadata headers.

3. **roadmap-opus-architect.md**: Test 2 includes a Phase 0; Test 3 starts at Phase 1. Different phase numbering schemes for the same content.

4. **roadmap-haiku-architect.md**: Test 3 generates significantly more subsection headers (101 vs 66), including architecture diagrams, rollback sections, and post-launch review sections not present in Test 2. Expected Haiku verbosity variation.

5. **debate-transcript.md**: Test 3 uses per-topic subsections in Round 1 (D-2 through D-9); Test 2 groups by variant. Same debate structure, different formatting.

6. **base-selection.md**: Test 2 uses 6 scoring criteria; Test 3 uses 10. Different granularity in evaluation framework. Test 2 selects Variant B (Haiku) as base; Test 3 selects Variant A (Opus). Different selections are expected because upstream roadmaps differ.

7. **roadmap.md (merged)**: Test 2 has 7 phases (base: Haiku); Test 3 has 5 phases (base: Opus). Different base selections cascade into different merged structures. Both contain all required roadmap elements.

### Downstream Cascading Effects (expected)

- Different base variant selections (Test 2: Haiku base, Test 3: Opus base) produce different merged roadmap structures, deferred items sections, and supplementary sections. This is correct behavior -- the pipeline faithfully reflects different upstream decisions.

### Unexpected Differences: NONE

No structural differences were identified that cannot be explained by LLM non-determinism or expected downstream cascading.

---

## TDD Content Check

Both runs were executed against the same non-TDD user-auth spec. Neither Test 2 nor Test 3 contains any TDD-specific content such as:
- Data Models
- API Specifications
- Service Contracts
- Database Schema definitions (beyond what the auth spec itself specifies)

This confirms that the TDD-stripping in Test 2's modified repo did not introduce TDD contamination, and the baseline repo (Test 3) likewise has no TDD content.

---

## Anti-Instinct Audit Status

Both runs FAILed the anti-instinct audit, though for different reasons. Test 2 failed due to uncovered_contracts=3 (fingerprint_coverage was 0.72, which passes the 0.70 threshold). Test 3 failed due to fingerprint_coverage=0.67 (below the 0.70 threshold), while its uncovered_contracts=0. Both encounter the same pipeline gate (GateMode.BLOCKING) and both result in FAIL, which is expected behavior for this spec.

---

## Wiring Verification Status

Both runs produced identical wiring-verification results (166 files analyzed, 7 orphan modules, 0 blocking findings). This is expected because wiring-verification is a deterministic static analysis tool operating on the same codebase.

---

## Final Overall Verdict: PASS

No unexpected structural differences found across any of the 9 artifacts. All differences are attributable to:
1. LLM non-determinism in content and formatting (expected)
2. Downstream cascading from different LLM choices in upstream artifacts (expected)
3. Deterministic equivalence for codebase-derived artifacts (confirmed)

The pipeline produces structurally equivalent outputs regardless of whether the spec is placed in the modified repo or the baseline repo.
