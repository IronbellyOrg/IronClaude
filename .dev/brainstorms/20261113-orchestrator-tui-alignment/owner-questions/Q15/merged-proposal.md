<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->

# Merged proposal: report only, with a named condition for ever reopening it

<!-- Source: Base (original, modified) - Change 1 -->
## Answer

v2 reports to the person or the coordinator only. It delivers no course correction into a session that is not an Orca worker. For a worker, v2 hands the correction to the coordinator, which decides whether to send a pulled follow-up (WC-12); v2 never sends one itself. Any wider delivery is a later, separate owner decision, taken only under the conditions below.

<!-- Source: Base (original, modified) - Changes 2, 4 -->
## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date; it is also the default if unanswered (merged-requirements.md:542).
- V2-01 (the #423 rewrite) uses ADJ's proposed text: "The first release delivers to the person or the coordinator only", and per session class "a coordinator follow-up (WC-12) for workers, a report to the person for the rest" (ADJ lines 705, 714).
- V2-03 (the v2 design) states, for each session class, what is observable and that correction is a report for non-workers. It shapes the typed fields and audit record so that a later delivery release, if ever approved, would not force a store migration; it designs no delivery path. (Change 4)
- Because v2 does not relay to agents other than through the coordinator, the #339 trust layer is not a v2 prerequisite (ADJ line 699; links to Q14).
- The question is reopened only when a delivery channel into the session class is named, a threat model for poisoned content exists, it is decided whether a person approves each delivered correction, and Q16 (one grant vocabulary and audit format) is answered. (Change 2)
- Optional, by a separate approved PR only: one sentence beside the contract's "they are never messaged" (WORKER-CONTRACT.md:288) saying v2 does not message non-worker sessions.

<!-- Source: Base (original) -->
## What it unlocks

- v2 can be designed and built without a new inbound channel or a signing scheme.
- Matches the contract as it stands (WORKER-CONTRACT.md:61, :288).
- Keeps v2 advisory, consistent with the sweep's "recommends nothing" split.

<!-- Source: Base (original, modified) - Change 3 -->
## What it costs or risks

- Narrows #423's "relay them to affected agents" for non-worker sessions.
- Open case: unattended watcher-launched sessions get no automatic correction; if no person reads the report in time, such a session keeps going. (Change 3)

<!-- Source: Base (original, modified) - Change 2 -->
## What stays unresolved

- Whether a later release should deliver to non-worker sessions; reopened only under the condition above.
