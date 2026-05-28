# Diff Analysis — Fix B Proposals (Opus vs Sonnet)

## Metadata
- Generated: 2026-05-25T14:40:00Z
- Variants compared: 2 (variant-1=opus, variant-2=sonnet)
- Total differences: 11
- Categories: structural (2), content (5), contradictions (1), unique (6), shared assumptions (3)
- Focus: correctness, risk, test-coverage

## Structural Differences

| # | Area | Variant 1 (Opus) | Variant 2 (Sonnet) | Severity |
|---|---|---|---|---|
| S-001 | Frontmatter | YAML frontmatter with `fix_id`, `confidence`, `addresses` | Plain markdown header (no frontmatter) | Low |
| S-002 | Section count | 6 top-level sections (problem, solution §2.1-2.5, test, BC, effort, confidence) | 5 top-level sections (problem, solution Parts 1-3, test, BC, confidence) | Low |

## Content Differences

| # | Topic | Variant 1 (Opus) approach | Variant 2 (Sonnet) approach | Severity |
|---|---|---|---|---|
| C-001 | Data-model change | Adds `mechanism_signature: tuple[str, frozenset[str]]` field to `IntegrationContract` with default value, persisting the dedup identity downstream | Does NOT modify the dataclass; uses internal stringly-typed key inside the extractor only | Medium (L2 architectural) |
| C-002 | `DISPATCH_PATTERNS[0]` change | Removes bare `DISPATCH` AND adds compound-noun arm `(?:[a-z]+-)?(?:class-priority\|priority\|named-theme\|...)[\s_-]?dispatch` to keep compound mentions detectable; dedup absorbs them | Removes bare `DISPATCH`; adds explicit `DISPATCH_TABLE`; nothing else — narrowest deletion possible | Medium (L2 architectural) |
| C-003 | Dedup-key design | `frozenset[str]` identifiers + `_signature_subsumed` with strict-subset + intersection rule (e.g., `{Interactive,Coalescible} ⊆ {Interactive,Coalescible,Bulk}` AND shares ≥1 → subsumed) | Stringly-typed `mechanism::sorted-identifiers` exact-match for ≥2-ident contexts; `hash(context)` fallback for low-ident contexts | High (L3 state mechanics — different boundary behaviour) |
| C-004 | Coverage broadening | New `dispatch_family` regex (mechanism-family aware) + adds `populate` to `impl_verbs` | New stem-based fallback (head-noun of compound mechanism term) constrained to same-line impl verb (no 3-line window expansion); does NOT add `populate` | Medium (L3 state mechanics — different correctness envelope) |
| C-005 | Risk framing | Risk = enumerative adjective list (false negative on future patterns) | Risk = stem-matching looseness (false positive on coverage when unrelated dispatch concerns appear) | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Whether `IntegrationContract` dataclass should grow a new field | YES — `mechanism_signature` persisted for downstream reuse | NO — internal-only key, no public API surface change | Medium — the two designs cannot both be merged verbatim; merge must choose |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | Opus | Adds `populate` to `impl_verbs` — catches the most common spec-author verb for dispatch tables; clean low-risk additive change | High |
| U-002 | Opus | Subsumption-based dedup (strict-subset + intersection check) — collapses contracts whose identifier-sets are asymmetric but mechanism-identical | Medium-High |
| U-003 | Opus | `mechanism_signature` persisted on dataclass enables future cross-method use (e.g., coverage-check identifier overlap defense) | Medium |
| U-004 | Opus | §2.5 architectural rationale ("why this is ONE coherent fix") + §5 effort estimate + §6 explicit strongest counter-argument | Medium |
| U-005 | Sonnet | Explicit `DISPATCH_TABLE` alternation in the tightened pattern (clarity, even though Opus matches it via `dispatch[_\s]?table`+IGNORECASE) | Medium |
| U-006 | Sonnet | Stem-based generic fallback applicable to ANY compound mechanism noun (middleware_chain, event_binding, etc.), not just dispatch | Medium |

## Shared Assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The TUIBBS-scp context windows for IC-005/IC-008/IC-010/IC-011 share enough identifiers (`Interactive`, `Coalescible`, `Bulk`) for mechanism-level dedup to collapse them | Both propose mechanism-level dedup keyed on identifier overlap | If a future spec has 4 hub-dispatch mentions with NON-overlapping identifier sets, neither proposal collapses them | UNSTATED |
| A-002 | `_classify_mechanism` correctly returns `dispatch_table` for all dispatch-related captures across the new compound-noun patterns | Both rely on this classifier without modifying it | Verified — line 320-323 of integration_contracts.py | STATED (verified) |
| A-003 | The existing `test_duplicate_lines_deduplicated` (3 identical lines → 1 contract) is preserved | Both claim preservation; verified via hand-trace for both proposals | Both proposals pass this test, but via different code paths (Opus via empty-ident exact-match; Sonnet via hash fallback) | STATED |

## Summary

- Total structural differences: 2 (both Low)
- Total content differences: 5 (1 High C-003, 4 Medium)
- Total contradictions: 1 (Medium)
- Total unique contributions: 6 (1 High U-001, 4 Medium-High, 1 Medium)
- Total shared assumptions: 3 (1 UNSTATED A-001 → promoted to debate; 2 STATED)
- Highest-severity items: C-003 (dedup semantics)
