# Option C — Modify `_extract_identifiers` Itself

## Problem statement

Same as Options A and B.

## Proposed change

Add a hyphenated-ID pattern directly to `_extract_identifiers` so it natively returns the full hyphenated token alongside the UPPER_SNAKE and PascalCase tokens.

Change `_extract_identifiers` body from:
```python
upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
return upper_snake + pascal
```

To:
```python
upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
hyphenated = re.findall(r"\b(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b", text, re.IGNORECASE)
return upper_snake + pascal + [t.upper() for t in hyphenated]
```

Helper `_canonicalize_identifiers` stays as drafted. Test 1 stays as drafted.

## Why this would work (per-test trace)

- **Test 1**: `_extract_identifiers("FR-S10-02")` now returns `["S10", "FR-S10-02"]`. `set(...)` = `{"S10", "FR-S10-02"}` ✓.
- **Test 2**: `_canonicalize_identifiers("fr-s10-02")` calls `_extract_identifiers("fr-s10-02")` which (with IGNORECASE on the hyphen-regex) returns `[]` from upper_snake + `[]` from pascal + `["FR-S10-02"]` from hyphenated. Combined with helper's own hyphen-regex (which would now be redundant) → de-duplicated frozenset → `{"FR-S10-02"}` — STILL MISSING `"S10"` unless we ALSO uppercase input in `_extract_identifiers` OR add the `.upper()` to the helper (which is Option B).
- **Tests 3 + 4**: pass.

## Open issue with this option

**Same problem as Option A**: Test 2's lowercase input doesn't yield `"S10"` because the `\b[A-Z][A-Z0-9_]{2,}\b` regex still requires uppercase. Option C alone is incomplete; it must be combined with Option B's `.upper()` to fully resolve OQ-1.

## Scope expansion analysis

- **`_extract_identifiers` is a public function in the file** (called by the construction site at PR-line 196 and potentially by external consumers). Modifying it changes the public contract.
- **Merged-output explicitly preserves `_extract_identifiers`** — its design rationale stated the helper wraps `_extract_identifiers` for backward compatibility. Option C violates that design.
- **V3's quality-engineer hypothesis card explicitly rejected** replacement-style F1 in favor of additive-only. Option C is closer to replacement-style.

## Risks

- Breaks backward compatibility for any external consumer of `_extract_identifiers`.
- Re-litigates V1/V2/V3 adversarial debate decision to preserve `_extract_identifiers` as-is.
- Even after applying, still requires Option B's `.upper()` to fully resolve OQ-1 — so it's strictly more scope for the same outcome.

## Test plan

- Apply Option C's change to `_extract_identifiers`.
- ALSO apply Option B's `.upper()` to `_canonicalize_identifiers` (because Option C alone doesn't fix Test 2).
- Run full test suite, especially `test_signature_subsumed_*` tests that might depend on `_extract_identifiers` returning ONLY the legacy UPPER_SNAKE/PascalCase set.
- Re-baseline any tests that depended on the legacy return shape.

## Confidence

0.30 — Option C is a worse-scoped version of Option B with extra risk. Not recommended.
