# Refactoring Plan — Hybrid Merge of 3 Fix Proposals

## Overview

- **Base shape**: V1 (RCA) 3-PR split
- **Incorporated from V2 (RefExp)**: `_canonicalize_identifiers` helper into PR A
- **Incorporated from V3 (QE)**: pin-tests-first sequencing + additive-only F1 + `test_t1` filter fix
- **Amended from Round 2.5**: Layer 3 `window_text.upper()` mandated alongside helper (INV-002 remediation)
- **Total changes planned**: 11 across 3 PRs (PR A: 7, PR B: 2, PR C: 2)
- **Risk profile**: PR A = Medium (touches 3 call sites + tests); PR B = Medium (policy decision); PR C = Low-Medium (re-baseline scope confined)

---

## PR A — Identifier Canonicalization (F1 + F3 + F5)

### Change A.1 — Add 2-3 behavior-pin tests (from V3, scaled down)

- **Source**: V3 hypothesis card "Phase 0" pin tests, scaled to minimal viable set per V3 Round 2 concession.
- **Target location**: `tests/roadmap/test_integration_contracts.py` (new test class `TestExtractIdentifiersInvariants`)
- **Approach**: insert before any production change; tests assert exact `set(_extract_identifiers(...))` equality for:
  - hyphenated requirement IDs: `set(_extract_identifiers("FR-S10-02")) == {"FR-S10-02", "S10"}` (additive-only)
  - mixed-case input: `set(_extract_identifiers("fr-s10-02")) == {"FR-S10-02", "S10"}` (canonicalization)
  - PascalCase preservation: `set(_extract_identifiers("ConcreteStrategy")) == {"CONCRETESTRATEGY"}` (per INV-003 remediation — explicit guard against PascalCase regression)
  - empty input: `set(_extract_identifiers("")) == set()`
- **Rationale**: Without these, the test suite cannot distinguish "fix worked" from "fix had no effect" (V3 U-001 + unanimous Round 2 concession).
- **Risk**: Low (additive tests). The PascalCase pin test will FAIL after the `.upper()` change if the helper is not amended for INV-003 — that failure IS the safety signal.

### Change A.2 — Introduce `_canonicalize_identifiers(text) -> frozenset[str]` helper

- **Source**: V2 hypothesis card.
- **Target location**: `src/superclaude/cli/roadmap/integration_contracts.py` — new private helper, placed near `_extract_identifiers`.
- **Approach**: extract-and-canonicalize as ONE step. Docstring names the 3 invariants explicitly:
  ```python
  def _canonicalize_identifiers(text: str) -> frozenset[str]:
      """Extract identifier-tokens from text into a canonical frozenset.

      Invariants:
        1. All tokens are uppercase (callers may match case-insensitively
           against any source by .upper()-ing both sides at the gate).
        2. Hyphenated requirement IDs (e.g. FR-S10-02) are emitted as ONE
           token, not split on hyphens. Underlying UPPER_SNAKE fragments
           (e.g. S10) are ALSO emitted alongside to preserve backward
           compatibility with existing assertions.
        3. Empty input yields an empty frozenset — callers MUST treat this
           as "no identifier evidence", never as "wildcard match".
      """
      ...
  ```
- **Rationale**: V2 U-002 (invariant naming prevents regression). V1 + V3 conceded in Round 2 that the helper is a separable + valuable addition.
- **Risk**: Medium — contract change for any future caller; mitigated by docstring + pin tests.

### Change A.3 — Replace `_extract_identifiers` call sites with the helper

- **Source**: V2 hypothesis card.
- **Target location**: PR-line 196 (`idents = frozenset(_extract_identifiers(context))`).
- **Approach**: `idents = _canonicalize_identifiers(context)`. The original `_extract_identifiers` STAYS as a public function for backward compatibility (returns the additive token set per Change A.1's pin tests); the helper wraps it with canonicalization.
- **Rationale**: Single seam for all 3 downstream call sites.
- **Risk**: Low — purely a refactor.

### Change A.4 — Mandate `window_text.upper()` at Layer 3 (INV-002 + INV-003 remediation)

- **Source**: V3 hypothesis card; ELEVATED from optional to mandatory by Round 2.5 fault-finder.
- **Target location**: PR-line 355: `if not any(ident in window_text for ident in contract_idents):`.
- **Approach**: change to `window_upper = window_text.upper()` and `if not any(ident in window_upper for ident in contract_idents):`. The `contract_idents` are already uppercase from the helper (Change A.3); without ALSO uppercasing the window, a roadmap citing `fr-s10-02` lowercase misses the `FR-S10-02` ident. Per INV-002, also addresses PascalCase tokens that survive `.upper()` only at the compare site (INV-003).
- **Rationale**: The Round 2.5 fault-finder PROVED via branch-trace that without this change, F3 is not closed. This is non-optional.
- **Risk**: Low — adds one `.upper()` call to a hot loop; performance impact negligible.

### Change A.5 — Update `test_t1` filter from substring to `mechanism_signature[1]`

- **Source**: V3 hypothesis card C-004.
- **Target location**: `tests/roadmap/test_integration_contracts.py` — `test_t1` (and any analogous test that filters by `"FR-S10-02" in c.spec_evidence`).
- **Approach**: change filter to `"FR-S10-02" in c.mechanism_signature[1]` (after Change A.3 makes this token present in the frozenset).
- **Rationale**: V3 U-001 (silent-green). Without this, `test_t1` continues to green-bar on substring containment regardless of whether the canonicalization works.
- **Risk**: Medium — if any other test does the same substring-on-evidence trick, it also needs updating. Grep audit required during PR review.

### Change A.6 — Update F5 fixture comment to be truthful

- **Source**: V1 + V2 + V3 (all agree).
- **Target location**: `tests/roadmap/test_integration_contracts.py` PR-line 132-134 (the TUIBBS comment).
- **Approach**: change "UPPER_SNAKE token `FR-S10-02`" to "hyphenated requirement-ID token `FR-S10-02` (canonicalized via `_canonicalize_identifiers`)". The helper's docstring (Change A.2) also serves as authoritative documentation.
- **Rationale**: F5 (the original PR review finding).
- **Risk**: Negligible.

### Change A.7 — Grep audit for other case-sensitive ident comparisons

- **Source**: implicit from INV-002 (Round 2.5).
- **Target location**: entire `src/superclaude/cli/roadmap/integration_contracts.py`.
- **Approach**: grep for `\bident\b` and any `frozenset.*in` patterns to find any OTHER consumer that does a case-sensitive ident substring check. Document findings in the PR description.
- **Rationale**: Defense-in-depth for the canonicalization-contract change (A-001 shared assumption).
- **Risk**: None (audit only).

---

## PR B — F2 Identifier-Overlap Guard Policy (depends-on: PR A merged)

### Change B.1 — Choose F2 policy via team discussion

- **Source**: V1's split rationale + V2's policy ambiguity acknowledgment.
- **Target location**: PR description / RFC issue (NOT code yet).
- **Approach**: surface the 2 options in the PR description: (a) refuse-to-cover when `contract_idents` empty (strict — V1's lean); (b) same-line co-occurrence fallback (require mechanism term + impl verb on the SAME LINE, not 3-line window — V2's lean).
- **Rationale**: V2 conceded this is a spec question, not a code question. The 3-PR split keeps this debate out of PR A.
- **Risk**: Low — RFC-level work.

### Change B.2 — Implement chosen F2 policy + add empty-idents regression test

- **Source**: V1 + V2 (mechanical implementation depends on B.1).
- **Target location**: `src/superclaude/cli/roadmap/integration_contracts.py` PR-line 351-358; `tests/roadmap/test_integration_contracts.py` new test (INV-007 remediation: this test must use a fixture that exercises an EMPTY `contract_idents` case, which PR A's F1 fix removes from the existing corpus).
- **Approach**: depends on B.1 outcome.
- **Risk**: Medium — coverage rate may shift; needs `superclaude roadmap` audit on real specs before/after.

---

## PR C — F4 Subsumption Symmetry (depends-on: PR A merged; can run parallel to PR B)

### Change C.1 — Determine F4 mechanism via design discussion

- **Source**: A-002 from diff-analysis + INV-009 (Round 2.5 — asymmetric subsumption may be intentional).
- **Target location**: PR description / RFC issue.
- **Approach**: read the original PR description for `_signature_subsumed` to confirm whether asymmetry was intentional. If unstated, propose symmetric containment with one of: (a) replace seen sig with broader (loses minimal sig's IC-### counter slot); (b) maintain equivalence-class map (preserves all counter slots; more code); (c) short-circuit dedup on either-direction-subset (loses one counter slot per pair).
- **Rationale**: V1 + V3 conceded F4 should be a separate PR; V2 conceded F2's analog. Round 2.5 surfaced the intentionality question as MEDIUM.
- **Risk**: Low — RFC-level work.

### Change C.2 — Implement chosen F4 mechanism + permutation tests + IC-### re-baseline

- **Source**: V1 + V3 mechanical.
- **Target location**: `_signature_subsumed` (PR-line 425-441); existing tests `test_duplicate_lines_deduplicated`, `test_sequential_id_assignment` (re-baseline if IDs shift).
- **Approach**: depends on C.1 outcome.
- **Risk**: Medium — IC-### shifts may ripple to roadmap audit consumers; mitigated by isolation in PR C.

---

## Changes NOT Being Made (and why)

- **V3's property-based hypothesis tests + JSON snapshot guard + new conftest.py** — REJECTED. V3 conceded in Round 2 that these are separable from the load-bearing Phase 0 pin tests. Move to a follow-up "test infrastructure" PR if the team wants this investment. Including them in PR A would inflate the review surface from ~80 LOC to ~250 LOC, drowning the actual fix.
- **V2's "single PR" framing** — OVERRULED. V1's 3-PR split is preserved because F2 and F4 each have independent debate axes (policy / mechanism) that don't belong with the regex fix. V2's helper IS preserved inside V1's PR A.
- **V1's "no helper" stance** — OVERRULED. V1 conceded in Round 2 that the helper is compatible with the split. V2's named-invariant docstring earns its 15 LOC by preventing the next contributor from re-introducing F3.

## Risk Summary

| PR | Risk | Mitigation | Rollback |
|----|------|-----------|----------|
| PR A | Medium | Pin tests precede production change; PascalCase pin (INV-003) catches helper regressions; grep audit (A.7) | Revert PR A only; PR B/C have not landed yet |
| PR B | Medium | RFC-first; empty-idents regression test required | Revert PR B; PR A and C stand independently |
| PR C | Medium | Permutation tests; IC-### re-baseline owned by this PR | Revert PR C; PR A and B stand independently |

## Review Status

Auto-approved (non-interactive mode; --interactive flag NOT set).
