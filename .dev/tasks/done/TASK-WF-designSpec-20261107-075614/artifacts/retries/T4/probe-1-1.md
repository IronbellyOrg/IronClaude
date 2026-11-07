5964432d497cff3032b17f322a817022f4b705ad
family row-test-naming
defect form: resume row 9 (nothing to do) has no test whose name carries the row number; the other eight resume rows, all engage rows and all release rows do.
command: grep -n -E -e "def test_resume_row_" -e "def test_resume_held" -- tests/pr_submit/test_merge_guard.py
before:
  930:def test_resume_row_1_no_guard():
  934:def test_resume_row_2_report_held_wins_over_reconcile():
  952:def test_resume_row_2_skips_settled_phases(phase):
  999:def test_resume_row_3_reconcile_reasons(state, to, read, reason, cause):
  1008:def test_resume_row_4_release_after_a_landed_recovered_push():
  1018:def test_resume_row_4_release_after_a_normal_completed_push():
  1022:def test_resume_row_4_holds_on_a_moved_head_or_unknown_target():
  1028:def test_resume_row_4_published_with_zero_counter_still_counts_one_edit():
  1032:def test_resume_held_without_publication_is_a_noop():
  1036:def test_resume_row_5_not_landed_stays_held():
  1041:def test_resume_row_6_ambiguous_tip_holds(phase):
  1049:def test_resume_row_7_retry_release_when_owned():
  1053:def test_resume_row_8_ownership_unproven_when_live_draft():
coupled sites: the resume row 9 assertions inside test_resume_row_2_skips_settled_phases and test_resume_row_8_ownership_unproven_when_live_draft stay as they are (they assert the same NOOP result from other rows).
after:
  930:def test_resume_row_1_no_guard():
  934:def test_resume_row_2_report_held_wins_over_reconcile():
  952:def test_resume_row_2_skips_settled_phases(phase):
  999:def test_resume_row_3_reconcile_reasons(state, to, read, reason, cause):
  1008:def test_resume_row_4_release_after_a_landed_recovered_push():
  1018:def test_resume_row_4_release_after_a_normal_completed_push():
  1022:def test_resume_row_4_holds_on_a_moved_head_or_unknown_target():
  1028:def test_resume_row_4_published_with_zero_counter_still_counts_one_edit():
  1032:def test_resume_row_9_held_without_publication_is_a_noop():
  1036:def test_resume_row_5_not_landed_stays_held():
  1041:def test_resume_row_6_ambiguous_tip_holds(phase):
  1049:def test_resume_row_7_retry_release_when_owned():
  1053:def test_resume_row_8_ownership_unproven_when_live_draft():
