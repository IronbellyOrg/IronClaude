# Proposal A: the gate is PR #539 merged; the live capture gates only what reads live values

## Answer

For #423, "#339 is complete" means PR #539 (the read-only sweep) is merged. The live Orca capture is not a gate on v2 as a whole; it gates only those v2 features that would read the values it records (the `working` class and `projection.attention`). The other #339 phases are prerequisites only if v2 relays to agents.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- V2-01 (the #423 rewrite) states: "starts after PR #539 merges; any v2 field that depends on live Orca values waits for the shared capture (#534) and is marked pending until then".
- V2-02 (the gate check) passes on the #539 merge alone. V2-03 (the v2 brainstorm) can start then, designing around the capture's open values instead of waiting for them.
- SW-14 (restoring the sweep's `working` class) is not a v2 gate; it stays a #534 follow-up.

## What it unlocks

- v2 design starts as soon as the sweep lands, without waiting on a live Orca session, which was unavailable on 2026-11-13 (merged-requirements.md:604) and needs an owner answer on who runs it (Q24).
- The gate matches what v2 actually reads: most catalogue fields (sessions, worktrees, packages, git state) come from the sweep's report, not from the uncaptured values.
- Removes the record-versus-code ambiguity (X-009) by not tying the whole gate to either.

## What it costs or risks

- The v2 design may assume field names or meanings that the capture later contradicts, so parts are redone.
- Departs from ADJ's recommended gate (line 294) and its proposed #423 text (line 699), so the rewrite needs new wording.
- A v2 built before the `working` class exists shows working sessions as "could not determine" (classify.py:251-257).

## What stays unresolved

- Which v2 fields are "live-value dependent"; the brainstorm must list them.
- Whether v2 relays to agents (decided in the brainstorm; Q15 bears on it).
