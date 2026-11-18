"""Step 3B.0: materialize reviewer-1..3 briefs (three sections each) from the T1 card, spec/plan hunks and the coverage matrix."""
import json
import re
import sys

root, out = sys.argv[1], sys.argv[2]
B = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
SPEC, PLAN = B + "source.md", B + "TASK-WF-designSpec-20261107-075614.md"
spec = open(f"{root}/{SPEC}", encoding="utf-8").read().splitlines()
plan = open(f"{root}/{PLAN}", encoding="utf-8").read().splitlines()
card = open(f"{out}/t1-card.md", encoding="utf-8").read()
matrix = json.load(open(f"{out}/artifacts/coverage-matrix.json"))["rows"]

INSTR = ('End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. '
         'Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), '
         'category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", '
         'claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, '
         'a repo-relative path, line_start, line_end and an optional quote). Example line: '
         '{"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],'
         '"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. '
         'After the block add a reviewer_model_self_report line stating the model you are running as in one line.')
EXTRA = ('Write the literal heading `## Findings block` and open the fence with ```findings-v2 (not ```json). Keep each claim at or under 300 characters and each quote at or under 200. '
         'After the self-report line add `rows_verified:` followed by the assigned row ids you actually checked. '
         'Return the whole card as your final message; you are read-only, the orchestrator saves it.')


def hunk(path, a, b, lines, lang="text"):
    body = "\n".join(lines[a - 1:b])
    return f"### {path}:{a}-{b}\n\n````{lang}\n{body}\n````\n"


def section(title, start, end):
    m = re.search(rf"^{re.escape(title)}\n(.*?)(?=^### |^## |\Z)", card[card.index(start):], re.S | re.M)
    return None


def between(a, b=None):
    i = card.index(a)
    j = card.index(b) if b else len(card)
    return card[i:j].rstrip() + "\n"


head = card[:card.index("## Findings")]  # header + coverage block (shared context)
slices = {
    1: between("### Deviation / root-cause slice", "### Coverage / acceptance slice"),
    2: between("### Coverage / acceptance slice", "### Structural / tech-debt slice"),
    3: between("### Structural / tech-debt slice", "## Refuted candidates"),
}
refuted = between("## Refuted candidates", "## Grounding gaps")
demote = lambda t: re.sub(r"^## ", "#### ", t, flags=re.M)  # card headings must not become brief sections
head, refuted = demote(head), demote(refuted)

CG = ("codegraph run state: index_state=fresh checked_at=2026-11-13T04:04:27Z "
      "worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel "
      "projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel\n")

assigned = {1: range(17, 48), 2: list(range(1, 17)) + list(range(64, 91)), 3: range(48, 64)}
persona = {
    1: ("analyzer", "You are reviewer 1, persona analyzer: hunt contradictions, wrong outcomes and missing cases between the design spec and the plan's tasks, especially in the decision tables, the fold and the resume logic."),
    2: ("qa", "You are reviewer 2, persona qa: hunt acceptance criteria that cannot fail, requirements with no checking criterion, and spec statements the plan never tests. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding."),
    3: ("refactorer", "You are reviewer 3, persona refactorer: hunt structural problems in the plan: wrong or missing dependencies, a task that narrows or drops spec scope, work placed in the wrong task, ordering hazards, and constraints no task enforces."),
}

hunks = {
    1: [hunk(SPEC, 97, 171, spec), hunk(SPEC, 173, 210, spec), hunk(PLAN, 52, 90, plan)],
    2: [hunk(SPEC, 1, len(spec), spec), hunk(PLAN, 159, 173, plan), hunk(PLAN, 188, 200, plan), hunk(PLAN, 17, 27, plan)],
    3: [hunk(SPEC, 236, 256, spec), hunk(SPEC, 283, 302, spec), hunk(PLAN, 116, 156, plan), hunk(PLAN, 17, 27, plan)],
}

for n in (1, 2, 3):
    name, lens = persona[n]
    rows = [r for r in matrix if int(r["requirement_id"].split("-")[1]) in set(assigned[n])]
    tbl = ["| Requirement / Task | Card ID | Status | Grounding |", "|--------------------|---------|--------|-----------|"]
    for r in rows:
        q = r["quote"].replace("|", "/")
        q = (q[:72] + "...") if len(q) > 75 else q
        status = (f"matched {r['matched_task_ids'][0]} ({r['best_ratio']})" if r["matched_task_ids"] else f"unmatched by containment ({r['best_ratio']})")
        tbl.append(f"| {r['requirement_id']}: {q} | - | {status} | source.md:{r['citation_line']} |")
    text = (
        f"# Reviewer brief {n} ({name})\n\n{lens}\n\n"
        "Audit the plan (tasklist) against its driving spec before execution. The plan was already executed once; judge what the plan and spec say, "
        "not the state of HEAD, and do not report a post-implementation difference as a plan defect. Read-only: no edits, no shell, no git.\n"
        f"Full files, if you need more than the hunks: spec `{SPEC}`, plan `{PLAN}` (Read, Grep and Glob are allowed).\n\n"
        "## T1 card excerpt\n\n" + head.rstrip() + "\n\n" + slices[n] + "\n" + (refuted if n == 1 else "") + "\n"
        + INSTR + " " + EXTRA + "\n\n"
        "## Grounding hunks\n\n" + CG + "\n" + "\n".join(hunks[n]) + "\n"
        "## Coverage slice\n\n" + "\n".join(tbl) + "\n\n"
        f"Assigned rows: {', '.join(r['requirement_id'] for r in rows)}.\n"
    )
    open(f"{out}/reviewer-briefs/reviewer-{n}.md", "w", encoding="utf-8").write(text)
    print(n, len(text), "chars", len(rows), "rows")
json.dump({f"reviewer-{n}": {"assigned": [r["requirement_id"] for r in matrix if int(r["requirement_id"].split("-")[1]) in set(assigned[n])]} for n in (1, 2, 3)},
          open(f"{out}/artifacts/assigned-rows.json", "w"))
