# D-0039 — `claude.min_version` policy spec (R1-mit)

**Task:** T02.20 (Phase 2, Roadmap R-039 / R1-mit)
**Modules:** `src/superclaude/cli/eval/config.py`, `src/superclaude/cli/eval/commands.py`
**CLI surface (re-uses):** `superclaude eval doctor [--json]`
**Status:** Implemented 2026-05-20

## Policy

R1-mit (roadmap risk register) pins the supported `claude` CLI version
range and enforces it from `eval doctor`. The version floor is recorded
as:

| Field | Value | Source |
|---|---|---|
| `min_version` | `0.5.0` | `superclaude.cli.eval.config.DEFAULT_MIN_CLAUDE_VERSION` |
| `max_version` | open-ended (no upper bound enforced at M2) | `EvalConfig` field for future override |

`max_version` is intentionally unbounded: the harness pre-commits to
forward compatibility with future `claude` releases; the field shape
(`tuple[int, int, int]`) leaves room for a future `max_claude_version`
addition without breaking callers (deferred per R1 follow-up).

Operators may override the floor by constructing
`EvalConfig(min_claude_version=(major, minor, patch))`. The doctor
module **does not embed a hard-coded constant** — the
`test_doctor_module_does_not_define_hardcoded_floor_constant` guard
asserts the constant `_MIN_CLAUDE_VERSION` is absent.

## Single source of truth

```
                  +-------------------------------------+
                  | superclaude.cli.eval.config         |
                  |   DEFAULT_MIN_CLAUDE_VERSION = (0,5,0)
                  |   EvalConfig.min_claude_version     |
                  +-----------------+-------------------+
                                    |
                                    v
       +----------------------------+----------------------------+
       |          _check_claude_version(config=...)              |
       |  - probe()  ->  "claude X.Y.Z"                          |
       |  - parse via _VERSION_RE                                |
       |  - compare parsed >= config.min_claude_version          |
       |  - CapabilityStatus(name="claude.min_version", hard)    |
       +----------------------------+----------------------------+
                                    |
                                    v
                      +-------------+-------------+
                      | build_doctor_report(...)  |
                      |   forwards config kwarg   |
                      +-------------+-------------+
                                    |
                                    v
                       eval doctor / --json payload
                       (exit 2 on below-floor stub)
```

## Surface changes

### `src/superclaude/cli/eval/config.py`

* New module-level constant `DEFAULT_MIN_CLAUDE_VERSION = (0, 5, 0)`.
* New `EvalConfig` field
  `min_claude_version: tuple[int, int, int] = DEFAULT_MIN_CLAUDE_VERSION`.
* `__all__` extended with `"DEFAULT_MIN_CLAUDE_VERSION"`.

### `src/superclaude/cli/eval/commands.py`

* `_MIN_CLAUDE_VERSION` removed (the doctor module no longer embeds a
  duplicate of the policy).
* `_check_claude_version(probe=None, min_version=None, *, config=None)`
  now sources its floor from `config.min_claude_version` when
  `min_version` is not supplied; falls back to a default-constructed
  `EvalConfig`. The legacy explicit-kwarg seam is preserved for tests
  that need to override the floor without constructing a config.
* `build_doctor_report(..., config: EvalConfig | None = None)`
  forwards the config to `_check_claude_version`. Existing callers
  remain backwards-compatible (`config=None` → default `EvalConfig`).

## Acceptance criteria → implementation map

| AC bullet (T02.20) | Implementation site |
|---|---|
| `_check_claude_version()` rejects claude installations below 0.5.0 with exit 2. | `_check_claude_version` returns `passed=False, failure_mode="hard"`; `doctor` Click handler emits `HARD_FAIL_EXIT_CODE` (= 2). Covered by `test_cli_doctor_exits_two_when_stub_reports_0_4_0`. |
| A reference fixture stubbing `claude --version` at `0.4.0` fails the doctor check. | `tests/cli/eval/test_doctor_version.py::test_check_claude_version_rejects_0_4_0_stub` + `test_cli_doctor_exits_two_when_stub_reports_0_4_0`. |
| Version floor is sourced from `EvalConfig` (not hard-coded in doctor). | `EvalConfig.min_claude_version` (config.py); `_check_claude_version(config=…)` (commands.py). Guard: `test_doctor_module_does_not_define_hardcoded_floor_constant`. |
| `artifacts/D-0039/spec.md` records the version policy. | This file. |

## Failure-mode matrix

| Probe output | Parsed | Floor | `passed` | `detail` |
|---|---|---|---|---|
| `"claude 0.5.0"` | `(0,5,0)` | `(0,5,0)` | True | `claude 0.5.0` |
| `"claude 0.5.7 (build 12)"` | `(0,5,7)` | `(0,5,0)` | True | `claude 0.5.7` |
| `"claude 0.4.0"` | `(0,4,0)` | `(0,5,0)` | False | `claude 0.4.0 < required 0.5.0` |
| `"unrecognised banner"` | None | `(0,5,0)` | False | `could not parse version from 'unrecognised banner'` |
| `None` (no probe) | n/a | `(0,5,0)` | False | `claude --version not callable` |
| probe raises | n/a | `(0,5,0)` | False | `version probe raised <ExcClass>: <msg>` |

## Out of scope for T02.20

- Upper-bound enforcement (`max_claude_version`): the policy is
  unbounded at M2; the field shape (`tuple[int, int, int]`) leaves room
  for a sibling field without breaking callers.
- Operator-facing `--min-claude-version=` CLI flag: deferred. The
  `EvalConfig` constructor path is the only override seam at M2.
- Real subprocess probe variance (rare `claude --version` banner
  changes): tracked via R1 follow-up; the `_VERSION_RE` regex
  (`r"(\d+)\.(\d+)\.(\d+)"`) handles all banner variants observed in
  M1/M2 dev hosts.
