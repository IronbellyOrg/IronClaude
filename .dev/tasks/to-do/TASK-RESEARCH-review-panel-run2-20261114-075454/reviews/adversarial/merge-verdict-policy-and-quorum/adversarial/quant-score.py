import re, json, sys
base = "/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/merge-verdict-policy-and-quorum/adversarial/"
V = {"A": open(base + "variant-1-original.md").read(), "B": open(base + "variant-2-original.md").read()}

# Requirement topics from the C-03 conflict row (no formal IDs, so topic/keyword matching per protocol edge case)
REQ = {
 "R01 any-blocking union policy": r"any-blocking|`union`|union",
 "R02 pluggable/named policy": r"pluggable|named polic|policy registry|`policy\(|policy interface",
 "R03 quorum over recorded completion states": r"completion state|COMPLETION_STATES|reviewers_complete|completion records",
 "R04 DEGRADED-style partial-panel outcome": r"DEGRADED",
 "R05 calibrator role in default stated": r"calibrat",
 "R06 evidence gate / adversarial merge / debate (reflect legacy)": r"evidence gate|adversarial merge|debate",
 "R07 quorum-supported clusters / k-of-n": r"k-of-n|2-of-3|quorum-supported|cluster support|`support`",
 "R08 INV-I fail-closed": r"INV-I\b|fail-closed|never PASS",
 "R09 INV-B 36-test verdict matrix": r"INV-B|36-test|36 `def test_`|36 tests",
 "R10 INV-L shadow": r"INV-L|shadow",
 "R11 INV-A contract 1.8.0": r"INV-A|1\.8\.0",
 "R12 research 03 cited": r"research/03|\br03\b",
 "R13 research 06 cited": r"research/06|\br06\b",
 "R14 research 07 cited": r"research/07|\br07\b",
 "R15 research 08 cited": r"research/08|\br08\b",
 "R16 research 12 cited": r"research/12|\br12\b",
 "R17 research 17 cited": r"research/17|\br17\b|defect register",
 "R18 PR-review effect": r"PR review|PR-review|PR flow",
 "R19 rf-qa effect": r"rf-qa",
 "R20 test or measurement": r"replay|quorum matrix|property test|falsifier",
 "R21 strongest objection answered": r"[Oo]bjection",
 "R22 exit codes 0/10/11 discussed": r"0/10/11|exit 10|10 and 11|exit code",
}
out = {}
for k, t in V.items():
    hits = {n: bool(re.search(p, t)) for n, p in REQ.items()}
    rc = sum(hits.values()) / len(REQ)
    # claims = tagged claims
    claims = len(re.findall(r"\[(?:CODE-VERIFIED|CODE-CONTRADICTED|UNVERIFIED|VERIFIED)[^\]]*\]", t))
    # contradictions: intra-variant, from diff-analysis X-005 (A), X-006 and X-003(E11 vs E16) (B)
    contra = {"A": 1, "B": 2}[k]
    ic = 1 - contra / claims
    # specificity
    body = [l for l in t.splitlines() if l.strip() and not l.startswith("#")]
    text = "\n".join(body)
    concrete = len(re.findall(r"`[^`]+`", text)) + len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))
    vague = len(re.findall(r"\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices|industry standard)\b", text, re.I))
    sr = concrete / (concrete + vague)
    # dependency completeness: 'section N(.N)' refs resolved against headings; B also E-n refs
    heads = set(re.findall(r"^#{2,3} (\d+(?:\.\d+)?)[ .]", t, re.M))
    refs = re.findall(r"\b[Ss]ections? (\d+(?:\.\d+)?)", t)
    refs += re.findall(r"\bsections? (\d+(?:\.\d+)?) (?:and|to) (\d+(?:\.\d+)?)", t)  # pairs handled loosely
    refs = [r if isinstance(r, str) else r[0] for r in refs]
    resolved = sum(1 for r in refs if r in heads or r.split(".")[0] in heads)
    total = len(refs)
    if k == "B":
        defined = set(re.findall(r"^\| (E\d+) \|", t, re.M))
        erefs = re.findall(r"\bE(\d+)\b", t)
        erefs = ["E"+e for e in erefs]
        resolved += sum(1 for e in erefs if e in defined)
        total += len(erefs)
    dc = resolved / total if total else 1.0
    sc_count = len(re.findall(r"^## ", t, re.M))
    out[k] = dict(RC=rc, RC_hits=sum(hits.values()), RC_total=len(REQ), RC_missing=[n for n,h in hits.items() if not h],
                  claims=claims, contra=contra, IC=ic, concrete=concrete, vague=vague, SR=sr,
                  refs_total=total, refs_resolved=resolved, DC=dc, sections=sc_count)
mx = max(v["sections"] for v in out.values())
for k in out:
    out[k]["SC"] = out[k]["sections"] / mx
    o = out[k]
    o["quant"] = 0.30*o["RC"] + 0.25*o["IC"] + 0.15*o["SR"] + 0.15*o["DC"] + 0.15*o["SC"]
print(json.dumps(out, indent=1))
