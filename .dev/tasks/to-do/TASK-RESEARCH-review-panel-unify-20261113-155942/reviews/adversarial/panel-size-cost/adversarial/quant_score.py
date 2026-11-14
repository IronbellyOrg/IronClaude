"""Deterministic quantitative layer for debate C14 (read-only; prints metrics, writes nothing).

Run: uv run python <this file>
Metrics follow refs/scoring-protocol.md A.1. Source requirements: no formal FR/NFR ids exist, so the
edge-case rule applies (section-level topic matching) against the requirement topics below, which are
taken from the C-14 block of synth-04 and the debate task statement.
IC uses a fixed, documented contradiction list (see CONTRADICTIONS) so the run is reproducible.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V = {
    "A": os.path.join(HERE, "variant-1-original.md"),
    "B": os.path.join(HERE, "variant-2-original.md"),
}

# Requirement topics (keyword groups; a requirement is matched when ANY keyword phrase is present).
REQS = {
    "R01 cap of 3 reviewers handled": ["_REFLECT_MAX_REVIEWERS", "cap of 3", "cap at 3", "cap of three"],
    "R02 escalation share / cost driver recount": ["38 of 39", "35 of 39", "tier_decision.yaml"],
    "R03 E2 evidence (flat in panel size)": ["COMBO-REPORT", "E2", "CR:381"],
    "R04 H-A unmeasured / pilot": ["H-A"],
    "R05 O-8 rubric lever / pre-filter": ["O-8", "pre-filter", "parsed-sparse"],
    "R06 2 vs 3 inside reflect unmeasured": ["not measured", "unmeasured", "Nothing measures"],
    "R07 default 4-reviewer template and live7": ["live7", "four reviewers", "4 reviewers"],
    "R08 G-67 clamp mismatch (4 vs 3)": ["G-67", "config.py:335"],
    "R09 shadow exit shortfall rule": ["reflect_shadow_exit", "2-of-3", "shortfall"],
    "R10 test coverage section": ["Test coverage needed"],
    "R11 risks with mitigation": ["Risks and mitigations"],
    "R12 cost / effort": ["## Cost", "Effort"],
    "R13 reversibility": ["revers", "rollback", "roll back", "revert", "kill switch"],
    "R14 executor-class exclusion": ["executor class", "hard-exclude", "executor"],
    "R15 consumer exposure (blocking vs advisory)": ["advisory", "blocking"],
    "R16 invariants / guard conditions": ["Invariant", "guard", "floor"],
}

# Contradictions / refuted claims found in-document by the debate (id -> variant). Each is a claim
# the checked files contradict or that contradicts another claim in the same variant.
CONTRADICTIONS = {
    "A": [
        "A1: 'through the parsed-sparse pre-filter' (flag decisive in 0-1 of 39)",
        "A8: B removes Tier 2 for 'up to 34-35' runs",
        "S2 table: B gives up Tier 2 on 'up to 34-35 of 38-39'",
        "S2 table: B 'saves a whole Tier 2 run on 35 of 39' (inverse of the same error)",
        "A9: B 'cannot be rolled back by data alone' (skill-text revert + --tier 2 kill switch)",
        "Design 'no new code': omits SKILL.md:340 shadow-parity coupling and the task-builder blocking POST gate (INV-012)",
    ],
    "B": [
        "E-5: 'at most 5' and 'row 8: 1 clear-cut' (files: 0 certain, at most 1)",
        "E-6: 'clear-cut flag-only run' (reflection-card C 0.68 escalates it via row 6)",
        "R1: 'up to 13 percent' of plans (follows from the 5)",
        "Phase 1 / G1 ordering: G1 cannot open on any data (zero candidates), contradicting 'ships if >=3 candidates' as a live branch",
    ],
}

CONCRETE = [
    r"\b\d+(?:\.\d+)?\s*(?:%|percent|points?|tokens?|runs?|files?|reviewers?|arms?|plans?)\b",
    r"\b[\w./-]+\.(?:py|md|json|yaml)(?::\d+)?\b",
    r"\b\d{1,3}(?:,\d{3})+\b",
    r"\bp\s*[=<]\s*0?\.\d+\b",
    r"`[^`]+`",
]
VAGUE = [r"\bappropriate\b", r"\bas needed\b", r"\bproperly\b", r"\badequate\b", r"\bshould consider\b",
         r"\bmight\b", r"\bvarious\b", r"\betc\.", r"\bbest practices?\b"]


def read(p):
    with open(p) as f:
        return f.read()


def metrics(name, text):
    low = text.lower()
    matched = [k for k, kws in REQS.items() if any(kw.lower() in low for kw in kws)]
    rc = len(matched) / len(REQS)
    # claims = numbered/bulleted substantive statements: table rows + list items
    claims = len([l for l in text.splitlines() if re.match(r"^\s*(?:[-*]|\d+\.)\s+\S", l) or re.match(r"^\|\s*[A-Z]\w*[- ]?\d", l)])
    ic = 1 - len(CONTRADICTIONS[name]) / max(claims, 1)
    conc = sum(len(re.findall(p, text)) for p in CONCRETE)
    vag = sum(len(re.findall(p, text, re.I)) for p in VAGUE)
    sr = conc / (conc + vag)
    # internal references: ids defined as headings/row starts vs referenced
    defined = set(re.findall(r"^\s*(?:\*\*)?(?:\|\s*)?(A\d+|C\d+|R\d+|E-\d+)\b", text, re.M))
    refs = re.findall(r"\b(A\d+|C\d+|R\d+|E-\d+)\b", text)
    # external ids (R04, R11, R06 ... research files, CR:, PR:) are excluded: only same-doc ids count
    refs_in = [r for r in refs if r in defined or r.startswith(("A", "C")) and re.match(r"^[AC]\d$", r)]
    resolved = [r for r in refs_in if r in defined]
    dc = len(resolved) / max(len(refs_in), 1)
    h2 = len(re.findall(r"^## ", text, re.M))
    return dict(name=name, matched=len(matched), nreq=len(REQS), RC=rc, claims=claims,
                contradictions=len(CONTRADICTIONS[name]), IC=ic, concrete=conc, vague=vag, SR=sr,
                refs=len(refs_in), resolved=len(resolved), DC=dc, h2=h2, missing=[k for k in REQS if k not in matched])


rows = {k: metrics(k, read(p)) for k, p in V.items()}
maxh2 = max(r["h2"] for r in rows.values())
for r in rows.values():
    r["SC"] = r["h2"] / maxh2
    r["quant"] = 0.30 * r["RC"] + 0.25 * r["IC"] + 0.15 * r["SR"] + 0.15 * r["DC"] + 0.15 * r["SC"]
for k, r in rows.items():
    print(k, {kk: (round(v, 4) if isinstance(v, float) else v) for kk, v in r.items()})
