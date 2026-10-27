# D-0059 — Design Notes

**Task:** T03.17 — Verify NFR-PERF2 concurrency resource bounds
**Roadmap row:** R-059
**NFR:** NFR-PERF2 (`peak RSS ≤ 2.25 GB at --parallel 15`)

This file captures the non-obvious design decisions behind the D-0059
implementation. The contract and verification matrix live in
[`spec.md`](spec.md); summary numbers live in [`evidence.md`](evidence.md).

---

## 1. Two-tier check: SOFT-SKIP at doctor, xfail at benchmark

The free-RAM precheck in `eval doctor` records a `CapabilityStatus` with
`failure_mode="skip"` rather than `"hard"`. The benchmark in
`tests/cli/eval/test_perf_resource_bounds.py` `xfail`s when the host
reports `<4 GB` free RAM.

**Why not HARD-fail in doctor?** A `failure_mode="hard"` row would cause
`build_doctor_report().passed == False`, which currently gates the entire
eval pipeline. Most contributors will never use `--parallel 15` (default
is 8 or lower); blocking their `eval doctor` run on a measurement that
only matters at saturation would create friction with no safety benefit.

**Why a warning at all?** The CI matrix and release benchmark *do* run
at `--parallel 15`. The SOFT-SKIP row + stderr warning gives those
runners a visible signal without breaking the boot of low-spec dev hosts.

**Why xfail (not skip) in the benchmark?** Skipping silently is the
wrong default for a measurement test: a future CI host with tight RAM
could mask a real regression. `xfail(reason=…, strict=False)` keeps the
test visible in the report and records the host limitation in
`perf-ram.json` (`host_xfail_reason` field).

## 2. `/proc/meminfo` over `psutil`

`uv run python -c "import psutil"` returns `ModuleNotFoundError` in this
project's `.venv`. Adding `psutil` as a runtime dep just to read free
RAM would be disproportionate.

`_default_free_ram_probe()` parses `/proc/meminfo` directly:

- prefers `MemAvailable:` (kernel ≥ 3.14) — accounts for reclaimable
  page cache, which is what we actually have to spend
- falls back to `MemFree:` on ancient kernels
- returns `None` on non-Linux hosts (no `/proc/meminfo`) — the precheck
  treats `None` as "cannot verify, surface as warning" rather than
  silently passing, so macOS / BSD CI hosts still get the row

The probe is dependency-injected (`free_ram_probe` parameter on
`build_doctor_report` and `_check_free_ram_for_parallel`) so tests can
inject deterministic byte counts without touching the host.

## 3. Platform-aware `ru_maxrss`

`resource.getrusage(RUSAGE_SELF).ru_maxrss` returns:

- **Linux:** kilobytes
- **macOS / BSD:** bytes

The benchmark normalises via `_ru_maxrss_bytes()`:

```python
if platform.system() == "Darwin":
    return int(raw)
return int(raw) * 1024
```

This matches the POSIX reality (POSIX leaves the unit unspecified;
Linux and macOS picked different conventions). Without this, the same
test would silently report values 1024× off on macOS runners.

## 4. Threading barrier in the benchmark

`_make_stub_worker(hold_event)` parks each worker on `hold_event.wait()`
after allocating a 1 KiB payload. A `threading.Timer(0.5s)` releases
the barrier.

**Why a barrier?** `ThreadPoolExecutor.map` with fast workers can drain
the queue serially — the snapshot then captures one or two workers, not
all 15. The barrier guarantees all 15 worker threads are simultaneously
holding their payload when the snapshot fires, which is the worst case
the ceiling is meant to protect against.

The 1 KiB allocation is deliberately small. The point of this benchmark
is to verify the *harness overhead* stays under the ceiling — payload
size is a parameter the eval pipeline controls separately. A larger
allocation would conflate harness RSS with workload RSS and make the
ceiling meaningless.

## 5. Evidence sink via `CLIEVAL_PERF_RAM_REPORT_PATH`

The benchmark writes `perf-ram.json` to:

1. `os.environ["CLIEVAL_PERF_RAM_REPORT_PATH"]` when set (release /
   evidence-harvest mode), OR
2. `tmp_path / "perf-ram.json"` (default — keeps unit-test runs hermetic)

This avoids the alternative of either (a) hardcoding the evidence
directory into the test (breaks CI sandboxing) or (b) requiring a
fixture-based factory that every CI runner has to know about.

The env-var contract is documented in `spec.md §4` and in the
benchmark module docstring.

## 6. Constants centralised, not hardcoded

`RAM_CEILING_GB`, `RAM_CEILING_BYTES`, `RAM_CEILING_TEXT`, and
`PARALLEL_RAM_GATE_THRESHOLD` live as module-level constants in
`src/superclaude/cli/eval/commands.py`. The invariant
`RAM_CEILING_BYTES == int(RAM_CEILING_GB * 1024**3)` is asserted by
`test_ram_ceiling_bytes_matches_text` so a future edit that changes the
text without the byte count (or vice versa) trips immediately.

The warning string `"2.25 GB"` is checked in two CLI tests — both
assert against `RAM_CEILING_TEXT` rather than the literal, so the
constant remains the single source of truth.

---

## Pointers

- Contract: [`spec.md`](spec.md) §1
- Implementation surface: [`spec.md`](spec.md) §2
- Evidence summary: [`evidence.md`](evidence.md)
- Raw evidence: `../../evidence/T03.17/perf-ram.json`,
  `../../evidence/T03.17/pytest-output.txt`
