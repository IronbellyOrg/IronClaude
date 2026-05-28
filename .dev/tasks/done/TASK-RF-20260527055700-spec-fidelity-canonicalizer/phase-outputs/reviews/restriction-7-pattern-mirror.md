# Restriction #7 — Pattern mirrors `integration_contracts.py:445`

**Verdict:** **PASS**

## Precedent at `integration_contracts.py:445`

```python
def _canonicalize_identifiers(text: str) -> frozenset[str]:
    """Extract identifier-tokens from text into a canonical frozenset.

    Invariants:
      1. All tokens are uppercase ...
      2. Hyphenated requirement IDs ... emitted as ONE token, not split.
      3. Empty input yields an empty frozenset ...
    """
    base_tokens = _extract_identifiers(text)
    hyphen_pattern = re.compile(r"\b(?=\S*\d)(?:[A-Z][A-Z0-9]*-)+[A-Z0-9]+\b", re.IGNORECASE)
    ...
    return frozenset(t.upper() for t in (base_tokens + hyphen_tokens + hyphen_fragments))
```

## New helper at `structural_checkers.py:295`

```python
def _canonicalize_requirement_id(family: str, raw: str) -> str:
    """Canonicalize a requirement ID to enable drift-tolerant comparison.

    Mirrors the precedent in integration_contracts.py:445 (_canonicalize_identifiers,
    KNOWLEDGE.md 2026-05-25 "Fix B Merged"). Strips leading zeros within the
    numeric tail while preserving family prefix and any sub-ID structure.

    Examples:
        D01     -> D1
        ...
    """
    import re
    match = re.match(r"^([A-Z]+)([-_]?)0*(\d+)(.*)$", raw)
    if not match:
        return raw
    prefix, _input_sep, num, rest = match.groups()
    sep = "-" if len(prefix) > 1 else ""
    return f"{prefix}{sep}{num}{rest}"
```

## Shape comparison

| Criterion | Precedent | New helper | Match? |
|---|---|---|---|
| a | Module-level pure helper | ✅ | ✅ | YES |
| b | Strip-or-normalize an identifier-like input | ✅ (case, fragment extraction) | ✅ (leading zeros, separator) | YES |
| c | Returns a string-shaped value | `frozenset[str]` (collection of strings) | `str` (single string) | YES (both string-domain; granularity differs by design — per-ID vs bulk extraction) |
| d | Docstring documents the canonicalization style | ✅ (Invariants 1-3) | ✅ (Examples + Note + Forward-looking note) | YES |
| e | New helper's docstring references `integration_contracts.py:445` as the precedent | N/A | ✅ "Mirrors the precedent in integration_contracts.py:445" (line 298) | YES |

## Verdict

PASS — shape parity confirmed. Both are module-level pure helpers with explicit-invariants docstrings; the new helper's docstring explicitly cites the precedent line. Byte-equivalence is intentionally not required (the two helpers operate on different ID granularities: per-ID single-string transform vs bulk frozenset extraction from prose).
