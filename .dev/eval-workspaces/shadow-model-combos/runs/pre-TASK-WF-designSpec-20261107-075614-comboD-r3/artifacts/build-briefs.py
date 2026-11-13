"""Step 3B.0: materialize one self-contained brief per reviewer (three sections, in order).
usage: uv run python build-briefs.py <out>   (run from the repo root)"""
import json, re, sys, pathlib, datetime

out = pathlib.Path(sys.argv[1])
SPEC = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md"
PLAN = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md"
spec = pathlib.Path(SPEC).read_text().splitlines()
plan = pathlib.Path(PLAN).read_text().splitlines()
card = (out / "t1-card.md").read_text()
cov = json.loads((out / "artifacts" / "coverage-matrix.json").read_text())["matrix"]
assigned = json.loads((out / "artifacts" / "assigned-rows.json").read_text())
rv = pathlib.Path("/home/coder/.claude/skills/sc-reflect-protocol/refs/reviewer-spec.md").read_text()
SHADOW = re.search(r"`(End your card with.*?in one line\.)`", rv).group(1)

def section(head):
    m = re.search(r"^## " + re.escape(head) + r".*?(?=^## |\Z)", card, re.S | re.M)
    return m.group(0).strip()

header = card.split("\n## ", 1)[0].strip().split("\n", 1)[1].strip()
persona_head = {1: ("analyzer", "Root cause and deviation"), 2: ("qa", "Coverage and acceptance"), 3: ("refactorer", "Structural and tech-debt")}
grounding = section("Grounding results")

def hunk(path, lines, a, b):
    body = "\n".join(lines[a - 1:b])
    return f"### {path}:{a}-{b}\n\n````markdown\n{body}\n````\n"

hunks = {
    1: [hunk(SPEC, spec, 129, 171), hunk(SPEC, spec, 187, 208), hunk(PLAN, plan, 52, 78)],
    2: [hunk(SPEC, spec, 1, len(spec))],
    3: [hunk(PLAN, plan, 12, 27), hunk(SPEC, spec, 238, 255), hunk(SPEC, spec, 358, 378)],
}
state = "codegraph run state: index_state=fresh checked_at=" + datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") + \
        " worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel"
byid = {m["requirement_id"]: m for m in cov}
for n in (1, 2, 3):
    persona, head = persona_head[n]
    rows = []
    for rid in assigned[f"reviewer-{n}"]:
        m = byid[rid]
        status = f"covered (containment {m['ratio']})" if m["matched_task_ids"] else f"lexically unmapped (best {m['ratio']})"
        card_id = m["matched_task_ids"][0] if m["matched_task_ids"] else "-"
        q = m["quote"].replace("|", "\\|")
        rows.append(f"| {rid}: {q} | {card_id} | {status} | source.md:{m['spec_line']} |")
    extra = ""
    if n == 2:
        extra = "\n\nAudit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding."
    text = f"""# Reviewer brief {n}: {persona}

## T1 card excerpt

{header}

{section(head)}

{grounding}

{SHADOW}{extra}

## Grounding hunks

{state}

{chr(10).join(hunks[n])}
## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
{chr(10).join(rows)}
"""
    (out / "reviewer-briefs" / f"reviewer-{n}.md").write_text(text)
    print(n, persona, len(text), "bytes;", len(assigned[f"reviewer-{n}"]), "rows")
print("reviewer_briefs_materialized: 3")
