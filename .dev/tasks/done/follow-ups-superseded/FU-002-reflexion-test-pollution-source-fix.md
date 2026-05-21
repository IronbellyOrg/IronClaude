---
id: "FU-002-reflexion-test-pollution-source-fix"
title: "Reflexion test fixtures pollute docs/mistakes/ and docs/memory/solutions_learned.jsonl"
status: "🟡 To Do"
type: "🐛 Bug"
priority: "🔼 High"
created_date: "2026-05-18"
parent_task: "TASK-RF-20260518-181333"
tags:
- "follow-up"
- "root-cause-fix"
---

## Background

TASK-RF-20260518-181333 Phase 3 cleaned up `docs/mistakes/test_database_connection-2026-05-18.md`, `test_reflexion_with_real_exception-2026-05-18.md`, `unknown-2026-05-18.md`, and reverted 16 simulated entries in `docs/memory/solutions_learned.jsonl`. QA Phase 3 then detected these files were RE-CREATED at mtime 20:47:59 by the running pytest suite (`uv run pytest tests/`).

## Symptom

Every `uv run pytest tests/` run re-creates polluted files under `docs/mistakes/` matching `test_*-<today>.md` and appends entries to `docs/memory/solutions_learned.jsonl`. These pollute the repo's persistent knowledge-base files with synthetic test-fixture data (simulated `ImportError`, `TypeError`, `ZeroDivisionError`, `FileNotFoundError`). The cleanup work in Phase 3 is undone on every test run.

## Root Cause Hypothesis

The reflexion test fixtures in `src/superclaude/pm_agent/reflexion.py` (or the test files themselves under `tests/pm_agent/`) call the real reflexion writer with default paths (`docs/mistakes/` and `docs/memory/solutions_learned.jsonl`) instead of injecting a temp-dir override via `tmp_path` fixture or monkeypatching the writer's output destination. The writer has no test-mode isolation; tests run against production output paths.

## Suggested Fix Direction

- Locate the reflexion writer's output-path resolution in `src/superclaude/pm_agent/reflexion.py`.
- Introduce a `REFLEXION_OUTPUT_DIR` env var or constructor parameter (`output_dir`, `mistakes_dir`, `solutions_path`).
- Update test fixtures under `tests/pm_agent/` to monkeypatch the writer (or pass `tmp_path`) so reflexion runs in tests write to ephemeral dirs only.
- Add a regression test that asserts no new files appear in `docs/mistakes/` and `docs/memory/solutions_learned.jsonl` is unchanged after running the reflexion test suite.

## Acceptance Criteria

- After `uv run pytest tests/`, `git status --porcelain` shows no new files in `docs/mistakes/` or modifications to `docs/memory/solutions_learned.jsonl`.
- Reflexion functionality preserved in production (default path still resolves to `docs/mistakes/` and `docs/memory/solutions_learned.jsonl`).
- Tests use a `tmp_path`-overridden writer (or env-var override).
- A regression test guards against future pollution.

## References

- Source: `src/superclaude/pm_agent/reflexion.py`
- Tests: `tests/pm_agent/` (specifically reflexion-tagged tests)
- Phase 3 QA report: `.dev/tasks/to-do/TASK-RF-20260518-181333/qa/qa-phase-3-report.md`
- Parent task: `TASK-RF-20260518-181333`
