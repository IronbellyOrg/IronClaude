# D-0059 — NFR-PERF2 concurrency resource bounds (RAM ceiling + free-RAM precheck)

| Field | Value |
|---|---|
| Task | T03.17 |
| Roadmap row | R-059 |
| Deliverable | D-0059 |
| Phase | 3 (Execution Engine and Reporter) |
| Spec source | design-spec §11 NFR-PERF2 |
| Status | LANDED (2026-05-20) |

## Contract

> Peak resident-set size MUST stay `<= 2.25 GB` when `--parallel 15` is in
> effect on the dev host (linux, 4 GB+ free RAM). The doctor MUST warn
> when free RAM is insufficient before accepting `--parallel 15`. Hosts
> with `<4 GB` free RAM are out-of-scope per infrastructure notes.

## Implementation surface

### Ceiling constants — `src/superclaude/cli/eval/commands.py`

- `RAM_CEILING_GB: float = 2.25` — design-spec §11 NFR-PERF2 number.
- `RAM_CEILING_BYTES: int = int(2.25 * 1024**3) = 2_415_919_104`.
- `RAM_CEILING_TEXT: str = "2.25 GB"` — the literal token operator-facing
  strings MUST contain (asserted by tests).
- `PARALLEL_RAM_GATE_THRESHOLD: int = 15` — matches
  `RunOrchestrator.MAX_PARALLEL`.

### Doctor precheck — `_check_free_ram_for_parallel` (SOFT-SKIP)

Signature:

```python
def _check_free_ram_for_parallel(
    *,
    requested_parallel: int | None,
    probe: Callable[[], int | None] | None = None,
    ceiling_bytes: int = RAM_CEILING_BYTES,
    threshold_parallel: int = PARALLEL_RAM_GATE_THRESHOLD,
) -> CapabilityStatus | None:
```

Behaviour matrix:

| `requested_parallel` | probe returns | result                                                |
|----------------------|---------------|-------------------------------------------------------|
| `None`               | n/a           | `None` (gate inactive)                                |
| `< 15`               | n/a           | `None` (gate inactive)                                |
| `>= 15`              | `>= 2.25 GB`  | `CapabilityStatus(passed=True, failure_mode="skip")`  |
| `>= 15`              | `<  2.25 GB`  | `CapabilityStatus(passed=False, failure_mode="skip")` |
| `>= 15`              | `None`        | `CapabilityStatus(passed=False, failure_mode="skip")` |
| `>= 15`              | raises        | `CapabilityStatus(passed=False, failure_mode="skip")` |

Failure-mode classification is always `"skip"` (SOFT-SKIP) so a host
with insufficient RAM does not block legitimate `--parallel 8` runs.
The detail string ALWAYS contains `"2.25 GB"` when the gate fires, so a
grep against the operator-facing artifact pins the cause without parsing
structure.

### Probe — `_default_free_ram_probe`

Reads `/proc/meminfo` (Linux only), preferring `MemAvailable` over
`MemFree` because `MemAvailable` accounts for reclaimable cache the way
an oncoming allocation would. Returns `None` on any failure (non-Linux,
locked-down container, missing keys). The doctor records a "probe
unavailable" SOFT-SKIP rather than crashing — a doctor that crashes on
tight hosts is worse than one that warns.

### CLI — `eval doctor --parallel <INT>`

- New `--parallel` option (type `int`, default `None`).
- When supplied AND `>= 15`, `build_doctor_report` consults the probe
  and appends a `host.free_ram_for_max_parallel` row to the report.
- On SOFT-SKIP, the CLI echoes a stderr warning of the shape:

  ```
  eval doctor: NFR-PERF2 warning: free RAM <N.NN> GB < 2.25 GB ceiling for --parallel 15
  ```

  The warning fires regardless of `--json` so CI logs and machine
  consumers see the same signal; the JSON payload also carries the row
  under `soft_skips` for structured parsing.
- Exit code is still 0 — SOFT-SKIP does not promote to HARD-fail.

### Benchmark — `tests/cli/eval/test_perf_resource_bounds.py`

`TestPerfResourceBoundsAtMaxParallel::test_peak_rss_within_ceiling_at_parallel_fifteen`:

1. Snapshot baseline `ru_maxrss` (POSIX stdlib `resource.RUSAGE_SELF`).
2. Spawn 15 stub workers via `RunOrchestrator` at
   `parallel = RunOrchestrator.MAX_PARALLEL`. Each worker holds at a
   barrier so the orchestrator's pool is at saturation when the snapshot
   fires.
3. Release the barrier, snapshot peak `ru_maxrss`.
4. Compute `delta_rss = max(0, peak - baseline)`.
5. Assert `delta_rss <= RAM_CEILING_BYTES`.
6. Write `perf-ram.json` describing the ceiling, the host snapshot, the
   delta, and the pass/xfail status.

Host-limitation carve-out: when `/proc/meminfo` reports `< 4 GB` free
RAM (or the procfs is unavailable), the test calls `pytest.xfail()`
with a documented reason. The AC explicitly allows this since the
NFR-PERF2 bench is gated to dev hosts at or above the 4 GB floor.

`ru_maxrss` units differ by platform: Linux reports kilobytes, macOS
reports bytes. `_ru_maxrss_bytes()` normalises both.

### Evidence sink — `CLIEVAL_PERF_RAM_REPORT_PATH`

Honoured by the benchmark to redirect `perf-ram.json` to the M3 release
evidence directory:

```
CLIEVAL_PERF_RAM_REPORT_PATH=<TASKLIST_ROOT>/evidence/T03.17/perf-ram.json
```

When unset the report lands in pytest's `tmp_path` — the test still
produces a verifiable artifact, just not at the release path.

## Schema — `perf-ram.json`

| Key                    | Type            | Meaning                                                |
|------------------------|-----------------|--------------------------------------------------------|
| `task`                 | string          | `"T03.17"`                                             |
| `deliverable`          | string          | `"D-0059"`                                             |
| `roadmap_row`          | string          | `"R-059"`                                              |
| `nfr`                  | string          | `"NFR-PERF2"`                                          |
| `ceiling_bytes`        | int             | `RAM_CEILING_BYTES`                                    |
| `ceiling_text`         | string          | `"2.25 GB"`                                            |
| `parallel`             | int             | concurrency the bench actually used (15 at the bench)  |
| `spec_count`           | int             | number of stub specs (15 at the bench)                 |
| `baseline_rss_bytes`   | int             | `ru_maxrss` snapshot before the orchestrator run       |
| `peak_rss_bytes`       | int             | `ru_maxrss` snapshot after the orchestrator returned   |
| `delta_rss_bytes`      | int             | `max(0, peak - baseline)`                              |
| `delta_rss_gb`         | float           | `delta_rss_bytes / (1024**3)` rounded to 4 dp          |
| `host_free_ram_bytes`  | int or null     | `/proc/meminfo` `MemAvailable` (or `MemFree`) snapshot |
| `host_free_ram_gb`     | float or null   | rounded view                                           |
| `host_platform`        | string          | `platform.platform()`                                  |
| `host_xfail_reason`    | string or null  | populated when the bench xfailed                       |
| `within_ceiling`       | bool            | `delta_rss_bytes <= ceiling_bytes`                     |

`test_perf_ram_report_schema_is_stable` pins the key set so a future
patch that drops a field fails CI instead of silently breaking downstream
tooling.

## Acceptance verification

| AC bullet                                                        | Evidence                                                                          |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Benchmark confirms peak RSS `<=2.25 GB` at `--parallel 15`       | `evidence/T03.17/perf-ram.json` (`within_ceiling=true`, `delta_rss_gb=0.0002`)    |
| Doctor emits warning containing `"2.25 GB"` on insufficient RAM  | `tests/cli/eval/test_doctor.py::test_cli_doctor_parallel_15_low_ram_emits_2_25_gb_warning` |
| `perf-ram.json` saved to `TASKLIST_ROOT/evidence/T03.17/`        | `evidence/T03.17/perf-ram.json`                                                   |
| `artifacts/D-0059/spec.md` documents ceiling and precheck        | this file                                                                         |

## Dependencies

- T03.15 (RunOrchestrator) — provides `RunOrchestrator.MAX_PARALLEL`.
- T03.16 (FR-G2 15-eval integration) — provides the parallel-15 wiring
  the benchmark mirrors.
- T01.13 (FR-CLI4 doctor) — provides the `eval doctor` Click group and
  `CapabilityStatus` shape the new check produces.
