# Diff Analysis: 3 Fix Proposals for PR #86 Review Findings

## Metadata

- Generated: 2026-05-26T10:23:00Z
- Variants compared: 3
- Variant 1 (V1): root-cause-analyst (split-into-3-PRs)
- Variant 2 (V2): refactoring-expert (canonicalize-helper)
- Variant 3 (V3): quality-engineer (phased-pin-tests-first)
- Focus areas: correctness, risk, test-coverage
- Total differences found: 13 (S=3, C=5, X=3, U=3, A=3, X excluded from sum where overlapping with C)

## Structural Differences

| # | Area | V1 (RCA) | V2 (RefExp) | V3 (QE) | Severity |
|---|------|----------|-------------|---------|----------|
| S-001 | Delivery shape | 3 separate PRs (A=F1+F3+F5, B=F2, C=F4) | 1 PR ≤40 LOC (helper + 2 surgical) | 1 PR with 3 internal phases (P0 pins, P1 F1+F3, P2 F2+F4) | High |
| S-002 | Test sequencing | Tests land alongside fix | Tests land alongside fix | Tests land BEFORE fix (Phase 0 pin tests red→green) | High |
| S-003 | New abstractions | None | One: `_canonicalize_identifiers(text) -> frozenset[str]` (15 LOC + 3-invariant docstring) | None (but adds conftest.py + snapshot JSON + property-based test infra) | Medium |

## Content Differences

| # | Topic | V1 (RCA) | V2 (RefExp) | V3 (QE) | Severity |
|---|-------|----------|-------------|---------|----------|
| C-001 | F1 regex strategy | New regex pattern + `.upper()` canonicalize at extraction time | Collapsed into `_canonicalize_identifiers` helper (invariants encoded in docstring) | **Additive-only**: preserve `S10` token AND add `FR-S10-02` token so existing assertions stay green | High |
| C-002 | F2 fix policy | Defer to PR B; refuse-to-cover when idents empty | Inline: flip `if contract_idents:` from bypass to requirement (one line) | Phase 2 separate sub-commit; same flip but with re-baseline | Medium |
| C-003 | F4 fix mechanism | Defer to PR C; symmetric containment (subset OR superset detection, merge into broader sig) | Symmetric containment inside same PR | Phase 2 sub-commit; symmetric containment + IC-### renumbering re-baseline | Low |
| C-004 | F5 (test fixture) | Rewrite comment to match extractor (no fixture change) | Comment becomes truthful because helper docstring names the invariants | Both: update comment AND change test_t1 filter from substring to `c.mechanism_signature[1]` | Medium |
| C-005 | Test surface area | New unit + permutation tests in same file | New unit tests in same file (modest) | 5 behavior-pin tests + property-based hypothesis tests + JSON snapshot guard + new conftest.py | High |

## Contradictions

| # | Point of Conflict | V1 (RCA) Position | V2 (RefExp) Position | V3 (QE) Position | Impact |
|---|-------------------|-------------------|----------------------|-------------------|--------|
| X-001 | Pin tests BEFORE or AFTER fix? | After (or alongside) | Alongside | **BEFORE** — Phase 0 mandates red→green acceptance signal | Medium |
| X-002 | Bundle F2+F4 with F1? | NO — split to PRs B & C | YES — same PR, surgical commits | YES — same PR, separate phase | High |
| X-003 | Introduce named abstraction? | NO — premature | YES — invariant-naming prevents regression | NO — but adds heavy test infra instead | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|-------------------|
| U-001 | V3 (QE) | **Test-fidelity failure mode**: identifies that test_t1/t6/t7 silently green-bar on substring containment of `FR-S10-02` rather than on identifier-set equality. A naive F1 fix leaves them green for the wrong reason — suite cannot distinguish "fix worked" from "fix had no observable effect." | **High** — neither V1 nor V2 surfaces this; without it, the entire test suite is a silent passthrough for the change |
| U-002 | V2 (RefExp) | **Named invariant docstring** as regression prevention. The `_canonicalize_identifiers` helper's docstring becomes load-bearing documentation that prevents the next contributor from re-introducing F3 the same way. | **Medium** — long-term hygiene; one-shot cost is 15 LOC |
| U-003 | V1 (RCA) | **Review-economics justification** for the 3-PR split: keeps coverage-policy debate (F2) and counter-renumbering debate (F4) out of the regex PR so each can be reviewed/tested/reverted on its own terms. | **Medium-High** — operational discipline; reduces risk of stacked rollbacks |

## Shared Assumptions (AD-2)

All three variants converge on these unstated preconditions:

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|-------------------|--------|--------|
| A-001 | `.upper()` canonicalization is acceptable as an implicit contract change to `_extract_identifiers` — none of the proposals audit downstream call sites for case-sensitive consumers | All 3 propose upper-casing somewhere in the chain | HIGH — could break any consumer that expects original casing | **UNSTATED** — promote to [SHARED-ASSUMPTION] |
| A-002 | `_signature_subsumed` SHOULD be symmetric. None challenge whether the asymmetric design is intentional (e.g., to preserve seed-order semantics for IC-### numbering). | All 3 fix F4 by making it symmetric | MEDIUM — if asymmetry was intentional, the fix breaks an invariant | **UNSTATED** — promote |
| A-003 | The PR's `mechanism_signature` refactor is the right underlying design. None question whether the entire `tuple[str, frozenset[str]]` shape is the right abstraction (vs. e.g., a class with explicit invariants). | All 3 patch the design; none reject it | LOW — accepting the PR's premise is the correct review posture | STATED implicitly by "fix this PR" framing |

## Summary

- Total structural differences: 3 (1 High, 1 High, 1 Medium)
- Total content differences: 5 (2 High, 2 Medium, 1 Low)
- Total contradictions: 3 (1 High, 2 Medium)
- Total unique contributions: 3 (1 High, 2 Medium-High)
- Total shared assumptions surfaced: 3 (UNSTATED: 2 promoted, STATED: 1)
- Highest-severity items: S-001 (PR shape), S-002 (test sequencing), C-001 (regex additive vs replace), C-005 (test surface), X-002 (bundle vs split), U-001 (silent-green tests), A-001 (canonicalization contract)
- Diff density: 13 substantive differences across 3 proposals → adversarial debate adds clear value (not "variants too similar" path)
