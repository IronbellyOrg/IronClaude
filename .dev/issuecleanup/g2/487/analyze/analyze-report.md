# Analyze report: src/superclaude/cli/eval/ (architecture, quick)

Command: `/sc:analyze src/superclaude/cli/eval/ --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/487/analyze`
Codegraph: index_state=fresh, checked_at=2026-11-24T02:41:05Z; degraded: none

Scope: architecture only, quick depth. 39 files (24 Python, 15 YAML suites). No source was modified.

## Findings

### F1 (high) The production executor is a documented null stub
`_NullLifecycleExecutor` (`src/superclaude/cli/eval/commands.py:1357`) implements spawn/inject/observe as no-ops and returns a canned `ObservedRun(exit_code=0)` (`commands.py:1377`). `_resolve_executor_factory` (`commands.py:1386`) hardwires that stub and tags it `produces_null_executor = True` (`commands.py:1401`), and `eval run` prints a warning when it is active (`commands.py:1881`). The real pieces exist but are not wired into the run path: `ClaudeProcessAdapter` (`src/superclaude/cli/eval/claude_process.py:107`, dependents: package init and one test) and `PtyDriver` (`pty_driver.py`). The docstring states production wiring "lands in M5 / M6" (`commands.py:1360`).

### F2 (medium) Concurrency is hard-clamped at 15
`RunOrchestrator.MAX_PARALLEL = 15` and `DEFAULT_PARALLEL = 8` (`src/superclaude/cli/eval/orchestrator.py:140`), clamped with `min(parallel, self.MAX_PARALLEL)` (`orchestrator.py:198`); the command repeats the clamp (`commands.py:1694`). A sub-group built on this orchestrator inherits the clamp.

### F3 (medium) The exit-code table is a fixed four-value contract
`SUCCESS=0, FAILURES=1, USAGE_ERROR=2, INTERRUPTED=3` (`src/superclaude/cli/eval/exit_codes.py:21`), consumed by six modules. No extension point.

### F4 (medium) Eval identifiers are closed by a regex
`EVAL_ID_PATTERN = ^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` (`src/superclaude/cli/eval/artifact_layout.py:108`), imported by `loader.py:43`. Lowercase-leading, hyphenated or underscored identifiers are rejected.

### F5 (info) Real reusable libraries exist beside the stub
`HomeIsolation` (`isolation.py:363`, 28 dependents), `EvalRunner` lifecycle with JSONL logging and timeout handling (`runner.py:712`), `RunOrchestrator` parallel runner (`orchestrator.py:110`, 9 dependents) and `RetryOncePolicy` (`retry.py:93`, eligible only for MCP-flaky tagged specs, not HTTP 429). Manifest validation uses a closed jsonschema `Draft202012Validator` (`loader.py:39`); the schema contents were not read at quick depth (UNVERIFIED).

### F6 (info) No lab package exists
No `src/superclaude/cli/lab/` directory and no `lab` module anywhere under `src/superclaude`. The sibling package the issue's spec proposes has not been started.

## Metrics
- 39 files, 24 Python modules, 15 YAML suites.
- Largest modules: `commands.py` (93 symbols), `runner.py` (65), `expect.py` (42), `models.py` (43), `loader.py` (40).
- Widest blast radius: `isolation.py` (28 dependents), `orchestrator.py` and `runner.py` (9 each).

## Recommendations
1. Treat cliEval as a library source, not a host: the stub executor (F1), the 15 clamp (F2), the fixed exit table (F3) and the id regex (F4) are all structural, so a sub-group under `superclaude eval` would inherit them.
2. Follow Part E's process-layer decision: use `ClaudeProcess(cwd=...)` directly, not `ClaudeProcessAdapter`, which changes the parent process's cwd and can race under threads (`src/superclaude/cli/eval/claude_process.py:335-365`; direct child cwd: `src/superclaude/cli/pipeline/process.py:103,215-218`). Reuse cliEval's isolation, containment, scratch, cancellation, disk-budget and reporter utilities; extract the companion's `RestrictedProcess` hardening (stdin-timeout fix, restricted reviewer profile, loopback ingress recording and hash-pinned config gate) into a shared module as required by `.dev/designs/spec-task-eval-framework/SPEC-AND-CONTEXT.md:621-624`. The hardening extraction is future work, not verified completed work; HTTP 429 backoff remains new code.
3. Nothing here is partly built toward the proposed framework; the work starts from zero outside this directory.
