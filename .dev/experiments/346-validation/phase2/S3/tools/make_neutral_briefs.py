"""Derive the RECONSTRUCTED neutral reviser briefs for the live-loop mode from the
verbatim briefs by removing only the orchestrator's finding-specific STEERING.

Usage: uv run python -I make_neutral_briefs.py <briefs_dir>
Writes RECONSTRUCTED-*.md next to the verbatim files and prints what was cut.
"""
import sys
from pathlib import Path

B = Path(sys.argv[1])
NEUTRAL = (
    "STEERING: none supplied (RECONSTRUCTED: the original steering named findings of the original reviews). "
    "Resolve every blocking finding of the latest review using that review's own replacement text where it "
    "exists. The governing criterion is the owner's: maximum effect with the fewest edge cases and unwanted "
    "blocks. Prefer ONE general mechanism over a growing list of evasion cases. Keep change numbering stable "
    "where possible and update every place that states a changed rule (decision table, message table, probe "
    "disposition rows, acceptance map, owner decisions, residual list, test plan) so that no two places state "
    "different values.\n\n"
)


def cut(text, start, end, repl):
    i, j = text.index(start), text.index(end)
    assert i < j and text.count(start) == 1 and text.count(end) == 1
    return text[:i] + repl + text[j:], text[i:j]


# fix cycle 1 reviser
t = (B / "R1-reviser-fix-cycle-1-L947.md").read_text(encoding="utf-8")
t = t.replace("Use the reviewer's exact replacement text where it exists, EXCEPT where this brief steers otherwise.",
              "Use the reviewer's exact replacement text where it exists.", 1)
assert "(the review: B-1..B-8 blocking, 14 minor, with replacement text)" in t
t = t.replace("(the review: B-1..B-8 blocking, 14 minor, with replacement text)",
              "(the review: its blocking findings and minor findings, with replacement text)", 1)
t, cut1 = cut(t, "STEERING (decided by the orchestrator, follow it):", "OUTPUT: edit refactor-plan.md;", NEUTRAL)
t = t.replace("listing each of B-1..B-8 with the change number(s) edited. Final reply: the plan path, then one line per blocking finding: B-n fixed / not fixed.",
              "listing each blocking finding of the review with the change number(s) edited. Final reply: the plan path, then one line per blocking finding: B-n fixed / not fixed.", 1)
(B / "RECONSTRUCTED-R1-reviser-fix-cycle-1-neutral.md").write_text(t, encoding="utf-8")

# fix cycle 2 reviser
t = (B / "R2-reviser-fix-cycle-2-L1000.md").read_text(encoding="utf-8")
t = t.replace("to resolve the blocking findings F-1..F-8 of the second independent review", "to resolve the blocking findings of the second independent review", 1)
t = t.replace("READ plan-review-2.md (F-1..F-8 with attack evidence and replacement text, m-1..m-12), plan-review.md (earlier B-1..B-8 attacks), and refactor-plan.md fully.",
              "READ plan-review-2.md (its blocking findings with attack evidence and replacement text, and its minor findings), plan-review.md (earlier attacks), and refactor-plan.md fully.", 1)
t, cut2 = cut(t, "The pattern of both reviews:", "OUTPUT: edit refactor-plan.md;", NEUTRAL)
t = t.replace("listing F-1..F-8 with the changes edited and the prototype result summary. Final reply: the plan path, then one line per F-n: fixed / not fixed, and the count of attacks that still leak in your prototype (it must be zero or listed).",
              "listing each blocking finding of the second review with the changes edited and the prototype result summary. Final reply: the plan path, then one line per blocking finding: fixed / not fixed, and the count of attacks that still leak in your prototype (it must be zero or listed). Before finishing, write a throwaway bash prototype of the classifier in a temp dir under /tmp (never in the repository; delete it at the end), run ALL attack strings from plan-review.md and plan-review-2.md and 15 benign commands through it at each level, record the results in a table, and put the corpus into the plan's test plan as named cases (T-ATK-n, T-OK-n).", 1)
(B / "RECONSTRUCTED-R2-reviser-fix-cycle-2-neutral.md").write_text(t, encoding="utf-8")

# chained-loop reviewer briefs 2 and 3: only ids, counts and original-run examples are generalised
SKIP = ("\n\nNOTE (RECONSTRUCTED): where this brief names a mechanism, rule, id or example that the plan you "
        "are reviewing does not contain, say so in one line and skip that item; do not invent it.\n")
t = (B / "R2-reviewer-L975.md").read_text(encoding="utf-8")
for old, new in [
    ("(the first review failed it with 8 blocking findings; a fixer has revised it)",
     "(the first review failed it with blocking findings; a fixer has revised it)"),
    ("plan-review.md (the first review: B-1..B-8 and the minor list)",
     "plan-review.md (the first review: its blocking and minor findings)"),
    ("1. For each of B-1..B-8, verify the fix really closes the original failure. Re-run the reviewer's original attack for B-1 (backtick substitution inside a push, backslash-newline continuation, dashed `/usr/lib/git-core/git-push`) and B-4 (gh api method flag forms) AGAINST",
     "1. For each blocking finding of the first review, verify the fix really closes the original failure. Re-run the first reviewer's original attack for every finding that has one AGAINST"),
]:
    assert t.count(old) == 1, old[:40]
    t = t.replace(old, new, 1)
(B / "RECONSTRUCTED-R2-reviewer-generic.md").write_text(t.rstrip("\n") + SKIP, encoding="utf-8")
t = (B / "R3-reviewer-L1032.md").read_text(encoding="utf-8")
(B / "RECONSTRUCTED-R3-reviewer-generic.md").write_text(t.rstrip("\n") + SKIP, encoding="utf-8")
print("CUT (fix 1):", len(cut1), "chars; CUT (fix 2):", len(cut2), "chars")
