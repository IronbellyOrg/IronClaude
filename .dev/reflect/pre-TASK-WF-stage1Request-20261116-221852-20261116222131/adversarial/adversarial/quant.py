"""Step 3 quantitative layer (deterministic, no LLM). Run from the repository root:
  uv run --no-project python -I <this file>
Metrics per the adversarial protocol: RC requirement coverage (source = the plan under audit's requirement set is
approximated by the diff-analysis point list: a variant matches a point when its text mentions the point's key terms),
IC internal consistency, SR specificity ratio, DC dependency completeness, SC section coverage."""
import json
import re
from pathlib import Path

D = Path(".dev/reflect/pre-TASK-WF-stage1Request-20261116-221852-20261116222131/adversarial/adversarial")
V = {i: (D / f"variant-{i}-original.md").read_text() for i in (1, 2, 3)}

# Requirement set = the 12 content points (C-001..C-012); key terms that signal a variant addresses the point.
POINTS = {
    "C-001": ["030154", "package id", "entry check"],
    "C-002": ["owner summary"],
    "C-003": ["protected-risk-dispute"],
    "C-004": ["35 percent"],
    "C-005": ["code-assigned severity"],
    "C-006": ["test_workflow_command"],
    "C-007": ["ruff check", "make lint"],
    "C-008": ["recorded as partial", "stays blocking"],
    "C-009": ["minor line", "every live line", "non-superseded"],
    "C-010": ["classif", "docstring"],
    "C-011": ["smoke"],
    "C-012": ["lines 3, 17", "source lines 3"],
}
VAGUE = ["appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practices"]
CONCRETE = re.compile(r"(\b\d+(\.\d+)?%?|\.py\b|\.md\b|:\d+|`[^`]+`)")
SECTION = re.compile(r"^(F\d+|coverage_judgement|reviewer_model_self_report|Verdict)", re.M)


def rc(t):
    low = t.casefold()
    hit = [p for p, keys in POINTS.items() if any(k.casefold() in low for k in keys)]
    return len(hit) / len(POINTS), hit


def sr(t):
    body = [ln for ln in t.splitlines() if ln.strip() and not ln.startswith(("persona:", "model_class:", "model:"))]
    c = sum(1 for ln in body if CONCRETE.search(ln))
    v = sum(1 for ln in body if any(w in ln.casefold() for w in VAGUE))
    return c / (c + v) if c + v else 0.0


def dc(t):
    refs = re.findall(r"\b(F\d+)\b", t)
    defined = set(re.findall(r"^(F\d+)\b", t, re.M))
    # refs to a finding id defined in the same card; references only counted when used in prose (not at line start)
    inline = [r for ln in t.splitlines() for r in re.findall(r"\b(F\d+)\b", ln[len(ln.split(' ')[0]):]) if ln.startswith("F")]
    ok = sum(1 for r in inline if r in defined)
    return (ok / len(inline)) if inline else 1.0


sec = {i: len(SECTION.findall(t)) for i, t in V.items()}
mx = max(sec.values())
out = {}
for i, t in V.items():
    r, hit = rc(t)
    ic = 1.0  # no intra-card contradiction found by the contradiction scan of diff-analysis (X-001/X-002 are cross-variant)
    s, d, c = sr(t), dc(t), sec[i] / mx
    q = 0.30 * r + 0.25 * ic + 0.15 * s + 0.15 * d + 0.15 * c
    out[i] = dict(RC=round(r, 4), matched_points=hit, IC=ic, SR=round(s, 4), DC=round(d, 4), SC=round(c, 4), quant=round(q, 4))
(D / "quant-scores.json").write_text(json.dumps(out, indent=1) + "\n")
for i, o in out.items():
    print(i, o)
