68452bae4a42000ec0997738b027d452c5256ffc
family bound-test-never-reaches-cut
defect form: a test asserts an upper or lower bound with an input that cannot reach the code the bound is meant to check, so removing that code leaves the test green
search: grep -n -e 'assert len(' -e '<= 80' -e 'seconds <' tests/unit/test_ccsession_tag.py
before-output: 2196:    assert len(label) <= 80, label|2203:    assert len(labels) >= 2|2343:    assert seconds < 20|
coupled sites: test_auto_name_stays_short_and_keeps_its_stamp_for_a_long_folder (input reaches only the 20-character folder cut and short words; fixed); test_auto_name_two_calls_in_the_same_second_differ (reaches the random part: removing it makes the labels equal in a second, the reviewer saw it fail); test_ask_gives_up_after_the_limit_with_exit_1 (CCSESSION_ASK_TIMEOUT=1 and no input: without the timeout the run lasts 30 s, so seconds < 20 fails)
after: 2199:    assert len(label) <= 80, label|2206:    assert len(labels) >= 2|2346:    assert seconds < 20|cut now reached: fixed test fails with ccsession:635 removed (1 failed), passes with it (1 passed)
