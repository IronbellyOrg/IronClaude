"""Deterministic UC-1 coverage computation (Step 1B.0 Pass 1 + Pass 2 rows, containment matching).

Usage: uv run python coverage_calc.py <spec.md> <tasklist.md> <out_dir>
Pass 1 regex finds zero labeled IDs in this spec (see pass1-ids.txt). Pass 2 rows below are
quote-pinned: a row whose quote is not a substring of its cited line is dropped at emission.
"""
import json
import re
import sys

spec_path, task_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
spec = open(spec_path, encoding="utf-8").read().split("\n")
task_text = open(task_path, encoding="utf-8").read().split("\n")

ID_REGEX = re.compile(r"\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b")
in_fence = False
parsed = []
for i, ln in enumerate(spec, 1):
    if ln.strip().startswith("```"):
        in_fence = not in_fence
        continue
    if not in_fence:
        for m in ID_REGEX.findall(ln):
            parsed.append((m, i))

# (spec line, verbatim quote) -- Pass 2 inference rows
ROWS = [
    (6, "default on at `--monitor 3` via `--merge-guard {draft,off}`"),
    (6, "release when the fix push is confirmed on the PR head, before replies and the re-trigger"),
    (6, "an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports"),
    (51, "No new `MonitorState`."),
    (75, "No `gh` or `git` word on any line, comments included (F6)."),
    (112, "maps, first match wins"),
    (118, "observed = read.transitions - guard.baseline"),
    (140, "`HALT_UNAVAILABLE(timeline_unreadable)`"),
    (156, "`push_completed` and `read.head_sha == target_sha`"),
    (166, "re-enter `release_decision` with `push_completed=True`"),
    (175, "Add to `EventType` in `models.py` (43 to 45"),
    (184, "`idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>`"),
    (201, "the whole record is erased (the fold returns `None`"),
    (208, "`original_is_draft` is never read from GitHub after the first record"),
    (214, "`DEFAULT_MERGE_GUARD = \"draft\"`"),
    (216, "Effective only at `--monitor 3`; accepted and inert below."),
    (221, "Modelled on `scripts/retrigger-review.sh`"),
    (230, "`gh api --paginate \"repos/${REPO}/issues/${PR}/timeline\"`"),
    (234, "Exit codes: 0 success; 1 `gh` failure or failed verification"),
    (240, "Loaded lazily at L3 Wave 3, Wave 6 and Wave 8."),
    (241, "No new python fence"),
    (242, "update it to 45 and name `draft_guard_requested` and `draft_guard_settled`"),
    (247, "PR #N is still mergeable; this run's fixes are local only."),
    (251, "`fix_cycle_id` gives guard-enabled cycles an explicit id"),
    (255, "needs one entry in `WRITE_VERB_CLASSIFICATION`"),
    (270, "Acceptance trace (must appear in this order in the run log)"),
    (301, "Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/`"),
    (301, "the final task runs the FULL suite"),
    (322, "protocol assertions that the Wave 0 bullet names `--resume`, is not gated on L3 or `draft`"),
    (326, "No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`)."),
    (362, "Cite tests and constants by symbol name"),
    (363, "Declare dependencies completely, one `Depends on:` line per dependency"),
    (377, "scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions"),
    (244, "`--merge-guard {draft,off}` in the argument-hint and the Options table"),
    (245, "Flag row and a paragraph"),
    (289, "export the public guard names"),
]

STOP = set("""a an the and or but nor of to in on at by for with from as is are was were be been being it its this that
these those which who whom whose will would shall should can could may might must do does did has have had not no
than then there their they them we you your i if so such into onto per via up out any all each every one only also
both either neither about over under after before between through while when where what""".split())


def content_words(s):
    return {w for w in re.findall(r"[a-z0-9_]+", s.casefold()) if w not in STOP and len(w) > 1}


# task items: each "## Task N" block + the Constraints block
items = []
cur = None
for ln in task_text:
    m = re.match(r"^## (Task \d+|Constraints)\b", ln)
    if m:
        cur = [m.group(1), []]
        items.append(cur)
    elif ln.startswith("## "):
        cur = None
    elif cur is not None:
        cur[1].append(ln)
items = [(n, "\n".join(b)) for n, b in items]

rows, dropped = [], []
for k, (ln, q) in enumerate(ROWS, 1):
    rid = f"INF-{k:03d}"
    if q not in spec[ln - 1]:
        dropped.append({"id": rid, "line": ln, "quote": q, "reason": "quote not in cited line"})
        continue
    w = content_words(q)
    best = None
    for name, body in items:
        r = len(w & content_words(body)) / len(w) if w else 0.0
        if best is None or r > best[1]:
            best = (name, r)
    matched = best[1] >= 0.6
    rows.append({
        "requirement_id": rid, "source": "inferred", "quote": q,
        "citation": f"source.md:{ln}",
        "matched_task_ids": [best[0]] if matched else [],
        "match_method": "containment" if matched else "none",
        "best_ratio": round(best[1], 4),
    })

parsed_total = len({p[0] for p in parsed})
total = parsed_total + len(rows)
matched_n = sum(1 for r in rows if r["match_method"] != "none")
union = round(matched_n / total, 4) if total else None
unm = [r["requirement_id"] for r in rows if r["match_method"] == "none"]
res = {
    "parsed_count": parsed_total, "inferred_count": len(rows), "inferred_dropped_at_emission": dropped,
    "coverage_pct": None if parsed_total == 0 else 1.0,
    "coverage_pct_union": union, "unmapped_requirements": [],
    "unmapped_requirements_union": unm,
    "coverage_degraded": "parsed-sparse" if len(rows) > parsed_total else None,
    "S_dev_density": round(len(unm) / total, 4) if total else None,
    "task_items": [n for n, _ in items],
    "matrix": rows,
}
json.dump(res, open(f"{out}/coverage-matrix.json", "w"), indent=1)
open(f"{out}/pass1-ids.txt", "w").write(f"parsed ID hits outside fences: {len(parsed)}\n")
with open(f"{out}/pass2-rows.txt", "w") as fh:
    for r in rows:
        fh.write(f"{r['requirement_id']} | {r['citation']} | {r['match_method']} {r['matched_task_ids']} {r['best_ratio']} | {r['quote']}\n")
print(json.dumps({k: v for k, v in res.items() if k != "matrix"}, indent=1))
