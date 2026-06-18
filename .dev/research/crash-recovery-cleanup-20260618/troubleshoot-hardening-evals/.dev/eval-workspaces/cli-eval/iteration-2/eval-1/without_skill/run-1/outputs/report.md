# Report — Running the `eval_smoke` suite

## What I set out to do
Select and supervise a run of the `eval_smoke` suite via this project's
`superclaude eval` CLI, then report what happened.

## How I selected the run
1. `superclaude eval --help` -> four subcommands: `describe`, `doctor`, `list`, `run`.
2. `superclaude eval list` -> confirmed **`eval_smoke (version 1.0, 3 evals)`** exists.
3. `superclaude eval describe --suite eval_smoke` -> 3 CLI-smoke evals:
   - **ES1** — `eval doctor --json --no-mcp` reports capabilities
   - **ES2** — `eval list --json` enumerates manifests
   - **ES3** — `eval run --suite real --no-pty` skips all real evals + emits artifacts
   - All three are marked `no_pty: skip`, so a `--no-pty` invocation would skip the
     entire suite. The supervised run therefore had to keep the PTY harness enabled.
4. `superclaude eval doctor --json --no-mcp` -> **all hard preconditions pass**
   (claude 2.1.175, make, jq, git, `~/.claude/` present). Soft skips only: the 3 MCP
   servers (skipped via `--no-mcp`, none on PATH) and the vendored PTY harness
   (`src/superclaude/cli/eval/pty/__init__.py` not present — `vendored.ptytest` soft-skip).

## How I supervised it, and what happened
I ran (PTY enabled, MCP skipped, all reporters on):
```
superclaude eval run --suite eval_smoke --no-mcp --json --verbose --junit \
  --keep-home --output-dir <dir>
```

Two terminal outcomes, both **exit 2 (harness-level rejection)** — the suite's
3 evals never executed:

- **Attempt 1 (custom output dir): `ScratchRootViolation`.** The AC12 scratch-root
  allowlist permits writes only under `/tmp/eval-runs/` or `<repo>/.dev/eval-runs/`.
  The requested SAVE-OUTPUTS path lives under `.dev/eval-workspaces/...`, outside both
  roots, so `--output-dir` could not be used as the live run target. I retargeted to
  the canonical `.dev/eval-runs/` root.

- **Attempt 2 (canonical root): FR-G5 hook-matcher coverage gate FAILED.** Before any
  worker dispatch, `eval run` runs a mandatory coverage gate that reads the host's
  `~/.claude/settings.json`, finds every PostToolUse matcher mentioning an
  auggie/airis MCP prefix, and requires the suite under test to contain at least one
  eval that exercises each. Three host matchers are uncovered by `eval_smoke`:
  ```
  PostToolUse: mcp__auggie__.*
  PostToolUse: mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*
  PostToolUse: mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
  ```
  `eval_smoke` is a CLI-only smoke suite — none of ES1/ES2/ES3 issue an auggie MCP
  tool call — so the gate fails closed and exits 2.

## Why this is the correct (not worked-around) result
- The gate is **unconditional** in `eval run` (`src/superclaude/cli/eval/commands.py:1822`);
  there is no flag to bypass it. `--no-mcp` only marks the MCP *servers* as
  skipped-by-flag in the doctor capability report — it does not remove the
  *hook matchers* from `settings.json`, which is what the FR-G5 gate inspects.
- `default_matcher_filter` (`src/superclaude/cli/eval/coverage.py:192`) deliberately
  scopes the gate to auggie/airis MCP matchers; those matchers are genuinely present
  in this host's `settings.json` (verified independently with `jq`).
- The only "fix" would be editing the host's `~/.claude/settings.json` to drop those
  matchers, or running a suite whose evals cover them (e.g. `real`). Both are out of
  scope for a read-only supervision task, so I stopped at the honest terminal state.

## Artifacts produced
The gate wrote its forensic trail under
`.dev/eval-runs/eval-smoke-supervised/.dev/eval-runs/2026-06-12/140627Z-77556236/`:
```
coverage_missing:mcp__auggie__._
coverage_missing:mcp__auggie__.__mcp__airis-mcp-gateway__auggie_._
coverage_missing:mcp__auggie__.__mcp__auggie-mcp__.__mcp__airis-mcp-gateway__auggie_._
```
No `summary.{md,json,yaml}`, no `junit.xml`, no per-eval HOMEs — the gate
short-circuits ahead of execution, exactly as the FR-G5 contract specifies.

## Bottom line
`eval_smoke` was correctly selected and the run was supervised to a deterministic
terminal outcome: **exit 2, harness-level rejection at the FR-G5 coverage preflight.**
The suite's 3 evals did not run because the host carries auggie/airis PostToolUse
hook matchers that a CLI-only smoke suite does not exercise. This is the gate working
as designed, not a flaky failure. To see ES1–ES3 actually execute, either run on a
host whose `settings.json` has no uncovered auggie/airis matchers, or point the
gate at a suite (e.g. `real`) whose evals cover them.
