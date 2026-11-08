fe9cd8a481c6c7543b8bba4d8b7e5784c0aa65a6

## family t5-parallel-runs-green (review r1-1, F1.1)
- defect form: the recorded parallel/serial run set contains a run with a failure, so the AC 'five -n auto runs and one serial run all pass' is not shown.
- command: grep -n -F -e "failed" -- .dev/tasks/to-do/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t5-runs.md
- before:
    25:    [ccsession] ERROR: shim failed to start (try: python3 .../shim-under-test.py)
- coupled sites: t5-runs.md result line ("5 of 6 runs fully green") and the run table; plan line 95 (AC text, not edited).
- after (set 2 recorded, ruling recorded; set 1 run 3 kept on purpose):
    25:    [ccsession] ERROR: shim failed to start (try: python3 .../shim-under-test.py)
- outcome: not fixed by design. Set 2 (/tmp/issue443-runs2) is 6 of 6 green; the one set 1 failure is the #352 class. Coordinator ruling msg_7ce89f6e15c5 carries T5.AC2 as a gap; no fourth review.
