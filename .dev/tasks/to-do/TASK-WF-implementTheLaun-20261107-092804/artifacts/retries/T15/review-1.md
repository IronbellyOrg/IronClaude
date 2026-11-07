b4448b44d29f2f1fb21048c4848e87d2e84e598a c7a9c31c94364963db199f5fd3db807f7d15bbe4
T15.AC1 met tests/hooks/test_launch_level_guard.py:1213
T15.AC2 met ./artifacts/speed-results.md:13
T15.AC3 met ./artifacts/speed-results.md:30
F1.1 sev=blocking trigger=B4 ac=scope at=tests/hooks/test_launch_level_guard.py:1004 anchor="LARGE_RUNS = 25" chk=n,n,n,y family=run-count fix=set LARGE_RUNS to 100 and regenerate the results file covers="Use 100 runs per case" first=A1 origin=new: T-SPD-5 used 25 runs per command although the task says 100 runs per case.
