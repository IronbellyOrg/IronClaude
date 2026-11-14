4874fd7e0861dfa267ea57f5d7198aaeb6b225ea
tree=efd5fe0f8d6bb674f08b553a42f32916f1252d67
AC marks: T1.AC1 met, T1.AC2 met, T1.AC3 met (reviewer a1, citations in tests/sweep/test_git_config_hole.py and ./artifacts/t1-red.log)
F1.1 sev=blocking trigger=B1 ac=scope at=tests/sweep/test_git_config_hole.py:207-218 anchor="the branch is parsed" chk=y,n,n,n family=control-assert fix=assert the returned WorktreeState shows the status was read first=A1 origin=new: the control asserts only the marker, coverage "read" and unscanned None; it never asserts that the branch was parsed.
F1.2 sev=blocking trigger=B4 ac=scope at=tests/sweep/test_git_config_hole.py:19 anchor="module-level `pytestmark = pytest.mark.integration`" chk=n,n,n,y family=integration-mark fix=add the module-level pytestmark line first=A1 origin=new: the file marks each test with @integration instead of a module-level pytestmark.
