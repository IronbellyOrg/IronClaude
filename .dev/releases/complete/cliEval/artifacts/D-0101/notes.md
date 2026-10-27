# D-0101 — Implementation Notes

## Design choices

### Why a frozen dataclass instead of a function?

`RetryOncePolicy` is a frozen dataclass (`MAX_ATTEMPTS`,
`flaky_tag`, `artifact_name`) rather than a pair of free functions
because:

1. The policy carries configurable state — `flaky_tag` and
   `artifact_name` default to the canonical strings but a future
   harness fork could rewire them without monkeypatching constants.
2. The runner stores the policy on `self._retry_policy`; checking
   `policy is not None` is a more readable conditional than
   `should_retry_fn is not None`.
3. The class collects the policy's three decision points
   (`is_eligible`, `should_retry`, `annotate`) under one type so a
   reader sees the contract at a glance instead of reconstructing it
   from imports.

### Why is the policy stateless?

A stateful policy that tracked "attempt count" internally would have
to be reset between evals; forgetting to reset is exactly the kind of
bug the NFR-REL2 work was authored to prevent. The runner owns the
attempt count externally (one consultation per `run()` call), so the
policy is stateless by construction.

### Where does the `MCP-flaky` tag live?

In `EvalSpec.requires` — the existing field that accepts arbitrary
capability strings. Two reasons:

1. The schema already accepts arbitrary strings there (one item per
   capability gate) so no schema migration is required.
2. Manifest authors already think of `requires:` as "things this eval
   depends on" — flakiness is a property of the dependency set, not
   the eval body.

A future schema cleanup could promote it to a dedicated `tags:`
array; the policy's `is_eligible()` would only need to swap the
membership check.

### Why `home_factory` instead of re-initialising the existing home?

`HomeIsolation.setup()` raises `RuntimeError` on a second call
without intervening teardown — this is correct for the production
class because setup includes filesystem operations that would be
destructive to repeat. The runner therefore needs a way to obtain a
*fresh* `HomeIsolation` for the retry attempt. Two options were
considered:

1. **Construct a new `HomeIsolation` in the runner.** Requires the
   runner to know the home's construction parameters
   (`eval_id`, `home_root`, ...). This couples the runner to the
   isolation class's API.
2. **Accept a `home_factory: Callable[[], HomeIsolation]` kwarg.**
   The caller controls construction; the runner just invokes the
   factory. (Selected.)

Tests can either pass a factory or omit it (re-entrant test homes
exist). Production callers wire a real factory.

### Why no first-attempt event in the JSONL log?

The per-eval JSONL log is a stream of lifecycle events; the retry
adds a second pass that re-uses every event name. Marking the
attempts with a `retry_attempt: 0/1` field on each event would
require schema changes to every event and a parser update on the
Reporter side. The `mcp_server_flaky` artifact key already records
*that* a retry occurred; the JSONL log records *what happened* on
the second pass under the same event names as the first.

If a future operator need surfaces a per-attempt forensic
requirement, the additive change is small: add a `retry_attempt`
field to `_JsonlLog.emit()` and bump it after the policy elects
retry.

## Edge cases verified

* **`MCP_FLAKY_TAG` alongside other capabilities.** The test
  `test_policy_is_eligible_for_tagged_spec_alongside_other_caps`
  pins eligibility when the tag sits beside real capability strings
  like `mcp.tavily`. The tag is found by membership, not by being
  the sole entry.
* **Pre-existing artifacts survive annotation.** The test
  `test_annotate_preserves_existing_artifacts` pins that
  `mcp_server_flaky` is added to (not over) the existing artifact
  map.
* **Idempotency under re-annotation.** The test
  `test_annotate_is_idempotent` pins that re-applying
  `annotate(annotated)` returns the input unchanged.
* **Recovery on retry still attaches the artifact.** The test
  `test_retry_recovery_returns_pass_with_artifact` pins that a
  PASS-after-FAIL run carries the artifact so the Reporter can
  surface the flake-and-recover signal.

## Trade-offs

| Trade-off | Choice | Rationale |
|---|---|---|
| Retry vs. abort on policy programming error | Retry (current) | The policy is intentionally simple; the orchestrator already isolates eval failures. |
| Annotate after recovery vs. only on persistent failure | Annotate both (current) | Reporter consumes a single signal; downstream tooling can compare against `status` to distinguish recovery from persistence. |
| Wire policy on `EvalRunner` vs. on `RunOrchestrator` | `EvalRunner` (current) | The retry decision is per-eval, not per-suite; the runner already owns the per-eval lifecycle. |
| Stateful vs. stateless policy | Stateless (current) | Avoids the "forgot to reset between evals" bug class entirely. |
