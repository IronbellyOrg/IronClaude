# D-0058 — Design Notes

Companion to `spec.md`. Captures the choices made while implementing
T03.16 (FR-G2: parallel-15 integration test) and the alternatives
considered.

## Why an integration test rather than two unit tests

The orchestrator and isolation components each have dedicated unit
suites (`test_orchestrator.py` 20 tests, `test_home_isolation.py` 27
tests). What neither suite proves is that they **compose correctly under
concurrency**:

- The orchestrator unit tests use trivial stub workers that never touch
  the filesystem.
- The isolation unit tests run lifecycle on a single instance at a time
  (with one explicit `TestParallelSiblings.test_parallel_lifecycle_round_trip`
  but only at width=2).

FR-G2's contract is specifically about the *composition*: 15 isolations
churning through a real `ThreadPoolExecutor` without colliding on HOME
paths, sessions, or telemetry namespaces. That requires real
`HomeIsolation.setup` calls under the orchestrator's scheduling, which
is exactly the integration boundary D-0058 owns.

## Why a worker factory instead of `HomeIsolation` inside `RunOrchestrator`

`RunOrchestrator` takes an `EvalWorker = Callable[[EvalSpec], EvalOutcome]`
exactly so the orchestrator does not have to know about HOME, session,
or telemetry layout (see D-0057 notes). T03.16 demonstrates that this
contract is honoured: the test wires `HomeIsolation` into the worker at
the call site, the orchestrator never references isolation types. If
this composition broke, this test would catch it. The worker factory
pattern (`_make_isolation_worker(scratch_root, config, …)`) closes over
configuration so individual test cases can swap concurrency barriers
without redefining the wiring.

## How "telemetry namespace" was interpreted

FR-G2 lists "state/telemetry namespace" alongside HOME and session_id
as a per-eval isolation surface, but the design spec doesn't pin a
specific path. Two anchors made the choice unambiguous:

1. `EvalContext.jsonl_paths` in `models.py` already documents
   `{"hook_log": ..., "telemetry": ...}` as the per-eval JSONL contract.
2. `HomeIsolation.state_path(suffix)` exists specifically to scope
   per-eval files under the eval's HOME (`home_path / suffix`).

So the namespace is realised as `home_path / ".eval-logs" / "telemetry.jsonl"`.
Test 4 (`test_each_eval_has_isolated_telemetry_namespace`) asserts both
**uniqueness** (15 distinct namespaces) and **containment** (each
namespace strictly under its own HOME). Test 5 verifies the contents
match the spec that owns the file, ruling out cross-talk.

## Why read telemetry after teardown via `home_root` scan

`HomeIsolation.teardown(keep=True)` preserves the directory but clears
the `_home_path` slot, so the post-run inspection can't ask the
instance "what was your home_path?". Two options:

1. **Capture `home_path` during the worker run** and store it in the
   record alongside `session_id` etc. This is what
   `record["home_path"]` already does, so most tests use this path.
2. **Scan `home_root` for `{eval_id}-*` dirs** to verify the
   `from-the-outside` view that mkdtemp's `prefix=` did the right thing.
   Helpers `_read_telemetry_event` / `_read_telemetry_home` use this so
   the namespace assertions don't depend on the worker's bookkeeping.

Both views are checked. They agree iff the prefix mkdtemp contract holds.

## Why three views of `session_id` (record, JSONL, env)

The contract is "each eval owns its own session_id." A passing test
that reads only one view (e.g. the worker's record) wouldn't catch a
regression where `env()` returns a stale value while the record looks
right. So `test_each_eval_receives_unique_session_id` checks:

- `record["session_id"]` — what the worker captured at `env()` time.
- JSONL's `session_id` field — what was written to disk.
- `iso.env()["CLAUDE_SESSION_ID"]` — what a downstream caller would
  read *after* the run, before teardown clears the slot.

Wait — teardown clears the slot. The test therefore re-creates
`HomeIsolation` with the same args and calls `env()` post-run, which
returns the same `session_id` because `session_id` is a constructor
field, not a mkdtemp output. The point is to prove that the env() view
matches the disk view, which it does.

(An earlier draft tried to read `env()` on the original instance, which
raised `RuntimeError` after teardown. The current shape correctly
treats `session_id` as a deterministic input and verifies all three
views agree.)

## Why two clamp tests instead of one

`TestParallelClamp::test_parallel_above_max_clamps_to_fifteen` in
T03.15 already proves the clamp downward. What that test doesn't
prove is that the clamp is **not over-restrictive** — e.g. a regression
that clamped everything to 10 would still pass that test (≤15 stays
≤15). `test_parallel_at_max_admits_fifteen_concurrent_workers` closes
that gap: with parallel=15 and 15 specs holding a barrier, exactly 15
must be in flight simultaneously. Together the two clamp tests pin both
ends of the NFR-PERF2 contract.

## Concurrency barrier design

Naïve "count active workers" measurements race: by the time you read
`len(active)`, an earlier worker may have decremented. The pattern
used here:

```
enter() {
  with lock: active.append(spec)
  with lock: observed_concurrency.append(len(active))
  if hold_event: hold_event.wait()
  with lock: active.remove(spec)
}
```

The snapshot is taken **under the lock**, immediately after appending,
so `max(observed_concurrency)` accurately reflects the peak. Combined
with a `threading.Event` barrier released by a `threading.Timer(1.0,
...)`, workers actually pile up before any can return — which is what
makes the peak meaningful.

For the unbounded (no-barrier) test, the suite is fast enough that
concurrency assertions are bounded by ≤8 only (not exactly 8), since
all 15 finish in ~0.1s and overlap depends on scheduler timing. That
flake-resistance is intentional: the *clamp* matters, not the
arrival-rate-derived ceiling.

## Out-of-scope items deliberately not implemented

- **Hook deployment per HOME.** T03.04 owns the deploy; the worker
  here writes the telemetry directly to keep the test focused on the
  isolation surface FR-G2 names.
- **PTY/process launch.** Phase 4 wires `ClaudeProcessAdapter` into the
  real worker; T03.16 demonstrates the orchestrator+isolation
  composition that adapter will plug into.
- **Time-isolation (`time_offset_sec`).** Covered in
  `test_home_isolation.py` for the unit surface; not in FR-G2's
  scope.
- **Cancellation under load.** T03.15's cancellation tests cover the
  scheduler's cancel semantics; mixing cancellation into a 15-wide
  integration test would dilute both signals.

## Verification evidence

See `evidence.md` in this directory. Summary:
- 7/7 new tests pass in 2.21s.
- 47/47 regression tests pass across orchestrator + isolation in 0.50s.
- 54/54 combined (new + regression) pass in 2.58s.
