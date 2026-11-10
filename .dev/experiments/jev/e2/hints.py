"""E2 hint rendering (identical format for every router).

render(ranked_pairs, budget_tokens=1200, max_pairs=12) -> str.  One item per pair: rank, both locators
`section N.N "<title>" lines a-b`, a code-written reason.  Items are added greedily in rank order until the next one would
exceed the budget (bytes/4) or max_pairs; an item is never truncated.  Unavailable or invalid routing -> the first 12 pairs
in document order (fallback), never deletion or PASS.
"""
from __future__ import annotations

HEADER = "Reading priorities (unverified; read the complete document):"


def tokens(s: str) -> int:
    return -(-len(s.encode("utf-8")) // 4)


def locator(p) -> str:
    no = (p.section_no + " ") if p.section_no else ""
    return f'section {no}"{p.section_title}" lines {p.line_start}-{p.line_end}'


def item(rank: int, pair) -> str:
    return f"{rank}. {locator(pair.a)} <-> {locator(pair.b)}: {pair.reason or 'candidate pair'}"


def select(ranked_pairs, budget_tokens: int = 1200, max_pairs: int = 12) -> list:
    """The pairs that fit: header counted, stop at the first item that does not fit (no skipping, no truncation)."""
    used = tokens(HEADER + "\n")
    chosen = []
    for q in ranked_pairs:
        if len(chosen) >= max_pairs:
            break
        t = tokens(item(len(chosen) + 1, q) + "\n")
        if used + t > budget_tokens:
            break
        used += t
        chosen.append(q)
    return chosen


def render(ranked_pairs, budget_tokens: int = 1200, max_pairs: int = 12) -> str:
    chosen = select(ranked_pairs, budget_tokens, max_pairs)
    return HEADER + "\n" + "".join(item(i + 1, q) + "\n" for i, q in enumerate(chosen))


def document_order(pool) -> list:
    return sorted(pool, key=lambda q: (q.a.line_start, q.b.line_start, q.a.pid, q.b.pid))


def fallback_pairs(pool, max_pairs: int = 12) -> list:
    return document_order(pool)[:max_pairs]


def valid_routing(ranked, pool) -> bool:
    """A routing result is valid only if it is a list of pool pairs without duplicates."""
    if not isinstance(ranked, list) or not ranked:
        return False
    keys = {q.key for q in pool}
    seen = set()
    for q in ranked:
        if getattr(q, "key", None) not in keys or q.key in seen:
            return False
        seen.add(q.key)
    return True


def hints_or_fallback(ranked, pool, budget_tokens: int = 1200, max_pairs: int = 12):
    """-> (text, used_fallback).  Never raises on bad routing."""
    if valid_routing(ranked, pool):
        return render(ranked, budget_tokens, max_pairs), False
    fb = fallback_pairs(pool, max_pairs)
    for q in fb:
        if not q.reason:
            q.reason = "document order (routing unavailable)"
    return render(fb, budget_tokens, max_pairs), True
