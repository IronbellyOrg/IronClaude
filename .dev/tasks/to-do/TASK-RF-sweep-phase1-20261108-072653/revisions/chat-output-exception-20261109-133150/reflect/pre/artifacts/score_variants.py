"""Step 3 (hybrid scoring) for the sc:adversarial run inside sc-reflect UC-1 run 3.

Read-only on inputs except it writes <ADV>/base-selection.md and <ADV>/scores.json.
Quantitative layer: deterministic metrics computed from the variant text (adapted to reviewer cards, see ADAPT).
Qualitative layer: two judge passes (qual-pass1.json forward, qual-pass2.json reverse) reconciled per the
position-bias protocol; the four disagreements were re-evaluated by the orchestrator (RESOLVED below).
Run: uv run --no-project python -I score_variants.py
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode")
ADV = ROOT / ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/reflect/pre/adversarial"
VARS = {"V1": "variant-1-original.md", "V2": "variant-2-original.md", "V3": "variant-3-original.md"}
CAL = {"V1": (26, 3), "V2": (18, 0), "V3": (19, 0)}  # (citations checked, failed) from the blind calibrations
DIMS = [
    ("Completeness", "C"),
    ("Correctness", "K"),
    ("Structure", "S"),
    ("Clarity", "L"),
    ("Risk Coverage", "R"),
    ("Invariant & Edge Case Coverage", "E"),
]
# Orchestrator re-evaluation of the passes' disagreements (explicit comparison of both pieces of evidence; verdict FINAL).
RESOLVED = {
    ("V1", "K1"): ("NOT_MET", "The blind calibration confirmed three wrong line references in this card (TL:353 is an Output path, not the preservation stop; the quoted branch is at TL:1210; the OQ-17 filename is at TL:1270/1273). A card with verified wrong citations does not meet 'no factual errors'. Pass 2 right."),
    ("V1", "K2"): ("NOT_MET", "R1-F1's fix says to 'untick it if needed'. Completed verdicts are never rewritten and the ledger only ticks; the plan's own convention (TL:1295) is 're-run this item' without unticking. The debate narrowed the fix to that wording (consensus M-05). Pass 2 right."),
    ("V1", "R1"): ("NOT_MET", "Only R1-F3 states a likelihood, and the debate showed it unsupported (DES:760 calls the field UNVERIFIED). Fewer than three risks carry probability and impact. Same rule as for V3 in both passes. Pass 2 right."),
    ("V2", "R1"): ("NOT_MET", "R2-F1 is 'conditional on the branch firing' and R2-F2 is deterministic, which gives a probability statement for two risks; R2-F3 has none. At least three are required. Applying the same rule uniformly to all three cards. Pass 2 right."),
}
VAGUE = re.compile(r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|arguably|best practices)\b", re.I)
CONCRETE = re.compile(r"(\bTL:\d+|\bDES:\d+|\bADD:\d+|\b[A-Z]{1,4}-\d+\b|\b\d+\.\d+\b|\b\d{2,}\b|`[^`]+`)")


def text(v):
    return (ADV / VARS[v]).read_text()


def quant(v, all_texts):
    t = text(v)
    checks = [
        "**Reviewer persona**" in t,
        "## Findings" in t,
        bool(re.search(r"\|\s*(HIGH|MEDIUM|LOW)\s*\|", t)),
        "## Tier-1 findings reviewed" in t,
        "## Slice coverage" in t,
        "## Notes" in t,
        "**Self-reported confidence C**" in t,
        len(re.findall(r"\|\s*R\d-F\d+\s*\|", t)) > 0 and all(re.search(r"\d", row) for row in re.findall(r"^\| R\d-F\d+ .*$", t, re.M)),
        all("fix" in row.lower() or "verif" in row.lower() for row in re.findall(r"^\| R\d-F\d+ .*$", t, re.M)),
    ]
    rc = sum(checks) / len(checks)
    checked, failed = CAL[v]
    ic = 1 - failed / checked
    concrete = len(CONCRETE.findall(t))
    vague = len(VAGUE.findall(t))
    sr = concrete / (concrete + vague)
    defined = set(re.findall(r"^\| (R\d-F\d+) ", t, re.M))
    refs = re.findall(r"\bR\d-F\d+\b", t)
    t1refs = [int(x) for x in re.findall(r"\bF(\d+)\b", t)]
    resolved = sum(1 for r in refs if r in defined) + sum(1 for n in t1refs if 1 <= n <= 10)
    total = len(refs) + len(t1refs)
    dc = resolved / total if total else 1.0
    secs = len(re.findall(r"^## ", t, re.M))
    maxsec = max(len(re.findall(r"^## ", x, re.M)) for x in all_texts.values())
    sc = secs / maxsec
    q = 0.30 * rc + 0.25 * ic + 0.15 * sr + 0.15 * dc + 0.15 * sc
    return dict(RC=rc, IC=ic, SR=sr, DC=dc, SC=sc, quant=q, concrete=concrete, vague=vague, rc_checks=checks, refs=total, resolved=resolved, sections=secs)


def qual():
    p1 = json.load(open(ADV / "qual-pass1.json"))["verdicts"]
    p2 = json.load(open(ADV / "qual-pass2.json"))["verdicts"]
    final, log = {}, []
    for v in VARS:
        final[v] = {}
        for cid in p1[v]:
            a, b = p1[v][cid], p2[v][cid]
            if a["verdict"] == b["verdict"]:
                final[v][cid] = (a["verdict"], a["evidence"])
                log.append((cid, v, a["verdict"], b["verdict"], "agree", a["verdict"]))
            else:
                fv, why = RESOLVED[(v, cid)]
                final[v][cid] = (fv, why)
                log.append((cid, v, a["verdict"], b["verdict"], "re-evaluated", fv))
    return p1, p2, final, log


def main():
    texts = {v: text(v) for v in VARS}
    qs = {v: quant(v, texts) for v in VARS}
    p1, p2, final, log = qual()
    sub = {}
    for v in VARS:
        sub[v] = {name: sum(1 for cid, (vd, _) in final[v].items() if cid[0] == pre and vd == "MET") for name, pre in DIMS}
        qs[v]["qual"] = sum(sub[v].values()) / 30
        qs[v]["combined"] = 0.5 * qs[v]["quant"] + 0.5 * qs[v]["qual"]
    # debate points won from the consensus scoring matrix
    cons = (ADV / "debate/consensus.md").read_text()
    won = {v: 0 for v in VARS}
    for row in re.findall(r"^\| ([SCXA]-\d{3}) [^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\| ([^|]*) \|", cons, re.M):
        w = row[1].strip()
        for v in VARS:
            if w.startswith(v) or w.startswith(f"split ({v}"):
                won[v] += 1
    floor_ok = {v: sub[v]["Invariant & Edge Case Coverage"] >= 1 for v in VARS}
    ranked = sorted([v for v in VARS if floor_ok[v]], key=lambda v: -qs[v]["combined"])
    top, second = ranked[0], ranked[1]
    margin = qs[top]["combined"] - qs[second]["combined"]
    tb = "No"
    base = top
    if margin < 0.05:
        if won[top] != won[second]:
            base = top if won[top] > won[second] else second
            tb = f"Yes (level 1, debate points won {top} {won[top]} vs {second} {won[second]})"
        else:
            ca = sum(1 for cid, (vd, _) in final[top].items() if cid[0] == "K" and vd == "MET")
            cb = sum(1 for cid, (vd, _) in final[second].items() if cid[0] == "K" and vd == "MET")
            if ca != cb:
                base = top if ca > cb else second
                tb = f"Yes (level 2, correctness criteria met {top} {ca} vs {second} {cb})"
            else:
                base = min(top, second)
                tb = "Yes (level 3, input order)"
    out = dict(quant={v: {k: (round(x, 4) if isinstance(x, float) else x) for k, x in qs[v].items()} for v in VARS}, qual_subtotals=sub, points_won=won, ranked=ranked, margin=round(margin, 4), tiebreaker=tb, base=base, floor_ok=floor_ok)
    (ADV / "scores.json").write_text(json.dumps(out, indent=2) + "\n")

    L = []
    L.append("# Base Selection: reviewer-card variants (sc:adversarial step 3, Mode A, depth standard)\n")
    L.append("Generated by `../artifacts/score_variants.py` (deterministic quantitative layer, reconciled qualitative layer). Inputs: `variant-N-original.md`, `qual-pass1.json` (forward order V1,V2,V3), `qual-pass2.json` (reverse order V3,V2,V1), `debate/consensus.md`, the three `reviewer-card-N-calibrated.yaml` files.\n")
    L.append("ADAPT: the scored artifacts are reviewer cards, not roadmaps, so the quantitative metrics are adapted as follows. RC = share of 9 required output-contract elements present (persona header, findings table, severities, Tier-1 table, slice coverage, notes, self-reported C, a file:line in every finding row, a fix or verifier in every finding row). IC = 1 - (citations the blind calibrator found wrong / citations checked), the card-level measure of internally ungrounded claims. SR = concrete tokens (line refs, ids, numbers, code spans) / (concrete + vague words). DC = internal references (R#-F#, T1 F#) that resolve to a defined finding or to T1 F1-F10, over all. SC = H2 sections / max across variants.\n")
    L.append("## Quantitative Scoring (50% weight)\n")
    L.append("| Metric | Weight | V1 | V2 | V3 |\n|---|---|---|---|---|")
    for m, w in (("RC", "0.30"), ("IC", "0.25"), ("SR", "0.15"), ("DC", "0.15"), ("SC", "0.15")):
        L.append(f"| {m} | {w} | " + " | ".join(f"{qs[v][m]:.3f}" for v in VARS) + " |")
    L.append("| **quant_score** | | " + " | ".join(f"**{qs[v]['quant']:.3f}**" for v in VARS) + " |\n")
    L.append("Computation detail: " + "; ".join(f"{v}: RC checks {sum(qs[v]['rc_checks'])}/9, IC {CAL[v][1]} failed of {CAL[v][0]}, SR concrete {qs[v]['concrete']} vs vague {qs[v]['vague']}, DC {qs[v]['resolved']}/{qs[v]['refs']}, sections {qs[v]['sections']}" for v in VARS) + ".\n")
    L.append("## Qualitative Scoring (50% weight): Additive Binary Rubric (30 criteria)\n")
    L.append("Evidence is the Claim-Evidence-Verdict text from the judge passes. Where the two passes agreed, the shared verdict and pass-1 evidence are shown; where they disagreed, the orchestrator's re-evaluation and reason are shown (marked RESOLVED).\n")
    for name, pre in DIMS:
        L.append(f"### {name} (5 criteria)\n")
        L.append("| Criterion | V1 | V2 | V3 |\n|---|---|---|---|")
        for i in range(1, 6):
            cid = f"{pre}{i}"
            cells = []
            for v in VARS:
                vd, ev = final[v][cid]
                tag = "MET" if vd == "MET" else "NOT MET"
                resolved = (v, cid) in RESOLVED
                cells.append(f"{tag}{' (RESOLVED)' if resolved else ''}: {ev}".replace("|", "/"))
            L.append(f"| {cid} | " + " | ".join(cells) + " |")
        L.append("")
    L.append("### Qualitative Summary\n")
    L.append("| Dimension | V1 | V2 | V3 |\n|---|---|---|---|")
    for name, _ in DIMS:
        L.append(f"| {name} | " + " | ".join(f"{sub[v][name]}/5" for v in VARS) + " |")
    L.append("| **Total** | " + " | ".join(f"**{sum(sub[v].values())}/30 = {qs[v]['qual']:.3f}**" for v in VARS) + " |\n")
    L.append("### Edge Case Floor Check\n")
    L.append("| Variant | Invariant & Edge Case Coverage | Eligible as base |\n|---|---|---|")
    for v in VARS:
        L.append(f"| {v} | {sub[v]['Invariant & Edge Case Coverage']}/5 | {'yes' if floor_ok[v] else 'no (below 1/5)'} |")
    L.append("")
    L.append("## Position-Bias Mitigation\n")
    L.append("Pass 1 evaluated V1, V2, V3; pass 2 evaluated V3, V2, V1, both with the same judge model. Totals by pass (MET of 30):\n")
    L.append("| Variant | Pass 1 | Pass 2 | Final |\n|---|---|---|---|")
    for v in VARS:
        t1 = sum(1 for z in p1[v].values() if z["verdict"] == "MET")
        t2 = sum(1 for z in p2[v].values() if z["verdict"] == "MET")
        L.append(f"| {v} | {t1} | {t2} | {sum(sub[v].values())} |")
    dis = [x for x in log if x[4] == "re-evaluated"]
    L.append(f"\nDisagreements found: {len(dis)} of 90 criterion-variant pairs. Verdicts changed by re-evaluation relative to pass 1: {sum(1 for x in dis if x[5] != x[2].replace('_', ' ').replace('NOT MET', 'NOT_MET'))}. Each re-evaluation compared both passes' evidence; the verdict is final.\n")
    L.append("| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |\n|---|---|---|---|---|---|")
    for cid, v, a, b, ag, f in log:
        if ag != "agree":
            L.append(f"| {cid} | {v} | {a} | {b} | disagree, re-evaluated | {f} |")
    L.append("\nAll 86 other pairs agreed. A pass-order effect is visible: pass 1 (V1 first) gave V1 the benefit on K1, K2, R1 and V2 on R1, and pass 2 (V1 last) did not; the re-evaluations side with the stricter reading in all four cases.\n")
    L.append("## Combined Scoring\n")
    L.append("| Variant | Quant (50%) | Qual (50%) | Combined | Debate points won |\n|---|---|---|---|---|")
    for v in VARS:
        L.append(f"| {v} | {qs[v]['quant']:.3f} | {qs[v]['qual']:.3f} | **{qs[v]['combined']:.3f}** | {won[v]} |")
    rank_txt = ", ".join(v + " " + format(qs[v]["combined"], ".3f") for v in ranked)
    L.append(f"\nRanking: {rank_txt}. Margin between first and second: {margin*100:.1f} percentage points. Tiebreaker applied: {tb}. Debate points are counted from the Winner column of `debate/consensus.md` (a row counts for a variant when its winner cell starts with that variant or 'split (V#').\n")
    names = {"V1": "reviewer 1, analyzer, sonnet slot", "V2": "reviewer 2, qa, haiku slot", "V3": "reviewer 3, refactorer, opus slot"}
    L.append(f"## Selected Base: Variant {base[1]} ({names[base]})\n")
    L.append("### Selection Rationale\n")
    cal_c = {"V1": 0.69, "V2": 0.86, "V3": 0.71}[base]
    L.append(f"{base} has the highest combined score ({qs[base]['combined']:.3f}); tiebreaker: {tb}. Its calibrated confidence is {cal_c}. The base only fixes the card's frame and the findings it already holds; the debate consensus (`debate/consensus.md`) decides the merged findings and severities, so the merge is not a copy of any one card.\n")
    L.append("### Strengths to Preserve from Base\n")
    L.append("- Per-finding table with evidence quote, smallest fix and a verifier; self-reported and calibrated confidence recorded.\n- Findings that survived the debate unchanged in kind.\n")
    L.append("### Strengths to Incorporate from Non-Base Variants\n")
    L.append("Taken from `debate/consensus.md` (merge candidates M-01 to M-10, severities as agreed in Round 2): each non-base variant's surviving findings, their evidence and fixes; the exact-count verifier design (three file sets); the narrowed embed-the-missing-clauses remedy for 7.10; the sha256 guard pattern; the 59-item stale-anchor note; and the Tier-1 verdict table.\n")
    (ADV / "base-selection.md").write_text("\n".join(L) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
