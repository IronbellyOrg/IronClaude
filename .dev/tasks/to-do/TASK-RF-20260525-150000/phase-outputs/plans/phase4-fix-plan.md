# Phase 4 Fix Plan — t7 Failure Analysis

## Initial Phase 4.1 Verdict: 27/28 pass; t7 fails.

## Failing Test

**`TestHubDispatchRegression::test_t7_stem_fallback_without_ident_overlap_uncovers`**

Assertion: `assert result.uncovered_count >= 1` — but actual is 0 (contract is covered when it should not be).

## Root Cause

The merged-output.md spec is **internally inconsistent**:

- §2.4 Layer 1 `dispatch_family` regex includes bare `priority` as an alternation: `(?:[a-z]+-)?(?:class-priority|priority|named-theme|...)[\s_-]?dispatch`
- §3 t7 asserts that the roadmap line "Implement priority dispatch for logging events." should NOT cover the hub contract (because identifier-overlap guard rejects the match).

But the Layer 1 regex DOES match "priority dispatch" (via the bare `priority` alternation). Layer 1 fires, finds the impl_verb `Implement` on the same line, marks the contract covered, and short-circuits before Layer 3 ever runs. So Layer 3's identifier-overlap guard never gets the chance to reject the match.

Evidence from test failure:
```
mechanism_signature=('dispatch_table', frozenset({'S10'}))
roadmap_evidence='Implement priority dispatch for logging events.'
roadmap_location='line 2'  # NOT 'line N (stem+overlap)' — confirms Layer 1, not Layer 3
```

The contract's identifier set is `{'S10'}` (extracted from `FR-S10-02` — `_extract_identifiers` regex `\b[A-Z][A-Z0-9_]{2,}\b` requires 3+ chars; `FR` is rejected, `S10-02` becomes `S10` because `-` is a word boundary).

## Spec's Own Acknowledgement

merged-output.md §6 (counter-argument) explicitly acknowledges the compound-noun list's brittleness:
> "§2.2's compound-noun list (`class-priority|priority|named-theme|...`) inherits Opus's enumeration code smell. A future spec using `event-loop dispatch` or `batch-priority dispatch` re-introduces the same false-positive class."

The spec authors knew the list was imperfect but didn't trace it through t7's assertion.

## Remediation

Remove bare `priority` from BOTH the extraction regex (`DISPATCH_PATTERNS[0]` §2.2) AND the coverage Layer 1 `dispatch_family` regex (§2.4). Rationale:

1. **t2 still passes**: roadmap has `class-priority dispatch` (matches the explicit `class-priority` alternation, which we KEEP).
2. **t6 still passes**: roadmap has `class-priority dispatch` (matches `class-priority`).
3. **t7 now correctly fails coverage**: roadmap has only bare `priority dispatch` → Layer 1 doesn't fire → Layer 3 fires → identifier-overlap guard rejects (no `FR-S10-02` / `S10` in roadmap window).
4. **t3 unaffected**: assertion is `len(contracts) <= 1`, satisfied whether `priority dispatch` extracts 0 or 1 contract.
5. **Honors design intent**: §2.4's three-layer design specifies Layer 3 as the false-positive defense for prose-level mechanism mentions without identifier overlap. Bare `priority` matching Layer 1 silently bypassed that defense.

**Deviation from merged-output.md §2.2 + §2.4 verbatim:** Remove bare `priority` from both regexes. Keep `class-priority` and all other alternations.

**Cycle count:** 1/2 (max 2 per Step 4.1).
