# D-0102 — Evidence

Live captures populated at T05.28 (M5 exit checkpoint):

- `.dev/releases/current/cliEval/evidence/T05.25/pytest-test-013.log` —
  full pytest -v output. Today: `2 failed, 4 passed in 0.23s`, exit 1.
- `tests/cli/eval/test_coverage_gate_integration.py` — 6-test module
  exercising both `eval doctor --check-coverage` and `eval run`
  top-of-run gate surfaces.
- `tests/cli/eval/fixtures/coverage_gate/` — 4-matcher fixture set
  (three covered + one uncovered).

Cross-references:

- `CP-P05-END.md` § Per-upstream-task status row T05.25 (PARTIAL).
- `CP-P04-END.md` § T04.14 (PASS — FR-G5 coverage gate landed).
- `evidence/T05.22/sc2.log` — independent confirmation that the
  doctor happy path (case 1) is green against the live
  `~/.claude/settings.json`.
