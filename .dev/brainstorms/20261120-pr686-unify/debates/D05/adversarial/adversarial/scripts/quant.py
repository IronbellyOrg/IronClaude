"""Deterministic quantitative layer for D05 (Step 3 of /sc:adversarial). Read-only on inputs.

Usage: uv run python -I quant.py variant-1-original.md variant-2-original.md
Metrics: RC requirement coverage, IC internal consistency, SR specificity, DC dependency
completeness, SC section coverage. Requirements are the elements BRIEF-COMMON asks of a
position paper (no formal requirement IDs exist, so section-level matching is used).
"""
import re
import sys

REQUIRED = [
    ("claim", r"^## Claim"),
    ("mechanism", r"^## Mechanism"),
    ("cited facts (5 to 10)", r"^## Cited facts"),
    ("costs", r"^## What it costs"),
    ("risks", r"^## What it risks"),
    ("gets right", r"^## What it gets right"),
]
# Intra-variant contradictions found in diff-analysis.md (X-001, X-003 are OURS-side tensions,
# both conceded by the OURS advocate; X-002 is an omission in CLAY, not a contradiction).
CONTRADICTIONS = {"variant-1-original.md": 2, "variant-2-original.md": 0}
VAGUE = [
    "appropriate", "as needed", "properly", "adequate", "should consider", "might", "various",
    "etc.", "best practices", "industry standard",
]


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}.*?$(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def score(path, max_sections):
    text = open(path, encoding="utf-8").read()
    h2 = re.findall(r"^## ", text, re.M)
    facts = len(re.findall(r"^\d+\. ", section(text, "Cited facts"), re.M))
    matched = 0
    for name, pat in REQUIRED:
        ok = re.search(pat, text, re.M) is not None
        if name.startswith("cited facts"):
            ok = ok and 5 <= facts <= 10
        matched += ok
    rc = matched / len(REQUIRED)
    claims = facts + len(re.findall(r"^\d+\. ", section(text, "Mechanism"), re.M))
    ic = 1 - CONTRADICTIONS[path.split("/")[-1]] / claims
    body = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    concrete = len(re.findall(r"\d+", body)) + len(re.findall(r"`[^`]+`", body))
    low = body.lower()
    vague = sum(low.count(v) for v in VAGUE)
    sr = concrete / (concrete + vague)
    # internal references: "fact N", "Mechanism N", "item N" resolve when that number exists
    refs = re.findall(r"\b(?:fact|facts|item|mechanism)s? (\d+)\b", body, re.I)
    resolved = [r for r in refs if int(r) <= max(facts, 4)]
    dc = (len(resolved) / len(refs)) if refs else 1.0
    sc = len(h2) / max_sections
    quant = rc * 0.30 + ic * 0.25 + sr * 0.15 + dc * 0.15 + sc * 0.15
    return dict(file=path, h2=len(h2), facts=facts, claims=claims, concrete=concrete,
                vague=vague, refs=len(refs), RC=rc, IC=ic, SR=sr, DC=dc, SC=sc, quant=quant)


paths = sys.argv[1:]
max_h2 = max(len(re.findall(r"^## ", open(p, encoding="utf-8").read(), re.M)) for p in paths)
for p in paths:
    r = score(p, max_h2)
    print(" ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}" for k, v in r.items()))
