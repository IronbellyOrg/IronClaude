import re, json
base = "/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/consumer-entry-effect-and-delivery/adversarial/"
V = {"A": open(base + "variant-1-original.md").read(), "B": open(base + "variant-2-original.md").read()}

# Requirement topics from the C-05 conflict row and the slot brief (no formal IDs, so topic/keyword matching per protocol edge case)
REQ = {
 "R01 conflict rows C-S7, CO-25, CO-35 named": r"C-S7[\s\S]*CO-25[\s\S]*CO-35|CO-25[\s\S]*CO-35",
 "R02 entry position (reflect UC-1 vs direct call)": r"UC-1|direct (?:panel )?call",
 "R03 effect at generation time (advisory vs revise loop)": r"advisory|revise loop",
 "R04 blocking at execution gate T5": r"\bT5\b",
 "R05 plugin delivery position": r"plugin copy|plugin delivery",
 "R06 no call-site change / call-site shape": r"call sites? (?:unchanged|do not change)|call-site|call sites",
 "R07 INV-M closed enum reflect_status": r"INV-M|reflect_status",
 "R08 INV-B 36-test verdict matrix": r"INV-B|36 `def test_`|36 tests|36-test",
 "R09 INV-N plugin parity pins": r"INV-N|parity",
 "R10 INV-K sync-dev / edit fence": r"INV-K|sync-dev|edit fence|fence",
 "R11 INV-J repo review rule S1-S5": r"INV-J|S1-S5",
 "R12 consistency with C-01": r"C-01",
 "R13 consistency with C-02": r"C-02",
 "R14 consistency with C-03": r"C-03",
 "R15 C-04 engine composition noted": r"C-04",
 "R16 DO4 owner decision": r"DO4",
 "R17 research 11 cited": r"research/11|\br11\b",
 "R18 research 18 cited": r"research/18|\br18\b",
 "R19 research 12 cited": r"research/12|\br12\b",
 "R20 research 13 cited": r"research/13|\br13\b|section 7",
 "R21 PR-review effect": r"PR review|PR code review|PR-review",
 "R22 rf-qa effect": r"rf-qa",
 "R23 test or measurement": r"replay|measurement",
 "R24 strongest objection answered": r"[Oo]bjection",
 "R25 code-verified tags": r"CODE-VERIFIED",
 "R26 stage 10.5 and Wave 4 line cites": r"SKILL\.md:(?:89|93|1630|1640|1646)",
 "R27 quick-depth rule D1": r"\bD1\b|quick",
}
out = {}
for k, t in V.items():
    hits = {n: bool(re.search(p, t)) for n, p in REQ.items()}
    rc = sum(hits.values()) / len(REQ)
    claims = len(re.findall(r"\[(?:CODE-VERIFIED|CODE-CONTRADICTED|UNVERIFIED|VERIFIED|RECOMPUTED)[^\]]*\]", t))
    # intra-variant contradictions found in the debate (see debate-transcript.md Section 'Intra-variant contradictions')
    # A: 1 (section 3 item 1 'panel can be switched on for both consumers with zero edits' vs D1 / objection 2: quick phases never reach)
    # B: 3 (E7 no tasklist lens vs section 2 'tasklist runs on the v1 engine'; contract 1.1 -> 1.2 bump vs pinned '1.1' readers;
    #       blocking effect placed at Stage 10.5 vs 10.5 fenced as non-executing and non-blocking)
    contra = {"A": 1, "B": 3}[k]
    ic = 1 - contra / claims
    body = [l for l in t.splitlines() if l.strip() and not l.startswith("#")]
    text = "\n".join(body)
    concrete = len(re.findall(r"`[^`]+`", text)) + len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))
    vague = len(re.findall(r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices|industry standard)\b", text, re.I))
    sr = concrete / (concrete + vague)
    heads = set(re.findall(r"^#{2,3} (\d+(?:\.\d+)?)[ .]", t, re.M))
    refs = re.findall(r"\bsections? (\d+(?:\.\d+)?)", t, re.I)
    resolved = sum(1 for r in refs if r in heads or r.split(".")[0] in heads)
    total = len(refs)
    if k == "A":
        items_defined = set(re.findall(r"^(\d+)\. ", t, re.M))
        irefs = re.findall(r"\bitems? (\d+)", t)
        resolved += sum(1 for i in irefs if i in items_defined)
        total += len(irefs)
    if k == "B":
        defined = set(re.findall(r"^(E\d+)\.", t, re.M))
        erefs = ["E" + e for e in re.findall(r"\bE(\d+)\b", t)]
        resolved += sum(1 for e in erefs if e in defined)
        total += len(erefs)
    dc = resolved / total if total else 1.0
    sc_count = len(re.findall(r"^## ", t, re.M))
    out[k] = dict(RC=rc, RC_hits=sum(hits.values()), RC_total=len(REQ), RC_missing=[n for n, h in hits.items() if not h],
                  claims=claims, contra=contra, IC=ic, concrete=concrete, vague=vague, SR=sr,
                  refs_total=total, refs_resolved=resolved, DC=dc, sections=sc_count)
mx = max(v["sections"] for v in out.values())
for k in out:
    out[k]["SC"] = out[k]["sections"] / mx
    o = out[k]
    o["quant"] = 0.30 * o["RC"] + 0.25 * o["IC"] + 0.15 * o["SR"] + 0.15 * o["DC"] + 0.15 * o["SC"]
print(json.dumps(out, indent=1))
