"""Step 3B.0: materialize <output>/reviewer-briefs/reviewer-<N>.md (three sections, verbatim hunks).
Usage: uv run python make-briefs.py <output> <spec> <plan> <worktree_root> <checked_at>
"""
import json
import sys

out, spec_p, plan_p, wt, checked = sys.argv[1:6]
spec = open(spec_p).read().split("\n")
plan = open(plan_p).read().split("\n")
card = open(out + "/t1-card.md").read().split("\n")
cov = json.load(open(out + "/artifacts/coverage-matrix.json"))
rows = cov["rows"]


def hunk(label, path, lines, a, b, lang="markdown"):
    body = "\n".join(lines[a - 1:b])
    return "### %s:%d-%d\n\n````%s\n%s\n````\n" % (label, a, b, lang, body)


def sect(start, end=None):
    """1-based inclusive card lines from the heading starting with `start` up to (excluding) the heading `end`."""
    a = next(i for i, l in enumerate(card) if l.startswith(start))
    b = next((i for i, l in enumerate(card) if end and i > a and l.startswith(end)), len(card))
    return "\n".join(card[a:b]).rstrip() + "\n"


header = "\n".join(card[0:5]).rstrip() + "\n"
SHADOW_LINE = (
    'End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. '
    'Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), '
    'category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", '
    'claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, '
    'a repo-relative path, line_start, line_end and an optional quote). Example line: '
    '{"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],'
    '"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. '
    'After the block add a reviewer_model_self_report line stating the model you are running as in one line.'
)
RSPEC = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md"
RPLAN = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md"
RBASE = ".dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboB-r3/artifacts/base-grounding.md"
base = open(out + "/artifacts/base-grounding.md").read().split("\n")
RSTATE = "codegraph run state: index_state=fresh checked_at=%s worktree_root=%s projectPath=%s\n" % (checked, wt, wt)

personas = {
    1: dict(name="analyzer", rows=(0, 25),
            card=header + "\n" + sect("## Findings", "## Verified"),
            hunks=[hunk(RSPEC, spec_p, spec, 99, 171), hunk(RPLAN, plan_p, plan, 52, 78)]),
    2: dict(name="qa", rows=(25, 50),
            card=header + "\n" + sect("## Coverage", "## Findings"),
            hunks=[hunk(RSPEC, spec_p, spec, 1, 378)]),   # D13: whole spec body (378 lines <= 400)
    3: dict(name="refactorer", rows=(50, 75),
            card=header + "\n" + sect("## Verified", None),
            hunks=[hunk(RPLAN, plan_p, plan, 17, 27), hunk(RSPEC, spec_p, spec, 283, 301), hunk(RBASE, "base", base, 1, len(base))]),
}
for n, p in personas.items():
    a, b = p["rows"]
    mine = rows[a:b]
    tbl = ["| Requirement / Task | Card ID | Status | Grounding |", "|---|---|---|---|"]
    for r in mine:
        st = "covered (%s %.2f)" % (r["match_method"], r["best_ratio"]) if r["matched_task_ids"] else "UNMATCHED by containment (best %s %.2f)" % (r["best_task"], r["best_ratio"])
        tbl.append("| %s: %s | %s | %s | %s |" % (r["requirement_id"], r["quote"][:90].replace("|", "/"), ",".join(r["matched_task_ids"]) or "none", st, r["citation"]))
    text = "# Reviewer brief %d (persona: %s)\n\n" % (n, p["name"])
    text += "## T1 card excerpt\n\n" + p["card"] + "\n" + SHADOW_LINE + "\n\n"
    text += "## Grounding hunks\n\n" + RSTATE + "\n"
    text += "Files you may Read directly (repo-relative): %s (spec), %s (plan), %s (base-commit excerpts). Cite spec/plan lines by these paths.\n\n" % (RSPEC, RPLAN, RBASE)
    text += "\n".join(p["hunks"]) + "\n"
    text += "## Coverage slice\n\n" + "\n".join(tbl) + "\n"
    open("%s/reviewer-briefs/reviewer-%d.md" % (out, n), "w").write(text)
    print(n, p["name"], len(text), "bytes", len(mine), "rows")
json.dump({"reviewer-%d" % n: {"assigned": [r["requirement_id"] for r in rows[p["rows"][0]:p["rows"][1]]]} for n, p in personas.items()},
          open(out + "/artifacts/assigned-rows.json", "w"), indent=1)
