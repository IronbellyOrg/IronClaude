"""Quantitative layer of base selection (RC, IC, SR, DC, SC), deterministic.

Usage: uv run python quant.py <adversarial-dir>
Writes <adversarial-dir>/scoring/quant.md and quant.json.
Running it twice on the same input gives identical output.
"""
import json
import re
import sys
from pathlib import Path

adv = Path(sys.argv[1])
out_dir = adv / "scoring"
files = {"A": adv / "variant-1-original.md", "B": adv / "variant-2-original.md", "C": adv / "variant-3-original.md"}

# RC: source requirements = the seed brief's eight questions, constraints and open questions (no formal IDs exist,
# so section-level topic matching is used, as the protocol allows). One regex per requirement.
REQS = {
    "Q1 events and what a hook can see": r"Hook can see|Visible to",
    "Q2 policy format, scope, storage, loading": r"model-policy\.json",
    "Q3 Jev vs code: cost and failure behaviour": r"\$0\.000025.*|0\.000025",
    "Q3 offline test plan on labelled calls": r"[Ll]abel",
    "Q4 rejection message": r"Blocked:",
    "Q4 override recording": r"[Oo]verride|[Gg]rant",
    "Q5 bypass resistance": r"[Bb]ypass",
    "Q6 time cost per event": r"Typical|typical",
    "Q7 numbered REQ with verification": r"REQ-01",
    "Q8 implementation plan in IronClaude layout": r"install_hooks",
    "room for version 2": r"[Vv]ersion 2|v2",
    "never rewrites a model": r"never (picks|rewrites|changes)|updatedInput|never rewrite",
    "states what it cannot see": r"[Cc]eiling",
    "missing or malformed policy per event": r"[Mm]alformed",
    "fits layout: sync-dev": r"sync-dev",
    "open question: scope all sessions vs governed": r"all sessions|governed",
    "open question: /model and UserPromptSubmit": r"UserPromptSubmit",
    "open question: availableModels per child": r"availableModels",
    "open question: Jev needed in v1": r"[Nn]o Jev|no Jev call|v1 needs no Jev",
}
# IC: intra-variant contradictions found in the debate (round 2 evidence) and claims = REQ count + event-table rows.
CONTRA = {
    "A": ["row 10 'blocks or records' vs row 11 'not rejected' for /model", "line 156 'Jev can never turn a block into an allow' vs line 159 allow-and-log on failure"],
    "B": ["line 89 class (b) 'a ceiling, not a judgment problem' vs line 92 it triggers the measured-need rule"],
    "C": ["E7 native list 'generated from the same policy' vs section 9 generation left to v2", "heredoc 'scanned as text' vs shell-stdin heredoc listed as a ceiling", "MP-07/REQ-31 need Edit, Write, NotebookEdit but the PreToolUse matcher omits them"],
}
EVENT_ROWS = {"A": 16, "B": 16, "C": 9}

CONCRETE = [
    r"\b\d+(\.\d+)?\s?(ms|KB|MB|%|h|s)\b",
    r"\b[\w./-]+\.(py|sh|json|md|jsonl):\d+",
    r"\bREQ-\d+\b",
    r"\bMP-[A-Z0-9-]+\b",
    r"\bp\s?(of at least|above|>=|≥)?\s?0\.\d+",
]
VAGUE = [r"as appropriate", r"as needed", r"\bproperly\b", r"\badequate", r"should consider", r"\bmight\b", r"\bvarious\b", r"\betc\.", r"best practices?", r"\bprobably\b", r"\bsomewhat\b"]


def count(patterns, text):
    return sum(len(re.findall(p, text, flags=re.I)) for p in patterns)


res = {}
sec_counts = {}
for v, p in files.items():
    t = p.read_text()
    sec_counts[v] = len(re.findall(r"^## ", t, flags=re.M))
mx = max(sec_counts.values())
for v, p in files.items():
    t = p.read_text()
    matched = [k for k, rx in REQS.items() if re.search(rx, t)]
    rc = len(matched) / len(REQS)
    nreq = len(set(re.findall(r"\bREQ-(\d+)\b", t)))
    claims = nreq + EVENT_ROWS[v]
    ic = 1 - len(CONTRA[v]) / claims
    conc, vag = count(CONCRETE, t), count(VAGUE, t)
    sr = conc / (conc + vag)
    defs = set(re.findall(r"^(?:\||-|\*)\s*\**REQ-(\d+)", t, flags=re.M))
    refs = set(re.findall(r"\bREQ-(\d+)\b", t))
    heads = set(re.findall(r"^## (\d+)\.", t, flags=re.M))
    sec_refs = set(re.findall(r"\bsection (\d+)\b", t, flags=re.I))
    total_refs = len(refs) + len(sec_refs)
    resolved = len(refs & defs) + len(sec_refs & heads)
    dc = resolved / total_refs if total_refs else 1.0
    sc = sec_counts[v] / mx
    q = 0.30 * rc + 0.25 * ic + 0.15 * sr + 0.15 * dc + 0.15 * sc
    res[v] = dict(RC=rc, IC=ic, SR=sr, DC=dc, SC=sc, quant=q, rc_missing=[k for k in REQS if k not in matched], contradictions=CONTRA[v], claims=claims, concrete=conc, vague=vag, refs=total_refs, resolved=resolved, sections=sec_counts[v])

lines = ["# Quantitative scoring (50% weight), deterministic", "", "| Metric | Weight | Variant A | Variant B | Variant C |", "|---|---|---|---|---|"]
for k, w, d in [("requirement_coverage", 0.30, "RC"), ("internal_consistency", 0.25, "IC"), ("specificity_ratio", 0.15, "SR"), ("dependency_completeness", 0.15, "DC"), ("section_coverage", 0.15, "SC")]:
    lines.append(f"| {k} | {w:.2f} | " + " | ".join(f"{res[v][d]:.4f}" for v in "ABC") + " |")
lines.append("| **quant_score** | | " + " | ".join(f"**{res[v]['quant']:.4f}**" for v in "ABC") + " |")
lines += ["", "## Detail", ""]
for v in "ABC":
    r = res[v]
    lines.append(f"- {v}: RC {len(REQS) - len(r['rc_missing'])}/{len(REQS)} requirements matched (missing: {r['rc_missing'] or 'none'}); IC {len(r['contradictions'])} intra-variant contradictions over {r['claims']} claims: {r['contradictions']}; SR concrete {r['concrete']} vs vague {r['vague']}; DC resolved {r['resolved']}/{r['refs']} references; SC {r['sections']} H2 sections (max {mx}).")
out_dir.mkdir(exist_ok=True)
(out_dir / "quant.md").write_text("\n".join(lines) + "\n")
(out_dir / "quant.json").write_text(json.dumps(res, indent=1))
print("\n".join(lines[:9]))
