# Diagnosability Tasklist

**Issue**: issue 540, foreground marker omission
**Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/cli/swarm/commands.py::run_cmd  **Round**: 0 of 3  **re-run permitted**: yes  **discriminator-required**: no  **capability-verdict**: n/a
**branch**: swill-ib/bug-swarm-refactor-find-recommends-unavailable-s  **repro-venue-id**: local foreground stub completion, file-presence check

## Emitter search

emitters-found: 1 (completion stdout summary at commands.py:2173, not a marker-existence emitter)
already-read-files: 3 (foreground contract, state and JSONL artifacts inspected directly; this count is restricted to captured output artifacts, not all source reads)
usable-capture-routes: 1 (permitted invocation-site filesystem inspection after process exit)
The missing-publication boolean is available through Path.exists on the exact output-root marker after the real CLI exits. That route already captured done_exists=false for both foreground and resume in tier1-observation.md. It is not a generated expected value. The normal stdout summary and dispatch log lack marker-existence data; the marker file cannot provide its own absent contents. A wrapper can inspect the path without production changes. No capability or permission block exists. Historical remote artifacts remain read-only historical evidence.

## Discriminator rows

core-rows=0, pack-rows=0, total-rows=0. No new measurement is required: direct post-exit filesystem capture already supplies the disputed datum. There is no pair of competing mechanisms, no inferred passing control and no invented outcome table. This partial audit describes absent built-in marker diagnostics, not unresolved marker-existence evidence.

## Fix candidate

Proposal only: wire the existing atomic marker writer into real completion continuations, after contract and terminal state, honoring effective completion policy and final contract status. Pair verification with actual CLI artifact assertions, including disabled policy and relevant terminal outcomes. No production patch was applied during diagnosis.

## Hard Constraints

Any later diagnostic instrumentation must be additive, invocation-site-only, reversible and annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.` No source instrumentation, log-level workaround, paid call, secret output or implicit implementation permission is proposed.

## Implementation tasks

None required for diagnosis. Existing direct observations and source tracing suffice to investigate this deterministic omission; do not add generic logging tasks. Repair-stage regression authoring is separate and needs its checked plan.

## Verification

Completed observational checks: real stub foreground CLI exit0, contract success, terminal state, done_exists=false; real stub resume exit0 with skipped=3, redispatched=0 and the same absent-marker state. Existing writer/CLI suites: 25 passed. See tier1-observation.md and artifacts/baseline-tests.txt. Detached tmux execution, failure/partial CLI outcomes and disabled-policy behavior were not runtime-tested and must not be called verified.

## Rollback

No instrumentation applied and no product changes to reverse. Retain all evidence; never delete it as cleanup. Future repair reversal must be defined by its plan, not this tasklist.

## Patch-round counter

No counted discriminator tasklist was emitted, so this run does not increment or modify the shared counter. The existing .dev/troubleshoot/diagnosability-rounds.json changed externally during this run (observed git diff --name-only); this session did not write it and will not revert another session's update. Round0 denotes this invocation's uncounted state, not a claim about another run's authoritative key.
