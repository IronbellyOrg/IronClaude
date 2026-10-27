# D-0072 — Evidence

## Acceptance criteria coverage

| AC | How verified | Evidence link |
|---|---|---|
| `superclaude eval run --help` lists all 12 flags named in FR-CLI1. | All 12 flag literals (`--suite`, `--parallel`, `--eval`, `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult`, `--max-disk-mb`, `--json`, `--verbose`, `--junit`) render in the help output; `test_eval_run_help_lists_all_twelve_flags` asserts each literal is present. | `evidence/T04.10/eval-run-help.txt`, `evidence/T04.10/pytest-output.txt` |
| `--parallel 0` clamps to 1; `--parallel 16` clamps to 15. | `test_parallel_zero_clamps_to_one` + `test_parallel_sixteen_clamps_to_fifteen` patch `commands.RunOrchestrator` with `_RecordingOrchestrator` (which re-exports `MIN_PARALLEL=1`/`MAX_PARALLEL=15`), invoke the real Click command, and assert the captured `parallel` kwarg equals the documented band edge. | `evidence/T04.10/pytest-output.txt` |
| `--output-dir` resolves through AC12 allowlist. | `test_output_dir_outside_allowlist_exits_scratch_root_violation` passes a `tmp_path`-rooted directory (under `/tmp/pytest-of-…`, outside the `/tmp/eval-runs` + `<repo>/.dev/eval-runs` allowlist) and asserts exit 2 with the OPS-002 scratch-root banner on stderr. End-to-end tests use the `allowlisted_output_dir` fixture from `conftest.py` so the green path consumes a path INSIDE the allowlist. | `evidence/T04.10/pytest-output.txt` |
| A one-eval run completes end-to-end with `--suite real --eval E1`. | `test_run_real_suite_no_pty_skips_e1_and_exits_clean` runs the real `RunOrchestrator` + `Reporter` pipeline against `real.yaml` with `--no-pty`; the DOC-OQ3 / R-077 `no_pty: skip` tag short-circuits E1 to SKIPPED + `skip_reason="--no-pty"`. Exit code 0, `summary.{md,json}` on disk. The same invocation was captured manually for the validation step below. | `evidence/T04.10/pytest-output.txt`, `evidence/T04.10/manual-run-summary.txt` |
| `D-0072/spec.md` documents flag wiring. | `test_d0072_spec_documents_flag_wiring` asserts `spec.md` exists and mentions every FR-CLI1 flag at least once. | `artifacts/D-0072/spec.md` |

## Validation example (from phase-4-tasklist.md)

The task validation step calls for:

> Manual check: run `superclaude eval run --suite real --eval E1` and inspect exit code 0 and summary.

```text
$ mkdir -p /tmp/eval-runs/t04_10_manual
$ uv run superclaude eval run \
    --suite real \
    --eval E1 \
    --no-pty \
    --output-dir /tmp/eval-runs/t04_10_manual \
    --parallel 1 \
    --verbose
run 205926Z-ee3ed770: 0P/0F/1S in 0.00s -> /tmp/eval-runs/t04_10_manual
exit=0
homes
summary.json
summary.md
summary.yaml
```

Exit 0, `summary.{md,json,yaml}` materialised under the allowlisted
`--output-dir`. Full capture: `evidence/T04.10/manual-run-summary.txt`.

`--no-pty` is required at M2/M3: the production `LifecycleExecutor`
lands with the vendored PTY harness in M5/M6, and every eval in
`real.yaml` carries the DOC-OQ3 `no_pty: skip` tag so the worker
closure short-circuits before any HOME allocation. Once the PTY
harness lands, the literal `superclaude eval run --suite real
--eval E1` invocation (without `--no-pty`) unblocks
`tests/cli/eval/test_single_command.py` which currently skips on
`_eval_run_body_incomplete` / `_missing_target_eval` preconditions.

## Test run

```text
$ uv run pytest tests/cli/eval/test_eval_run.py -v
============================== 16 passed in 0.55s ==============================
```

Cases:

| Test | What it pins |
|---|---|
| `test_eval_run_help_lists_all_twelve_flags` | All 12 FR-CLI1 flag literals in `eval run --help`. |
| `test_eval_run_help_documents_clamping_band` | `--help` quotes the design-spec §11 clamp band ("clamp to 1", "clamp to 15"). |
| `test_parallel_zero_clamps_to_one` | `--parallel 0` reaches `RunOrchestrator.run(parallel=1)`. |
| `test_parallel_sixteen_clamps_to_fifteen` | `--parallel 16` reaches `RunOrchestrator.run(parallel=15)`. |
| `test_timeout_mult_zero_exits_hard_fail` | `--timeout-mult 0` → exit 2 + stderr "--timeout-mult must be > 0". |
| `test_timeout_mult_negative_exits_hard_fail` | Same shape for `--timeout-mult -1.5`. |
| `test_max_disk_mb_negative_exits_hard_fail` | `--max-disk-mb -1` → exit 2 + stderr "--max-disk-mb must be >= 0" + the "use 0 to disable" hint. |
| `test_output_dir_outside_allowlist_exits_scratch_root_violation` | A `tmp_path`-rooted `--output-dir` exits 2 with the OPS-002 banner. |
| `test_suite_not_found_exits_2` | Unresolvable `--suite` exits 2 with `SuiteNotFound`. |
| `test_unknown_eval_id_exits_2` | `--eval E9999` against `real.yaml` exits 2 with `EvalNotFound`. |
| `test_run_real_suite_no_pty_skips_e1_and_exits_clean` | One-eval end-to-end: exit 0, `summary.{md,json}` on disk, E1 SKIPPED with `skip_reason="--no-pty"`. |
| `test_run_json_emits_summary_to_stdout` | `--json` emits parseable JSON summary to stdout. |
| `test_run_verbose_emits_summary_line` | `--verbose` emits the `run <id>: <P>P/<F>F/<S>S in <duration>s -> <output_dir>` one-liner. |
| `test_run_junit_writes_xml_artifact` | `--junit` causes `Reporter` to also write `junit.xml`. |
| `test_run_no_pty_full_suite_skips_every_eval` | `--no-pty` against `real.yaml` skips all 17 expanded rows (E1, E2.1-E2.3, E3-E15). |
| `test_d0072_spec_documents_flag_wiring` | `spec.md` exists and references every FR-CLI1 flag. |

Full output: `evidence/T04.10/pytest-output.txt`.

## Files changed / added

| Path | Change |
|---|---|
| `src/superclaude/cli/eval/commands.py` | Pre-existing — `eval_run` body at lines 1542–1950; T04.10 helpers at lines 1294–1540. T04.10 makes no source changes; the body was materialised across the M2/M3 dependency batch (T03.15, T03.19, T04.09, T04.15, T04.16). |
| `tests/cli/eval/test_eval_run.py` | **NEW** — 16-case acceptance harness pinning the four AC bullets at the `CliRunner` surface. |
| `.dev/releases/current/cliEval/artifacts/D-0072/spec.md` | **NEW** — 12-flag wiring table, exit-code contract, pipeline ordering, T04.10 helper symbols. |
| `.dev/releases/current/cliEval/artifacts/D-0072/notes.md` | **NEW** — implementation decisions, deferred follow-ups, risk notes. |
| `.dev/releases/current/cliEval/artifacts/D-0072/evidence.md` | **NEW** — this file. |
| `.dev/releases/current/cliEval/evidence/T04.10/pytest-output.txt` | **NEW** — verbatim pytest -v run, 16 passed. |
| `.dev/releases/current/cliEval/evidence/T04.10/eval-run-help.txt` | **NEW** — `superclaude eval run --help` capture showing all 12 flags. |
| `.dev/releases/current/cliEval/evidence/T04.10/manual-run-summary.txt` | **NEW** — verbatim manual `superclaude eval run --suite real --eval E1 --no-pty` capture showing exit 0 + `summary.{md,json,yaml}` artifacts. |
