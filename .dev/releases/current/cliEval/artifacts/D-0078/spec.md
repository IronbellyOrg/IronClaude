# D-0078 — TEST-007 Reporter contract tests

**Roadmap row:** R-078 (TEST-007)
**Phase task:** T04.17 (phase-4-tasklist.md §T04.17)
**Test module:** `tests/cli/eval/test_reporter_contract.py`
**Producers under test:**
- `src/superclaude/cli/eval/run_report.py` (FR-RPT1 / D-0054 / T03.11)
- `src/superclaude/cli/eval/reporter.py` (COMP-008 / D-0055 / T03.13)
- `src/superclaude/cli/eval/models.py::RunSummary.to_dict` (DM-004 / T03.09)
- `src/superclaude/cli/eval/schemas/summary.schema.json` (DM-012 / T03.10)

## 1. Goal

Pin the four load-bearing TEST-007 obligations the Reporter (COMP-008)
must satisfy for downstream consumers (CI summary jobs, the JUnit
pipeline, the `superclaude eval run` exit-code dispatcher). The Reporter
is the single point where the orchestrator's accounting becomes
machine-readable bytes; if its contract drifts, every downstream consumer
silently inherits the drift. These tests stand as the canonical
regression line.

## 2. Test matrix

The four pytest cases in `tests/cli/eval/test_reporter_contract.py`
correspond one-to-one with the TEST-007 scenarios named in the phase-4
tasklist:

| # | Scenario | Test function | Pins |
|---|---|---|---|
| 1 | **N'-vs-K equality** | `test_n_prime_equals_k_lets_every_emitter_render` | When `len(summary.evals) == counts.expanded_n_prime`, every emitter (`to_markdown`, `to_json`, `to_yaml`, `to_junit`) renders without raising; `Reporter.write(...)` drops the canonical four-file artefact set; JUnit `<testsuite tests="...">` mirrors `expanded_n_prime`. |
| 2 | **SKIPPED inclusion** | `test_skipped_rows_included_in_evals_with_skip_reason` | SKIPPED rows survive in `summary.json :: evals[]` with `status="SKIPPED"`, `skip_reason` and `skip_flag_triggered` populated; per-status `totals.skipped` and `counts.skipped_s` reflect the tally; the markdown table surfaces the same rows + reasons. |
| 3 | **Mismatch → exit code 2** | `test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two` | A mismatched summary (`len(evals) != counts.expanded_n_prime`) raises `ReporterContractViolation` from every emitter and from `write_aggregated_report` *before* any artefact is written to disk; `REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2`; the exception carries `expected`, `actual`, and `run_id` plus a diagnostic message including both sides of the mismatch. |
| 4 | **JSON schema fidelity** | `test_reporter_json_validates_against_summary_schema` | The JSON the Reporter renders validates against `summary.schema.json` (DM-012 / T03.10) on *both* the in-memory string from `Reporter.to_json()` and the bytes the writer drops on disk via `Reporter.write(...)`; both payloads compare equal so a refactor cannot divergence them. The fixture covers every distinct row class (PASS / SKIPPED / FAIL / ERRORED) so every `oneOf` branch in the schema is exercised. |

## 3. Fixture design

`_summary(evals=..., expanded_n_prime=..., kept_k=..., skipped_s=...)`
auto-derives the counts when overrides are not supplied. Overriding
`expanded_n_prime` to a value other than `len(evals)` is the canonical
way to construct the mismatch fixture: the Reporter sees
`len(evals) != counts.expanded_n_prime` and raises.

Fixtures are intentionally self-contained — they do not reuse
`test_run_report.py` helpers — so a refactor of the writer helpers
cannot quietly drop the contract guarantees this module pins.

## 4. Exit code 2 mapping (Scenario 3 detail)

Design-spec §4 maps the four eval-run exit codes as follows:

| Code | Meaning |
|---|---|
| 0 | All evals satisfied their `expects:` blocks; no FAIL / ERRORED / TIMEOUT / XPASS. |
| 1 | At least one eval failed; orchestrator finished cleanly. |
| **2** | **Harness contract error — the orchestrator's accounting and the rendered `evals[]` disagree. Reporter contract violation lives here.** |
| 3 | Interrupted (SIGINT) before the orchestrator completed. |

`REPORTER_CONTRACT_VIOLATION_EXIT_CODE` is the integer the CLI
dispatcher returns when it catches `ReporterContractViolation` — the
runner / orchestrator catches the exception at the run boundary and
exits with this constant. The test pins the constant value (`== 2`) so
a future refactor that changes the constant fails loudly here rather
than silently in a downstream consumer.

The TEST-008 exit-code suite (T04.19) covers the process-level exit
code through `subprocess.run` against `superclaude eval run`. This test
module pins the constant + exception type contract at the library
boundary; T04.19 will pin the same contract end-to-end at the process
boundary.

## 5. Acceptance criteria mapping

From phase-4-tasklist.md §T04.17:

| AC | Verified by |
|---|---|
| File `tests/cli/eval/test_reporter_contract.py` contains 4 tests covering N'-vs-K equality, skipped inclusion, mismatch failure, JSON schema fidelity. | The four tests enumerated in §2. |
| `uv run pytest tests/cli/eval/test_reporter_contract.py -v` exits 0 with all 4 passing. | `evidence/T04.17/test-output.txt` (4 passed). |
| Mismatch test asserts process exit code 2 and `ReporterContractViolation` raised. | `test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two` — both `REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2` and `isinstance(..., ReporterContractViolation)` are asserted, alongside the per-emitter raise checks. |
| `TASKLIST_ROOT/artifacts/D-0078/spec.md` records the test matrix. | This file. |

## 6. Cross-links

* FR-RPT1 (T03.11) — implements the N'-vs-K guard inside every renderer
  and writer; this test module is its canonical regression line.
* DM-012 (T03.10) — declares the `summary.schema.json` shape that
  Scenario 4 validates against.
* COMP-008 / T03.13 (`Reporter`) — the class-shaped surface this module
  exercises via `Reporter.to_markdown / to_json / to_yaml / to_junit /
  write`.
* TEST-008 (T04.19) — pins the same exit-code contract at the process
  boundary; together with this module the contract is verified at both
  the library boundary (library raise + constant) and the CLI boundary
  (subprocess returncode).
