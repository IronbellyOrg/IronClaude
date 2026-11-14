"""Deterministic quantitative layer for the adversarial base selection (5 metrics, weights 0.30/0.25/0.15/0.15/0.15).

Run: uv run python quant.py <adversarial-dir>
Heuristic by design: every number is computed from the variant text with regexes, so two runs give the same output.
"""
import json
import re
import sys
from pathlib import Path

A = Path(sys.argv[1])
texts = [(A / f"variant-{i}-original.md").read_text() for i in (1, 2, 3)]

# RC: requirements taken from the seed brief (constraints + success criteria); a requirement is covered when its regex matches.
REQS = {
    "two redesigns": r"redesign (a|b|1|2)\b|3\.1 redesign|3\.2 redesign",
    "mechanism and step order": r"order of steps|exact order|mechanism",
    "quoted draft wording": r"draft wording|quoted draft|draft brief wording|brief additions",
    "model roles per panel": r"model roles",
    "time budget in seconds": r"time budget",
    "+35% arithmetic vs named baseline": r"1\.35|\+35%",
    "critical path identified": r"critical path",
    "idle time reallocation": r"idle|slack",
    "coverage matrix over ten issues": r"coverage matrix",
    "per-run probabilities": r"p low-high|per run\b|p\(reach\)",
    "overfitting safeguard": r"anti-overfitting|overfitting",
    "gain low-high per run": r"expected gain",
    "harness share vs redesign share": r"redesign share|harness share|share from the redesign|harness fixes h1",
    "overhead (time and tokens)": r"overhead",
    "implementation effort": r"implementation effort",
    "failure modes": r"failure modes?",
    "three theories T1-T3": r"\bt1\b[\s\S]*\bt2\b[\s\S]*\bt3\b",
    "redesign-to-theory mapping": r"mapping of (the )?redesigns|theories addressed|answers? the open question|t1 and t2 primary",
    "defect classes with generality evidence": r"recurrence|recorded instance",
    "other review targets (spec, docs)": r"specification|documentation",
    "comparison table": r"comparison of the two redesigns|### 3\.4 comparison|## 4\. comparison",
    "hold-out validation experiment": r"validation experiment|hold-out",
    "pre-registered decision rule": r"pre-registered|decision rule",
    "numbered testable requirements": r"\b(req-\d+|r-\d+)\b|^\d+\. ",
    "no ground-truth quotes rule": r"ground[- ]truth",
    "findings-v1 contract kept": r"findings-v1",
    "reviewers stay read-only": r"read-only|disallowedtools",
    "cheap models only / panels": r"haiku \+ 2x luna",
}
CONC = re.compile(
    r"\b\d+(\.\d+)?\s?(s|%|k|kb|lines|tokens|runs|characters|items|x)\b|\b(req|r)-\d+\b|`[^`\n]+`|\b[a-z]+\.py\b",
    re.I,
)
VAGUE = re.compile(
    r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices)\b", re.I
)
# Contradictions: points of diff-analysis.md where the variant is on the wrong side of a checked fact (see base-selection.md).
CONTRA = {1: ["X-001", "X-002", "X-005", "X-008"], 2: ["X-005(1.6x deadline)", "3(f) sums H and redesign"], 3: ["X-001", "X-003", "X-004", "X-005", "X-006", "X-007"]}


def claims(t):
    return [ln for ln in t.splitlines() if re.search(r"\d", ln) and len(ln) > 25]


def h2(t):
    return len([ln for ln in t.splitlines() if ln.startswith("## ")])


def refs(t):
    heads = set()
    for ln in t.splitlines():
        m = re.match(r"#{2,4}\s+(\d+(?:\.\d+)?)", ln)
        if m:
            heads.add(m.group(1))
    ids = set(re.findall(r"\|\s*((?:REQ|R)-\d+)\s*\|", t))
    nums = set(re.findall(r"^(\d+)\.\s", t, re.M))
    total = res = 0
    for m in re.finditer(r"\b(?:section|§)\s*(\d+(?:\.\d+)?)", t, re.I):
        total += 1
        res += m.group(1) in heads
    for m in re.finditer(r"\b((?:REQ|R)-\d+)\b", t):
        if m.group(1) in ids:
            total += 1
            res += 1
        elif not re.search(r"\|\s*" + re.escape(m.group(1)) + r"\s*\|", t):
            total += 1
    for m in re.finditer(r"\(see (\d+(?:\.\d+)?)", t, re.I):
        total += 1
        res += m.group(1) in heads
    for m in re.finditer(r"\b(\d\.\d)\([a-i]\)", t):
        total += 1
        res += m.group(1) in heads
    return res, total


max_h2 = max(h2(t) for t in texts)
out = {}
for i, t in enumerate(texts, 1):
    low = t.lower()
    cov = {k: bool(re.search(p, low, re.M)) for k, p in REQS.items()}
    rc = sum(cov.values()) / len(cov)
    n_claims = len(claims(t))
    ic = 1 - len(CONTRA[i]) / n_claims
    conc = len(CONC.findall(t))
    vag = len(VAGUE.findall(t))
    sr = conc / (conc + vag)
    r, tot = refs(t)
    dc = r / tot if tot else 1.0
    sc = h2(t) / max_h2
    q = 0.30 * rc + 0.25 * ic + 0.15 * sr + 0.15 * dc + 0.15 * sc
    out[f"V{i}"] = dict(
        RC=round(rc, 4), RC_detail=f"{sum(cov.values())}/{len(cov)} missing={[k for k, v in cov.items() if not v]}",
        IC=round(ic, 4), IC_detail=f"{len(CONTRA[i])} contradictions / {n_claims} claims",
        SR=round(sr, 4), SR_detail=f"{conc} concrete / {vag} vague",
        DC=round(dc, 4), DC_detail=f"{r} resolved / {tot} references",
        SC=round(sc, 4), SC_detail=f"{h2(t)} H2 sections, max {max_h2}",
        quant=round(q, 4),
    )
print(json.dumps(out, indent=2))
