# T02.20 — Evidence summary

**Task:** Pin claude version range in eval doctor (R1-mit)
**Phase:** 2 (cliEval) · **Roadmap:** R-039 · **Deliverable:** D-0039
**Date:** 2026-05-20
**Status:** PASS

## Acceptance criteria (verbatim from phase-2-tasklist)

1. **Function `_check_claude_version()` rejects claude installations below 0.5.0 with exit 2.**
   - Verified by `tests/cli/eval/test_doctor_version.py::test_cli_doctor_exits_two_when_stub_reports_0_4_0`.
2. **A reference fixture stubbing `claude --version` at 0.4.0 fails the doctor check.**
   - `test_check_claude_version_rejects_0_4_0_stub` stubs the probe with `"claude 0.4.0"` and asserts `passed=False`, `"< required 0.5.0"` in detail.
3. **Version floor is sourced from `EvalConfig` (not hard-coded in doctor).**
   - `EvalConfig.min_claude_version` (new field, default `(0,5,0)`) is the sole source.
   - Guard: `test_doctor_module_does_not_define_hardcoded_floor_constant` asserts `commands._MIN_CLAUDE_VERSION` is absent.
   - Behaviour: `test_check_claude_version_floor_sourced_from_eval_config` raises floor via `EvalConfig(min_claude_version=(0,9,0))` and confirms the boundary shifts.
4. **`TASKLIST_ROOT/artifacts/D-0039/spec.md` records the version policy.**
   - Spec written at `.dev/releases/current/cliEval/artifacts/D-0039/spec.md`; companion `notes.md` + `evidence.md` complete the artifact triple.

## Test results

```
$ uv run pytest tests/cli/eval/test_doctor_version.py tests/cli/eval/test_doctor.py tests/cli/eval/test_config.py -v
…
============================== 47 passed in 0.15s ==============================
```

Full log: `pytest.log`.

## Files touched

| Path | Change |
|---|---|
| `src/superclaude/cli/eval/config.py` | + `DEFAULT_MIN_CLAUDE_VERSION`, + `EvalConfig.min_claude_version` |
| `src/superclaude/cli/eval/commands.py` | - `_MIN_CLAUDE_VERSION`, `_check_claude_version` sources floor from `EvalConfig`, `build_doctor_report` forwards `config=` |
| `tests/cli/eval/test_config.py` | required-field set updated to include `min_claude_version` |
| `tests/cli/eval/test_doctor_version.py` | new module (13 tests, all green) |
| `.dev/releases/current/cliEval/artifacts/D-0039/{spec,notes,evidence}.md` | new artifact triple |
| `.dev/releases/current/cliEval/evidence/T02.20/{pytest.log,summary.md}` | new evidence |

## Validation (manual)

> "Manual check: stub claude binary at 0.4.0 and run doctor; confirm exit 2."

Performed via Click `CliRunner` inside `test_cli_doctor_exits_two_when_stub_reports_0_4_0`, which monkeypatches `commands._default_claude_version_probe` to return `"claude 0.4.0"` and asserts `result.exit_code == HARD_FAIL_EXIT_CODE` (= 2) plus the HARD-failure artifact line on stderr.

## Notes

- R1-mit policy: `min_version 0.5.0` recorded, `max_version` left unbounded at M2 (documented in `spec.md` "Out of scope"). A future task can add `EvalConfig.max_claude_version` without touching the floor contract.
- Backwards compatibility: existing callers of `build_doctor_report()` continue to work unchanged because `config=None` → default-constructed `EvalConfig` with the 0.5.0 floor.
