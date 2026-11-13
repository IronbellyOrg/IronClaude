"""Deterministic quantitative layer for Step 3 (RC, IC, SR, DC, SC). Usage: uv run python scoring/quant.py"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
V = {i: (D / f"variant-{i}-original.md").read_text() for i in range(1, 6)}
DIFF = (D / "diff-analysis.md").read_text()

# Requirements from the seed brief (Constraints + Success Criteria + Open Questions), one regex each.
REQS = {
    "five redesigns": r"[Ff]ive redesigns|Redesign 5|D5\b|R5\b",
    "schedule when/how often": r"how often|frequency|[Ss]chedule",
    "message size": r"chars|characters|size cap|bytes",
    "transport rationale": r"[Tt]ransport",
    "Orca mail evaluated": r"Orca",
    "SendMessage evaluated": r"SendMessage|cross-session",
    "A2A evaluated": r"A2A",
    "JSON files evaluated": r"JSON|jsonl",
    "+35% cap arithmetic": r"35 ?%",
    "contamination safeguards": r"[Cc]ontaminat|anchoring",
    "convergence alarm": r"[Cc]onvergence|Jaccard",
    "gain estimate": r"[Gg]ain",
    "B1": r"\bB1\b", "B2": r"\bB2\b", "B5": r"\bB5\b", "B6": r"\bB6\b", "B8": r"\bB8\b",
    "I1": r"\bI1\b", "I4": r"\bI4\b", "I5": r"\bI5\b", "I6": r"\bI6\b", "I7": r"\bI7\b",
    "three theories": r"\bT1\b.*|Theor", "T2": r"\bT2\b", "T3": r"\bT3\b",
    "first experiment": r"[Ff]irst experiment",
    "blind judge": r"judge",
    "read-only reviewers": r"read-only",
    "no ground truth": r"ground truth|ground-truth",
    "findings-v1 / ledger": r"findings-v1",
    "models ember/luna/haiku": r"ember.*luna|luna.*ember",
    "sonnet/grok": r"sonnet|grok",
    "harness vs collaboration share": r"harness",
    "headless claude -p": r"claude -p",
    "baselines 348/300/715/821": r"348|\b300 s|715|821",
}
CONCRETE = re.compile(r"\d+(\.\d+)?\s*(s|%|KB|chars|characters|runs|tokens)\b|\b\d+ of \d+\b|[<>]=?\s*\d|`[^`]+`|\b[BI][1-8]\b")
VAGUE = re.compile(r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices?|industry standard)\b", re.I)
REF = re.compile(r"\b(?:Redesign|Design|section|Section|§)\s?(\d+(?:\.\d+)?)|\b(R-\d{2}|REQ-[A-Z]+\d+|H-\d+)\b")


def grid_errors(i):
    rows = [l for l in DIFF.splitlines() if re.match(rf"^\| V{i}-", l)]
    n = sum(l.count("ERROR") for l in rows)
    if i == 3:
        n += 1  # X-006: V3 req 6 contradicts its own R1 (diff-analysis Contradictions)
    return n


def metrics(i):
    t = V[i]
    lines = [l for l in t.splitlines() if l.strip() and not l.startswith("#")]
    rc = sum(bool(re.search(p, t)) for p in REQS.values()) / len(REQS)
    claims = sum(bool(re.search(r"\d", l)) for l in lines)
    ic = 1 - grid_errors(i) / claims
    c, v = sum(len(CONCRETE.findall(l)) for l in lines), sum(len(VAGUE.findall(l)) for l in lines)
    sr = c / (c + v)
    heads = " ".join(re.findall(r"^#+ .*$", t, re.M))
    defined = set(re.findall(r"\b(R-\d{2}|REQ-[A-Z]+\d+|H-\d+)\b\s*[.:|*]", t)) | set(re.findall(r"^\|\s*\**(R-\d{2}|REQ-[A-Z]+\d+|H-\d+)", t, re.M)) | set(re.findall(r"^\s*[-*\d.]*\s*\**(R-\d{2}|REQ-[A-Z]+\d+|H-\d+)", t, re.M))
    tot = res = 0
    for m in REF.finditer(t):
        tot += 1
        num, rid = m.group(1), m.group(2)
        if num:
            res += bool(re.search(rf"(^|\s){re.escape(num)}[.: ]|Redesign {re.escape(num)}\b|[DR]{re.escape(num)}\b", heads))
        else:
            res += rid in defined
    dc = res / tot if tot else 1.0
    return rc, ic, sr, dc, len(re.findall(r"^## ", t, re.M)), (grid_errors(i), claims, c, v, res, tot)


rows = {i: metrics(i) for i in V}
mx = max(r[4] for r in rows.values())
print("| Variant | RC | IC | SR | DC | SC | quant | detail (errors/claims, concrete/vague, refs resolved/total) |")
print("|---|---|---|---|---|---|---|---|")
for i, (rc, ic, sr, dc, h2, d) in rows.items():
    sc = h2 / mx
    q = rc * .30 + ic * .25 + sr * .15 + dc * .15 + sc * .15
    print(f"| V{i} | {rc:.3f} | {ic:.3f} | {sr:.3f} | {dc:.3f} | {sc:.3f} | {q:.3f} | {d[0]}/{d[1]}, {d[2]}/{d[3]}, {d[4]}/{d[5]} |")
