# Roadmap Suite Full Run (PR A applied)

**Date:** 2026-05-26
**Branch:** fix/integration-contracts-mechanism-signature
**Command:** `uv run pytest tests/roadmap/ -v --no-header`

## Summary line

```
======================= 1693 passed, 11 skipped in 4.84s =======================
```

## Failures (if any)

None.

## Notable verifications

- The 4 pin tests from `TestExtractIdentifiersInvariants` are GREEN (verified independently in `pin-tests-transition.md`).
- `test_t1_one_contract_per_hub_mechanism` (updated in Step 2.8 to use `c.mechanism_signature[1]`) is GREEN — confirms canonicalization actually fires, not silent-substring match on the raw evidence string.
- `test_t7_stem_fallback_without_ident_overlap_uncovers` (regression test for Layer 3 overlap-guard false-positive defense) is GREEN — confirms the Step 2.5 helper deviation (digit-lookahead in hyphen pattern + non-uppercased base_tokens) does not regress this defense.
- All 11 skipped tests are pre-existing skips, unrelated to PR A.

**Verdict:** PASS
