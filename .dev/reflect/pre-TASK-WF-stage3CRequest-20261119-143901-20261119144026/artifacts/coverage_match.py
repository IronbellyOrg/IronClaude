"""Wave 1B coverage matcher (coverage-mapping.md, D13 containment rule).

Deterministic: the INF rows below are fixed (Pass 2 output), each quote is
checked to be a substring of the cited spec line, and each row is matched to
the single best plan unit by case-folded, stopword-stripped content-word
containment (threshold 0.6, ties -> first unit in plan order).

Run: uv run python coverage_match.py   (from this artifacts folder or anywhere)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = Path(
    "/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/"
    ".dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901"
)
SPEC = PKG / "source.md"
PLAN = PKG / "TASK-WF-stage3CRequest-20261119-143901.md"

# Fixed stopword set: articles, conjunctions, prepositions, auxiliaries.
STOPWORDS = frozenset(
    """
    a an the
    and or but nor so yet if then than that whether
    of in on at to for from by with into onto about after before over under
    between through during without within upon via per as up down out off
    is are was were be been being am do does did done has have had having
    will would shall should can could may might must
    """.split()
)

THRESHOLD = 0.6

# (id, spec line, verbatim quote <= 2 sentences)
INF_ROWS = [
    ("INF-001", 3, "Run it on a fresh branch made from `origin/master`."),
    ("INF-002", 3, "Do NOT run `/sc:implement` on the package until the owner says go in chat."),
    ("INF-003", 20, "The stage 3b package `TASK-WF-stage3BRequest-20261117-172514` is in the done subfolder of the repository task folder, and PR #605 is merged."),
    ("INF-004", 20, "There is no owner gate inside this package. The owner's go to run it is a separate chat message recorded in the stage ledger `stage-requests/README.md`."),
    ("INF-005", 24, "Task 1: edit `src/superclaude/agents/reflect-reviewer.md`. Re-read the place by its text first."),
    ("INF-006", 24, 'One edit only: in the bullet that begins "- The Severity column of the Deviations table (HIGH, MEDIUM, LOW) is a label, not the grade.", insert the passage below directly after the sentence "A deviation that meets a blocking condition is Blocking whatever its label says; a HIGH that is only wording is a Note." and before the sentence that begins "When no consumer can be established".'),
    ("INF-007", 24, "Keep one space between sentences."),
    ("INF-008", 24, "Copy the passage from the fenced block below; do not retype it. It is byte-identical to the measured text (source file `.dev/stage3c-variants/brainstorm/reflect-reviewer.md`, sha256 `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8`, in the stage 0 to 3 worktree)."),
    ("INF-009", 27, 'Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids, or pass a named acceptance check while a behaviour the spec states is absent or wrong (for example a missing message prefix, or a missing "no output written" rule). If so, correcting it changes a required behaviour or acceptance check: grade it `Blocking (Decision):` or `Blocking (Missing):`, not `Medium:`.'),
    ("INF-010", 30, 'In `tests/skills/test_review_severity_rule.py`, add two needles to the tuple in `test_c_reflect_reviewer_grade_bullets_pinned`: `"Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids"` and `"A behaviour that would happen anyway (for example exit 0 on success) is not that."`. Make each needle a Python string that holds the exact text, backticks included.'),
    ("INF-011", 32, 'Do not change the frontmatter, the Behavioral Mindset, the Boundaries list, the Correctness gaps section, the columns of the Deviations table, the S1, S2 and S3 bullets, the cap bullet, or the bullet that begins "- This grading applies".'),
    ("INF-012", 34, 'Before editing, run `git grep -n "reflect-reviewer" -- tests src` and write its output to `./artifacts/stage3c-task1-notes.md`, with one sentence on which tests read the agent file.'),
    ("INF-013", 34, "After the edit, run every test file that output names once and record each result in the same file."),
    ("INF-014", 39, '`grep -c "Before you write \\`Medium:\\`" src/superclaude/agents/reflect-reviewer.md` prints 1.'),
    ("INF-015", 40, '`grep -c "A behaviour that would happen anyway (for example exit 0 on success) is not that." src/superclaude/agents/reflect-reviewer.md` prints 1.'),
    ("INF-016", 41, '`grep -c "a HIGH that is only wording is a Note. Before you write" src/superclaude/agents/reflect-reviewer.md` prints 1.'),
    ("INF-017", 42, "`git diff -- src/superclaude/agents/reflect-reviewer.md` shows exactly one changed line, the Severity column bullet. The removed and added versions of that line differ only by the inserted passage plus one space."),
    ("INF-018", 43, "`uv run pytest tests/skills/test_review_severity_rule.py -v` passes with the two new needles."),
    ("INF-019", 44, "`uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes."),
    ("INF-020", 46, "the `git grep` output and its one sentence;"),
    ("INF-021", 47, "the results of the other test files that output names;"),
    ("INF-022", 48, "one line saying the reflect skill (`skills/sc-reflect-protocol`) and the adversarial merge were not edited."),
    ("INF-023", 50, "Task 2: run `make sync-dev` and `make verify-sync`, then run the four test files above once more after the last edit."),
    ("INF-024", 50, "Write the pass counts and the `make verify-sync` result to `./artifacts/stage3c-final-run.md`."),
    ("INF-025", 50, "Check that nothing under the project `.claude/` folder other than `.claude/settings.json` is staged."),
    ("INF-026", 54, "`make verify-sync` passes."),
    ("INF-027", 55, "The four test files pass."),
    ("INF-028", 56, "`./artifacts/stage3c-final-run.md` exists."),
    ("INF-029", 60, "That merge step is the reflect protocol's and the adversarial skill's, outside this file. No edit to `skills/sc-reflect-protocol`, the adversarial skill, or the merge text."),
    ("INF-030", 61, "That is a detection problem, not a grading one, and is not addressed here."),
    ("INF-031", 62, "No edit to the S1 to S3 bullets, `evidence-validator.md`, `sc-implement-protocol/refs/qa.md`, the own-scale primitives or `src/superclaude/cli/**/*.py`. No plugin surface."),
    ("INF-032", 62, "No new question in any command. No Jev call."),
    ("INF-033", 63, "The re-runs are not a task here."),
    ("INF-034", 65, "Known limits to carry into the plan's summary"),
    ("INF-035", 67, "The passage names two kinds of finding from spec E (\"a missing message prefix\", \"a missing 'no output written' rule\") as examples. It was measured with them, so they stay."),
    ("INF-036", 67, "Its held-out result on spec B does not depend on them."),
    ("INF-037", 68, "The measurement was small: one reviewer model (sonnet), three reviewers per arm, one scorer and no second reader. The briefs carried first-pass coverage hints for every arm."),
    ("INF-038", 69, 'Whether dropping "plain codepoint order" is a real blocker is a judgment: it changes the order of digits and apostrophes, not of lowercase letters.'),
    ("INF-039", 73, "`src/superclaude/` is the source of truth: edit there, then run `make sync-dev`."),
    ("INF-040", 74, "Stage nothing under the project `.claude/` folder; only `.claude/settings.json` is tracked."),
    ("INF-041", 75, "Python work uses UV only (`uv run pytest ...`)."),
    ("INF-042", 76, "`.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included. Staging is not committing."),
    ("INF-043", 77, "Acceptance checks are by content and quote the sentence they protect. Line numbers in a task body are hints; re-read each place by its text."),
]

# Plan units in plan order: (id, first line, last line), 1-based inclusive.
PLAN_UNITS = [
    ("Constraints", 17, 27),
    ("Task 1", 31, 48),
    ("Task 2", 52, 61),
]


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.casefold()) if w not in STOPWORDS}


def main() -> None:
    spec_lines = SPEC.read_text(encoding="utf-8").splitlines()
    plan_lines = PLAN.read_text(encoding="utf-8").splitlines()
    units = [
        (uid, a, b, content_words("\n".join(plan_lines[a - 1 : b])))
        for uid, a, b in PLAN_UNITS
    ]

    rows, dropped = [], []
    for rid, line, quote in INF_ROWS:
        if quote not in spec_lines[line - 1]:
            dropped.append(rid)  # quote not verbatim on cited line -> dropped
            continue
        words = content_words(quote)
        best_uid, best_ratio = None, -1.0
        for uid, _a, _b, uw in units:  # plan order; strict > keeps first on ties
            ratio = len(words & uw) / len(words) if words else 0.0
            if ratio > best_ratio:
                best_uid, best_ratio = uid, ratio
        matched = best_ratio >= THRESHOLD
        rows.append(
            {
                "requirement_id": rid,
                "quote": quote,
                "citation": f"source.md:{line}",
                "matched_task_ids": [best_uid] if matched else [],
                "match_method": "containment" if matched else "none",
                "ratio": round(best_ratio, 4),
                "best_unit": best_uid,
                "source": "inferred",
            }
        )

    total = len(rows)
    matched_n = sum(1 for r in rows if r["match_method"] != "none")
    unmapped = [r["requirement_id"] for r in rows if r["match_method"] == "none"]
    summary = {
        "parsed_count": 0,
        "inferred_count": total,
        "dropped_rows": dropped,
        "matched_count": matched_n,
        "total_count": total,
        "coverage_pct": None,
        "coverage_pct_union": round(matched_n / total, 4) if total else None,
        "unmapped_requirements": [],
        "unmapped_requirements_union": unmapped,
        "missing_implementations_count": 0,
        "S_dev_density": round(min(1.0, max(0.0, len(unmapped) / total)), 4) if total else None,
        "coverage_degraded": "parsed-sparse" if total > 0 else None,
        "threshold": THRESHOLD,
        "plan_units": [{"id": u, "lines": f"{a}-{b}"} for u, a, b in PLAN_UNITS],
    }
    (HERE / "coverage-matrix.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    for r in rows:
        print(f"{r['requirement_id']} {r['match_method']:<11} {r['ratio']:.4f} {r['best_unit']}")


if __name__ == "__main__":
    main()
