"""Deterministic coverage matcher for reflect Wave 1B (UC-1).

Pass 1: ID_REGEX outside fenced code. Pass 2 rows are supplied below (quote-pinned);
each quote must be a verbatim substring of its cited source line. Matching for INF rows
is the containment rule: casefolded, stopword-stripped content words, ratio >= 0.6
against a single task's text. Pure string arithmetic.
"""
import json
import re
import sys
from pathlib import Path

SRC, PLAN, OUT = map(Path, sys.argv[1:4])
ID_REGEX = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
STOP = set(
    "a an the and or but nor so yet of in on at to for from by with as into onto over under "
    "is are was were be been being am do does did has have had will would shall should can could "
    "may might must it its this that these those".split()
)

ROWS = [
    (16, "Every subcommand prints one JSON object (`ok`, `exit`, `message`, `review`, plus its own fields); an accepted review whose verdict is FAIL still exits 0"),
    (18, "`ledger.json` (the only state: per review the document hash, hunks, prior findings, accepted check, accepted fix map, attempt counter, deferred list, flags `degraded`, `closed`, `invalid`)"),
    (36, "The diff runs at line level with `difflib.SequenceMatcher(autojunk=False)` and then at token level inside changed blocks; only changed tokens are eligible"),
    (37, 'Minor findings, citation notes and "related defects" cannot own a hunk, so fixing them fails `fixcheck`.'),
    (39, "A second structural failure sets the terminal state `invalid`, which is escalated and never replaced."),
    (40, 'shown once at the end with the reviewer\'s own severity label and the sentence "PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer\'s, unvalidated."'),
    (68, "`src/superclaude/core/HOW-WE-WORK.md`, `WORKER-CONTRACT.md` and the installer are not edited."),
    (70, "with `/sc:spec-panel` renamed to `/sc:spec-panel-diffgate` and only these edits:"),
    (71, 'Frontmatter `name: spec-panel-diffgate`; `description:` gains "with a computed re-review surface (diffgate variant)".'),
    (72, "Usage line 22: replace `[--re-review <prior-findings-file> --baseline <saved-copy>]` with `[--diffgate-dir <dir> [--expect-round N]]`."),
    (73, "keep the bullet as `- **Read**: Specification content analysis and parsing` and delete only its clause that names `src/superclaude/examples/release-spec-template.md`"),
    (74, "bullets 2 and 7 keep 427's text with the small additions shown; bullets 1, 3, 4, 5 and 6 are replaced."),
    (86, "New section `## Diffgate`, between `## Review Loop` and `## Output Formats`, one physical line per item:"),
    (99, "`## Unattended mode` (line 451): byte-identical apart from the command name."),
    (101, "Infrastructure skill, delegate-only, no slash command, frontmatter `name: sc-diffgate`, `allowed-tools: Read, Bash`."),
    (112, "Exit codes: 0 done (includes an accepted review whose verdict is FAIL); 1 input rejected"),
    (125, "Quoted values are JSON strings (`json.loads` on the token)."),
    (127, "`src/superclaude/skills/sc-diffgate/scripts/diffgate.py` (new, about 420 lines, stdlib only)."),
    (149, "Fix-map rules: M1 every hunk is owned by one or more open blocking ids of the review (several ids per hunk allowed); M2 every blocking id has a hunk or a `declined` line"),
    (154, "the flg-r1-shaped fixture (four mapped blocking fixes with four new blockers on them, one MAJOR graded minor on a shared line, one minor-only fix)"),
    (155, "Small synthetic v1, v2, v3 documents and good, bad-anchor, unanchored, structural-failure and degraded reports; the flg-r1-shaped fixture."),
    (156, "an isolated temporary-HOME install of the command and `sc-diffgate` runs `diffgate.py --help` outside the repository and leaves a sentinel `spec-panel.md` byte-unchanged."),
    (157, 'Add `UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}`, compare against `set(UNATTENDED_COMMANDS) | set(UNATTENDED_VARIANTS)`'),
    (158, 'Line 33 becomes `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "spec-panel-diffgate"}`'),
    (160, "must not describe the `fixcheck` retry limit with a digit pattern its `CAP_REGRESSION` matcher catches"),
    (162, "New `docs/designs/spec-panel-diffgate.md`: this SPEC trimmed to decisions, formats, residual risks and the measurement plan."),
    (162, "`make sync-dev` copies the command and the skill folder into `.claude/`, which is never staged; `make verify-sync` must pass."),
    (170, "never `superclaude install --force`, which rewrites every command file, `spec-panel.md` included"),
    (181, "**The one-line substitution in every review brief (reviews 1, 2 and 3):**"),
    (187, "Any `--re-review ... --baseline ...` in a brief is removed (the variant refuses them)."),
    (189, "**The one line the reviser briefs gain (both fix cycles):**"),
    (195, "publishes the exact before and after text of every changed brief line in its run log"),
    (201, "A worker in the experiment's permission mode runs `diffgate.py status` through the installed path with no permission prompt."),
    (204, "CRITICAL or MAJOR labels on (a) findings first raised in review 3, deferred, demoted and over-`via`-cap findings included"),
    (209, "Blindness audit, mandatory for every arm: after the loop, one fresh `/sc:spec-panel --mode critique` review 1 of the final document in a new session with no ledger."),
]


def words(text):
    return {w for w in re.findall(r"[a-z0-9][a-z0-9_.\-]*", text.casefold()) if w not in STOP}


src_lines = SRC.read_text(encoding="utf-8").splitlines()
# Pass 1 (outside fences)
parsed, fence = [], False
for ln in src_lines:
    if ln.lstrip().startswith("```"):
        fence = not fence
        continue
    if not fence:
        parsed += ID_REGEX.findall(ln)

plan = PLAN.read_text(encoding="utf-8")
tasks = {}
for m in re.finditer(r"^## Task (\d+):(.*?)(?=^## |\Z)", plan, re.M | re.S):
    tasks[int(m.group(1))] = m.group(0)

matrix, bad = [], []
for i, (line, quote) in enumerate(ROWS, 1):
    rid = f"INF-{i:03d}"
    if quote not in src_lines[line - 1]:
        bad.append((rid, line))
        continue
    qw = words(quote)
    best = max(((len(qw & words(t)) / len(qw), n) for n, t in tasks.items()), key=lambda x: (x[0], -x[1]))
    ratio, tid = best
    matrix.append({
        "requirement_id": rid, "source": "inferred", "citation": f"source.md:{line}",
        "quote": quote, "best_task": tid, "ratio": round(ratio, 4),
        "matched_task_ids": [tid] if ratio >= 0.6 else [],
        "match_method": "containment" if ratio >= 0.6 else "none",
    })

matched = sum(1 for r in matrix if r["matched_task_ids"])
out = {
    "parsed_ids": sorted(set(parsed)), "parsed_count": len(set(parsed)),
    "inferred_count": len(matrix), "dropped_at_emission": bad,
    "coverage_pct": None if not parsed else None,
    "coverage_pct_union": round(matched / len(matrix), 4) if matrix else None,
    "unmapped_requirements": [], "unmapped_requirements_union": [r["requirement_id"] for r in matrix if not r["matched_task_ids"]],
    "matrix": matrix,
}
OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "matrix"}, indent=2))
