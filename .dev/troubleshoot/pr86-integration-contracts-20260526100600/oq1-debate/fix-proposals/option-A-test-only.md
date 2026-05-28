# Option A — Test-Only Fix (change Test 1 wrapper)

## Problem statement

The 4 pin tests in the PR A merged-output spec assert behavior that the helper code as drafted cannot deliver:

- **Test 1**: `assert set(_extract_identifiers("FR-S10-02")) == {"FR-S10-02", "S10"}` — `_extract_identifiers` is NOT modified by PR A; on `"FR-S10-02"` the regex `\b[A-Z][A-Z0-9_]{2,}\b` matches only `"S10"` because the leading `FR` fails the `{2,}` 3-character minimum. Test 1 FAILS post-fix.
- **Test 2**: `assert _canonicalize_identifiers("fr-s10-02") == frozenset({"FR-S10-02", "S10"})` — helper calls `_extract_identifiers(text)` with original case; on lowercase input it returns `[]`. The hyphen-regex (with `re.IGNORECASE`) returns `["fr-s10-02"]`, then `.upper()` makes it `"FR-S10-02"`. Result is `frozenset({"FR-S10-02"})` — MISSING `"S10"`.

## Proposed change

**Test code change only. Helper code stays exactly as drafted in merged-output.md.**

Change Test 1 from:
```python
def test_hyphenated_requirement_id_emits_full_token(self):
    assert set(_extract_identifiers("FR-S10-02")) == {"FR-S10-02", "S10"}
```

To:
```python
def test_hyphenated_requirement_id_emits_full_token(self):
    assert _canonicalize_identifiers("FR-S10-02") == frozenset({"FR-S10-02", "S10"})
```

This matches the call-pattern of tests 2-4. With uppercase input `"FR-S10-02"`, the helper's first line `base_tokens = _extract_identifiers(text)` returns `["S10"]` (the regex matches the middle `S10`). The hyphen-regex returns `["FR-S10-02"]`. Combined and uppercased → `frozenset({"FR-S10-02", "S10"})` ✓.

## Open issue with this option

**Test 2 still fails.** Test 2 specifically tests lowercase input (`"fr-s10-02"`) to validate the helper's case-canonicalization invariant. With the helper unchanged, lowercase input still yields `frozenset({"FR-S10-02"})` (missing `S10`).

The user/orchestrator would need to ALSO either:
- (a) Weaken Test 2's expected set to `frozenset({"FR-S10-02"})` — REJECTS the invariant the helper's docstring claims ("All tokens are uppercase").
- (b) Apply Option B's helper change anyway.
- (c) Drop Test 2 entirely.

None of these are clean.

## Evidence

- Helper docstring in merged-output.md (Step 2): "Invariants: 1. All tokens are uppercase ..."
- Mental regex trace verified by qa-qualitative review (5/5 confidence, see qa-qualitative-review.md).

## Risks

- Test 2 still fails — issue not fully resolved.
- Splits the canonicalization invariant: "uppercase" applies to outputs but not inputs (asymmetric).
- Future contributor may add another test with lowercase input and hit the same bug.

## Test plan

- Apply only the Test 1 change.
- Run `uv run pytest tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants -v`.
- Observe: Test 1 PASS, Test 2 FAIL.
- Verdict: incomplete — does not satisfy the merged-output spec's Test Plan claim of "GREEN after Steps 2-4."

## Confidence

0.45 — Option A is a partial fix. It resolves Test 1 but leaves Test 2 broken, which means the merged-output's stated Test Plan can't be honored.
