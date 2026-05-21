# T05.28 Evidence — Phase 5 / M5 exit gate

## Files

- `eval-list.txt` — live `uv run superclaude eval list` capture.
  Output: `real (version 1.0, 17 evals)`, exit 0. Confirms
  Verification 1 (15 conceptual / 17 expanded eval ids enumerate).
- `eval-doctor-check-coverage.txt` — live `uv run superclaude eval
  doctor --suite real --check-coverage` capture. Output: `all HARD
  capabilities satisfied`, `coverage gate: 3/3 matcher(s) covered
  (passed)`. Confirms Verification 2.
- `eval-doctor-exit.txt` — `0`.
- `eval-run-parallel-8.log` — live `uv run superclaude eval run
  --suite real --parallel 8` capture. Output: `NameError: name
  '_new_run_id' is not defined` at `commands.py:1418`. Exit:
  `---EXIT:1`. Confirms Verification 3 + Exit Criterion 1 are NOT
  MET.

## AC mapping

See `CP-P05-END.md` § Verification (2 / 3 confirmed), § Exit Criteria
(2 / 3 met), § Acceptance Criteria (3 / 4 met). The single FAIL row
is the inherited runner blocker (Verification 3 / Exit Criterion 1);
all other M5 acceptance criteria are honestly met.

## Status

`CP-P05-END.md` records `status: FAIL`. Single remediation surface
(see § Recommended remediation step 1):
wire `compose_run_id` into `commands.py:1418`.
