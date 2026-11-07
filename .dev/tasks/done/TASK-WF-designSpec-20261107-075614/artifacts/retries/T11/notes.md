313eea655daecb07153f2c6d37ae2627dc90dfdf
A1 r1-1 F1.1 minor tests/pr_submit/test_merge_guard_scenarios.py:10 ac=T11.AC1 n,n,n,n The module docstring says the fake_gh fixture is imported from test_set_draft_state.py, but the file defines its own fixture and imports only HEAD, REPO and FakeGh; wording only, the behavior is right.
A1 r1-1 F1.2 note tests/pr_submit/test_merge_guard_scenarios.py:351 ac=scope n,n,n,n The helper assert_never_readied re-filters ready_calls, which already excludes --undo, so it equals ready_calls == []; redundant but correct.
