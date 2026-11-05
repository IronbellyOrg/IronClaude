6aa687ed1dbc99706aeda1e704d3208db8ccfb64
A1 r1-1 F1.1 note tests/unit/test_ccsession_tiers.py:1538 ac=T1.AC1 n,n,n,n extra os.getsid assertion beyond the brief; it requires the fix to give the shim its own session (Task 3 does, via os.setsid), origin=new
A1 r1-1 F1.2 minor .dev/tasks/to-do/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t1-before.log:19 ac=T1.AC3 n,n,n,n leftover check in the log uses a regex over all per-test copies instead of the exact copy path and does not check sleep 60; reviewer re-ran and confirmed none left, origin=new
