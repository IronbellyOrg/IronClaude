# Reviewer-only measurement, round 2 (2026-11-19)

Same set-up as `measure/SCORES.md`: sonnet reviewers, three per arm, briefs 1 to 3 of each run, agent text swapped per arm, reviewers blind to each other and to earlier results. Scored by the main session reading each card's "What diverged" cells; no second reader. Arms: control (master text), brainstorm (`measure/brainstorm/`), troubleshoot (`measure/troubleshoot/`, spec E only), carry-scope (third variant, `measure/carryscope/`).

## Spec E (csv2jsonl), target findings

| Finding | control | brainstorm | troubleshoot | carry-scope |
|---|---|---|---|---|
| Missing `csv2jsonl: ` prefix graded Blocking | 1 of 3 | 3 of 3 | 3 of 3 | 2 of 3 |
| Missing "no output written" graded Blocking | 0 of 3 | 3 of 3 | 1 of 3 | 0 of 3 (2 raised it as Medium) |
| No JSON writer task graded Blocking | 3 of 3 | 3 of 3 | 3 of 3 | 2 of 3 |
| Blocking rows, 3 cards | 5 | 10 | 12 + 1 Safety | 4 |

Carry-scope reviewer 2 wrote that opening the output first "would leave an empty file on a read error" and still graded it Medium, so the bullet's step-order clause was not applied.

## Held-out spec B (wordcount), clean briefs

| Finding | control | brainstorm | carry-scope |
|---|---|---|---|
| Ties sorted before the top-N cut (old M6, owner-ruled blocker) raised at all | 0 of 3 | 0 of 3 | 0 of 3 |
| Plan drops "plain codepoint order" from the tie rule, graded Blocking | 0 of 3 (3 Medium) | 3 of 3 | 0 of 3 (2 Medium, 1 not raised) |
| No task creates the `wordcount` command (old B2), graded Blocking | 0 of 3 (1 Medium) | 2 of 3 | 0 of 3 (not raised) |
| `code/tokenize.py` shadows the standard library, graded Blocking | 1 of 3 (2 more as non-gating correctness gaps) | 0 (1 as a gap) | 0 (2 as gaps) |
| Plan header points at the old run folder, graded Blocking (Safety) | 1 of 3 | 1 of 3 (`consumer-unknown`) | 0 |
| Blocking rows, 3 cards | 2 | 6 | 0 |

Whether the codepoint qualifier is a real blocker is a judgment: alphabetical and codepoint order agree on lowercase letters but not on digits and apostrophes, which the spec's word rule allows. The header-path Safety rows (one in control, one in brainstorm) are probably false: the path is a copy artifact of the throwaway set-up.

## Reading

- Brainstorm variant: best on E and the only arm that moved held-out grades upward; no extra over-grading compared with control on B.
- Carry-scope: worse than brainstorm on E and fewer findings than control on B (one reviewer raised a single Note). Not recommended.
- Troubleshoot: over-grades (round 1).
- The tie-before-cut blocker was never raised by any reviewer in any arm: a detection miss, not a grading fault; no grading text fixes it.

Limits: one model, three reviewers per arm, one scorer, briefs carry first-pass hints, the brainstorm variant names two E findings as examples, the merge step is not tested.
