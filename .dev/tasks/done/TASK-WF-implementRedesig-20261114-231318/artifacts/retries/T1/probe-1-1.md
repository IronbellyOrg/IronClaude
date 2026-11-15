425f1d1f9d6b52546b1f56cde8ae0d30df59dd94
family: count-claim (a row count of the sibling manifest stated in results/step0.md)
defect form: the text says 50 non-ABSENT rows; the manifest has 48
search: grep -n -E -e '\b50\b' -e 'non-ABSENT' -- /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/step0.md
before: step0.md:9 holds '50 non-ABSENT rows' (check column) and 'All 50 rows OK' (result column), both on line 9
coupled sites: results/step0.md line 9 only (no other line states the count); results/import-time.md states no manifest count
after: grep -n -E -e '\b50\b' over results/step0.md prints no line containing the word 50; line 9 now says 48 non-ABSENT rows and All 48 rows OK
