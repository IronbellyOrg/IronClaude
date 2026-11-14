9166c23cce094921f5b1d325c7ebb588998125b4
## family alarm-partial-sum (from r1-1)
defect form: a row-level total built from the ok packages only, compared with complete-row totals
command: grep -n -e 'def row_ledger' -e 'status' -e 'def row_jaccard' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/alarms.py
before:
30:def row_jaccard(r):
34:def row_ledger(r):
35:    v = [p.get("ledger_rows") for p in r["packages"].values() if p.get("status") == "ok"]
coupled sites: alarms.py row_ledger (sum), report() l0/ledg comparisons; row_jaccard is a mean (not a sum, unaffected); tests/test_alarms.py needs an incomplete-row case
## family vacuous-test-check (from r1-1)
defect form: a test asserts a key exists where pre already writes it, so the computed value is never exercised
command: grep -n -e 'anon_leak' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_anon.py
before:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py:40:    assert c["ledger_rows"] == 3 and "anon_leak" in c and c["arm"] == "A6-F3"
coupled sites: tests/test_collab_summary.py test_pre_post_and_r23_keys; collab_summary.py post (unchanged)
after (alarm-partial-sum):
30:def row_jaccard(r):
34:def row_ledger(r):
37:    if not ps or any(p.get("status") != "ok" or p.get("ledger_rows") is None for p in ps):
after (vacuous-test-check):
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py:43:    assert c["ledger_rows"] == 3 and c["anon_leak"] == 0 and pkg1.audit()["anon_leak"] == 0 and c["arm"] == "A6-F3"
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py:49:    assert c["anon_leak"] >= 2 and pkg1.audit()["anon_leak"] == c["anon_leak"]
