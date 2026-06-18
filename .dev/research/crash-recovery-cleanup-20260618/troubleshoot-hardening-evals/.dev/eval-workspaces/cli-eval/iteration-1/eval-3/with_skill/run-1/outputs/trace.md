# Trace — Inspect `installer_sync_drift` + `--no-pty` safety verdict

Pipeline: `/sc:cli-eval run` (inspection-only path, non-interactive). Branch: `run`.
Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
Date: 2026-06-12

## Wave 0 — Mandatory fresh-context load (re-read + cite)

Per the protocol, I re-read the live contract surface before asserting any flag/behavior.
The authority for `--no-pty` semantics is the schema field + the operator guide — not memory.

| # | Source re-read | What it establishes | Citation |
|---|----------------|---------------------|----------|
| 1 | `src/superclaude/commands/cli-eval.md` | This is the `run` pipeline; W2 drills via `eval describe`; W3 surfaces `--no-pty` skip + FR-G5 gotchas | cli-eval.md:50-52 |
| 2 | `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md` | RUN W2 surfaces `no_pty: skip` markers; Error-Handling row: "All evals SKIPPED (`--no-pty`) → report as skipped, NOT pass" | SKILL.md:116-119, 184 |
| 3 | `.../refs/run-pipeline.md` | `--no-pty` → SKIPPED with `skip_reason="--no-pty"` and **exit 0**; "CI-canary path, NOT a real pass. For real PASS/FAIL, omit `--no-pty`" | run-pipeline.md:33-35 |
| 4 | `.../refs/eval-contracts.md` | Map only (not truth); points at suite.schema.json + suites-guide.md as the cite targets; `no_pty` enum = only `"skip"` | eval-contracts.md:6, 20, 52 |
| 5 | `src/superclaude/cli/eval/suites/suite.schema.json` | **Authoritative `no_pty` semantics**: enum `["skip"]`; when `"skip"`, `eval run --no-pty` short-circuits the eval → `EvalOutcome` status `SKIPPED`, `skip_reason="--no-pty"`, `skip_flag_triggered="--no-pty"` **before any HOME setup**; advisory, no effect when `--no-pty` absent | suite.schema.json:153-157 |
| 6 | `src/superclaude/cli/eval/suites/installer_sync_drift.yaml` | The suite manifest itself (see W-inspect below) | installer_sync_drift.yaml:32-90 |
| 7 | `docs/eval/suites-guide.md` | Operator gotcha: every `no_pty: skip` eval short-circuits to SKIPPED + exit 0 under `--no-pty`; "To actually exercise the evals, omit `--no-pty`." FR-G5 empty-HOME workaround. | suites-guide.md:547-554, 526-537 |

**Gate check**: no canonical source missing/moved. Digest complete. Proceeding.

## W-inspect — Inspect the suite via the CLI (not by opening the YAML blindly)

### Command 1 — describe through the CLI
```bash
timeout 120 uv run superclaude eval describe --suite installer_sync_drift
```
EXIT=0. Output (validated manifest, YAML):
- `name: installer_sync_drift`, `version: '1.0'`, `eval_count` (see list) = 1.
- `defaults`: `per_eval_timeout_sec: 180`, `per_eval_memory_mb: 512`, `capture_tty: true`, `keep_home_on_success: false`.
- `required_binaries` (all `failure_mode: hard`): `claude>=0.5.0`, `make`, `uv`, `git`.
- `optional_capabilities: []`.
- **evals[0]**: `id: S1` — "make verify-sync — src/ vs .claude/ parity + installer registration"
  - `category: installer-sync`, `timeout_sec: 180`
  - `isolation.home_strategy: shared`
  - **`no_pty: skip`**  ← the load-bearing marker
  - input: prompt instructing Claude Code (via PTY) to run `make verify-sync` and report exit + stdout; `expect_tool_call: Bash`.
  - expects: `exit_code == 0`; stdout `not_contains` each of `drift detected`, `MISSING from _FRESHNESS_SCRIPTS`, `STALE in _FRESHNESS_SCRIPTS`, `❌ DRIFT`.

### Command 2 — confirm it is in the registered library
```bash
timeout 120 uv run superclaude eval list --json | (filter installer_sync_drift)
```
EXIT=0 → `{'eval_count': 1, 'name': 'installer_sync_drift', 'version': '1.0'}`.
Confirms exactly **1 eval** and a schema-valid, loadable suite.

### Corroboration (read of YAML, allowed)
`installer_sync_drift.yaml:50-90` matches the CLI output 1:1; the in-file comment block
`installer_sync_drift.yaml:29-31` states `no_pty=skip` exists to keep `--no-pty` semantics
uniform across the inventory (the PTY harness drives a Claude Code subprocess).

## W-answer — the actual question

`--no-pty` semantics (suite.schema.json:153-157, run-pipeline.md:33-35, suites-guide.md:549-554):
running `eval run --no-pty` short-circuits every `no_pty: skip` eval to **SKIPPED**
(`skip_reason="--no-pty"`, `skip_flag_triggered="--no-pty"`), **before HOME setup**, exit 0.

This suite has **1/1** evals tagged `no_pty: skip` (S1). Therefore `--no-pty` skips the
**entire** suite — 0 assertions evaluated, `make verify-sync` never invoked. Exercises NOTHING.
That is the CI-canary path (proves the harness wiring), not a real pass. SKIPPED ≠ PASS
(SKILL.md:184; eval-contracts.md:37).

For a real run: **omit `--no-pty`** so the PTY harness drives Claude Code → `make verify-sync`.
Because the host `~/.claude/settings.json` carries hook matchers, the FR-G5 coverage gate
(exit 2) applies; use the empty-HOME workaround (suites-guide.md:535-537):
```bash
TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run --suite installer_sync_drift --no-mcp; rm -rf "$TMPHOME"
```

## Commands + exit codes summary
| Command | Exit |
|---|---|
| `uv run superclaude eval describe --suite installer_sync_drift` | 0 |
| `uv run superclaude eval list --json` (filtered) | 0 |
| grep `docs/eval/suites-guide.md` (no-pty / FR-G5) | 0 |

No files modified (read-only inspection + this trace/report).
