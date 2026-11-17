"""Step 3B.0: materialize the three reviewer briefs (three sections each, verbatim hunks)."""
import re

OUT = ".dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116185848"
PLAN = ".dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md"
SRC = ".dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md"
PF = ".dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115"
SPEC = PF + "/02-brainstorm/merged-requirements.md"
S1 = ".dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md"
S3 = ".dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md"
PREV = ".dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116174316/REPORT.md"
MW = "src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md"
SK = "src/superclaude/skills/sc-implement-protocol/SKILL.md"
QA = "src/superclaude/skills/sc-implement-protocol/refs/qa.md"
WC = "src/superclaude/core/WORKER-CONTRACT.md"
TR = "src/superclaude/skills/tech-research/SKILL.md"
STAT = "tests/skills/test_implement_severity_static.py"

CODEGRAPH = ("codegraph run state: index_state=not-used checked_at=2026-11-16T18:58:48Z "
             "worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel "
             "projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel "
             "(the files under review are Markdown plans; use Read, Grep and Glob only)")


def hunk(path, a, b):
    lines = open(path, encoding="utf-8").read().split("\n")[a - 1:b]
    body = "\n".join(lines)
    return f"### {path}:{a}-{b}\n\n````text\n{body}\n````\n"


def card_slice(names):
    text = open(f"{OUT}/t1-card.md", encoding="utf-8").read()
    parts = re.split(r"(?m)^(?=## )", text)
    keep = [p for p in parts if any(p.startswith("## " + n) for n in names)]
    return re.sub(r"(?m)^## ", "#### ", "".join(keep).strip()) + "\n"


MATRIX = {
    "INF-001": "Constraints", "INF-002": "Constraints", "INF-003": "Task 7", "INF-004": "Task 8", "INF-005": "Task 8",
    "INF-006": "Constraints", "INF-007": "Constraints", "INF-008": "Constraints", "INF-009": "Constraints (by hand)",
    "INF-010": "Task 3", "INF-011": "Constraints", "INF-012": "Constraints", "INF-013": "Constraints",
    "INF-014": "Task 8", "INF-015": "Task 7", "INF-016": "Task 5", "INF-017": "Task 4", "INF-018": "Task 2",
    "INF-019": "Task 3", "INF-020": "Constraints", "INF-021": "Constraints", "INF-022": "Task 2 (by hand)",
}


def slice_rows(ids):
    out = ["## Coverage slice", "", "| Requirement (inferred row of source.md) | Plan item | Status | Grounding |", "|---|---|---|---|"]
    for i in ids:
        out.append(f"| {i} | {MATRIX['INF-%03d' % i]} | covered | artifacts/inferred-table.md |")
    return "\n".join(out) + "\n"


BRIEFS = {
    1: dict(
        persona="analyzer",
        card=["Earlier blocking findings", "Findings of this card"],
        hunks=[(PLAN, 17, 34), (PLAN, 38, 68), (PLAN, 72, 127), (MW, 40, 64), (SK, 186, 198), (WC, 30, 40),
               (QA, 222, 226), (QA, 274, 290), (TR, 476, 492), (TR, 504, 518), (STAT, 290, 300)],
        rows=[7, 8, 10, 11, 12, 13, 16, 17, 18, 19],
    ),
    2: dict(
        persona="qa",
        card=["Coverage", "Earlier blocking findings"],
        hunks=[(SRC, 1, 94), (PLAN, 17, 34), (PLAN, 131, 153), (SPEC, 430, 441), (SPEC, 938, 952), (PREV, 24, 63)],
        rows=list(range(1, 23)),
    ),
    3: dict(
        persona="refactorer",
        card=["Findings of this card", "Preliminary verdict"],
        hunks=[(PLAN, 17, 34), (PLAN, 53, 68), (PLAN, 72, 89), (PLAN, 131, 153), (S1, 120, 130), (S1, 162, 173),
               (S1, 188, 213), (S3, 19, 25), (S3, 38, 52), (S3, 203, 210)],
        rows=[3, 4, 5, 14, 15, 20, 21, 22],
    ),
}

for n, b in BRIEFS.items():
    parts = ["## T1 card excerpt", "", card_slice(b["card"])]
    if b["persona"] == "qa":
        parts.append("Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.\n")
    parts += ["", "## Grounding hunks", "", CODEGRAPH, ""]
    for h in b["hunks"]:
        parts.append(hunk(*h))
    parts += ["", slice_rows(b["rows"])]
    text = "\n".join(parts)
    # the brief carries exactly three H2 sections and no shell or git instruction
    outside = re.sub(r"````text\n.*?\n````", "", text, flags=re.S)
    assert len(re.findall(r"(?m)^## ", outside)) == 3, (n, re.findall(r"(?m)^## .*", outside))
    open(f"{OUT}/reviewer-briefs/reviewer-{n}.md", "w", encoding="utf-8").write(text)
    print(n, b["persona"], len(text))
