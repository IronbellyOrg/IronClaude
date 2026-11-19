9e98842b21d0a581b9bb6f1eaf613a14b78f4ba4
minor F1.1 (reviewer, ac=T23.AC2, height 8): at height 8 the desk view is 9 rows (160, 116) and 11 rows (80); the cause is the wrapping one-line panel summary of the forced ledger layout, not the desk panes; it predates this task (logged in the p2 notes; tests/observe/test_height_budget.py allows +4 at height 8). Parent severity: origin outside the diff, so not blocking.
note: plan text says the first desk line is "qid  age <age>"; the code draws "age <age>" (no message id) per Task 14, owner-approved Part C and the harness RB-14 check.
note: at width 80 the panes stack as question, evidence, list; the spec names no order.
note: the run line moves from the list title to the list body when a narrow list pane (46 cells) would cut the title.
note: 36 tests in tests/observe/test_render.py read the old single-column desk and fail until Task 24 reworks them; no golden changed.
