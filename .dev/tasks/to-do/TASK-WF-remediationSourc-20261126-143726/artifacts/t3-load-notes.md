# T3 load-check outcomes (honest summary, written by the implementer)

Seven-test load check (`t3-load-summary.json`; 8 parallel processes x 4 rounds = 32 runs, 16 busy-loop burners):
- "shim failed to start" (the original defect): 0 of 32 runs. Unfixed file: 8 to 19 percent of runs.
- 3 of 32 runs failed in `test_every_shim_launch_gets_the_port_for_its_settings` with "another shim took 127.0.0.1:<port> at the same moment" (rounds 1, 2, 3, one each: `fixed-r1-p2.log` port 4094, `fixed-r2-p0.log` port 4065, `fixed-r3-p0.log` port 4044; each is below 32768; each has `rc` 1 and `shim_failed_to_start` 0 in `t3-load-summary.json`).
  T3.AC4 is therefore NOT met: its wording needs "0 failed process-runs of 32" and 3 of 32 failed.
  That test never calls `_free_port` and sets no `CC_SHIM_PORT` (test lines 2397 to 2419): its port is `models.shim_port(4010)`, the settings hash. Not caused by this change by construction (the test does not use the changed code), but the cause of the failure itself is not proven (old-versus-new comparison runs did not start: relative `.venv/bin/pytest` path; no old-file run under the same load exists). Left as a follow-up.

Twenty whole-file runs under load (`t3-wholefile-summary.json`; one process at a time, 16 burners, timeout 945 s; timing run 472.5 s):
- 20 of 20 runs: `1 failed, 218 passed`; 0 "shim failed to start"; 0 "another shim took"; run times 384.7 to 479.8 s; no timeouts.
- The one failure in every run is `test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier` (`--model` where `--name` expected). Cause (inferred: the short and the long `--basetemp` also differ in location, not only in length): the harness's 223-character `--basetemp` path. Single-test checks: plain pass; short `--basetemp` pass; long `--basetemp` FAIL on the new file and FAIL on the old (HEAD) test file. So it is a harness path-length artifact, independent of this change and of the shims. The rows are in `t3-orca-isolation.log` (written after the A1 review; the single test alone and unloaded: `1 passed`; short `--basetemp`: `1 passed`; harness-like long `--basetemp`: `1 failed` on the new file and `1 failed` on the HEAD file, which equals `tree-old`'s test file).
- By the plan's rule it is recorded by name, run alone unloaded (passes), counts as a failed run; no run is repeated until it passes. The literal "all 20 results rc 0" is therefore NOT met by this harness: T3.AC5 is NOT met (20 of 20 results have `rc` 1). No listed wall-clock test (`test_cooldown_expires_and_repeats`, the `CCSESSION_FIRST_BYTE_TIMEOUT` tests) failed in any run (the `failed` lists in `t3-wholefile-summary.json` name only the orca test).

Unloaded whole file (plain pytest, no harness): `219 passed` (`t3-whole-file.log`).
