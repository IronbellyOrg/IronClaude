# Proposal B: one sentence in the guide's Orca section, not a table row

## Answer

Yes to discoverability, but as one bullet in the prose "Orca coordination" section of `HOW-WE-WORK.md` (the routing guide), saying the person can watch workers with `superclaude observe` in their own terminal, person only, never as a worker. No row in the machine-read routing or other-commands tables. Own small PR after PR #539 merges.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- OB-07 (the routing-row work item) is reworded from "row" to "bullet in Orca coordination", and its test-edit acceptance items are dropped because the two table tests do not read that section (`tests/core/test_how_we_work_routing_table.py` checks only the marked level, routing and other-commands blocks, lines 22-24).
- A supervised worker adds the bullet, copies the guide byte-for-byte to the plugin mirror (project CLAUDE.md rule), and runs the routing tests to show nothing broke; the PR session opens the PR with `/sc:pr-submit --monitor 3`.

## What it unlocks

- The observer becomes findable next to the `/sc:sweep` bullet it complements (`HOW-WE-WORK.md:398` onward).
- No test edits: INV-029 (an invariant-probe finding that a CLI-only entry fits neither machine-read table without a test change) does not apply.
- The "person only" sentence (INV-013) has a natural home: the same section already says which commands are never workers.

## What it costs or risks

- `/sc:recommend` may not route to a bullet the way it routes to a table row (UNVERIFIED how it weighs prose).
- It still touches the guide and its mirror, which PR #539 also edits, so it still waits for #539 to merge.
- It differs from the spec's planned shape for OB-07, so the spec row and its test acceptance items change.

## What stays unresolved

- Whether a table row is still wanted later, for example once the observer has a slash command or reaches its next release.
