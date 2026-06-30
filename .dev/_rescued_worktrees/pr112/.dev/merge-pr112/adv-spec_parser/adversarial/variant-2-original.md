# Variant 2 — ours_only (Mode A original copy)

Source: `.dev/merge-pr112/adv-spec_parser/inputs/ours_only.py` (HEAD / R0-R1 branch)

Contracts-sourced `_REQUIREMENT_PATTERNS` dict (Contract #8) + a `_MD_TRAILING_D_RE`
helper constant + a VALUE-GLOBAL post-pass dedup.

```python
_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    family: re.compile(rf"\b{body}\b")
    for family, body in _CONTRACTS_ID_PATTERNS.items()
}

_MD_TRAILING_D_RE = re.compile(r"-(D-?\d+)$")


def extract_requirement_ids(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for family, pattern in _REQUIREMENT_PATTERNS.items():
        ids = sorted(set(pattern.findall(text)))
        if ids:
            result[family] = ids

    # VALUE-GLOBAL dedup: removes a bare-D token from the D list if its VALUE
    # equals the trailing-D portion of ANY MD token — even when the bare-D is a
    # legitimate standalone occurrence at a different span.
    if "MD" in result and "D" in result:
        md_trailing_d: set[str] = set()
        for md_token in result["MD"]:
            m = _MD_TRAILING_D_RE.search(md_token)
            if m:
                md_trailing_d.add(m.group(1))
        filtered_d = [d for d in result["D"] if d not in md_trailing_d]
        if filtered_d:
            result["D"] = filtered_d
        else:
            del result["D"]

    return result
```
