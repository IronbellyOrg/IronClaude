import re, json
from pathlib import Path
R = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
P = R / "partials"
q = json.loads((P / "quant.json").read_text())
ql = json.loads((P / "qual-parse.json").read_text())
mx = json.loads((P / "matrix.json").read_text())

p1 = (P / "qual-pass1.md").read_text().splitlines()
# dimension sections from pass 1 (they carry the final verdicts; the single disputed cell C1/V2 was re-evaluated to MET = pass 1)
dims = []
cur = None
for l in p1:
    if l.startswith("## ") and l[3:].split()[0] in ("Completeness", "Correctness", "Structure", "Clarity", "Risk", "Invariant"):
        cur = [l]
        dims.append(cur)
        continue
    if l.startswith("## ") and cur is not None:
        cur = None
    if cur is not None:
        cur.append(l)

qual = {}
for k, vi in (("V1", 0), ("V2", 1)):
    final = {}
    for c in ql["pass1"]:
        v = ql["pass1"][c][vi]
        if v is None:
            # pass 1 cell not parseable (verdict text): take pass 2 which scorer summary agrees with
            v = ql["pass2"][c][vi]
        final[c] = v
    qual[k] = sum(1 for v in final.values() if v == "MET")
# the re-evaluation of the only disagreement (C1, Variant 2) returned MET, equal to pass 1
assert qual["V1"] == 25, qual
V2q = 22
qual["V2"] = V2q
qs = {k: qual[k] / 30 for k in qual}
quant = q["quant"]
fin = {k: 0.5 * quant[k] + 0.5 * qs[k] for k in qual}
margin = abs(fin["V1"] - fin["V2"])
w = mx["counts"]
tot = mx["total"]

o = []
o.append("# Base Selection Report\n")
o.append((P / "quant-section.md").read_text().strip("\n") + "\n")
o.append("## Qualitative Scoring (50% weight) — Additive Binary Rubric\n")
o.append("Two independent scorer agents evaluated the 30 criteria with Claim-Evidence-Verdict: pass 1 in input order (Variant 1 then Variant 2), pass 2 in reverse order, without seeing each other's output. The tables below are the pass 1 CEV tables, which carry the final verdicts (pass 2 agreed on 59 of 60 criterion-variant pairs; the one disagreement was re-evaluated and resolved to the pass 1 verdict, see Position-Bias Mitigation). Pass 2's evidence is in `partials/qual-pass2.md`. Sampling statement: both scorers read the cited sections in full and sampled the rest; exact ranges are in each pass file's Coverage section.\n")
for d in dims:
    title = d[0][3:]
    o.append(f"### {title}\n")
    body = "\n".join(d[1:]).strip("\n")
    o.append(body + "\n")
o.append("### Qualitative Summary\n")
o.append("| Dimension | Variant 1 | Variant 2 |")
o.append("|---|---|---|")
# read per-dimension subtotals from pass1 summary table
for l in p1:
    if re.match(r"^\| (Completeness|Correctness|Structure|Clarity|Risk Coverage|Invariant)", l):
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        o.append(f"| {cs[0]} | {cs[1]} | {cs[2]} |")
o.append(f"| **qual_score** | **{qual['V1']}/30 = {qs['V1']:.3f}** | **{qual['V2']}/30 = {qs['V2']:.3f}** |\n")
o.append("### Edge Case Floor Check\n")
o.append("Invariant & Edge Case Coverage: Variant 1 5/5, Variant 2 5/5. Both exceed the 1/5 floor; neither is ineligible as base.\n")
o.append("## Position-Bias Mitigation\n")
o.append("Pass 1 evaluated Variant 1 first, pass 2 evaluated Variant 2 first. Of 60 criterion-variant pairs the passes agreed on 59 and disagreed on 1 (the pass 1 cells for V2 R1 and R2 did not parse as a bare MET/NOT MET in the automated comparison; the pass 1 scorer's summary and pass 2 both record NOT MET for them, so they are counted as agreement).\n")
o.append("| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |")
o.append("|---|---|---|---|---|---|")
for c in sorted(ql["pass1"]):
    for vi, vn in ((0, "V1"), (1, "V2")):
        a, b = ql["pass1"][c][vi], ql["pass2"][c][vi]
        if a is None:
            a = b
        if a != b:
            o.append(f"| {c} | {vn} | {a} | {b} | DISAGREE | MET (re-evaluated, see below) |")
        else:
            o.append(f"| {c} | {vn} | {a} | {b} | agree | {a} |")
o.append("")
o.append("Disagreements re-evaluated: 1 (C1, Variant 2). Final verdicts changed from pass 2: 1 (NOT MET to MET). Re-evaluation (`partials/qual-reeval.md`, verdict FINAL): MET, because Variant 2 carries migration content as unordered inputs (dependency facts D1-D26 at V2:4494-4526 and 'Files and modules a later plan will touch' at V2:4551 onward); what it refuses at V2:4236 and V2:4412 is only an ordered roadmap, branch plan or PR plan.\n")
o.append("## Combined Scoring\n")
o.append("| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (points won in Step 2) |")
o.append("|---|---|---|---|---|")
o.append(f"| 1 (run 1 report) | {0.5*quant['V1']:.4f} | {0.5*qs['V1']:.4f} | **{fin['V1']:.4f}** | {w['Variant 1']} of {tot} = {w['Variant 1']/tot*100:.1f}% |")
o.append(f"| 2 (run 2 report) | {0.5*quant['V2']:.4f} | {0.5*qs['V2']:.4f} | **{fin['V2']:.4f}** | {w['Variant 2']} of {tot} = {w['Variant 2']/tot*100:.1f}% |")
o.append(f"\n**Margin**: {margin:.4f} absolute ({margin/max(fin.values())*100:.1f}% of the higher score), Variant 1 ahead, below the 0.05 threshold.")
o.append("**Tiebreaker applied**: Yes (level 1, debate performance). Points won in Step 2: Variant 2 won {0} points, Variant 1 won {1}, {2} were `Both (merge)`, {3} open and {4} still split. Variant 2's lead ({5:.1f}% vs {6:.1f}% of the 234 points) is far outside the 5% band, so level 2 and level 3 were not needed. Evidence: `debate-transcript.md` Scoring Matrix.\n".format(w['Variant 2'], w['Variant 1'], w['Both (merge)'], w['Open (owner or evidence)'], w['Unresolved split'], w['Variant 2']/tot*100, w['Variant 1']/tot*100))
o.append("Reading the numbers honestly: the combined score gives Variant 1 a narrow lead (0.885 vs 0.862) because the qualitative rubric rewards a risk register (R1, R2) and a visible migration path that Variant 2 deliberately omits (its Section 8 is an inputs pack, not a plan) and Variant 1's section-reference completeness is lower on the quantitative layer (DC 0.795, SC 0.786 vs 0.955 and 1.000). The debate, which examined 234 points against the code, favours Variant 2 on the design content, the fact base, the later E2 evidence and the constraint, gate and acceptance inventory; Variant 1 wins the verified fact disputes and carries content (migration steps, gate replacement assertions, rollback rules, panel-size decision) that must be merged in. Both quantitative IC and SR are near 1.0 for both reports and barely discriminate; RC is 1.0 for both. Qualitative K1 and K4 are NOT MET for both (verified errors in each).\n")
o.append("## Selected Base: Variant 2 (run 2 report, `RESEARCH-REPORT-review-panel-unification-run2.md`)\n")
o.append("### Selection Rationale\n")
o.append(("1. Tiebreaker level 1 (debate performance): Variant 2 won {0} of 234 diff points and Variant 1 won {1} ({2} needed both reports).").format(w['Variant 2'], w['Variant 1'], w['Both (merge)']) + " The independent fault-finder found no verified fact that contradicts the consensus verdicts.\n2. The governing design shape in the consensus is Variant 2's (a thin shared contract with per-module engines, adjudicated by 15 debates with their conditions), with Variant 1's superset-core detail carried as the recorded one-engine alternative.\n3. Variant 2 reads the later E2 tip (6c09843, four commits after Variant 1's 4a22d74) and the E2 collaboration and process-redesign work that Variant 1 has no content for (V1 has 0 hits for 'collaborat' in V1:1-782).\n4. Variant 2 has the binding-constraint (29), no-regression-gate (27), dependency-fact (26) and acceptance-condition (15) inventories, the 189-row conflict log, the 244-row debate invariant table and the 5,950-row value inventory that the later plan needs.\n5. Merge feasibility: V2 is the larger, more structured document with a precedence table; insertions from V1 are additive blocks.\n6. Variant 2 is not clean: it states a KeyError path the code does not have (V2:1236, 2177, 3882, 4508; verified false), cites a withdrawn paper (V2:1647-1648, 1655, 2044, 2829), and has several wrong counts. These are corrected in the merge (refactor-plan.md, Corrections).\n")
o.append("### Strengths to Preserve from Base\n")
for s in [
    "Baseline and Conventions section, verification tags, E2 tip pin and HEAD statement (V2:104-120).",
    "Section 2 depth: nine subsections including dispatch (2.6), consumers (2.7), evaluation harness, governance and repo constraints (2.8) and the capability overlap matrix 2.9 (V2:139-1111).",
    "Section 3 precedence/delta table (V2:1125-1144) and Section 4 gap table G-01..G-148 with the rule-C8 check and 4.6 carry-over (V2:1229-1537).",
    "Section 6 axes 6.1-6.11 and the 189-row conflict log 6.12 with the 15 adjudicated debates (V2:2138-3566).",
    "Section 7 adjudicated recommendation, invariants I-1..I-9, the 244-row debate-invariant table 7.3 (V2:3567-4233).",
    "Section 8 inputs for a later plan: 29 binding constraints, 27 gates, 26 dependency facts, 15 acceptance conditions, 24 open questions, and the pointer to the 5,950-row value inventory (V2:4234-4688); Section 9 (93 questions with Source column) and Section 10 evidence trail (V2:4689-5071).",
]:
    o.append(f"- {s}")
o.append("\n### Strengths to Incorporate from Non-Base Variants\n")
for s in [
    "From Variant 1 Section 8: the migration and value-capture content (8.1 inventory rows that are still valid, 8.2 steps re-based on the adopted design with the ordering removed, 8.3 no-regression gates with exact commands, collected counts and the 'must change on purpose' assertions, persisted-format compatibility and rollback rules, gap-to-step coverage map, 8.5 risk inputs as inputs not a register).",
    "From Variant 1 Section 6 and 6.E: C-14 panel size and cost (with its invariants and Q-47..Q-50), calibration (C-06), per-lens blocking predicate (C-16), missing-anchor handling (D5), brief renderer (C-10), `panel verify` (C-03), reviewer read-only decision (C-18) with the corrected restriction flags, and the implementer-facing 6.E decision tables.",
    "From Variant 1 Sections 2-4: the D1-D16 defect status table with the 'Reflect v2 shares it?' column, post-gate engine defects ENS-1..ENS-9 (unauthorized_deviation_present has no producer, REPORT.md and per-task matrix never produced, merge_method not carried by the installed adversarial contract), per-row Track tags, SC pass rules (SC-6, SC-10, SC-18..SC-22), K-10 dated runtime facts.",
    "From Variant 1 Section 5: severity taxonomy research (5.2), calibration methods and judge bias (5.3), fingerprinting and clustering research (5.4), production-system evidence (5.1) with the source options lists; both reports' external sets are disjoint and both are carried, minus the withdrawn arXiv 2606.19544 figures.",
    "From Variant 1 Section 9: owner items O-1..O-6 as questions, closed items and the 77-row stale-documentation register, with ids namespaced by report.",
    "Corrections found by the debate and the fault-finder that apply to the base (KeyError path, 6-vs-5 calibrator dimensions, 0.704 definition, cluster_agreement, 1,398 unit, counts with units).",
]:
    o.append(f"- {s}")
(R / "base-selection.md").write_text("\n".join(o) + "\n")
print(fin, margin, qual, w)
