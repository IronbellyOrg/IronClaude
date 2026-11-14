a9d6be7252ea167aab6d56f1fe55110894480bbc
A1 r1-1 F1.1 note tests/sweep/test_cli_contract.py:1033 ac=scope amiss:n,false:n,harm:n,constraint:n The new test pins removable_reason == "unpushed branch: no upstream"; DESIGN FR-013 names only the condition `no upstream`, so the test also freezes the code's `unpushed branch:` prefix (consistent with DESIGN and classify.py:454, not a defect).
