"""Reflect UC-1 Step 1B.0/1B.2b coverage map, deterministic. Run from the repository root:
  uv run --no-project python -I <this file>
Pass 1: ID_REGEX over source.md. Pass 2: INF rows (verbatim quote + line), validated here as substrings of the cited line.
Matching: parsed rows exact ID in tasklist; INF rows containment >= 0.6 of content words in ONE task item (protocol rule);
a second, informational column also tests the Constraints section (not a task item, not used for coverage_pct_union)."""
import json
import re
from pathlib import Path

PKG = Path(".dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852")
OUT = Path(".dev/reflect/pre-TASK-WF-stage1Request-20261116-221852-20261116222131/artifacts")
src_lines = (PKG / "source.md").read_text().splitlines()
plan = (PKG / "TASK-WF-stage1Request-20261116-221852.md").read_text()

ID_REGEX = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
STOP = set("""a an the and or but if then of to in on at by for with from as is are was were be been being it its this that these those
into onto over under per via not no nor so than too very can could should would may might must shall will do does did has have had
which who whom what when where while also only each every any all both either neither such""".split())


def words(s):
    return {w for w in re.findall(r"[a-z0-9_./`<>-]+", s.casefold()) if w not in STOP and len(w) > 1}


# Pass 1
parsed = {}
for n, ln in enumerate(src_lines, 1):
    for m in ID_REGEX.findall(ln):
        parsed.setdefault(m, n)

# Pass 2 rows: (id, line, verbatim quote)
INF = [
    ("INF-001", 61, "`src/superclaude/cli/review/safety_route.py` (GR1 vocabulary in one list, GR12 raise-only rule), `src/superclaude/cli/review/safety_cmd.py`, the subcommand `superclaude review safety-scan <file>` registered in the tuple of `src/superclaude/cli/review/__init__.py`, and the tests `tests/review/test_review_safety_route.py` and `tests/review/test_review_safety_cmd.py`."),
    ("INF-002", 61, "It takes plain row text, imports no codec and no classifier, reports unreadable or missing input as such (exit 2, never a hit count), and stores no tag."),
    ("INF-003", 62, "prints every non-superseded minor line of every task's notes file, runs `superclaude review safety-scan` over each notes file, prints \"no notes file for T<id>\" for a missing file, asks nothing, changes no verdict or archive outcome;"),
    ("INF-004", 62, "Paragraph \"Follow-up print (record and print only).\" in `SKILL.md` (\"Done\") and `refs/managed-workspace.md` (after the closing fence of the `FINAL:` block, before step 6);"),
    ("INF-005", 62, "both files copied byte for byte to the plugin twin (pinned by `test_h_implement_protocol_plugin_twins_byte_equal`); `refs/qa.md` unedited (SHA-256 recorded at the task start); active-flow smoke check recorded in `./artifacts/print-smoke.txt`."),
    ("INF-006", 63, "C1 (classifier, its inputs supplier and its command: Tasks 5, 9, 10, 11 and 12), C2 (follow-up ledger codec, filing logic and the ledger reference: Tasks 4, 7 and 8), C4 (skill folder, rule, scale map, registry, install check and registry drift tests: Tasks 1, 2, 3, 6, 14 and 15), C10 (the owner summary: Task 16)."),
    ("INF-007", 63, "One Constraints bullet states that these are not built."),
    ("INF-008", 64, "Its seven other tasks are cut (rows C2 and C7); its ledger row and request file are marked withdrawn by the main session."),
    ("INF-009", 65, "Two tasks fit `depth: quick` (2 to 4 phases, one task per phase)."),
    ("INF-010", 66, "command `superclaude review safety-scan <file>` (option `--unattended`); files `src/superclaude/cli/review/safety_route.py`, `src/superclaude/cli/review/safety_cmd.py`, `tests/review/test_review_safety_route.py`, `tests/review/test_review_safety_cmd.py`; paragraph title \"Follow-up print (record and print only).\"; artifacts `./artifacts/qa-md-sha256-before.txt` and `./artifacts/print-smoke.txt`; no stored tag `protected-risk-dispute`."),
    ("INF-011", 67, "The Constraints now name `src/superclaude/cli/review/__init__.py` as the third existing file the package edits (Task 1 registers `safety_cmd`)."),
    ("INF-012", 22, "Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account."),
    ("INF-013", 22, "No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task."),
    ("INF-014", 7, "Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier facts (M, C and E run only with code-supplied inputs; the \"M or C is Y gives BLOCKING\" row is never enabled; confidence is an ordinal band), pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only."),
    ("INF-015", 18, "Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass counts), the list of files created, a statement that no carrier was edited (`git diff --stat` over carriers is empty), the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file."),
]
bad = [i for i, ln, q in INF if q not in src_lines[ln - 1]]
assert not bad, f"quote not found on cited line: {bad}"

# Task items and Constraints section of the plan
tasks = {}
for m in re.finditer(r"^## Task (\d+):.*?(?=^## |\Z)", plan, re.S | re.M):
    tasks[f"T{m.group(1)}"] = m.group(0)
constraints = re.search(r"^## Constraints.*?(?=^## )", plan, re.S | re.M).group(0)

rows = []
for pid, ln in parsed.items():
    hit = [t for t, txt in tasks.items() if re.search(rf"\b{re.escape(pid)}\b", txt)]
    rows.append(dict(id=pid, source="parsed", line=ln, matched=hit, method="exact" if hit else "none"))
for iid, ln, q in INF:
    w = words(q)
    best, ratio = None, 0.0
    for t, txt in tasks.items():
        r = len(w & words(txt)) / len(w)
        if r > ratio:
            best, ratio = t, r
    c = len(w & words(constraints)) / len(w)
    ok = ratio >= 0.6
    rows.append(dict(id=iid, source="inferred", line=ln, matched=[best] if ok else [], method="containment" if ok else "none",
                     best_task_ratio=round(ratio, 3), constraints_ratio=round(c, 3), quote=q))

P = [r for r in rows if r["source"] == "parsed"]
I = [r for r in rows if r["source"] == "inferred"]
pm = sum(1 for r in P if r["matched"])
im = sum(1 for r in I if r["matched"])
res = dict(
    parsed_count=len(P), inferred_count=len(I),
    coverage_pct=round(pm / len(P), 4) if P else None,
    coverage_pct_union=round((pm + im) / (len(P) + len(I)), 4),
    unmapped_requirements=[r["id"] for r in P if not r["matched"]],
    unmapped_requirements_union=[r["id"] for r in rows if not r["matched"]],
    coverage_degraded="parsed-sparse" if len(I) > len(P) else None,
    S_scope=len(tasks),
    S_dev_density=round(sum(1 for r in rows if not r["matched"]) / len(rows), 4),
    matrix=rows,
)
(OUT / "coverage-matrix.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
print({k: v for k, v in res.items() if k != "matrix"})
for r in rows:
    print(r["id"], r["source"], r["method"], r["matched"], r.get("best_task_ratio", ""), r.get("constraints_ratio", ""))
