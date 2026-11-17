import re, json
base = "/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/tasklist-medium-and-fidelity-vocab/adversarial/"
V = {"A": open(base + "variant-1-original.md").read(), "B": open(base + "variant-2-original.md").read()}

# Requirement topics from conflict row X-15 and the task brief (no formal requirement IDs, so topic/keyword matching per the protocol edge case)
REQ = {
 "R01 tasklist Medium decision (blocking or not)": r"Medium (?:as|is|stays|keeps)|keeps Medium|adopts `?Medium",
 "R02 label map to the core severity pair": r"CRITICAL.{0,80}MAJOR|MAJOR.{0,80}MINOR",
 "R03 fidelity prompt placement relative to the core": r"outside the core|under the core|module vocabulary|separate gate",
 "R04 CLI gate HIGH-only exit / frontmatter fields": r"high_severity_count|tasklist_ready",
 "R05 repo rule S1-S5 cited": r"S1-S5|S1 to S5|\bS1\b",
 "R06 S4 own-severity-model clause discussed": r"\bS4\b",
 "R07 research 12 cited": r"research/12|research 12|\b12\b, \b11\b|RT research/12",
 "R08 research 11 cited": r"research/11|research 11",
 "R09 research 05 cited": r"research/05|research 05|\b05\b",
 "R10 gaps GQ-060 / GQ-160": r"GQ-060|GQ-160",
 "R11 INV-J (S1-S5 binary rule, 2 fix cycles)": r"INV-J",
 "R12 INV-M (reflect_status closed enum)": r"INV-M",
 "R13 P2 patch loop behaviour": r"\bP2\b|patch loop",
 "R14 pinned tests (sweep rows, test_j, worker-contract)": r"test_j|sweep|worker_contract|S-119",
 "R15 C-01 dependency": r"C-01",
 "R16 C-02 dependency": r"C-02",
 "R17 C-03 dependency": r"C-03",
 "R18 PR code review effect": r"PR code review|PR review|\bC-10\b",
 "R19 rf-qa effect": r"rf-qa",
 "R20 test or measurement": r"M-X15|\bM1\b|Static tests|measurement",
 "R21 strongest objection answered": r"[Oo]bjection",
 "R22 shared SPEC_FIDELITY_GATE contract": r"SPEC_FIDELITY_GATE",
 "R23 Medium kept out of the core schema": r"no `?Medium`? token|`Medium` stays out|no new core token|Medium. has no schema value",
 "R24 exit code / gate behaviour unchanged": r"exit code|exits 1",
}
out = {}
# intra-variant contradictions from diff-analysis.md: X-008 (A: skill-vs-CLI 'not one code path' vs 'one product'), X-002 (B: 'skill's own model' vs 'skill states no model')
contra_map = {"A": 1, "B": 1}
for k, t in V.items():
    hits = {n: bool(re.search(p, t)) for n, p in REQ.items()}
    rc = sum(hits.values()) / len(REQ)
    claims = len(re.findall(r"\[(?:CODE-VERIFIED|CODE-CONTRADICTED|UNVERIFIED|VERIFIED|READ)[^\]]*\]", t))
    ic = 1 - contra_map[k] / claims
    body = [l for l in t.splitlines() if l.strip() and not l.startswith("#")]
    text = "\n".join(body)
    concrete = len(re.findall(r"`[^`]+`", text)) + len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))
    vague = len(re.findall(r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices|industry standard)\b", text, re.I))
    sr = concrete / (concrete + vague)
    # internal references: 'section N(.N)' resolved against numbered headings; B also E<n> refs resolved against E<n>. definitions
    heads = set(re.findall(r"^#{2,3} (\d+(?:\.\d+)?)[ .]", t, re.M))
    refs = re.findall(r"\b[Ss]ections? (\d+(?:\.\d+)?)", t)
    resolved = sum(1 for r in refs if r in heads or r.split(".")[0] in heads)
    total = len(refs)
    if k == "B":
        defined = set(re.findall(r"^(E\d+)\. ", t, re.M))
        erefs = ["E" + e for e in re.findall(r"\bE(\d+)\b", t)]
        resolved += sum(1 for e in erefs if e in defined)
        total += len(erefs)
    dc = resolved / total if total else 1.0
    sc_count = len(re.findall(r"^## ", t, re.M))
    out[k] = dict(RC=rc, RC_hits=sum(hits.values()), RC_total=len(REQ), RC_missing=[n for n, h in hits.items() if not h],
                  claims=claims, contra=contra_map[k], IC=ic, concrete=concrete, vague=vague, SR=sr,
                  refs_total=total, refs_resolved=resolved, DC=dc, sections=sc_count)
mx = max(v["sections"] for v in out.values())
for k in out:
    out[k]["SC"] = out[k]["sections"] / mx
    o = out[k]
    o["quant"] = 0.30 * o["RC"] + 0.25 * o["IC"] + 0.15 * o["SR"] + 0.15 * o["DC"] + 0.15 * o["SC"]
print(json.dumps(out, indent=1))
