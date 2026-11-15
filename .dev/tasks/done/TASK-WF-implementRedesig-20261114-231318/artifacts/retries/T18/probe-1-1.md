dcbafbbbb2b98561998d2d5745447d43b70d1275
family: sandbox-gt-run-depth (the ground-truth check looks for run `briefs` folders at one fixed depth under the runs root)
defect form: a glob or find that reaches runs/<id>/briefs only, so runs/spike-timing/<run>/briefs and runs/spike-compliance/<run>/briefs are never searched
search: grep -n -E -e '/\*/briefs' -e 'name briefs' -e 'RUN/briefs' -- .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_check_scripts.py .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-order.sh .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/open-manual-checks.sh
coupled sites: the header comment of bin/check-sandbox-gt.sh (line 4, says "every RUN/briefs folder under the runs root"); the depth-one fixture in tests/test_check_scripts.py (lines 48, 67, 80); the run folders written by bin/run-spike.sh (read only here)
before:
.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh:4:# ($SW_SB_ROOT, default /tmp/evalsb-recipe) and over every RUN/briefs folder under the runs root ($RL_RUNS_ROOT, default
.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh:31:  for b in "$RUNS"/*/briefs; do
after:
.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh:4:# ($SW_SB_ROOT, default /tmp/evalsb-recipe) and over every RUN/briefs folder under the runs root ($RL_RUNS_ROOT, default
.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh:36:    done < <(find "$RUNS" -name .git -prune -o -type d -name briefs -print | sort)
