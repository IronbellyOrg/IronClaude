# Trace — Running the `eval_smoke` suite (baseline / without_skill)

Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
Date: 2026-06-12
Goal: select and supervise a run of the `eval_smoke` suite via the `superclaude eval` CLI, then report what happened.

All Python invoked through UV. Every shell command capped with `timeout`. No source files modified (read-only except this outputs dir).

---

## Step 1 — Discover the eval surface

```
mkdir -p .dev/eval-workspaces/cli-eval/iteration-1/run-eval-smoke/without_skill/outputs/
uv run superclaude eval --help
```
Exit code: **0**

Subcommands: `describe`, `doctor`, `list`, `run`. Harness = "the cliEval real-eval harness".

## Step 2 — Enumerate suites and read the run contract

```
uv run superclaude eval list          # EXIT 0
uv run superclaude eval run --help     # EXIT 0
```

`eval list` confirmed `eval_smoke (version 1.0, 3 evals)` is present (12 suites total).

`run --help` documented the exit-code contract:
- `0` — every eval reached PASS / SKIPPED / XFAIL, no breach.
- `1` — at least one FAIL / ERRORED / TIMEOUT / XPASS.
- `2` — harness-level rejection (invalid flag, scratch-root violation, suite not found, disk-budget exceeded, **coverage-gate failure**).
- `3` — operator interrupt (SIGINT/SIGTERM).

Notable flags: `--suite` (required), `--parallel` (default 8), `--output-dir` (AC12 scratch-root allowlisted), `--no-mcp`, `--no-pty`, `--junit`, `--json`, `--verbose`.

## Step 3 — Inspect the `eval_smoke` manifest

```
uv run superclaude eval describe --suite eval_smoke
```
Exit code: **0**

The suite drives the `claude` CLI to execute three CLI-smoke prompts:
- **ES1** — `superclaude eval doctor --json --no-mcp` reports capabilities (expects stdout contains `"capabilities"`, exit 0).
- **ES2** — `superclaude eval list --json` enumerates manifests (expects `"name": "real"`, exit 0).
- **ES3** — `superclaude eval run --suite real --no-pty --no-mcp --junit --json` skips all real evals and emits artifacts (expects `summary.json`, exit 0).

Suite defaults: `capture_tty: true`, `per_eval_timeout_sec: 120`. Every eval carries `no_pty: skip` (running with `--no-pty` skips the whole suite). Required hard binaries: `claude (>=0.5.0)`, `jq`, `make`, `git`.

## Step 4 — Preconditions check (`eval doctor`)

```
uv run superclaude eval doctor --json
which claude; claude --version
```
Exit code: **0**

- All HARD rows PASS: `claude` = `/config/.local/bin/claude` (v2.1.175), `make`, `jq`, `git` all on PATH; `~/.claude/` exists.
- `hard_failures: []`.
- Soft skips (non-blocking): `mcp_server.auggie-mcp`, `mcp_server.airis-mcp-gateway`, **`vendored.ptytest`** (PTY harness not vendored — `src/superclaude/cli/eval/pty/__init__.py` not found, "vendored at M2").

## Step 5 — First launch attempt (rejected: scratch-root)

```
uv run superclaude eval run --suite eval_smoke --parallel 3 \
  --output-dir .dev/eval-workspaces/.../outputs/eval-run --junit --json --verbose
```
Exit code: **2**

Rejected with `ScratchRootViolation`: the required outputs path under `.dev/eval-workspaces/` escapes the AC12 allowlist. Allowed roots are only `/tmp/eval-runs/`, `<repo>/.dev/eval-runs/`, or a path passed via `--output-dir` (call-scoped extension). Reference: `docs/eval/scratch-roots.md`.

**Decision:** point `--output-dir` at the allowed `<repo>/.dev/eval-runs/eval_smoke-iter1` scratch root; the required `outputs/` dir receives this trace + report + the run log.

## Step 6 — Second launch (past scratch-root, blocked by coverage gate)

```
mkdir -p .dev/eval-runs/eval_smoke-iter1
uv run superclaude eval run --suite eval_smoke --parallel 3 \
  --output-dir .dev/eval-runs/eval_smoke-iter1 --junit --json --verbose
```
Exit code: **2**

Output:
```
eval doctor: coverage gate FAILED — uncovered matcher patterns:
  - PostToolUse: mcp__auggie__.*
  - PostToolUse: mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*
  - PostToolUse: mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
```

## Step 7 — Root-cause the coverage-gate failure (read-only)

Read `src/superclaude/cli/eval/commands.py` (run path) and `src/superclaude/cli/eval/coverage.py`:
- The **FR-G5 hook-matcher coverage gate** (`coverage_gate(...)`, commands.py ~L1822) runs **before any worker dispatch**, with **no skip flag** in `run`.
- It reads `~/.claude/settings.json`, extracts PostToolUse hook matchers matching the MCP-tool-prefix filter, and requires that **some eval in the suite reference each such matcher**.
- The host's `settings.json` registers three auggie PostToolUse matchers; the three CLI-smoke evals don't touch auggie MCP tools, so all three matchers are uncovered → gate fails → exit 2.

Confirmed host matchers:
```
jq -r '.hooks.PostToolUse[]?.matcher' /config/.claude/settings.json | grep -i auggie
# mcp__auggie__.*
# mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*
# mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
```

## Step 8 — Reconfirm with `--no-mcp` (gate still fails)

```
uv run superclaude eval run --suite eval_smoke --output-dir .dev/eval-runs/eval_smoke-iter1 --no-mcp
```
Exit code: **2** (identical three uncovered patterns).

`--no-mcp` marks MCP *capabilities* as skipped but does NOT relax the coverage gate, which reads the static hook registrations in `settings.json`, not MCP runtime availability.

## Step 9 — Inspect run-dir artifacts + confirm null executor

```
find .dev/eval-runs/eval_smoke-iter1/.dev -type f
grep -n "_NullLifecycleExecutor|produces_null_executor|_resolve_executor_factory" src/superclaude/cli/eval/commands.py
```

- Run dir contains ONLY a coverage-artifact subtree (`coverage_missing:<pattern>` JSON files, one per uncovered matcher) under timestamped run folders. **No per-eval HOME directories were created** — confirming the gate short-circuits before any eval executes.
- `_resolve_executor_factory()` returns a `_NullLifecycleExecutor` tagged `produces_null_executor = True` ("vendored at M2"; real `ClaudeProcessAdapter + PtyDriver` lands at M5/M6). So even past the gate, every eval would run through a null runner and the missing PTY harness (`vendored.ptytest` soft-skip + per-eval `no_pty: skip`) would skip them.

Sample artifact (`coverage_missing:mcp__auggie__._`):
```json
{ "coverage_missing": true, "covered_by": [], "event": "PostToolUse",
  "pattern": "mcp__auggie__.*", "settings_source": "/config/.claude/settings.json" }
```

---

## Outcome

The `eval_smoke` suite **did not execute any of its 3 evals**. The run halts at the FR-G5 hook-matcher coverage gate with **exit code 2** (harness-level rejection), because the host's `~/.claude/settings.json` registers three auggie PostToolUse hook matchers that no smoke-suite eval covers. This is a host/suite configuration mismatch, not a defect in the eval logic. No source files or settings were modified (read-only constraint honored).
