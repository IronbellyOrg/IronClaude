# Proposal C: yes, eventually; v2 must be able to correct non-worker sessions, behind the trust layer

## Answer

Yes. v2's goal includes delivering course corrections to non-worker sessions (watcher-launched and person-started), as #423's "relay them to affected agents" intends, but only after the #339 trust layer exists; the first release reports only, and the design plans the delivery path now.

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- V2-01 (the #423 rewrite) keeps "relay to affected agents" as a goal, with "first release: report to the person or the coordinator only; delivery to other sessions after the #339 trust layer".
- Because v2 will relay to agents, the #339 trust decisions become v2 prerequisites for the delivery release (ADJ line 699), so SW-12 (the deferred phases: `/sc:close`, resume, trust layer) moves onto v2's path for that release, and Q16 (one grant vocabulary and audit format) must be answered first.
- V2-03 (the v2 design) must name the delivery channel for each non-worker class; none exists today (question.md fact 10).

## What it unlocks

- Keeps #423's stated purpose (proactive correction of affected agents) intact.
- Unattended watcher-launched sessions could eventually be corrected without a person in the loop.
- Gives the trust-layer work (#339 comment 2) a concrete consumer.

## What it costs or risks

- A new inbound channel into sessions the contract says are "never messaged" (WORKER-CONTRACT.md:288); poisoned content is the main risk, and signing alone does not stop it (#339 comment 2, "encryption alone is not enough", ADJ line 295).
- Pulls unbuilt phases (trust layer) onto v2's path and lengthens it.
- The delivery channel is unknown; designing for it now may be wasted if no safe channel exists.

## What stays unresolved

- Which channel reaches a person-started or watcher-launched session.
- Whether a person must approve each delivered correction.
