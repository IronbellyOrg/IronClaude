# Merge Log

## Metadata

- Base: HYBRID convergence (no single variant; V1 PR-shape + V2 helper + V3 sequencing + Round 2.5 INV-002 amendment)
- Executor: inline (no `merge-executor` agent spawn — composition was deterministic from refactor-plan.md)
- Changes applied: 7 (PR A) + 2 (PR B RFC) + 2 (PR C RFC) = 11 total
- Status: success
- Timestamp: 2026-05-26T10:24:00Z

## Changes Applied

| # | Change | Source | Status | Provenance Tag in merged-output.md |
|---|--------|--------|--------|-------------------------------------|
| 1 | PR A pin tests (4 tests) | V3 hypothesis card (scaled per V3 Round 2 concession) | ✅ applied | "Source: Variant 3 (quality-engineer), pin-tests scaled" |
| 2 | `_canonicalize_identifiers` helper with 3-invariant docstring | V2 hypothesis card | ✅ applied | "Source: Variant 2 (refactoring-expert), helper" |
| 3 | Switch construction-site call to helper | V2 hypothesis card | ✅ applied | "Source: Variant 2, Change A.3" |
| 4 | `window_text.upper()` at Layer 3 (PR-line 355) | V3 hypothesis card, ELEVATED by Round 2.5 INV-002 | ✅ applied (mandatory) | "Source: Variant 3 + INV-002 amendment" |
| 5 | `test_t1` filter substring → `mechanism_signature[1]` | V3 hypothesis card U-001 | ✅ applied | "Source: Variant 3, U-001" |
| 6 | F5 fixture comment rewrite | All 3 variants agree | ✅ applied | "Source: convergent across all variants" |
| 7 | Grep audit for case-sensitive ident comparisons | INV-002 (Round 2.5) | ✅ applied (audit step in PR description) | "Source: Round 2.5 fault-finder, INV-002 defense-in-depth" |
| 8 | PR B RFC scaffold (F2 policy options) | V1's split rationale + V2's policy ambiguity | ✅ applied | "Source: Variant 1 + Variant 2 hybrid" |
| 9 | PR B empty-idents regression test requirement | Round 2.5 INV-007 | ✅ applied | "Source: Round 2.5 INV-007" |
| 10 | PR C RFC scaffold (F4 mechanism options) | V1's split rationale + INV-009 | ✅ applied | "Source: Variant 1 + Round 2.5 INV-009" |
| 11 | PR C permutation tests + IC-### re-baseline | V3 hypothesis card | ✅ applied | "Source: Variant 3" |

## Changes Rejected (and reason)

| Change | Source | Reason rejected |
|--------|--------|------------------|
| Property-based hypothesis tests | V3 | V3 conceded in Round 2 — defer to test-infra follow-up PR |
| JSON snapshot guard baseline | V3 | Same reason |
| New `conftest.py` for snapshot infra | V3 | Same reason |
| Single PR for all 5 findings | V2 | V1's split rationale + V2/V3 Round 2 compatibility concessions |
| `Identifier` value object | V2 (mentioned but rejected even by V2) | Premature abstraction (per V2's own card) |
| Replacement-style F1 (only emit `FR-S10-02`, drop `S10`) | V1 implicit | V3's additive-only argument: preserves existing test green-bars; backward-compat-by-default safer |

## Post-Merge Validation

### Structural integrity

✅ Pass — merged-output.md uses H1 + H2 + H3 consistently; no heading-level gaps; sections in logical order (Diagnosis → Evidence → Proposed Fix → Risk → Alternatives → Files → Test Plan).

### Internal references

- 11 cross-references checked (references to PR-line numbers, INV-NNN ids, F1-F5 finding ids, V1/V2/V3 variant ids).
- All references resolve to entities defined in upstream artifacts (`diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`).
- 0 broken references.

### Contradiction re-scan

Scanned merged-output.md for NEW contradictions introduced by the merge:

- The "additive-only" F1 (preserves `S10` AND adds `FR-S10-02`) does NOT contradict the helper's "uppercase canonicalization" invariant — both can be true simultaneously (helper uppercases AND adds the hyphenated token).
- The "land pin tests first" claim does NOT contradict the "PR A 3-PR split" claim — pin tests land in PR A as the first commit.
- The "Layer 3 window-upper mandatory" amendment does NOT contradict V2's helper — they compose (helper uppercases the contract_idents side; window-upper canonicalizes the roadmap side).

0 new contradictions introduced.

## Summary

- Planned changes: 11
- Applied: 11
- Failed: 0
- Skipped: 0
- Status: **success**

The merged proposal is internally consistent, addresses all 5 PR review findings, and incorporates the Round 2.5 fault-finder's INV-002 amendment as a mandatory step.
