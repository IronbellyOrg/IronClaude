# D-0051 — NFR-REL2 Bounded Retry Policy

| Field | Value |
|---|---|
| Task | T03.08 |
| Component(s) | `runner.py` (EvalRunner), `docs/eval/retry.md`, `tests/cli/eval/test_retry_policy.py` |
| Roadmap | R-051 (NFR-REL2) |
| Spec refs | design-spec §12 (Bounded retry), §14 (R3 mitigation), decisions.md §B (OQ-10 deferral) |
| Depends on | D-0049 (EvalRunner class, T03.05) |
| Consumed by | R3-mit (T05.23) for MCP-flaky retry-once; FR-RPT1 N'-vs-K invariant (T03.11); FR-CLI3 `--eval` subset path |

## 1. Goal

Pin the **bounded retry policy** the design-spec §13 declares:

> *Failed evals are NOT retried by default. The harness produces a
> deterministic single-pass run. The user can re-run with `--eval
> <failed-ids>` after diagnosing.*

Three deliverables in scope:

1. `EvalRunner.DEFAULT_RETRY_COUNT = 0` class constant and a
   `retry_count: int = 0` constructor kwarg that rejects any non-zero
   value at construction time.
2. `EvalRunner.MCP_FLAKY_TAG = "MCP-flaky"` class constant reserving
   the exact tag string the future R3-mit retry-once branch (T05.23)
   will look for, so manifest tooling can reference the canonical pin
   instead of a literal string.
3. `docs/eval/retry.md` documenting the `--eval <id>` subset re-run
   path, the constants above, and the OQ-10 deferral.

The runner ships **no retry code**. The contract is *absence-of-retry*;
the test suite at `tests/cli/eval/test_retry_policy.py` guards that
absence so a future change cannot silently re-execute failing evals.

## 2. Public Surface

```python
from superclaude.cli.eval.runner import EvalRunner

EvalRunner.DEFAULT_RETRY_COUNT  # ClassVar[int]; canonical pin == 0
EvalRunner.MCP_FLAKY_TAG        # ClassVar[str]; canonical pin == "MCP-flaky"

EvalRunner(
    ...,
    retry_count=EvalRunner.DEFAULT_RETRY_COUNT,  # only accepted value
)
```

### 2.1 Constructor parameter contract

| Param | Default | Contract |
|---|---|---|
| `retry_count` | `EvalRunner.DEFAULT_RETRY_COUNT` (== 0) | Must equal `DEFAULT_RETRY_COUNT`. Any other int (positive or negative) raises `ValueError("EvalRunner retry_count must be 0 ...")`. The error message references NFR-REL2, the `--eval <id>` workaround, and `docs/eval/retry.md`. |

The error path is deliberately loud rather than silently clamping: a
non-zero retry would violate the FR-RPT1 N'-vs-K invariant (the
orchestrator expects exactly one `EvalOutcome` per submitted
`EvalSpec`) and re-introduce non-determinism into the run summary.

### 2.2 Class constants

| Constant | Type | Value | Purpose |
|---|---|---|---|
| `DEFAULT_RETRY_COUNT` | `ClassVar[int]` | `0` | Authoritative pin for the bounded-retry contract. CI safety checks can read this constant to confirm the deployed harness has retries disabled. |
| `MCP_FLAKY_TAG` | `ClassVar[str]` | `"MCP-flaky"` | Reserved tag string for the future R3-mit (T05.23) retry-once branch. Manifest tooling and the future R3-mit code reference this constant instead of a literal so the rename surface is one place. |

## 3. Behavioural Contract

### 3.1 Single-pass invariant

For every `EvalSpec` passed to `EvalRunner.run`, the executor's
`spawn` / `inject` / `observe` trio is called **at most once** (zero
times if the lifecycle errored before spawn). This holds across all
outcome statuses (`PASS`, `FAIL`, `ERRORED`, `TIMEOUT`, `INTERRUPTED`).

### 3.2 Construction-time validation

| Input | Behaviour |
|---|---|
| `retry_count` absent | Default of `0` applied; runner constructs normally. |
| `retry_count == 0` | Accepted; identical to default. |
| `retry_count != 0` (positive or negative) | `ValueError` raised before any other side effect. The error message contains the literals `retry_count`, `NFR-REL2`, and `--eval`. |

### 3.3 Future-extension hook

R3-mit (T05.23) will introduce a code path that:

1. Inspects the eval's tags for `EvalRunner.MCP_FLAKY_TAG`.
2. Classifies the failure mode (OQ-10 closes the exact taxonomy).
3. Re-runs the lifecycle exactly once if both 1 and 2 match.

Today, the constant exists but no consumer references it inside the
runner itself.

## 4. Acceptance Criteria → Test Mapping

| AC bullet | Test | Pin |
|---|---|---|
| Default `retry_count=0` enforced | `test_default_retry_count_is_zero` | `EvalRunner.DEFAULT_RETRY_COUNT == 0` |
| Monkeypatched runner confirms no retries on failure | `test_monkeypatched_runner_confirms_no_retry_loop` | Outer `run()` call count == 1; executor trio count == 1 each |
| Failing eval not re-executed | `test_fail_outcome_does_not_retry` | Counting executor records `spawn=inject=observe=1`; outcome is `FAIL` |
| Errored eval not re-executed | `test_errored_outcome_does_not_retry` | Counting executor records `spawn=1, inject=1, observe=0`; outcome is `ERRORED` |
| Non-zero retry_count rejected | `test_non_zero_retry_count_rejected`, `test_other_non_zero_retry_count_rejected[-1,2,10]` | `ValueError` with `retry_count`, `NFR-REL2`, `--eval` in message |
| Explicit zero retry_count accepted | `test_explicit_zero_retry_count_accepted` | Runner constructs and emits `PASS` outcome |
| `MCP_FLAKY_TAG` constant defined | `test_mcp_flaky_tag_constant_defined` | `EvalRunner.MCP_FLAKY_TAG == "MCP-flaky"` |
| `--eval <id>` subset re-run path documented | `test_retry_docs_present_and_describe_subset_path` | `docs/eval/retry.md` exists and contains tokens `NFR-REL2`, `--eval`, `MCP-flaky`, `retry_count` |

## 5. Out of Scope (deferred)

| Item | Reason | Lands in |
|---|---|---|
| MCP-flaky retry-once code path | OQ-10 taxonomy not yet empirically closed. | R3-mit (T05.23), M3/M5 |
| Tag-aware EvalSpec parsing for `MCP_FLAKY_TAG` | EvalSpec has no `tags` field today; the manifest schema would gain one alongside R3-mit. | R3-mit (T05.23) |
| CLI surface change for `--retry-count` | Not authored by NFR-REL2; the harness keeps a single CLI surface (`--eval <id>`). | N/A |

## 6. Provenance

* Phase file row: `phase-3-tasklist.md` T03.08, R-051.
* Design-spec source: `design-spec.md §13 — Bounded retry (no infinite retry)`.
* Decisions source: `decisions.md §B — OQ-10 resolution status`.
* Implementation diff anchor: `src/superclaude/cli/eval/runner.py` `EvalRunner` class body (constants) + `__init__` (retry_count validation).
* Test anchor: `tests/cli/eval/test_retry_policy.py`.
* Documentation anchor: `docs/eval/retry.md`.
