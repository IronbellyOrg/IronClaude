# D-0072 — `eval run` FR-CLI1 flag wiring (COMP-001 / R-072)

**Task:** T04.10 (Phase 4, Roadmap R-072)
**Module:** `src/superclaude/cli/eval/commands.py` — `eval_run`
**Command surface:** `src/superclaude/cli/eval/commands.py:1542–1950`
**Helper layer:** `src/superclaude/cli/eval/commands.py:1294–1540` (T04.10 helpers anchored on FR-G4 `artifact_layout`)
**Tests:** `tests/cli/eval/test_eval_run.py` (16 cases)
**Status:** Implemented 2026-05-21

## Command export

```python
@eval_group.command("run")
@click.option("--suite", ...)
@click.option("--parallel", ...)
@click.option("--eval", "eval_ids", multiple=True, ...)
@click.option("--no-mcp", is_flag=True, ...)
@click.option("--no-pty", is_flag=True, ...)
@click.option("--output-dir", ...)
@click.option("--keep-home", is_flag=True, ...)
@click.option("--timeout-mult", ...)
@click.option("--max-disk-mb", ...)
@click.option("--json", "as_json", is_flag=True, ...)
@click.option("--verbose", is_flag=True, ...)
@click.option("--junit", is_flag=True, ...)
def eval_run(...) -> None:
    """Run a cliEval suite end-to-end (FR-CLI1 / D-0072)."""
```

## Flag → component wiring

The twelve FR-CLI1 flags fan out across the five M2/M3 surfaces:

| Flag | Component / Symbol | Source anchor | Behaviour |
|---|---|---|---|
| `--suite` | `resolve_suite_manifest` + `SuiteLoader.load` | `commands.py:1758,1765` | Resolves manifest by filesystem path, stem, or `name` field; `SuiteNotFound` → exit 2; `SuiteLoaderError` → exit 2. |
| `--parallel` | `RunOrchestrator.run(parallel=…)` | `commands.py:1681–1684,1881,1883` | Clamped to `[MIN_PARALLEL=1, MAX_PARALLEL=15]` (design-spec §11) before reaching the orchestrator. Below band ⇒ 1; above band ⇒ 15. |
| `--eval` | Post-expansion filter | `commands.py:1772–1783` | Repeatable; filters `parsed.evals` by id; unmatched ids ⇒ `EvalNotFound` exit 2. |
| `--no-mcp` | `CapabilityGates(skip_flags=("--no-mcp",))` | `commands.py:1810–1814` | Added to the gate's skip-flag tuple so MCP capabilities are marked `skipped-by-flag` (FR-G4). |
| `--no-pty` | `CapabilityGates(skip_flags=…)` **and** per-eval short-circuit on `spec.no_pty == "skip"` | `commands.py:1812–1813,1839–1850` | Two-stage: gate flag for FR-CLI1 contract; runtime DOC-OQ3 / R-077 check yields `SKIPPED` outcome with `skip_reason="--no-pty"` before any HOME allocation. |
| `--output-dir` | `resolve_scratch_root` → `EvalConfig.allowed_scratch_roots` | `commands.py:1716–1746` | Validated against AC12 / OPS-002 allowlist (`/tmp/eval-runs`, `<repo>/.dev/eval-runs`); rejection ⇒ `SCRATCH_ROOT_VIOLATION` exit 2. Defaults to `compose_run_dir(cwd, started_at, suite_name)`. |
| `--keep-home` | `EvalRunner.keep_home_on_pass` | `commands.py:1469` (via `_run_one_spec`) | Forwarded through `_run_one_spec` to the runner; default removes per-eval HOME on PASS. |
| `--timeout-mult` | `EvalRunner.default_timeout_sec` scaler | `commands.py:1686–1691,1457` | Validated `> 0` (else `HARD_FAIL` exit 2); scales the suite-wide fallback timeout per spec. |
| `--max-disk-mb` | `DiskBudgetPoller(max_disk_mb=…)` | `commands.py:1693–1699,1820–1823` | Validated `>= 0` (else `HARD_FAIL` exit 2); `0` disables the poller (NFR-PERF4). |
| `--json` | `click.echo(json.dumps(summary.to_dict(), indent=2, …))` | `commands.py:1923–1924` | Mirrors the on-disk `summary.json` to stdout. |
| `--verbose` | `_format_run_summary_line(summary, resolved_output)` | `commands.py:1925–1926,1526` | Prints `run <id>: <P>P/<F>F/<S>S in <duration>s -> <output_dir>` one-liner. |
| `--junit` | `Reporter(summary=summary, emit_junit=True)` | `commands.py:1918` | Reporter also writes `junit.xml` into `output_dir`. |

## Exit-code contract (design-spec §4)

| Exit | Cause | Path in `eval_run` |
|---|---|---|
| `0` `RUN_CLEAN_EXIT_CODE` | Every expanded eval reached PASS / SKIPPED / XFAIL with no breach. | `commands.py:1950` |
| `1` `RUN_FAILURES_EXIT_CODE` | ≥1 outcome in FAIL / ERRORED / TIMEOUT / XPASS. | `commands.py:1944–1949` |
| `2` Various `HARD_FAIL`-class codes | Flag validation, `ScratchRootViolation`, `SuiteNotFound`, `SuiteLoaderError`, `EvalNotFound`, coverage-gate fail, disk-budget breach. | `commands.py:1691,1699,1733,1761,1768,1782,1801,1942–1943` |
| `3` `RUN_INTERRUPTED_EXIT_CODE` | Operator interrupt (SIGINT/SIGTERM) propagated via `CancellationToken`. | `commands.py:1931–1932` |

## Pipeline ordering (top-of-run → bottom-of-run)

The command sequences component invocations so harness-level rejections short-circuit BEFORE any worker dispatch:

1. **Flag validation + clamp** (lines 1681–1699) — `--parallel`, `--timeout-mult`, `--max-disk-mb`.
2. **Single clock read** (line 1707) — feeds both `_new_run_id` and `RunSummary.started_at`.
3. **AC12 scratch-root resolution** (lines 1716–1746) — `resolve_scratch_root` then `mkdir(parents=True)`; `home_root` derived under `output_dir`.
4. **Suite resolution + parse + post-expansion filter** (lines 1758–1783).
5. **FR-G5 coverage gate** (lines 1794–1801, T04.14 / D-0075).
6. **CapabilityGates construction** (lines 1809–1815) — skip flags carried; `check_all()` deliberately not called here.
7. **Disk budget + cancellation token + signal handler** (lines 1820–1825).
8. **Worker closure** (lines 1832–1860) — `--no-pty` short-circuit BEFORE `_run_one_spec`.
9. **Orchestrate** (lines 1870–1889) — `SignalHandlerInstaller` install guarded by `_can_install_signal_handler`.
10. **Assemble RunSummary + Reporter.write** (lines 1897–1918) — counts, totals, artifacts, junit.
11. **Stdout surface** (lines 1923–1926) — `--json` xor `--verbose`.
12. **Exit code mapping** (lines 1931–1950).

## T04.10 helper symbols

Eight module-private helpers anchor the body (`commands.py:1294–1540`). The names are pinned by `tests/cli/eval/test_single_command.py::_eval_run_body_incomplete`:

| Helper | Purpose | Anchor |
|---|---|---|
| `_utc_iso_now` | Single UTC ISO clock read for run-id + summary stamps. | `commands.py:1308` |
| `_new_run_id` | FR-G4 `compose_run_id(started_at, suite_name)` wrapper. | `commands.py:1322` |
| `_default_output_dir` | FR-G4 `compose_run_dir` default when `--output-dir` is omitted. | `commands.py:1335` |
| `_can_install_signal_handler` | Main-thread guard for `SignalHandlerInstaller`. | `commands.py:1346` |
| `_NullLifecycleExecutor` | M2/M3 zero-side-effect executor; production wiring lands M5/M6. | `commands.py:1361` |
| `_resolve_executor_factory` | Factory injection point for tests. | `commands.py:1390` |
| `_run_one_spec` | Per-spec runner: `HomeIsolation` + `EvalRunner` wiring. | `commands.py:1405` |
| `_compute_run_stats` | DM-012 `RunCounts` + `RunTotals` tally. | `commands.py:1477` |
| `_format_run_summary_line` | `--verbose` one-liner formatter. | `commands.py:1526` |

## Acceptance bullets

| AC | How satisfied |
|---|---|
| `superclaude eval run --help` lists all 12 flags named in FR-CLI1 | `test_eval_run_help_lists_all_twelve_flags` asserts each flag literal is in the rendered output. |
| `--parallel 0` clamps to 1; `--parallel 16` clamps to 15 | `test_parallel_zero_clamps_to_one` + `test_parallel_sixteen_clamps_to_fifteen` patch `RunOrchestrator` and assert on the captured `parallel` kwarg. |
| `--output-dir` resolves through AC12 allowlist | `test_output_dir_outside_allowlist_exits_scratch_root_violation` asserts a `tmp_path`-rooted directory exits 2 with the OPS-002 banner. |
| A one-eval run completes end-to-end with `--suite real --eval E1` | `test_run_real_suite_no_pty_skips_e1_and_exits_clean` runs the full pipeline with `--no-pty`; asserts exit 0 + `summary.{md,json}` on disk + `E1` SKIPPED + `skip_reason="--no-pty"`. |
| `D-0072/spec.md` documents flag wiring | This file. `test_d0072_spec_documents_flag_wiring` pins the deliverable. |

## Scope boundary

T04.10 covers the **command body**: flag declarations, validation,
helper wiring, orchestrator construction, and exit-code mapping. It
does **not** ship the production `LifecycleExecutor`: that lands in
M5 / M6 alongside the vendored PTY harness. Until then the only
operator-reachable green path is `--no-pty`, which short-circuits
every eval in `real.yaml` (DOC-OQ3 / R-077 tags every E1-E15 row
`no_pty: skip`). Synthetic suites whose specs lack the tag fall
through to `_NullLifecycleExecutor` (zero-side-effect PASS) so the
end-to-end stack stays exercisable.

FR-G6 single-command runnability (T04.11) consumes this command via
`subprocess.run` and asserts the literal AC invocation
`uv run superclaude eval run --suite real --eval E1` exits 0 with
`summary.{md,json}` on disk. That smoke test currently skips on the
``--no-pty`` precondition until the M5 PTY harness lands; the
acceptance bullets above pin the same surface via Click's
`CliRunner` so M2/M3 coverage is unconditional.
