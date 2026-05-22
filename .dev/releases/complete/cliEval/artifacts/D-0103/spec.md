# D-0103 — TEST-014 `--no-mcp` skip semantics

**Owner task:** T05.26 (phase-5 tasklist)
**Roadmap link:** R-102
**Dependencies:** T01.11 (CapabilityGates), T03.11 (FR-RPT1), T04.10 (run-helpers)
**Test module:** `tests/cli/eval/test_no_mcp_skip.py`

## 1. Purpose

Pin the contract that `superclaude eval run --suite real --no-mcp`
classifies every MCP-dependent eval (E1, E2.1, E2.2, E2.3) as `SKIPPED`
with a populated `skip_reason`, and that the resulting `RunSummary`
satisfies the DM-012 dimensional invariant
`kept_k + skipped_s == counts.expanded_n_prime`. The mitigation is the
R9 PR scope creep guard: a reviewer on a host without MCP capability
must still be able to exercise the harness end-to-end and see the four
contract-bearing rows in the summary.

## 2. Surfaces under test

| Surface | Source | What TEST-014 pins |
|---|---|---|
| Manifest | `src/superclaude/cli/eval/suites/real.yaml` | `optional_capabilities[].gate_flag == "--no-mcp"` for every `mcp_server.*` row; E1 / E2.1-3 declare a matching `requires:` tuple. |
| Gate | `CapabilityGates` (`capabilities.py`:221+) | `CapabilityGates(skip_flags={"--no-mcp"})` puts every MCP cap into `soft_skips` with `skipped_by_flag=True` regardless of probe result (override semantics). |
| Outcome shape | `EvalOutcome` (`models.py`:284+) | Skip rows carry `status="SKIPPED"`, populated `skip_reason="capability_gate:<cap>"`, and `skip_flag_triggered="--no-mcp"`. |
| Counts | `RunCounts` (`models.py`:733+) | `counts.kept_plus_skipped_equals_n_prime` is `True`; `RunSummary.__post_init__` rejects any inconsistent flag value. |
| Runtime | `eval_run.run_one` (`commands.py`:1530+) | Closure short-circuits MCP-tagged specs BEFORE `_run_one_spec` is called when `--no-mcp` is active. (Wiring lands at T04.x; the M2 closure currently honours only `--no-pty`.) |

## 3. Skip-reason format

Canonical format the closure SHOULD emit (matches the convention
established by `test_reporter_contract.py::_skipped`):

```
skip_reason         = "capability_gate:<capability-name>"
skip_flag_triggered = "--no-mcp"
```

`<capability-name>` is the first `mcp_server.*` entry in
`spec.requires` that intersects the gate's `soft_skips` set. The
informational `skip_flag_triggered` is documented but TEST-014 only
asserts that `skip_reason` is non-empty (per task note: "The DM-001
`skip_flag_triggered` field is informational only; TEST-014 does not
require asserting its value beyond `skip_reason` being populated.").

## 4. Acceptance criteria (T05.26 verbatim)

1. File `tests/cli/eval/test_no_mcp_skip.py` exits 0 asserting MCP
   evals classify SKIPPED with non-empty `skip_reason` under `--no-mcp`.
2. RunSummary `counts.kept_plus_skipped_equals_n_prime` is True under
   the skip scenario.
3. Each SKIPPED eval entry includes a populated `skip_reason` value.
4. `TASKLIST_ROOT/artifacts/D-0103/spec.md` records the skip semantics.
   *(this file)*

## 5. Test layout

The test module is organised into four sections (mirroring TEST-007 /
TEST-013 conventions):

* **AC1 — manifest**:
  `test_real_suite_lists_no_mcp_gate_flag_in_optional_capabilities`,
  `test_real_suite_mcp_evals_carry_mcp_server_requires`.
* **AC2 — gate primitive**:
  `test_capability_gates_no_mcp_flag_skips_every_mcp_capability`.
* **AC3 — closure shape (parametrised over E1 / E2.1 / E2.2 / E2.3)**:
  `test_run_one_short_circuits_mcp_spec_with_no_mcp_flag`,
  plus the two negative branches
  (`test_run_one_does_not_short_circuit_non_mcp_spec_under_no_mcp`,
  `test_run_one_runs_mcp_spec_when_no_mcp_flag_absent`).
* **AC4 — RunCounts invariant**:
  `test_run_summary_counts_kept_plus_skipped_equals_n_prime_under_no_mcp`,
  plus the reverse-pin
  `test_run_summary_rejects_inconsistent_kept_plus_skipped_flag`.
* **End-to-end (gated)**:
  `test_eval_run_no_mcp_skips_mcp_evals_end_to_end` — gated on T04.10
  forward-deps AND the closure honouring `--no-mcp`. Auto-clears once
  the wiring lands.

## 6. Forward-dep gating rationale

The runtime `run_one` closure currently short-circuits only
`--no-pty` (`commands.py`:1537-1548); the matching `--no-mcp` branch
is the M3 follow-up that this task verifies. Two layered gates
preserve TEST-014 utility while the wiring is in flight:

1. `hasattr(_commands_mod, ...)` for T04.10 helpers
   (`_run_one_spec`, `_new_run_id`, `_compute_run_stats`,
   `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`).
2. Source-level probe `_no_mcp_runtime_wired()` looks for
   `"capability_gate:"` plus a `no_mcp` branch in `eval_run`'s source.

Each gate emits a `pytest.skip(...)` with a remediation pointer rather
than `xfail` so the test board stays clean and the skip auto-clears.

## 7. R9 mitigation traceability

TEST-014 closes the R9 risk: a reviewer landing this task PR on a host
without MCP can still run the full real-suite harness end-to-end. The
four MCP-tagged rows surface as SKIPPED with a populated `skip_reason`
so the audit chain remains intact — no MCP capability ⇒ no E1 / E2.1-3
PASS row, but the orchestrator and the Reporter still produce a
schema-valid summary with the correct count invariant.

## 8. Evidence

* Test log: `evidence/T05.26/pytest.log` (full `uv run pytest -v` output).
* Manifest extract: `evidence/T05.26/real-yaml-extract.md` records the
  exact lines that establish the optional_capabilities ↔ requires
  coupling.
* Test module: `tests/cli/eval/test_no_mcp_skip.py`.
