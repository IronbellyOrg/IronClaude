from pathlib import Path
R = Path("src/superclaude/rules/prompts/document_review_loop_prompts.md")
t = R.read_text(encoding="utf-8")

row = "| After a review report with open blocking findings, to revise | REVISE prompt |\n"
assert t.count(row) == 1
t = t.replace(row, row +
 "| After the loop's PASS (a scoped PASS, or a first review that passed) | GATE prompt, once |\n"
 "| After a gate review with open blocking findings | REVISE prompt, then one RE-REVIEW prompt: the gate loop |\n")

para = "At `review: 3` with an open blocking finding the loop escalates to the user; no REVISE prompt and no fourth review.\n"
assert t.count(para) == 1
t = t.replace(para, para + "\n"
 "The gate loop under the GATE prompt numbers its own reviews (`review: 1 of 3` for the gate review, `review: 2 of 3` for its re-review), so no report is ever a fourth review.\n")

block = '''### GATE prompt

Run it once, after the loop's PASS, on the document as it then stands. Brief the gate reviewer in a fresh context that has seen no report of this loop, and grade with the FIRST-REVIEW prompt's grading check.

- **Gate loop**: a blocking finding of the gate review starts one gate loop: one REVISE prompt with the gate's blocking ids, then one RE-REVIEW prompt with the gate report as PRIOR. A PASS of that re-review ends the loop; a FAIL escalates to the user with the open blocking findings, with no second gate loop and no further review.
- **Stall rule**: if every blocking finding of the gate review repeats a blocking finding of an earlier review in this loop (the same stated text and the same wrong outcome), the loop is stalled: escalate to the user with them and start no gate loop.
- **Ceiling**: the loop's 3 reviews and 2 fix cycles, plus the gate review, one fix cycle and one re-review: at most 5 reviews and 3 fix cycles in all.
- Gate brief: "This is a first review of a complete document; no prior rounds exist. Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."

'''
assert t.count("## Never\n") == 1
t = t.replace("## Never\n", block + "## Never\n")
R.write_text(t, encoding="utf-8")

old = "and whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review."
new = "and whole-document assurance needs a separate, labelled first review, the gate review, whose blockers never start a fourth review: they start at most one gate loop of one fix cycle and one re-review, a FAIL or a stall there escalates to the user, and a document gets at most 5 reviews and 3 fix cycles in all."
for rel in ("src/superclaude/commands/spec-panel.md", "plugins/superclaude/commands/spec-panel.md"):
    p = Path(rel); s = p.read_text(encoding="utf-8")
    assert s.count(old) == 1, rel
    p.write_text(s.replace(old, new), encoding="utf-8")
print("ok")
