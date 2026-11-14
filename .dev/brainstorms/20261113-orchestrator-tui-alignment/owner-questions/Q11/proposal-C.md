# Proposal C: no recurring chat report yet; park the clause

## Answer

Neither, for now. The coordinator's automated chat output stays the decision ledger (outstanding owner decisions and held items only), the sweep reply appears only when someone actually runs `/sc:sweep`, and #339's "static report in chat every 3 to 5 minutes" clause is parked until the coordinator loop and the contract note between observer and sweep both exist.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date, and the #339 clause is listed as deferred (for example as a row in the #534 follow-up table, the issue that tracks Phase 1 follow-ups).
- Section 6.7 of the spec (the coordinator's status output rule) drops its last sentence about an in-chat report; its first sentence already limits automated status to the decision ledger (merged-requirements.md:1040).
- No code, contract or skill edit.

## What it unlocks

- Matches what exists: the recurring coordinator loop is not built, and WC-16 (the worker-contract coordinator loop rule) says the sweep is a capped duty, not a scheduler (debate-transcript.md:625). A "every 3 to 5 minutes" promise has nothing to run it.
- Avoids committing to a format before the observer and sweep agree on one word list (the contract note, variant-5-original.md:216).
- Matches the owner's stated preference that automated checks show outstanding decisions only, not periodic status chatter (SEED Batch 2 item 8 quoted at merged-requirements.md:1040).

## What it costs or risks

- #339's explicit ask is not met in any form for now; the person still has to run a command or open a file to see the fleet.
- Leaves the sweep reply's chat-summary exception (pragmatic.md:22-23) in place without a stated purpose in the recurring loop.
- One more deferred item to track.

## What stays unresolved

- Which report (sweep, observer or both) the clause will mean when it is unparked.
- When the coordinator loop is built.
