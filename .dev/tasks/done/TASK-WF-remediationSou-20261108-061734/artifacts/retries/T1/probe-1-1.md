0e3f563466981fcebe2faa51b2b5f06203b5470d

## family=cmd-provenance (from review r1-1)

Defect form: a measurement artifact's only command record is the report generator's hardcoded boilerplate, not the actual invocation, so "plus the command used" is unmet and the recorded -k contradicts the artifact's own table.

Search command (read-only): grep -n -e "SPD or speed" -e "Run: " .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md tests/hooks/test_launch_level_guard.py

before-output (touched files + AC-named files):
- .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md:7: - Run: 2026-11-08 06:47 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
- tests/hooks/test_launch_level_guard.py:1097: f'- Run: {{run_stamp}} UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.'

Coupled sites (same scope, same rule): every artifact this package produces with an LL_SPEED_RESULTS report header (d1 now; d4 and d2 will get the same generator header when Tasks 2-3 run), because each carries the same hardcoded boilerplate line; the executor-added provenance line must be added to each when it is created. No coupled site in tracked source: the generator line (test :1097) is not edited by this task (the guard-script constraint does not forbid test edits, but this task's AC is the artifact, not the generator).

after (fix pass output; the placeholder line below is superseded):
- (to be appended by the fix pass)
after:
- .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d1-serial-idle.md:8:- Run: 2026-11-08 06:47 UTC, `LL_SPEED_RESULTS=<this file> uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.
- tests/hooks/test_launch_level_guard.py:1095:        f"- Run: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC, "
- tests/hooks/test_launch_level_guard.py:1097:        'tests/hooks/test_launch_level_guard.py -k "SPD or speed"`.',
- note: the generator boilerplate line remains (now at artifact line 8 after the executor-added COMMAND USED line was inserted at line 2); the artifact now also records the actual invocation at line 2, which is the fix for F1.1.
