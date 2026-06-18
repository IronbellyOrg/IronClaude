# Trace — /sc:cli-eval run --suite eval_smoke (with_skill, iteration-1)

Working dir: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
Date: 2026-06-12. Non-interactive subagent: AskUserQuestion replaced by stated-menu + sensible default.
Pipeline selected: **run** (`$1 = run`).

---

## Wave 0 — Mandatory fresh-context load (citations)

Re-read the live eval CLI/contract surface directly (the protocol delegates this to the
`eval-docs-loader` agent; as a subagent I performed the reads and cite them here). Authority for
every flag/field below is these reads, not a remembered contract.

| Concern | Source read | Cited fact |
|---|---|---|
| `eval` subcommands + flags | `src/superclaude/cli/eval/commands.py` | `@click.group("eval")` (L762) with `doctor` (L767), `list` (L924), `describe` (L1205), `run` (L1553). `eval run` flags: `--suite` (required), `--parallel` (default `RunOrchestrator.DEFAULT_PARALLEL`, clamp 1..15 L1692-1695), `--eval` (repeatable), `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult` (default 1.0, must be >0 L1697), `--max-disk-mb` (default `DEFAULT_DISK_BUDGET_MB`, 0 disables), `--json`, `--verbose`, `--junit`. |
| Exit codes | `src/superclaude/cli/eval/exit_codes.py` | `SUCCESS=0`, `FAILURES=1`, `USAGE_ERROR=2` (operator misuse / harness / FR-G5), `INTERRUPTED=3`. |
| `eval run` exit map | `commands.py` L1678-1687, L1989-2004 | 0 = all PASS/SKIPPED/XFAIL no breach; 1 = any FAIL/ERRORED/TIMEOUT/XPASS; 2 = harness rejection (scratch-root, suite-not-found, disk-budget, FR-G5); 3 = interrupted. |
| FR-G5 coverage gate | `commands.py` L1813-1829 | Runs BEFORE worker dispatch: `coverage_gate(settings_path=~/.claude/settings.json, suite=specs, ...)`; on `not coverage.passed` prints uncovered-matcher roster to stderr and `sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)` (=2). Missing/unreadable settings.json ⇒ empty matcher set ⇒ green. |
| `--no-pty` → SKIPPED | `commands.py` L1887-1905 | In `run_one`: `if no_pty and spec.no_pty == "skip": return EvalOutcome(status="SKIPPED", skip_reason="--no-pty", skip_flag_triggered="--no-pty")` before any HOME setup. |
| **M2 null-executor** | `commands.py` L1357-1404 (`_NullLifecycleExecutor`, `_resolve_executor_factory`) | Production PTY executor (ClaudeProcessAdapter + PtyDriver) lands at M5/M6 and is NOT on disk. Current factory returns `_NullLifecycleExecutor` which returns canned `exit_code=0`. L1879-1885: emits stderr `WARNING: _NullLifecycleExecutor active — run results MUST NOT be treated as authoritative` **only when `not as_json`** (the `--json` guard suppresses it). |
| summary.json schema + status enum | `src/superclaude/cli/eval/models.py` | `RunSummary` 11 fields (L820-832); `RunCounts` (manifest_n/expanded_n_prime/kept_k/skipped_s/flag); `RunTotals` (passed/failed/skipped/errored/interrupted/timeout); `EvalOutcome` 9 fields incl. `status`, `skip_reason`, `artifacts`, `error_class`. `EVAL_STATUSES` 8-literal enum (L49-62): PASS/FAIL/ERRORED/TIMEOUT/INTERRUPTED/SKIPPED/XFAIL/XPASS. SKIPPED ≠ PASS. |
| Artifact layout + run-id | `src/superclaude/cli/eval/artifact_layout.py` | `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (L76 `RUN_DIR_PREFIX`); run-id = `<HHMMSSZ>-<8hex sha256(suite+\n+started_at)>` (L151-171). Output root defaults to `Path.cwd()` (`commands.py` `_default_output_dir` L1331-1339), independent of `$HOME`. |
| HOME preservation | `commands.py` L1606-1614, runner wiring | `--keep-home` preserves per-eval HOME on PASS (default removes). Non-PASS evals keep HOME for forensics; path surfaces in that eval's `artifacts{}`. |
| Suite manifest + gotchas | `suites/eval_smoke.yaml`, `docs/eval/suites-guide.md` | eval_smoke v1.0, 3 evals (ES1/ES2/ES3), all `no_pty: skip`, `ephemeral` HOME. suites-guide §preflight confirms FR-G5 gate semantics + per-suite workarounds. |

**Host preconditions probed (Bash, read-only):**
- Platform = `Linux` ⇒ doctor will not refuse (AC1/R-109 Linux-only).
- `claude` = `2.1.175` at `/config/.local/bin/claude` ≥ 0.5.0 (HARD ok); `~/.claude/` present.
- **`~/.claude/settings.json` EXISTS** at `/config/.claude/settings.json` ⇒ FR-G5 gate is LIVE and will fire for `eval_smoke` (no covering matchers).

Gate check: no canonical source missing/moved. Digest complete. Proceeding.

---

## W1 — Enumerate via CLI

```
uv run superclaude eval list --json        # exit 0
```
12 suites returned; `eval_smoke` present: `{"name":"eval_smoke","version":"1.0","eval_count":3}`. Menu sourced from CLI, not a dir scrape.

## W2 — Describe eval_smoke

```
uv run superclaude eval describe --suite eval_smoke    # exit 0
```
Confirmed ES1/ES2/ES3, each `no_pty: skip`, `isolation.home_strategy: ephemeral`, `timeout_sec` 60/60/120.

## W3 — Invocation + gotchas (menu I would have shown; default chosen)

AskUserQuestion suppressed (non-interactive). Menu I would have presented:
- **A** — CI-canary skip: `eval run --suite eval_smoke --no-pty --no-mcp --json` → all-SKIPPED (NOT pass).
- **B (DEFAULT)** — real run under FR-G5 empty-HOME workaround: `TMPHOME=$(mktemp -d) HOME=$TMPHOME uv run superclaude eval run --suite eval_smoke --no-mcp ...; rm -rf "$TMPHOME"`.
- **C** — real run WITHOUT workaround first (demonstrate exit-2 gate), then B.

Chosen: **C then B** (forensic: show the gate fire, then clear it). All commands bounded with `timeout 180`.

## W4 — Monitor live runs (bounded foreground; runs are sub-second under M2 null-executor)

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `uv run superclaude eval run --suite eval_smoke --no-mcp --json` (no workaround) | **2** | FR-G5 coverage gate FAILED — stderr named uncovered PostToolUse matchers (`mcp__auggie__.*`, ...). No summary.json written (aborted pre-dispatch). |
| 2 | `env HOME=$TMPHOME uv run superclaude eval run --suite eval_smoke --no-mcp --json` | **0** | Gate cleared (empty HOME = no matchers). summary.json written. `--json` suppressed the null-executor WARNING. |
| 3 | `env HOME=$TMPHOME uv run superclaude eval run --suite eval_smoke --no-mcp --verbose` | **0** | stderr emitted `WARNING: _NullLifecycleExecutor active — run results MUST NOT be treated as authoritative`. verbose line: `3P/0F/0S/0E/0I/0T`. |

Run #1 stderr (forensic):
```
eval doctor: coverage gate FAILED — uncovered matcher patterns:
  - PostToolUse: mcp__auggie__.*
  - PostToolUse: mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*
  - PostToolUse: mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
```

## W5 — Parse summary.json (machine truth, NOT scrollback)

Run-dir (run #2): `.dev/eval-runs/2026-06-12/134335Z-07aca9f1/`
`jq` over `summary.json`:
- `counts`: manifest_n=3, expanded_n_prime=3, kept_k=3, skipped_s=0, kept_plus_skipped_equals_n_prime=true.
- `totals`: passed=3, failed=0, skipped=0, errored=0, interrupted=0, timeout=0.
- Per-eval: ES1/ES2/ES3 all `status:PASS`, `duration_sec:0.0`, `skip_reason:null`, `error_class:null`, `artifacts:{}`.
- FR-G4 layout intact: `summary.{md,json,yaml}` + `per-eval/ES{1,2,3}/artifacts/` + empty `homes/`.
- Preserved failed-HOMEs: NONE (no non-PASS eval; `homes/` empty, consistent with all-PASS + no `--keep-home`).

**Honesty note:** the 3/3 PASS is the **M2 `_NullLifecycleExecutor` canned-exit-0 path**, surfaced by the run #3 WARNING. It is NOT an authoritative validation of the ES1-ES3 prompts (no Claude subprocess ran). Reported as a clean harness/plumbing run, not a substantive green.

## Run-dirs produced
- `.dev/eval-runs/2026-06-12/134326Z-1d7a5f28/` — run #1, FR-G5 abort, no summary.
- `.dev/eval-runs/2026-06-12/134335Z-07aca9f1/` — run #2 (`--json`), summary present.
- `.dev/eval-runs/2026-06-12/134348Z-3b12db34/` — run #3 (`--verbose`), summary present.
