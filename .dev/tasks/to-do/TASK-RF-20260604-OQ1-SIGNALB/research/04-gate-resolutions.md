# Research: Gate Resolutions (gap-fill)

**Topic type:** Gate-finding resolution
**Status:** Complete
**Date:** 2026-06-04

Resolves the rf-qa research-gate findings. The load-bearing correctness point (genuine RED→GREEN) was
VERIFIED PASS by rf-qa; the 3 findings are hygiene/coverage and do not change the built task.

## R1 — Genuine RED→GREEN transcript fix (VERIFIED, carry into the build)

rf-qa CONFIRMED researcher 2's key correction: the existing `test_resume_pass_recovered_counts_as_completed`
uses `PASS_TRANSCRIPT` for T03.01, which `_classify_transcript` scores as `TaskStatus.PASS` — so a naive
`assert report.validated_last is True` would pass VACUOUSLY (Signal B already True on a PASS transcript).
For a genuine RED→GREEN, the Opt-2a test MUST change T03.01's transcript to a RECOVERED shape that
`_classify_transcript` scores as `FAIL_RECOVERABLE` (non-zero/error envelope). Then:
- Pre-Opt-2a: `signal_b_pass = (FAIL_RECOVERABLE is TaskStatus.PASS)` = False → `validated_last` False → RED.
- Post-Opt-2a: PASS_RECOVERED exemption → `signal_b_pass = True` → `validated_last` True → GREEN.
The builder MUST encode this transcript change as part of the test item (not just add the assertion).

## R2 — models.py facts (closes finding #3; VERIFIED on origin/master)

- `BoundaryTask.derived_status: TaskStatus | None = None  # Signal B` (resume/models.py:49). The
  transparency assignment `lc.derived_status = TaskStatus.PASS_RECOVERED` for the exempted case is
  meaningful — the report surfaces `derived=` from this field (`_blocking_reasons`).
- `TaskStatus.PASS_RECOVERED = "pass_recovered"` (models.py:50); `is_success` returns
  `self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)` (models.py:57-58). No models.py EDIT is needed
  (reference only) — the Opt-2a change is confined to integrity.py + the test.

## R3 — Doc-hygiene findings (acknowledged, non-blocking)

- research/02 lacks a `## Summary` heading — the researcher returned an inline summary; substantively
  complete. Non-blocking.
- research/03 doc-claims lack [CODE-VERIFIED]/[UNVERIFIED] tags — the analyst + rf-qa independently
  re-verified the template/CLAUDE.md claims against current files; built-task correctness unaffected.
  Builder should cite `src/superclaude/templates/...` (canonical) in `template_schema_doc`.

## Net effect on the build
Carry R1 (genuine-RED transcript change) into the test item explicitly. R2/R3 are closed/acknowledged.
All else from research 01/02/03 stands.
