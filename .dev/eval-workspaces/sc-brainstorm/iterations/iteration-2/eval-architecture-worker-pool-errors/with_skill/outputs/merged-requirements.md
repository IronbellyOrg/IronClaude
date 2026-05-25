---
spec_type: requirements
domain: architecture
strategy: enterprise
adversarial_status: pass
convergence_score: 0.71
proposal_count: 5
source_proposals: [proposal-1-architect, proposal-2-devops, proposal-3-qa, proposal-4-security, proposal-5-performance]
debate_transcript: ./adversarial/debate-transcript.md
source_seed: ./seed-brief.md
agents: "opus:architect:'long-term system fit and extensibility',sonnet:devops:'rollout sequencing and operational surface',haiku:qa:'failure-mode coverage and gate enforcement',sonnet:security:'data exposure and replay safety',sonnet:performance:'latency budget and throughput'"
---

# Merged Requirements: Unified Worker-Pool Error Handling

## Problem Statement

The platform's 12 worker fleets handle errors inconsistently — some retry indefinitely (causing SMTP-credit burn and pod thrash), some swallow errors silently (causing missed customer webhooks), and only 2 have any DLQ (with incompatible schemas). Three Q1 incidents traced directly to this inconsistency; Q1 cloud spend included ~$40k of runaway-retry cost. Redesign as a unified `internal/workers/errors/` subsystem — typed taxonomy (Retryable/NonRetryable/Poison), per-fleet DLQ on a shared schema, shared CLI replay plane, chaos harness, per-fleet error-rate SLOs — and migrate all 12 fleets in ≤2-week chunks ordered by Q1-incident pain. Feature-flagged rollback per fleet, no message loss for billing-critical fleets, ≤5% per-message latency overhead enforced by CI benchmark, ≥4× reduction in retry-induced cost by end of Q3.

## Constraints

- **C1** — No message loss for billing-critical fleets (`billing-batch-workers`, `webhook-delivery-workers`). Absolute. *(seed Q5)*
- **C2** — Queue-schema backward-compat: in-flight messages keep flowing during migration; no schema rewrites. *(seed Q5)*
- **C3** — Per-fleet migration chunks ≤2 weeks. *(seed Q5)*
- **C4** — Hot-path latency overhead ≤ 100µs p99 (which lands under the 5% per-message budget on a 10ms baseline). Enforced by per-PR CI benchmark. *(seed Q5; debate Tension 5; Performance NFR-perf-1)*
- **C5** — Coexists with refactored `internal/workers/base/retry.py` — 4 existing callers preserved, no breaking change. *(enrichment, codebase)*
- **C6** — Old DLQs (`ingest-workers/dlq.py`, `webhook-delivery-workers/failed_queue.py`) are **drained** through the new client; not deleted while messages live in them. *(seed Q6, Q10)*
- **C7** — All DLQ access is per-fleet IAM (`dlq:read:<fleet>`, `dlq:replay:<fleet>`); no engineer-wide default. *(debate Tension 4; Security)*

## Functional Requirements

- **FR1** — Build `internal/workers/errors/` subsystem with the typed-error taxonomy (`RetryableError`, `NonRetryableError`, `PoisonError`) supporting Stripe-style attempt-bounded retryability (`RetryableError(promote_after_attempts=N)`). *(architect §taxonomy; QA test class 6; research-deep §1)*
- **FR2** — `DLQClient` interface with two implementations: `KafkaDLQ` (matches `ingest-workers` shape) and `PostgresDLQ` (matches `webhook-delivery-workers` shape). Both write a **shared envelope schema** `{message_id, original_payload, error_class, error_context, attempts, ts, fleet, redacted_fields[]}`. *(architect §dlq; research-deep §2 per-fleet-DLQ-shared-schema pattern)*
- **FR3** — Shared CLI replay plane (`python -m workers.errors.replay --fleet=<F> --filter=<expr> --justification=<text>`). DLQ-shape-agnostic; rate-limited to 100 msg/sec default; requires `--rate=<N>` and an explicit override flag for higher rates. Sandbox mode (`--target=staging`) available for billing-critical fleets when batch > 100 messages. *(architect §replay; DevOps §replay-rate-limit; Security §replay-safety)*
- **FR4** — Audit log writes to existing `internal/audit/event_log.py` on every DLQ write, read, and replay with: `actor`, `action`, `fleet`, `message_id`, `justification` (required for human replays), `result`. Batched 1000-entries-or-1-second; sync mode available. *(Security §audit; Performance NFR-perf-3)*
- **FR5** — PII redaction at DLQ-write time: producer schemas tag fields `pii=true`; redaction field-set pre-computed at deploy time (not per message); tagged fields are hashed or redacted before persistence. Token-header stripping (`Authorization`, `X-Api-Key`) on webhook payloads. *(Security §data-handling; Performance §where-I-push-back)*
- **FR6** — Chaos harness ships with MVP (`internal/workers/errors/chaos.py`). 10 test classes (8 from QA + 1 PII-redaction from Security + 1 latency-regression from Performance). Each fleet's migration PR must demonstrate all 10 against its own handler. *(QA §test-taxonomy; Security §PII test; Performance §latency-regression test; debate Tension 3)*
- **FR7** — Per-fleet feature flag in `config/flags.yaml` to fall back to pre-redesign behavior. Old per-fleet error code marked deprecated in migration PR; removed in a follow-up PR ≥2 weeks after canary proves out. *(seed Q10; architect §migration-shape)*
- **FR8** — Per-fleet observability dashboard panel: `error_class_total{fleet, error_class, outcome}` Prometheus counter with **bounded label cardinality** (no per-message labels); single "all fleets at a glance" view aggregating across the 12. *(architect §observability; Performance §metrics-cardinality)*
- **FR9** — Migration order: Q1-incident fleets first (`email-dispatch`, `image-processing`, `webhook-delivery`), then billing-critical (`billing-batch`, `ingest-workers`), then the 7 small fleets (code-mod-assisted, batched 2-3 per PR). `email-dispatch` runs in **shadow mode** for ≥1 week before enforcement (highest-volume fleet, latency-regression risk). *(DevOps §migration-order; Performance pushback on volume)*
- **FR10** — Synchronous `image-processing → thumbnail-workers` call is refactored to async (queue-based) as part of the `image-processing` migration. ~1 sprint added to that fleet's chunk. *(debate Tension 7)*

## Non-Functional Requirements

- **NFR1** — Hot-path overhead ≤ 100µs p99 measured on a representative production handler per fleet; enforced by per-PR benchmark gate. *(C4; Performance NFR-perf-1)*
- **NFR2** — DLQ write latency does not block worker liveness — async writes with a bounded queue; full-queue policy is per-fleet (block-and-page, local-spool-with-bound, or drop-with-audit). *(Performance NFR-perf-2)*
- **NFR3** — Retry-induced cost reduced ≥4× by end of Q3 vs Q1 baseline (~$40k → ≤$10k). Subsystem operational cost (DLQ storage + audit + metrics) ≤ 20% of Q1 retry baseline (≤$8k/quarter). *(seed success criteria; Performance NFR-perf-5; DevOps cost section)*
- **NFR4** — Aggregate worker throughput post-migration ≥ 13M messages/hour (current baseline ~15M/hr, ≤15% degradation absolute). *(Performance §throughput-floor)*
- **NFR5** — Zero billing-critical-fleet message loss across the migration window (verified via idempotency-key replay-counts matching production counts). *(C1; QA AC-Q5)*
- **NFR6** — DLQ retention: per-fleet, default 30 days, hard cap; auto-delete with audit past retention. Retention is enforced as a security control. *(Security §data-handling)*

## Acceptance Criteria

- **AC1** — All 10 chaos tests green for every fleet's specific handler before that fleet's migration is declared done. Test artifacts recorded in CI. *(FR6; QA AC-Q1)*
- **AC2** — Per-fleet error-rate SLO defined and alerting: numerator `RetryableError-promoted-to-NonRetryable`, denominator total messages, budget varies per fleet (0% billing-critical, 0.1% customer-facing, 1% best-effort). *(QA AC-Q2)*
- **AC3** — Per-fleet runbook at `docs/runbooks/workers/<fleet>.md` covering DLQ diagnosis, DLQ-unavailable failover, and replay procedure. *(QA AC-Q3; DevOps §operational-surfaces)*
- **AC4** — Per-fleet canary soak ≥2 weeks at 5% traffic with the new code path enabled; zero billing-critical-fleet message loss verified. *(NFR5; QA AC-Q5)*
- **AC5** — Per-PR latency benchmark green: hot-path overhead ≤ 100µs p99 vs baseline; PR blocked if budget breached. *(NFR1; Performance §where-I-push-back-on-QA)*
- **AC6** — Cost dashboard shows retry-induced spend reduction trend; end-of-Q3 cumulative reduction ≥ 4× from Q1 baseline. *(NFR3)*
- **AC7** — Quarterly chaos test (post-migration) executes the full 10-test suite against every fleet; failure = SEV-3 ticket and remediation in the following sprint. *(seed success criteria; FR6)*
- **AC8** — Quarterly DLQ-access review: every `dlq:read:*` and `dlq:replay:*` grant re-attested by fleet owner; revocations audited. *(C7; Security §audit)*

## Risks

- **R1** (severity: HIGH) — **Misclassified "retryable" error.** A schema-validation bug raised as `RetryableError` gets infinite-retry-equivalent treatment — same Q1 failure mode, new mechanism. *Mitigation*: chaos test class 2 (deterministic-error fail-fast) is the canonical detection; per-fleet error-rate SLO (AC2) alerts on promotion-rate spikes; mandatory PR template includes "what error classes can this handler raise" checklist. *(seed Q11a)*
- **R2** (severity: HIGH) — **DLQ unavailability cascade** (Cloudflare-2023 pattern). If a fleet's DLQ goes down and the fleet doesn't have an explicit fallback policy, behavior is undefined. *Mitigation*: NFR2 requires per-fleet full-queue policy; chaos test class 5 verifies the documented behavior actually happens; quarterly review of policies. *(seed Q11b; research-deep §2)*
- **R3** (severity: HIGH) — **Latency regression silently disabling subsystem.** Fleets that can't tolerate overhead disable the subsystem via feature flag, undoing the work. *Mitigation*: per-PR benchmark gate (AC5); subsystem disablement requires an SEV-3 with ≥1-week documented investigation; promotion-to-fix tracked. *(Performance §what-I-push-back-on-hardest)*
- **R4** (severity: MEDIUM) — **PII leak via failed-message audit.** A producer fails to tag a PII field, message lands in DLQ with raw PII, audit log replicates it. *Mitigation*: pre-deploy schema check (CI gate) verifies every producer's PII-tagging coverage against an inventory; retention cap (NFR6) bounds blast radius. *(Security §threat-model)*
- **R5** (severity: MEDIUM) — **Synchronous-call refactor in `image-processing` causes regressions.** Moving the `→ thumbnail-workers` call to async changes ordering semantics. *Mitigation*: shadow-mode comparison run for 1 week (same as `email-dispatch`); explicit ordering-test in chaos suite for this fleet. *(FR10; debate Tension 7)*
- **R6** (severity: LOW) — **Replay-throttle bypass for "emergency" recovery.** The 100 msg/sec default has an SRE-override path; over time this becomes the default and loses its safety value. *Mitigation*: override usage logged + reviewed monthly; override > 1000 msg/sec requires manager approval. *(Security §replay-safety; DevOps §rate-limit)*
- **R7** (severity: LOW) — **Web UI scope creep.** The deferred web UI gets pulled into this work mid-stream. *Mitigation*: explicit out-of-scope; UI is a separate project; this spec ensures CLI + audit log are built so a future UI lands without backfilling. *(debate remaining-disagreements)*

## Open Questions

- **OQ1** — Per-message-type override policy: hard cap (≤3 overrides per fleet) or library-enforced taxonomy + advisory linting? Debate Tension 7 reserves this as carried-forward. *(seed Q3 open-question)*
- **OQ2** — Web UI for self-service replay: in what quarter does it ship? Out of scope here; flagged for Q4/Q1-next-year prioritization. *(debate remaining-disagreements)*
- **OQ3** — Cross-fleet error correlation view (single error-graph spanning fleets) vs per-fleet only. Deferred until ≥6 fleets are migrated and the data shape is clearer. *(seed open question Q4)*

## Out of Scope (explicit)

- Web UI for DLQ replay (CLI-only in this spec; future project).
- Full Temporal migration (taxonomy borrows from Temporal; runtime does not).
- Per-message custom retry policies (only per-fleet defaults + per-error-class overrides).
- Cross-region DLQ replication (single-region; multi-region is a future architectural decision).

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (typed taxonomy) | Architect §taxonomy; QA test class 6; research-deep §1 |
| FR2 (per-fleet DLQ + shared schema) | Architect §dlq; research-deep §2 |
| FR3 (CLI replay + rate-limit + sandbox) | Architect §replay; DevOps + Security |
| FR4 (audit log with required fields) | Security §audit; debate Tension 4 |
| FR5 (PII redaction at write time) | Security §data-handling; Performance impl pushback |
| FR6 (chaos harness at MVP, 10 tests) | QA + Security + Performance; debate Tension 3 |
| FR7 (per-fleet feature flag) | Seed Q10; architect §migration-shape |
| FR8 (bounded-cardinality metrics) | Architect §observability; Performance §metrics |
| FR9 (incident-first migration order + shadow mode) | DevOps; Performance pushback on volume |
| FR10 (image-processing sync→async refactor) | Debate Tension 7 |
| NFR1 (100µs hot-path budget) | Performance NFR-perf-1; debate Tension 5 |
| NFR2 (async DLQ writes) | Performance NFR-perf-2 |
| NFR3 (≥4× retry-cost reduction; ≤20% subsystem cost) | Seed success criteria; Performance + DevOps cost |
| NFR4 (throughput floor) | Performance §throughput-floor |
| NFR5 (zero billing-critical message loss) | C1; QA AC-Q5 |
| NFR6 (retention cap as security control) | Security §data-handling |
| AC1-AC4, AC7 (chaos + SLO + runbook + soak + quarterly) | QA + architect |
| AC5 (per-PR latency gate) | Performance; debate Tension 5 |
| AC6 (cost dashboard) | DevOps; NFR3 verification |
| AC8 (quarterly access review) | Security §audit |
| R1-R5 (high/medium risks) | Seed Q11 + each persona's failure-mode analysis |
| R6 (replay-throttle bypass) | Security + DevOps interaction |
| R7 (UI scope creep) | Debate remaining-disagreements |
| OQ1-OQ3 | Seed brief + debate carry-forwards |
| Out-of-scope items | Debate remaining-disagreements; seed brief Q5 |
