"""Materialize the three Wave 3B.0 reviewer briefs (Step 3B.0). Run: uv run python mkbriefs.py <repo_root> <output_dir>"""
import datetime
import json
import os
import re
import sys

root, out = sys.argv[1], sys.argv[2]
rel = lambda p: os.path.relpath(p, root)
SNAP = f"{out}/artifacts/base-e8db2fe6"
IN = f"{root}/.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614"
SPEC, PLAN = f"{IN}/source.md", f"{IN}/TASK-WF-designSpec-20261107-075614.md"
card = open(f"{out}/t1-card.md", encoding="utf-8").read().split("\n")
matrix = json.load(open(f"{out}/artifacts/coverage-matrix.json"))["matrix"]
checked = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

FENCE = {".py": "python", ".sh": "bash", ".md": "markdown"}


def lines(path):
    return open(path, encoding="utf-8").read().split("\n")


def hunk(path, a, b, note=""):
    body = "\n".join(lines(path)[a - 1:b])
    lang = FENCE.get(os.path.splitext(path)[1], "text")
    fence = "`" * 5 if lang == "markdown" else "```"
    h = f"### {rel(path)}:{a}-{b}"
    if note:
        h += f"\n\n({note})"
    return f"{h}\n\n{fence}{lang}\n{body}\n{fence}\n"


def section(prefix):
    i = next(k for k, l in enumerate(card) if l.startswith(prefix))
    j = next((k for k in range(i + 1, len(card)) if card[k].startswith("## ")), len(card))
    return "\n".join(card[i:j]).rstrip()


def para(prefix):
    return next(l for l in card if l.startswith(prefix))


INSTR = ("End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. "
         "Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), "
         "category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens \"reflect-pre\", "
         "claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, "
         "a repo-relative path, line_start, line_end and an optional quote). Example line: "
         "{\"id\":\"F1\",\"severity\":\"MAJOR\",\"blocking\":false,\"category\":\"contradiction\",\"lens\":\"reflect-pre\",\"claim\":\"Task 3 says X but task 5 says Y.\",\"refs\":[\"R-1\"],"
         "\"citations\":[{\"role\":\"plan\",\"path\":\"plan.md\",\"line_start\":10,\"line_end\":12}]}. "
         "After the block add a reviewer_model_self_report line stating the model you are running as in one line.")

ASSIGN = {
    1: ("analyzer", [3, 6, 7, 8, 9, 10, 12, 13, 14, 24, 29]),
    2: ("qa", [1, 2, 16, 19, 21, 23, 25, 26, 27, 28, 30, 34, 35]),
    3: ("refactorer", [4, 5, 11, 15, 17, 20, 22, 31, 32, 33]),
}
PERSONA_TEXT = {
    "analyzer": "Persona: analyzer. Look for root causes of defects in the plan: contradictions between the plan and the spec or inside either one, "
                "acceptance criteria a wrong implementation would still pass, inputs a function needs but is never given, steps that cannot be carried out as written.",
    "qa": "Persona: qa. Look at coverage and acceptance: requirements the plan never turns into a task or a checkable criterion, criteria that cannot fail mechanically, "
          "tests the plan relies on that do not exist or would fail. Audit the coverage matrix AGAINST the spec body in your grounding hunks; "
          "surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.",
    "refactorer": "Persona: refactorer. Look at structure: task ordering and declared dependencies, files edited by several tasks, repository pins (tests that fail when text or counts change), "
                  "import and layering problems, work that lands in the wrong task.",
}

HUNKS = {
    1: [
        (SPEC, 99, 112, "function contracts incl. release_decision and resume_decision signatures"),
        (SPEC, 129, 171, "engage, release and resume decision tables"),
        (SPEC, 241, 241, "the Wave 0 bullet requirement"),
        (PLAN, 66, 78, "Task 4"),
        (PLAN, 132, 144, "Task 9"),
        (f"{SNAP}/src/superclaude/pr_submit/recovery.py", 33, 42, "base commit e8db2fe66"),
        (f"{SNAP}/src/superclaude/pr_submit/recovery.py", 69, 95, "base commit e8db2fe66"),
        (f"{SNAP}/src/superclaude/pr_submit/models.py", 20, 30, "base commit e8db2fe66"),
    ],
    2: [
        (SPEC, 1, 378, "the whole spec body (378 lines)"),
        (PLAN, 44, 50, "Task 2"),
        (PLAN, 104, 114, "Task 7"),
        (PLAN, 118, 130, "Task 8"),
        (f"{SNAP}/tests/skills/test_worker_contract.py", 1090, 1105, "base commit e8db2fe66"),
        (f"{SNAP}/tests/pr_submit/test_static_grep.py", 479, 484, "base commit e8db2fe66"),
    ],
    3: [
        (PLAN, 17, 27, "plan Constraints"),
        (PLAN, 29, 33, "Phase 1 and Task 1 heading"),
        (f"{SNAP}/src/superclaude/pr_submit/conflicts.py", 25, 36, "base commit e8db2fe66"),
        (f"{SNAP}/src/superclaude/pr_submit/fsm.py", 100, 112, "base commit e8db2fe66"),
        (f"{SNAP}/tests/pr_submit/test_static_grep.py", 37, 52, "base commit e8db2fe66"),
        (f"{SNAP}/tests/pr_submit/test_conflict_sync_protocol.py", 587, 610, "base commit e8db2fe66"),
        (f"{SNAP}/src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh", 1, 52, "base commit e8db2fe66; the model for the new script"),
    ],
}
# plan dependency lines (all reviewers' refactorer slice)
dep = [f"{i}: {l}" for i, l in enumerate(lines(PLAN), 1) if l.startswith("Depends on:") or re.match(r"^## Task \d+", l)]

EXCERPT = {
    1: lambda: "\n\n".join([para("Temporal anchor:"), para("H1 "), para("H2 ")]),
    2: lambda: "\n\n".join([section("## Coverage"), para("H3 "), para("H4 "), section("## Risk surface")]),
    3: lambda: "\n\n".join([section("## Facts verified"), section("## Risk surface"), section("## Recommendations")]),
}

for n, (persona, ids) in ASSIGN.items():
    rows = [r for r in matrix if int(r["requirement_id"].split("-")[1]) in ids]
    assert len(rows) == len(ids), (n, len(rows), len(ids))
    t = []
    t.append(f"# Reviewer {n} brief ({persona}), UC-1 pre-execution reflection, Tier 2\n")
    t.append("You are reviewer %d of 3. You are read-only: you may Read, Grep and Glob; you must not edit, write, move or delete anything, and you run no shell commands. "
             "Return one reviewer card as your reply (the orchestrator saves it). Audit the plan against its spec using only the evidence below and what you can Read.\n" % n)
    t.append(PERSONA_TEXT[persona] + "\n")
    t.append("Rules for evidence:\n"
             f"- Plan under review: `{rel(PLAN)}`. Spec it implements: `{rel(SPEC)}`. Cite plan and spec lines with role plan or spec and that repo-relative path.\n"
             f"- The spec says it read the repository at master `e8db2fe66`. The plan was executed afterwards, so the live checkout (HEAD) now holds the finished implementation and is NOT the code the plan was written against. "
             f"Read repository facts from the base-commit copy under `{rel(SNAP)}/` (same layout as the repository). Do not cite HEAD code as a defect of the plan; "
             "a claim that is true only at HEAD is later change, not a plan defect. Put code evidence in the claim text as `path:line` of the base copy; citations objects point only at the plan or spec.\n"
             "- The code graph index describes HEAD, not the base commit: do not use it for base-commit facts.\n"
             "- Do not read anything under `.dev/tasks/` and do not read other reflect or eval run directories; they hold the execution history, not the evidence.\n"
             "- Report a defect only when you can show it from a cited line. If a plan line is wrong, say what it should say. A zero-finding card is valid when you state which rows you verified.\n"
             "- Mark severity MAJOR or CRITICAL only when an implementer following the plan would produce a wrong outcome or the plan cannot be carried out; otherwise MINOR.\n")
    t.append("## T1 card excerpt\n")
    t.append(EXCERPT[n]() + "\n")
    t.append(INSTR + "\n")
    t.append("## Grounding hunks\n")
    t.append(f"codegraph run state: index_state=fresh checked_at={checked} worktree_root={root} projectPath={root}\n")
    for p, a, b, note in HUNKS[n]:
        t.append(hunk(p, a, b, note))
    if n == 3:
        t.append(f"### {rel(PLAN)}:dependency-lines\n\n(Task headings and every `Depends on:` line of the plan, as `plan line: text`)\n\n```text\n" + "\n".join(dep) + "\n```\n")
    t.append("## Coverage slice\n")
    t.append("| Requirement / Task | Card ID | Status | Grounding |\n|---|---|---|---|")
    for r in rows:
        status = "covered" if r["match_method"] != "none" else "unmapped (containment %.2f)" % r["best_ratio"]
        card_id = ", ".join(r["matched_task_ids"]) or "none"
        q = r["quote"].replace("|", "\\|")
        t.append(f"| {r['requirement_id']}: {q} | {card_id} | {status} | {r['citation']} |")
    open(f"{out}/reviewer-briefs/reviewer-{n}.md", "w", encoding="utf-8").write("\n".join(t) + "\n")
    print(n, persona, len(rows), "rows,", os.path.getsize(f"{out}/reviewer-briefs/reviewer-{n}.md"), "bytes")

json.dump({f"reviewer-{n}": {"assigned": [f"INF-{i:03d}" for i in ids], "observed": []} for n, (_, ids) in ASSIGN.items()},
          open(f"{out}/artifacts/coverage-assign.json", "w"), indent=1)
print("briefs_materialized: 3")
