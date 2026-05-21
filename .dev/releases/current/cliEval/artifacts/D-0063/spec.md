# D-0063 — TEST-006 PTY lifecycle integration tests + FR-G1 ban-import rule

**Task:** T03.22 (Phase 3, Roadmap TEST-006 / R-063)
**Modules:**
- `tests/cli/eval/test_pty_lifecycle.py` (new)
- `tests/cli/eval/test_ban_import_rule.py` (new)
- `pyproject.toml` (`[tool.ruff.lint.flake8-tidy-imports.banned-api]` — wired in T02.19; this task pins it via tests)
**Status:** Implemented 2026-05-20

## Scope

T03.22 lands the first-class FR-G1 enforcement test for the cliEval
harness. FR-G1 ("real-subprocess discipline") forbids any in-process
shortcut to the Claude API and requires every eval to drive the real
`claude` binary as a child process. The deliverable is two test files
plus a confirmation that the static lint rule banning `anthropic`
imports is wired:

1. **`tests/cli/eval/test_pty_lifecycle.py`** — runtime integration tests
   that exercise the FR-LC1 lifecycle end-to-end with a PtyDriver-backed
   `LifecycleExecutor`. Coverage matrix below.
2. **`tests/cli/eval/test_ban_import_rule.py`** — static-analysis
   tests asserting that `uv run ruff check src/superclaude/cli/eval/`
   exits 0 on the clean tree and non-zero when a synthetic
   `import anthropic` is injected, with the TID251 message including
   the FR-G1 remediation hint.

## Lifecycle test matrix (`test_pty_lifecycle.py`)

| # | Test | Subject | FR/COMP pinned |
|---|------|---------|----------------|
| 1 | `test_real_claude_help_spawn_and_transcript` | Real `claude --help` spawned via `PtyDriver`; transcript file holds `Usage`; exit 0; FR-G1 PASS outcome through `EvalRunner.run`. Skipped on hosts without `claude` in PATH. | FR-G1, COMP-007, COMP-004 |
| 2 | `test_lifecycle_prompt_ready_and_input_injection` | Deterministic Python stub mimicking REPL: `expect_prompt_ready` returns within timeout; `inject_prompt` round-trips text; transcript captures both banner and echo. | FR-G1, COMP-007 |
| 3 | `test_lifecycle_timeout_reaps_child` | Hanging subprocess + `default_timeout_sec=0.5` → outcome status `TIMEOUT` AND `PtyDriver.is_alive()` is `False` after the runner returns (no zombie). | FR-G1, NFR-REL1, COMP-004 |
| 4 | `test_lifecycle_transcript_persisted_end_to_end` | Stub runs to clean exit through `EvalRunner.run`; transcript file written to runner-allocated path; per-eval JSONL log written under `home_path/.eval-logs/`. | FR-G1, FR-LC1, COMP-004 |
| 5 | `test_eval_package_does_not_import_anthropic_at_runtime` | Importing every public submodule of `superclaude.cli.eval` in a fresh subprocess does NOT pull `anthropic` into `sys.modules` — guards against a dynamic-import bypass of the static linter. | FR-G1 |

### Fixture surface

* `FakeHome` — minimal `HomeIsolation` duck-type. Surface (`setup`,
  `teardown`, `env`, `home_path`) matches the runner-class tests; the
  full `HomeIsolation` machinery is exercised by `test_isolation.py`.
* `PtyLifecycleExecutor` — `LifecycleExecutor` implementation that
  wraps `PtyDriver` for the FR-LC1 spawn/inject/observe trio. Adds a
  `cancel()` method NFR-REL1 calls on the timeout path. The executor
  captures the pre-prompt banner during `inject` (because pexpect
  consumes it from the buffer during `expect_prompt_ready`) so the
  transcript faithfully reflects what the user would have seen.

## Ban-import rule test matrix (`test_ban_import_rule.py`)

| # | Test | Subject |
|---|------|---------|
| 1 | `test_clean_tree_passes_ruff_check` | `uv run ruff check src/superclaude/cli/eval/` exits 0 on master. |
| 2 | `test_synthetic_import_anthropic_is_flagged_by_ruff` | Writing `import anthropic` under `src/superclaude/cli/eval/_probe_synth_ban_import_rule/probe.py` makes ruff exit non-zero AND mentions `TID251` AND mentions `anthropic`. |
| 3 | `test_ban_message_references_fr_g1` | The TID251 error carries the FR-G1 remediation hint from `pyproject.toml`, guarding against a TOML edit that drops the `msg` field. |

The probe directory is removed in a fixture-scoped `finally` so every
test ends with a clean tree even if interrupted.

## Ban-import rule configuration

The rule itself lives in `pyproject.toml` under
`[tool.ruff.lint.flake8-tidy-imports.banned-api]` (wired in T02.19) and
declares three banned import paths:

```toml
"anthropic".msg                  = "FR-G1: in-process anthropic SDK imports are banned. ..."
"anthropic.AsyncAnthropic".msg   = "FR-G1: in-process anthropic SDK imports are banned. ..."
"anthropic.Anthropic".msg        = "FR-G1: in-process anthropic SDK imports are banned. ..."
```

The full remediation message in each entry points at `PtyDriver`
(`src/superclaude/cli/eval/pty_driver.py`) and `ClaudeProcessAdapter`
(`src/superclaude/cli/eval/claude_process.py`) as the only sanctioned
paths to the Claude API.

The rule is **repo-global**, not scoped to `src/superclaude/cli/eval/`
— no production code under `src/superclaude/` should ever pull the
SDK in-process, so the ban doubles as a safety net for non-eval
modules. Per AC, running `uv run ruff check src/superclaude/cli/eval/`
also flags it under that subtree.

## Acceptance Criteria → coverage

| AC | Requirement | Verified by |
|----|-------------|-------------|
| AC1 | `tests/cli/eval/test_pty_lifecycle.py` runs a single-eval fixture spawning the real claude binary via PTY and exits 0. | `test_real_claude_help_spawn_and_transcript` (full file run: 5 passed). |
| AC2 | Test asserts: prompt readiness observed, input injected, transcript file written, timeout reaps the child. | `test_lifecycle_prompt_ready_and_input_injection`, `test_lifecycle_transcript_persisted_end_to_end`, `test_lifecycle_timeout_reaps_child`. |
| AC3 | `uv run ruff check src/superclaude/cli/eval/` exits 0 on clean tree AND non-zero on synthetic `import anthropic`; `tool.ruff.lint.flake8-tidy-imports.banned-api` declares the rule per COMP-013. | `test_clean_tree_passes_ruff_check`, `test_synthetic_import_anthropic_is_flagged_by_ruff`, `test_ban_message_references_fr_g1`. |
| AC4 | `TASKLIST_ROOT/artifacts/D-0063/spec.md` documents the lifecycle test matrix and the ban-import rule configuration. | This document. |

## Out of scope

* Real `claude` interactive REPL with auth. Test #2 deliberately uses a
  Python stub for the prompt-ready / inject round-trip because the
  real binary requires authentication that is not available in CI.
  Test #1 only exercises the non-interactive `claude --help` path.
* Per-eval signal handling beyond the cancel/reap pair covered by
  test #3. Full SIGINT propagation is the contract of NFR-REL1 / T03.07
  and is exercised by `test_runner_class.py`.
* Hook deploy contents. The lifecycle tests pass `deploy_hooks=lambda _p: None`
  because hook deployment is FR-HK1's contract (T02.14 / D-0034); this
  module pins the **lifecycle** wiring, not the hook payload.
