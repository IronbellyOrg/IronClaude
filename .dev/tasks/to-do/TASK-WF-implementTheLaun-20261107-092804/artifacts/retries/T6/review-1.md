a71679b8baffe69f6b4fc5cc10faf788beaaf140 0e3ac0c5f894004cd7b71d4bf5c901947fe6bd96
T6.AC1 met tests/hooks/test_launch_level_guard.py:1556-1572
T6.AC2 met tests/hooks/test_launch_level_guard.py:1542
T6.AC3 met tests/hooks/test_launch_level_guard.py:1638-1661
T6.AC4 met tests/hooks/test_launch_level_guard.py:1328
F1.1 sev=blocking trigger=B1 ac=scope at=tests/hooks/test_launch_level_guard.py:1263 anchor="a payload with `\/` escapes in a tamper path is blocked" chk=y,n,n,n family=nrm-mr-coverage fix=add a raw-bytes JSON test with \/ escapes, strict xfail for Task 9 covers="every T-NRM case of MR section 8.2" first=A1 origin=new: row nrm4-escaped-slash sends shell-style backslash-slash text through the command field, so the jq decode of JSON \/ escapes (T-NRM-4) has no test.
F2.1 sev=blocking trigger=B1 ac=scope at=tests/hooks/test_launch_level_guard.py:1266 anchor="blocked at every level (LL-PUSH-FORM at FS)" chk=y,n,n,n family=nrm-mr-coverage fix=add a test that nrm5-push, nrm8-push-space and nrm2-push block at W, WA and F as strict xfail for Task 7 covers="every T-NRM case of MR section 8.2" first=A1 origin=new: the rows use FS_ONLY, so W, WA and F are skipped although T-NRM-5 and T-NRM-8 require blocked at every level.
