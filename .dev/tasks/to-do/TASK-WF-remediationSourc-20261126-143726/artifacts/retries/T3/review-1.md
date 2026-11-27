a9fc1ce2ec233f8373318a94053ad56959ea7755 08a655f4493fb58c8e8d0d16003328da1277bb17
(reviewer output, A1 review of T3; verbatim marks, then findings with the parent's keys)
Earlier blocking findings: none.
T3.AC1 met: tests/unit/test_ccsession_tiers.py:850-862, and :1933 asserts _free_port() + reach < low; the three patching tests pass in artifacts/t3-whole-file.log:5 (219 passed).
T3.AC2 met: artifacts/t3-green.log:2 shows 2 passed.
T3.AC3 met: artifacts/t3-whole-file.log:5 shows 219 passed, rc=0.
T3.AC4 unmet: F1.1.
T3.AC5 unmet: F2.1, F3.1.
T3.AC6 met: artifacts/t3-ruff.log:2,4.
T3.AC7 met: the diff touches only tests/unit/test_ccsession_tiers.py (hunk at :848).
F1.1 sev=blocking trigger=B1 ac=T3.AC4 at=.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-summary.json:97 anchor="ends with 0 failed process-runs of 32" chk=amiss:y,false:n,harm:n,constraint:n family=load-check-not-met fix=Report AC4 as not met without re-running; name the three failures (rounds 1, 2, 3; rc 1, shim_failed_to_start 0, another_shim 2) and say whether their ports are below 32768 covers="ends with 0 failed process-runs of 32" first=A1 origin=new: 3 of 32 process-runs failed in test_every_shim_launch_gets_the_port_for_its_settings; "shim failed to start" is 0.
F2.1 sev=blocking trigger=B1 ac=T3.AC5 at=.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-wholefile-summary.json:7 anchor="the check passes only when all 20 results have `rc` 0" chk=amiss:y,false:n,harm:n,constraint:n family=load-check-not-met fix=Report AC5 as not met and do not repeat the runs; name the failing test; say whether it is shim-related covers="all 20 results have `rc` 0" first=A1 origin=new: all 20 results have rc 1 (the one failing test is test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier).
F3.1 sev=blocking trigger=B1 ac=T3.AC5 at=.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-notes.md:10 anchor="run that single test alone and unloaded (`uv run pytest <its node id> -q -p no:cacheprovider -o addopts=`)" chk=amiss:y,false:n,harm:n,constraint:n family=missing-evidence-row fix=Add a log under ./artifacts/ for the single-test unloaded run and for the --basetemp length comparisons on the new and the HEAD test file covers="run that single test alone and unloaded" first=A1 origin=new: the notes claim the single test passes alone and fails with a 223-character --basetemp on both files, with no log row behind it.
