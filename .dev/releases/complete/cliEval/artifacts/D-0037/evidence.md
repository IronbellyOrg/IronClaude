# D-0037 — Evidence (Task T02.17)

## Implementation

* `src/superclaude/cli/eval/pty_stream.py` — `PtyStream` class with
  ANSI-aware line buffer, `PtyTimeout` / `PtyStreamError` exception
  hierarchy, `ANSI_ESCAPE_RE` exported for downstream re-use.
* `src/superclaude/cli/eval/__init__.py` — re-exports
  `ANSI_ESCAPE_RE`, `PtyStream`, `PtyStreamError`, `PtyTimeout`
  alongside the existing PtyDriver surface.

## Tests

`tests/cli/eval/test_pty_stream.py` — 30 tests grouped by acceptance bullet:

| Group                             | Tests                                                                                                                                                                                                                                                                                                       |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ANSI regex surface                | `test_ansi_regex_strips_csi_sgr_color_codes`, `test_ansi_regex_strips_cursor_moves`, `test_ansi_regex_strips_osc_title_set_bel_terminated`, `test_ansi_regex_strips_osc_title_set_st_terminated`, `test_ansi_regex_strips_c1_singleton`                                                                       |
| ANSI strip via PtyStream          | `test_strips_ansi_csi_sgr`, `test_strips_osc_title_set`, `test_can_disable_ansi_stripping`                                                                                                                                                                                                                    |
| Line buffering                    | `test_buffers_partial_lines`, `test_yields_multiple_lines_in_order`, `test_keep_newline_preserves_terminator`, `test_strips_crlf_by_default`, `test_drain_returns_unterminated_remainder`                                                                                                                     |
| Timeout semantics                 | `test_raises_pty_timeout_when_no_line_arrives`, `test_pty_timeout_is_pty_stream_error`, `test_per_call_timeout_overrides_default`, `test_timeout_reports_pending_buffer_size`, `test_slow_stream_eventually_returns_line`                                                                                     |
| Iteration protocol                | `test_iteration_yields_all_clean_lines`, `test_iteration_after_close_stops_immediately`, `test_iteration_propagates_pty_timeout`                                                                                                                                                                              |
| Constructor + source coercion     | `test_constructor_rejects_non_positive_timeout`, `test_constructor_rejects_non_positive_poll_interval`, `test_constructor_rejects_bad_source`, `test_accepts_object_with_read_stdout_method`, `test_read_line_rejects_zero_timeout`, `test_read_after_close_raises`, `test_context_manager_closes`            |
| ANSI fixture run-to-run stability | `test_identical_plain_text_across_runs`                                                                                                                                                                                                                                                                       |
| End-to-end PtyDriver smoke        | `test_end_to_end_with_real_pty_driver`                                                                                                                                                                                                                                                                        |

## Verification command

```
uv run pytest tests/cli/eval/test_pty_stream.py -v
```

## Verification result

* Captured log: `evidence/T02.17/pytest-T02.17.log`
* Summary: **30 passed in 1.35s** (Python 3.12.12 / pytest 9.0.3 /
  pexpect 4.9.0). End-to-end smoke against a real PTY-driven Python
  subprocess passed alongside the in-process scripted-reader tests.

## Acceptance bullet → evidence link

| T02.17 acceptance bullet                                                                                  | Pinned test(s)                                                                                                                              |
|---|---|
| `PtyStream` strips ANSI escape sequences from byte chunks and yields line-buffered output.                | `test_strips_ansi_csi_sgr`, `test_strips_osc_title_set`, `test_buffers_partial_lines`, `test_yields_multiple_lines_in_order`, `test_end_to_end_with_real_pty_driver` |
| `PtyTimeout` is raised when no new line arrives within the configured timeout.                            | `test_raises_pty_timeout_when_no_line_arrives`, `test_per_call_timeout_overrides_default`, `test_iteration_propagates_pty_timeout`           |
| ANSI test fixture is normalized to identical plain-text output across runs.                               | `test_identical_plain_text_across_runs` (3-iteration byte-identical assertion), `test_iteration_yields_all_clean_lines`                       |
| `TASKLIST_ROOT/artifacts/D-0037/spec.md` documents the API.                                               | This deliverable's `spec.md` + `notes.md`.                                                                                                  |

## Cross-test sanity check

Full `tests/cli/eval/` run after the PtyStream landing:

```
uv run pytest tests/cli/eval/ -q --no-header
============================= 584 passed in 7.99s ==============================
```

No pre-existing tests were disturbed; the 30 PtyStream tests are purely
net-new. PtyDriver's 21 tests remained green, confirming the new module
did not touch the upstream chunk-producer contract.

## Validation (per phase-2-tasklist.md T02.17)

* **Manual check** — feed an ANSI-laden byte stream and confirm clean
  line output: covered by `test_strips_ansi_csi_sgr`,
  `test_strips_osc_title_set`, `test_identical_plain_text_across_runs`
  (3 iterations through `ANSI_FIXTURE` produce identical
  `EXPECTED_LINES`).
* **Evidence** — linkable artifact produced:
  `.dev/releases/current/cliEval/evidence/T02.17/pytest-T02.17.log`
  (30 passed in 1.35 s).
