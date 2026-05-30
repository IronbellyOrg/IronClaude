<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: HYBRID (V1 structure + V2 helper + V3 sequencing + INV-002 amendment) -->
<!-- Merge date: 2026-05-26T10:24:00Z -->

# Merged Fix Proposal — PR #86 Review Remediation

**Target**: PR #86 `fix/integration-contracts-mechanism-signature` (head sha `67ab0af5`)
**Findings addressed**: F1, F2, F3, F4, F5 (all 5 from reviewer comments r3299815777/779/783/789/792)
**Strategy**: 3 PRs. PR A merges first. PR B and PR C are RFC-first follow-ups that **both depend on PR A landing** (because they touch code paths PR A's helper rewrites) but are **independent of each other** (can land in either order, in parallel).

## Diagnosis (one-paragraph)

PR #86's `mechanism_signature` refactor introduces a coherent identifier-handling subsystem (`_extract_identifiers` → `mechanism_signature` → Layer 3 overlap guard → `_signature_subsumed`) but each call site silently disagrees on canonicalization (case, hyphenation, empty-set semantics). The 5 review findings are best understood as: **3 defects in one un-named invariant** (F1 hyphenation, F3 case-normalization, F5 stale test documentation — all rooted in `_extract_identifiers`'s implicit contract) + **2 independent defects** (F2 empty-idents coverage policy at Layer 3, F4 asymmetric subsumption in `_signature_subsumed`). The hybrid fix: name the invariant via a `_canonicalize_identifiers` helper in PR A (with pin tests landing first to defeat silent-green test regression), ship F2 and F4 as separate follow-up PRs each gated on a small policy decision.

<!-- Source: Variant 1 (root-cause-analyst), Section "Claim" — merged per Change A.1 framing -->
<!-- Source: Variant 2 (refactoring-expert), Section "Claim" — invariant-naming argument -->
<!-- Source: Variant 3 (quality-engineer), Section "Claim" — silent-green test risk -->

## Evidence (PR sha `67ab0af5`)

### F1 — `_extract_identifiers` drops hyphenated requirement IDs

`git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py` lines 412-419:

```python
def _extract_identifiers(text: str) -> list[str]:
    """Extract UPPER_SNAKE_CASE and PascalCase identifiers from text.
    FR-MOD2.4: Named mechanism identifier matching.
    """
    upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
    pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
    return upper_snake + pascal
```

Verified empirically: `re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", "FR-S10-02") == ['S10']`. The `\b` word boundary on `-` (non-word char) splits hyphenated IDs into fragments; `FR` is rejected (only 2 chars), `S10` matches, `02` rejected (starts with digit).

### F2 — Layer 3 skips identifier-overlap guard when `contract_idents` empty

PR sha lines 350-358:

```python
if contract_idents:
    window_start = max(0, j - 2)
    window_end = min(len(roadmap_lines), j + 3)
    window_text = " ".join(roadmap_lines[window_start:window_end])
    if not any(ident in window_text for ident in contract_idents):
        continue
covered = True
```

When `contract_idents` is empty (any mechanism whose extracted ident set is ∅), the guard is bypassed and stem+verb match marks the contract covered — reintroducing the "Implement priority dispatch for logging" false-positive class that the guard was added to prevent.

### F3 — Layer 3 identifier overlap is case-sensitive

Same lines 355-356: `if not any(ident in window_text for ident in contract_idents):` uses Python's direct substring `in` operator with no `.upper()` / `.lower()`. Inconsistent with Layer 2 at PR-line 261 (`if ident.upper() in rline.upper():`).

### F4 — `_signature_subsumed` is order-dependent

PR sha lines 425-441:

```python
def _signature_subsumed(
    sig: tuple[str, frozenset[str]],
    seen: dict[tuple[str, frozenset[str]], int],
) -> bool:
    mech, idents = sig
    if not idents:
        return sig in seen
    for (smech, sidents) in seen:
        if smech != mech:
            continue
        if idents and sidents and idents.issubset(sidents) and (idents & sidents):
            return True
        if idents == sidents:
            return True
    return False
```

Only returns True when NEW signature's idents are a `.issubset()` of an already-seen signature. A minimal sig seen first → a later superset is NOT subsumed → duplicate contracts.

### F5 — Test fixture comment mismatches `_extract_identifiers` behavior

`git show 67ab0af5:tests/roadmap/test_integration_contracts.py` lines 132-134:

```python
# Synthetic fixture per RQ-1 Option A: TUIBBS-scp-inspired prose with shared
# UPPER_SNAKE token `FR-S10-02` in every hub-dispatch context window so
# `_signature_subsumed` fires deterministically (subset+overlap dedup).
```

The comment claims `FR-S10-02` is a single UPPER_SNAKE token, but per F1, `_extract_identifiers` tokenizes it as `['S10']`. The test's subset+overlap dedup is being validated against the fragment, not the full requirement ID — the test still green-bars but its premise is broken.

<!-- Source: All 3 variants converged on these evidence citations -->

## Proposed Fix — 3 Sequential PRs

### PR A — Identifier Canonicalization (F1 + F3 + F5)

**Touches**: `src/superclaude/cli/roadmap/integration_contracts.py` (helper + Layer 3 window-upper); `tests/roadmap/test_integration_contracts.py` (pin tests + `test_t1` filter + F5 comment).

**Step 1 — Add pin tests** (land FIRST, in same commit as fix):

```python
class TestExtractIdentifiersInvariants:
    """Behavior-pin tests asserting exact set equality.

    These are red→green acceptance signals for the canonicalization fix.
    Substring-based downstream assertions silently green-bar regardless of
    fix correctness; these pin tests close that gap.
    """

    def test_hyphenated_requirement_id_emits_full_token(self):
        assert set(_extract_identifiers("FR-S10-02")) == {"FR-S10-02", "S10"}

    def test_mixed_case_canonicalized_via_helper(self):
        assert _canonicalize_identifiers("fr-s10-02") == frozenset({"FR-S10-02", "S10"})

    def test_pascal_case_uppercases_consistently(self):
        # INV-003 guard: PascalCase tokens must survive .upper() AND
        # Layer-3 window-upper. This pin test would FAIL if either side
        # of the canonicalization chain regresses.
        assert _canonicalize_identifiers("ConcreteStrategy") == frozenset({"CONCRETESTRATEGY"})

    def test_empty_text_yields_empty_frozenset(self):
        assert _canonicalize_identifiers("") == frozenset()
```

**Step 2 — Add `_canonicalize_identifiers` helper**:

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
    # Additive: preserve existing UPPER_SNAKE + PascalCase tokens AND
    # capture hyphenated requirement IDs.
    base_tokens = _extract_identifiers(text.upper())  # Honors invariant 1: uppercase input ensures the case-sensitive UPPER_SNAKE regex matches token fragments like `S10` even for lowercase requirement IDs. Validated by OQ-1 adversarial debate (oq1-debate/adversarial/).
    hyphen_pattern = re.compile(r"\b(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b", re.IGNORECASE)
    hyphen_tokens = hyphen_pattern.findall(text)
    return frozenset(t.upper() for t in (base_tokens + hyphen_tokens))
```

**Step 3 — Switch construction site to use helper** (PR-line 196):

```python
# BEFORE: idents = frozenset(_extract_identifiers(context))
# AFTER:
idents = _canonicalize_identifiers(context)
```

**Step 4 — Mandate `window_text.upper()` at Layer 3** (PR-line 355, INV-002 + INV-003 remediation):

```python
# BEFORE:
#   if not any(ident in window_text for ident in contract_idents):
# AFTER:
window_upper = window_text.upper()
if not any(ident in window_upper for ident in contract_idents):
```

**Step 5 — Update `test_t1` filter from substring to `mechanism_signature[1]`** (and audit for similar patterns):

```python
# BEFORE (silently green): filter = lambda c: "FR-S10-02" in c.spec_evidence
# AFTER (asserts canonicalization actually fired):
filter = lambda c: "FR-S10-02" in c.mechanism_signature[1]
```

**Step 6 — Rewrite F5 fixture comment**:

```python
# Synthetic fixture per RQ-1 Option A: TUIBBS-scp-inspired prose with shared
# hyphenated requirement-ID token `FR-S10-02` (canonicalized via
# `_canonicalize_identifiers` — see helper docstring for invariants) in every
# hub-dispatch context window so `_signature_subsumed` fires deterministically.
```

**Step 7 — Grep audit**: run `grep -nE "\bident\b|frozenset.*\bin\b" src/superclaude/cli/roadmap/integration_contracts.py` and document any other case-sensitive ident comparisons in the PR description.

### PR B — F2 Empty-Idents Coverage Policy (RFC-first)

**Step 1 — RFC**: surface the two options in a PR description / GitHub issue:

- Option (a) — strict: refuse-to-cover when `contract_idents` empty. Reasoning: empty idents = no evidence of the mechanism identity, so a generic verb match isn't enough.
- Option (b) — permissive-with-stricter-gate: when `contract_idents` empty, require same-line co-occurrence of mechanism term + impl verb (no 3-line window). Reasoning: keeps some coverage for mechanisms that genuinely have no UPPER_SNAKE / PascalCase identifiers.

Audit existing real-world specs to measure coverage delta under each option. Team picks one.

**Step 2 — Implement chosen policy + add regression test**: the regression test MUST use a fixture that DELIBERATELY exercises an empty-idents codepath (INV-007: PR A's fix removes the existing empty-idents corpus by populating idents for previously-hyphenated cases).

### PR C — F4 Subsumption Symmetry (RFC-first)

**Step 1 — RFC**: confirm whether the asymmetric design was intentional (INV-009 + A-002). Read the original PR description and recent commit messages. If unstated, propose one of:

- (a) Replace `seen` sig with broader on superset detection. Cost: loses minimal sig's IC-### counter slot (renumbering downstream).
- (b) Maintain equivalence-class map keyed by minimal-sig-of-class. Cost: more code; preserves all counter slots.
- (c) Short-circuit dedup on either-direction-subset. Cost: loses one counter slot per pair (similar to (a) but symmetric).

**Step 2 — Implement chosen mechanism + permutation tests + IC-### re-baseline**:

```python
def test_signature_subsumed_is_order_independent(self):
    # Feed signatures in (minimal, superset) AND (superset, minimal) order;
    # assert dedup produces same contract count.
    ...
```

Re-baseline `test_duplicate_lines_deduplicated` and `test_sequential_id_assignment` for any IC-### shifts.

## Risk + Rollback

| PR | Primary risk | Mitigation | Rollback target |
|----|--------------|------------|-----------------|
| PR A | `.upper()` canonicalization is a contract change; downstream consumer may rely on original case | Step 7 grep audit; pin test for PascalCase regression; helper docstring documents the contract | Revert PR A only — PR B and PR C have not landed |
| PR B | Coverage rate may shift under either option; could surprise teams running `superclaude roadmap` audits | Real-spec audit BEFORE merging; landed behind an internal flag if uncertain | Revert PR B only — independent of PR A and PR C |
| PR C | IC-### renumbering propagates to roadmap audit consumers (downstream task IDs) | Permutation tests; baseline diff in PR description; coordinate with audit consumers | Revert PR C only — independent of PR A and PR B |

## Alternative Fixes Considered

- **Single-PR bundle** (V2's original): rejected per V1's split rationale + V3 Round 2 concession that F2/F4 deserve independent debate venues.
- **Property-based hypothesis tests + JSON snapshot guard + new conftest.py** (V3's full Phase 0): rejected per V3 Round 2 concession that this infrastructure is separable from the load-bearing pin tests. Move to a follow-up "test infrastructure" PR if the team wants it.
- **Larger refactor** (`Identifier` value object, tokens-vs-RequirementID split): rejected per V2 Round 1 — premature abstraction for a 441-LOC pure-function module.

## Files to Change

- `src/superclaude/cli/roadmap/integration_contracts.py` (PR A: helper, Layer 3 window-upper; PR B: F2 policy; PR C: F4 symmetry)
- `tests/roadmap/test_integration_contracts.py` (PR A: pin tests, `test_t1` filter, F5 comment; PR B: empty-idents regression test; PR C: permutation test + re-baseline)

## Test Plan (PR A scope)

1. Pin tests land FIRST in the diff (Step 1) — RED on PR sha `67ab0af5`, GREEN after Steps 2-4.
2. `test_t1` filter change (Step 5) — GREEN after the canonicalization fires; would have been silently green before.
3. Run full `tests/roadmap/` and `superclaude roadmap` audit on `.dev/releases/current/*/spec.md` files; diff coverage results before/after. Document any net changes in PR description.
4. Run `make lint` + `make verify-sync` (`.claude/` is gitignored; no sync impact expected since this is a CLI change, not a skill).
