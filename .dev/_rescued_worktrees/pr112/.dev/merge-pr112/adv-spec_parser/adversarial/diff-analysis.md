# Diff Analysis: Merge-Conflict Resolution Comparison (spec_parser.py Requirement-IDs region)

## Metadata
- Generated: 2026-06-04
- Variants compared: 3 (V1=proposed_hybrid, V2=ours_only, V3=theirs_only)
- Mode: A (compare existing files)
- Depth: quick (Round 1 only)
- Total differences found: 3 substantive diff points
- Categories: structural (1), content (2), contradictions (0), unique (0), shared assumptions (1)

## Context
Both V2 (ours/HEAD) and V3 (theirs/master) independently ported the SAME upstream feature:
MD-family `M{n}-D{nn}` milestone-prefixed deliverable ID handling (PR #111 / augmentcode #111).
The conflict is the canonical "both branches ported the same fix" case. The resolution must
preserve ONE coherent complete implementation — not a naive concatenation.

## Structural Differences

| #     | Area                    | V1 (hybrid)              | V2 (ours)                              | V3 (theirs)              | Severity |
|-------|-------------------------|--------------------------|----------------------------------------|--------------------------|----------|
| S-001 | `_REQUIREMENT_PATTERNS` source | Contracts dict-comprehension | Contracts dict-comprehension + extra `_MD_TRAILING_D_RE` const | Hardcoded 6 literal patterns | High |

**Verified fact (empirical):** the contracts dict-comprehension in V1/V2 compiles to BYTE-IDENTICAL
patterns to V3's hardcoded table, with identical key order (`MD, FR, NFR, SC, G, D`; MD index 0, D index 5).
So S-001 is a *provenance/SoT* difference, not a behavioral one for the pattern table itself.

## Content Differences

| #     | Topic                | V1 (hybrid) Approach          | V2 (ours) Approach                     | V3 (theirs) Approach          | Severity |
|-------|----------------------|-------------------------------|----------------------------------------|-------------------------------|----------|
| C-001 | Bare-D dedup algorithm | **Span-aware** (suppress bare-D only if its char span ⊆ an MD span) | **Value-global** (drop bare-D if its VALUE equals any MD trailing-D) | **Span-aware** (identical to V1) | High |
| C-002 | Contract #8 (regex-literal duplication) | 0 duplicate literals (best) | 1 semi-dup (`_MD_TRAILING_D_RE` re-derives `D-?\d+`) | 6 duplicate literals (full SoT regression) | High |

**C-001 correctness:** Value-global dedup (V2) WRONGLY drops a legitimate standalone `D01` that
coincidentally shares its value with an `M1-D01` tail elsewhere. Span-aware dedup (V1, V3) preserves it.
This is the augmentcode #111 correctness fix.

## Contradictions

None. The three variants are alternative implementations of one agreed feature; no contradictory claims.

## Unique Contributions

| #     | Variant | Contribution | Value |
|-------|---------|--------------|-------|
| (none) | — | No variant contributes a capability absent from the others; all three implement MD-family extraction. V2's only unique element (`_MD_TRAILING_D_RE` + value-global pass) is a *defect*, not a contribution. | n/a |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The contracts registry `superclaude.contracts.ID_PATTERNS` always contains an `"MD"` key (ordered first). All three variants depend on MD being a recognized family; V1/V2 additionally do an explicit `_REQUIREMENT_PATTERNS["MD"]` key lookup that KeyErrors if MD is removed from contracts. | All variants extract an MD family | LOW — removing MD from contracts is a deliberate breaking SoT change; KeyError is desirable fail-loud behavior consistent with master:§Flaw 4 (no fail-open). | UNSTATED (promoted) |

## Summary
- Total structural differences: 1 (S-001)
- Total content differences: 2 (C-001, C-002)
- Total contradictions: 0
- Total unique contributions: 0
- Total shared assumptions surfaced: 1 (UNSTATED: 1, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-001, C-001, C-002 (all High)
