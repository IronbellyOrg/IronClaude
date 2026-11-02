"""Build .dev/review-severity-rule/site-sweep.md: every sweep hit with its plan task or its not-a-rule reason.

Usage (repo root, before any src edit): uv run python -I .dev/review-severity-rule/sweep/build_site_sweep.py
Inputs: sweep/patterns.tsv, sweep/hits.tsv (run_sweep.sh), sweep/fixloop-hits.tsv (fixloop_scan.py --tsv),
sweep/coverage.tsv (classify_covered.py), cap-edits.yaml, sweep-edits.yaml.
Exits 1 if any hit has no disposition.
"""
import pathlib
import re
import sys

import yaml

R = pathlib.Path(".dev/review-severity-rule")
S = R / "sweep"

CAP_GROUP_TASK = {"agents": 12, "templates": 13, "skills-a": 14, "skills-b": 15, "portify": 16, "prd-core": 17}
INV_FILE_TASK = [  # (path fragment, task) for inventory-covered lines
    ("output-styles/pragmatic.md", 1), ("agents/rf-qa.md", 2), ("agents/rf-qa-qualitative.md", 3),
    ("agents/rf-analyst.md", 3), ("templates/documents/", 4), ("templates/modularization-template-review/", 4),
    ("templates/workflow/", 5), ("agents/rf-team-lead.md", 6), ("skills/prd/", 7), ("skills/tdd/", 7),
    ("cli/prd/", 7), ("skills/tech-reference/", 8), ("skills/tech-research/", 8), ("skills/readme/", 9),
    ("skills/operational-guide/", 9), ("skills/task/", 10), ("skills/task-builder/", 10), ("rules/prompts/", 11),
    ("skills/sc-implement-protocol/", 18),
]
# Explicit dispositions (file:line -> text) for hits that are not rules of this kind, or are covered by a task
# whose site list the premap could not parse.
EXPLICIT = {
    "src/superclaude/cli/prd/prompts.py:1173": "Task 7 (inventory 2.4: prd CLI prompt FAIL line)",
    "src/superclaude/cli/prd/prompts.py:1175": "not a rule: closing line 'if you can't verify it, it fails'; an unverifiable claim is a blocking finding under S1",
    "src/superclaude/skills/task-builder/SKILL.md:869": "Task 10 (inventory 2.4: task-builder 869-870 gap list)",
    "src/superclaude/agents/rf-team-lead.md:462": "Task 6 (pinned Fix Cycles line: blocking-only FIX trigger, max 2 cycles)",
    "agents/sc-self-review.md:31": "not a rule: advice to recommend targeted actions; no verdict and no fix loop",
    "agents/self-review.md:35": "not a rule: advice to recommend targeted actions; no verdict and no fix loop",
    "plugins/superclaude/agents/self-review.md:35": "not a rule: advice to recommend targeted actions; no verdict and no fix loop",
    "src/superclaude/agents/self-review.md:35": "not a rule: advice to recommend targeted actions; no verdict and no fix loop",
    "src/superclaude/cli/roadmap/executor.py:2949": "not a rule: user-facing hint printed after a failed run",
    "src/superclaude/skills/operational-guide/SKILL.md:540": "not a rule of this kind: already HALTs at the cap and presents the remaining issues to the user (cap number is Task 14)",
    "src/superclaude/agents/rf-qa-qualitative.md:690": "not a rule: check item about the reviewed task's own Open Questions section, not an at-cap rule",
    "src/superclaude/agents/rf-qa.md:336": "not a rule: check item about the reviewed task's own Open Questions section, not an at-cap rule",
    "src/superclaude/skills/operational-guide/SKILL.md:1025": "not a rule: content requirement for the generated guide (stale-doc findings appear in the guide)",
    "src/superclaude/skills/operational-guide/SKILL.md:1573": "not a rule: content requirement for the generated guide (stale-doc findings appear in the guide)",
    "src/superclaude/skills/roadmap/SKILL.md:555": "not a rule of this kind: generation-time obligation scan; violations are recorded in the roadmap with a blocking annotation, not passed by a review loop",
    "src/superclaude/templates/documents/skill_template.md:323": "not a rule: unresolved requirement ambiguities become the task's Open Questions; not review findings",
    "src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:204": "not a rule of this kind: manifest schema-validation retry loop, not a review loop (allowlisted in Task 20(f))",
    "src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md:50": "not a rule of this kind: manifest schema-validation retry loop, not a review loop (allowlisted in Task 20(f))",
    "src/superclaude/rules/core/anti_hallucination_task_completion_rules.md:81": "not a rule of this kind: closes the 'Penalty for Forgery' rule (fabricated sources); fabrication is a blocking defect",
    "src/superclaude/rules/core/anti_sycophancy.md:81": "not a rule of this kind: closes the 'Penalty for Forgery' rule (fabricated sources); fabrication is a blocking defect",
    "agents/sc-pm-agent.md:541": "not a rule: example output in documentation ('Adds prevention checklist if issues found'); allowlisted in Task 20(i)",
    "src/superclaude/agents/pm-agent.md:564": "not a rule: example output in documentation ('Adds prevention checklist if issues found'); allowlisted in Task 20(i)",
    "plugins/superclaude/agents/pm-agent.md:564": "not a rule: example output in documentation ('Adds prevention checklist if issues found'); allowlisted in Task 20(i)",
}
ZERO_TOLERANCE_REASONS = [  # (regex on the hit text, reason) for "zero tolerance" hits that stay
    (r"fabricat|forger", "not a rule of this kind: zero tolerance for fabrication or forgery; fabrication is a blocking defect"),
    (r"hallucinat", "not a rule of this kind: anti-hallucination rule; a hallucinated claim is a blocking defect"),
    (r"can.t verify it", "not a rule of this kind: an unverifiable claim is a blocking finding under S1 (closing line of the shared prompt block)"),
    (r"incremental writing", "not a rule: incremental-writing process rule for output files, not a review verdict"),
    (r"dismissal", "not a rule: rule against dismissing errors, not a verdict rule"),
    (r"verification (policy|standards)|accuracy policy", "not a rule of this kind: claims must be verified; an unverified claim is blocking"),
    (r"closing line is VERBATIM", "not a rule: template comment about the shared closing line"),
]
P14_DESCRIPTIVE = ("not a rule of this kind: names the fix-agent step (encoding note, lint check, or a pointer to the M3/I20 "
                   "protocol) without setting which findings it receives; the I20 and M3 steps that set the scope are Task 19 rows")


def inv_task(file: str) -> str:
    for frag, task in INV_FILE_TASK:
        if frag in file:
            return f"Task {task}"
    return "Task ?"


cover = {}
for ln in (S / "coverage.tsv").read_text().splitlines():
    k, v = ln.split("\t")
    cover[k] = v
cap_group = {r["id"]: r["group"] for r in yaml.safe_load((R / "cap-edits.yaml").read_text())["rows"]}
sweep_rows = {}
for r in yaml.safe_load((R / "sweep-edits.yaml").read_text())["rows"]:
    lines = r.get("lines") or [r.get("line")]
    nums = []
    for x in lines:
        nums += [int(x)] if isinstance(x, int) else [n for p in re.findall(r"\d+(?:-\d+)?", str(x))
                                                       for n in range(int(p.split("-")[0]), int(p.split("-")[-1]) + 1)]
    for n in nums:
        sweep_rows.setdefault(f"{r['file']}:{n}", []).append(f"{r['id']} ({r.get('finding', '')})")


def disposition(pid: str, key: str, text: str) -> str:
    if key in sweep_rows:
        return "Task 19, sweep-edits " + ", ".join(sweep_rows[key])
    if key in EXPLICIT:
        return EXPLICIT[key]
    c = cover.get(key)
    if c and c.startswith("cap-edits"):
        rid = c.split()[1]
        return f"Task {CAP_GROUP_TASK[cap_group[rid]]}, cap-edits {rid}"
    if c:
        return f"{inv_task(key)}, {c}"
    if pid == "P08":
        for rx, reason in ZERO_TOLERANCE_REASONS:
            if re.search(rx, text, re.IGNORECASE):
                return reason
    if pid == "P14":
        return P14_DESCRIPTIVE
    return ""


rows, missing = [], []
patterns = [ln.split("\t", 1) for ln in (S / "patterns.tsv").read_text().splitlines()]
for raw in (S / "hits.tsv").read_text().splitlines():
    pid, rest = raw.split("\t", 1)
    file, line, text = rest.split(":", 2)
    d = disposition(pid, f"{file}:{line}", text)
    rows.append((pid, f"{file}:{line}", text.strip(), d))
    if not d:
        missing.append(f"{pid} {file}:{line}")
fix_rows = []
for raw in (S / "fixloop-hits.tsv").read_text().splitlines():
    ids, key, text = raw.split("\t", 2)
    d = disposition("FIX", key, text)
    fix_rows.append((ids, key, text.strip(), d))
    if not d:
        missing.append(f"{ids} {key}")

esc = lambda s: s.replace("|", "\\|").replace("\n", " ")[:160]
out = [
    "# Site sweep: every wording of the old review rule",
    "",
    "Date 2026-11-02, HEAD f90877be, before any source edit. Required by the user decision of 2026-11-02 08:41 UTC",
    "(coordinator message msg_9d0fe67f82c7). Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-053741/`.",
    "",
    "## Search 1: fixed pattern list",
    "",
    "Command (repo root): for each row of `sweep/patterns.tsv`,",
    "`git grep -n -I -i -E \"<pattern>\" -- src plugins commands agents skills` (root `commands/`, `agents/`, `skills/` are the",
    "root twins; templates live under `src/superclaude/templates` and `plugins/superclaude/templates`). Raw output: `sweep/hits.tsv`.",
    "",
    "| id | pattern |",
    "|---|---|",
    *[f"| {p} | `{esc(x)}` |" for p, x in patterns],
    "",
    "## Search 2: fix-loop scope",
    "",
    "Command: `uv run python -I .dev/review-severity-rule/sweep/fixloop_scan.py --tsv` (patterns F1-F5 in that file; same",
    "patterns as `FIX_LOOP_PATTERNS` in the Task 20 test). Raw output: `sweep/fixloop-hits.tsv`.",
    "",
    "## Dispositions",
    "",
    f"Search 1: {len(rows)} hits; search 2: {len(fix_rows)} lines; hits without a disposition: {len(missing)}.",
    "A disposition is a plan task (with its cap-edits, inventory or sweep-edits row) or the reason the line is not a rule",
    "that fails on minor findings, rechecks or fixes them, passes open blocking findings, or caps a review loop above 2.",
    "",
    "### Search 1 hits",
    "",
    "| pattern | site | text | disposition |",
    "|---|---|---|---|",
    *[f"| {p} | `{k}` | {esc(t)} | {esc(d)} |" for p, k, t, d in rows],
    "",
    "### Search 2 lines",
    "",
    "| patterns | site | text | disposition |",
    "|---|---|---|---|",
    *[f"| {p} | `{k}` | {esc(t)} | {esc(d)} |" for p, k, t, d in fix_rows],
    "",
]
(R / "site-sweep.md").write_text("\n".join(out))
print(f"{len(rows)} search-1 hits, {len(fix_rows)} search-2 lines, {len(missing)} without disposition")
for m in missing:
    print("MISSING", m)
sys.exit(1 if missing else 0)
