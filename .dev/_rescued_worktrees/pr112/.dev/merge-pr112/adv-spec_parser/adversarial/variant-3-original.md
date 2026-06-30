# Variant 3 — theirs_only (Mode A original copy)

Source: `.dev/merge-pr112/adv-spec_parser/inputs/theirs_only.py` (origin/master, commit 93cda9c9)

HARDCODED 6-pattern `_REQUIREMENT_PATTERNS` dict (MD first) + span-aware inline bare-D dedup.

```python
_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    "MD": re.compile(r"\bM\d+-D-?\d+\b"),
    "FR": re.compile(r"\bFR-\d+(?:\.\d+)?\b"),
    "NFR": re.compile(r"\bNFR-\d+(?:\.\d+)?\b"),
    "SC": re.compile(r"\bSC-\d+\b"),
    "G": re.compile(r"\bG-\d+\b"),
    "D": re.compile(r"\bD-?\d+\b"),
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
