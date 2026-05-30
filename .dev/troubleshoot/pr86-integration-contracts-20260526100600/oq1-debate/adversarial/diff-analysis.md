# Diff Analysis — OQ-1 Resolution Options

## Metadata

- Generated: 2026-05-26T13:42:00Z
- Variants compared: 3
- Variant 1: Option A (test-only fix)
- Variant 2: Option B (helper uppercases input — qa-qualitative's recommendation)
- Variant 3: Option C (modify `_extract_identifiers` itself)
- Focus areas: correctness, test-coverage, scope-discipline
- Depth: quick (Round 1 only; no Round 2 rebuttals; no Round 2.5 invariant probe)

## Structural Differences (taxonomy: L1 surface)

| # | Area | V1 (A) | V2 (B) | V3 (C) | Severity |
|---|------|--------|--------|--------|----------|
| S-001 | Number of files modified | 1 (test only) | 2 (helper + test) | 1 (production helper region) | Low |
| S-002 | Acknowledges incompleteness | YES (explicit) | NO (claims complete) | YES (explicit — says "STILL MISSING `S10`") | Low |

## Content Differences (taxonomy: L3 state-mechanics)

| # | Topic | V1 (A) | V2 (B) | V3 (C) | Severity |
|---|-------|--------|--------|--------|----------|
| C-001 | Test 1 strategy | Wrap with `_canonicalize_identifiers` | Wrap with `_canonicalize_identifiers` (same as A) | Test 1 unchanged | Medium |
| C-002 | Test 2 lowercase input handling | Helper unchanged → Test 2 FAILS | Helper `text.upper()` → Test 2 PASSES | Helper unchanged → Test 2 FAILS (even with C's regex change to `_extract_identifiers`) | **High** |
| C-003 | `_extract_identifiers` modification | NO | NO | YES (adds 3rd regex line) | High |
| C-004 | Scope of canonicalization | Test-side only | Helper boundary (input + output) | Extractor itself | High |
| C-005 | All 4 pin tests pass post-fix? | NO (Test 2 fails) | **YES** (verified by trace) | NO (Test 2 still fails) | **High** |

## Contradictions

| # | Conflict | V1 position | V2 position | V3 position | Impact |
|---|----------|-------------|-------------|-------------|--------|
| X-001 | Is the helper's stated invariant 1 ("All tokens are uppercase") satisfied for lowercase input? | Implicitly weakens it — input case asymmetry | Honors it uniformly via `.upper()` | Implicitly weakens it — extractor returns uppercase only via its case-sensitive regex | High — directly contradicts the docstring contract |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V2 (B) | The ONLY option that satisfies all 4 pin tests with a single change (1 word: `.upper()`) | High |
| U-002 | V3 (C) | Surfaces that even modifying `_extract_identifiers` to add hyphenation doesn't fix Test 2's case issue — proves case-canonicalization must happen at the helper boundary | Medium-High |
| U-003 | V1 (A) | Surfaces that the underlying problem isn't a single fix — it's a contract-level decision about WHERE canonicalization belongs | Medium |

## Shared Assumptions

| # | Assumption | Classification |
|---|-----------|----------------|
| A-001 | The 4 pin tests are correctly written and reflect the intended invariants — none of the options propose changing what the tests assert | STATED (all 3 frame their work as "make the tests pass", not "rewrite the tests") |
| A-002 | `_extract_identifiers` is a public contract that should be preserved if possible | STATED (all 3 acknowledge this; A and B respect it, C violates it) |
| A-003 | The helper's docstring invariant 1 ("All tokens are uppercase") is normative, not aspirational | UNSTATED — V1 and V3 implicitly weaken it; V2 implicitly honors it. **Promoted to debate point.** |

## Summary

- Total differences: 5 content + 2 structural + 1 contradiction + 3 unique + 1 promoted assumption = **12**
- Highest-severity items: C-002 (Test 2 lowercase handling — only B passes), C-005 (only B passes all 4 pin tests), X-001 (only B honors the docstring contract)
- Diff density adequate for debate (no "variants too similar" skip path).
