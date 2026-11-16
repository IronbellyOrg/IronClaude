import re, json
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
V = {"V1": (ROOT / "variant-1-original.md").read_text(), "V2": (ROOT / "variant-2-original.md").read_text()}

# --- Requirement coverage: the requirements the merged document must satisfy (from the compare task statement and
# the later-plan consumer). Matched by regex; no LLM judgement.
REQ = {
 "R01 ten-section report shape: Problem Statement": r"^## 1\. Problem Statement",
 "R02 Current State Analysis": r"^## 2\. Current State Analysis",
 "R03 Target State": r"^## 3\. Target State",
 "R04 Gap Analysis": r"^## 4\. Gap Analysis",
 "R05 External Research Findings": r"^## 5\. External Research Findings",
 "R06 Options Analysis": r"^## 6\. Options Analysis",
 "R07 Recommendation": r"^## 7\. Recommendation",
 "R08 section 8 (plan or inventory content)": r"^## 8\. ",
 "R09 Open Questions": r"^## 9\. Open Questions",
 "R10 Evidence Trail": r"^## 10\. Evidence Trail",
 "R11 value inventory with destinations": r"(?i)value inventory",
 "R12 conflict outcomes and debate results": r"(?i)adversarial result|adjudicat",
 "R13 gap analysis rows with severity": r"(?i)\| *(Critical|Important|Minor) *\|",
 "R14 migration / value-capture content": r"(?i)migration|value-capture",
 "R15 no-regression gates": r"(?i)no-regression",
 "R16 binding constraints": r"(?i)binding constraint|\bK-\d+\b",
 "R17 git ref constraint (feat/review-panel vs feat/review-panel/<name>)": r"feat/review-panel/",
 "R18 E1 reflect Tier 2 kernel and shadow runs": r"(?i)shadow",
 "R19 E2 tasklist review-panel study": r"(?i)tasklist-review-panel|E2",
 "R20 E3 #346 review loop and installed-only variants": r"(?i)#346|installed-only|stoprule",
 "R21 shared core location src/superclaude/cli/review": r"src/superclaude/cli/review",
 "R22 future consumers PR review and rf-qa": r"(?i)rf-qa",
 "R23 owner decisions / open questions routed": r"(?i)owner",
 "R24 evidence verification tags": r"CODE-VERIFIED|UNVERIFIED",
}
rc = {}
rc_detail = {}
for k, t in V.items():
    hit = [name for name, rx in REQ.items() if re.search(rx, t, re.M)]
    rc[k] = len(hit) / len(REQ)
    rc_detail[k] = [n for n in REQ if n not in hit]

# --- Internal consistency: 1 - internal contradictions / scorable claims.
# scorable claims = lines carrying a file:line citation. Internal contradictions = intra-report
# inconsistencies established during diff analysis and the debate (listed, with ids).
cite = re.compile(r"[\w/.-]+\.(py|md|sh|json|yaml):\d+")
claims = {k: sum(1 for l in t.splitlines() if cite.search(l)) for k, t in V.items()}
internal = {
 "V1": ["V1 8.4 states 'ironbelly/shadow-runs 3 commits ahead' (stale: 5 now; r25 re-derivation #2)",
        "V1 labels 16 of 20 conflicts DECIDED-BY-EVIDENCE although the same report calls 4 debates partial and C-04 depends on availability vs diversity (V2 advocate and X-052; status overclaim)",
        "V1 Q-54..Q-61 itself flags a verdict-vocabulary contradiction (PENDING/exit 12 vs ESCALATE) in the carried design (U-106)",
        "V1 count '37 reflect test files' (V1:381) vs 38 (r25 re-derivation #6)",
        "V1 rf-* '43 call sites' unit unstated and not reproducible (X-022)"],
 "V2": ["V2 SC-04 'declared quorum (decision)' vs delta row G-14 decided quorum (X-004)",
        "V2 G-85 and 3.5 list the workflow/tasklist entry open while delta row T-4/3.5 says decided (X-005)",
        "V2 SC-17 'decision, 0.75 or 0.80' vs delta row 'decided by the code: 0.80' (C-017)",
        "V2 Section 7 C-2 and D9 assert KeyError on the ledger merge path while V2 axis 1 and Appendix B say rejected at findings.py:104 (X-049, X-053; orchestrator VERIFIED-V1)",
        "V2 2.4 treats installed-variant scripts as read (verified) while 2.9 OQ-01 tags all E3i cells UNVERIFIED (X-034)",
        "V2 G-06 rated Important although its own rubric (V2:1121) makes a fail-open verdict Critical (CL-15, V2 advocate concession)",
        "V2 uses arXiv 2606.19544 (withdrawn) at V2:1647-1648, 1655, 2044, 2829 (X-036; r25 #26)",
        "V2 'pr_submit 50 test files' vs 47 (r25 #6); '(6)' occurrences vs 5 lines/7 (X-017)"],
}
ic = {k: 1 - len(internal[k]) / claims[k] for k in V}

# --- Specificity ratio
conc = re.compile(r"\b\d+(\.\d+)?\s?(%|ms|s\b|MB|KB|files?|rows?|tests?|keys?|lines?|commits?|runs?)|\b[\w/-]+\.(py|md|sh|json|yaml)\b|\b[0-9a-f]{7,40}\b|\bL?\d{2,5}\b")
vague = re.compile(r"(?i)\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices|industry standard)\b")
sr = {}
srn = {}
for k, t in V.items():
    c = len(conc.findall(t)); v = len(vague.findall(t))
    srn[k] = (c, v)
    sr[k] = c / (c + v)

# --- Dependency completeness: Section references that resolve to a heading
def dc(t):
    heads = re.findall(r"(?m)^#{2,6} (\d+(?:\.\d+)*)[ .]", t)
    hs = set(heads)
    refs = re.findall(r"(?:Section|Sec\.|§)\s?(\d+(?:\.\d+)*)", t)
    ok = sum(1 for r in refs if r in hs or r.split(".")[0] in {h.split(".")[0] for h in hs} and "." not in r)
    return ok, len(refs)
dcv = {}
dcn = {}
for k, t in V.items():
    ok, n = dc(t)
    dcn[k] = (ok, n)
    dcv[k] = ok / n if n else 1.0

# --- Section coverage
h2 = {k: len(re.findall(r"(?m)^## ", t)) for k, t in V.items()}
mx = max(h2.values())
sc = {k: h2[k] / mx for k in V}

W = dict(rc=0.30, ic=0.25, sr=0.15, dc=0.15, sc=0.15)
quant = {k: W["rc"] * rc[k] + W["ic"] * ic[k] + W["sr"] * sr[k] + W["dc"] * dcv[k] + W["sc"] * sc[k] for k in V}
res = dict(rc=rc, ic=ic, sr=sr, dc=dcv, sc=sc, quant=quant, claims=claims, srn=srn, dcn=dcn, h2=h2, rc_missing=rc_detail, internal=internal)
(ROOT / "partials" / "quant.json").write_text(json.dumps(res, indent=1))

o = []
o.append("## Quantitative Scoring (50% weight)\n")
o.append("All five metrics were computed by `/tmp/cmp_quant.py` (deterministic regex and counts over `variant-1-original.md` and `variant-2-original.md`; re-running gives identical numbers). Source requirements: the report-shape and decision-relevant items listed under RC (the inputs have no formal FR-/NFR- ids, so the skill's section-level topic-matching edge case applies).\n")
o.append("| Metric | Weight | Variant 1 (run 1) | Variant 2 (run 2) |")
o.append("|---|---|---|---|")
o.append(f"| requirement_coverage | 0.30 | {rc['V1']:.3f} ({round(rc['V1']*len(REQ))}/{len(REQ)}; missing: {', '.join(m.split(' ')[0] for m in rc_detail['V1']) or 'none'}) | {rc['V2']:.3f} ({round(rc['V2']*len(REQ))}/{len(REQ)}; missing: {', '.join(m.split(' ')[0] for m in rc_detail['V2']) or 'none'}) |")
o.append(f"| internal_consistency | 0.25 | {ic['V1']:.3f} (1 - {len(internal['V1'])}/{claims['V1']} cited-claim lines) | {ic['V2']:.3f} (1 - {len(internal['V2'])}/{claims['V2']} cited-claim lines) |")
o.append(f"| specificity_ratio | 0.15 | {sr['V1']:.3f} ({srn['V1'][0]} concrete / {srn['V1'][1]} vague) | {sr['V2']:.3f} ({srn['V2'][0]} concrete / {srn['V2'][1]} vague) |")
o.append(f"| dependency_completeness | 0.15 | {dcv['V1']:.3f} ({dcn['V1'][0]}/{dcn['V1'][1]} Section refs resolve) | {dcv['V2']:.3f} ({dcn['V2'][0]}/{dcn['V2'][1]} Section refs resolve) |")
o.append(f"| section_coverage | 0.15 | {sc['V1']:.3f} ({h2['V1']}/{mx} H2 sections) | {sc['V2']:.3f} ({h2['V2']}/{mx} H2 sections) |")
o.append(f"| **quant_score** | | **{quant['V1']:.3f}** | **{quant['V2']:.3f}** |")
o.append("\n### Internal contradictions counted for IC (established in diff analysis, orchestrator verification and debate)\n")
for k in ("V1", "V2"):
    o.append(f"**{k}** ({len(internal[k])}):")
    for x in internal[k]:
        o.append(f"- {x}")
    o.append("")
o.append("Note on IC: the denominator is the number of lines that carry a file:line citation (a proxy for scorable, falsifiable claims); the numerators are the internal inconsistencies actually established, so IC is high for both and differentiates weakly. Note on SR: the concrete-indicator regex is deliberately broad (numbers with units, file names, hashes, line refs), so SR is near 1.0 for both reports and differentiates weakly.")
(ROOT / "partials" / "quant-section.md").write_text("\n".join(o) + "\n")
print(json.dumps({k: {m: round(res[m][k], 3) for m in ("rc", "ic", "sr", "dc", "sc", "quant")} for k in V}, indent=1))
print(claims, srn, dcn, h2)
print(rc_detail)
