# Variant 1 — proposed_hybrid (Mode A original copy)

Source: `.dev/merge-pr112/adv-spec_parser/inputs/proposed_hybrid.py`

Contracts-sourced `_REQUIREMENT_PATTERNS` dict-comprehension (Contract #8) + span-aware
inline bare-D dedup (augmentcode #111 correctness). No `_MD_TRAILING_D_RE` helper.

```python
_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    family: re.compile(rf"\b{body}\b")
    for family, body in _CONTRACTS_ID_PATTERNS.items()
}


def extract_requirement_ids(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    md_pattern = _REQUIREMENT_PATTERNS["MD"]
    md_spans: list[tuple[int, int]] = [m.span() for m in md_pattern.finditer(text)]
    for family, pattern in _REQUIREMENT_PATTERNS.items():
        if family == "D" and md_spans:
            ids = sorted(
                {
                    m.group()
                    for m in pattern.finditer(text)
                    if not any(
                        start <= m.start() and m.end() <= end
                        for (start, end) in md_spans
                    )
                }
            )
        else:
            ids = sorted(set(pattern.findall(text)))
        if ids:
            result[family] = ids
    return result
```
