#!/usr/bin/env python3
"""Quantitative layer (scoring-protocol.md A.1) for slot X-13, process-redesign-modules.

Deterministic, stdlib only, no model judgment except the contradiction list below,
which is a fixed table of debate-verified findings (each with line refs and the
debate evidence that verified it). Run: uv run python quant-score.py
Writes quant-score-output.json next to this file. Running twice gives identical JSON.

Variants scored AS WRITTEN: A = variant-1-original.md (Proposal A), B = variant-2-original.md.

Definitions used
----------------
quant_score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC

RC  12 source requirements R1..R12 (task brief). A variant matches a requirement when every
    phrase of at least one phrase-group appears case-insensitively in the variant text.
    RC = matched / 12.
IC  IC = 1 - contradictions / total_claims.
    total_claims = number of lines containing a citation pattern
    [`(]?[\\w/.]+\\.(py|md|json):\\d+  or one of the tags [CODE-VERIFIED], [UNVERIFIED],
    [DESIGN], [CODE-CONTRADICTED].
    contradictions = number of entries in CONTRADICTIONS below: claims the debate VERIFIED
    against code or text to be false, or to contradict the same variant's own other statement
    or its own cited source (each entry lists variant line refs and the verifying evidence).
    Wrong-citation-on-a-true-claim (cosmetic line shifts) is NOT counted.
SR  concrete = number of non-heading, non-blank lines with at least one concrete indicator:
    a digit (covers numbers and file:line cites), a backticked identifier, or a named threshold
    word (at most, at least, no more than, threshold, floor, percent).
    vague = regex occurrences of the vague indicators of scoring-protocol.md A.1 SR:
    appropriate, as needed, properly, adequate, should consider, might, various, etc.,
    best practices, industry standard.
    SR = concrete / (concrete + vague).
    Deviation: also excluded from the line count: table separator rows and the `Status:` line
    (metadata lines are excluded by the protocol).
DC  internal references = occurrences of `section N` / `section N.N`, `Round N`, `E<n>` evidence
    ids and `3.<n>` subsection refs. resolved = target exists in the same variant: a `## N.`
    heading, a line-leading `N.M` subsection, a `| E<n> |` table row, or a heading containing
    `Round N`. DC = resolved / total (1.0 if total is 0).
    Deviations (all because the variants also cite external documents):
      - `section N` is excluded as external when the preceding token holds `/` or `.md`, or is
        `slice`, `scope`, or an r<number> alias (r10, r13), or when the following text is
        `of <something>.md` / `of <backticked file>`.
      - `E<n>` is counted only in a variant that defines E-rows (`| E<n> |`); in the other variant
        E1..E7 are extractor labels of the E2 brainstorm, not evidence ids. Occurrences followed
        by `'s`, a quote, a backtick, `brainstorm`, `text`, `planning`, `gates`, `arm`, or
        preceded by `extractors ` / `the `, are brainstorm labels and are excluded. The defining
        first cell of an E-row is not counted as a reference.
      - `3.<n>` (n = 1..9) is a reference only when it is not at line start (definition), not inside
        a longer dotted number (3.0.3), and not preceded by a word char, dot or slash. `3.0` is a
        decimal (e.g. '3.0 percent'), not a subsection.
    Known limitation: in variant B some `E<n>` tokens are E2-brainstorm extractor labels (for
    example 'E6 is experimental'); they resolve against B's E-rows by coincidence, so B's DC
    denominator is slightly inflated. All counted refs resolve, so this cannot lower B's DC.
SC  SC = H2 headings (lines starting `## `) / max over variants.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANTS = {"A": "variant-1-original.md", "B": "variant-2-original.md"}

# ---------------------------------------------------------------- RC
RC_REQS = [
    ("R1", "core shape: pre-pass or sidecar/assigned/observed", [["pre-pass"], ["sidecar", "assigned", "observed"]]),
    ("R2", "advisory vs demotion/promotion (CO-23, GQ-130)", [["demot", "promot"]]),
    ("R3", "recipes for read-only tools", [["read-only", "bash"]]),
    ("R4", "CB-2 vs Medium routing (CO-24)", [["cb-2", "medium"]]),
    ("R5", "slot keys / lens binding (GQ-131)", [["_slot_keys"], ["gq-131"]]),
    ("R6", "gates G0 and D1-D7 (GQ-135)", [["d2", "g0"]]),
    ("R7", "design consequence for core and modules", [["shared core"], ["design consequence"]]),
    ("R8", "invariants preserved/endangered", [["preserved", "endangered"]]),
    ("R9", "test or measurement that shows it right or wrong", [["measurement"], ["would show"]]),
    ("R10", "consistency with adjudicated C-01, C-02, C-03", [["c-01", "c-02", "c-03"]]),
    ("R11", "effect on PR code review and rf-qa", [["pr review", "rf-qa"], ["pr code review", "rf-qa"]]),
    ("R12", "strongest objection and answer", [["objection", "answer"]]),
]

# ---------------------------------------------------------------- IC
CLAIM_RE = re.compile(r"[`(]?[\w/.]+\.(py|md|json):\d+")
TAG_RE = re.compile(r"\[(CODE-VERIFIED|UNVERIFIED|DESIGN|CODE-CONTRADICTED)\]")

# Debate-verified contradictions / false claims, per variant (as-written text line numbers).
CONTRADICTIONS = {
    "A": [
        {"id": "A-X1", "lines": [20, 110],
         "claim": "an item with no finding 'is reported in observed through the existing mechanism'",
         "contradicts": "A line 110 'observed is a declaration'; code: nothing writes observed but the orchestrator (findings_v2.py:6, SKILL.md:345)",
         "verified_by": "round1-advocate-A concession 1; round1-advocate-B weakness 1; round2-advocate-A section 'B weakness 1' (conceded)"},
        {"id": "A-X2", "lines": [43],
         "claim": "'At HEAD no component edits a reviewer finding before the merge' resting on ledger.py:3-4",
         "contradicts": "A's own quote of ledger.py:3-4 is a status rule ('Only this module changes a finding's status'); the cite does not carry the claim",
         "verified_by": "round1-advocate-B weakness 5; round2-advocate-A (gave up this argument, ledger.py:3-4 is a status rule); diff-analysis X-003; debate-transcript X-003 (both agree)"},
        {"id": "A-X3", "lines": [18, 69],
         "claim": "core adds additive advisory item-evidence flags to precheck.json built on verify_cmd._check",
         "contradicts": "_check reaches only findings-v2 citations (verify_cmd.py:133-143); script-attached item evidence has no checker; A line 69 itself lists byte-identity of precheck.json as endangered",
         "verified_by": "round1-advocate-B weakness 2; round1-advocate-A concession 6; round2-advocate-A item 1 (withdrew part (c))"},
        {"id": "A-X4", "lines": [20, 89],
         "claim": "v1 engine carries item answers under an open unknown key such as 'probe', checkable by the module",
         "contradicts": "ledger copies only round, reviewer_id, fid, blocking into members (ledger.py:172-179, re-read by this scorer); no host exists for the module check on v1",
         "verified_by": "round1-advocate-A concession 5; round2-advocate-A (v1 loop has no snapshot/sidecar/precheck step); round2-advocate-B (CONFIRMED)"},
        {"id": "A-X5", "lines": [12, 113],
         "claim": "if no extractor passes M1, A 'degrades, by construction' to a leftover with value (card loader plus sidecar entry point)",
         "contradicts": "leftover equals arm K (a plain-words checklist with a loader); A's own advocate withdrew the 'has value' wording; A line 117 concedes the core cannot prove examination",
         "verified_by": "round1-advocate-B weakness 4; round2-advocate-A ('a claim about harm, not value'; withdrawn)"},
    ],
    "B": [
        {"id": "B-X1", "lines": [35, 93],
         "claim": "'The brief renderer appends ... each card's recipe_text'; T-B1 golden files of rendered briefs",
         "contradicts": "no brief renderer exists in cli/review (only ledger._brief_ids); briefs are orchestrator prose",
         "verified_by": "round1-advocate-A weakness 4; round1-advocate-B concession 1; round2.5 INV-019 re-ran the search"},
        {"id": "B-X2", "lines": [43],
         "claim": "a PROBLEM row without a finding is listed under follow-up candidates by the report builder (non-blocking rows are already listed, ledger.py:468)",
         "contradicts": "ledger.py:467-474 prints ledger rows only (others = [r for r in ledger['rows'] if not r['blocking']]); a PROBLEM row with no finding is not a ledger row (re-read by this scorer)",
         "verified_by": "round1-advocate-A weakness 6; round2-advocate-B item g (CONFIRMED; 'My R1 citation ledger.py:468 was wrong')"},
        {"id": "B-X3", "lines": [34, 36],
         "claim": "reviewer ids are <slot_id>-<i> (panel.py:668) and feed the existing sidecar keyed by reviewer id",
         "contradicts": "the sidecar key is the card file stem (cluster_cmd.py:146), 'reviewer-<N>' in the reflect flow; three reviewer-id spaces exist",
         "verified_by": "round1-advocate-B concession 6; round2.5 INV-003"},
        {"id": "B-X4", "lines": [38, 118],
         "claim": "the merge reads the overlay only when the profile says rowcheck: apply; the core 'puts no behaviour in the core that a profile does not switch on'",
         "contradicts": "merge_cmd.command (merge_cmd.py:71-118) hands raw text to ledger.merge_round, no extension point or profile layer; the overlay needs merge_cmd and ledger.py changes (INV-D)",
         "verified_by": "round1-advocate-A weakness 4; round1-advocate-B concession 3; round2-advocate-B decision (i) (dropped the profile value and overlay)"},
        {"id": "B-X5", "lines": [36, 43, 79],
         "claim": "row block placed after the findings block while 'the brief file document_review_loop_prompts.md is untouched'",
         "contradicts": "that brief says 'end the report with the findings block' (document_review_loop_prompts.md:33) and a pinned sentence says the last section is the Findings block",
         "verified_by": "round1-advocate-A weakness 8; round1-advocate-B concession 2; round2.5 INV-015"},
        {"id": "B-X6", "lines": [34],
         "claim": "slot key 'recipes' chosen after checking name collisions (only recipe_name in the swarm lens registry)",
         "contradicts": "src/superclaude/cli/swarm/recipes/ is an existing package (ls re-run by this scorer); the check missed it",
         "verified_by": "round1-advocate-B concession 5; round2-advocate-A new fact; debate-transcript C-013"},
    ],
}

# ---------------------------------------------------------------- SR
VAGUE_RE = re.compile(
    r"\b(appropriate|as needed|properly|adequate|should consider|might|various|best practices|industry standard)\b|\betc\.",
    re.I,
)
THRESH_RE = re.compile(r"\b(at most|at least|no more than|threshold|floor|percent)\b", re.I)
SEP_RE = re.compile(r"^\|[-| :]+\|$")

# ---------------------------------------------------------------- DC
SECTION_RE = re.compile(r"\b[Ss]ection (\d+(?:\.\d+)?)(?![\dA-Za-z])")
ROUND_RE = re.compile(r"\bRound (\d+)")
E_RE = re.compile(r"\bE(\d{1,2})\b")
SUB_RE = re.compile(r"(?<![\w./])3\.([1-9])(?!\d|\.\d)")  # 3.0 is a decimal ('3.0 percent'), never a subsection
EROW_RE = re.compile(r"^\|\s*(E\d+)\s*\|")
H2_RE = re.compile(r"^## (\d+)\.")
SUBDEF_RE = re.compile(r"^(\d+\.\d+)\s")


def read(name):
    return (HERE / name).read_text(encoding="utf-8")


def rc(text):
    low = text.lower()
    out = []
    for rid, name, groups in RC_REQS:
        hit = any(all(p in low for p in g) for g in groups)
        out.append({"id": rid, "requirement": name, "matched": hit})
    return out


def ic(variant, lines):
    total = sum(1 for ln in lines if CLAIM_RE.search(ln) or TAG_RE.search(ln))
    contra = CONTRADICTIONS[variant]
    return total, contra


def sr(lines, text):
    concrete = 0
    substantive = 0
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or SEP_RE.match(s) or s.startswith("Status:"):
            continue
        substantive += 1
        if re.search(r"\d", s) or re.search(r"`[^`]+`", s) or THRESH_RE.search(s):
            concrete += 1
    vague = len(VAGUE_RE.findall(text))
    ratio = concrete / (concrete + vague) if (concrete + vague) else 0.0
    return concrete, vague, substantive, ratio


def is_external_section(text, m):
    before = text[: m.start()].rstrip()
    tok = re.search(r"(\S+)$", before)
    tok = tok.group(1) if tok else ""
    if "/" in tok or ".md" in tok or tok.lower() in ("slice", "scope") or re.fullmatch(r"r\d+", tok):
        return True
    after = text[m.end(): m.end() + 60]
    if re.match(r"\W*\s*of\s+(`|[\w./-]+\.md)", after):
        return True
    return False


def dc(lines):
    text = "\n".join(lines)
    h2 = {m.group(1) for ln in lines for m in [H2_RE.match(ln)] if m}
    subs = {m.group(1) for ln in lines for m in [SUBDEF_RE.match(ln)] if m}
    erows = {m.group(1) for ln in lines for m in [EROW_RE.match(ln)] if m}
    heads = [ln for ln in lines if ln.startswith("#")]
    refs = []  # (kind, target, lineno, resolved)
    for i, ln in enumerate(lines, 1):
        for m in SECTION_RE.finditer(ln):
            if is_external_section(ln, m):
                continue
            tgt = m.group(1)
            ok = (tgt in h2) or (tgt in subs)
            refs.append(("section", tgt, i, ok))
        for m in ROUND_RE.finditer(ln):
            ok = any(f"Round {m.group(1)}" in h for h in heads)
            refs.append(("round", m.group(1), i, ok))
        for m in SUB_RE.finditer(ln):
            if m.start() == 0:
                continue
            tgt = "3." + m.group(1)
            refs.append(("subsection", tgt, i, tgt in subs))
        if erows:
            scan_from = 0
            em = EROW_RE.match(ln)
            if em:
                scan_from = em.end()
            for m in E_RE.finditer(ln, scan_from):
                tail = ln[m.end(): m.end() + 14]
                head = ln[max(0, m.start() - 11): m.start()]
                if re.match(r"('s|\s*[\"'`“]|\s+(brainstorm|text|planning|gates|arm))", tail):
                    continue
                if head.endswith("extractors ") or head.endswith("the "):
                    continue
                tgt = "E" + m.group(1)
                refs.append(("evidence", tgt, i, tgt in erows))
    total = len(refs)
    resolved = sum(1 for r in refs if r[3])
    ratio = resolved / total if total else 1.0
    return total, resolved, ratio, refs


def main():
    data = {}
    h2count = {}
    for v, fname in VARIANTS.items():
        text = read(fname)
        lines = text.split("\n")
        h2count[v] = sum(1 for ln in lines if ln.startswith("## "))
        reqs = rc(text)
        rc_val = sum(1 for r in reqs if r["matched"]) / len(reqs)
        total_claims, contra = ic(v, lines)
        ic_val = 1 - len(contra) / total_claims
        conc, vague, subst, sr_val = sr(lines, text)
        dtot, dres, dc_val, drefs = dc(lines)
        data[v] = {
            "file": fname,
            "RC": {"value": rc_val, "matched": sum(1 for r in reqs if r["matched"]), "total": len(reqs), "detail": reqs},
            "IC": {"value": ic_val, "contradictions": len(contra), "total_claims": total_claims, "contradiction_list": contra},
            "SR": {"value": sr_val, "concrete_lines": conc, "vague_occurrences": vague, "substantive_lines": subst,
                   "concrete_share_of_substantive_lines_info_only": round(conc / subst, 6)},
            "DC": {"value": dc_val, "resolved": dres, "total": dtot,
                   "refs": [{"kind": r[0], "target": r[1], "line": r[2], "resolved": r[3]} for r in drefs]},
            "H2_count": h2count[v],
        }
    mx = max(h2count.values())
    for v in data:
        sc = data[v]["H2_count"] / mx
        data[v]["SC"] = {"value": sc, "h2": data[v]["H2_count"], "max_h2": mx}
        d = data[v]
        d["quant_score"] = round(
            0.30 * d["RC"]["value"] + 0.25 * d["IC"]["value"] + 0.15 * d["SR"]["value"]
            + 0.15 * d["DC"]["value"] + 0.15 * d["SC"]["value"], 6)
    out = {"slot": "X-13 process-redesign-modules", "layer": "quantitative (scoring-protocol.md A.1)", "variants": data}
    (HERE / "quant-score-output.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("variant  RC     IC     SR     DC     SC     quant_score")
    for v in data:
        d = data[v]
        print(f"{v:<8} {d['RC']['value']:.4f} {d['IC']['value']:.4f} {d['SR']['value']:.4f} "
              f"{d['DC']['value']:.4f} {d['SC']['value']:.4f} {d['quant_score']:.6f}")
    for v in data:
        d = data[v]
        print(f"{v}: RC {d['RC']['matched']}/{d['RC']['total']}; IC contradictions {d['IC']['contradictions']} / claims {d['IC']['total_claims']}; "
              f"SR concrete {d['SR']['concrete_lines']} vague {d['SR']['vague_occurrences']}; "
              f"DC {d['DC']['resolved']}/{d['DC']['total']}; H2 {d['H2_count']}")


if __name__ == "__main__":
    main()
