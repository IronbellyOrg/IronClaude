"""E2 candidate pool (shared machinery: all routers see the same pool).

exhaustive(passages) -> int      the n(n-1)/2 count, never sent anywhere.
prefilter(passages, cfg) -> list[Pair]   pairs with an explicit reference, a shared id, a shared backticked term or path
    basename, a shared number+unit word, or >= 2 shared rare content words (IDF within the document), capped at
    cfg["pool_cap"] pairs by a deterministic prefilter score.  All weights and the cap live in decision.toml [prefilter].
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

WORD_RE = re.compile(r"[a-z][a-z\-]{3,}")
STOPWORDS = set("""about above after again also another any are because been before being below between both but can cannot could
did does doing down during each either else even every for from further had has have having here how however into its itself just
may might more most must need needs never new nor not off once only onto other our out over own per same shall should since some such
than that the their them then there these they this those through thus too under until upon very was were what when where which
while who whom whose why will with within without would you your yours whether also use used uses using one two three four five
each when then than""".split())

DEFAULT_CFG = {
    "pool_cap": 150, "min_words": 3, "rare_frac": 0.04, "rare_min_df": 2, "min_shared_rare_words": 2,
    "w_explicit": 6.0, "w_id": 1.0, "w_term": 1.0, "w_path": 1.0, "w_numunit": 1.0, "w_word": 0.5,
}


@dataclass
class Pair:
    a: object                      # Passage (document order: a.pid < b.pid)
    b: object
    features: dict = field(default_factory=dict)
    score: float = 0.0
    reason: str = ""

    @property
    def key(self):
        return (self.a.pid, self.b.pid)


def exhaustive(passages) -> int:
    n = len(passages)
    return n * (n - 1) // 2


def eligible(passages, cfg=None):
    c = {**DEFAULT_CFG, **(cfg or {})}
    return [p for p in passages if p.kind != "heading" and not p.is_header and len(p.text.split()) >= c["min_words"]]


def _words(p):
    return {w for w in WORD_RE.findall(p.text.lower()) if w not in STOPWORDS}


def _idf(df, n):
    return math.log((n + 1) / df)


def prefilter(passages, cfg=None) -> list:
    c = {**DEFAULT_CFG, **(cfg or {})}
    return prefilter_uncapped(passages, c)[: c["pool_cap"]]


def prefilter_uncapped(passages, cfg=None) -> list:
    """Every admitted pair, sorted by the prefilter score (the pool is its first pool_cap entries)."""
    c = {**DEFAULT_CFG, **(cfg or {})}
    el = eligible(passages, c)
    n = len(el)
    if n < 2:
        return []
    words = {p.pid: _words(p) for p in el}
    all_ids = {p.pid: set(p.ids_defined) | set(p.ids_referenced) for p in el}
    df_w, df_id, df_t, df_p, df_n = {}, {}, {}, {}, {}
    for p in el:
        for w in words[p.pid]:
            df_w[w] = df_w.get(w, 0) + 1
        for x in all_ids[p.pid]:
            df_id[x] = df_id.get(x, 0) + 1
        for x in set(p.terms):
            df_t[x] = df_t.get(x, 0) + 1
        for x in set(p.paths):
            df_p[x] = df_p.get(x, 0) + 1
        for x in set(p.numbers_with_units):
            df_n[x] = df_n.get(x, 0) + 1
    rare_max = max(c["rare_min_df"], math.ceil(c["rare_frac"] * n))
    rare = {w for w, d in df_w.items() if c["rare_min_df"] <= d <= rare_max}
    defined_by = {}
    for p in el:
        for x in p.ids_defined:
            defined_by.setdefault(x, set()).add(p.pid)
    sec_to_pids = {}
    for p in el:
        if p.section_no:
            sec_to_pids.setdefault(p.section_no, set()).add(p.pid)

    def refs(src, dst):
        """src explicitly refers to dst: cites an id dst defines, or cites dst's section number."""
        out = []
        for x in src.ids_referenced:
            if dst.pid in defined_by.get(x, ()) and dst.pid != src.pid:
                out.append(x)
        for s in src.section_refs:
            if dst.section_no == s and dst.section_no != src.section_no:
                out.append("section " + s)
        return out

    pairs = []
    for i in range(n):
        a = el[i]
        for j in range(i + 1, n):
            b = el[j]
            r_ab, r_ba = refs(a, b), refs(b, a)
            sh_id = sorted(all_ids[a.pid] & all_ids[b.pid])
            sh_t = sorted(set(a.terms) & set(b.terms))
            sh_p = sorted(set(a.paths) & set(b.paths))
            sh_n = sorted(set(a.numbers_with_units) & set(b.numbers_with_units))
            sh_w = sorted((words[a.pid] & words[b.pid]) & rare)
            explicit = bool(r_ab or r_ba)
            if not (explicit or sh_id or sh_t or sh_p or sh_n or len(sh_w) >= c["min_shared_rare_words"]):
                continue
            score = (c["w_explicit"] if explicit else 0.0)
            score += c["w_id"] * sum(_idf(df_id[x], n) for x in sh_id)
            score += c["w_term"] * sum(_idf(df_t[x], n) for x in sh_t)
            score += c["w_path"] * sum(_idf(df_p[x], n) for x in sh_p)
            score += c["w_numunit"] * sum(_idf(df_n[x], n) for x in sh_n)
            score += c["w_word"] * sum(_idf(df_w[x], n) for x in sh_w)
            f = {"explicit_ab": r_ab, "explicit_ba": r_ba, "shared_ids": sh_id, "shared_terms": sh_t, "shared_paths": sh_p,
                 "shared_numunits": sh_n, "shared_rare_words": sh_w}
            pairs.append(Pair(a=a, b=b, features=f, score=round(score, 9)))
    pairs.sort(key=lambda q: (-q.score, q.a.pid, q.b.pid))
    return pairs
