---
spec_type: research-evaluation
domain: research
strategy: systematic
adversarial_status: pass
convergence_score: 0.72
proposal_count: 3
source_proposals: [proposal-1-architect, proposal-2-analyzer, proposal-3-scribe]
source_seed: ../seed-brief.md
debate_transcript: ./adversarial/debate-transcript.md
agents: "opus:architect:'prioritize platform fit, long-term maintainability, and runtime governance',sonnet:analyzer:'focus on benchmarks, evidence quality, and risk decomposition',haiku:scribe:'focus on policy clarity, decision documentation, and stakeholder framing'"
---

# Merged Requirements: Bun vs Node Evaluation for New Backend Services

## Problem Statement

The platform team must produce a defensible Q2 2026 decision on whether to allow Bun for new backend services, starting with a planned real-time WebSocket gateway. The decision is **selective adoption, not migration** — the existing 40-service Node 20 LTS fleet is out of scope. Bun must demonstrate **substantially better behavior on at least one workload axis we care about (WebSocket fanout, HTTP throughput, or DX) AND no worse operational stability** to clear the bar. A 10% edge is insufficient; a 2x edge with stable ops is sufficient. The forcing function is the WebSocket gateway team's runtime decision in ~6 weeks; absent a policy, they default to Node, which is acceptable but leaves the question unresolved.

## Functional Requirements

- **FR1** — Produce a written **Runtime Allowlist Policy** documenting Bun's status (one of: `allow`, `pilot-only-with-conditions`, `disallow`) for new backend services, the conditions for that status, and the review cadence to revisit it. *(seed brief Q1, success criteria; debate Tension 1 consensus)*
- **FR2** — Conduct a **bounded pilot** on the planned WebSocket gateway (or equivalent representative workload if the gateway slips) with explicit entry criteria, exit criteria, and a documented revert procedure (≤1 sprint estimated revert time). *(debate Tension 2; analyzer proposal §pilot scope)*
- **FR3** — Produce a **native-dependency compatibility matrix** covering the three load-bearing native deps (`bcrypt`, `node-rdkafka`, `sharp`) and any others surfaced during pilot scoping. Status per dep: `works`, `works-with-shim`, `blocked`. *(seed brief Q7; analyzer proposal §native-dep risk)*
- **FR4** — Produce a **workload-axis comparison report** with evidence (quantitative where available, evidence-based where not) for: WebSocket fanout at 10k+ connections, HTTP throughput on a representative middleware stack, DX (build time, test time, devloop friction). *(seed brief Q3, success criteria)*
- **FR5** — Produce an **observability parity statement** for our specific stack (OpenTelemetry SDK + Datadog APM + pino → Vector → Loki) covering: which auto-instrumentations work, which require a shim, which are blocked. *(seed brief Q6; debate Tension 3 / scribe failure mode 2)*
- **FR6** — Produce a **revert playbook** for any pilot service: trigger conditions, decision authority, step-by-step revert procedure, validation checklist. *(seed brief Q5, Q9; debate Tension 2 consensus)*
- **FR7** — Establish a **Bun version governance policy**: who owns version bumps, cadence, criteria for adopting a new Bun release on production services. Parity with how we govern Node LTS today. *(seed brief OQ "long-term governance"; architect proposal §governance)*

## Non-Functional Requirements

- **NFR1** — Decision defensibility: the policy must be reviewable by engineering leadership against the cited evidence in <30 minutes. Numbers, not vibes. *(seed brief Q10; scribe proposal §stakeholder framing)*
- **NFR2** — Pilot blast radius: at most one production service in pilot at a time. Pilot service must be on the customer-traffic critical path only if a revert path is rehearsed end-to-end first. *(debate Tension 2 / analyzer position)*
- **NFR3** — Compatibility floor: any allowed Bun version must pass the load-bearing-native-dep matrix at `works` or `works-with-shim` for `bcrypt` and `sharp`; `node-rdkafka` may be `blocked` if the policy excludes Kafka-producer services from the allowlist. *(analyzer proposal §native-dep risk)*
- **NFR4** — Reversion SLO: end-to-end revert from Bun back to Node for a pilot service must complete in ≤1 sprint elapsed time, with at most 30 minutes of customer-visible degradation during the cutover. *(seed brief Q5; debate Tension 2)*
- **NFR5** — Observability parity bound: any auto-instrumentation gap must have either a shim within 1 sprint of pilot start, OR a documented manual instrumentation pattern, OR be a policy-level blocker. No silent gaps. *(scribe proposal failure mode 2)*

## Acceptance Criteria

- **AC1** — Runtime Allowlist Policy document published to `docs/platform/runtime-allowlist.md` (or equivalent), reviewed by engineering leadership, version-stamped, with explicit `next_review_date` ≤ 2 quarters out. *(FR1; scribe proposal §deliverable)*
- **AC2** — Workload-axis comparison report includes: (a) ≥3 published benchmarks from independent sources with version + date + workload shape per data point; (b) ≥1 internal benchmark run on a representative workload using our deploy pipeline. Each claim cites a source. *(FR4; analyzer proposal §evidence quality)*
- **AC3** — Native-dep compatibility matrix populated for `bcrypt`, `sharp`, `node-rdkafka`, plus any deps surfaced in the pilot scoping pass. Each row carries a date of last verification and a Bun version. *(FR3)*
- **AC4** — Observability parity statement enumerates the OpenTelemetry instrumentations we actually use today (auto-discoverable from `package.json` + dd-trace config) and assigns each a status: `works`, `works-with-shim`, `blocked`. Shims, if any, are linked. *(FR5)*
- **AC5** — Revert playbook is rehearsed in pre-prod **before** any pilot service touches customer traffic. Rehearsal artifact (timed runbook execution log) is attached to the pilot proposal. *(FR6; NFR4)*
- **AC6** — Bun version governance policy: an entry in `docs/platform/version-policy.md` (or equivalent) naming the owner, the cadence, and the criteria for bumps. Parallels the Node LTS section. *(FR7)*

## Risks

- **R1** (severity: HIGH) — **Runtime instability in production.** Bun is younger than Node; a runtime bug at peak load could cause an incident with no quick upstream fix. *Mitigation*: pilot only on a service with a rehearsed revert; observability must surface anomalies before customer impact; require the revert playbook before pilot traffic; cap pilot blast radius at one service.
- **R2** (severity: HIGH) — **Observability gap that hides degradation.** If OpenTelemetry/dd-trace doesn't fully attach to Bun, we may be flying with partial telemetry on the most experimental service in the fleet. *Mitigation*: NFR5 — no silent gaps; require shim or manual instrumentation before traffic; pilot service runs in shadow-mode visibility for first 72 hours.
- **R3** (severity: MEDIUM) — **Native-dep regression after Bun version bump.** Bun's NAPI compatibility has improved but historically had regressions across versions. *Mitigation*: native-dep matrix re-verified on every Bun version bump; pilot service version-pinned; FR7 governance owns the bump cadence.
- **R4** (severity: MEDIUM) — **Single-vendor runtime risk.** Bun is owned by Oven (single-vendor, VC-backed). If Oven pivots or shuts down, we lose upstream support — Node has a foundation. *Mitigation*: discipline of Bun-specific API usage (lint rule); revert playbook makes Bun-to-Node mechanical; document the failover scenario in the governance doc.
- **R5** (severity: LOW) — **Hiring/onboarding friction.** New hires may need a short ramp. *Mitigation*: we hire JS/TS, not "Node engineers"; ramp is days, not weeks; documented in onboarding.

## Open Questions

- **OQ1** — Should the WebSocket gateway *be* the pilot, or should we pick a lower-blast-radius greenfield service first? Analyzer favors lower-blast-radius first; architect argues the WebSocket workload is exactly where Bun's claim is strongest, so testing it on a lower-stakes service doesn't answer the question. **Decision pending leadership review.**
- **OQ2** — `node-rdkafka` status as of pilot start date. If `blocked`, do we exclude Kafka-producer services from the Bun allowlist entirely, or is there an acceptable alternative (KafkaJS in pure-JS mode with documented perf delta)?
- **OQ3** — What's the trigger for *removing* Bun from the allowlist if pilot fails? Define a concrete failure surface (e.g., one SEV-2 attributable to Bun runtime), not "we'll know it when we see it".
- **OQ4** — Worker-thread parity for the two internal libraries that use it — fully measured during pilot scoping, or deferred to pilot execution?

## Out of Scope (explicit)

- Migrating any of the existing 40 Node services.
- Deno evaluation (different decision frame, different runtime).
- Build-tooling-only Bun adoption (e.g., `bun install` as a faster `npm install` without `bun run` at runtime) — this is a separate, lower-risk decision and can be made independently.
- Lambda/serverless runtime choice — we don't run Lambda for these workloads.

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (allowlist policy) | Seed brief Q1, Q10; scribe proposal §deliverable; ratified by all 3 proposals |
| FR2 (bounded pilot) | Seed brief Q2; analyzer proposal §pilot scope; debate Tension 2 |
| FR3 (native-dep matrix) | Seed brief Q7; analyzer proposal §native-dep risk; enrichment |
| FR4 (workload-axis report) | Seed brief Q3, Q4, success criteria; analyzer proposal §evidence quality |
| FR5 (observability parity) | Seed brief Q6; scribe proposal failure mode 2 |
| FR6 (revert playbook) | Seed brief Q5, Q9; debate Tension 2 consensus |
| FR7 (version governance) | Seed brief OQ; architect proposal §governance |
| NFR1 (defensibility) | Seed brief Q10; scribe proposal §stakeholder framing |
| NFR2 (blast radius) | Analyzer proposal §pilot scope; debate Tension 2 |
| NFR3 (compatibility floor) | Analyzer proposal §native-dep risk |
| NFR4 (reversion SLO) | Seed brief Q5; debate Tension 2 |
| NFR5 (no silent gaps) | Scribe proposal failure mode 2 |
| AC1-AC6 | Aggregated from all three proposals; final wording per scribe; quantitative thresholds per analyzer |
| R1 (runtime instability) | All three proposals identified independently |
| R2 (observability gap) | Scribe proposal §trust; analyzer proposal §evidence |
| R3 (native-dep regression) | Enrichment finding (node-rdkafka segfault history); analyzer proposal |
| R4 (single-vendor) | Architect proposal §governance; scribe proposal §risk-framing |
| OQ1 (pilot target) | Debate Tension 1 — unresolved, deferred to leadership |
| OQ2 (rdkafka decision) | Enrichment finding; analyzer proposal |
| OQ3 (removal trigger) | Architect proposal §governance |
| OQ4 (worker-thread) | Seed brief Q8; carried forward |
