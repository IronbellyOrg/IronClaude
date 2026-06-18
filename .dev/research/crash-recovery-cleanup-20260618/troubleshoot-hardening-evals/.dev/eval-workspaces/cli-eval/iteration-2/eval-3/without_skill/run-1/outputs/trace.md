# Trace — "Can I trust the 3/3 PASS from eval_smoke?"

Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
Date: 2026-06-12. Read-only investigation (one probe run into a scratch `--output-dir`).

## Step 1 — Locate eval CLI + smoke suite
- `find src/superclaude/cli/eval -type f` → exit 0. Found suite `src/superclaude/cli/eval/suites/eval_smoke.yaml`, plus `commands.py`, `runner.py`, `models.py`, `run_report.py`, `exit_codes.py`, `orchestrator.py`.

## Step 2 — Read the smoke suite
- `Read eval_smoke.yaml` → exit 0.
  - 3 evals: ES1 (`eval doctor`), ES2 (`eval list`), ES3 (`eval run --suite real --no-pty`).
  - **Every eval carries `no_pty: skip`.**
  - The suite header comment states: "--no-pty skips the whole suite" and ES3's body itself runs `real` with `--no-pty`, which "short-circuits all 15 real evals via the PTY-skip path."

## Step 3 — Read exit-code contract
- `Read exit_codes.py` → SUCCESS=0, FAILURES=1, USAGE_ERROR=2, INTERRUPTED=3.
- `models.py`: `SKIPPED_STATUSES = {SKIPPED, INTERRUPTED}`, `PASSED_STATUSES = {PASS, XFAIL}`, `FAILED_STATUSES = {FAIL, XPASS}`. SKIPPED is neither passed nor failed.

## Step 4 — Read final exit-code decision (commands.py:1986-2004)
- Exit code is decided **only** by:
  `if totals.failed>0 or totals.errored>0 or totals.timeout>0: exit 1; else exit 0`.
- SKIPPED contributes to none of those → **an all-SKIPPED run exits 0 (clean).**
- `eval run --help` confirms verbatim: "`0` — every expanded eval reached a terminal **PASS / SKIPPED / XFAIL** outcome."

## Step 5 — Confirm host capabilities
- `uv run superclaude eval doctor --json --no-mcp` → exit 0. claude/make/jq/git all `passed:true`. So binaries are NOT the blocker.

## Step 6 — Run eval_smoke with --no-pty (scratch output dir)
- `env HOME=/tmp/empty_home uv run superclaude eval run --suite eval_smoke --no-pty --no-mcp --json --output-dir .dev/eval-runs/smoke-nopty-probe2` → **EXIT=0**.
  - All 3 evals: `status:"SKIPPED"`, `skip_reason:"--no-pty"`, `expects:[]`, `duration_sec:0.0`.
  - totals: passed=0, failed=0, **skipped=3**.
  - (A first attempt with my real `$HOME` hit the FR-G5 hook-matcher coverage gate → exit 2, stderr "coverage gate FAILED — uncovered matcher patterns: mcp__auggie__.*". Host-specific pre-run gate, unrelated to suite outcome. Re-ran with empty HOME to clear it.)

## Step 7 — Run a single eval on the REAL (PTY) path — the decisive test
- `env HOME=/tmp/empty_home2 uv run superclaude eval run --suite eval_smoke --no-mcp --json --eval ES2 --output-dir .dev/eval-runs/smoke-pty-probe` → **EXIT=0**.
  - ES2: `status:"PASS"`, **`duration_sec:0.0`**, **`expects:[]`**, `skip_reason:null`.
  - `started_at == finished_at`; whole-run `duration_sec: 0.0045`.
  - A real Claude PTY drive of "run `superclaude eval list --json`" cannot finish in 4 ms → the eval body and its assertions never actually ran. PASS was emitted anyway.

## Step 8 — Root-cause in source
- `runner.py:_classify_outcome` (400-422): docstring + code —
  `if all(result.passed for result in state.expects): return "PASS"`.
  Comment: **"An empty `expects` tuple with no harness failure is `PASS` by design."** (`all()` over `[]` is vacuously True.)
- `commands.py:_NullLifecycleExecutor` (1357-1383): `spawn`/`inject` are no-ops; `observe` returns canned `ObservedRun(exit_code=0, stdout="", stderr="", duration_sec=0.0)`.
- `commands.py:_resolve_executor_factory` (1386-1405): unconditionally returns `_NullLifecycleExecutor`, tagged `produces_null_executor=True`. Docstring: "Production wiring (ClaudeProcessAdapter + PtyDriver) lands ... (M5/M6). Until then this factory returns the _NullLifecycleExecutor."
- `commands.py:_run_one_spec` (1408-1476): wires `expect_callables=()` — **empty by design**. Docstring step 3: "Wires the executor + an **empty `expect_callables`** tuple. The expects resolver ... lands in a follow-up; for now every spec that survives the `--no-pty` short-circuit returns PASS via the null executor."
- `commands.py:1879`: there IS an operator WARNING ("_NullLifecycleExecutor active — run results MUST NOT be treated as authoritative") — but it is **suppressed when `--json` is passed** (`and not as_json`) and goes to stderr only.

## Conclusion of trace
Two independent reasons the 3/3 PASS is not a real eval pass:
1. The smoke suite is built so the only documented green path is `--no-pty`, which marks all 3 evals SKIPPED (not PASS) yet still exits 0.
2. Even on the non-`--no-pty` path, the CLI is wired to a `_NullLifecycleExecutor` with `expect_callables=()`, so evals return a **vacuous PASS** (zero assertions, 0.0s) without spawning Claude or checking anything. The production PTY executor (M5/M6) is not yet wired in.
