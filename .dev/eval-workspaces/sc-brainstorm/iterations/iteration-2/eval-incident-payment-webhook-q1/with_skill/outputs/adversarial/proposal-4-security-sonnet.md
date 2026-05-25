---
proposal_id: 4
persona: security
model: sonnet
lens: PCI-DSS, defense-in-depth, conservative blast-radius bias
---

# Proposal 4 — Security (sonnet): Conservative Variant — Compliance Posture Plus Per-Merchant Trust Tiering

## Position

I agree with Proposal 3's central finding (PCI evidence gap is the biggest single risk on the table) but disagree on the *scope* of the recommended fix. Proposal 3 proposes a chain-of-custody DLQ + merchant-side corroboration as if all merchants can be brought along on the same timeline. In practice, they cannot. We need a **trust-tiered** posture: enterprise merchants (where compliance evidence is contractually meaningful) get the full chain; long-tail merchants get a documented best-effort posture that we DO NOT misrepresent to auditors. The single-tier "all merchants on the chain" plan will spend a year shipping nothing useful.

## Required investigation steps

Same as Proposal 3, plus:

5. **Stratify merchants by contractual evidence requirements.** Three buckets: Tier-1 (enterprise, contractual SLO, contractual audit clause) — full chain. Tier-2 (paid, no special clause) — documented best-effort. Tier-3 (free / trial) — best-effort, no compliance claim. The proportion in each bucket determines whether the Proposal 3 plan is achievable in one year or in three.
6. **Inventory existing audit responses** — what have we actually told PCI / SOC2 auditors about the evidence chain in the last two cycles? Is there written attestation that is now known to be inaccurate? **This determines remediation urgency and any disclosure obligation.**

## Required remediations (delta vs Proposal 3)

- **S1' — Tiered chain-of-custody DLQ.** Tier-1 merchants get cryptographic chain (Proposal 3's S1). Tier-2 and Tier-3 get bounded-DLQ with audit-log entries but not signed entries. Documented in compliance attestation as "tiered evidence; cryptographic chain for contractual customers".
- **S2' — Merchant-ack callback for Tier-1 only at launch.** Tier-2 opt-in if they ask. Tier-3 not offered. Do not block on the long tail.
- **S3** (HMAC rotation) — agreed with Proposal 3, no change.
- **S4** (log redaction) — agreed with Proposal 3, with one addition: a **historical log scan** for HMAC key strings before any rotation announcement. Rotate-and-then-discover is worse than discover-and-then-rotate.
- **S5** (DLQ access logging) — agreed, with one addition: **per-merchant break-glass procedure**. Any DLQ access for a merchant in dispute requires a justification field referencing a ticket; auto-emails the merchant's account manager.
- **S6 (new)** — **Disclosure-readiness check on the audit attestation history.** If we have told auditors something the evidence chain cannot back up, legal must be looped in **before** the remediation lands (otherwise remediation looks like coverup). Engineering does not own this decision but must surface it.

## What I'd push back on

Proposal 3's "do not continue claiming what we cannot prove" is correct as a principle and wrong as a one-step remediation. The right shape is: **document the gap to auditors now**, ship the tiered fix over 2-4 quarters, narrow the attestation language in the next audit cycle to match what we actually do. Going to auditors with "we found a gap, here's the remediation timeline" is a normal control finding; going to them next cycle with the gap still unannounced is a material misstatement.

## What I'd concede

Everything substantive in Proposal 3 stands. My contribution is on **sequencing and tiering**, not on whether the controls are right. Proposal 3 read as a single-tier all-merchants plan would block ship on cross-customer coordination that nobody owns; tiered, the same control set ships.

## Confidence

High on the tiering necessity (this is how every PCI-scope payments platform actually operates; single-tier "all merchants" is a strawman). Medium-high on the disclosure-readiness framing — that's a lawyer's call from this point.

## Cost

Tier-1 scope: similar to Proposal 3's S1+S5 (~3 engineer-weeks). Tier-2 / Tier-3 scope: ~2 engineer-weeks for bounded-DLQ-without-chain. Disclosure-readiness check: legal + 1 engineer-week. Total platform engineering: ~6 engineer-weeks. Cross-functional cost (legal, customer-success): non-trivial; non-negotiable for renewal.
