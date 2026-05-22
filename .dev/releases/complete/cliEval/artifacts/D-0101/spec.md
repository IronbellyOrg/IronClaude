# D-0101 — R3-mit MCP Retry-Once Policy

| Field | Value |
|---|---|
| Task | T05.23 |
| Component(s) | `src/superclaude/cli/eval/retry.py` (new), `src/superclaude/cli/eval/runner.py` (EvalRunner), `docs/eval/retry.md`, `tests/cli/eval/test_mcp_retry_once.py` |
| Roadmap | R-100 (R3-mit) |
| Spec refs | design-spec §13 (Bounded retry), §14 (R3 mitigation), decisions.md §B (OQ-10 closure) |
| Depends on | D-0049 (EvalRunner class, T03.05), D-0051 (NFR-REL2 bounded retry, T03.08) |
| Consumed by | Reporter (COMP-008 / T03.13) — surfaces `mcp_server_flaky` artifact in summary tables |

## 1. Goal

Land the **opt-in retry-once branch** the design-spec §14 reserves
for MCP-flaky evals. Concretely:

> *On the first non-PASS outcome whose status matches the flaky
> taxonomy (FAIL, ERRORED, TIMEOUT) AND whose spec carries the
> `MCP-flaky` capability tag, the runner re-executes the per-eval
> lifecycle exactly once. The final outcome — whether the retry
> recovered or the failure persisted — carries the
> `mcp_server_flaky` artifact in `outcome.artifacts`.*

Four deliverables in scope:

1. New module `src/superclaude/cli/eval/retry.py` exporting
   `RetryOncePolicy`, `MCP_FLAKY_TAG`, `MCP_SERVER_FLAKY_ARTIFACT`,
   `is_mcp_flaky_tagged`, `is_flaky_outcome`.
2. `EvalRunner` integration: additive `retry_policy` and
   `home_factory` kwargs; `run()` consults the policy after each
   first attempt and re-invokes the lifecycle via `_execute_once()`
   when the policy elects retry.
3. `docs/eval/retry.md` update reflecting the R3-mit contract: the
   taxonomy table, manifest example, orthogonality with `retry_count`,
   and OQ-10 closure note.
4. `tests/cli/eval/test_mcp_retry_once.py` regression suite (26
   tests) covering policy unit behaviour, EvalRunner integration, and
   compatibility with the NFR-REL2 `retry_count` rejection.

The policy is **stateless and immutable** (frozen dataclass) — the
runner tracks attempt count externally so a stateful policy bug
cannot loop.

## 2. Public Surface

```python
from superclaude.cli.eval.retry import (
    MCP_FLAKY_TAG,                # "MCP-flaky" (mirrors EvalRunner.MCP_FLAKY_TAG)
    MCP_SERVER_FLAKY_ARTIFACT,    # "mcp_server_flaky"
    RetryOncePolicy,              # frozen dataclass; MAX_ATTEMPTS == 2
    is_mcp_flaky_tagged,          # (EvalSpec) -> bool
    is_flaky_outcome,             # (EvalOutcome) -> bool
)
from superclaude.cli.eval.runner import EvalRunner

EvalRunner(
    ...,
    retry_policy=RetryOncePolicy(),    # opt-in; default None disables R3-mit
    home_factory=lambda: HomeIsolation(...),  # required in prod (setup is not re-entrant)
)
```

### 2.1 RetryOncePolicy contract

| Method | Returns | Contract |
|---|---|---|
| `is_eligible(spec)` | `bool` | `True` iff `MCP_FLAKY_TAG in spec.requires`. |
| `should_retry(spec, outcome)` | `bool` | `True` iff `is_eligible(spec)` AND `is_flaky_outcome(outcome)`. The runner consults this only on the *first* attempt's outcome. |
| `annotate(outcome)` | `EvalOutcome` | Returns a new outcome with `mcp_server_flaky="true"` added to `outcome.artifacts`. Idempotent: re-application returns the input unchanged when the artifact is already present. |

### 2.2 Flaky taxonomy

| Status | Eligible | Rationale |
|---|---|---|
| `FAIL` | Yes | MCP timeout expressed through expect callable |
| `ERRORED` | Yes | Harness exception (often MCP transport) |
| `TIMEOUT` | Yes | Most common MCP-flake signature |
| `PASS` | No | Nothing to retry |
| `SKIPPED` | No | Capability gate — did not run |
| `INTERRUPTED` | No | SIGINT — operator intent |
| `XFAIL` / `XPASS` | No | Expected-failure contract |

### 2.3 EvalRunner integration

`EvalRunner.run(spec)` now wraps `_execute_once(spec)` in a single
policy-gated retry branch:

```python
outcome = self._execute_once(spec)
if self._retry_policy is not None and self._retry_policy.should_retry(spec, outcome):
    if self._home_factory is not None:
        self._home = self._home_factory()
    retry_outcome = self._execute_once(spec)
    outcome = self._retry_policy.annotate(retry_outcome)
return outcome
```

`home_factory` is consulted only when wired. Production callers MUST
wire one because `HomeIsolation.setup()` raises `RuntimeError` on a
second call without an intervening teardown — the factory produces a
fresh `HomeIsolation` so the second lifecycle sees the same contract.
Test stubs whose `setup()` is callable across teardown may omit the
factory.

## 3. Behavioural Contract

### 3.1 Retry-once invariant

For every `EvalSpec` passed to `EvalRunner.run`:

* If `retry_policy is None`: the executor trio fires **exactly once**
  (NFR-REL2 default).
* If `retry_policy` is wired AND `should_retry()` returns `False`:
  the executor trio fires **exactly once**.
* If `retry_policy` is wired AND `should_retry()` returns `True`:
  the executor trio fires **exactly twice** — the original attempt
  plus one retry. The policy never re-consults `should_retry()` on
  the retry attempt's outcome.

### 3.2 Artifact attachment

The `mcp_server_flaky` artifact is attached **after** the retry
attempt completes, regardless of whether the retry's status is `PASS`,
`FAIL`, `ERRORED`, or `TIMEOUT`. The artifact records *the fact
that a retry occurred*, not the result of the retry.

| Scenario | First attempt | Retry attempt | Final status | Artifact present? |
|---|---|---|---|---|
| Non-tagged eval, fails | FAIL | — | FAIL | No |
| Tagged eval, passes | PASS | — | PASS | No |
| Tagged eval, fails then passes | FAIL | PASS | PASS | Yes |
| Tagged eval, fails persistently | FAIL | FAIL | FAIL | Yes |
| Tagged eval, errors then errors | ERRORED | ERRORED | ERRORED | Yes |
| Tagged eval, times out then succeeds | TIMEOUT | PASS | PASS | Yes |

### 3.3 Orthogonality with NFR-REL2

| Construction | Behaviour |
|---|---|
| `retry_count=0`, `retry_policy=None` | NFR-REL2 default — no retry under any condition. |
| `retry_count=0`, `retry_policy=RetryOncePolicy()` | R3-mit policy active for tagged evals only. |
| `retry_count=1`, `retry_policy=None` | `ValueError` at construction time (NFR-REL2 guard). |
| `retry_count=1`, `retry_policy=RetryOncePolicy()` | `ValueError` at construction time (NFR-REL2 guard not relaxed by policy presence). |

## 4. Acceptance Criteria → Test Mapping

| AC bullet | Test | Pin |
|---|---|---|
| Constants exist with canonical values | `test_constants_are_canonical` | `MCP_FLAKY_TAG == "MCP-flaky"`, `MCP_SERVER_FLAKY_ARTIFACT == "mcp_server_flaky"`, `EvalRunner.MCP_FLAKY_TAG == MCP_FLAKY_TAG` |
| Tagged spec is eligible | `test_policy_is_eligible_for_tagged_spec`, `test_policy_is_eligible_for_tagged_spec_alongside_other_caps` | `RetryOncePolicy().is_eligible(spec) is True` |
| Untagged spec is not eligible | `test_policy_not_eligible_for_untagged_spec`, `test_policy_not_eligible_when_only_other_caps_present` | `RetryOncePolicy().is_eligible(spec) is False` |
| Flaky statuses trigger retry on tagged spec | `test_should_retry_on_flaky_status_for_tagged_spec[FAIL/ERRORED/TIMEOUT]` | `should_retry()` returns `True` |
| Non-flaky statuses never trigger retry | `test_should_not_retry_on_non_flaky_status[PASS/SKIPPED/INTERRUPTED/XFAIL/XPASS]` | `should_retry()` returns `False` |
| Untagged spec never retries even on FAIL | `test_should_not_retry_untagged_even_on_fail` | `should_retry()` returns `False` |
| Annotate adds artifact | `test_annotate_adds_mcp_server_flaky_artifact` | `outcome.artifacts["mcp_server_flaky"] == "true"` |
| Annotate preserves existing artifacts | `test_annotate_preserves_existing_artifacts` | Pre-existing keys survive |
| Annotate is idempotent | `test_annotate_is_idempotent` | Re-application returns input unchanged |
| Module helpers agree with policy | `test_module_level_helpers_agree_with_policy` | `is_mcp_flaky_tagged` / `is_flaky_outcome` agree with policy decisions |
| Runner does not retry without policy | `test_no_policy_means_no_retry_even_on_flaky_failure` | `spawn_count == 1`, no artifact |
| Runner does not retry untagged eval | `test_runner_does_not_retry_untagged_eval` | `spawn_count == 1`, no artifact |
| Runner retries tagged + flaky | `test_runner_retries_once_on_mcp_flaky_failure` | `spawn_count == 2`, artifact present, final FAIL |
| Recovery yields PASS with artifact | `test_retry_recovery_returns_pass_with_artifact` | `spawn_count == 2`, artifact present, final PASS |
| First-attempt PASS skips retry | `test_retry_skips_when_first_attempt_passes` | `spawn_count == 1`, no artifact |
| Policy does not relax retry_count guard | `test_policy_does_not_unlock_nonzero_retry_count` | `retry_count=1` + policy still raises `ValueError` |
| Runner accepts policy without home_factory | `test_runner_accepts_policy_without_home_factory` | Retry path works against re-entrant test home |

## 5. Out of Scope

| Item | Reason | Lands in |
|---|---|---|
| Persisting first-attempt outcome to a per-eval JSONL retry namespace | Per-eval JSONL captures lifecycle events but not retry attempt boundaries; Reporter consumes the artifact key only. | Deferred — open an item if forensic need surfaces post-M5. |
| Promoting R3-mit to default-on | OQ-10 closed in favor of opt-in tag-based behaviour so the manifest author retains control. | N/A — explicit decision. |
| Adding a manifest schema `tags:` array | `EvalSpec.requires` already accepts arbitrary strings; tag lives there to avoid schema migration. | N/A — explicit decision. |
| Per-attempt timeout multiplier | Phase 5 keeps the single `timeout_sec`; multipliers add ambiguity to the FR-RPT1 N'-vs-K invariant. | Deferred — out of scope for R3-mit. |

## 6. OQ-10 Closure

OQ-10 asked: *"Does R3-mit remain at P1 (opt-in tag) or get promoted
to P0 (default-on)?"* The empirical evidence collected through
T05.02..T05.21 shows MCP flake rates concentrated on a small subset
of evals (Tavily, Context7 transport timeouts). Promoting to P0 would
mask non-flake bugs across the whole suite. **Decision:** keep R3-mit
at P1, opt-in via `MCP-flaky` tag. Recorded in
`.dev/releases/current/cliEval/decisions.md §B`.

## 7. Provenance

* Phase file row: `phase-5-tasklist.md` T05.23, R-100.
* Design-spec source: `design-spec.md §14 — R3 mitigation`.
* Decisions source: `decisions.md §B — OQ-10 closure record`.
* Implementation diff anchor: `src/superclaude/cli/eval/retry.py`
  (new module), `src/superclaude/cli/eval/runner.py` `EvalRunner`
  class body (`run()` + `_execute_once()` split, additive kwargs).
* Test anchor: `tests/cli/eval/test_mcp_retry_once.py` (26 tests).
* Documentation anchor: `docs/eval/retry.md`.
