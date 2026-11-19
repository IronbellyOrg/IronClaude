# Phase 6 render gate, iteration 2: reviewer summary

Three fresh reviewers, one per width (160, 116, 80), text and ANSI tier. Each scored RB-01 to RB-29 (RB-18 not yet scheduled, RB-19 replaced by RB-27).

| Width | High or Medium failing | Other |
|---|---|---|
| 160 | none | RB-22 FAIL (Low, deferred) |
| 116 | none | RB-22 FAIL (Low, deferred) |
| 80 | none | RB-22 FAIL (Low, deferred) |

RB-29 scope note given to the reviewers: the desk is the question pane and the LINKED SESSION pane; the worker table below is scored under RB-12 and RB-28.

Iteration 1 (iter-1 folder): RB-29 failed at 116 and 80 (two of three reviewers). Cause: in the narrow list pane the four-line disclosure sat above the question rows. Fix in render.py `_list_frame`: with the desk open the question rows lead. The 160 reviewer passed RB-29 in iteration 1.

Minor notes from reviewers: the selected row is a short stub ending in `>` by design (the desk holds the full text); the first desk line is `age <age>` without a message id (Part C).
