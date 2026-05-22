# cliEval Pipeline — User Guide

**Audience:** operators running `superclaude eval` from the command line; CI authors wiring eval into pipelines.

**Last verified:** 2026-05-22 against `src/superclaude/cli/eval/` post-remediation (TASK-RF-20260522-153212).

> This is the **task-oriented user guide**. For deep technical reference (manifest schema, hook telemetry, retry policy, retention policy), see the docs under [`docs/eval/`](../eval/). For the canonical design specification, see [`.dev/releases/current/cliEval/design-spec.md`](../../.dev/releases/current/cliEval/design-spec.md).

---

## Table of Contents

- [What cliEval is](#what-clieval-is)
- [Quick start](#quick-start)
- [The four subcommands](#the-four-subcommands)
  - [`eval doctor` — preflight](#eval-doctor--preflight)
  - [`eval list` — enumerate suites](#eval-list--enumerate-suites)
  - [`eval describe` — inspect a manifest](#eval-describe--inspect-a-manifest)
  - [`eval run` — execute a suite](#eval-run--execute-a-suite)
- [Exit codes](#exit-codes)
- [Output layout](#output-layout)
- [Scratch-root allowlist (AC12 / OPS-002)](#scratch-root-allowlist-ac12--ops-002)
- [Coverage gate (FR-G5)](#coverage-gate-fr-g5)
- [Reading the verbose summary line](#reading-the-verbose-summary-line)
- [Common workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Reference](#reference)

---

## What cliEval is

`superclaude eval` runs a suite of **falsifiable, evidence-producing evals** against the local `claude` binary. Each eval is a single-turn interaction backed by a YAML manifest entry, executed inside an isolated per-eval `HOME` so concurrent runs cannot stomp on each other's state.

The harness produces three canonical artifacts per run — `summary.md` (human-readable), `summary.json` (machine-readable), `summary.yaml` (CI-friendly) — plus an optional `junit.xml` for CI dashboards and per-eval forensic trees (logs, tty transcripts, captured artifacts).

cliEval is **Linux-only in v1** (AC1 / R-109). On macOS or Windows the doctor refuses with a friendly stderr message before any capability check runs.

---

## Quick start

```bash
# 0. Verify host preconditions (do this FIRST on a new machine)
uv run superclaude eval doctor

# 1. See what suites are available
uv run superclaude eval list

# 2. Inspect a suite's expanded eval list
uv run superclaude eval describe --suite real

# 3. Run a suite
uv run superclaude eval run --suite real

# 4. Run a quick subset with a verbose summary line
uv run superclaude eval run --suite real --eval E1 --eval E2 --verbose

# 5. CI-style invocation with JUnit XML
uv run superclaude eval run --suite real --output-dir /tmp/eval-runs/ci --json --junit
```

Artifacts land under `<output-dir>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` — anchored via `compose_run_dir` so the layout is identical regardless of which root you choose (FR-G4).

---

## The four subcommands

### `eval doctor` — preflight

Verifies the host satisfies every HARD capability before you ever launch a run. Run this first on any new machine, after upgrading the `claude` binary, or whenever a run mysteriously fails with exit `2`.

```bash
uv run superclaude eval doctor                          # green checklist, human-readable
uv run superclaude eval doctor --json                   # deterministic machine-readable payload
uv run superclaude eval doctor --no-mcp                 # skip MCP-server gates
uv run superclaude eval doctor --check-coverage --suite real   # also run the FR-G5 matcher coverage gate
uv run superclaude eval doctor --output-dir /tmp/eval-runs     # validate a candidate --output-dir against AC12
uv run superclaude eval doctor --parallel 15            # also runs NFR-PERF2 free-RAM precheck
```

**What it checks:**
- `claude>=0.5.0`, `jq`, `make`, `git`, `~/.claude/` extant (HARD capabilities)
- MCP-server availability (SOFT capabilities, unless `--no-mcp`)
- `ptytest` vendoring marker
- Optionally the FR-G5 hook-matcher coverage gate (`--check-coverage`)
- Optionally an `--output-dir` candidate against the AC12 scratch-root allowlist
- Optionally a free-RAM precheck (NFR-PERF2) when `--parallel >= 15`

**Exit codes:**
- `0` — every HARD capability satisfied
- `2` — at least one HARD capability failed, OR `--output-dir` escaped the allowlist, OR the host is not Linux

The stderr artifact always identifies the cause. For a scratch-root violation it quotes the `SCRATCH_ROOT_POLICY` verbatim so you can correct the invocation without leaving the terminal.

---

### `eval list` — enumerate suites

Lists every manifest under `src/superclaude/cli/eval/suites/` with `name`, `version`, and the post-parameterize-expansion eval count.

```bash
uv run superclaude eval list                                    # table to stdout
uv run superclaude eval list --json                             # JSON array
uv run superclaude eval list --suites-dir /path/to/manifests    # alternate suites dir
```

**Exit codes:**
- `0` — every discovered manifest loaded green (or no manifests found)
- `2` — at least one manifest failed schema validation, eval-id regex, or capability resolution

An empty/missing suites directory prints `(no suites found)` and still exits `0`.

---

### `eval describe` — inspect a manifest

Prints the validated, post-parameterize-expansion manifest. Parameterized rows (e.g. `E2`) become multiple entries (`E2.1`, `E2.2`, ...) in the output.

```bash
uv run superclaude eval describe --suite real                   # YAML (default)
uv run superclaude eval describe --suite real --json            # JSON
uv run superclaude eval describe --suite real --eval E2.1       # single eval
```

**`--suite` resolution order:** filesystem path → filename stem → `name:` field.

**Exit codes:**
- `0` — manifest validated and printed
- `2` — schema rejection, id-regex rejection, capability rejection, missing suite (`SuiteNotFound`), or missing eval id (`EvalNotFound`)

---

### `eval run` — execute a suite

The primary execution entry point. Wires twelve flags through to the `RunOrchestrator`, `CapabilityGates`, `Reporter`, and `DiskBudgetPoller`.

```bash
# Minimal — runs the full suite at default parallelism (8 workers)
uv run superclaude eval run --suite real

# Subset, verbose, MCP-skipped (use when auggie isn't installed)
uv run superclaude eval run --suite real --eval E1 --eval E2 --no-mcp --verbose

# CI invocation — pin output, emit JUnit and JSON
uv run superclaude eval run \
  --suite real \
  --output-dir /tmp/eval-runs/ci \
  --json \
  --junit

# Debug a single failing eval — keep its HOME for forensic inspection
uv run superclaude eval run --suite real --eval E5 --keep-home --verbose

# Long-running suite — bump timeout multiplier and disk budget
uv run superclaude eval run --suite real --timeout-mult 2.0 --max-disk-mb 4096
```

#### Full flag reference

| Flag | Type | Default | Purpose |
|---|---|---|---|
| `--suite` | TEXT | (required) | Suite name, filename stem, or manifest path |
| `--parallel` | INT | `8` | Worker concurrency; clamps to `[1, 15]` per design-spec §11 |
| `--eval` | TEXT (repeatable) | (no filter) | Filter to one or more post-expansion eval ids; empty selection exits `2` with `EvalNotFound` |
| `--no-mcp` | flag | off | Mark MCP capabilities as skipped-by-flag |
| `--no-pty` | flag | off | Run without the vendored PTY harness (degrades stdout capture); per-eval `no_pty: skip` tags fire here |
| `--output-dir` | DIRECTORY | `.dev/eval-runs/<run-id>/` | Destination for artifacts; **must resolve under the AC12 allowlist** |
| `--keep-home` | flag | off | Preserve per-eval HOME directories on PASS (default removes them) |
| `--timeout-mult` | FLOAT | `1.0` | Multiplier applied to each spec's `timeout_sec` before reaching `EvalRunner.default_timeout_sec`; must be `> 0` |
| `--max-disk-mb` | INT | `1024` | Disk-budget ceiling for `output_dir` in megabytes (NFR-PERF4). `0` disables the poller entirely |
| `--json` | flag | off | Emit the run summary as JSON to stdout in addition to writing to disk |
| `--verbose` | flag | off | Print a human-readable summary line to stdout when the run finishes |
| `--junit` | flag | off | Also write a `junit.xml` JUnit XML report into `output_dir` |

---

## Exit codes

cliEval pins exactly four canonical exit codes, declared in [`src/superclaude/cli/eval/exit_codes.py`](../../src/superclaude/cli/eval/exit_codes.py) and re-exported under descriptive local names at every consumer module:

| Code | Constant | Meaning |
|---|---|---|
| `0` | `SUCCESS` | Every expanded eval reached PASS / SKIPPED / XFAIL and no breach occurred |
| `1` | `FAILURES` | At least one eval ended FAIL / ERRORED / TIMEOUT / XPASS but the harness ran to completion |
| `2` | `USAGE_ERROR` | Harness-level rejection: invalid flag, scratch-root violation, suite not found, disk-budget exceeded, capability gate failed, coverage gate failed, schema error, invalid eval id, etc. |
| `3` | `INTERRUPTED` | SIGINT / SIGTERM landed mid-run and cooperative cancellation drained |

Code `2` is the catch-all "harness refused to run / aborted before completing the run." The stderr line always identifies the specific cause via a typed exception class name (`ScratchRootViolation`, `SuiteNotFound`, `SchemaError`, `InvalidEvalId`, `UnresolvedCapability`, `CoverageGateFailed`, `DiskBudgetExceeded`, etc.).

Cross-references:
- Process-boundary contract: [`tests/cli/eval/test_exit_codes.py`](../../tests/cli/eval/test_exit_codes.py)
- Canonical definitions: `src/superclaude/cli/eval/exit_codes.py`

> **Why not 130 for interrupted?** Some shells expose `signal+128 = 130` for SIGINT, but cliEval pins **`3`** at the process boundary because that's the design-spec §4 contract. The constant is documented inline in `exit_codes.py`.

---

## Output layout

`eval run` writes artifacts under the FR-G4 reproducible layout (anchored via `compose_run_dir`):

```
<output-dir>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/
├── summary.md          # human-readable run report (design-spec §9)
├── summary.json        # machine-readable, matches summary.schema.json
├── summary.yaml        # CI-friendly YAML view
├── junit.xml           # ONLY when --junit is set
└── per-eval/
    └── <eval_id>/
        ├── logs.jsonl
        ├── tty.transcript
        └── artifacts/
```

The `<run-id>` is a deterministic `<HHMMSSZ>-<8-hex>` string derived from the start timestamp and suite name, so two runs at the same instant against the same suite collide on the same path (FR-G4 acceptance criterion).

`--output-dir <X>` makes `<X>` the **output root**, not the run-dir. The layout is layered underneath, so `eval run --output-dir /tmp/eval-runs/foo` produces `/tmp/eval-runs/foo/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/summary.md` — the same shape you get under `.dev/eval-runs/` by default.

---

## Scratch-root allowlist (AC12 / OPS-002)

Every filesystem write — per-eval `HOME`, per-eval working tree, the `--output-dir` target — must resolve under one of these allowed roots:

```
1. /tmp/eval-runs/             — canonical scratch root
2. <repo>/.dev/eval-runs/      — repo-relative scratch root
3. --output-dir <path>         — extends the allowlist for the current invocation only
```

**Anything else is rejected before any filesystem write.** The check happens in `resolve_scratch_root` (`src/superclaude/cli/eval/config.py`), which every scratch-minting caller funnels through.

Two architectural invariants the recent remediation tightened:

1. **No bare-prefix tautology (H4):** `resolve_scratch_root("/tmp/eval-runs")` (the prefix itself, with no sub-path) now **raises `ScratchRootViolation`**. Only strict sub-paths are accepted. This closes a foot-gun where passing the prefix as the candidate would make the allowlist check tautological.

2. **No write-before-validate (H5 / OPS-002):** The allowlist is extended with the resolved `--output-dir` and the derived `home_root` **before** any `mkdir` runs. Both at the `commands.py` entry point and at the per-eval `HomeIsolation.setup()` layer, a non-allowlisted path raises **before** any on-disk side effect.

If you see `ScratchRootViolation: ...` on stderr, the offending path is identified verbatim alongside the full `SCRATCH_ROOT_POLICY` text — you don't need to consult the docs to correct the invocation.

For the full policy text and detailed allowlist semantics, see [`docs/eval/scratch-roots.md`](../eval/scratch-roots.md).

---

## Coverage gate (FR-G5)

The FR-G5 hook-matcher coverage gate enforces that **every** PostToolUse hook matcher pattern in `~/.claude/settings.json` is exercised by at least one eval in the suite under test. The bug PR #49 fixed was exactly this class of silent regression: a matcher pattern broke and no eval noticed because no eval issued a matching tool call.

**When the gate runs:**
- `eval doctor --check-coverage [--suite <name>]` — explicit preflight check
- `eval run` — implicit at the top of every run, AFTER suite parse and BEFORE any worker is dispatched (so a coverage breach short-circuits without touching any per-eval HOME)

**v1 coverage scope:** the three auggie-prefix matcher families:
- `mcp__auggie__*`
- `mcp__auggie-mcp__*`
- `mcp__airis-mcp-gateway__*`

**Failure modes:**
- Missing matcher → `coverage_gate failed (missing matchers: <list>)` on stderr, exit `2`, plus a `coverage_missing:<pattern>` artifact under the run-dir
- **Corrupt `settings.json` (post-H2 fix):** the gate now **fails closed** — parse errors return `CoverageResult(passed=False, parse_error=...)` instead of the previous silent-green path. A misconfigured host can no longer run as if all matchers were covered.

---

## Reading the verbose summary line

When you pass `--verbose`, `eval run` prints a single human-readable line to stdout when the run finishes. The format (post-H3) renders the full DM-012 status taxonomy:

```
run <run-id>: <P>P/<F>F/<S>S/<E>E/<I>I/<T>T in <duration>s -> <output_dir>
```

| Letter | Bucket | DM-012 statuses included |
|---|---|---|
| `P` | passed | `PASS`, `XFAIL` |
| `F` | failed | `FAIL`, `XPASS` |
| `S` | skipped | `SKIPPED` |
| `E` | errored | `ERRORED` |
| `I` | interrupted | `INTERRUPTED` |
| `T` | timeout | `TIMEOUT` |

A clean run reads `1P/0F/0S/0E/0I/0T`. A run with one failing eval reads `0P/1F/0S/0E/0I/0T` and exits `1`. The full status taxonomy is enforced in code via the `EVAL_STATUSES` / `PASSED_STATUSES` / `FAILED_STATUSES` / `SKIPPED_STATUSES` partitions in [`src/superclaude/cli/eval/models.py`](../../src/superclaude/cli/eval/models.py), so the summary line cannot drift from the canonical set.

---

## Common workflows

### Daily development loop

```bash
# Quick smoke check
uv run superclaude eval doctor && uv run superclaude eval run --suite real --eval E1 --verbose
```

### Debugging a single failing eval

```bash
# Run only the failing eval, keep its HOME for inspection
uv run superclaude eval run --suite real --eval E5 --keep-home --verbose

# Then inspect the preserved per-eval HOME
ls .dev/eval-runs/<YYYY-MM-DD>/<run-id>/per-eval/E5/
```

### CI invocation

```bash
uv run superclaude eval doctor --json > /tmp/eval-doctor.json || exit 2
uv run superclaude eval run \
  --suite real \
  --output-dir /tmp/eval-runs/$BUILD_ID \
  --parallel 8 \
  --max-disk-mb 2048 \
  --json \
  --junit
# Read /tmp/eval-runs/$BUILD_ID/.dev/eval-runs/.../junit.xml in your CI dashboard
```

### Host without MCP servers

```bash
uv run superclaude eval doctor --no-mcp
uv run superclaude eval run --suite real --no-mcp --verbose
```

### Host without a real TTY (e.g. some container runners)

```bash
uv run superclaude eval run --suite real --no-pty --verbose
# Evals tagged `no_pty: skip` in the manifest will be SKIPPED rather than ERRORED
```

---

## Troubleshooting

### `exit 2` with no clear stderr line

Run `eval doctor` first. Most exit-`2` failures from `eval run` are pre-flight conditions the doctor will diagnose:

```bash
uv run superclaude eval doctor --check-coverage --suite real --output-dir <your-output-dir>
```

### `ScratchRootViolation` on a path you think should work

You're either passing a bare allowlist prefix (`/tmp/eval-runs` with no sub-path — H4 now rejects this) or passing a path outside the three allowed roots. The stderr artifact will quote the policy verbatim; check it against your invocation.

### `coverage_gate failed (missing matchers: ...)` on a fresh checkout

Your `~/.claude/settings.json` declares hooks with matchers that no eval in the suite under test exercises. Either add an eval covering the matcher or run with a suite that does. To diagnose without running the full pipeline:

```bash
uv run superclaude eval doctor --check-coverage --suite real
```

### `disk_budget_exceeded` mid-run

The poller (NFR-PERF4) tripped against `--max-disk-mb`. Unsubmitted specs synthesize `SKIPPED outcome (skip_reason="disk_budget_exceeded")`; in-flight workers run to completion. Either raise `--max-disk-mb` or split the suite into smaller batches.

### Run got interrupted (exit `3`)

A SIGINT / SIGTERM landed mid-run and cooperative cancellation drained. Unsubmitted specs receive a synthesized `INTERRUPTED` outcome. Re-running the same `--suite` + `--eval` selection picks up cleanly — runs do not share state.

### `_NullLifecycleExecutor active — non-production executor selected`

Expected on the current code path — the production lifecycle executor hasn't shipped yet, so `eval run` is wired to the null executor and **the WARNING is emitted to stderr on every run** (M2 / CC3). Run results from the null executor MUST NOT be treated as authoritative. The warning will stop firing once the production executor replaces the null stub.

---

## Reference

**Source modules:**
- [`src/superclaude/cli/eval/commands.py`](../../src/superclaude/cli/eval/commands.py) — Click subcommand definitions, `eval_group`, `eval_run`, `eval doctor`, `eval list`, `eval describe`
- [`src/superclaude/cli/eval/exit_codes.py`](../../src/superclaude/cli/eval/exit_codes.py) — canonical exit-code values
- [`src/superclaude/cli/eval/config.py`](../../src/superclaude/cli/eval/config.py) — `EvalConfig`, `SCRATCH_ROOT_POLICY`, `resolve_scratch_root`
- [`src/superclaude/cli/eval/artifact_layout.py`](../../src/superclaude/cli/eval/artifact_layout.py) — `compose_run_id`, `compose_run_dir`, `EVAL_ID_PATTERN` (FR-SCH2 schema regex)
- [`src/superclaude/cli/eval/coverage.py`](../../src/superclaude/cli/eval/coverage.py) — FR-G5 hook-matcher coverage gate
- [`src/superclaude/cli/eval/orchestrator.py`](../../src/superclaude/cli/eval/orchestrator.py) — `RunOrchestrator`, `allocate_session_id`
- [`src/superclaude/cli/eval/reporter.py`](../../src/superclaude/cli/eval/reporter.py), [`run_report.py`](../../src/superclaude/cli/eval/run_report.py) — artifact writers

**Deep technical reference:**
- [`docs/eval/scratch-roots.md`](../eval/scratch-roots.md) — authoritative AC12 / OPS-002 policy text
- [`docs/eval/runtime.md`](../eval/runtime.md) — runtime architecture
- [`docs/eval/retention.md`](../eval/retention.md) — retention policy
- [`docs/eval/retry.md`](../eval/retry.md) — retry policy
- [`docs/eval/validation-commands.md`](../eval/validation-commands.md) — validation commands
- [`docs/eval/release-checklist.md`](../eval/release-checklist.md) — release process

**Specifications:**
- [`.dev/releases/current/cliEval/design-spec.md`](../../.dev/releases/current/cliEval/design-spec.md) — canonical design spec (FR-G1 … FR-G6, FR-CLI1 … FR-CLI4, FR-SCH1, FR-SCH2, etc.)

**Tests pinning these contracts:**
- `tests/cli/eval/test_exit_codes.py` — process-boundary exit-code contract
- `tests/cli/eval/test_scratch_root_allowlist.py` — AC12 enforcement
- `tests/cli/eval/test_eval_id_regex.py` — FR-SCH2 schema regex
- `tests/cli/eval/test_coverage_gate.py` — FR-G5 coverage gate
- `tests/cli/eval/test_eval_run.py` — `eval run` end-to-end
- `tests/cli/eval/test_orchestrator.py` — orchestrator + `allocate_session_id`

---

**Document provenance:** Generated 2026-05-22 against the post-remediation tree (TASK-RF-20260522-153212). Every flag declaration, exit code, layout invariant, and policy citation in this document was verified against the runtime via `uv run python -c "from superclaude.cli.eval.commands import eval_group; ...; CliRunner().invoke(eval_group, ['<sub>', '--help'])"`.
