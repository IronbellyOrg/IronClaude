"""Deterministic quantitative layer (Step 3, scorer pass 1) for slot C-07 (dispatch-and-launch-mechanism).

Run: uv run python quant-score.py   (writes quant-score-output.json next to this file and prints it)

Formulas are those of sc-adversarial-protocol refs/scoring-protocol.md A.1:
  quant = 0.30*RC + 0.25*IC + 0.15*SR + 0.15*DC + 0.15*SC
No LLM judgment is used here; the only judgment inputs are the requirement-topic list (provenance below)
and the intra-variant contradiction counts (provenance below), both fixed in this file.
"""
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent
V = {
    "A": (D / "variant-1-original.md").read_text(),  # Variant 1 = Proposal A
    "B": (D / "variant-2-original.md").read_text(),  # Variant 2 = Proposal B
}

# ---------------------------------------------------------------------------------------------
# RC: requirement topics.
# Provenance: the source has no formal requirement IDs (FR-/NFR-/R-), so the protocol edge case
# "section-level topic matching" applies. Topics come from (a) the C-07 row of
# phase-outputs/discovery/undecidable-conflicts.md (positions, "Why undecidable", research files
# 04, 03, 06, 07, 13, GQ-049, invariants INV-G/INV-L/INV-F) and (b) the position-paper template
# sections the variants were asked to fill (design consequence, evidence, invariants, PR-review and
# rf-qa effect, test or measurement, strongest objection, consistency with C-01/C-02/C-03).
# A topic is matched when its regex matches anywhere in the variant text.
# ---------------------------------------------------------------------------------------------
REQ = {
    # from the two positions in the C-07 row
    "T01 raw-id launcher (claude -p --model <raw id>)": r"claude -p|raw[- ]id|raw model id",
    "T02 class-word Agent call": r"class[- ]word",
    "T03 read-only reflect-reviewer": r"reflect-reviewer",
    "T04 reflect profile ceiling": r"ceiling|_REFLECT_LAUNCH",
    "T05 gateway models": r"\bgateway\b",
    "T06 transcript identity check": r"identity check|message\.model|model_observed|transcript",
    "T07 Agent model enum": r"\benum\b",
    "T08 swarm HTTP transport": r"\bswarm\b",
    # from 'Why undecidable' in the C-07 row
    # same-line (paragraph-level) co-occurrence; a first draft limited it to one sentence, which mis-specified the topic
    "T09 reach vs mechanical read-only trade-off": r"read-only[^\n]{0,400}\breach\b|\breach\b[^\n]{0,400}read-only",
    "T10 Claude Code behaviours not pinned by the repo": r"not pin|does not pin|not pinned|unpinned",
    "T11 resolvedModel named": r"resolvedModel",
    "T12 family-alias resolution not verified": r"family-alias|family alias",
    "T13 no cost or quality comparison of the paths": r"CO-10|cost[^.\n]{0,60}(never measured|absent|unmeasured|not measured)|no run compares|never been compared|comparison no run",
    "T14 E2 sessions leave Bash open": r"Bash[^.\n]{0,60}(open|left open)|leaves Bash open|Bash stays open",
    # invariants named in the row
    "T15 INV-G": r"INV-G",
    "T16 INV-L": r"INV-L",
    "T17 INV-F": r"INV-F",
    # research files and open question named in the row
    "T18 research 04 cited": r"\br04\b|research/04",
    "T19 research 03 cited": r"\br03\b|research/03",
    "T20 research 06 cited": r"\br06\b|research/06",
    "T21 research 07 cited": r"\br07\b|research/07",
    "T22 research 13 cited": r"\br13\b|research/13",
    "T23 GQ-049": r"GQ-049",
    # position-paper template sections
    "T24 test or measurement": r"[Tt]est or measurement|\bM-\d\b|measurements? (?:that|on existing)",
    "T25 strongest objection answered": r"[Ss]trongest objection",
    "T26 PR-review effect": r"PR review|PR code review",
    "T27 rf-qa effect": r"rf-qa",
    "T28 consistency with C-01, C-02 and C-03 stated": r"(?s)(?=.*C-01)(?=.*C-02)(?=.*C-03)(?=.*(?:adjudicated|Consistent|consistency))",
    "T29 swarm/gateway env data map (launch map)": r"`launch`",
    "T30 shadow mode (INV-L) edit fence": r"edit fence|shadow",
}

TAG_RE = re.compile(r"\[(?:CODE-VERIFIED|CODE-CONTRADICTED|UNVERIFIED|VERIFIED|OBSERVED-RUNTIME)[^\]]*\]")
LEGEND_RE = re.compile(r"^(Citation form|Citation tags|Tags):")
META_RE = re.compile(r"^(Status|Position|Conflict IDs|Code state|Citation form|Citation tags):")
VAGUE_RE = re.compile(
    r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices|industry standard)\b",
    re.I,
)

# ---------------------------------------------------------------------------------------------
# IC: contradictions = intra-variant contradictions recorded in diff-analysis.md.
# diff-analysis Summary: "Total contradictions: 9 (cross-variant 7: X-001 to X-007; intra-variant 2:
# X-008, X-009, both in Variant A)". X-008 (E2 identity evidence ran under bypassPermissions, but the
# read-only adapter needs --restricted, which refuses bypassPermissions) and X-009 (reflect ceiling
# admits claude-p before the read-only condition is checked) are both tagged XI-A.
# No intra-variant contradiction is recorded for Variant B in X-001..X-009 (X-002 and X-007 are
# cross-variant factual errors of B about A / about the repo, which the protocol does not count as an
# internal contradiction). Counts used: A = 2, B = 0.
# ---------------------------------------------------------------------------------------------
CONTRA = {"A": 2, "B": 0}


def strip_legend(t):
    return "\n".join(l for l in t.splitlines() if not LEGEND_RE.match(l))


def compute(k, t):
    hits = {n: bool(re.search(p, t)) for n, p in REQ.items()}
    rc = sum(hits.values()) / len(REQ)

    claims = len(TAG_RE.findall(strip_legend(t)))
    ic = 1 - CONTRA[k] / claims

    body = [l for l in t.splitlines() if l.strip() and not l.startswith("#") and not META_RE.match(l)]
    text = "\n".join(body)
    spans = re.findall(r"`[^`]+`", text)
    rest = re.sub(r"`[^`]+`", " ", text)
    ids = re.findall(r"\b(?:INV|CO|FX|GQ|OQ|C|X|R)-?\d+[A-Za-z]?\b|\b(?:INV)-[A-Z]\b", rest)
    nums = re.findall(r"\b\d+(?:\.\d+)?%?", rest)
    concrete = len(spans) + len(ids) + len(nums)
    vague = len(VAGUE_RE.findall(text))
    sr = concrete / (concrete + vague)

    # DC: internal references only (external research-file sections and synth ids excluded).
    heads = set(re.findall(r"^#{2,3} (\d+(?:\.\d+)?)[ .]", t, re.M))
    refs = []  # (kind, ref, resolved)
    for m in re.finditer(r"[Ss]ections? (\d+(?:\.\d+)?)", t):
        pre = t[max(0, m.start() - 8):m.start()]
        if re.search(r"(?:\br|\bw|\bW|synth-)\d{2} $|\b(?:r04|r13|r16|r08|r09|r06|W02|w02) $", pre):
            continue  # section of an external research file
        ref = m.group(1)
        refs.append(("section", ref, ref in heads or ref.split(".")[0] in heads))
    # 'point N' / 'item N' refs resolve against numbered list items present in the same variant
    listed = set(re.findall(r"^\s*(\d+)\. ", t, re.M))
    for m in re.finditer(r"\b(?:point|item)s? (\d+)\b", t):
        refs.append(("point/item", m.group(1), m.group(1) in listed))
    # E-n refs (B's evidence table) resolve against table rows '| En |'
    defined_e = set(re.findall(r"^\| (E\d+) \|", t, re.M))
    for m in re.finditer(r"\bE(\d+)\b", t):
        e = "E" + m.group(1)
        if "@" in t[m.start() - 1:m.start()]:
            continue  # E2@<sha> is a branch label, not an evidence row
        if m.group(1) == "2" and t[m.end():m.end() + 1] == "@":
            continue
        # skip E1/E2/E3 used as 'E1 path' / 'E2's' experiment labels in A (A has no E-table)
        if defined_e:
            refs.append(("E-row", e, e in defined_e))
    # M-n refs (A's measurements) resolve against '^M-n,' definitions
    defined_m = set(re.findall(r"^(M-\d+),", t, re.M))
    for m in re.finditer(r"\b(M-\d+)\b", t):
        if defined_m:
            refs.append(("M-n", m.group(1), m.group(1) in defined_m))
    total = len(refs)
    resolved = sum(1 for r in refs if r[2])
    dc = resolved / total if total else 1.0
    unresolved = [f"{r[0]}:{r[1]}" for r in refs if not r[2]]

    sections = len(re.findall(r"^## ", t, re.M))
    return dict(
        RC=rc, RC_hits=sum(hits.values()), RC_total=len(REQ),
        RC_matched=[n for n, h in hits.items() if h],
        RC_missing=[n for n, h in hits.items() if not h],
        claims=claims, contradictions=CONTRA[k], IC=ic,
        concrete=concrete, concrete_parts=dict(code_spans=len(spans), ids=len(ids), numbers=len(nums)),
        vague=vague, SR=sr,
        refs_total=total, refs_resolved=resolved, refs_unresolved=unresolved, DC=dc,
        sections=sections,
    )


out = {k: compute(k, t) for k, t in V.items()}
mx = max(v["sections"] for v in out.values())
for k, o in out.items():
    o["SC"] = o["sections"] / mx
    o["quant_score"] = 0.30 * o["RC"] + 0.25 * o["IC"] + 0.15 * o["SR"] + 0.15 * o["DC"] + 0.15 * o["SC"]
out["_meta"] = {
    "variant_map": {"A": "variant-1-original.md (Proposal A)", "B": "variant-2-original.md (Proposal B)"},
    "contradiction_provenance": "diff-analysis.md Summary: intra-variant X-008, X-009 in Variant A; none recorded for Variant B",
    "requirement_topics": list(REQ),
}
(D / "quant-score-output.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
