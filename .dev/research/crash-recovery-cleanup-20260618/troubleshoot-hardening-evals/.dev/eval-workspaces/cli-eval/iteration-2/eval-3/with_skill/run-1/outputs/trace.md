# Trace — "Can I trust the eval_smoke 3/3 PASS?"

Question: is the 3/3 PASS / exit 0 from `eval_smoke` a real, trustworthy eval pass?
Method: read the skill + reporter authoritativeness contract, locate the executor in source,
then empirically reproduce verbose vs --json to establish which executor produced the PASS.
Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`

## Step 1 — Read protocol + reporter authoritativeness contract
- Read `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md`.
  - W5 (lines 138-147): reporter MUST "establish which executor produced the result"; a
    non-production/stubbed executor emits a `results MUST NOT be treated as authoritative`
    warning that is "suppressed by `--json`"; such a run is "NON-AUTHORITATIVE (plumbing only)".
  - Error-handling row (line 190): "Non-production/stubbed executor (canned PASS) → Label run
    NON-AUTHORITATIVE … Re-run `--verbose` to surface the warning `--json` suppressed."
- Read `src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md`.
  - W4 (lines 49-53): "Authoritativeness probe: prefer `--verbose` over … `--json` … The harness
    may run a non-production executor (e.g. a milestone-gated `_NullLifecycleExecutor` that emits
    canned PASS before the real PTY executor lands)."
- Read `src/superclaude/agents/eval-run-reporter.md`.
  - Lines 20-26: "A PASS is only as authoritative as the executor that produced it … a green
    `summary.json` can be a *plumbing* pass, not a real one."

## Step 2 — Locate the executor in source
- `grep -rn "_NullLifecycleExecutor|authoritative|MUST NOT" src/superclaude/cli/eval/`
  → `src/superclaude/cli/eval/commands.py` (executor class + warning).
- Read `commands.py:1357-1476`:
  - `class _NullLifecycleExecutor` (1357): "Zero-side-effect LifecycleExecutor for the M2/M3
    surface. Production wiring (ClaudeProcessAdapter + PtyDriver) lands in M5 / M6 …".
  - `.observe()` (1377-1383) returns a hardcoded `ObservedRun(exit_code=0, stdout="", stderr="",
    duration_sec=0.0)` — i.e. a CANNED PASS with no subprocess.
  - `_resolve_executor_factory()` (1386-1405): "Until then this factory returns the
    `_NullLifecycleExecutor`." Tags the factory `produces_null_executor = True`.
  - `_run_one_spec` docstring (1408-1442): "for now every spec that survives the `--no-pty`
    short-circuit returns PASS via the null executor."
- Read `commands.py:1850-1909` (warning emission):
  - 1858: `executor_factory = _resolve_executor_factory()`.
  - 1879-1885: `if getattr(executor_factory, "produces_null_executor", False) and not as_json:`
    → emits to stderr `eval run: WARNING: _NullLifecycleExecutor active — non-production executor
    selected; run results MUST NOT be treated as authoritative.`
  - The `and not as_json` clause is the documented `--json` SUPPRESSION (comment 1866-1869).

## Step 3 — eval_smoke suite shape
- `grep -n "no_pty|version|id:" src/superclaude/cli/eval/suites/eval_smoke.yaml`:
  - version "1.0"; evals ES1/ES2/ES3; ALL carry `no_pty: skip` (lines 55,76,98).
  - Implication: WITH `--no-pty` → all 3 SKIP (exit 0). WITHOUT `--no-pty` (the user's case,
    since they saw 3 PASS) → all 3 flow through the null executor → canned PASS.

## Step 4 — Empirical: verbose run (warning surfaces)
Command (empty-HOME workaround per W3, default scratch root = repo `.dev/eval-runs/`):
```
TMPHOME=$(mktemp -d) && timeout 120 env HOME=$TMPHOME uv run superclaude eval run \
  --suite eval_smoke --verbose --no-mcp 2>&1 | head -70; rm -rf "$TMPHOME"
```
Output (EXIT=0):
```
eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.
run 140633Z-71832b0f: 3P/0F/0S/0E/0I/0T in 0.01s -> .../.dev/eval-runs/2026-06-12/140633Z-71832b0f
```
→ 3 PASS, exit 0, **and** the non-authoritative WARNING. (A first attempt with
`--output-dir "$TMPHOME/out"` exited 2 via the AC12 scratch-root allowlist; rerun without it.)

## Step 5 — Empirical: --json run (warning suppressed)
```
TMPHOME=$(mktemp -d) && env HOME=$TMPHOME uv run superclaude eval run --suite eval_smoke \
  --json --no-mcp 2>&1 | grep -i "WARNING|authoritative|NullLifecycle"; rm -rf "$TMPHOME"
```
Only match: the unrelated UV `VIRTUAL_ENV=/lsiopy … will be ignored` line. The
`_NullLifecycleExecutor` / "MUST NOT be treated as authoritative" line is ABSENT — exactly the
`not as_json` suppression at commands.py:1879. This is why the user's `--json`/summary view showed
a clean 3/3 PASS with no caveat.

## Step 6 — Empirical: summary.json shape (canned PASS)
```
suite=…/eval_smoke.yaml ver=1.0
counts={'manifest_n':3,'expanded_n_prime':3,'kept_k':3,'skipped_s':0,...}
statuses=[('ES1','PASS',0.0),('ES2','PASS',0.0),('ES3','PASS',0.0)]
```
Every eval: `status=PASS, duration_sec=0.0` — the literal canned `ObservedRun(...,duration_sec=0.0)`
from `_NullLifecycleExecutor.observe()` (commands.py:1382). No subprocess was spawned; 0.0s and
empty stdout/stderr are the tell.

## Conclusion
Executor = `_NullLifecycleExecutor` (commands.py:1357), returned by `_resolve_executor_factory`
(1402) for the current M2/M3 milestone. The 3/3 PASS is a PLUMBING pass, NON-AUTHORITATIVE. The
real `ClaudeProcessAdapter + PtyDriver` executor lands at M5/M6; until then no `eval_smoke` PASS
exercises real CLI behavior.
