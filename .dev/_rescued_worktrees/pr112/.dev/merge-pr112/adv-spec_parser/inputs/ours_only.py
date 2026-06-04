# ---------- Requirement IDs ----------

_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    family: re.compile(rf"\b{body}\b")
    for family, body in _CONTRACTS_ID_PATTERNS.items()
}

# Matches the trailing D-portion of a milestone-prefixed deliverable ID
# (e.g. "M1-D01" -> "D01"). Used by extract_requirement_ids to deduplicate the
# bare-D family list against MD-family tokens that would otherwise generate a
# phantom bare-D match for the same source span. Ported from PR #111 (861047c2);
# the MD *pattern body* itself lives only in superclaude.contracts.ID_PATTERNS.
_MD_TRAILING_D_RE = re.compile(r"-(D-?\d+)$")


def extract_requirement_ids(text: str) -> dict[str, list[str]]:
    """Extract requirement ID families via regex.

    Returns dict keyed by family prefix (MD, FR, NFR, SC, G, D)
    with sorted unique ID lists.

    Note: when the MD family captures a token like "M1-D01", the D family regex
    will independently match the trailing "D01" portion of the same source span.
    To preserve the family boundary (M{n}-D{nn} is a roadmap-internal deliverable
    sequence; bare D{nn} is a spec-namespace ID), we strip those trailing-D
    duplicates from the D family list when an MD match already covers them.
    """
    result: dict[str, list[str]] = {}
    for family, pattern in _REQUIREMENT_PATTERNS.items():
        ids = sorted(set(pattern.findall(text)))
        if ids:
            result[family] = ids

    # Dedup: remove bare-D tokens that are the trailing portion of an MD-family token.
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


# ---------- Function Signatures ----------
