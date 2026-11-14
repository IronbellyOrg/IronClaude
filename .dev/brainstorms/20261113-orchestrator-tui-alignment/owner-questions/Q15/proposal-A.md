# Proposal A: never; a standing rule that no program messages a non-worker session

## Answer

No, never. Make it a standing rule, not a first-release limit: v2 (and any later automated program) never delivers anything into a session that is not an Orca worker; for those sessions it only reports to the person, and workers are reached only through the coordinator's existing pulled follow-ups (WC-12).

## What happens next if the owner picks it

- The answer is recorded in the decision ledger with its date.
- V2-01 (the #423 rewrite) replaces "relay them to affected agents" with "report to the person or the coordinator; workers receive coordinator follow-ups (WC-12) only; no delivery to any other session, now or later".
- V2-03 (the v2 design) states the rule for each session class without a "revisit" clause.
- The rule can be copied into the worker contract next to "they are never messaged" (WORKER-CONTRACT.md:288) by a later, separately approved PR; this answer does not authorize that edit.

## What it unlocks

- The #339 trust layer (Phase 4) is never a v2 prerequisite for delivery, so v2's gate stays as Q14 sets it (ADJ line 699).
- The simplest trust boundary: no new inbound channel into a person's own session exists to defend, sign or audit.
- Matches today's contract wording for person-started sessions (WORKER-CONTRACT.md:288).

## What it costs or risks

- Closes a door #423 opened ("relay them to affected agents"); reopening it later needs a new owner decision that overrides a stated standing rule.
- Watcher-launched sessions, which may run unattended, can never be corrected automatically; a person must act on the report.
- Constrains future designs (for example the orchestrator of orchestrators in #339 comment 1) before they are researched.

## What stays unresolved

- How quickly a person sees and acts on a report for an unattended session.
