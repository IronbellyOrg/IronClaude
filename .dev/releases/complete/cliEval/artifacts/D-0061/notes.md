# D-0061 — Design Notes

Companion to `spec.md`. Captures the choices made while implementing
T03.20 (NFR-ISO1: no shared mutable state across `N×15` trials) and
the alternatives considered.

## Why N=3

The task line reads "Author integration test running 3 trials of 15-eval
parallel runs," which pins the lower bound. Higher N (e.g. 5, 10) would
catch slightly lower-probability races but would also push wall-clock
above what a per-PR CI run wants to amortize. With N=3 and 15 evals at
parallel=8, the test consistently completes in ~0.4s on the dev host —
small enough to live in the default suite without gating.

If a future regression manifests intermittently at N=3, the constant at
the top of the test file is the only knob to bump. Splitting N across
multiple tests was considered and rejected because the cross-trial
assertions need access to the full 45-record set; partitioning loses
the ability to detect collisions that cross test boundaries.

## Why a single shared `scratch_root` across all trials

The fixture deliberately mounts every trial against the same
`scratch_root`. A per-trial scratch root would hide exactly the bugs
this test is designed to catch:

- A `HomeIsolation` regression that caches `mkdtemp` outputs by
  `eval_id` and re-uses them across runs would not surface — each
  trial's cache miss would happen against a fresh directory.
- A telemetry writer that opens a file handle once per process would
  silently fan into the first trial's file; per-trial roots would
  conceal the cross-talk by giving each trial its own root.

Sharing the root is therefore the entire point.

## Why session_id includes the trial number

The worker allocates `session_id = f"sess-t{trial}-{spec.id}"`. Two
considerations drove this:

1. **Canonical uniqueness by construction.** If session_id were
   independent of trial, a regression where two trials happened to
   collide on UUID values would surface as an *AC* failure, but the
   reader would have to dig to discover whether the canonical worker
   record itself was duplicating values. Stamping the trial in lets
   the canonical record carry uniqueness *trivially*, leaving the
   env / JSONL view assertions to detect drift.
2. **Bug surfacing.** A future regression where `env()` returns a
   stale session_id from the previous trial would still pass
   "canonical record uniqueness" but fail T4's env-view check. The
   trial-stamped scheme separates the two signals.

The cross-trial assertion proper does not depend on this choice — even
a non-trial-stamped session_id allocator that produced distinct values
would satisfy NFR-ISO1. The trial stamp is purely an instrumentation
choice for diagnosis.

## Why reuse the spec ids (E000..E014) across trials

Each trial uses the same `_build_specs(15)` output. Re-using `eval_id`
values across trials is deliberate: if `HomeIsolation` keyed any
internal cache off `eval_id` (e.g. a `_home_cache: dict[str, Path]`),
trial 2's `E007` would receive trial 1's `E007` HOME, and T2's
"home_paths pairwise distinct" assertion would catch it immediately.

A unique-per-trial id scheme would mask that regression.

## Why test 6 (telemetry contents belong to owning eval) is not redundant with test 5

Test 5 asserts JSONL **paths** are pairwise distinct. Test 6 reads
each file and asserts its **contents** belong to the eval that owns
the path. The two checks rule out different bugs:

- Test 5 catches a regression where two workers compute the same JSONL
  path (e.g. via a shared mutable default argument).
- Test 6 catches a regression where two workers compute *distinct*
  paths but share a file handle — so the file at path A ends up
  containing the record meant for path B's eval.

Both bugs are plausible regressions of "shared mutable state"; both
need to be ruled out for NFR-ISO1 to be honoured.

## Why no port-binding mocks

NFR-ISO1 calls out "no port collisions," but `HomeIsolation` does not
allocate ports today. Three options were considered:

1. **Mock a port allocator and assert per-eval port distinctness.**
   Rejected — the assertion would be on the mock, not on the real
   code, so it would not regress when the real code grew a real port
   allocator.
2. **Bind real sockets in the worker and assert no `OSError: Address
   already in use`.** Rejected — flaky on hosts where another test or
   process happens to hold a port, and the test's failure mode would
   be indistinguishable from "host had something else on port X."
3. **Assert no env key in the per-eval env dict carries `PORT` in its
   name.** Adopted. The structural assertion is a forward-pointer:
   the first regression that introduces port-bound state would have to
   add a `PORT`-suffixed env variable, which T7 would flag *before*
   any real port could be bound. When that day comes, T03.20 can be
   updated to enforce per-eval port uniqueness on the real allocator.

## Why `teardown(keep=True)` for every eval

The HOMEs need to survive past the worker return so the final
assertions can re-read the JSONL files. The pattern is identical to
the one `test_parallel_15.py` uses — `teardown(keep=True)` clears the
private `_home_path` slot (so `iso.home_path` raises after teardown)
but leaves the directory on disk. The test never depends on
post-teardown access through the instance; it always reads either
through the in-memory `records` list or through the canonical JSONL
file on disk.

## Why two suite classes (`AcrossTrials` and `WithinEachTrial`)

Splitting the assertions into two test classes keeps the failure
signal clean:

- A failure in `WithinEachTrial` means a *single trial* of 15
  evals lost isolation. T03.16's existing suite should already have
  caught this; if it didn't, the regression is intra-trial and the
  T03.16 surface is the place to fix it.
- A failure in `AcrossTrials` means inter-trial isolation broke.
  T03.16 cannot catch this by construction (it only runs one trial),
  so T03.20 owns the signal.

Both surfaces are exercised by the same 3×15 trial setup; the split
is purely about which slice of the contract a given test asserts.

## Wall-clock budget

The full file completes in ~0.4s on the dev host. That budget includes
3 × 15 = 45 `tempfile.mkdtemp` calls plus 45 JSONL writes plus the
orchestrator's thread-pool overhead. The test is comfortably below
any per-PR CI gating threshold.

## Out-of-scope items deliberately not implemented

- **Cancellation across trials.** Mixing cancellation into the
  cross-trial integration would conflate "did the cancel arrive
  promptly" with "did inter-trial isolation hold," diluting both
  signals.
- **PTY lifecycle.** T03.22 owns the PTY layer; cross-trial PTY
  testing is a future task if it ever becomes necessary.
- **Disk-budget breach mid-trial.** T03.19 owns the disk-budget
  surface; the no-shared-state assertion is orthogonal.
- **Real `auggie-first.jsonl` writer.** The AC names it as an example
  of a shared file handle; the harness does not currently emit one.
  Test 5 (JSONL path uniqueness) and Test 6 (contents belong to owner)
  are the structural proxies that will catch any such writer the
  moment it lands.

## Verification evidence

See `evidence.md` in this directory. Summary:
- 10/10 new tests pass in 0.40s.
- 64/64 regression tests pass across the new file plus
  `test_parallel_15.py` (T03.16), `test_orchestrator.py` (T03.15), and
  `test_home_isolation.py` (T02.11) in 2.85s.
