# Eval Retry Policy (NFR-REL2 + R3-mit)

**Status:** Stable as of T03.08 (Phase 3, D-0051) for the NFR-REL2
default. The R3-mit retry-once branch landed in T05.23 (Phase 5,
D-0101) and is opt-in per manifest entry via the `MCP-flaky` tag.

## TL;DR

`superclaude eval run` produces a **deterministic single-pass run** by
default. Failed evals are never retried automatically. To re-run a
failure after diagnosis, use the `--eval <id>` subset path documented
below.

The R3-mit policy (T05.23) adds a single, opt-in exception: an eval
whose manifest entry lists `MCP-flaky` in its `requires:` array is
retried **exactly once** when the first attempt produces a non-PASS
outcome that maps to a flaky failure mode (FAIL, ERRORED, TIMEOUT).
The final outcome — whether the retry recovered to PASS or the failure
persisted — carries the `mcp_server_flaky` artifact in
`outcome.artifacts` so post-mortem tooling can identify retries
without re-parsing the per-eval JSONL log.

```text
EvalRunner.DEFAULT_RETRY_COUNT = 0          # NFR-REL2 default
EvalRunner.MCP_FLAKY_TAG       = "MCP-flaky" # R3-mit tag (T05.23)
RetryOncePolicy.MAX_ATTEMPTS   = 2          # original + 1 retry
```

## Why no default retry?

The harness ships a **bounded retry policy** so the run output is
reproducible and the FR-RPT1 N'-vs-K invariant (one `evals[]` row per
expanded eval id) is never violated by hidden re-executions. The
[design-spec §13][design-spec-13] enumerates the constraints:

[design-spec-13]: ../../.dev/releases/current/cliEval/design-spec.md

> *Failed evals are NOT retried by default. The harness produces a
> deterministic single-pass run. The user can re-run with `--eval
> <failed-ids>` after diagnosing.*

Concretely:

* `EvalRunner.__init__` accepts a `retry_count` keyword argument with a
  default of `0` (the class constant `DEFAULT_RETRY_COUNT`). Any
  non-zero value raises `ValueError` at construction time so an
  accidental caller cannot silently re-execute a failed eval and break
  the orchestrator's per-spec accounting.
* `run_eval` (the FR-LC1 lifecycle skeleton) has no retry loop. A
  failing `ExpectResult` produces a `FAIL` outcome; a harness exception
  produces `ERRORED`. Neither path re-enters the lifecycle.
* The orchestrator (`RunOrchestrator`, T03.15) collects one
  `EvalOutcome` per submitted future via
  `concurrent.futures.as_completed` and writes it through to the
  Reporter. There is no orchestrator-layer retry either.

## Re-running a failed eval — the `--eval` subset path

After a run completes, the Reporter writes `summary.{md,json}` to the
run directory. Inspect the table to identify failed eval ids, then
re-run only those evals:

```bash
# Full suite run (deterministic single pass)
superclaude eval run suites/full.yaml --parallel 8

# Re-run only the failing ids after diagnosis (any number of --eval)
superclaude eval run suites/full.yaml --eval E03 --eval E07

# Quick smoke (3-4 evals); same flag, different subset
superclaude eval run suites/quick.yaml --eval E01 --eval E02
```

Notes:

* `--eval` accepts the **expanded** id (post-parameterize) so a
  parameterized eval like `E07[case=a]` is targetable by its full
  identifier. An id that does not match any expanded eval exits with
  code 2 (see `tests/cli/eval/test_eval_id_regex.py` and
  `src/superclaude/cli/eval/commands.py` — FR-CLI3).
* Subset runs are independent processes — they allocate a fresh
  `HomeIsolation` per eval and emit a fresh `summary.{md,json}` under
  their own run directory. There is no shared state with the originating
  run.
* `--keep-home` controls whether failed HOMEs survive the second run
  the same way it does for the first. Default behaviour preserves
  failed HOMEs and discards successful ones; the `--keep-home` flag
  forces preservation for both.

## R3-mit retry-once (T05.23 / D-0101)

R3-mit reserves exactly one in-process retry for evals whose failure
mode matches **MCP server flakiness**. The policy is opt-in per
manifest entry and orthogonal to `retry_count`:

1. The manifest tags the eval by including `MCP-flaky` in its
   `requires:` array (the same field that already carries capability
   names — no schema migration required).
2. On the first observed failure whose status is `FAIL`, `ERRORED`,
   or `TIMEOUT`, the runner re-executes the lifecycle exactly once.
3. Both the recovered-PASS and persistent-failure paths attach the
   `mcp_server_flaky` artifact to `outcome.artifacts`. The artifact
   key's value is the literal string `"true"` — the Reporter renders
   the presence of the key, not its content.

### Taxonomy

The retry is gated on a fixed status set:

| Status | Eligible for retry? | Rationale |
|---|---|---|
| FAIL | Yes | Could be expect-side MCP timeout |
| ERRORED | Yes | Harness exception (often MCP transport) |
| TIMEOUT | Yes | Most common MCP-flake signature |
| PASS | No | Nothing to retry |
| SKIPPED | No | Capability gate — did not run |
| INTERRUPTED | No | SIGINT — operator intent |
| XFAIL / XPASS | No | Expected-failure contract |

### Manifest example

```yaml
evals:
  - id: E07
    title: "Tavily MCP search returns at least one result"
    requires:
      - mcp.tavily       # capability gate
      - MCP-flaky        # opt-in to R3-mit retry-once
    expects: [...]
```

### Orthogonality with NFR-REL2

The R3-mit policy is wired through an additive `retry_policy` kwarg on
`EvalRunner`. It does **not** relax the existing `retry_count != 0`
construction guard — accidental sweeps that hand the runner a non-zero
retry count still raise `ValueError`. The two mechanisms answer
different questions:

* `retry_count` (NFR-REL2): "the operator-facing retry budget" —
  pinned to 0 because FR-RPT1 requires one `evals[]` row per expanded
  eval id.
* `retry_policy` (R3-mit): "the per-eval flaky-server escape hatch" —
  pinned to a single attempt and only fires on the `MCP-flaky` tag.

### OQ-10 decision

OQ-10 closed in favor of keeping R3-mit at P1: the policy lands
behind an opt-in tag rather than being promoted to a default-on
behaviour. The taxonomy (`FAIL` / `ERRORED` / `TIMEOUT`) was resolved
empirically against the M5 test surface; see
`.dev/releases/current/cliEval/decisions.md §B` and
`.dev/releases/current/cliEval/artifacts/D-0101/notes.md`.

## Operator-facing invariants

* `EvalRunner.DEFAULT_RETRY_COUNT` is the canonical pin for the
  NFR-REL2 contract. Reading it from a script (e.g. CI safety check)
  lets a deployment confirm the harness build has the bounded retry
  policy in place.
* `EvalRunner.MCP_FLAKY_TAG` is the canonical pin for the R3-mit tag
  string. Manifest tooling SHOULD reference it instead of hard-coding
  `"MCP-flaky"`.
* `RetryOncePolicy.MAX_ATTEMPTS` is the canonical pin for the R3-mit
  attempt budget (original + 1 retry = 2). The policy is stateless;
  the runner tracks attempt count externally.
* Any change to these constants requires an updated design-spec entry
  and an explicit M5 closure record per the OQ-10 decision row.

## See also

* `src/superclaude/cli/eval/runner.py` — `EvalRunner` class body,
  `DEFAULT_RETRY_COUNT`, `MCP_FLAKY_TAG`, and the R3-mit retry branch
  in `run()` / `_execute_once()`.
* `src/superclaude/cli/eval/retry.py` — `RetryOncePolicy` and module
  helpers `is_mcp_flaky_tagged`, `is_flaky_outcome`.
* `tests/cli/eval/test_retry_policy.py` — regression suite locking the
  NFR-REL2 contract in place.
* `tests/cli/eval/test_mcp_retry_once.py` — regression suite locking
  the R3-mit retry-once policy in place (26 tests covering policy
  decisions, integration with `EvalRunner`, and orthogonality with
  `retry_count`).
* `.dev/releases/current/cliEval/design-spec.md §13` — Bounded retry
  contract.
* `.dev/releases/current/cliEval/decisions.md §B` — OQ-10 closure
  record.
* `.dev/releases/current/cliEval/artifacts/D-0051/spec.md` — Per-task
  deliverable record for T03.08 (NFR-REL2).
* `.dev/releases/current/cliEval/artifacts/D-0101/spec.md` — Per-task
  deliverable record for T05.23 (R3-mit).
