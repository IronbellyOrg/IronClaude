# BUILD REQUEST: cliEval-P3 — Orchestrator + Runner + Reporter + `eval run`

## What This Is

Phase 3 of the **cliEval release**. The heaviest phase. Builds the actual execution engine: the parallel scheduler (`orchestrator.py`), the per-eval lifecycle driver (`runner.py`), and the result-aggregation reporter (`reporter.py`). Adds the `eval run --suite SUITE` subcommand.

## Why It Matters

This phase is where the harness becomes **alive**: a real Claude Code subprocess is spawned, a real eval is driven end-to-end, real hook side-effects are observed, real JSONL telemetry is asserted, and a real result artifact is written to `.dev/eval-runs/<ISO>/<run-id>/`.

The smoke-test acceptance for this phase REQUIRES a working 1-eval end-to-end run (a stub minimal eval, not E1-E15 yet) — this is the proof that the entire harness architecture is viable.

## Inputs (read before starting)

- **Design spec:** `.dev/releases/current/cliEval/design-spec.md` — read §2 (architecture), §6 (lifecycle sequence), §9 (reporting), §10 (integration), §12 (concurrency model).
- **Decisions log:** `.dev/releases/current/cliEval/decisions.md` — read all 4 decisions; D-3 in particular for the HOME isolation composition.
- **Phase 1 + 2 outputs (DEPENDENCIES, must be MERGED):** `pty/`, `isolation.py`, `capability_gates.py`, `models.py`, `loader.py`, `expect.py`. Both P1 and P2 must have landed before P3 starts.
- **Existing parallel pattern to mirror:** `src/superclaude/cli/prd/executor.py:774-802` `ThreadPoolExecutor` + `as_completed`. Use this pattern, NOT `execution/parallel.py`.
- **Existing report shape to mirror:** `src/superclaude/cli/sprint/executor.py:190-335` `AggregatedPhaseReport`. Copy the shape (`to_yaml`, `to_markdown`); swap "phase" terminology for "eval".
- **Existing subprocess scaffolding:** `src/superclaude/cli/pipeline/process.py:24-150` `ClaudeProcess` — can be reused or wrapped by `runner.py`'s PtyDriver invocation.

## Scope (what THIS task builds)

### Files to create

1. `src/superclaude/cli/eval/orchestrator.py` — `RunOrchestrator` class; `ThreadPoolExecutor(max_workers=N)`; schedules `EvalSpec` → submits `runner.run()`; collects via `as_completed`; per-eval timeout; failure aggregation; signal handling (SIGINT/SIGTERM cleanup)
2. `src/superclaude/cli/eval/runner.py` — `EvalRunner` class; per-eval lifecycle: build HomeIsolation → spawn PtyDriver → inject prompts → wait for idle → apply Expect.* → capture TTY → teardown
3. `src/superclaude/cli/eval/reporter.py` — `AggregatedRunReport` dataclass with `to_markdown()`, `to_json()`, `to_junit()` methods; writes artifact tree under `.dev/eval-runs/<ISO>/<run-id>/`
4. Extend `src/superclaude/cli/eval/commands.py` — add `eval run` subcommand with flags `--suite`, `--parallel`, `--eval`, `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult`, `--json`, `--verbose` (per design-spec §4)
5. `src/superclaude/cli/eval/suites/stub.yaml` — minimal 1-eval test manifest for smoke testing (eval that does NOT need MCP; e.g., asserts that `superclaude install` deploys 9 hooks)
6. `tests/cli/test_eval/test_orchestrator.py` — scheduling logic (mocked runner), `as_completed` iteration, timeout enforcement, SIGINT handling
7. `tests/cli/test_eval/test_runner.py` — mocked PtyDriver, real HomeIsolation; verify the lifecycle order (build → spawn → inject → wait → assert → teardown)
8. `tests/cli/test_eval/test_reporter.py` — to_markdown / to_json / to_junit shape; artifact tree layout; failure-detail capture
9. `tests/cli/test_eval/test_eval_run_smoke.py` — REAL end-to-end test: invoke `eval run --suite stub` against an actual Claude Code subprocess; assert PASS for the 1 stub eval; verify artifact tree exists

### Acceptance criteria (per design-spec §6, §9, §12)

- **AC-P3.1:** `uv run superclaude eval run --suite stub` spawns a real Claude Code subprocess in an isolated HOME, runs the 1 stub eval, writes artifacts to `.dev/eval-runs/<ISO>/<run-id>/`, exits 0 on PASS.
- **AC-P3.2:** The artifact tree contains: `summary.md`, `summary.json`, `manifest.snapshot.yaml`, `evals/<eval-id>/{result.json, stdout.log, stderr.log, expect-trace.md}`. On failure: also `evals/<eval-id>/home/` (preserved for post-mortem).
- **AC-P3.3:** `--parallel 8` runs up to 8 evals concurrently with no HOME-directory collision, no JSONL corruption, no shared-state race (verified with the stub eval parameterized 8 ways).
- **AC-P3.4:** `--eval E1,E2` filters to a subset; running just stub passes filter when ID matches.
- **AC-P3.5:** `--no-mcp` skips evals declaring `requires: [mcp_server.*]` with status SKIPPED and reason in result.
- **AC-P3.6:** Per-eval timeout fires correctly: if a stub eval sleeps >timeout_sec, the runner kills the PtyDriver subprocess + marks result TIMEOUT.
- **AC-P3.7:** SIGINT during a run cancels in-flight evals, marks them INTERRUPTED, writes a partial summary, exits 3.
- **AC-P3.8:** Failure mode: a deliberately-broken stub eval (assertion guaranteed to fail) produces a FAIL result with rich evidence in `expect-trace.md`.
- **AC-P3.9:** `summary.md` is human-readable with a table; `summary.json` is machine-readable and valid JSON; `junit.xml` (when `--junit` passed) validates against JUnit DTD.
- **AC-P3.10:** All new tests pass.
- **AC-P3.11:** `make verify-sync` still EXIT=0.
- **AC-P3.12:** `test_eval_run_smoke.py` is gated with `pytestmark = [skipif(not _HAS_CLAUDE_BINARY)]` so it skips cleanly in environments without the `claude` binary.

### Out of scope for THIS task

- The 15 real evals (Wave 2)
- Wiring `eval_group` into `cli/main.py` (P4)
- Makefile target / .gitignore updates (P4)
- CI integration

## Naming convention

- Task file path: `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P3-orchestrator-runner-reporter/TASK-RF-20260518-cliEval-P3-orchestrator-runner-reporter.md`
- Branch: `feat/cliEval-P3-orchestrator-runner-reporter`
- PR title: `feat(eval): cliEval P3 — orchestrator + runner + reporter + eval run subcommand`

## Open questions for the executor

- Q1: For `eval run` invocation pattern — should we use Click's `result_callback` to write the final summary post-run, or inline the writing in the command function? Recommendation: inline; cleaner traceback when reporting fails.
- Q2: How should `--verbose` output stream live? Per-eval lines to terminal? Or per-eval progress bar? Recommendation: rich's Progress with per-eval bars if `rich` is already a dep; else simple per-eval status lines.
- Q3: The stub eval needs to be SIMPLE — what's the minimum useful smoke test? Recommendation: "spawn claude, send `/help`, confirm output contains `Available Commands`, exit." No state assertions, no MCP, no hooks-specific logic. Just proves the harness moves bits end-to-end.
- Q4: Should the per-eval `home/` directory be deleted SYNCHRONOUSLY in the runner thread or DEFERRED to a background thread post-run? Recommendation: sync per-eval (cleaner failure mode).

## Dependencies

- **Depends on:** P1 (pty/, isolation, gates) AND P2 (models, loader, expect) — both must be merged.
- **Blocks:** P4 (CLI wiring needs `eval run` to exist), Wave 2 (eval bodies depend on the harness being callable).

## Estimated LOC: ~440

(Per design-spec §17: orchestrator.py ~120 LOC, runner.py ~150 LOC, reporter.py ~120 LOC, commands.py extensions ~50 LOC, stub.yaml ~20 LOC, tests ~250 LOC across 4 files.)
