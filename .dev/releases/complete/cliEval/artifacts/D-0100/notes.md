# D-0100 — Implementation notes

## How "zero violations" is established

`superclaude eval doctor --suite real --check-coverage` (commands.py:692-838) executes the
following sequence when `--suite` is set:

1. **Capability gates** — `build_doctor_report(...)` checks HARD binaries, Claude CLI version,
   `~/.claude/` presence, and the ptytest vendor row.
2. **Manifest resolution** — `resolve_suite_manifest("real", _DEFAULT_SUITES_DIR)` returns
   `src/superclaude/cli/eval/suites/real.yaml`. A missing path raises `SuiteNotFound` →
   exit 2.
3. **Loader validation** — `SuiteLoader().load(manifest_path)` runs FR-SCH1 (`suite.schema.json`)
   and FR-SCH2 (`validate_eval_id` regex) across every authored eval row, expanding the E2
   parameterize block into E2.1 / E2.2 / E2.3 in the process. Any schema or regex rejection
   raises `SuiteLoaderError` → exit 2 BEFORE the coverage gate runs.
4. **Coverage gate** — `coverage_gate(settings_path=~/.claude/settings.json, suite=<specs>, ...)`
   crosswalks the loader's `EvalSpec` tuple against the hooks.json matcher patterns. A missing
   matcher entry yields `CoverageResult.passed == False` → exit 2.
5. **Renderer** — checklist + coverage summary printed to stdout; warnings (none in this run)
   would go to stderr.

A 0 exit therefore implies:

- Every HARD capability is satisfied.
- The `real` manifest exists and parses against `suite.schema.json`.
- Every eval row (and every parameterize-expanded id) passes `validate_eval_id`.
- The matcher-coverage gate is green for all three v1 matcher families.

## Per-eval enumeration: doctor vs describe

The doctor command's primary stdout is the checklist; the per-eval roster is implicit in the
`coverage_map` (only auggie-family ids surface there) plus the `SuiteLoader` return value
(commands.py:788). The complete roster lives in `superclaude eval describe --suite real --json`,
which is captured in `describe-ids.txt` for the AC "All 15 evals (E1, E2.1-3, E3..E15) appear
in the doctor output". The describe output is the loader's projection of the same parsed
manifest the doctor consumed; both commands share `SuiteLoader().load(...)`.

## What this DOES NOT prove

- **Eval bodies pass `eval run`.** SC2 validates the manifest contract, not the runtime
  outcome. End-to-end run-green is the M5 exit criterion (CP-P05-END / T05.28) and runs at
  `--parallel 8` against the live PTY harness.
- **Hook scripts emit the OQ-2-frozen ledger rows.** T05.07..T05.21 evidence notes the
  pre-existing telemetry-emission gap (`logs/freshness.jsonl` vs the current scripts that
  write to `logs/freshness-hook.jsonl` / `state/reads.jsonl` / `state/bg-agents/`). T05.22
  is schema-coverage only; the script-side wiring is tracked separately.
- **`eval describe` body equality.** The describe output is a snapshot of the validated
  manifest; matching its content against D-0082 / D-0083..D-0099 happens per-eval in
  T05.02..T05.21, not here.

## Soft skips

Three SOFT-SKIP rows appear in the checklist; none are schema violations:

| Row | Reason | Impact on SC2 |
|---|---|---|
| `mcp_server.auggie-mcp` | binary not on PATH | none — capability gate is informational; `--no-mcp` would also skip. |
| `mcp_server.airis-mcp-gateway` | binary not on PATH | none — same as above. |
| `vendored.ptytest` | PTY vendor stub absent at `cli/eval/pty/__init__.py` | none — orthogonal to manifest validation; PTY landed in M2 / will land per T02.x. |

These are recorded in `sc2.log` for completeness; they do not gate SC2.
