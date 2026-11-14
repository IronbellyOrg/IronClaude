# Proposal B: the gate is PR #539 merged, the capture recorded, and the `working` class restored in code

## Answer

For #423, "#339 is complete" means three things: PR #539 (the read-only sweep) is merged, the shared live Orca capture (#534) is recorded, and the sweep's `working` class is restored in code from that capture, with its test and its #534 row closed. The other #339 phases are prerequisites only if v2 relays to agents.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- SW-14 (restore the `working` class) becomes required: after the capture (XC-03), a supervised worker restores Rule 5's four conditions from the recorded names (`classify.py:251-257`), adds a pinning test, and the PR session opens the PR with `/sc:pr-submit --monitor 3` under the owner's grant row; the #534 row is closed.
- V2-01 (the #423 rewrite) states the three-part gate; V2-02 (the gate check) passes only when SW-14 has merged.
- V2-05 (the v2 research pass) still runs early, because it is ungated.

## What it unlocks

- v2 is designed against a sweep that can actually say a session is working, rather than "could not determine" for every such row (classify.py:251-257 comment; design open item 6).
- Matches ADJ's own words most literally: "the #534 live capture that restores the sweep's `working` class" (ADJ line 294, 699).
- Removes the record-versus-code ambiguity (X-009) by choosing the stricter reading.

## What it costs or risks

- Adds a code PR (SW-14) to v2's critical path, after a live capture that needs Orca reachable and an owner answer on who runs it (Q24).
- v2 starts later; it is a planning gate, and v2 is advisory only.
- If the capture shows the four conditions cannot be built from what Orca exposes, v2 waits on a sweep redesign.

## What stays unresolved

- Whether v2 relays to agents (decided in the brainstorm; Q15 bears on it).
