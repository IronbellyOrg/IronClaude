# D-0022 — Evidence pointer

**Task:** T01.26 (Phase 1, Roadmap FR-G3 / R-022)

Execution evidence lives at:

- `.dev/releases/current/cliEval/evidence/T01.26/run.md` — `pytest` log
  for the new `tests/cli/test_cli_registration.py` module and CLI smoke
  output (`superclaude --help`, `superclaude eval --help`).

Test sources:

- `tests/cli/test_cli_registration.py` — 5 regression tests covering
  every T01.26 AC bullet (see `spec.md` AC mapping table).
