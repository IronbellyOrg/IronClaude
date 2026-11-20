# Combined measurement, round 4 (2026-11-20)

Arms (key: `arms/KEY.md`, `Z-x/reflect-reviewer.md`): X = master + stage 3c passage (`arms/s3c.md`). Y = X + the Weak check edit (`arms/s3c-weak.md`). Z = X + one added bullet "Broken plan check." (from `brainstorm-tokenize/reflect-reviewer.md`; `diff -u arms/s3c.md` shows 1 added line, 0 removed). The Z line keeps the plan-defect routing and anchor, names the stdlib-shadowing example, and leaves out the probe step, the three-part Blocking licence, the anti-downgrade and "plausible" clauses and the spec-silent exact-value clause. X and Y columns are copied from `SCORES-ROUND3.md` (not re-scored). Z: 4 reviewers per spec, general-purpose agents on sonnet reading `Z-E/` or `Z-B/reflect-reviewer.md`, briefs 1, 2, 3, 1 of `rerun-20261118/E` and `rerun-20261118/B-clean`, cards `Z-E/card-1..4.md`, `Z-B/card-1..4.md`. Scored by the main session from the graded "What diverged" cells (both `Blocking (Decision):` and `Blocking (Decision), ...` forms counted; each row read before deciding).

## Spec E (csv2jsonl)

| Finding | X | Y | Z |
|---|---|---|---|
| Missing `csv2jsonl: ` prefix graded Blocking | 4 of 4 | 4 of 4 | 4 of 4 |
| Missing "no output written" graded Blocking | 4 of 4 | 4 of 4 | 3 of 4 (Z3 Medium, inside a T4-omissions row) |
| No task builds the JSON writer graded Blocking | 4 of 4 | 3 of 4 (Y1 Medium) | 4 of 4 |
| Blank lines have no check, graded Blocking | 0 of 4 | 4 of 4 | 0 of 4 as a named row (Z2 lists it inside a combined T4-omissions Blocking row, like X-E/card-3 row 5) |
| Undefined row number `<n>` graded Blocking | 0 of 4 (Medium) | 4 of 4 | 0 of 4 (Medium in Z1, Z3, Z4; Note in Z2) |
| "Rows already written stay written" has no check, graded Blocking | 0 of 4 (Medium or folded into the T2/T3 hand-off row) | 3 of 4 | 0 of 4 as a named row (folded into Blocking writer or hand-off rows in Z2, Z3, Z4; Medium in Z1) |
| Key order has no check, graded Blocking | 0 of 4 | 2 of 4 | 0 of 4 as a named row (Z2 lists it in the combined T4 row; Medium in Z3, Z4) |
| Blocking rows, 4 cards | 16 (4.0 per card) | 24 (6.0 per card) | 13 (3.25 per card) |

## Spec B (wordcount, B-clean)

| Finding | X | Y | Z |
|---|---|---|---|
| Plan drops "plain codepoint order", graded Blocking | 4 of 4 | 4 of 4 | 4 of 4 |
| Ties sorted before the top-N cut raised at all (not in scope) | 0 of 4 | 0 of 4 | 0 of 4 |
| No task creates the `wordcount` command, graded Blocking | 1 of 4 (1 more Medium) | 1 of 4 | 1 of 4 (Z3; Z1 Medium) |
| `code/tokenize.py` shadows the standard library, graded Blocking | 0 of 4 (1 as a non-gating gap) | 4 of 4 | 3 of 4 (Z1, Z3, Z4; Z2 did not raise it) |
| No-words file graded Blocking | 0 of 4 (not raised) | 0 of 4 (1 Medium) | 0 of 4 (not raised) |
| Literal `FILE` in quoted messages graded Blocking | 0 of 4 | 2 of 4 | 0 of 4 |
| Plan header path graded Blocking (Safety) (probably false) | 2 of 4 | 1 of 4 | 0 of 4 (Medium in all four; Z3 and Z4 tagged `consumer-unknown`) |
| Blocking rows, 4 cards | 7 (1.75 per card) | 14 (3.5 per card) | 8 (2.0 per card) |

## Reading

- Z keeps most of the tokenize gain: 3 of 4 on spec B against 0 of 4 for X and 4 of 4 for Y. The three cards that raised it graded it Blocking (Decision) in the Deviations table on the T1 or T5 check, as the line asks. Z against X: Fisher two-sided p about 0.14, so this is not significant at 4 cards; Z against Y: 3 of 4 against 4 of 4, no detectable difference.
- The one Z card that missed it (Z-B/card-2) never raised the clash at all, the same pattern as X-B cards 1, 2 and 4. So the open question from the brainstorm (can routing alone raise recall, or did the probe step or the example do it) is only partly answered: routing fixes grade and placement; the missing card shows recall is not fully fixed by the line. The data cannot say which part of the Z line raised recall in the three that found it.
- Z removes the Weak check's extra Blocking rows. Spec E: 3.25 per card (X 4.0, Y 6.0); spec B: 2.0 per card (X 1.75, Y 3.5). None of the Y-only row classes was promoted as a named row (blank lines, `<n>`, rows written, key order, `FILE`). Z also dropped the plan-header Safety rows from Blocking to Medium (X 2, Y 1, Z 0), which is a side effect to check, not a designed one.
- Cost: one catch on spec E fell, "no output written" 4 of 4 to 3 of 4 (Z-E/card-3 put it in a Medium T4-omissions row whose text echoes the line's exclusion "a wrong implementation could pass"). That is one card and could be noise; Y lost one card on the writer in the same way. It is a watch item, not a result.
- Brainstorm pass bars from `merged-requirements.md` section 3 item 8: tokenize at least 3 of 4: met (exactly at the bar); E at most 4.5 and B at most 2.75 Blocking rows per card: met (3.25, 2.0); no new promotion of the named Y-only classes: met as named rows (Z2 lists blank lines and key order inside one combined Blocking row, as X-E/card-3 did); prefix, no-output, writer and codepoint catches held at X levels: not fully met (no-output 3 of 4).

Limits: 4 reviewers per arm per spec, one model, one scorer, no blind second reader (the scorer is the session that ran the brainstorm and knew which arm was Z); briefs carry first-pass hints and run 4 reuses brief 1; the Z line names the tokenize example, so spec B is its tuning spec and the tokenize score is not a held-out test; spec E has no plan-defect target, so it only measures extra rows; the no-example control (`brainstorm-tokenize/reflect-reviewer-control-no-example.md`) was not run, so the contribution of the example is untested; X and Y are the round 3 numbers, run on a different day with different reviewer instances; the merge step is not tested; general-purpose agents rather than the real reviewer agent type; the placement as a separate bullet after line 123 is tested only here.
