# D-0013 — Prompt Assertion Test Evidence

## Task: T04.02

## Tests Added

**File:** `tests/sprint/test_process.py`
**Class:** `TestClaudeProcess` (appended 7 new test methods)

### Test Methods

| Test | Assertion | SC/FR Ref |
|---|---|---|
| `test_build_prompt_result_file_section_present` | `"## Result File" in prompt` | SC-013 |
| `test_build_prompt_result_file_after_important` | `prompt.rindex("## Result File") > prompt.rindex("## Important")` | SC-013 |
| `test_build_prompt_result_file_path_uses_as_posix` | `config.result_file(phase).as_posix() in prompt` | FR-006 |
| `test_build_prompt_result_file_continue_instruction` | `"EXIT_RECOMMENDATION: CONTINUE" in prompt` | FR-006 |
| `test_build_prompt_result_file_halt_instruction` | `"EXIT_RECOMMENDATION: HALT" in prompt` | STRICT-tier |
| `test_build_prompt_existing_sections_not_displaced` | Section ordering: Sprint Context < Execution Rules < Scope Boundary < Important < Result File | SC-013 |
| `test_build_prompt_result_file_is_last_h2_section` | No `^##` heading follows `## Result File` in prompt | SC-013 |

## Test Execution Output

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.3

tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_result_file_section_present PASSED
tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_result_file_after_important PASSED
tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_result_file_path_uses_as_posix PASSED
tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_result_file_continue_instruction PASSED
tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_result_file_halt_instruction PASSED
tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_existing_sections_not_displaced PASSED
tests/sprint/test_process.py::TestClaudeProcess::test_build_prompt_result_file_is_last_h2_section PASSED

41 passed in 0.13s
```

## Full Suite Regression Check

```
uv run pytest tests/sprint/ -v
713 passed, 20 warnings in 37.48s
```

**Exit code: 0. Zero regressions.**

## OQ-001 Verification

Attribute name used in `build_prompt()` for phase access: `self.phase` (confirmed at D-0002,
`process.py:105`). Tests use `config.phases[0]` which is a `Phase` object — consistent with
`ClaudeProcess.__init__` signature.
