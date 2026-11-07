b4448b44d29f2f1fb21048c4848e87d2e84e598a
family run-count
defect form: a speed case timed with fewer than 100 runs without an explicit allowance in the task text
command: grep -nE "RUNS ?= ?[0-9]+" tests/hooks/test_launch_level_guard.py
before-output:
1001:SPD_RUNS = 100
1004:LARGE_RUNS = 25
coupled sites: the Method sentence of the results file (reworded), the t15-test.log, speed-results.md rows; ENVELOPE_RUNS = 5 is the envelope stress case, for which the task gives no count
after:
1001:SPD_RUNS = 100
1004:LARGE_RUNS = SPD_RUNS
1009:ENVELOPE_RUNS = 5
