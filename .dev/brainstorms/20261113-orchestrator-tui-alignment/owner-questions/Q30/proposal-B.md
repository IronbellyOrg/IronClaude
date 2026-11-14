# Proposal B: a real coordinator Run from the owner's ordinary work, at a quiet moment, with written acceptance

## Answer

OB-04 reads one real coordinator Run that the owner is already running for other work (never this alignment program's own coordinator), at a moment when no worker in it is waiting on an answer; the owner accepts in writing that a question in that Run may be consumed, and names the Run id before the attempt.

## What happens next if the owner picks it

1. After OB-03 passes, the owner picks a Run from ordinary work, records its id and the acceptance sentence in the ledger with `GRANT(OB-04,live-read)`.
2. In that coordinator's own terminal (the only one that can read it, Q-1), at a quiet moment, the observer runs its exact read; no `run-use`.
3. The record notes the Run id, the terminal, whether any question disappeared (checked against the coordinator's own view before and after), and whether the panel was usable.
4. If a question disappears, OB-06 is held and the owner re-asks it in that coordinator.

## What it unlocks

- The most representative evidence possible: a real coordinator with a live `--wait` listener and real acknowledgements, in the layout people will actually use.
- No extra setup: no throwaway coordinator session, worker or worktree.

## What it costs or risks

- If the read does consume, a real question in the owner's other work is lost; the "quiet moment" lowers but does not remove that risk.
- The owner's other work is exposed to a test; the owner must accept that in writing.
- Choosing "quiet" depends on the owner's judgment of that Run's state.

## What stays unresolved

- Whether one real Run's result generalises to other Runs and other Orca builds.
