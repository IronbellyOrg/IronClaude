# Proposal C: the gate is PR #539 merged plus the shared capture recorded

## Answer

For #423, "#339 is complete" means PR #539 (the read-only sweep) is merged and the shared live Orca capture (#534) is recorded. Restoring the sweep's `working` class in code is not part of the gate. `/sc:close`, resume and the trust layer are prerequisites only if the v2 brainstorm decides v2 relays to agents, not only to a person.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date; it is also the spec's default reading (merged-requirements.md:541).
- V2-01 (the #423 rewrite) states: "starts after PR #539 merges and the #534 shared capture is recorded"; the words "that restores the sweep's `working` class" are dropped or reworded as "that records the values the `working` class needs".
- V2-02 (the gate check) passes on a dated ledger entry citing the merge and the capture record (merged-requirements.md:399).
- SW-14 (restore the class) is not needed for v2; it stays a #534 follow-up.

## What it unlocks

- v2 is designed with the real live values in hand (the `agentWait`, `liveness` and `status` names and `projection.attention` for a live and a blocked worker), without waiting for a code PR.
- Keeps the gate a matter of records, which a ledger entry can check, rather than a code change on the critical path (spec weak point W5, merged-requirements.md:415).
- Close to ADJ's recommendation (line 294) and keeps the other phases out unless v2 relays to agents.

## What it costs or risks

- v2 can be built while the sweep still shows working sessions as "could not determine" (classify.py:251-257), so v2 must carry that gap.
- Still waits on a live capture, which needs Orca reachable and an owner answer on who runs it (Q24).
- Departs slightly from ADJ's literal wording ("restores").

## What stays unresolved

- When the `working` class is restored.
- Whether v2 relays to agents (brainstorm; Q15 bears on it).
