# CLOSEOUT — TASK-RF-20260325-cli-tdd

Closed: 2026-05-17 — status `done-cli-layer` reflects the scope actually
shipped. CLI surface is fully delivered, tested, and consumed by
downstream tasks; deeper pipeline-layer integration remains open.

## What landed

- CLI flags: `--input-type`, `--tdd-file`
- `RoadmapConfig` / `TasklistValidateConfig` fields
- `build_extract_prompt_tdd` (14 sections)
- Executor branching
- Generalized fidelity prompt
- Gate compatibility docs
- 11 new pytest tests pass, 4791 regression tests pass, backward
  compat confirmed
- 10 files modified across `cli/roadmap/`, `cli/tasklist/`, gates.py docs

See `phase-outputs/reports/final-integration-report.md`.

## Residual gaps verified open as of 2026-05-17 (code-checked)

- **C-1** — `src/superclaude/cli/roadmap/semantic_layer.py` has no
  `input_type` / TDD awareness in the active pipeline.
- **C-2** — `src/superclaude/cli/roadmap/structural_checkers.py:474-491`
  still references `spec_file_paths` exclusively (no TDD-format
  assumptions accommodation).
- **I-1, I-5, B-1** — DEVIATION_ANALYSIS_GATE redesign untouched on
  master.
- Deferred: `spec_source` aliasing, `build_generate_prompt` TDD
  awareness, `build_test_strategy_prompt` TDD enrichment.

## Downstream consumption

CLI surface shipped here was exercised E2E by `TASK-E2E-20260326-tdd-pipeline`
(Done) and follow-on `TASK-RF-20260326-e2e-modified` (Done). The deeper
layer gaps did not block those E2E runs.

## Follow-up

File a new RF task if/when full TDD pipeline parity (deep semantic
layer + structural checkers + DEVIATION_ANALYSIS_GATE) is prioritized.
Suggested name: `TASK-RF-YYYYMMDD-tdd-pipeline-deep-layer`.
