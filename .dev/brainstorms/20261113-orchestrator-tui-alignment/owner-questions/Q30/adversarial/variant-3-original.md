# Proposal C: a disposable representative Run opened for the test, never the program's own

## Answer

OB-04 reads a disposable coordinator Run the owner opens only for this test, made representative by a live `--wait` listener and at least one question-and-acknowledgement cycle with a test worker; never the alignment program's own coordinator Run. The owner accepts in writing that questions in that disposable Run may be consumed.

## What happens next if the owner picks it

1. After OB-03 passes, the owner opens a coordinator session for the test, creates its Run, and starts one test worker on a trivial task that asks one question; the coordinator answers and the worker acknowledges, while the coordinator keeps a `--wait` armed.
2. The owner records the Run id, the acceptance sentence and `GRANT(OB-04,live-read)` in the ledger.
3. In that coordinator's own terminal, the observer runs its exact read (no `run-use`); the record notes the Run id, the terminal, whether any question disappeared, and whether the panel was usable.
4. The test Run, its worker and its worktree are closed afterwards; OB-06 can then link the record.

## What it unlocks

- Live evidence with a real listener and acknowledgement cycle, which the seeded test lacks, while nothing of value can be lost.
- OB-06 (the guard flip) can proceed once its other prerequisites hold.

## What it costs or risks

- Setup: a test coordinator session, a test worker and its worktree (worker-start creates one), and Orca must be reachable.
- A synthetic Run may still differ from real use (one worker, one question), so it is representative only in mechanism.
- The owner must open the session personally, since a coordinator is person-opened.

## What stays unresolved

- Whether the result holds on other Orca builds (the build pin of OB-05 covers that).
