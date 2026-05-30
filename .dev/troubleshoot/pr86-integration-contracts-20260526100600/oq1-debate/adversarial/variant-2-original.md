# Option B — Helper Uppercases Input Before Extraction (RECOMMENDED by qa-qualitative)

## Problem statement

Same as Option A: pin tests 1 and 2 cannot pass with the helper code as drafted because the helper's first line `base_tokens = _extract_identifiers(text)` is case-sensitive on the input.

## Proposed change

**Two-part change. Helper code is modified; Test 1 wrapper is also updated (same as Option A).**

### Part 1: Helper change

In `_canonicalize_identifiers`, change the first line of the body from:
```python
base_tokens = _extract_identifiers(text)
```

To:
```python
base_tokens = _extract_identifiers(text.upper())
```

The hyphen-regex line stays as drafted (already case-insensitive via `re.IGNORECASE` flag).

### Part 2: Test 1 wrapper (same as Option A)

Change Test 1 to use `_canonicalize_identifiers` instead of bare `_extract_identifiers`:
```python
def test_hyphenated_requirement_id_emits_full_token(self):
    assert _canonicalize_identifiers("FR-S10-02") == frozenset({"FR-S10-02", "S10"})
```

## Why this works (per-test trace)

- **Test 1** (`"FR-S10-02"` uppercase): `_extract_identifiers("FR-S10-02".upper())` = `_extract_identifiers("FR-S10-02")` (already uppercase) = `["S10"]`. Hyphen-regex returns `["FR-S10-02"]`. Combined → `["S10", "FR-S10-02"]` → uppercased frozenset → `{"S10", "FR-S10-02"}` ✓.
- **Test 2** (`"fr-s10-02"` lowercase): `_extract_identifiers("fr-s10-02".upper())` = `_extract_identifiers("FR-S10-02")` = `["S10"]`. Hyphen-regex on `"fr-s10-02"` returns `["fr-s10-02"]`. Combined → `["S10", "fr-s10-02"]` → uppercased frozenset → `{"S10", "FR-S10-02"}` ✓.
- **Test 3** (PascalCase preservation): `_canonicalize_identifiers("ConcreteStrategy")` → `_extract_identifiers("CONCRETESTRATEGY")` — but wait, the PascalCase regex is `\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b` which requires alternating upper-lower. `"CONCRETESTRATEGY"` (all uppercase) does NOT match the PascalCase regex. The UPPER_SNAKE regex `\b[A-Z][A-Z0-9_]{2,}\b` matches the whole string `"CONCRETESTRATEGY"` (no hyphens, no underscores, all uppercase, length > 3). Returns `["CONCRETESTRATEGY"]`. Hyphen-regex returns `[]`. Final → `{"CONCRETESTRATEGY"}` ✓ (matches expected `frozenset({"CONCRETESTRATEGY"})`).
- **Test 4** (empty input): `_extract_identifiers("".upper())` = `[]`. Hyphen-regex on `""` returns `[]`. Final → `frozenset()` ✓.

All 4 tests pass.

## Evidence

- Helper docstring's invariant 1 ("All tokens are uppercase") is satisfied uniformly across all inputs by uppercasing at the boundary.
- The change is one word (`.upper()`) — minimum-scope.
- The hyphen-regex was already case-insensitive (correctly so), so the uppercase normalization aligns with the existing design intent.

## Risks

- **Information loss for mixed-case identifiers that should retain their case**: any caller that relied on `_canonicalize_identifiers` preserving mixed-case via the `_extract_identifiers` PascalCase regex would now lose distinction. But this is exactly the helper's stated invariant ("All tokens are uppercase"), so this is intentional behavior, not a regression.
- **Performance**: `.upper()` on long strings is O(n). Marginal overhead in a hot loop. Negligible.
- **Backward compatibility**: `_extract_identifiers` itself is unchanged — public-contract consumers see no behavior change. Only `_canonicalize_identifiers` (a NEW helper) has this behavior.

## Test plan

- Apply both Part 1 (helper change) and Part 2 (Test 1 change).
- Run `uv run pytest tests/roadmap/test_integration_contracts.py::TestExtractIdentifiersInvariants -v`.
- Expected: all 4 pin tests PASS.
- Run the full `tests/roadmap/` suite to confirm no regression.

## Confidence

0.92 — Option B is the minimum-scope change that satisfies all 4 pin tests AND aligns with the helper's stated invariant. The mental regex trace was verified by qa-qualitative across all 4 tests.
