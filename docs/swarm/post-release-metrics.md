# Post-Release Metrics Review Framework

**Deliverable:** OPS-006 (R-155 / T09.07, D-0136) — MultiModelSwarm Phase 9
Operational Handoff.

**Audience:** Release owners and operators running the post-release review for the
`superclaude swarm` orchestrator.

This document defines (1) the post-release metrics to track, (2) the artifacts
each metric is derived from, (3) the review window, and (4) the
backlog-feedback loop that turns findings into work items.

> **No metrics-export pipeline ships in v1.** Automated Prometheus /
> OpenMetrics export is explicitly **DEFERRED** per the parent spec —
> `merged-requirements.compressed.md:724`: *"Prometheus / OpenMetrics output
> at event boundaries? **Defer.**"* There is no scrape endpoint, no exporter,
> and no time-series backend. Every metric below is derived **manually or by an
> ad-hoc script** from the artifacts the orchestrator already writes to each
> job's `--output` directory. This doc does **not** claim a telemetry pipeline
> that does not exist.

## Source artifacts (what we read, not what we scrape)

Every metric is derived from one of the three artifacts the orchestrator emits
into each job's `--output` directory. No additional instrumentation exists in
v1.

| Artifact | What it contains | Per-job |
|---|---|---|
| `return-contract.yaml` | DM-012 `ResultContract`: `status` (`success` / `partial` / `failed`), `workers_requested`, `workers_succeeded`, `workers_failed`, `elapsed_ms`, `output_files[]` (each a `WorkerResult` with per-worker `status`, `elapsed_ms`, `attempts`, `http_code`, `model_label`), `merged_path`, `lens`, `caller_metadata` (carries `suspect` + `tier`). | one |
| `execution-log.jsonl` | Append-only event stream: `worker_start` / `worker_progress` / `worker_done` records (each with `timestamp`, `worker_index` (int or null), `payload` incl. `status` and `elapsed_ms`); the authoritative event surface. | one |
| `.swarm-state.json` | DM-014 `SwarmState`: `job_id`, current phase (`preflight_ok` / `reducing` / terminal), `updated` timestamp. Used to detect resume usage and stalled jobs. | one |

A companion `execution-log.md` (human-readable) mirrors the JSONL but the JSONL
is authoritative; do not parse the Markdown for metrics.

**Collection model:** point a script at the set of `--output` directories from
the review window, parse the YAML/JSONL/JSON above, and aggregate. There is no
push, no scrape, no exporter. If automated export is wanted later, that is a
**future** work item (see Prometheus-deferred note above), not a v1 capability.

## Metrics to track

All metrics are derived by aggregating the per-job artifacts above across the
review window. Each row names the exact field(s) and source artifact so the
metric can be re-derived without guesswork.

### M1 — Run outcome rates (success / partial / failed)

- **Definition:** fraction of jobs in each terminal class.
- **Source:** `return-contract.yaml` → `status` (one of `success` /
  `partial` / `failed`, the IMM-5 enum). Count occurrences per value, divide
  by total jobs.
- **Why:** the headline health signal; a rising `partial`/`failed` share is the
  primary post-release regression indicator.

### M2 — Per-worker M/N (succeeded vs requested)

- **Definition:** per job, `workers_succeeded` / `workers_requested`; aggregate
  as a distribution (and a mean fill rate) across jobs.
- **Source:** `return-contract.yaml` → `workers_requested`,
  `workers_succeeded`, `workers_failed` (INV-005 invariant:
  `workers_succeeded + workers_failed == workers_requested`).
- **Why:** distinguishes "lens fully fanned out" from "ran degraded but still
  passed the partial floor." Cross-check against M1.

### M3 — Worker failure rate by cause

- **Definition:** count of failed workers grouped by failure signature.
- **Source:** `return-contract.yaml` → `output_files[]` per-worker `status` +
  `http_code` + `attempts`; corroborate against `execution-log.jsonl`
  `worker_done` payloads. Group by `http_code` (e.g. 5xx vs timeout) and by
  retry exhaustion (`attempts` > 1).
- **Why:** separates transport flakiness (retried 5xx) from hard failures.

### M4 — `elapsed_ms` distributions (job-level and per-worker)

- **Definition:** distribution (p50 / p95 / max) of job wall-clock and of
  per-worker wall-clock.
- **Source:** `return-contract.yaml` → top-level `elapsed_ms` (job) and
  `output_files[].elapsed_ms` (per worker). For finer event timing, diff
  `worker_start`/`worker_done` timestamps in `execution-log.jsonl`.
- **Why:** latency budget tracking and slow-model detection (group per-worker
  `elapsed_ms` by `model_label`).

### M5 — Suspect-flag frequency

- **Definition:** fraction of jobs whose lens emitted `suspect=true` (the
  bare_review lens is the canonical `suspect=true` lens, COMP-024).
- **Source:** `return-contract.yaml` → `caller_metadata.suspect` (FR-020
  expansion stamps `suspect` + `tier`).
- **Why:** measures how often the FR-020 suspect path fires, which gates the
  recommended-next-command remediation handoff.

### M6 — Resume usage

- **Definition:** count of jobs that were resumed rather than run fresh.
- **Source:** `.swarm-state.json` presence + non-terminal phase transitions
  (`preflight_ok` / `reducing`) across the job's lifetime, corroborated by
  re-entry events in `execution-log.jsonl`.
- **Why:** validates the resume contract is exercised in real operation
  (Open Question 3 audience); high resume rates may indicate instability.

### M7 — Amalgamation-mode mix

- **Definition:** distribution of jobs by `amalgamation_mode`
  (`raw` / `normalize` / `normalize+merge`) and merge-emission rate.
- **Source:** `return-contract.yaml` → `amalgamation_mode` and whether
  `merged_path` is non-null (null when mode ≠ `normalize+merge` or
  `workers_succeeded` < 2).
- **Why:** confirms merge is used as designed and surfaces jobs that wanted a
  merge but fell below the 2-worker floor.

> **Minimum bar (T09.07 validation):** at least M1–M5 above are tracked, plus
> a scheduled review window. M6–M7 are recommended additions.

## Review window

- **Cadence:** a single **2-week post-release review**, scheduled to begin on
  the 14th calendar day after the MultiModelSwarm v1 production-handoff date
  (M9 exit). A follow-up review at the 6-week mark is optional and triggered
  only if the first review flags an open regression.
- **Window date:** `<set on M9 exit: release_date + 14 days>` —
  **HUMAN-DECISION.** This date is bound at release time; it is **not**
  auto-stamped by this doc. Record the concrete date and the named owner in the
  Phase 9 exit checkpoint (`phase-9-cp2.md`) when the release lands.
- **Owner:** `<release owner — named at M9 exit>`. The owner runs the
  collection script over the window's `--output` directories, fills the M1–M7
  table, and chairs the review.
- **Inputs:** the full set of per-job `return-contract.yaml` /
  `execution-log.jsonl` / `.swarm-state.json` artifacts produced during the
  window. No external dashboard is consulted (none exists — see the
  Prometheus-deferred note).

## Backlog-feedback loop

The review exists to convert observed signal into tracked work. The loop:

1. **Collect.** Owner runs the aggregation script over the window's artifacts
   and produces the M1–M7 figures.
2. **Compare against thresholds.** Flag any metric that crosses a review
   threshold, e.g.:
   - M1 `failed` rate above the team's tolerance, or any upward `partial`
     trend.
   - M3 a recurring `http_code` / retry-exhaustion signature.
   - M4 p95 `elapsed_ms` regression vs the release baseline.
   - M5 suspect-flag frequency materially higher or lower than expected for the
     deployed lens mix.
3. **Triage to backlog.** For each flagged metric, file a backlog item that
   cites the metric ID (M1–M7), the source artifact field, and at least one
   example `job_id` (from `return-contract.yaml` / `.swarm-state.json`) as
   evidence. No finding is "noted and dropped" — it either becomes a backlog
   item or is explicitly recorded as within-tolerance with a reason.
4. **Prioritize.** Release owner assigns severity; transport-flakiness items
   (M3 retried 5xx) rank below hard-failure or latency-regression items.
5. **Close the loop.** Resolved backlog items that change orchestrator behavior
   feed the next release's regression baseline (new expected M1/M4 values).

This loop is **manual** by design in v1. Automating the collect/compare steps
into a scheduled exporter is the deferred Prometheus/OpenMetrics work — out of
scope here.

## References

- **OPS-006 / R-155 / T09.07 / D-0136** — this deliverable
  (`.dev/releases/complete/MultiModelSwarm/tasklist/phase-9-tasklist.md:208`).
- **Prometheus/OpenMetrics DEFERRED** — parent spec
  `.dev/releases/complete/MultiModelSwarm/merged-requirements.compressed.md:724`
  ("Prometheus / OpenMetrics output at event boundaries? **Defer.**").
- **Emitted artifacts** — DM-012 `ResultContract` / DM-014 `SwarmState` /
  COMP-012 JSONL+Markdown logger
  (`src/superclaude/cli/swarm/{reduce,models,logging_}.py`).
- **Related operational docs** — `docs/swarm/observability-procedure.md`
  (OPS-003, artifact debugging recipes), `docs/swarm/operator-runbook.md`
  (OPS-001, run/status/logs/watch/resume workflows),
  `docs/swarm/monitoring-patterns.md` (wait patterns).
