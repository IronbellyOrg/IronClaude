# Precedent Pattern — `_canonicalize_identifiers` at integration_contracts.py:445

Captured: 2026-05-27 06:25 UTC
File: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/integration_contracts.py`

## Actual location

- Lines **445-469** (`def _canonicalize_identifiers` through `return frozenset(...)`).
- Module-level pure helper, called by `_check_identifier_overlap` at line 196.

## Function signature

```python
def _canonicalize_identifiers(text: str) -> frozenset[str]:
```

## Docstring + body excerpt (verbatim)

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
    base_tokens = _extract_identifiers(text)
    hyphen_pattern = re.compile(r"\b(?=\S*\d)(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b", re.IGNORECASE)
    hyphen_tokens = hyphen_pattern.findall(text)
    hyphen_fragments = _extract_identifiers(" ".join(t.upper() for t in hyphen_tokens))
    return frozenset(t.upper() for t in (base_tokens + hyphen_tokens + hyphen_fragments))
```

## Style elements to mirror in `_canonicalize_requirement_id`

1. **Module-level pure helper** — no class membership, no shared state.
2. **Docstring with explicit Invariants** — numbered, behavioral.
3. **Regex compiled with re.compile** (inline use is acceptable for the simpler regex needed here).
4. **Deterministic + idempotent return** — for identical inputs, identical output.
5. **No I/O, no logging side effects** — pure transformation.

## Differences (justified)

- The new helper takes `(family, raw) -> str` (single ID), while this precedent takes `(text) -> frozenset` (extraction from prose). Both are "canonicalize identifier representation"; the granularity differs because the consumer at `check_signatures.phantom_id` needs per-ID canonicalization for set diff classification, not bulk extraction.
- The new helper strips leading zeros in the numeric tail and preserves sub-ID dotted suffixes; the precedent normalizes case and re-emits hyphen fragments. The shape (pure helper + invariants docstring + idempotent) is what restriction #7 requires, not byte-equivalence.
