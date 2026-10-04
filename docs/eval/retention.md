# Eval Artifact Retention Policy (OPS-003)

**Status:** Stable as of T04.21 (Phase 4, D-0081 / R-081). Updated 2026-05-22 post cliEval Phase 5+6 remediation (TASK-RF-20260522-153212) — run-dir date segment changed from `<ISO>` to `<YYYY-MM-DD>` per the canonical `compose_run_dir` output; `summary.yaml` added to the always-emitted artifact set per M4 (Reporter + write_aggregated_report parity). Pins the
operator-visible retention contract for `superclaude eval run` artifacts
on every termination path (clean exit, per-eval FAIL/ERROR, harness
abort on disk-budget breach, SIGINT/SIGTERM cancellation).

## TL;DR

`superclaude eval run` is **biased toward preserving evidence**. The
default behaviour is:

* The **run directory** under `--output-dir` (default `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`,
  anchored via `compose_run_dir` per FR-G4) is **never cleaned up automatically**,
  regardless of exit code.
* **Run-level summaries** (`summary.md`, `summary.json`, `summary.yaml`, `junit.xml`
  when `--junit` is set) are written before the process exits and are retained on every
  termination path — including SIGINT, harness abort, and disk-budget
  breach.
* **Per-eval HOME directories** under the scratch root follow status:
  * PASS → removed (default) unless `--keep-home` is passed.
  * FAIL / ERRORED / TIMEOUT → **always kept** for forensic inspection.
  * Setup failure (NFR-ISO2) → kept with a `.eval-meta/setup_failed`
    tag pinning the exception class / message.
* On a **disk-budget breach** (exit code 2) the dispatcher writes a
  `disk_budget_exceeded.json` side-car and emits an
  [OPS-003 retention-advice string](#disk-budget-breach-advice) to
  stderr so the operator knows what was preserved and which knobs to
  turn on the next invocation.

```text
DiskBudgetPoller.ARTIFACT_NAME = "disk_budget_exceeded.json"
DISK_BUDGET_EXCEEDED_EXIT_CODE  = 2
HomeIsolation.SETUP_FAILED_TAG_RELPATH = ".eval-meta/setup_failed"
EvalRunner._finalize keep semantics: keep = True if status != "PASS" else keep_home_on_pass
```

## 1. Run directory: never auto-cleaned

`--output-dir` (default the FR-G4 layout root `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`,
anchored via `compose_run_dir`) is treated as **append-only** by the harness. Nothing
the orchestrator writes is ever rewound. Specifically:

> **H1 / FR-G4 anchor:** When `--output-dir <X>` is supplied, the FR-G4 layout is
> layered underneath: `<X>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`. The supplied path
> is the OUTPUT ROOT, not the run-dir. (Post-H1 fix in cliEval Phase 5+6 remediation
> — see [AC matrix row H1](../../.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/reports/06-ac-matrix.md).)

* The orchestrator never deletes a previously-written run directory.
* The Reporter writes `summary.md`, `summary.json`, `summary.yaml`, and (when
  `--junit` is on) `junit.xml` *just before* the process exits on
  every termination branch documented in [design-spec §4][ds-4] —
  including:
  * Clean run (exit 0)
  * One or more FAIL / ERROR / TIMEOUT outcomes (exit 1)
  * Harness contract violation / disk-budget breach (exit 2)
  * Cooperative cancellation (SIGINT/SIGTERM → exit 3)
* The summaries record `counts.expanded == K` against
  `counts.manifest_n == N'` so the FR-RPT1 invariant is preserved even
  on a partial run.

Operators are expected to garbage-collect old run directories manually
(or via a periodic CI cleaner). The harness does not ship its own
sweeper because there is no safe default — a CI runner that times out
its job at the 15-minute mark must NOT discover its artifacts have been
swept by a sibling job's harness invocation.

[ds-4]: ../../.dev/releases/current/cliEval/design-spec.md

## 2. `--keep-home`: per-eval HOME retention on PASS

`--keep-home` is a Click flag forwarded into
`EvalRunner.keep_home_on_pass`. The default is **False** — PASS evals
have their scratch HOME (`<scratch-root>/<run-id>/<eval-id>/`) removed
during the FR-LC1 step-7 teardown. Failing evals, errored evals, and
timed-out evals **always** preserve their HOME for inspection
regardless of `--keep-home`.

| Outcome status | `--keep-home` False (default) | `--keep-home` True |
|---|---|---|
| PASS | HOME removed | HOME preserved |
| FAIL | HOME preserved | HOME preserved |
| ERRORED | HOME preserved | HOME preserved |
| TIMEOUT | HOME preserved | HOME preserved |
| SKIPPED | (HOME never allocated) | (HOME never allocated) |
| Setup failure (NFR-ISO2) | HOME preserved, tagged | HOME preserved, tagged |

The keep/remove decision is centralised in
`src/superclaude/cli/eval/runner.py::_finalize`:

```python
keep = True if status != "PASS" else keep_home_on_pass
_safe_teardown(home, keep=keep, on_teardown_error=on_teardown_error)
```

Teardown errors are routed through `on_teardown_error` so they cannot
flip a PASS into a FAIL — the design-spec invariant is that teardown
is best-effort.

## 3. NFR-ISO2: setup failures always preserve the HOME

The atomic-setup contract (NFR-ISO2 / T02.13) catches any exception
thrown by the per-eval setup pipeline (`HomeIsolation.acquire`),
writes a `.eval-meta/setup_failed` artifact tag inside the partially-
materialised HOME, and re-raises the exception unchanged. The HOME is
**not** torn down on the failure path; the runner reports the eval as
ERRORED and the HOME remains on disk with its setup_failed tag.

The tag's filename is pinned by
`HomeIsolation.SETUP_FAILED_TAG_RELPATH = ".eval-meta/setup_failed"`.
The first line of the tag is the exception class (e.g.
`builtins.PermissionError`), followed by the stringified message and
the traceback. Operators can grep for this file under the scratch root
to find every HOME that crashed during setup.

This policy applies regardless of `--keep-home`: setup failures
always preserve evidence because the failure happened *before* any
per-eval body could write a transcript that would otherwise carry the
diagnostic signal.

## 4. Disk-budget breach: advice + side-car

On every disk-budget breach (NFR-PERF4 — see
[`docs/eval/runtime.md`](runtime.md) and design-spec §13), the
`DiskBudgetPoller` writes a `disk_budget_exceeded.json` side-car into
the run directory naming the measured usage, budget, output dir, and
breach timestamp. The orchestrator synthesises `SKIPPED` outcomes for
every unsubmitted spec with `skip_reason="disk_budget_exceeded"` so the
N'-vs-K invariant is preserved. In-flight workers run to completion;
the poller never kills a worker.

### Disk-budget breach advice

Before exiting with code 2 the Phase 4 dispatcher emits this verbatim
string to stderr:

```text
disk-budget exceeded: the run was aborted to protect the host filesystem. The run directory, summary.{md,json}, junit.xml, per-eval artifacts for finished evals, and disk_budget_exceeded.json side-car are retained for forensic inspection. Raise --max-disk-mb (or set to 0 to disable the budget) and/or pass --keep-home False on the next invocation; see docs/eval/retention.md for the full OPS-003 retention policy.
```

The advice text is pinned in
`src/superclaude/cli/eval/disk_budget.py::DISK_BUDGET_RETENTION_ADVICE`
and is the **single source of truth** for the OPS-003 retention
advice. This document quotes that constant verbatim, the CLI dispatcher
echoes that constant verbatim, and
`tests/cli/eval/test_retention_policy.py` asserts both surfaces carry
the same bytes. Drift between the doc, the CLI, and the constant is
therefore a test failure rather than a silent operator surprise.

## 5. Cancellation (SIGINT/SIGTERM)

When the cooperative cancellation token fires (exit code 3 per
[design-spec §4][ds-4]) the orchestrator stops accepting new submissions
but lets in-flight workers complete naturally. Every outcome the
runner emitted is committed to `summary.{md,json,yaml}` / `junit.xml`
before the process exits. The run directory is not cleaned up;
operators can re-run with `--eval <id>` to retry the specs that were
cancelled mid-flight (see [retry.md](retry.md)).

## 6. Summary retention matrix

| Exit code | Run dir | summary.{md,json,yaml} | junit.xml | Per-eval artifacts (passed evals) | Per-eval artifacts (failed evals) | Per-eval HOMEs |
|---|---|---|---|---|---|---|
| 0 (clean) | kept | kept | kept (when `--junit`) | kept | n/a | passes follow `--keep-home`; others n/a |
| 1 (failures) | kept | kept | kept | kept | kept | passes follow `--keep-home`; failures kept |
| 2 (harness abort) | kept | kept (partial run, N'-vs-K preserved) | kept | kept | kept | passes follow `--keep-home`; failures + setup-fail kept; unsubmitted = SKIPPED (no HOME) |
| 3 (interrupted) | kept | kept (partial run) | kept | kept | kept | passes follow `--keep-home`; in-flight cancelled outcomes kept |

## 7. Operator playbook

When a `superclaude eval run` exits with code 2 (disk-budget breach),
the operator can recover with this sequence:

1. Read the OPS-003 stderr advice (rendered immediately before the
   exit) for the run-dir path and the recommended knobs.
2. `cat <run-dir>/disk_budget_exceeded.json` to confirm which budget
   was breached (`usage_bytes`, `budget_bytes`, `ticked_at`).
3. Inspect `<run-dir>/summary.md` / `summary.json` / `summary.yaml` for the partial
   run — `counts.expanded` will be < `counts.manifest_n` and
   `counts.skipped` will include the `disk_budget_exceeded` skip
   reason.
4. Garbage-collect old run dirs under `--output-dir` (the harness will
   never auto-prune them) and re-run with a larger `--max-disk-mb`
   (or `--max-disk-mb 0` to disable the budget when CI gives you a
   dedicated runner).
5. To re-run only the unfinished specs, pass
   `--eval <id1> --eval <id2> ...` for the SKIPPED rows. See
   [retry.md](retry.md) for the subset-replay contract.

When a `superclaude eval run` exits with code 1 (per-eval failures):

1. Inspect `<run-dir>/summary.md` for the FAIL / ERROR / TIMEOUT
   rows. Each row's `artifacts` mapping cross-links to
   `per-eval/<eval-id>/logs.jsonl` and `per-eval/<eval-id>/tty.transcript`.
2. The per-eval HOME under `<scratch-root>/<run-id>/<eval-id>/` is
   preserved — `cd` into it to reproduce the failing eval's
   filesystem state.
3. `ls **/.eval-meta/setup_failed` under the scratch root to find any
   setup failures and pivot to their captured exception.

## See also

* [`docs/eval/runtime.md`](runtime.md) — disk-budget poller (NFR-PERF4),
  concurrency knobs, and timeout semantics.
* [`docs/eval/scratch-roots.md`](scratch-roots.md) — scratch-root
  resolution rules and the `.eval-meta` directory layout.
* [`docs/eval/retry.md`](retry.md) — re-running failed evals via
  `--eval <id>`.
* [`.dev/releases/current/cliEval/design-spec.md`][ds-4] — §4 CLI
  surface, §10 risk matrix (R4), §13 NFR-PERF4 disk-budget poller.
* [`.dev/releases/current/cliEval/artifacts/D-0081/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0081/spec.md)
  — D-0081 deliverable spec for OPS-003.
