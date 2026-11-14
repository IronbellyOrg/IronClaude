# Proposal A: no routing entry for now

## Answer

No. The observer stays out of the routing guide until it is fully switched on (its coordinator-questions panel is still off on master) and the contract note between the observer and the sweep is written; the question is asked again then.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- Work item OB-07 (the routing-row PR) does not start; its #534 follow-up row (the sweep's follow-up list) reads "deferred by owner".
- No file in the routing guide, its plugin mirror, the sc-recommend table or the routing tests changes.

## What it unlocks

- No change to two machine-read test tables that a CLI-only entry does not fit (INV-029, an invariant-probe finding: `tests/core/test_how_we_work_routing_table.py:193-205` and `:297-298`).
- No PR, no review cycle and no rebase against PR #539, which edits the same four files.
- Avoids advertising a dashboard whose question panel is still off (the guard is `False` on master; owner question Q6) and whose words do not yet match the sweep's (the contract note is unwritten).

## What it costs or risks

- The observer stays hard to find: no routing guide, user guide or command file mentions `superclaude observe` today (grep, 2026-11-14). A person or agent asking "how do I see my workers" is not pointed at a tool that already exists.
- `/sc:recommend`, which routes from the guide, cannot suggest it.
- The "person only" sentence (INV-013) is written nowhere, so nothing tells an agent not to run it as a worker.

## What stays unresolved

- When, and in what form, the observer becomes discoverable.
