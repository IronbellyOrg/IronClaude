# D-0036 — Evidence (Task T02.16)

## Implementation

* `src/superclaude/cli/eval/pty_driver.py` — `PtyDriver` class, 5-method
  contract, two custom exception types, prompt-ready default pattern,
  vendored-pexpect-first import.
* `src/superclaude/cli/eval/__init__.py` — re-exports
  `PtyDriver`, `PtyDriverError`, `PtyDriverTimeout`, `PtyDriverEOF`,
  `PtyDriverNotStarted`, `DEFAULT_PROMPT_READY_PATTERN`.
* `pyproject.toml` — `pexpect>=4.9` added to `[project] dependencies`
  (NFR-MAINT1 floor).

## Tests

* `tests/cli/eval/test_pty_driver.py` — 21 tests:

| Group                          | Tests                                                                                                                              |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Surface contract               | `test_method_surface_matches_comp_007_contract`, `test_constructor_rejects_empty_command_list`, `test_constructor_rejects_non_positive_timeout`, `test_interaction_before_spawn_raises_not_started` |
| Prompt + I/O round-trip        | `test_expect_prompt_ready_returns_before_timeout_against_stub`, `test_inject_prompt_then_read_stdout_round_trips_text`, `test_write_stdin_does_not_append_newline`, `test_read_stdout_returns_empty_string_when_idle` |
| Exit-code capture              | `test_wait_exit_captures_exit_code_from_stub[0,1,42,124]` (parametrized × 4), `test_wait_exit_reports_signal_termination_as_negative`, `test_wait_exit_idempotent_after_clean_exit` |
| Failure modes                  | `test_expect_prompt_ready_raises_timeout_when_pattern_missing`, `test_expect_prompt_ready_raises_eof_when_child_dies_first`, `test_wait_exit_raises_timeout_when_child_still_alive` |
| Lifecycle hygiene              | `test_double_spawn_while_alive_raises`, `test_pid_returns_int_after_spawn`, `test_inject_prompt_rejects_bytes` |
| Real-binary smoketest          | `test_real_claude_help_smoketest` — opt-in (skipped when `claude` binary absent on host)                                          |

## Verification command

```
uv run pytest tests/cli/eval/test_pty_driver.py -v
```

## Verification result

* Captured log: `evidence/T02.16/pytest-T02.16.log`
* Summary: **21 passed in 5.24s** (Python 3.12.12 / pytest 9.0.3 /
  pexpect 4.9.0 / `claude` 0.5.0 present on dev host so the opt-in
  smoketest ran and passed).

## Acceptance bullet → evidence link

| T02.16 acceptance bullet                                                                                       | Pinned test(s)                                                                                              |
|---|---|
| `PtyDriver` exposes the 5 methods named in COMP-007.                                                           | `test_method_surface_matches_comp_007_contract`                                                              |
| A unit test spawns a real `claude --help` (or test-stub) subprocess via PTY and `expect_prompt_ready()` returns within the timeout. | `test_expect_prompt_ready_returns_before_timeout_against_stub` (always) + `test_real_claude_help_smoketest` (opt-in) |
| `wait_exit()` captures and returns the subprocess exit code accurately.                                        | `test_wait_exit_captures_exit_code_from_stub[0,1,42,124]` + `test_wait_exit_reports_signal_termination_as_negative` |
| `TASKLIST_ROOT/artifacts/D-0036/spec.md` documents the method contract and FR-G1 satisfaction.                 | This deliverable's `spec.md` + `notes.md`.                                                                   |

## Cross-test sanity check

Full `tests/cli/eval/` run after the PtyDriver landing:

```
uv run pytest tests/cli/eval/ -v --no-header -q
============================= 554 passed in 6.71s ==============================
```

No pre-existing test was disturbed; the additions are purely net-new.
