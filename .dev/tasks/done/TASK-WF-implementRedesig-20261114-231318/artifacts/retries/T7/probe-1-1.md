9a2c19ac6a5c46a994d676084e105e7aaf2c5628
family: fixture-comment (a character count stated in a comment of a fixture case)
defect form: a comment states the length of the item as 16 characters and the promoted id as 17; the item C4.12345678901234 has 17 characters and the promoted id 18
search: grep -n -E -e 'characters' -- .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/reports/make_rl_reports.py
before: make_rl_reports.py:442 only (the comment above the promote_long_id case)
coupled sites: the item literal at line 444 and tests/test_rowcheck.py (reads the case by name only, states no length)
after: grep -n -E -e 'characters' over make_rl_reports.py line 442 now says an item of 17 characters gives the promoted id P + item, 18 characters, over the limit of 16
