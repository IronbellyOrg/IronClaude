import re, sys
from pathlib import Path
O, P = Path(sys.argv[1]), Path(sys.argv[2])
card = (O / "t1-card.md").read_text()
secs = {m.group(1): m for m in re.finditer(r"^## (.+)$", card, re.M)}
def sec(name):
    names = list(secs); i = names.index(name); start = secs[name].start()
    end = secs[names[i+1]].start() if i + 1 < len(names) else len(card)
    return card[start:end].strip()
plan = P / f"{P.name}.md"
spec = P / "source.md"
def hunk(path, a=None, b=None, lang="markdown"):
    lines = Path(path).read_text().splitlines()
    a = a or 1; b = b or len(lines)
    return f"### {path}:{a}-{b}\n```{lang}\n" + "\n".join(lines[a-1:b]) + "\n```\n"
speclines = spec.read_text().splitlines()
heads = [i+1 for i, l in enumerate(speclines) if re.match(r"^## ", l)] + [len(speclines)+1]
spec_hunks = "".join(hunk(spec, heads[i], heads[i+1]-1) for i in range(len(heads)-1))
triage = (O / "artifacts/unmapped-triage.yaml").read_text().split("rows:")[0]
cov = f"Coverage: Pass 1 parsed 0 ids; Pass 2 inferred 338 rows (artifacts/inferred-requirements.yaml); containment matched 111 (coverage_pct_union 0.3284, artifacts/coverage-matrix.yaml); by-reference triage of the 227 unmatched rows (artifacts/unmapped-triage.yaml):\n```yaml\n{triage}```\nThe 5 needs-review rows are spec §2.1 (source.md:57-72): no plan task cites §2.1.\n"
common = ("You are a read-only Tier-2 reviewer for a /sc:reflect UC-1 (pre-execution) run. Plan under review = the tasklist in your grounding hunks (cite it as plan:<line>); driving spec = source.md (cite source.md:<line>); repo files cite as path:line. "
          "Start adversarial: assume defects exist. Verify each T1 finding in your slice (confirm, refute with evidence, or correct its severity) and add NEW findings the T1 card missed. Classify each finding's origin as plan or spec-inherited, and its deviation class vs the spec as one of authorized | necessary | drift | regression (regression = the plan contradicts a spec acceptance criterion or constraint). Do not execute anything.\n")
personas = {
 1: ("analyzer", ["Summary", "Spec contradictions", "Feasibility vs code"],
     hunk("src/superclaude/cli/install_codegraph.py", 1, 60, "python") + hunk("src/superclaude/cli/install_codegraph.py", 271, 365, "python") + hunk("src/superclaude/cli/install_mcp.py", 1, 30, "python") + hunk("src/superclaude/cli/install_mcp.py", 854, 925, "python")),
 2: ("qa", ["Summary", "Coverage gaps", "Acceptance-command defects"],
     "Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.\n\n" + spec_hunks),
 3: ("refactorer", ["Summary", "Stand-alone defects", "Structural signals"],
     hunk(".github/workflows/test.yml", 1, 40, "yaml") + hunk(".github/workflows/test.yml", 130, 175, "yaml")),
}
for n, (persona, names, extra) in personas.items():
    body = f"# Reviewer {n} brief (persona: {persona})\n\n{common}\n## T1 card excerpt\n\n" + "\n\n".join(sec(x) for x in names)
    body += "\n\n## Grounding hunks\n\n" + hunk(plan) + extra
    body += "\n## Coverage slice\n\n" + cov
    (O / f"reviewer-briefs/reviewer-{n}.md").write_text(body)
    print(n, persona, len(body))
