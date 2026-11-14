# Proposal B: report only (advisory) for v2; no delivery to non-worker sessions

## Answer

v2 reports to the person or the coordinator only. It delivers no course correction into a session that is not an Orca worker; corrections for workers go through the coordinator's pulled follow-ups (WC-12). Any wider delivery would be a later, separate owner decision.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date; it is also the default if unanswered (merged-requirements.md:542).
- V2-01 (the #423 rewrite) uses ADJ's proposed text: "The first release delivers to the person or the coordinator only", and per session class "a coordinator follow-up (WC-12) for workers, a report to the person for the rest" (ADJ lines 705, 714).
- V2-03 (the v2 design) states, for each session class, what is observable and that correction is a report for non-workers.
- Because v2 does not relay to agents other than through the coordinator, the #339 trust layer is not a v2 prerequisite (ADJ line 699; links to Q14).

## What it unlocks

- v2 can be designed and built without a new inbound channel or a signing scheme.
- Matches the contract as it stands: workers pull follow-ups (WORKER-CONTRACT.md:61); person-started sessions "are never messaged" (WORKER-CONTRACT.md:288).
- Keeps v2 advisory, consistent with the sweep's "recommends nothing" split (round2-rebuttal-V4.md:118).

## What it costs or risks

- Narrows #423's "relay them to affected agents" for non-worker sessions.
- Unattended watcher-launched sessions get no automatic correction.
- "Later, separate decision" leaves the long-term direction open, so a future design may reopen it.

## What stays unresolved

- Whether a later release should deliver to non-worker sessions, and under which trust design (Q16 bears on it).
