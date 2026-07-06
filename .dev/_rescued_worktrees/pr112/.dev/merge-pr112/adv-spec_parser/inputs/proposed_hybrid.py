# ---------- Requirement IDs ----------

# R0.3 + R5 (PR #111 port): the family→pattern table is derived from the
# canonical contracts registry (Contract #8 — no duplicate regex literals).
# ``superclaude.contracts.ID_PATTERNS`` enumerates the families in canonical
# order with ``MD`` FIRST and ``D`` LAST, which is exactly the ordering the
# milestone-prefixed deliverable (``M{n}-D{nn}``) handling requires: MD is
# matched as its own family rather than being silently collapsed under the
# bare-D family. The word-boundary anchors ``\b…\b`` are a local rendering
# concern and are NOT part of the SoT body.
_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    family: re.compile(rf"\b{body}\b")
    for family, body in _CONTRACTS_ID_PATTERNS.items()
}


def extract_requirement_ids(text: str) -> dict[str, list[str]]:
    """Extract requirement ID families via regex.

    Returns dict keyed by family prefix (MD, FR, NFR, SC, G, D)
    with sorted unique ID lists.

    Note: when the MD family captures a token like "M1-D01", the bare-D regex
    (``\\bD-?\\d+\\b``) will independently match the trailing "D01" portion of the
    *same source span*. To preserve the family boundary (M{n}-D{nn} is a
    roadmap-internal deliverable sequence; bare D{nn} is a spec-namespace ID),
    we drop those phantom bare-D matches.

    The dedup is *span-aware*, not value-global: a bare-D match is suppressed only
    when its character span is contained within an MD-family match's span. This
    preserves a legitimate standalone "D01" that happens to share its value with
    the trailing portion of some "M1-D01" elsewhere in the document — value-global
    membership dedup would wrongly drop it (augmentcode #111).
    """
    result: dict[str, list[str]] = {}

    # Collect MD-family match spans up front; bare-D matches whose span falls
    # inside one of these are the phantom trailing-D portions we must suppress.
    md_pattern = _REQUIREMENT_PATTERNS["MD"]
    md_spans: list[tuple[int, int]] = [m.span() for m in md_pattern.finditer(text)]

    for family, pattern in _REQUIREMENT_PATTERNS.items():
        if family == "D" and md_spans:
            # Span-aware: keep a bare-D occurrence unless it is contained within
            # an MD-family span (i.e. it is the "-D01" tail of an "M1-D01" token).
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


# ---------- Function Signatures ----------
