# Phase 6 render gate, iteration 1: reviewer summary

Three fresh reviewers, one per width, text and ANSI tier.

| Width | High or Medium failing | Other |
|---|---|---|
| 160 | none | RB-22 FAIL (Low, deferred) |
| 116 | RB-29 | RB-22 FAIL (Low, deferred) |
| 80 | RB-29 | RB-22 FAIL (Low, deferred) |

RB-29 findings: the worker table heading `dispatchId` read as a raw field name on the desk (80 and 116; the 160 reviewer ruled it is outside the desk), and at 116 the four-line disclosure came before the question rows in the 46-cell list pane. The second is a real defect and was fixed for iteration 2.

Before this run the first harness pass failed RB-05, RB-24 and RB-26 because the harness read the two-column rows as one column; the harness now splits panes (render_compare.py `_split_panes`), and iter-1 holds the rerun.
