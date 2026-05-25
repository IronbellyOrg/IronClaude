---
proposal_id: 4
persona: security
model: sonnet
lens: data exposure, audit, replay safety, blast radius
---

# Proposal 4 — Security: The DLQ Is A Data-Exposure Surface, Treat It Like One

## Position

Every prior proposal treats the DLQ as an operational queue. **It is a data-exposure surface.** Failed messages contain customer PII, billing details, webhook payloads with API tokens, and (in `email-dispatch`) email-body content. A unified DLQ subsystem without a security model is a regression — today's per-fleet ad-hoc DLQs at least have *unintentional* access opacity; a centralized replay UI with default-broad permissions removes even that.

## Security requirements (mandatory, not optional)

### Access control

- **DLQ read access**: per-fleet IAM role, not engineer-wide. Today's `webhook_failures` Postgres table is readable by anyone with prod-read. New DLQ subsystem requires explicit grant: `dlq:read:<fleet>` and `dlq:replay:<fleet>`.
- **Replay execution**: requires `dlq:replay:<fleet>` AND a justification field (free-text, required, captured in audit log). Pre-approved playbooks (e.g., "replay after downstream incident") can pre-fill justification; ad-hoc replays require a manager approval in the UI for billing-critical fleets.
- **Web UI** (DevOps/architect deferred this): when it ships, MFA required, session-based, default-deny.

### Data handling

- **PII redaction at DLQ-write time**: any message with a field tagged `pii=true` in the producer schema gets the PII field hashed or redacted before DLQ persistence. Producers update their schemas to tag PII (~1 day per fleet). The DLQ never persists raw PII.
- **Token redaction**: webhook payloads with `Authorization` / `X-Api-Key` headers get those headers stripped before DLQ storage. Replay attempts on these messages require re-fetching credentials (the replay tool prompts; doesn't silently use cached).
- **Retention**: hard cap per fleet (default 30 days). Auto-delete past retention with audit. Retention is a *security* requirement, not just a cost requirement — older failed messages are a higher-blast-radius data trove.

### Audit

- Every DLQ write, read, and replay logged to the existing `internal/audit/event_log.py` with: `actor` (service or human), `action`, `fleet`, `message_id`, `justification` (if human), `result`.
- Audit log is **append-only** and replicated to a separate retention store (SOC2 evidence).
- Quarterly access review: list every `dlq:read:*` and `dlq:replay:*` grant, owner re-attests.

### Replay safety

- **Replay sandbox mode**: option to replay against a non-prod downstream for verification before prod replay. Required for billing-critical fleets when the replay size > 100 messages.
- **Replay throttle**: rate-limit (DevOps' point) is also a security control — it prevents a compromised account from flooding downstreams or exfiltrating via timing-channel replay.
- **No "replay all" affordance** in the UI for billing-critical fleets. Replay batches must be ≤1000 messages; larger requires a CLI invocation that explicitly logs the operator's CIDR.

## Threat model (explicit)

1. **Insider misuse**: An engineer with prod-read replays a customer's failed webhook to a downstream they don't normally hit. *Mitigation*: per-fleet IAM, justification field, audit log, quarterly access review.
2. **Compromised service account**: A service token leaks; attacker uses it to read DLQ data. *Mitigation*: rotating service tokens, fleet-scoped IAM, anomaly alert on read-rate spikes.
3. **Information disclosure via failed messages**: A bug puts a token in a log line, which ends up in the DLQ envelope. *Mitigation*: redaction at write time + retention cap.
4. **Replay amplification attack**: An attacker who gains replay access uses it to trigger downstream-exhausting load. *Mitigation*: rate-limit, manager approval for billing-critical, sandbox mode.

## Where I push back on prior proposals

**Architect's audit log via `internal/audit/event_log.py`**: correct *substrate*, but the architect didn't specify what fields get logged. Specify them (above).

**DevOps's "replay rate-limit defaults"**: necessary but not sufficient. Rate-limit + justification + audit + per-fleet IAM are the *package* — pulling any one out makes the others weaker.

**QA's chaos harness**: should add a 9th test — replay a message with PII, assert PII is redacted in the audit log and not re-exposed in transit.

## Cost

~1 sprint to wire the IAM model into the new subsystem. ~0.5 sprint per producer to tag PII fields (12 producers × 0.5 = 6 sprints, parallelizable). Retention + audit: ~0.5 sprint. Replay UI security (deferred to UI build): ~1 sprint *added* to the UI work.
