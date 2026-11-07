2e08cfbe0f231dcbea4d9887a017f686a608a579
A1 r1-1 F1.1 note ac=T10.AC3 at=tests/hooks/test_launch_level_guard.py chk=n,n,n,n: no MCP_CASES entry has more than one double underscore after the server segment, so the last-double-underscore parse (FR-L-45) is not pinned; a mutation to first-double-underscore passes.
A1 r1-1 F1.2 note ac=T10.AC2 at=tests/hooks/test_launch_level_guard.py chk=n,n,n,n: GRID_CLASSES is hand-typed; a 17th class added to the script would not fail the module.
A1 r1-1 F1.3 note ac=T10.AC2 at=tests/hooks/test_launch_level_guard.py chk=n,n,n,n: REPO and PUSHFORM cells at W, WA and F are unreachable by a real call; only FS is checked against EXPECTED.
A1 r1-1 F1.4 note ac=T10.AC1 at=tests/hooks/test_launch_level_guard.py chk=n,n,n,n: untested edges: TaskCreate/TaskStop/TaskOutput NONE, upper-case MCP prefixes, create_ref, pull_request_read, Agent isolation true.
A1 r1-1 F1.5 note ac=T10.AC4 at=tests/hooks/test_launch_level_guard.py chk=n,n,n,n: accepted leaks are labelled by test ids and comments only; the corpus rows repeating them carry no label.
