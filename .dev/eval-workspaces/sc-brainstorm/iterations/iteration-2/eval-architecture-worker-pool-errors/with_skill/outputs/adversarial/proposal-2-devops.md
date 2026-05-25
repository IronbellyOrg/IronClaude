---
proposal_id: 2
persona: devops
model: sonnet
lens: deploy, rollout, on-call, operational surface
---

# Proposal 2 — DevOps: Migrate by Operational Pain, Not by Architectural Cleanliness

## Position

The architect's subsystem is fine in shape but wrong in *order*. Don't migrate fleets in dependency order; migrate them in **pain order**. The three fleets that caused Q1 incidents — `email-dispatch`, `image-processing`, `webhook-delivery` — go first. The billing-critical fleets (`billing-batch`, `webhook-delivery`) get a higher safety bar but still go *before* the easy wins. The 7 small fleets at the tail get bulk-migrated as a final pass, possibly using a code-mod tool.

## Migration order (concrete)

**Quarter A (now-ish through ~6 weeks)**:
1. **`email-dispatch`** — Q1 incident: $50k SMTP-credit burn from infinite retry. Highest-confidence win.
2. **`image-processing`** — Q1 incident: pod thrash. Migrating here also forces us to address the synchronous `image-processing → thumbnail-workers` call (open question Q5 in seed).
3. **`webhook-delivery`** — Q1 incident: silent drop, 6 hours of missed webhooks. Billing-critical; needs the full safety bar.

**Quarter B (next ~6 weeks)**:
4. **`billing-batch`** — billing-critical, no Q1 incident but the second highest-stakes fleet. Migrating it with the new subsystem proven on 3 less-critical fleets de-risks it.
5. **`ingest-workers`** — has an existing DLQ; useful migration to *drain* and consolidate.

**Quarter C (final pass)**:
6-12. **The 7 small fleets** — code-mod where possible (a script that rewrites the most common try/except → typed-error patterns), per-fleet code review, batch them in groups of 2-3 per PR.

## Operational surfaces the architect's plan under-specifies

1. **On-call runbook for the DLQ.** When DLQ X has a backlog of N messages, what does on-call do? "Replay them" is not a runbook. The runbook needs: how to identify *why* they failed (filter by error class), how to safely replay a subset, how to spot a poison-message cluster, how to escalate.

2. **DLQ retention + cost.** Per-fleet Kafka DLQs cost broker storage; per-fleet Postgres DLQs cost table growth. Need: retention policy per fleet, archival path for messages older than N days, cost dashboard.

3. **Replay rate-limiting.** A naive replay-everything operation on a 100k-message DLQ will *recreate* the original load spike. Replay tool MUST default to a rate-limit (e.g., 100 msg/sec) and require explicit override. Audit every override.

4. **Feature-flag tooling.** Per-fleet feature flag for the new error-handling code → existing config infra or new? If existing (`config/flags.yaml`), document. If new, that's a subsystem-of-a-subsystem and bumps cost ~1 sprint.

5. **Deployment cadence during migration.** A fleet mid-migration is in a fragile state. Don't deploy other fleet changes during its migration sprint without an explicit check. SRE needs to gate.

## Where I diverge from the architect

The architect's plan is "build the subsystem, then migrate." That's a 2-quarter scaffolding tax before any Q1-incident-class problem is fixed. **Invert it**: build the *minimum-viable subsystem* (taxonomy + per-fleet DLQ contract + CLI replay), migrate `email-dispatch` *first* (the worst offender), prove the model, then iterate. The web UI for replay can wait until 6+ fleets are on the new subsystem. The chaos harness can wait until 3 fleets are on it.

## Cost (operational)

- DLQ broker/storage: ~$2k/month new (vs the $40k/quarter retry cost — clear win).
- On-call training: 2 lunch-and-learns + a written runbook per fleet (~3 hours each).
- Quarterly chaos test: ~2 days/quarter SRE time once scaffolding is in place.

## What I'd push back on

Anyone saying "build the full architect spec before migrating any fleet" is choosing scaffolding cleanliness over incident reduction. The Q1 incidents are the *forcing function* — every week of delay on `email-dispatch` migration is direct exposure.
