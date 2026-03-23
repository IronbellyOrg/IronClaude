# M5: Retry-once vs MAX_CONCURRENT Batch Conflict — Remediation Proposal

## Problem

When a topological level dispatches a full batch of `MAX_CONCURRENT = 10` tasks, the current spec says failed tasks retry once but does not define how that retry interacts with the hard concurrency cap.

This creates an ambiguity:
- If a failed task retries immediately, the system may exceed the cap or consume a slot that was not explicitly reserved.
- If multiple tasks fail in the same full batch, later failures may have no retry slot available.
- The scheduler behavior becomes timing-dependent, which makes execution nondeterministic and harder to reason about.

## Design Decision

**Retries MUST NOT execute immediately when the original batch is still in flight.**

Instead:
1. A full sub-group dispatches up to 10 tasks.
2. Any task that fails on its first attempt is marked `retry_pending`.
3. The orchestrator continues waiting until **all first-attempt tasks in that dispatched sub-group reach a terminal attempt-1 state**:
   - `completed`
   - `failed_retry_pending`
   - `manual` / `timed_out_no_retry` if some other policy makes retry inapplicable
4. Only after the sub-group’s initial pass is fully drained does the orchestrator open a **retry pass** for that same sub-group.
5. Retry tasks run **within the same `MAX_CONCURRENT = 10` cap**.
6. The next sub-group at the same topological level does **not** begin until both the initial pass and retry pass for the current sub-group are complete.

This makes retry scheduling deterministic and keeps concurrency accounting simple: **attempts and retries use the same capped execution window, but never overlap within a sub-group.**

---

## Step-by-Step Execution Model

### Step 1: Split topological level into capped sub-groups

For any topological level:
- If task count `N <= 10`, there is one sub-group.
- If `N > 10`, split into sequential sub-groups of at most 10 tasks each.

Example:
- 23 ready tasks → sub-group A (10), sub-group B (10), sub-group C (3)

### Step 2: Run the sub-group initial pass

For the active sub-group:
- Dispatch all tasks in the sub-group, up to 10 concurrent.
- No retry is dispatched while any first-attempt task from that sub-group is still running.

Task outcomes during initial pass:
- Success → mark `completed`
- First failure eligible for retry → mark `retry_pending`
- Failure not eligible for retry → mark terminal failure state

### Step 3: Drain initial pass before any retry starts

The sub-group initial pass is considered complete only when every task in that sub-group has finished its first attempt.

This is the critical rule that resolves M5:
- A first-attempt failure does **not** immediately consume a new slot.
- The failed task simply joins a retry queue for that sub-group.
- Additional first-attempt failures in the same sub-group also join that retry queue.

So if 3 of 10 tasks fail, the retry queue becomes `[t2, t7, t9]`, but none retries until the other 7 first-attempt executions have finished.

### Step 4: Open a retry pass for the same sub-group

Once the initial pass is fully drained:
- Collect all `retry_pending` tasks from that sub-group.
- Dispatch them as a retry pass, still under the same concurrency cap of 10.

Because only retry-eligible failures are in the retry pass, the retry pass size is always `<= 10`.

Examples:
- 1 failed task → retry pass of 1
- 4 failed tasks → retry pass of 4
- 10 failed tasks → retry pass of 10

### Step 5: Do not retry a retry

Each task gets at most one retry.

Retry-pass outcomes:
- Retry success → mark `completed`
- Retry failure → mark terminal `failed`
- Retry timeout under timeout policy → mark terminal per timeout policy (`manual` or `failed`)

A retry failure never creates another queue entry.

### Step 6: Advance only after sub-group fully settles

A sub-group is complete only when:
- all initial-pass tasks have finished, and
- all retry-pass tasks have finished

Only then may the orchestrator:
- start the next sub-group in the same topological level, or
- if none remain, advance to the next topological level

---

## Retry Slot Management

## Core Rule

**There is no permanently reserved retry slot.**

Instead, retry capacity is created by **phase separation**:
- Initial-pass tasks use up to 10 slots
- After initial pass drains, those same slots are reused for retry-pass tasks

This is preferable to a 9+1 reservation model because:
1. It preserves full throughput for the common case where no task fails.
2. It handles multiple failures naturally.
3. It avoids waste from an idle reserved retry slot.
4. It eliminates timing races around “which failure gets the reserve slot.”

## Scheduler Invariant

At all times within a sub-group:

`running_initial_attempts + running_retries <= MAX_CONCURRENT`

And additionally:
- if any `running_initial_attempts > 0`, then `running_retries = 0`
- retries may run only after `running_initial_attempts = 0` for that sub-group

In plain language: **initial attempts and retries never overlap inside the same sub-group.**

---

## Exact Ordering Rules

The spec should define the following precise ordering:

1. Determine ready tasks for current topological level.
2. Partition into sub-groups of at most 10.
3. For each sub-group, in order:
   1. Dispatch all tasks in initial pass.
   2. Wait until all initial-pass tasks finish.
   3. Build retry queue from first-attempt failures eligible for retry.
   4. If retry queue is non-empty, dispatch retry pass under same cap.
   5. Wait until all retries finish.
   6. Mark sub-group complete.
4. After all sub-groups in the topological level complete, advance to the next topological level.

This means:
- retries happen **after batch completion**, not during batch execution
- retries for sub-group A finish before sub-group B starts
- later topological levels never start while retries from an earlier level remain unresolved

---

## Concrete Example

### Scenario

- `MAX_CONCURRENT = 10`
- Topological level L has exactly 10 tasks: `T1..T10`
- `T3` and `T8` fail on first attempt

### Correct behavior

#### Initial pass
- Dispatch `T1..T10`
- `T3` fails → mark `retry_pending`
- `T8` fails → mark `retry_pending`
- Remaining tasks continue to completion
- No retry starts yet

#### Retry pass
- Initial pass is now drained
- Retry queue = `[T3, T8]`
- Dispatch retry of `T3` and `T8`
- If `T3` succeeds, mark completed
- If `T8` fails again, mark terminal failed

#### Advancement
- Sub-group completes only after `T3` and `T8` retry pass settles
- Only then may the scheduler move to the next sub-group or topological level

### Why this solves M5

At no point does the system need an 11th slot.
At no point does one failed task block another failed task from receiving its retry.
The retry queue can hold multiple failed tasks without violating concurrency.

---

## Manifest / Status Model

To make this behavior explicit, add attempt-aware states or fields.

Recommended per-task fields:

```json
{
  "id": "task_7",
  "status": "pending|running|completed|retry_pending|failed|manual",
  "attempt": 1,
  "max_attempts": 2,
  "first_error": "message|null",
  "final_error": "message|null"
}
```

Recommended sub-group runtime bookkeeping:
- `initial_pass_total`
- `initial_pass_completed`
- `retry_queue_count`
- `retry_pass_completed`

Minimum semantic requirements:
- first-attempt failures that will be retried must be distinguishable from terminal failures
- manifest should show that a task is waiting for retry, not silently stuck

---

## Normative Spec Text

Use language like this in the Spawn V2 spec:

### Retry Scheduling

- A task that fails on its first attempt and is eligible for retry MUST be marked `retry_pending`.
- A retry MUST NOT be dispatched while any first-attempt task in the same dispatched sub-group is still running.
- After all first-attempt tasks in the sub-group complete, the orchestrator MUST execute a retry pass containing all `retry_pending` tasks from that sub-group.
- Retry passes MUST execute under the same `MAX_CONCURRENT = 10` limit as initial dispatches.
- A retry failure MUST be terminal unless another policy explicitly overrides it.

### Concurrency Interaction

- The concurrency cap applies to both initial attempts and retries.
- Initial attempts and retries for the same sub-group MUST NOT overlap.
- The next sub-group in the same topological level MUST NOT start until the current sub-group’s retry pass, if any, has completed.
- The next topological level MUST NOT start until all sub-groups and retry passes in the current level have completed.

---

## Rejected Alternative: Reserve 1 Retry Slot

The alternative is to reserve capacity inside the 10-cap, effectively running `9 normal + 1 retry reserve`.

This is weaker than deferred retry because:
- it reduces steady-state throughput even when no failures occur
- it still needs additional policy for multiple simultaneous failures
- it introduces fairness questions about retry ordering
- it complicates batching logic for little benefit

Therefore the recommended approach is:

**Use full-cap initial dispatch, then deferred retry pass after batch drain.**

---

## Final Recommendation

Adopt the following simple rule:

**Retries execute only after the active capped sub-group finishes its first-attempt batch. Failed tasks from that sub-group enter a retry queue, and that queue is drained in a retry pass that reuses the same `MAX_CONCURRENT = 10` slots. No next sub-group or next topological level starts until the retry pass finishes.**

This gives Spawn V2:
- deterministic scheduling
- no cap violations
- support for multiple same-batch failures
- no wasted reserved slot
- clear manifest semantics and easier implementation

## Files to Update

- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md`
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/remediation/major/M5-retry-batch-conflict.md`
