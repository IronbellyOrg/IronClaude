e50d93fe7e7ec8bfb6c87275c3e814a51d61eaa5
minor F1.1 (scope): the plan-ask test asserts one short list row ending in ">" and the whole ask (no hash) in the desk, not a hard-split in the list pane; list rows are one cut row by design (Part C), and nothing is lost on the screen.
minor F1.2 (scope): the desk tests were reworked mainly through a new split_panes helper in tests/observe/conftest.py (applied by the screen_lines wrapper) and pane_rows, plus pane_body and title_of in the new tests; panes_flat is unchanged.
minor F1.3 (evidence): only summary.md is kept per gate iteration, as for p3 and p4; the record the criterion names is scores/p5/scores.json.
note: iteration 1 of the gate failed RB-29 at 116 and 80; fixed in render.py _list_frame (rows lead beside an open desk); the harness also gained _split_panes before the reviewers ran.
note: the golden files are byte-identical to the task start tree; the diff against HEAD still shows the earlier tasks' regenerated goldens.
