# Combined measurement, round 3 (2026-11-19, owner "run 4 per arm")

Arms (key: `arms/KEY.md`): X = master + stage 3c passage (sha256 7696a2b2...). Y = X + the Weak check edit of the run B session (sha256 02f75e35..., built with `git merge-file`). Reviewers: 4 per arm per spec, general-purpose agents on sonnet reading the arm's agent file, briefs 1, 2, 3, 1 of `rerun-20261118/E` and `rerun-20261118/B-clean`, cards saved next to this file. Scored by the main session from the graded "What diverged" cells; no second reader.

## Spec E (csv2jsonl)

| Finding | X | Y |
|---|---|---|
| Missing `csv2jsonl: ` prefix graded Blocking | 4 of 4 | 4 of 4 |
| Missing "no output written" graded Blocking | 4 of 4 | 4 of 4 |
| No task builds the JSON writer graded Blocking | 4 of 4 | 3 of 4 (Y1 Medium) |
| Blank lines have no check, graded Blocking | 0 of 4 | 4 of 4 |
| Undefined row number `<n>` (spec silent, plan asserts the exact message), graded Blocking | 0 of 4 (Medium) | 4 of 4 (Y3 folds it into its blank-lines row) |
| "Rows already written stay written" has no check, graded Blocking | 0 of 4 (Medium or folded into the T2/T3 hand-off row) | 3 of 4 |
| Key order has no check, graded Blocking | 0 of 4 | 2 of 4 |
| Blocking rows, 4 cards | 16 (4.0 per card) | 24 (6.0 per card) |

## Spec B (wordcount, B-clean)

| Finding | X | Y |
|---|---|---|
| Plan drops "plain codepoint order", graded Blocking | 4 of 4 | 4 of 4 |
| Ties sorted before the top-N cut (owner-ruled blocker) raised at all | 0 of 4 | 0 of 4 |
| No task creates the `wordcount` command, graded Blocking | 1 of 4 (1 more Medium) | 1 of 4 |
| `code/tokenize.py` shadows the standard library, graded Blocking | 0 of 4 (1 as a non-gating gap) | 4 of 4 |
| No-words file (text but no words) graded Blocking | 0 of 4 (not raised) | 0 of 4 (1 Medium) |
| Literal `FILE` in quoted messages (spec ambiguous) graded Blocking | 0 of 4 | 2 of 4 |
| Plan header path graded Blocking (Safety) (probably false: a copy artifact) | 2 of 4 | 1 of 4 |
| Blocking rows, 4 cards | 7 (1.75 per card) | 14 (3.5 per card) |

## Reading

- On spec E the Weak check adds nothing to the target findings (both arms 4 of 4) and adds 2 Blocking rows per card. Some of those (blank lines, rows already written) are arguable weak checks; the row-number rows grade a spec silence as Blocking through the Weak check's last sentence.
- On spec B the Weak check's only gain is the `tokenize.py` clash (0 to 4 of 4, Fisher two-sided p about 0.03). The Weak check text names that exact case as an example ("a module name that shadows the standard library"), so spec B is its tuning spec, not a held-out test. It does not move the two findings it was built for: the tie at the cut (0 of 4 in both arms) and the no-words file (0 of 4 Blocking in both arms). It doubles Blocking rows per card.
- Stage 3c alone held its round 2 result: E targets 4 of 4, codepoint 4 of 4; the missing command fell from 2 of 3 to 1 of 4.

Limits: 4 reviewers per arm, one model, one scorer, no blind second reader, briefs carry first-pass hints, run 4 reuses brief 1, both texts name examples from the spec they were tuned on, the merge step is not tested, general-purpose agents rather than the real reviewer agent type.
