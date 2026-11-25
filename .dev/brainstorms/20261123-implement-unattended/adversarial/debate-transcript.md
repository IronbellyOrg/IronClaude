# Debate transcript (inline, one round)

Each lens argues the contested points of diff-analysis.md. The session plays all three; it is a single model, so this is a structured self-critique, not independent debate. Logged as such.

## Point 1 and 11: `--plan-only` and the approval flag name
- C: a plan-only run gives the owner a runnable plan and an executor-computed hash.
- A: the coordinator can compute SHA-256 itself; the managed ledger already pins the same value (managed-workspace.md, `PLAN:` line); a new run mode is new surface.
- B: a mode that only compares a hash is enough; never infer approval.
- Ruling: no `--plan-only`. The benefit "known to be runnable" is obtained for free by qualifying every task's AC before the first `start` line under `--unattended` (a `E-NO-AC` on task 7 after six tasks ran cannot be repaired on a managed plan, because the first start pins the plan, `E-PLAN-CHANGED`). `--approve-plan` rejected as a name: the command compares a hash, it does not approve anything.

## Point 9: E-ARCHIVE-BLOCKED as partial
- C: all tasks are done; partial lets the coordinator read the deliverable.
- A: WORKER-CONTRACT D2 freezes on `blocked` or `failed` with a STOP code and names E-ARCHIVE-BLOCKED as a stop with no halted task. Partial would let dependents start on an unarchived plan after "usable" is recorded.
- Ruling: A. FINAL `issues` is blocked (a person decides on a blocking defect), helper refusal and the skip flag are failed.

## Point 12: parallel batches
- A: forcing sequential changes behaviour.
- B: batch members get no ladder and halt `batch`, which needs a person; an unattended run should take the ladder.
- Ruling: B. Under `--unattended` the independent-set markers are ignored. Existing behaviour for attended runs is untouched.

## Point 13: extras
- A: 4 minute kill. B: waits of at most 4 minutes, 20 minute cap.
- Ruling: B. WC-10 asks for waits of at most 4 minutes so the session can heartbeat; killing a test suite at 4 minutes would turn normal suites into skips.

## Point 15: a task completed by a Ruling
- A: succeeded. B: partial.
- Ruling: B. A Ruling is a known unmet criterion accepted by a person; `succeeded` would hide it from the coordinator.

## Point 16: skip flag
- Neither proposal handled the managed case early. A managed run with `--skip-final-review` does all the work and then ends `E-ARCHIVE-BLOCKED` by design. Under unattended it is refused before any write.

## Point 3: previous contract
- B: move an existing contract to `.prev`. Rejected: the sibling commands refuse a directory that already holds a contract, and WC-6 gives every retry a new directory.
