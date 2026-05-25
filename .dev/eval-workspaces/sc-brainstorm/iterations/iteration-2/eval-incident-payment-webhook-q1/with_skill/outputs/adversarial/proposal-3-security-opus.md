---
proposal_id: 3
persona: security
model: opus
lens: PCI-DSS scope, credential handling, audit-evidence chain, adversarial inputs
---

# Proposal 3 — Security (opus): The Compliance Posture Is Worse Than We're Telling Auditors

## Position

Both analyzer proposals frame this as a reliability problem. It is also — and possibly primarily — a **compliance and credential-handling problem**. Two of the facts in the seed brief are individually fine and together damning:

1. The DLQ table has no TTL, no compaction, and grew past 2M rows. We are claiming PCI-DSS §10.2 evidence-chain compliance with an unbounded, unaudited storage tier in the chain.
2. Some merchants 200-OK then drop on their side. Our "delivered" count is over-counted by an unknown margin. Our internal audit reports a delivery rate; that rate is not corroborated by merchant-side reconciliation.

Either of these alone is a finding. Together they say: **the PCI evidence chain has gaps we don't measure**. If an auditor subpoenas the chain for a specific transaction during a chargeback dispute, we cannot prove what we currently tell them we can prove.

## Required investigation steps

1. **End-to-end evidence-chain audit** for a sample of 100 transactions across the three Q1 incidents. For each: (a) does the dispatcher have a delivery-attempt record? (b) does the merchant's reconciliation show receipt? (c) if (a) says delivered and (b) says missing, what's our compliance posture?
2. **HMAC signing-key handling review.** Are merchant signing keys in any logs (request, response, retry, DLQ replay)? Are they redacted in error traces? What's the rotation cadence? Who has read access to the key store?
3. **DLQ contents PII/PCI scoping review.** Webhook bodies are claimed to not contain PAN; verify this is enforced at producer time, not just by policy. Verify the DLQ table is in PCI scope and inherits the same controls (encryption-at-rest, access logging, retention bounds).
4. **Threat-model the merchant-side pathologies.** A malicious or compromised merchant returning 200-OK-then-drop creates plausible deniability for fraud cooperation. Is there a detection surface? Should there be?

## Required remediations

- **S1** — **Bounded DLQ with cryptographic chain-of-custody.** Each DLQ entry signed at producer time, retention 18 months (matching PCI-DSS §10), eviction signed at evictor time with audit-log entry. Replay produces a new chain entry, not a mutation of the original. This is *the* PCI fix.
- **S2** — **Merchant-side delivery corroboration.** For Tier-1 enterprise merchants, an optional `webhook-ack` callback (we send → merchant processes → merchant calls back our /ack endpoint with the transaction ID). For merchants that don't opt in, document explicitly that our "delivered" count is one-sided and revise the §10.2 evidence claim to match. **Do not continue claiming what we cannot prove.**
- **S3** — **HMAC signing-key rotation policy.** Quarterly forced rotation for all merchants, with a 14-day overlap window. Hard requirement for SOC2 + PCI renewal. Aligns with the merchant-side auth-rotation pathology from Q8 (we are not the only side that rotates badly).
- **S4** — **Signing-key handling in logs/traces.** Redaction at log-write time, never log-read time. Audit existing log retention for any historical key exposure. If found, rotate affected merchants immediately, notify on legal advice.
- **S5** — **Access logging on the DLQ table itself.** Every read of a webhook body in the DLQ generates an audit entry — operator name, timestamp, transaction ID, justification field. Today reads are unaudited.

## What I'd push back on

Proposal 1 names observability as the root cause. Proposal 2 names architectural amplification. Both are correct from their lens. **Neither names the compliance-evidence gap, and that's the one finding that turns into a Form 8-K disclosure if it surfaces during an audit.** Reliability remediation that doesn't carry compliance-grade evidence is technically debt being repaid into the wrong account.

## What I'd concede to Proposals 1 & 2

Proposal 1's latency-drift alert (R1) is necessary regardless of compliance framing — accept and adopt. Proposal 2's bounded DLQ (R2) is the same control as my S1 viewed from a different lens — combine; do not implement twice. Per-merchant queue isolation (Proposal 2 R1) is reliability-first but ALSO improves blast radius for any future single-merchant compromise. Accept on both grounds.

## Confidence

High on the compliance findings (the unbounded DLQ + over-counted "delivered" rate is a documented and provable gap, not a speculation). Medium-high on the merchant-side corroboration design (the ack-callback pattern works; enterprise merchants will pay for it; getting all merchants to adopt is multi-quarter). Lower on the threat-model of merchant-side fraud cooperation — that's an open inquiry, not a known finding.

## Cost

S1+S5 (DLQ controls): ~3 engineer-weeks. S2 (merchant corroboration): ~6 engineer-weeks for the platform side; merchant adoption is a customer-success project lasting 2 quarters. S3 (HMAC rotation): ~2 engineer-weeks platform + customer-comms cost. S4 (log redaction audit): ~1 engineer-week if no exposure found; multi-week incident response if exposure found.

This proposal's recommendations are non-negotiable for PCI/SOC2 renewal; cost is the cost of staying in business.
