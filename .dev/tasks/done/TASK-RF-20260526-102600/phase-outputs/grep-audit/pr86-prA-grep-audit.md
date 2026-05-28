# PR A — Grep Audit for Case-Sensitive Ident Comparisons (Step 7)

**Date:** 2026-05-26
**Branch:** fix/integration-contracts-mechanism-signature
**Audit command:** `grep -nE "\bident\b|frozenset.*\bin\b" src/superclaude/cli/roadmap/integration_contracts.py`

## Full grep output (post-PR-A state)

```
260:            for ident in identifiers:
262:                    if ident.upper() in rline.upper():
356:                            if not any(ident in window_upper for ident in contract_idents):
469:    return frozenset(t.upper() for t in (base_tokens + hyphen_tokens + hyphen_fragments))
```

**Note (final-QA-gate cycle 1 update, 2026-05-26):** The original audit was captured immediately after Step 2.10 against the original Step 2.5 helper. After Phase 2 QA cycle-1 deviation refined the helper (added `hyphen_fragments` line + digit-lookahead in hyphen pattern), the return statement moved from line 461 to line 469 and now references `(base_tokens + hyphen_tokens + hyphen_fragments)`. The audit's substantive conclusion is unchanged — Layer 3 is the only site that required remediation, and `t.upper()` on every emitted token still honors invariant 1. Lines above re-verified via `grep -nE "\bident\b|frozenset.*\bin\b"` on the post-deviation file.

## Findings vs R1 G3 audit

R1's G3 audit established that on PR sha `67ab0af5` (pre-fix), the SOLE case-sensitive ident substring check was at Layer 3 (then-PR-line 355: `if not any(ident in window_text for ident in contract_idents):`). All other ident checks (Layer 2 at line 262, description checks at 282/284, stem-term hit at 307, stem-then-line at 342, matched_text classification at 384) already normalized case.

After PR A's Step 4 amendment:

- Line 260 `for ident in identifiers:` — loop iterator, not a comparison. ✅ Not in scope.
- Line 262 `ident.upper() in rline.upper()` — Layer 2, already case-insensitive (pre-PR-A). ✅ Unchanged, correct.
- Line 356 `ident in window_upper for ident in contract_idents` — Layer 3, NOW case-insensitive via the `window_upper = window_text.upper()` insertion at line 355 and the substitution of `window_text` → `window_upper` in the membership check. ✅ INV-002 amendment applied per Step 2.7.
- Line 469 `frozenset(t.upper() for t in (base_tokens + hyphen_tokens + hyphen_fragments))` — the new `_canonicalize_identifiers` helper's return statement (post Phase-2 QA cycle-1 deviation refinement adding `hyphen_fragments`). The `t.upper()` on every token honors invariant 1 (all tokens uppercase). ✅ Helper introduced per Step 2.5, refined per the documented deviation.

**Verdict:** PASS — the post-fix state matches the expected baseline. Layer 3 (the sole case-sensitive site identified by R1's G3 audit) is remediated. No additional case-sensitive ident sites were missed. Combined with `contract_idents` being produced by `_canonicalize_identifiers` (which uppercases all tokens), the AND-not-OR contract from the Round 2.5 fault-finder is satisfied: helper canonicalizes on the contract side, window-upper canonicalizes on the roadmap side, both required.
