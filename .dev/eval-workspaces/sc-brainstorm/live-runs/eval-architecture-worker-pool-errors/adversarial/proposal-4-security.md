---
proposal_id: 4
persona: security
model: sonnet
lens: data exposure and replay safety
---

# Proposal 4 — Security: Redaction, Replay Authorization, and Auditability

## Position

Treat failure envelopes and replay as security-sensitive surfaces. Error records often contain payloads, stack traces, paths, and credentials; replay can repeat harmful side effects.

## Requirements Emphasis

- Error envelopes must separate safe metadata from sensitive payload fragments.
- Redaction rules must run before persistence or display.
- Replay requires authorization, justification, rate limits, and immutable audit records.
- Non-idempotent work must not be auto-replayed without explicit approval.
- Failure logs must avoid leaking secrets while preserving enough diagnostic context.

## Risks

- Storing raw exception context may expose secrets or customer data.
- Replay without authorization can duplicate side effects.
- Audit gaps make incident review impossible.

## Acceptance Focus

A security review can verify that failure data is redacted, replay is controlled, and every manual intervention is traceable.
