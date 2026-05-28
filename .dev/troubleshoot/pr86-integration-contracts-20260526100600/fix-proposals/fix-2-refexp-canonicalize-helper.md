# Tier 2 Hypothesis — Refactoring-Expert (architectural cleanup angle)

**Author**: refactoring-expert (Tier 2, parallel hypothesis)
**Tier**: 2
**Type**: refactor-vs-surgical decision + structural recommendation
**Scope**: `src/superclaude/cli/roadmap/integration_contracts.py` @ PR #86 sha `67ab0af5`
**PR**: <https://github.com/IronbellyOrg/IronClaude/pull/86>

## Claim

The 5 review findings are **NOT five surgical bugs orbiting a missing abstraction** — they are **four real surgical bugs (F1, F2, F3, F4) plus one stale comment (F5), all sharing a single under-specified concept: what *is* a "mechanism identifier"?** The PR added the new `mechanism_signature: tuple[str, frozenset[str]]` field without ever giving that frozenset a name, a normalizer, or an invariant. The signature is built at one site, consumed at three (Layer 3 overlap guard, `_signature_subsumed`, F2's truthiness gate), and *every one of those call sites makes a different implicit assumption* about case, hyphenation, and emptiness semantics. So the right answer is **one tiny structural seam — a `_canonicalize_identifiers()` helper that defines normalization once — plus the four surgical fixes**. Anything bigger (a full `Identifier` value object, an `IdentifierSet` class, a "tokens vs requirement IDs" split) is over-engineering for a 441-LOC pure-function module with one consumer.

## Evidence — the structural seam the refactor missed

Three call sites consume `_extract_identifiers` output, each with a **different implicit contract**:

1. **Construction site** (`git show 67ab0af5:src/superclaude/cli/roadmap/integration_contracts.py` line 196):
   ```python
   idents = frozenset(_extract_identifiers(context))
   ```
   No normalization. Whatever the regex returns is canonical-by-fiat.

2. **Layer 2 coverage check** (line 262):
   ```python
   if ident.upper() in rline.upper():
   ```
   Case-insensitive at *compare* time. Tolerates mixed-case roadmap prose.

3. **Layer 3 overlap guard** (line 355) — added by THIS PR:
   ```python
   if not any(ident in window_text for ident in contract_idents):
   ```
   Case-**sensitive**. Direct substring. Silently disagrees with site #2.

4. **`_signature_subsumed`** (lines 432-441) — added by THIS PR:
   ```python
   if not idents: return sig in seen
   ...
   if idents and sidents and idents.issubset(sidents) and (idents & sidents):
       return True
   ```
   Empty set → exact-tuple-only dedup. **No notion of "empty means weak, fall back to evidence-line dedup"** — so the F2 emptiness pathology is doubled here too (an empty-ident signature collides with another empty-ident signature only if mechanism + evidence are byte-identical, which the old code already handled via `seen_evidence`; the new code lost that path).

The **missing concept** is not "a value object for `Identifier`". The missing concept is a **two-line docstring contract on what an identifier-set means**, materialized as a `_canonicalize_identifiers()` helper. Specifically:

- "An identifier is a non-empty uppercase string." (kills F3.)
- "Hyphenated requirement IDs are single identifiers." (kills F1.)
- "An empty identifier-set means *no evidence available*, not *signature matches everything*." (kills F2 and tightens `_signature_subsumed`.)

Once those three sentences exist in code as `_canonicalize_identifiers(text) -> frozenset[str]`, F1+F3 collapse into that helper, F2 becomes a one-line condition flip ("require *non-empty* identifiers, not 'if any'"), and F4's symmetric-containment fix stays exactly as Tier 1 describes — independent.

## Proposed Fix — ONE coherent change set

**Verdict: refactor + surgical, not pure-refactor and not 5-fixes.** Introduce **one helper function and one invariant comment** as the structural backbone, then make the four surgical fixes hang off it. Total diff ≤ 40 LOC.

```python
# NEW — one helper, defined once, used at three sites.
def _canonicalize_identifiers(text: str) -> frozenset[str]:
    """Extract and canonicalize mechanism identifiers from text.

    Invariants:
    - All identifiers are uppercase (case-insensitive matching downstream).
    - Hyphenated requirement IDs (FR-S10-02, RFC-1234) are ONE identifier.
    - Empty result means 'no identifier evidence', NOT 'matches anything'.
      Downstream callers MUST gate behavior on emptiness explicitly.
    """
    upper_snake = re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", text)
    pascal = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", text)
    hyphenated = re.findall(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b", text)
    return frozenset(t.upper() for t in (upper_snake + pascal + hyphenated))
```

Then:

- **F1 fix** — `_extract_identifiers` becomes a thin alias that calls `_canonicalize_identifiers` (or is replaced by it). Hyphenated regex lands here.
- **F3 fix** — the Layer 3 overlap-guard substring check now compares uppercase-vs-uppercase by construction. The `.upper()` at compare time is no longer needed; the invariant is enforced at extraction.
- **F2 fix** — change Layer 3's `if contract_idents:` from a *bypass* to a *requirement*: `if not contract_idents: continue  # cannot verify overlap, refuse to cover via stem fallback`. The invariant comment in `_canonicalize_identifiers` makes this explicit and reviewable.
- **F4 fix** — symmetric containment in `_signature_subsumed`, as Tier 1 describes. *Independent* of the helper.
- **F5 fix** — pure comment correction in the test fixture (now actually correct because F1 makes `FR-S10-02` a real single identifier).

**Cost/benefit:**

| Option                          | LOC delta | Risk           | Conceptual cleanup |
| ------------------------------- | --------- | -------------- | ------------------ |
| 5 fully-surgical fixes          | ~25       | low            | low — drift recurs |
| **Helper + 4 surgical (mine)**  | **~40**   | **low**        | **high — invariants codified** |
| Full `Identifier` value object  | ~120      | medium         | high but unused elsewhere |
| Tokens-vs-RequirementID split   | ~80       | medium         | premature — one consumer |

The helper-plus-surgical option costs **15 extra LOC** to lock in invariants the next contributor cannot accidentally drift from. The value-object option would add a class, an `__init__`, an `__eq__`, a `__hash__`, and migration of a `frozenset[str]` field — for zero behavior gain.

## Confidence

**Self-reported: 0.78.**

I am confident the helper exists and is small (0.95 on F1/F3 collapsing cleanly). I am less confident on F2's semantic decision — "refuse to cover" vs "fall back to evidence-line dedup like the pre-PR `seen_evidence` did". Both are defensible; the team needs to pick one. That is a spec question, not a refactor question, which is why I rate 0.78 rather than 0.90+.

## Risks — over-engineering

- **Risk of premature abstraction**: if I went further (a `MechanismIdentifier` class, an `IdentifierSet` with `.canonicalize()` / `.matches_window()` methods, a tokens-vs-IDs split), I would be inventing seams for a 441-LOC module with one caller. I explicitly recommend against this. The helper function is the **smallest abstraction that names the invariant**.
- **Risk that `.upper()`-at-extraction breaks PascalCase semantics**: `PascalCase` after `.upper()` becomes `PASCALCASE`, indistinguishable from UPPER_SNAKE. If downstream cares about that distinction, it would need to be preserved (e.g. tag identifiers by kind). Inspection of all three call sites suggests they do *not* care — all three do substring containment, not kind-based dispatch — but this needs a one-line confirmation in review.
- **Risk of test re-baseline stacking**: same as Tier 1's F1+F2+F3 stacking risk. The helper does not reduce the stacking; it makes the stack reviewable.

## "If I'm wrong, it's probably because..."

…the team genuinely intended `mechanism_signature` to be a **lossy fingerprint** rather than a normalized identifier set — i.e. case-sensitive substring with hyphen-splitting was a deliberate design choice for the dedup to fire on fragments. In that case, the helper hides the design intent under a name that overstates the invariant. The right move would instead be to **add a docstring to the existing `_extract_identifiers` and the `mechanism_signature` field** explaining the lossy-fingerprint contract, and to leave the four surgical fixes truly surgical. I weight this at ~15% — the F2 emptiness behavior makes "lossy fingerprint" hard to justify, since a lossy fingerprint should still trip the overlap guard on emptiness.

## Files to change

- `src/superclaude/cli/roadmap/integration_contracts.py` — add `_canonicalize_identifiers`, replace `_extract_identifiers` body or alias it, apply F2/F3/F4 surgical fixes at lines 339-360 and 424-441.
- `tests/roadmap/test_integration_contracts.py` — F5 comment fix; add new unit tests for the helper's three invariants (uppercase, hyphenated-as-one, empty-set semantics); permutation-order test for F4; re-baseline any assertion that depended on `S10` rather than `FR-S10-02`.

## Test plan

1. **Helper unit tests** (new):
   - `assert _canonicalize_identifiers("FR-S10-02 governs") == frozenset({"FR-S10-02"})`
   - `assert _canonicalize_identifiers("fr_s10_02") == frozenset()  # lowercase rejected at extraction`
   - `assert _canonicalize_identifiers("FR_S10_02") == frozenset({"FR_S10_02"})`
   - `assert _canonicalize_identifiers("DispatchTable") == frozenset({"DISPATCHTABLE"})`  # confirms uppercase invariant
2. **F2 regression**: empty-ident contract + roadmap line "Implement priority dispatch for logging" → `covered == False` (the bypass-to-requirement flip).
3. **F3 regression**: contract with ident `{"FR-S10-02"}` + roadmap line containing `fr-s10-02` (lowercase) → `covered == True` (uppercase canonicalization).
4. **F4 permutation**: feed `(mech, {A})` then `(mech, {A,B,C})` AND the reverse order; assert both produce the same final contract count.
5. **F5**: re-run `test_integration_contracts.py::TestSignatureSubsumed::*` with the corrected comment — the dedup now fires on the *full* `FR-S10-02` token, not the fragment `S10`. Re-baseline IC-### numbering if affected.
6. **Existing suite**: full `uv run pytest tests/roadmap/test_integration_contracts.py -v` — flag any test whose pre-PR assumption depended on case-sensitive or hyphen-split tokenization.
