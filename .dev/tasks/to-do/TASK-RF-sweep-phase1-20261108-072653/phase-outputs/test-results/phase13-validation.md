# Phase 13 validation (item 13.8)

Run 2026-11-12 after items 13.1 to 13.7. Each block: the command, its exit code, the last 30 lines of output and one PASS or FAIL line.

## Check 1 pytest tests/core tests/commands tests/recommend tests/skills

Command: `uv run pytest tests/core tests/commands tests/recommend tests/skills -v`
```text
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=no-snapshot] PASSED [ 98%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=batch] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=head-moved] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=head-moved] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=head-moved] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=budget] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=advice-rejected] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=advice-rejected] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=dispute] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=dispute] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=no-runner-up] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=brief-invalid] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=no-evidence] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=no-evidence] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=no-evidence] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=2 reason=operator-review] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=3 reason=operator-review] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=4 reason=operator-review] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_every_halt_reason_line_parses_and_archives[T1: halt review=5 reason=operator-review] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_malformed_halt_reason_lines_are_rejected[T1: halt reason=no-evidence] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_malformed_halt_reason_lines_are_rejected[T1: halt review=6 reason=batch] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_issues_then_shifted_final_archives_then_already_archived PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_symlinked_retries_directory_is_rejected_before_any_move[True] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_symlinked_retries_directory_is_rejected_before_any_move[False] PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_symlinked_brief_file_is_rejected PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_verdict_regex_matches_notes_example_line_with_exact_files PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_field_after_files_is_swallowed_into_files PASSED [ 99%]
tests/skills/test_workflow_archive.py::test_compliant_complete_with_notes_token_keeps_print_state_files PASSED [100%]

============================ 2641 passed in 55.74s =============================
(exit 0)
```
Check 1 pytest tests/core tests/commands tests/recommend tests/skills: PASS (exit 0)

## Check 2 cmp guide and plugin copy

Command: `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
```text

(exit 0)
```
Check 2 cmp guide and plugin copy: PASS (exit 0)

## Check 3 ruff check

Command: `uv run ruff check tests/core/test_how_we_work_routing_table.py`
```text
All checks passed!
(exit 0)
```
Check 3 ruff check: PASS (exit 0)

## Check 4 ruff format --check

Command: `uv run ruff format --check tests/core/test_how_we_work_routing_table.py`
```text
1 file already formatted
(exit 0)
```
Check 4 ruff format --check: PASS (exit 0)

