# MultiModelSwarm — Operator Workflow Runbook

> 📚 Part of the [swarm documentation](./README.md). This runbook is organized
> **one section per operator workflow verb** — **run, status, logs, watch,
> resume, kill, attach** — and gives a single-line `superclaude swarm …`
> command for each. For per-flag detail and exit codes see the
> [Command Reference](./command-reference.md) (the authority for every flag
> cited here); for environment / Rich TUI / T2 proxy / tmux setup see the
> [Operator Runbook → environment material](./runbook.md).
>
> **Roadmap:** OPS-001 / R-150 (Phase 9 / T09.01). This file is the
> workflow-organized companion to the AC-organized [runbook.md](./runbook.md);
> it cross-references that file rather than duplicating its env/TUI/tmux/proxy
> sections.

## Scope and conventions

This runbook walks an operator through the lifecycle of a swarm job using
only commands that exist in the [Command Reference](./command-reference.md).
Two of the seven workflows are **flags on `run` / `status`**, not standalone
subcommands:

- **resume** = `swarm run --resume JOB_ID --output DIR`
- **watch** = `swarm status --watch …` (and the `logs --follow` live-tail)

All commands run through the project's UV environment — prefix with
`uv run` per the [Environment Mandate](./runbook.md#environment-mandate-ac-001).
The global exit-code convention is `0` success · `1` rule/contract failure ·
`2` usage error; per-command specifics are in the
[Command Reference](./command-reference.md).

**Sibling OPS docs** (cross-linked where relevant):

- [env-readiness.md](./env-readiness.md) — environment readiness check (OPS-002).
- [observability-procedure.md](./observability-procedure.md) — state / log / sentinel artifacts + debugging recipes (OPS-003).
- [rollback-procedure.md](./rollback-procedure.md) — rollback + detached-disable + artifact preservation (OPS-004).

## run — dispatch a swarm job

Start a job. A `run` executes **Wave 0 preflight → Wave 1 dispatch** and, when
`--output` is supplied, writes the observability artifacts the other workflows
read. The simplest entry point is the lens shortcut:

```bash
uv run superclaude swarm run --lens bare-review --target src/foo.py --output out --transport stub
```

Other input modes (all from the [run reference](./command-reference.md#swarm-run)):

```bash
# Full JobSpec file (positional SPEC_PATH)
uv run superclaude swarm run job.json --output out --transport stub

# JobSpec from stdin
uv run superclaude swarm scaffold --lens refactor-find | uv run superclaude swarm run --stdin --target src/foo.py --output out

# Real T2 proxy fan-out (see runbook env contract before running)
uv run superclaude swarm run --lens bare-review --target src/foo.py --output out --transport openai_compat
```

**Key flags** (per the [run reference](./command-reference.md#swarm-run)):
`--lens`, `--target`, `--output`, `--transport stub|openai_compat`, `--stdin`,
`--detached`, `--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label`,
`--auto-inject-guard`.

> `--auto-inject-guard` is a `run` flag; the custom prompt directory itself is
> **not** a `swarm run` CLI option — it is the JobSpec `custom_prompt_dir` field,
> set in a spec file (validated only for `--lens custom`). See the
> [run reference](./command-reference.md#swarm-run).

- `--output DIR` wires all observability artifacts — **without it, a spec-file
  run dispatches but writes nothing**. It is required with `--lens` and
  `--resume`.
- `--detached` launches inside a `tmux` session `swarm-<job_id>`; exits `2` if
  tmux is unavailable (no silent inline fallback). See
  [runbook.md → tmux is Optional](./runbook.md#tmux-is-optional-ac-008) and the
  [attach](#attach--re-attach-to-a-detached-job) / [kill](#kill--terminate-a-detached-job)
  sections below.

Before running against `--transport openai_compat`, confirm the proxy env with
[env-readiness.md](./env-readiness.md) (OPS-002) and the
[T2 Proxy Env Contract](./runbook.md#t2-proxy-env-contract-ac-017).

**Exit codes:** `0` dispatched · `1` preflight failed (structured rule block on
stderr) · `2` usage error (unknown lens, conflicting input modes, `--detached`
without tmux). The four-file fresh-run artifact set is documented in
[observability-procedure.md](./observability-procedure.md) (OPS-003) and the
[run artifacts reference](./command-reference.md#run-artifacts).

## status — check a job's wave phase

Report the job's current phase from `<DIR>/.swarm-state.json`. Phases progress
`preflight_ok` → `dispatching` → `normalizing` → `reducing` → `terminal`:

```bash
uv run superclaude swarm status --output out
```

Guard against running it against the wrong directory by pinning the expected
job id (a mismatch exits `2`):

```bash
uv run superclaude swarm status --output out --job lens-bare-review-ab12cd34
```

A single status line looks like:

```text
status: phase=terminal job_id=lens-bare-review-ab12cd34 updated=2026-06-09T00:18:03Z
```

**Key flags** (per the [status reference](./command-reference.md#swarm-status)):
`--output` (required), `--job`, `--watch`, `--watch-interval`,
`--watch-max-iterations`. For continuous polling, see
[watch](#watch--poll-until-terminal) below.

**Exit codes:** `0` non-terminal phase, terminal+success, or terminal with
unreadable contract · `1` terminal+partial/failed (requires the M5 contract) ·
`2` usage error (dir/state missing, corrupt JSON, `--job` mismatch). The
state-file artifact is detailed in
[observability-procedure.md](./observability-procedure.md) (OPS-003).

## logs — dump or tail a job's execution log

Show the execution log. The Markdown surface (`--md`, default) is human-facing;
the JSONL surface (`--jsonl`) is the same record stream for piping into `jq`:

```bash
uv run superclaude swarm logs --output out
```

```bash
# Machine surface, last 20 lines
uv run superclaude swarm logs --output out --jsonl --lines 20
```

Live-tail a running job (polls until terminal or Ctrl-C). `--tail` is the
shorthand for `--jsonl --follow`:

```bash
uv run superclaude swarm logs --output out --follow
```

```bash
uv run superclaude swarm logs --output out --tail
```

**Key flags** (per the [logs reference](./command-reference.md#swarm-logs)):
`--output` (required), `--job`, `--jsonl` / `--md`, `--follow` / `-f`,
`--tail`, `--lines`, `--watch-interval`, `--watch-max-iterations`.

**Exit codes:** `0` read OK / follow exited cleanly · `2` usage error
(`--output` missing, log file missing, `--job` mismatch). The JSONL and
Markdown log layers and debugging recipes live in
[observability-procedure.md](./observability-procedure.md) (OPS-003); CI
wait-on-a-job patterns are in
[monitoring-patterns.md](./monitoring-patterns.md).

## watch — poll until terminal

There is no standalone `watch` subcommand. Watching is the `--watch` flag on
`status` (phase polling) and the `--follow` / `--tail` flags on `logs` (event
polling). To watch the wave phase re-emit one grep-friendly line per poll until
the job reaches `terminal` (or Ctrl-C):

```bash
uv run superclaude swarm status --output out --watch
```

Tune the cadence and (mainly for tests) cap the number of polls:

```bash
uv run superclaude swarm status --output out --watch --watch-interval 5
```

```bash
uv run superclaude swarm status --output out --watch --watch-interval 1 --watch-max-iterations 60
```

To watch the event stream instead of the phase, use the `logs` live-tail from
the [logs](#logs--dump-or-tail-a-jobs-execution-log) section
(`--follow` honours its own `--watch-interval`, default `0.5s`).

**Key flags** (per the [status reference](./command-reference.md#swarm-status)):
`--watch`, `--watch-interval` (default `2.0`, min `0.01`),
`--watch-max-iterations`.

**Exit codes:** inherited from `status` — `2` on usage error (missing dir/state,
`--job` mismatch); otherwise per the terminal phase. The three CI/automation
"ways to wait on a job" are catalogued in
[monitoring-patterns.md](./monitoring-patterns.md), with the durable artifacts
they read in [observability-procedure.md](./observability-procedure.md)
(OPS-003).

## resume — rehydrate a job and skip succeeded workers

There is no standalone `resume` subcommand. Resume is the `--resume JOB_ID` flag
on `run`. It rehydrates from `<DIR>/manifest.json`, skips any worker whose
`*.meta.json` reports `status=success`, and re-runs Wave 2 normalize + Wave 3
reduce. `--output` must point at the **original** job directory:

```bash
uv run superclaude swarm run --resume lens-bare-review-ab12cd34 --output out --transport openai_compat
```

To re-resolve the lens-derived prompt/recipe fields from the **current**
registry on resume (FR-025), add `--force-relens`:

```bash
uv run superclaude swarm run --resume lens-bare-review-ab12cd34 --output out --force-relens
```

**Key flags** (per the [run reference](./command-reference.md#swarm-run)):
`--resume` (requires `--output`; mutually exclusive with `SPEC_PATH` /
`--stdin` / `--lens` / `--detached`), `--force-relens` (requires `--resume`),
`--output`, `--transport`.

**Resume emits more than a fresh run.** Because it re-runs Wave 2/3, a resumed
`<DIR>` additionally contains `return-contract.yaml`, `done.json`, the
per-worker normalized outputs, and `merged.md` when
`amalgamation_mode == normalize+merge` — see the
[run artifacts reference](./command-reference.md#run-artifacts) and
[observability-procedure.md](./observability-procedure.md) (OPS-003).

**Exit codes:** as for `run` — `0` dispatched · `1` preflight/contract failure ·
`2` usage error.

## kill — terminate a detached job

Tear down the `swarm-<JOB_ID>` tmux session for a job launched with
`run --detached`. The command is idempotent — killing an already-terminated job
is a clean no-op:

```bash
uv run superclaude swarm kill lens-bare-review-ab12cd34
```

Pass `--output` to also flip `<DIR>/.swarm-state.json` to `terminal` and write
`done.json` with `terminal_status=killed`, so polling consumers (`status`,
`logs`, `monitoring-patterns.md` waiters) observe the termination:

```bash
uv run superclaude swarm kill lens-bare-review-ab12cd34 --output out
```

**Key flags** (per the [kill reference](./command-reference.md#swarm-kill)):
positional `JOB_ID`, optional `--output DIR`.

**Exit codes:** `0` terminated cleanly OR no live session present · `2` usage
error (tmux missing, nested tmux, illegal `JOB_ID`, or `--output` not a
directory). See [runbook.md → tmux is Optional](./runbook.md#tmux-is-optional-ac-008)
for the tmux dependency, and
[rollback-procedure.md](./rollback-procedure.md) (OPS-004) for disabling
detached mode as a rollback lever.

## attach — re-attach to a detached job

Re-attach your terminal to a detached `swarm-<JOB_ID>` tmux session. It blocks
until you detach (Ctrl-b d) or the session ends, and takes no options:

```bash
uv run superclaude swarm attach lens-bare-review-ab12cd34
```

If there is no live session for `JOB_ID`, attach is a graceful no-op (so poll
wrappers don't error). To inspect a job you can't attach to — already terminal,
or run inline without `--detached` — read its artifacts with
[status](#status--check-a-jobs-wave-phase) and
[logs](#logs--dump-or-tail-a-jobs-execution-log) instead, neither of which needs
tmux.

**Arguments** (per the [attach reference](./command-reference.md#swarm-attach)):
positional `JOB_ID` only — no flags.

**Exit codes:** `0` attached+detached cleanly OR no live session for `JOB_ID` ·
non-zero propagated from tmux on its own failure · `2` tmux not installed,
caller already nested in tmux, or `JOB_ID` has tmux-illegal characters. See
[runbook.md → tmux is Optional](./runbook.md#tmux-is-optional-ac-008).

## See also

- [Command Reference](./command-reference.md) — authoritative per-flag detail and exit codes for all eight subcommands.
- [runbook.md](./runbook.md) — environment mandate (AC-001), Rich TUI (AC-007), T2 proxy env contract (AC-017), tmux modes (AC-008).
- [env-readiness.md](./env-readiness.md) — environment readiness check + script (OPS-002).
- [observability-procedure.md](./observability-procedure.md) — state file / JSONL log / Markdown log / done sentinel + debugging recipes (OPS-003).
- [rollback-procedure.md](./rollback-procedure.md) — rollback, detached-disable, artifact preservation (OPS-004).
- [monitoring-patterns.md](./monitoring-patterns.md) — three CI/automation ways to wait on a job.

> Authored for OPS-001 / R-150 (Phase 9 / T09.01). Examples are drawn from the
> [Command Reference](./command-reference.md); regenerate from the live
> `uv run superclaude swarm <cmd> --help` surface if flags drift.
