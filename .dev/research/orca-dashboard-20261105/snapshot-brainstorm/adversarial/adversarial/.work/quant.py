"""Deterministic quantitative metrics (scoring-protocol A.1) for the 3 variants.

Usage: uv run python quant.py
Rules (fixed before running; no judgment):
- Statement: a non-blank line outside ``` fences that is not a heading,
  table separator or HTML comment.
- RC: seed brief has no requirement IDs, so section-level topic matching:
  26 topics from the seed's Constraints, Success Criteria and Open
  Questions, each a fixed regex; RC = topics matched / 26.
- IC: 1 - internal contradictions / scorable claims. Internal contradiction
  counts come from diff-analysis.md (V1: X-005, X-006, X-010; V2: X-007,
  X-008, X-009; V3: none). Scorable claim = statement with a concrete or
  normative indicator.
- SR: concrete statements / (concrete + vague), vague list = protocol list.
- DC: internal refs (s.N[.M], section N[.M], requirement/gate/task IDs)
  resolved against heading numbers and ID definitions in the same variant.
- SC: H2 count / max H2 count.
"""
import re
from pathlib import Path

ART = Path(__file__).resolve().parent.parent
VARS = {"V1": "variant-1-opus-architect.md", "V2": "variant-2-sonnet-analyzer.md",
        "V3": "variant-3-haiku-backend.md"}
CONTRA = {"V1": 3, "V2": 3, "V3": 0}
TOPICS = {
    "ascii_fenced": r"ASCII", "no_ansi_required": r"ANSI",
    "80_columns": r"80[- ]col|80 col|80-column|78[- ]col",
    "owner_requester": r"owner|requester", "impact_evidence": r"impact",
    "unanswered_context": r"unanswered|unresolved", "heartbeat": r"heartbeat",
    "no_double_count": r"counted once|count(ed)? once|double[- ]count",
    "as_of": r"as[- ]of", "scope": r"\bscope\b", "freshness": r"fresh",
    "missing_sources": r"missing", "paging": r"\bpag(e|es|ing)\b",
    "omitted_rows": r"omitted", "not_urgent_alert": r"urgent|alert",
    "last_successful": r"last successful", "unknown_not_zero": r"unknown",
    "cost_token_denominator": r"\btoken|\bcost", "synthetic": r"synthetic",
    "oldest_blocking": r"oldest", "state_empty": r"empty",
    "state_busy": r"busy", "state_stale": r"stale",
    "state_checks_failing": r"checks? fail|failing check",
    "evaluation_tasks": r"evaluation", "feasibility_gate": r"feasibility",
}
CONCRETE = re.compile(
    r"\d|`|\b(Orca|ASCII|ANSI|NDJSON|JSON|AgentHUD|Agent Deck|gh-dash|otel-tui"
    r"|btop|PagerDuty|Dolphie|DEMO|REPORT\.md)\b")
NORMATIVE = re.compile(r"\b(must|never|always|only|exactly|at least|at most)\b", re.I)
VAGUE = re.compile(r"\b(appropriate|appropriately|as needed|properly|adequate|"
                   r"adequately|should consider|might|various|etc\.?|best practices?|"
                   r"industry standard)\b", re.I)
IDREF = re.compile(r"\b(R-[A-Z]{3}-\d{2}|R\d{2}|(?:DEC|BLK|COM|CHG|VER|COV|FMT|OVF)-\d"
                   r"|EV-\d+|ET-\d+|MC-\d|FG-\d|G0\d|G\d|E0\d)\b")
SECREF = re.compile(r"\b(?:s\.|[Ss]ection )(\d+(?:\.\d+)?)")


def statements(text):
    out, fence = [], False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        s = ln.strip()
        if fence or not s or s.startswith("#") or s.startswith("<!--"):
            continue
        if re.fullmatch(r"\|?[\s:|-]+\|?", s):
            continue
        out.append(s)
    return out


def metrics(text, h2max):
    st = statements(text)
    prose = "\n".join(st)
    rc_hits = {k: bool(re.search(v, text, re.I)) for k, v in TOPICS.items()}
    claims = [s for s in st if CONCRETE.search(s) or NORMATIVE.search(s)]
    conc = sum(1 for s in st if CONCRETE.search(s))
    vague = sum(1 for s in st if VAGUE.search(s))
    heads = set(re.findall(r"^#{2,4} (\d+(?:\.\d+)?)[. ]", text, re.M))
    secrefs = SECREF.findall(prose)
    sec_ok = [r for r in secrefs if r in heads or r.split(".")[0] in heads and "." not in r]
    defined = set()
    for ln in text.splitlines():
        m = re.match(r"^\|\s*\**([A-Z][A-Z0-9-]*\d)\**[\s|]", ln.strip()) or \
            re.match(r"^[-*]?\s*\**([A-Z][A-Z0-9-]*\d)\**[:.)\s]", ln.strip())
        if m:
            defined.add(m.group(1))
    idrefs = IDREF.findall(prose)
    id_ok = [r for r in idrefs if r in defined]
    refs, ok = len(secrefs) + len(idrefs), len(sec_ok) + len(id_ok)
    h2 = len(re.findall(r"^## ", text, re.M))
    return {
        "RC": sum(rc_hits.values()) / len(TOPICS), "rc_miss": [k for k, v in rc_hits.items() if not v],
        "claims": len(claims), "concrete": conc, "vague": vague,
        "refs": refs, "resolved": ok,
        "unresolved": sorted(set(r for r in secrefs if r not in sec_ok)
                             | set(r for r in idrefs if r not in id_ok)),
        "h2": h2,
    }


def main():
    texts = {k: (ART / f).read_text() for k, f in VARS.items()}
    h2max = max(len(re.findall(r"^## ", t, re.M)) for t in texts.values())
    for k, t in texts.items():
        m = metrics(t, h2max)
        ic = 1 - CONTRA[k] / m["claims"]
        sr = m["concrete"] / (m["concrete"] + m["vague"])
        dc = m["resolved"] / m["refs"] if m["refs"] else 1.0
        sc = m["h2"] / h2max
        q = m["RC"] * .30 + ic * .25 + sr * .15 + dc * .15 + sc * .15
        print(f"{k}: RC={m['RC']:.3f} miss={m['rc_miss']} | IC={ic:.3f} "
              f"({CONTRA[k]}/{m['claims']}) | SR={sr:.3f} ({m['concrete']}/"
              f"{m['concrete']}+{m['vague']}) | DC={dc:.3f} ({m['resolved']}/{m['refs']}) "
              f"unresolved={m['unresolved']} | SC={sc:.3f} ({m['h2']}/{h2max}) | quant={q:.3f}")


if __name__ == "__main__":
    main()
