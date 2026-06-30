<!-- Provenance: This document was produced by /sc:adversarial (Mode A, --depth quick) -->
<!-- Base: Variant 1 (proposed_hybrid) -->
<!-- Merge date: 2026-06-04 -->

# Merged Resolution — spec_parser.py Requirement-IDs region

<!-- Source: Base (Variant 1, proposed_hybrid) — selected as merge base; no further changes -->

The adversarial comparison selected **Variant 1 (proposed_hybrid)** as the merged artifact verbatim.
The full resolved file is the separately written
`/config/workspace/IronClaude-RoadmapRewrite/.dev/merge-pr112/spec_parser.py.resolved`.
This is the conflict-region payload of that file:

```python
# ---------- Requirement IDs ----------

# R0.3 + R5 (PR #111 port): the family→pattern table is derived from the
# canonical contracts registry (Contract #8 — no duplicate regex literals).
# superclaude.contracts.ID_PATTERNS enumerates the families in canonical
# order with MD FIRST and D LAST, which is exactly the ordering the
# milestone-prefixed deliverable (M{n}-D{nn}) handling requires.
_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    family: re.compile(rf"\b{body}\b")
    for family, body in _CONTRACTS_ID_PATTERNS.items()
}


def extract_requirement_ids(text: str) -> dict[str, list[str]]:
    """Extract requirement ID families via regex. (MD, FR, NFR, SC, G, D)

    Span-aware bare-D dedup: a bare-D match is suppressed only when its
    character span is contained within an MD-family match's span — preserving
    a legitimate standalone "D01" that shares a value with an "M1-D01" tail
    elsewhere (augmentcode #111).
    """
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

## Verdict
- **Status:** PASS
- **Convergence:** 1.00 (3/3 diff points resolved unanimously)
- **Confidence:** 0.93 → raised to 0.97 after empirically confirming V1 passes both master MD-family tests
- **Selected base:** Variant 1 (proposed_hybrid)
- **Unresolved conflicts:** 0
- **HIGH-severity unaddressed invariants:** none
