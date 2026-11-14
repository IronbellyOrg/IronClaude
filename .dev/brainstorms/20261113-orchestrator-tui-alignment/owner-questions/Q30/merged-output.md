<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (proposal-C) -->
<!-- Merge date: 2026-11-14T03:10Z -->

# Merged answer for Q30: which coordinator Run OB-04 reads

<!-- Source: Base (original) -->
## Answer

OB-04 reads a disposable coordinator Run that the owner opens only for this test, made representative by a live `--wait` listener and one question-and-acknowledgement cycle with a test worker; never the alignment program's own coordinator Run. The owner accepts in writing that questions in that disposable Run may be consumed.

<!-- Source: Base (original, modified) - steps reordered and extended per Changes 1, 2, 3 -->
## What happens next

1. Preconditions: OB-03 (the seeded test) has passed, Orca answers, and the ledger holds the Run id, the acceptance sentence and `GRANT(OB-04,live-read)`. If any is missing, OB-04 stays held and OB-06 waits.
2. The owner opens a coordinator session for the test and creates its Run. Preflight: from that session's own terminal, confirm the observer starts and can read the Run at all; "not usable in the holder terminal" is a valid recorded result that holds OB-06.
3. The owner starts one test worker on a trivial task that asks one known question. While that question is still unanswered and the coordinator's `--wait` is armed, the observer runs its exact read in the holder terminal (no `run-use`).
4. Loss is judged against ground truth, never with a plain `check` (which removes messages): the known question must still reach the coordinator through its `--wait`, be answered, and be acknowledged by the worker. The record names the Run id, the terminal, whether the question survived, and whether the panel was usable, plus the Orca build string.
5. The test Run, worker and worktree are closed; OB-06 can link the record.

## What it unlocks
Live evidence with a real listener and acknowledgement cycle, which the seeded test lacks, with nothing of value at risk; OB-06 can then proceed once its other prerequisites hold.

## What it costs or risks
- Setup: a test coordinator session, a test worker and its worktree; the owner opens the coordinator personally.
- One worker and one question show the mechanism, not real message volume.

## What stays unresolved
- Whether the result holds on other Orca builds (OB-05's build pin covers that).
