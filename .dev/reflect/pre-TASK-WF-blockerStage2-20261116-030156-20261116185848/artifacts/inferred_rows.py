"""Wave 1B.0 Pass 2 helper: quote-pinned INF rows for source.md, verified and matched by containment (rules of refs/coverage-mapping.md)."""
import json
import re
import sys

OUT = ".dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116185848"
SPEC = ".dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md"
PLAN = ".dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md"

ROWS = [
    ("INF-001", 11, "the sweep only records (`promote` off), the classifier has no authority"),
    ("INF-002", 12, "the two `rf-qa.md` cap sites are not touched here (stage 3)"),
    ("INF-003", 13, "Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's kappa, confusion matrix, recall on the panel's blockers, flip rate over three replicates, split by deliverable kind, the count of rows that had each code-supplied input, and the limits."),
    ("INF-004", 14, "Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines"),
    ("INF-005", 14, "Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline, the script's output over the shadow runs that exist so far (zero is a valid and stated result), and the sentence that the owner's go for stage 3 is given in chat and not by this file."),
    ("INF-006", 15, "**Acceptance lines inside this package** that a later task of the same package makes false get an end point."),
    ("INF-007", 19, "No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking."),
    ("INF-008", 19, "Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account."),
    ("INF-009", 27, "Every task that edited `src/superclaude/skills/task/SKILL.md` is dropped (old Task 2 and the task-skill half of old Task 5)."),
    ("INF-010", 28, "Record and print only: one read-only call, no `--promote`, no `--write`, no question."),
    ("INF-011", 29, "tech-research keeps its ledger-writing edit (Task 4); no sweep, no offer, and the halt-offer sentences beside its two cap sentences are dropped because no offer exists in this stage."),
    ("INF-012", 30, "No new plugin surface."),
    ("INF-013", 31, "`follow-ups.md` stays a separate file; no mapping to `review-ledger/1`; `ledger.py` is not edited."),
    ("INF-014", 69, "Task 8's `--confirmed-misses` file now holds `<run_id>:<row id>` entries (split at the last colon), each matched to the ledger whose metadata `run_id` equals its left part; a bare id is rejected, an unmatched entry makes the figure \"not computable\"."),
    ("INF-015", 70, "Task 7 now runs the supplier first (Step A, `stage2-eval-inputs-<set>.json`), builds one input file per set holding the blind-table columns plus the supplier's inputs and the question ids to answer (Step B; still no consensus, grade, label or scale map), and has the agents answer only those ids, every other question recorded UNSET or NA by code (Step C)."),
    ("INF-016", 71, "`follow-ups safety` now prints a last line `worker_status_signal: partial` (the ledger holds a row tagged `protected-risk-dispute`) or `none`; Task 5 adds the mapping and the producer to the WC-4 status-mapping bullet after the existing pinned text, and three tests (text mapping removed fails, safety output over fixtures)."),
    ("INF-017", 72, "Task 4 now edits four active templates (Research Analyst, Research QA, Synthesis QA, Lens-Specific QA), adds one new line under Step 3.1 and one under Step 5.N+1 covering every reviewer of the step, gives analysts a \"Non-blocking findings\" table, and states that the two legacy templates are not edited."),
    ("INF-018", 76, "Task 2 `safety` saves the tag through the stage 1 writer (or the command does when the route only returns rows); a test shows the tag in the ledger after `safety` and after a second `write`."),
    ("INF-019", 78, "Task 3 prints \"No follow-up ledger was written in this run.\" for 0 and the recorded-and-not-filed line only for 1 or more"),
    ("INF-020", 87, "The file needs a `reviewed: <date> by <name>` line; without it (empty file included) the figure is \"not computable\"."),
    ("INF-021", 88, "New Constraints bullet; Task 7 adds `classifier_eval.py` and its test; Task 8's test covers zero runs and zero non-blocking rows."),
    ("INF-022", 89, "`incomplete` is sticky in a ledger; tested in Task 2."),
]

STOP = set("a an the and or but of to in on at by for with from as is are was were be been being this that these those it its into than then so such not no nor per via which who whom whose when where while if else also only each every any all both more most other some own same too very can will just do does did has have had may must shall should would could".split())


def words(s):
    return [w for w in re.findall(r"[a-z0-9_`<>./-]+", s.lower().replace("`", "")) if w not in STOP and len(w) > 1]


spec_lines = open(SPEC, encoding="utf-8").read().split("\n")
plan_text = open(PLAN, encoding="utf-8").read()
# items: Constraints section + each Task section
items = {}
parts = re.split(r"(?m)^(?=## )", plan_text)
for p in parts:
    m = re.match(r"## (Task \d+|Constraints)", p)
    if m:
        items[m.group(1)] = p
item_words = {k: set(words(v)) for k, v in items.items()}

matrix, bad = [], []
for rid, ln, quote in ROWS:
    line = spec_lines[ln - 1]
    ok = quote in line
    if not ok:
        bad.append((rid, ln))
    qw = words(quote)
    uniq = list(dict.fromkeys(qw))
    best = ("none", 0.0)
    for k, ws in item_words.items():
        ratio = sum(1 for w in uniq if w in ws) / max(1, len(uniq))
        if ratio > best[1]:
            best = (k, ratio)
    matched = best[1] >= 0.6
    matrix.append({"id": rid, "source": "inferred", "citation": f"source.md:{ln}", "quote_ok": ok,
                   "best_item": best[0], "ratio": round(best[1], 3),
                   "match_method": "containment" if matched else "none"})
json.dump(matrix, open(f"{OUT}/artifacts/inferred_rows_result.json", "w"), indent=1)
tot = len(matrix)
mt = sum(1 for r in matrix if r["match_method"] != "none")
print(f"quote mismatches: {bad}")
print(f"rows={tot} matched={mt} coverage_pct_union={mt / tot:.4f}")
for r in matrix:
    print(r["id"], r["citation"], r["best_item"], r["ratio"], r["match_method"], "QUOTE_OK" if r["quote_ok"] else "QUOTE_BAD")
sys.exit(1 if bad else 0)
