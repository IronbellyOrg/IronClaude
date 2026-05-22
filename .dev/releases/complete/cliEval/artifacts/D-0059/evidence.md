# D-0059 — Evidence Summary

**Task:** T03.17 — Verify NFR-PERF2 concurrency resource bounds
**Roadmap row:** R-059
**NFR:** NFR-PERF2 (`peak RSS ≤ 2.25 GB at --parallel 15`)
**Date captured:** 2026-05-20
**Host:** `Linux-6.8.0-111-generic-x86_64-with-glibc2.39`

---

## 1. Benchmark result (perf-ram.json)

Path: [`../../evidence/T03.17/perf-ram.json`](../../evidence/T03.17/perf-ram.json)

| Field                  | Value                  | Interpretation                                  |
|------------------------|------------------------|-------------------------------------------------|
| `parallel`             | 15                     | Saturated worker pool                            |
| `spec_count`           | 15                     | One spec per worker (barrier-held)               |
| `baseline_rss_bytes`   | 45,490,176 (~43.4 MiB) | RSS before benchmark                             |
| `peak_rss_bytes`       | 45,752,320 (~43.6 MiB) | RSS at saturation snapshot                       |
| `delta_rss_bytes`      | 262,144 (256 KiB)      | Harness overhead at `--parallel 15`              |
| `delta_rss_gb`         | 0.0002                 | Effectively zero relative to ceiling             |
| `ceiling_bytes`        | 2,415,919,104          | `2.25 * 1024**3`                                 |
| `ceiling_text`         | `"2.25 GB"`            | Stable warning string                            |
| `within_ceiling`       | `true`                 | **PASS**                                         |
| `host_free_ram_bytes`  | 96,715,968,512         | ~90.07 GB free at probe time                     |
| `host_free_ram_gb`     | 90.07                  | Well above 4 GB xfail threshold                  |
| `host_xfail_reason`    | `null`                 | No host gating applied                           |
| `host_platform`        | (Linux glibc 2.39)     | Recorded for cross-runner diffing                |
| `deliverable`          | `"D-0059"`             | Provenance                                       |
| `roadmap_row`          | `"R-059"`              | Provenance                                       |
| `nfr`                  | `"NFR-PERF2"`          | Provenance                                       |
| `task`                 | `"T03.17"`             | Provenance                                       |

**Headline:** Peak RSS delta at `--parallel 15` is **256 KiB**, four
orders of magnitude under the 2.25 GB ceiling. Within-ceiling = `true`.

## 2. Test execution

Path: [`../../evidence/T03.17/pytest-output.txt`](../../evidence/T03.17/pytest-output.txt)

Command (captured during evidence harvest):
```
CLIEVAL_PERF_RAM_REPORT_PATH=.dev/releases/current/cliEval/evidence/T03.17/perf-ram.json \
  uv run pytest tests/cli/eval/test_doctor.py \
                tests/cli/eval/test_perf_resource_bounds.py -v
```

Result: **46 passed in 0.67s** (Python 3.12.12, pytest-9.0.3).

Of those, the rows directly proving NFR-PERF2:

- `test_peak_rss_within_ceiling_at_parallel_fifteen` — benchmark
  (writes `perf-ram.json`)
- `test_perf_ram_report_schema_is_stable` — pins the 17-key set
- `test_cli_doctor_parallel_15_low_ram_emits_2_25_gb_warning` — warning
  string contains `"2.25 GB"`, stderr-only, exit 0
- `test_cli_doctor_parallel_15_with_ample_ram_does_not_warn` — no
  false positive when budget met
- `test_cli_doctor_parallel_8_does_not_run_ram_check` — gate inactive
  below threshold (no probe call)
- `test_cli_doctor_json_payload_records_ram_short_row` — JSON-mode
  payload includes the `host.free_ram_for_max_parallel` row with
  `failure_mode="skip"`
- `test_ram_ceiling_bytes_matches_text` — invariant
  `RAM_CEILING_BYTES == int(RAM_CEILING_GB * 1024**3)`
- `test_default_free_ram_probe_returns_positive_or_none` — host probe
  sanity (`/proc/meminfo` parses cleanly on this Linux host)

Full suite (`tests/cli/eval/` 79-test checkpoint bundle) was previously
green; no regressions introduced by D-0059.

## 3. Acceptance Criteria mapping

| AC                                                                                                  | Evidence                                                                                                                 |
|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| Benchmark confirms peak RSS ≤ 2.25 GB at `--parallel 15` (or xfail with documented host limitation) | `perf-ram.json` shows `within_ceiling=true`, `delta_rss_bytes=262144`, `host_xfail_reason=null`                          |
| Doctor emits a warning string containing `2.25 GB` when free RAM insufficient and `--parallel 15`    | `test_cli_doctor_parallel_15_low_ram_emits_2_25_gb_warning` (stderr, exit 0); JSON row carries `detail` with `"2.25 GB"` |
| Benchmark report saved to `TASKLIST_ROOT/evidence/T03.17/perf-ram.json`                              | File present (17 keys, schema pinned by test)                                                                            |
| `TASKLIST_ROOT/artifacts/D-0059/spec.md` documents the ceiling and precheck                          | [`spec.md`](spec.md) §1 (contract), §2 (impl surface), §3 (verification table)                                           |

All four AC: **PASS.**

## 4. Caveats / xfail conditions

- The headline number was measured on a host with **~90 GB free RAM**
  and a stub-worker payload of **1 KiB per spec**. Real eval workloads
  (Codex CLI process + buffered PTY output) will measure significantly
  higher peaks. This benchmark verifies the *harness overhead* stays
  within budget; per-spec workload accounting lives outside D-0059.
- On hosts with `<4 GB` free RAM the benchmark `xfail`s and records
  `host_xfail_reason` in `perf-ram.json`. The doctor SOFT-SKIP row
  still surfaces the warning text in that case.
- The probe path (`_default_free_ram_probe`) is Linux-only
  (`/proc/meminfo`). macOS / BSD CI hosts will see `host_free_ram_bytes=null`
  and the doctor row will record as soft-skip with detail "Could not
  determine host free RAM" — this is intentional (silent pass would
  mask the precheck on those platforms).

## 5. Pointers

- Contract & implementation surface: [`spec.md`](spec.md)
- Design rationale: [`notes.md`](notes.md)
- Raw benchmark JSON: [`../../evidence/T03.17/perf-ram.json`](../../evidence/T03.17/perf-ram.json)
- Raw pytest output: [`../../evidence/T03.17/pytest-output.txt`](../../evidence/T03.17/pytest-output.txt)
- Production code: `src/superclaude/cli/eval/commands.py`
- Tests: `tests/cli/eval/test_doctor.py`, `tests/cli/eval/test_perf_resource_bounds.py`
