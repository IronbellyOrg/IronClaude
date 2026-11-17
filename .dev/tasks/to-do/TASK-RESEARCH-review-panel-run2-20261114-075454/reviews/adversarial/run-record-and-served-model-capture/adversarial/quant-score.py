#!/usr/bin/env python3
"""Quantitative layer (scoring-protocol.md A.1) for slot C-08, Pass 1.

Pure stdlib, regex/keyword based, no LLM judgement. Deterministic: the output
JSON carries a sha256 of its own scored content so two runs can be compared.

Run: uv run python quant-score.py
Reads:  variant-1-original.md, variant-2-original.md, diff-analysis.md
Writes: quant-score-output.json (next to this script)
"""
import hashlib
import json
import re
from pathlib import Path

ADV = Path(__file__).resolve().parent
VARIANTS = {"V1": ADV / "variant-1-original.md", "V2": ADV / "variant-2-original.md"}
DIFF = ADV / "diff-analysis.md"
OUT = ADV / "quant-score-output.json"

# Weights (A.1)
W = {"RC": 0.30, "IC": 0.25, "SR": 0.15, "DC": 0.15, "SC": 0.15}

# ---------------------------------------------------------------- RC topics
# No formal requirement IDs exist, so section/topic-level matching (protocol edge
# case). A topic matches when an ID regex hits, OR any kw_any regex hits, OR every
# group of kw_all has at least one hit. Case-insensitive.
TOPICS = [
    ("T01", "CO-19 served model from transcript", [r"\bCO-19\b"], [],
     [[r"transcript"], [r"adapter"], [r"served model|model_observed|observed model"]]),
    ("T02", "CO-20 memory writer / study switch", [r"\bCO-20\b"],
     [r"study switch", r"read-freeze", r"freezes? reads"], []),
    ("T03", "CO-11 adapter home (installed-path)", [r"\bCO-11\b"], [],
     [[r"adapter"], [r"INV-F|installed[- ]path|package CLI"]]),
    ("T04", "C-S10 strata list", [r"\bC-S10\b"],
     [r"strata (become|are) (a )?module", r"module[- ]registered"], []),
    ("T05", "FX-16 spec-shaped telemetry fields", [r"\bFX-16\b"],
     [r"RFC-2119", r"spec-shaped"], []),
    ("T06", "FX-19 lost-update / serialising", [r"\bFX-19\b"], [r"lost[- ]update"], []),
    ("T07", "OQ-19 reviewer model actually used", [r"\bOQ-19\b"],
     [r"reviewer model actually used"], []),
    ("T08", "OQ-21 adapter home", [r"\bOQ-21\b"], [], [[r"adapter"], [r"home|placement"]]),
    ("T09", "OQ-23 real manifest race", [r"\bOQ-23\b"],
     [r"real (two-process )?(manifest )?race", r"never been run|was never run|no run has measured"], []),
    ("T10", "INV-F installed-path rule", [r"\bINV-F\b"], [r"installed[- ]path rule"], []),
    ("T11", "INV-H no document text", [r"\bINV-H\b"], [r"no document text"], []),
    ("T12", "INV-A contract field names", [r"\bINV-A\b"], [r"contract field names"], []),
    ("T13", "INV-L shadow changes no verdict", [r"\bINV-L\b"], [r"changes no verdict"], []),
    ("T14", "served model never from orchestrator", [], [],
     [[r"orchestrator"], [r"transcript"], [r"never|not from|replaced|writes none|rejects"]]),
    ("T15", "cost on one row per agent attempt", [],
     [r"one row per agent attempt", r"one entry per agent", r"per[- ]agent (row|entry|attempt|usage|cost)",
      r"one row or entry per agent"], []),
    ("T16", "two labelled cost bases", [],
     [r"two labelled", r"labelled cost bases?", r"reviewer-only.{0,80}all.agents"], []),
    ("T17", "concurrent writes serialised", [], [],
     [[r"flock|lock"], [r"serialis|exclusive|concurren"]]),
    ("T18", "no document text in telemetry (mechanism)", [], [],
     [[r"document text"], [r"telemetry|record|event"],
      [r"type[- ]check|closed key|hash pointers|typed values"]]),
    ("T19", "strata module list", [],
     [r"module[- ]registered (list|strata)", r"strata (become|are) (a )?module", r"strata.{0,40}module"], []),
    ("T20", "memory writer owner and study switch", [], [],
     [[r"memory"], [r"writer"], [r"script step|stays? (an )?LLM|unchanged|LLM-written|LLM read"]]),
    ("T21", "PR code review effect", [], [r"PR code review", r"PR panel", r"PR review"], []),
    ("T22", "rf-qa effect", [], [r"rf-qa"], []),
    ("T23", "pre-registered test or measurement", [], [r"pre-registered", r"registered before any run"], []),
    ("T24", "strongest objection answered", [], [],
     [[r"strongest objection"], [r"\banswer\b"]]),
    ("T25", "consistency with C-01/C-02/C-03", [], [],
     [[r"C-01"], [r"C-02"], [r"C-03"], [r"consistent|agrees"]]),
    ("T26", "null fallback, identity_source stays requested-pinned", [], [],
     [[r"requested-pinned"], [r"\bnull\b"]]),
    ("T27", "non-reviewer agent roles covered", [], [],
     [[r"debater"], [r"judge|validator"], [r"orchestrator"]]),
    ("T28", "contract 1.8.0 untouched", [], [r"1\.8\.0"], []),
    ("T29", "SKILL edit fence", [], [r"edit fence", r"fence"], []),
    ("T30", "adapter replay on the 15 E1 logs", [], [], [[r"15 E1"], [r"stream logs|logs"]]),
]


def topic_match(text, ids, kw_any, kw_all):
    f = re.IGNORECASE
    for p in ids:
        if re.search(p, text, f):
            return "id"
    for p in kw_any:
        if re.search(p, text, f | re.DOTALL):
            return "keyword"
    if kw_all and all(any(re.search(p, text, f) for p in grp) for grp in kw_all):
        return "keyword"
    return None


# ---------------------------------------------------------------- IC
TAG_RE = re.compile(r"\[(?:CODE-VERIFIED|CODE-CONTRADICTED|UNVERIFIED)[^\]]*\]")


def intra_contradictions():
    """INTRA-A / INTRA-B contradiction IDs, parsed from diff-analysis.md."""
    res = {"V1": [], "V2": []}
    for line in DIFF.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (X-\d+) \| INTRA-([AB])\b", line)
        if m:
            res["V1" if m.group(2) == "A" else "V2"].append(m.group(1))
    return res


# ---------------------------------------------------------------- SR
CONCRETE = [
    r"\d",  # any number / quantity / threshold / line ref
    r"`[^`]+`",  # named code entity
    r"\b[\w/.\-]+\.(?:py|md|json|jsonl|sh|ya?ml)\b",  # file name
    r"\bpercent\b",
    r"\bzero\b",
]
VAGUE = [
    r"\bappropriate\b", r"\bas needed\b", r"\bproperly\b", r"\badequate\b",
    r"\bshould consider\b", r"\bmight\b", r"\bvarious\b", r"\betc\.", r"\bbest practices\b",
    r"\bindustry standard\b",
]


def statements(text):
    """Substantive statements: skip preamble before first H2, headings, table
    header/separator rows. Table rows count as one statement per row; prose lines
    are split on sentence boundaries."""
    lines = text.splitlines()
    first_h2 = next((i for i, l in enumerate(lines) if l.startswith("## ")), 0)
    out = []
    in_table_header_done = False
    for l in lines[first_h2:]:
        s = l.strip()
        if not s or s.startswith("#"):
            in_table_header_done = False
            continue
        if re.match(r"^Status:\s*Complete\s*$", s):
            continue
        if s.startswith("|"):
            if re.match(r"^\|[\s:\-|]+\|?$", s):
                in_table_header_done = True
                continue
            if not in_table_header_done:  # header row precedes the separator row
                continue
            out.append(s)
            continue
        in_table_header_done = False
        for part in re.split(r"(?<=[.;])\s+(?=[A-Z(\[`])", s):
            if len(part.split()) >= 6:
                out.append(part)
    return out


# ---------------------------------------------------------------- DC
def parse_structure(text):
    lines = text.splitlines()
    h2 = [l for l in lines if l.startswith("## ")]
    sec_defs = set()
    for l in lines:
        m = re.match(r"^#{2,4}\s+(\d+(?:\.\d+)*)\b", l)
        if m:
            sec_defs.add(m.group(1))
            # a subsection "4.1" also implies its parent "4"
            sec_defs.add(m.group(1).split(".")[0])
    # numbered evidence items: "N. [" or "N. text" at line start inside "## 4." (A) -> collected globally
    item_defs = {int(m.group(1)) for m in re.finditer(r"^(\d+)\.\s", text, re.M)}
    b_defs = {int(m.group(1)) for m in re.finditer(r"^\|\s*B-(\d+)\s*\|", text, re.M)}
    m_defs = {int(m.group(1)) for m in re.finditer(r"^\s*(?:[-*]\s+)?M(\d)\b[.,]", text, re.M)}
    # objection numbers: numbered lines inside any section whose heading mentions "objection",
    # plus an explicit "(objection N)" label in a heading.
    obj_defs = set()
    cur_obj = False
    for l in lines:
        if l.startswith("#"):
            cur_obj = bool(re.search(r"objection", l, re.I))
            for m in re.finditer(r"objection\s+(\d+)", l, re.I):
                obj_defs.add(int(m.group(1)))
            continue
        if cur_obj:
            m = re.match(r"^\s*(\d+)\.\s", l)
            if m:
                obj_defs.add(int(m.group(1)))
    return {"h2": len(h2), "sec_defs": sec_defs, "item_defs": item_defs,
            "b_defs": b_defs, "m_defs": m_defs, "obj_defs": obj_defs}


EXTERNAL_CTX = re.compile(r"SKILL|research|\bR\d\d\b|synth|`###|spec-panel|CLAUDE", re.I)


def internal_refs(text, st):
    """Return list of (kind, ref, resolved) for internal references."""
    refs = []
    # section references (word form only); skip external-document contexts
    for m in re.finditer(r"\b[Ss]ections? (\d+(?:\.\d+)*)((?:\s*(?:,|and)\s*\d+(?:\.\d+)*)*)", text):
        ctx = text[max(0, m.start() - 40):m.start()]
        if EXTERNAL_CTX.search(ctx):
            continue
        nums = [m.group(1)] + re.findall(r"\d+(?:\.\d+)*", m.group(2) or "")
        for n in nums:
            refs.append(("section", n, n in st["sec_defs"]))
    # item references (own numbered evidence list)
    for m in re.finditer(r"\bitems? (\d+)((?:\s*(?:,|and)\s*\d+)*)", text):
        nums = [m.group(1)] + re.findall(r"\d+", m.group(2) or "")
        for n in nums:
            refs.append(("item", n, int(n) in st["item_defs"]))
    # B-NN references (exclude table-row definitions)
    for m in re.finditer(r"(?<!^\| )\bB-(\d+)\b", text, re.M):
        line_start = text.rfind("\n", 0, m.start()) + 1
        if re.match(r"\|\s*B-\d+\s*\|", text[line_start:m.end() + 2]) and m.start() - line_start <= 3:
            continue
        refs.append(("B-NN", m.group(1), int(m.group(1)) in st["b_defs"]))
    # M1..M5 measurement references (exclude definition-line starts)
    for m in re.finditer(r"\bM([1-9])\b", text):
        line_start = text.rfind("\n", 0, m.start()) + 1
        if re.match(r"^\s*(?:[-*]\s+)?M\d[.,]", text[line_start:m.end() + 1]):
            continue
        refs.append(("M", m.group(1), int(m.group(1)) in st["m_defs"]))
    # objection references
    for m in re.finditer(r"\bobjection (\d+)\b", text, re.I):
        refs.append(("objection", m.group(1), int(m.group(1)) in st["obj_defs"]))
    return refs


# ---------------------------------------------------------------- main
def score_variant(key, path, contradictions):
    text = path.read_text(encoding="utf-8")
    st = parse_structure(text)

    # RC
    topic_rows = []
    matched = 0
    for tid, label, ids, kw_any, kw_all in TOPICS:
        basis = topic_match(text, ids, kw_any, kw_all)
        topic_rows.append({"id": tid, "topic": label, "matched": bool(basis), "basis": basis})
        matched += 1 if basis else 0
    rc = matched / len(TOPICS)

    # IC
    claims = len(TAG_RE.findall(text))
    ncontra = len(contradictions)
    ic = 1 - ncontra / claims if claims else 0.0

    # SR
    stm = statements(text)
    concrete = sum(1 for s in stm if any(re.search(p, s) for p in CONCRETE))
    vague = sum(1 for s in stm if any(re.search(p, s, re.I) for p in VAGUE))
    sr = concrete / (concrete + vague) if (concrete + vague) else 0.0

    # DC
    refs = internal_refs(text, st)
    resolved = sum(1 for r in refs if r[2])
    dc = resolved / len(refs) if refs else 1.0
    unresolved = [f"{k} {n}" for k, n, ok in refs if not ok]

    return {
        "h2_count": st["h2"],
        "rc": rc, "rc_matched": matched, "rc_total": len(TOPICS), "rc_topics": topic_rows,
        "ic": ic, "ic_claims_tagged": claims, "ic_contradictions": ncontra,
        "ic_contradiction_ids": contradictions,
        "sr": sr, "sr_concrete_statements": concrete, "sr_vague_statements": vague,
        "sr_total_substantive_statements": len(stm),
        "dc": dc, "dc_total_refs": len(refs), "dc_resolved_refs": resolved,
        "dc_unresolved": unresolved,
        "dc_ref_breakdown": {k: sum(1 for r in refs if r[0] == k) for k in
                             sorted({r[0] for r in refs})},
    }


def main():
    contra = intra_contradictions()
    assert contra["V1"] == ["X-004", "X-010"], contra
    assert contra["V2"] == ["X-002", "X-003", "X-007", "X-008", "X-009"], contra

    res = {k: score_variant(k, p, contra[k]) for k, p in VARIANTS.items()}
    max_h2 = max(r["h2_count"] for r in res.values())
    for r in res.values():
        r["sc"] = r["h2_count"] / max_h2
        r["sc_max_h2"] = max_h2
        r["quant_score"] = (r["rc"] * W["RC"] + r["ic"] * W["IC"] + r["sr"] * W["SR"]
                            + r["dc"] * W["DC"] + r["sc"] * W["SC"])
        for k in ("rc", "ic", "sr", "dc", "sc", "quant_score"):
            r[k] = round(r[k], 4)

    payload = {"weights": W, "variants": res}
    blob = json.dumps(payload, sort_keys=True, indent=2)
    payload["content_sha256"] = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    for k, r in res.items():
        print(k, "RC", r["rc"], "IC", r["ic"], "SR", r["sr"], "DC", r["dc"], "SC", r["sc"],
              "QUANT", r["quant_score"])
    print("sha256", payload["content_sha256"])


if __name__ == "__main__":
    main()
