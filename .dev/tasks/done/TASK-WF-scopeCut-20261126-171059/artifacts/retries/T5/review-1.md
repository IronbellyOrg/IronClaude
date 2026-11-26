1aec63c6b8c340fabceb4d511a4753af001cf679 tree=111e9485ea8b637230a613e2b72222f13c79cc6a
T5.AC1 met: scripts/apply_org_rulesets.py:821-860 (UsageError for every usage mistake), tests/org_rulesets/test_cli.py:28-52.
T5.AC2 met: scripts/apply_org_rulesets.py:864-881 (refusal printed on stderr, EXIT_FAILED), tests/org_rulesets/test_cli.py:56-69.
T5.AC3 met: tests/org_rulesets/test_cli.py:72-106 (comment line, one DELETE per id; read-back failure prints the one written id and exits 69).
T5.AC4 met: scripts/apply_org_rulesets.py:898-902, tests/org_rulesets/test_cli.py:109-116.
T5.AC5 met: tests/org_rulesets/test_cli.py:125-142 (closed list of allowed shapes, no upstream org name, no protected id).
T5.AC6 met: tests/org_rulesets/test_cli.py:145-151, scripts/apply_org_rulesets.py:32-33.
T5.AC7 met: 125 passed, ruff check and ruff format --check clean (reviewer's own run).
F1.1 sev=blocking trigger=B4 ac=scope at=scripts/apply_org_rulesets.py:758 anchor="`EXIT_FAILED` (69) for a refusal or a failed step" chk=n,n,n,y family=exit-code-unhandled-oserror fix=catch OSError in main (and name it on stderr, exit EXIT_FAILED) and add a test that passes an --out folder that cannot be created covers="`EXIT_FAILED` (69) for a refusal or a failed step" first=start origin=inherited: an --out folder that cannot be created ends the run with a traceback and exit 1 instead of "failed:" on stderr and exit 69 (reviewer reproduced it with a fake runner and --out under a missing parent); no POST happened. Parent note: the flagged lines are Task 4 text present in the start tree, but the exit-code contract that Task 5's task-added `main` states ("EXIT_FAILED (69) for a refusal or a failed step") depends on them, so the inherited cap is lifted (qa.md, Finding origin: task-added sentence depends on it).
F1.1 resolved
