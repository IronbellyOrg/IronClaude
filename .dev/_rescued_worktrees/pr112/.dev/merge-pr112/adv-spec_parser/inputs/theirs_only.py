# ---------- Requirement IDs ----------

_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    # MD must be ordered BEFORE D so milestone-prefixed deliverable IDs (M{n}-D{nn})
    # are extracted as their own family rather than being silently collapsed under
    # the bare-D family. See TASK-RF-20260531-044100 design decision D1 and
    # /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md L657 ("Deliverable ID Convention").
    "MD": re.compile(r"\bM\d+-D-?\d+\b"),
    "FR": re.compile(r"\bFR-\d+(?:\.\d+)?\b"),
    "NFR": re.compile(r"\bNFR-\d+(?:\.\d+)?\b"),
    "SC": re.compile(r"\bSC-\d+\b"),
    "G": re.compile(r"\bG-\d+\b"),
    "D": re.compile(r"\bD-?\d+\b"),
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
