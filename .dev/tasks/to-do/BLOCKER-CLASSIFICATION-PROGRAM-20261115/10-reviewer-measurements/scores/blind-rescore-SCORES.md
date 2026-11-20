# Blind rescore of rounds 3 and 4 (2026-11-20)

All 24 cards (X, Y, Z; 4 per arm per spec) were copied to `blind/E/` and `blind/B/` under shuffled names. Two opus scorers, one per spec, read only the cards, the spec and the plan, never the arm key (`arms/BLIND-KEY.md`) or earlier scores. Raw scorer tables with evidence quotes: `blind/SCORES-E.md`, `blind/SCORES-B.md`. Unblinded by the main session with the key. "Blocking" below counts a Blocking row of its own plus a finding named inside another Blocking row (folded), shown as own+folded.

X = master + stage 3c (PR 688). Y = X + Weak check. Z = X + Broken plan check.

## Spec E

| Item | X | Y | Z |
|---|---|---|---|
| E1 missing `csv2jsonl: ` prefix | 4 | 4 | 4 |
| E2 missing "no output written" | 4 | 4 | 3 (one Medium) |
| E3 no JSON writer task | 4 | 3 | 4 |
| E4 blank lines unchecked | 0+1 | 4+0 | 0+1 |
| E5 row number `<n>` undefined | 0 | 4+0 | 0 |
| E6 rows already written unchecked | 0+3 | 3+1 | 0+3 |
| E7 key order unchecked | 0 | 2+0 | 0+1 |
| E8 T2/T3 hand-off undefined | 3 | 1 | 1 |
| Blocking rows, 4 cards | 16 (4.0 per card) | 24 (6.0) | 13 (3.25) |

## Spec B

| Item | X | Y | Z |
|---|---|---|---|
| B1 "plain codepoint order" dropped | 4 | 4 | 4 |
| B2 ties not sorted before the top-N cut | 0 (never raised) | 0 | 0 |
| B3 no `wordcount` command | 1 | 1 | 1 (one more Medium) |
| B4 `tokenize.py` shadows the standard library | 0 (one card: gaps table only) | 4 | 3 (one card never raised it) |
| B5 file with text but no words | 0 | 0 (one Medium) | 0 |
| B6 literal `FILE` in messages | 0 | 2 | 0 |
| B7 plan header points at another run folder | 2 | 1 | 0 |
| B8 default N of 10 never reached | 0 | 0 (three Medium) | 0 |
| Blocking rows, 4 cards | 7 (1.75 per card) | 14 (3.5) | 8 (2.0) |

## Reading

The blind rescore reproduces every headline number of SCORES-ROUND3.md and SCORES-ROUND4.md (targets and Blocking rows per card). Two details differ from the earlier non-blind tables: X and Z both fold "rows already written" into another Blocking row on 3 of 4 cards (the earlier tables counted named rows only), and Z card 1 on spec E never raised the row number at all (SCORES-ROUND4 listed it as Medium). Neither changes the reading: Z keeps stage 3c's spec E result, adds the `tokenize.py` catch on 3 of 4 cards, adds no Weak check over-grading rows, and removes the probably-false header-path Blocking rows.

Limits: 4 cards per arm, one model per round, one blind scorer per spec, briefs reused (card 4 used brief 1).
