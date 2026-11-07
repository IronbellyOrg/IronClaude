bb05a78128b0ec419876a148437ce898b8960c30
family fold-notapplied-draft-direction
defect form: the tests for a settled not_applied request of the draft direction assert only phase, unsettled, failed_mutations and disabled_cause, so a fold that touched owned_draft or run_toggles for that direction would pass.
command: grep -n -E -e "not_applied" -- tests/pr_submit/test_merge_guard.py src/superclaude/pr_submit/merge_guard.py
before:
  tests/pr_submit/test_merge_guard.py:221:    "ready_not_applied_returns_to_held": (
  tests/pr_submit/test_merge_guard.py:222:        ENGAGED + [req("ready"), settled("ready", "skipped", cause="not_applied")],
  tests/pr_submit/test_merge_guard.py:231:    "draft_not_applied_after_failed_engage_returns_to_release_pending": (
  tests/pr_submit/test_merge_guard.py:236:            settled("draft", "skipped", cause="not_applied", attempt=2),
  tests/pr_submit/test_merge_guard.py:266:def test_fold_first_request_not_applied_erases_the_record():
  tests/pr_submit/test_merge_guard.py:269:        settled("draft", "skipped", cause="not_applied"),
  tests/pr_submit/test_merge_guard.py:274:def test_fold_request_not_applied_request_takes_a_fresh_baseline():
  tests/pr_submit/test_merge_guard.py:277:        settled("draft", "skipped", cause="not_applied"),
  src/superclaude/pr_submit/merge_guard.py:179:    ``not_applied`` request of either direction clears its key and returns the
  src/superclaude/pr_submit/merge_guard.py:234:        if cause == "not_applied":
coupled sites: the table entry draft_not_applied_after_failed_engage_returns_to_release_pending, test_fold_first_request_not_applied_erases_the_record and test_fold_request_not_applied_request_takes_a_fresh_baseline in tests/pr_submit/test_merge_guard.py (all draft direction; the ready direction entry ready_not_applied_returns_to_held already asserts owned_draft and run_toggles).
after:
  tests/pr_submit/test_merge_guard.py:221:    "ready_not_applied_returns_to_held": (
  tests/pr_submit/test_merge_guard.py:222:        ENGAGED + [req("ready"), settled("ready", "skipped", cause="not_applied")],
  tests/pr_submit/test_merge_guard.py:231:    "draft_not_applied_after_failed_engage_returns_to_release_pending": (
  tests/pr_submit/test_merge_guard.py:236:            settled("draft", "skipped", cause="not_applied", attempt=2),
  tests/pr_submit/test_merge_guard.py:247:    # A draft-direction not_applied must leave ownership and the toggle counters
  tests/pr_submit/test_merge_guard.py:249:    "draft_not_applied_keeps_a_held_state": (
  tests/pr_submit/test_merge_guard.py:253:            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
  tests/pr_submit/test_merge_guard.py:264:    "draft_not_applied_keeps_a_released_state": (
  tests/pr_submit/test_merge_guard.py:270:            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
  tests/pr_submit/test_merge_guard.py:281:    "draft_not_applied_keeps_a_disabled_state": (
  tests/pr_submit/test_merge_guard.py:291:            settled("draft", "skipped", cause="not_applied", cycle="fix-2"),
  tests/pr_submit/test_merge_guard.py:323:def test_fold_first_request_not_applied_erases_the_record():
  tests/pr_submit/test_merge_guard.py:326:        settled("draft", "skipped", cause="not_applied"),
  tests/pr_submit/test_merge_guard.py:331:def test_fold_request_not_applied_request_takes_a_fresh_baseline():
  tests/pr_submit/test_merge_guard.py:334:        settled("draft", "skipped", cause="not_applied"),
  src/superclaude/pr_submit/merge_guard.py:179:    ``not_applied`` request of either direction clears its key and returns the
  src/superclaude/pr_submit/merge_guard.py:234:        if cause == "not_applied":
