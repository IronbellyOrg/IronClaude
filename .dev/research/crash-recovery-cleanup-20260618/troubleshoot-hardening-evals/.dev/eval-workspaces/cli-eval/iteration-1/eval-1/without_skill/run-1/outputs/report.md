# Report — `eval_smoke` run (what happened)

## TL;DR

I selected and ran the **`eval_smoke`** suite through the `superclaude eval` CLI. It **did not run any of its 3 evals** — the run stopped at a precondition gate and exited with **code 2** (harness-level rejection). The cause is a configuration mismatch on this host, not a bug in the suite or the evals.

## How I selected and supervised the run

1. **Discovered the surface**: `superclaude eval --help` → subcommands `list`, `describe`, `doctor`, `run`.
2. **Confirmed the suite exists**: `superclaude eval list` showed `eval_smoke (version 1.0, 3 evals)`.
3. **Read what it does**: `superclaude eval describe --suite eval_smoke`. The 3 evals (ES1/ES2/ES3) drive the `claude` CLI to run `eval doctor`, `eval list`, and `eval run --suite real` and assert on their stdout/exit codes. The suite uses a PTY (`capture_tty: true`) and each eval is marked `no_pty: skip`.
4. **Checked preconditions**: `superclaude eval doctor --json` → no hard failures (claude 2.1.175, make, jq, git all present). Three soft skips, including the PTY harness not being vendored.
5. **Ran it (supervised, backgrounded with a log + timeouts)**: `superclaude eval run --suite eval_smoke --output-dir .dev/eval-runs/eval_smoke-iter1 --junit --json --verbose`.

## What happened

The run halted **before executing a single eval**, with this on stderr and **exit code 2**:

```
eval doctor: coverage gate FAILED — uncovered matcher patterns:
  - PostToolUse: mcp__auggie__.*
  - PostToolUse: mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*
  - PostToolUse: mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
```

### Why (root cause)

The `eval run` path enforces an **FR-G5 hook-matcher coverage gate** before dispatching any work. It reads `~/.claude/settings.json`, finds every MCP-prefixed `PostToolUse` hook matcher registered there, and requires that **at least one eval in the suite exercises each matcher**. This host's `settings.json` registers three `auggie` PostToolUse matchers, but the three CLI-smoke evals never touch auggie MCP tools — so all three matchers are "uncovered" and the gate fails closed.

I confirmed this is a configuration mismatch, not a transient issue:
- `--no-mcp` does **not** help — the gate reads the *static hook registrations* in settings.json, not MCP runtime availability. Re-running with `--no-mcp` produced the identical failure (exit 2).
- The run directory contains **only** coverage artifacts (`coverage_missing:<pattern>.json`, one per uncovered matcher) and **no per-eval HOME directories**, proving the gate short-circuited before any eval ran.

### Two other things worth knowing

These wouldn't have mattered today (the gate stops the run first), but they shape what a "successful" run looks like at the current milestone:
- **No PTY harness yet**: `eval doctor` flags `vendored.ptytest` as not present ("vendored at M2"), and every eval has `no_pty: skip`.
- **Null executor at M2**: the run's executor factory returns a `_NullLifecycleExecutor` (the real `claude`-driving PTY executor lands at M5/M6). So even past the gate, the evals would currently run through a stubbed executor / be skipped rather than truly driving `claude`.

## Bottom line

- **Suite selected:** `eval_smoke` (3 evals).
- **Result:** 0 evals ran; **exit 2** at the FR-G5 coverage gate.
- **Cause:** host `~/.claude/settings.json` registers 3 auggie `PostToolUse` hook matchers that the smoke suite doesn't cover. Read-only constraint honored — nothing modified to "make it pass."

### To actually get the suite green (operator choices — not done here, would require write access)

1. Add a smoke eval that exercises an auggie MCP tool so the registered matchers are covered; **or**
2. Run on a host whose `settings.json` has no uncovered MCP `PostToolUse` matchers; **and**
3. Once the M5/M6 PTY executor + vendored `ptytest` land, run with the PTY harness (not `--no-pty`, which would skip the suite) so the evals truly drive the `claude` CLI.
