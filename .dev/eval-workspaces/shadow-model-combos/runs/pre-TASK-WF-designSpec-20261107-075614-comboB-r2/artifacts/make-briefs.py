"""Step 3B.0: materialize the three reviewer briefs (verbatim slices, hunks by line range)."""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
R = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614"
SPEC = f"{R}/source.md"
PLAN = f"{R}/TASK-WF-designSpec-20261107-075614.md"
card = (out / "t1-card.md").read_text(encoding="utf-8")


def section(title_prefix):
    m = re.search(rf"^## {re.escape(title_prefix)}.*?(?=^## |\Z)", card, re.S | re.M)
    return m.group(0).rstrip() + "\n"


def hunk(path, a, b, lang):
    lines = (root / path).read_text(encoding="utf-8").splitlines()
    body = "\n".join(lines[a - 1 : b])
    fence = "````" if "```" in body else "```"
    return f"### {path}:{a}-{b}\n\n{fence}{lang}\n{body}\n{fence}\n"


FINDINGS_LINE = (
    "End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. "
    "Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), "
    "category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens \"reflect-pre\", "
    "claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, "
    "a repo-relative path, line_start, line_end and an optional quote). Example line: "
    "{\"id\":\"F1\",\"severity\":\"MAJOR\",\"blocking\":false,\"category\":\"contradiction\",\"lens\":\"reflect-pre\","
    "\"claim\":\"Task 3 says X but task 5 says Y.\",\"refs\":[\"R-1\"],\"citations\":[{\"role\":\"plan\",\"path\":\"plan.md\",\"line_start\":10,\"line_end\":12}]}. "
    "After the block add a reviewer_model_self_report line stating the model you are running as in one line."
)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
CG = f"codegraph run state: index_state=fresh checked_at={now} worktree_root={root} projectPath={root}"

TSG = "tests/pr_submit/test_static_grep.py"
RTS = "src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh"
common = [
    hunk(TSG, 35, 36, "python"),
    hunk(TSG, 107, 132, "python"),
    hunk(TSG, 481, 487, "python"),
    hunk(TSG, 540, 552, "python"),
    hunk(RTS, 46, 51, "bash"),
]

matrix = json.loads((out / "artifacts/coverage-matrix.json").read_text())["matrix"]


def table(rows):
    head = "| Requirement / Task | Card ID | Status | Grounding |\n|--------------------|---------|--------|-----------|\n"
    body = ""
    for r in rows:
        q = r["quote"].replace("|", "\\|")
        if len(q) > 90:
            q = q[:87] + "..."
        tid = ", ".join(r["matched_task_ids"]) or "none"
        st = "covered" if r["matched_task_ids"] else "UNMAPPED by rule"
        body += f"| {r['id']}: {q} | {tid} | {st} ({r['match_method']} {r['ratio']}) | {r['citation']} |\n"
    return head + body


briefs = {
    1: dict(
        excerpt=section("Summary") + "\n" + section("Findings"),
        hunks=[hunk(SPEC, 73, 172, "markdown"), hunk(PLAN, 52, 90, "markdown")] + common,
        rows=[r for r in matrix if r["line"] <= 215],
    ),
    2: dict(
        excerpt=section("Coverage (UC-1)") + "\n" + section("Risks not findings"),
        hunks=[hunk(SPEC, 1, 378, "markdown"), hunk(PLAN, 1, 28, "markdown")] + common,
        rows=matrix,
    ),
    3: dict(
        excerpt=section("Findings") + "\n" + section("Recommendations"),
        hunks=[hunk(SPEC, 212, 256, "markdown"), hunk(SPEC, 283, 301, "markdown"), hunk(PLAN, 92, 200, "markdown")] + common,
        rows=[r for r in matrix if r["line"] > 215],
    ),
}
d = out / "reviewer-briefs"
d.mkdir(exist_ok=True)
for n, b in briefs.items():
    text = (
        f"# Reviewer brief {n}\n\n## T1 card excerpt\n\n{re.sub(r'^## ', '### ', b['excerpt'], flags=re.M)}\n{FINDINGS_LINE}\n\n"
        f"## Grounding hunks\n\n{CG}\n\n" + "\n".join(b["hunks"]) + f"\n## Coverage slice\n\n{table(b['rows'])}"
    )
    (d / f"reviewer-{n}.md").write_text(text, encoding="utf-8")
    print(n, len(text), "bytes", len(b["rows"]), "rows")
