# Final render gate, iteration 1: reviewer summary

Three fresh reviewers, one per width (160, 116, 80), text and ANSI tier. Every row RB-01 to RB-29 was scored (RB-19 is replaced by RB-27 and is N/A).

| Width | High or Medium failing | Other |
|---|---|---|
| 160 | none | RB-22 FAIL (Low, deferred) |
| 116 | none | RB-22 FAIL (Low, deferred) |
| 80 | none | RB-22 FAIL (Low, deferred) |

Script rows (`checks.json`): every row passes except RB-22; RB-16 and RB-19 are `na` by design (RB-16 scored by the reviewers from the ANSI, PASS at every width).

Reviewer notes (not blocking): the plan ask reads `(plan hash )?` after the hash is removed (RB-27, Part C); at height 8 the forced layout runs 1 to 3 rows over (logged diagnostic overflow); the 80-column count words are the owner-ruled short forms.
