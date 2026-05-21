# D-0039 — Evidence index

Task: **T02.20 — Pin claude version range in eval doctor (R1-mit)**
Status: **PASS** (2026-05-20)

## Pytest

- `.dev/releases/current/cliEval/evidence/T02.20/pytest.log` —
  47 passed (test_config.py + test_doctor.py + test_doctor_version.py).

Highlight rows:

| Test | Verifies AC bullet |
|---|---|
| `test_default_min_claude_version_is_0_5_0` | min_version 0.5.0 recorded |
| `test_eval_config_exposes_min_claude_version_field` | floor sourced from EvalConfig |
| `test_check_claude_version_rejects_0_4_0_stub` | 0.4.0 stub fails the check |
| `test_cli_doctor_exits_two_when_stub_reports_0_4_0` | doctor exits 2 on below-floor stub |
| `test_doctor_module_does_not_define_hardcoded_floor_constant` | no duplicate constant in doctor |
| `test_check_claude_version_floor_sourced_from_eval_config` | strict EvalConfig changes the floor |
| `test_check_claude_version_lowered_floor_lets_old_release_pass` | permissive EvalConfig accepts older builds |
| `test_build_doctor_report_uses_config_floor` | build_doctor_report wires the config kwarg |
| `test_build_doctor_report_default_config_uses_0_5_0` | default config keeps 0.5.0 floor |

## Files touched

- `src/superclaude/cli/eval/config.py` — added
  `DEFAULT_MIN_CLAUDE_VERSION` + `EvalConfig.min_claude_version`.
- `src/superclaude/cli/eval/commands.py` — `_check_claude_version`
  sources floor from `EvalConfig`; `build_doctor_report` forwards a
  `config=` kwarg; legacy hard-coded `_MIN_CLAUDE_VERSION` removed.
- `tests/cli/eval/test_config.py` — updated required-field set.
- `tests/cli/eval/test_doctor_version.py` — new module (13 tests).

## Spec

- `artifacts/D-0039/spec.md` — version policy + surface changes.
- `artifacts/D-0039/notes.md` — design rationale.
