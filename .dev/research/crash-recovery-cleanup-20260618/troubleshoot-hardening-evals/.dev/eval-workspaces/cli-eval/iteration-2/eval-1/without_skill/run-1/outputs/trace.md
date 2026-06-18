# Trace — Supervised `eval_smoke` run

Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
Date: 2026-06-12. All Python via `uv run`. Each command capped at `timeout 180`.

## Step 1 — Discover the eval surface

```
uv run superclaude eval --help
```
Exit: 0. Subcommands: `describe`, `doctor`, `list`, `run`.

## Step 2 — Select the suite (list + run help)

```
uv run superclaude eval list
uv run superclaude eval run --help
```
Exit: 0 / 0. `eval_smoke (version 1.0, 3 evals)` present in the catalog (13 suites total).
Run flags noted: `--suite` (required), `--no-mcp`, `--no-pty`, `--output-dir`,
`--json`, `--verbose`, `--junit`, `--keep-home`. Exit-code contract:
0 = all terminal PASS/SKIP/XFAIL; 1 = some FAIL/ERROR/TIMEOUT/XPASS;
2 = harness rejection; 3 = operator interrupt.

## Step 3 — Inspect the chosen suite

```
uv run superclaude eval describe --suite eval_smoke
```
Exit: 0. 3 evals (ES1 `eval doctor --json --no-mcp`, ES2 `eval list --json`,
ES3 `eval run --suite real --no-pty`). All 3 carry `no_pty: skip` (a `--no-pty`
run would skip the whole suite). Required hard binaries: claude>=0.5.0, jq, make, git.

## Step 4 — Preflight host preconditions

```
uv run superclaude eval doctor --json --no-mcp
```
Exit: 0. All HARD rows pass (claude 2.1.175, make, jq, git, ~/.claude present).
Soft skips: 3 MCP servers (`--no-mcp`) and `vendored.ptytest` (PTY harness NOT
vendored at `src/superclaude/cli/eval/pty/__init__.py`). Standalone doctor does
NOT request the coverage gate (`coverage_gate.requested=false`).

## Step 5 — First run attempt (custom output dir) — REJECTED

```
uv run superclaude eval run --suite eval_smoke --no-mcp --json --verbose --junit \
  --keep-home --output-dir .dev/eval-workspaces/.../outputs/eval-run
```
Exit: 2. `ScratchRootViolation` — AC12 scratch-root allowlist permits only
`/tmp/eval-runs/` and `<repo>/.dev/eval-runs/`. The required SAVE-OUTPUTS path is
outside both, so `--output-dir` could not extend the allowlist to it.
Decision: retarget to the canonical `.dev/eval-runs/` root, copy artifacts out after.

## Step 6 — Second run attempt (canonical root) — HALTED BY GATE

```
uv run superclaude eval run --suite eval_smoke --no-mcp --json --verbose --junit \
  --keep-home --output-dir .dev/eval-runs/eval-smoke-supervised
```
Exit: 2. Halted at the FR-G5 / D-0075 hook-matcher **coverage gate**, BEFORE any
worker dispatch. Uncovered matcher patterns (all PostToolUse, all auggie/airis MCP):
```
PostToolUse: mcp__auggie__.*
PostToolUse: mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*
PostToolUse: mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
```

## Step 7 — Ground the failure

```
grep -rn "coverage gate FAILED|coverage_gate" src/superclaude/cli/eval/   # commands.py:1822, coverage.py
jq -r '.hooks.PostToolUse[]?.matcher | select(test("mcp__auggie|airis"))' ~/.claude/settings.json
```
Confirmed the 3 matchers are real PostToolUse registrations in the host's
`~/.claude/settings.json`. `coverage_gate()` in `src/superclaude/cli/eval/commands.py:1822`
runs unconditionally in `eval run` (no bypass flag); `coverage.py:192` `default_matcher_filter`
only enforces auggie/airis MCP matchers; `eval_smoke` issues no such MCP tool call,
so each matcher is "uncovered" and the gate fails closed (exit 2).

## Step 8 — Capture gate artifacts

```
find .dev/eval-runs/eval-smoke-supervised -type f
```
Gate wrote one forensic file per uncovered matcher under the run dir:
`coverage_missing:mcp__auggie__._`, `…__mcp__airis-mcp-gateway__auggie_._`,
`…__mcp__auggie-mcp__.__mcp__airis-mcp-gateway__auggie_._`.
No `summary.{md,json,yaml}` / `junit.xml` and no per-eval HOMEs were produced —
the gate short-circuits ahead of execution by design.

## Outcome

The `eval_smoke` suite did NOT execute its 3 evals. The run is a deterministic,
reproducible **harness-level rejection (exit 2)** at the FR-G5 coverage preflight,
caused by the host's auggie/airis PostToolUse hook matchers having no covering eval
in this CLI-only smoke suite. Not pivoted around (no flag exists; host settings.json
is out of scope / read-only).
