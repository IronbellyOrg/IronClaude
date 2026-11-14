78930ede7a7ee767148a9b727bc4eec0479ac169
A1 r1-1 F1.1 minor .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_launch.py:193 ac=T7.AC1 n,n,n,n F-5 asserts the ALARM line only, not hook_calls 0 and isolated true in collab.json
A1 r1-1 F1.2 minor .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py:107 ac=T7.AC1 n,n,n,n F-3 re-counts slots instead of reading the observable_moves_executed counter
A1 r1-1 F1.3 minor .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py:72 ac=T7.AC1 n,n,n,n F-13 breaks ctx/index.json instead of making the hook exit 1 mid-run; a non-zero hook exit is left to S0
A1 r1-1 F1.4 minor .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py:50 ac=T7.AC1 n,n,n,n T-17 asserts R-23 key presence; only some null-valued F3 keys are asserted None
