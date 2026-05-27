---
schema_version: "1.0"
source_seed_brief_path: ".dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-worker-pool-errors/seed-brief.md"
domain: architecture
strategy: enterprise
adversarial_status: pass
convergence_score: 0.72
fit_to_intent: pass
unresolved_conflicts:
  - "Durable persistence backend for failure envelopes deferred to /sc:design — both relational and append-only log-store options remain viable depending on incident-replay volume."
spec_type: requirements
proposal_count: 5
source_proposals: [proposal-1-architect, proposal-2-devops, proposal-3-qa, proposal-4-security, proposal-5-performance]
debate_transcript: ./adversarial/debate-transcript.md
agents: "opus:architect:'long-term system fit and extensibility',sonnet:devops:'rollout sequencing and operational surface',haiku:qa:'failure-mode coverage and gate enforcement',sonnet:security:'data exposure and replay safety',sonnet:performance:'latency budget and throughput'"
---

# Merged Requirements: Worker-Pool Error Handling Redesign

## Problem Statement

Worker-pool failure behavior is inconsistent across execution paths in this codebase. ParallelExecutor collapses task failures to ambiguous `None` results; remediate_executor implements rich snapshot + rollback semantics; batch_retry persists an attempt ledger; prd/process distinguishes transient vs non-transient launch failures; and pipeline/trailing_gate models its own retry state machine. Downstream consumers (CLI workflows, pipeline gates, evaluators, self-correction) cannot reliably distinguish success, failure, cancellation, partial success, or poison inputs across these executors. The redesign defines requirements for a unified worker-pool error-handling contract that preserves throughput, makes each work item's terminal state explicit, supports bounded retries with idempotency-aware replay, scopes rollback policy, enforces redaction, and enables per-executor incremental migration without a flag day.

## Functional Requirements

- **FR1 — Stable error envelope** — Define a stable worker error envelope for every failed, cancelled, quarantined, skipped, or unknown work item. Required envelope fields: work item id, worker/pool id, task id (where available), terminal status, error class, cause summary, cause chain, attempt count, retry policy applied, idempotency key (where computable), replay eligibility flag, redaction marker, timestamps (started, last_attempt, terminal), and rollback decision (where applicable). Envelope is the contract — raw exceptions are never the contract.

- **FR2 — Typed error taxonomy** — Define a typed error taxonomy with at least: `retryable_transient` (dependency timeout, rate limit, network blip, temporary resource exhaustion), `non_retryable_deterministic` (invalid input, invariant violation, authorization failure, missing required state), `poison_unclassifiable` (inputs that repeatedly crash classification/deserialization), `cancellation` (shutdown, operator action, budget exhaustion), `timeout` (per-task deadline exceeded), `rollback_failed` (rollback hook itself raised), and `unknown` (worker disappeared / status unrecoverable). Retryable errors MUST be promoted to terminal failure or quarantine after policy exhaustion — never retried indefinitely.

- **FR3 — Mixed-outcome preservation** — Every pool execution result MUST preserve per-task outcomes. A pool-level failure MUST NOT erase successful, failed, cancelled, quarantined, or unknown tasks from the returned contract. The pool result reports counts and per-item envelopes for each terminal state separately.

- **FR4 — Compatibility adapters** — Provide compatibility adapters for existing result shapes during migration. Specifically: ParallelExecutor's `None`-on-failure pattern, remediate_executor's snapshot/rollback signaling, batch_retry's terminal-status field, process.py's transient/non-transient flag, and trailing_gate's retry state enum MUST each have a documented adapter that emits BOTH the legacy status AND the new envelope during the compatibility window.

- **FR5 — Bounded retry policy** — Define retry policy requirements: max_attempts (typed per error class), backoff strategy, jitter, retry budget (per-pool and per-error-class), idempotency check (or explicit "non-idempotent — no auto-retry" marker), and promotion rule on exhaustion (failed vs quarantined). Retry policy is configurable per executor; defaults are documented.

- **FR6 — Quarantine / dead-letter behavior** — Define quarantine behavior for poison inputs and exhausted retryables. Quarantined items MUST preserve diagnostic metadata (envelope + classification trail) without exposing sensitive raw payloads by default. Quarantine entries are reviewable, replayable (subject to FR7), and have an explicit retention/cleanup policy.

- **FR7 — Safe replay controls** — Define replay requirements: replay MUST be rate-limited (per-operator and per-pool), auditable (justification logged, audit envelope created linking original failure to replay attempt), idempotency-aware (auto-replay blocked for non-idempotent work unless policy explicitly permits with required approval), dry-run capable (validates envelope + policy + authz without executing), and approval-gated for non-idempotent / cross-system-side-effect work.

- **FR8 — Explicit rollback scoping** — Define rollback semantics as explicit pool policy. Three supported modes: `partial_success_preservation` (failed items rolled back individually, successes preserved), `per_item_rollback` (each failed item's side effects undone independently), or `atomic_group_rollback` (configured group succeeds or rolls back as a unit). The chosen policy MUST be visible in the pool result and in each work item's envelope. `rollback_failed` is a distinct terminal state (per FR2).

- **FR9 — Observability requirements** — Define metrics and log requirements: terminal-state distribution (counts per status), error-class breakdown, retry-storm detection (retry rate over time per pool), quarantine growth rate, replay outcomes (success/failure/denied), cancellation count, timeout count, rollback success/failure counts, and unknown-status incidence. Metrics MUST support per-worker, per-pool, per-executor, and per-error-class dimensions.

- **FR10 — Operator-facing diagnostics** — Define diagnostics sufficient for an operator to answer: which items failed, why (error class + cause summary), whether they can be retried (replay eligibility), what recovery action was taken (rollback decision, quarantine status), and what the audit trail shows for any manual intervention. CLI output formats expose this without requiring backend access.

- **FR11 — Redaction requirements** — Define redaction for persisted or displayed error context. Sensitive payloads, credentials, tokens, secret-bearing stack frames, and PII MUST be redacted before persistence or display by default. Redaction markers in the envelope indicate what was elided. Operator override (with audit + authz) permits unredacted view in incident-response workflows.

- **FR12 — Per-executor migration** — Define migration requirements per executor / call site: feature-flagged enablement, rollback criteria, compatibility window, removal deadline for legacy status behavior, and named owner accountable for cutover. Migration order is documented (recommended: trailing_gate → batch_retry → process → remediate_executor → parallel.py, ordered by existing-failure-richness ascending so the lowest-information executor lands the contract last).

- **FR13 — Shutdown contract** — Define worker-pool shutdown behavior: in-flight tasks receive cancellation context (cooperative cancellation token), queued work remains durable or resumable, and the final pool contract reports completed / failed / cancelled / unknown counts as separate fields. No collapsing.

## Non-Functional Requirements

- **NFR1 — Success-path overhead bounded** — Classification and status recording on the success path MUST have bounded, measurable overhead. Rich envelope serialization occurs primarily on the failure path. Target: success-path overhead is a configurable budget per executor class; default budget MUST be specified in design phase.

- **NFR2 — Failure-path backpressure** — Failure-path persistence MUST support batching and backpressure so error storms do not amplify incidents. A failure-store outage MUST trigger a degraded mode (envelope retained in memory or local spool) — not pool failure cascade.

- **NFR3 — Bounded retry behavior** — Retry behavior MUST be bounded to prevent infinite retry loops and dependency saturation. Retry budgets are enforced at pool and error-class scope.

- **NFR4 — Durable envelope + audit** — Error envelopes and replay audit records MUST be durable enough for incident review (review window: at least one incident response cycle) and downstream gating (CLI, pipeline gates, evaluators).

- **NFR5 — Stable downstream contract** — The envelope contract MUST be stable across versions for downstream CLI workflows, pipeline gates, remediation workflows, and evaluators. Breaking changes require a deprecation cycle.

- **NFR6 — Incremental adoption** — The design MUST allow incremental adoption per executor / call site without a repository-wide flag day. Compatibility shim coexists with new envelope during the migration window.

- **NFR7 — Security controls enforceable pre-rollout** — Security controls (redaction, replay authorization, audit completeness) MUST be enforceable and tested BEFORE broad rollout. Security review is a rollout gate.

- **NFR8 — Multi-dimensional metrics** — Metrics and logs MUST support per-worker, per-pool, per-executor, per-error-class, per-terminal-state, and per-retry-policy analysis. Dashboards (or equivalent telemetry surfaces) expose retry storms, quarantine growth, and replay outcomes in real time.

- **NFR9 — CI green during migration** — CI MUST remain green throughout the migration window. A migration PR is blocked if it would red the gate. (Mirrors the migration discipline that worked for the pytest→vitest case in this same codebase.)

## Acceptance Criteria

- **AC1 — Single terminal state** — Contract tests prove that every task reaches exactly one terminal state: `succeeded`, `failed`, `cancelled`, `quarantined`, `skipped`, or `unknown`. No task ends in two states; no task ends in zero states.

- **AC2 — Mixed batch fidelity** — A mixed batch with successes, failures, cancellations, and quarantines reports all item outcomes in separate per-item envelopes. The pool result is not collapsed to a single generic failure.

- **AC3 — Retryable promotion** — A retryable dependency failure retries with bounded backoff (per FR5) and is promoted to `failed` or `quarantined` after policy exhaustion. Promotion is deterministic and tested.

- **AC4 — Non-retryable not retried** — A non-retryable deterministic failure is not retried; it produces a failure envelope on first attempt.

- **AC5 — Poison quarantined** — A poison input is quarantined (not failed-and-replayed). Auto-replay is blocked. Manual replay requires approval (per FR7).

- **AC6 — Cancellation reported distinctly** — A cancellation or shutdown path reports `cancelled` (cooperatively cancelled), `in_flight_at_shutdown` (worker did not respond before shutdown deadline), and `unknown` (worker disappeared) distinctly. Per FR13.

- **AC7 — Replay gated** — Replay requires eligibility check (envelope flag), rate-limit check, operator justification (logged), and audit envelope creation. Tests cover each gate.

- **AC8 — Non-idempotent auto-replay blocked** — Non-idempotent work cannot be auto-replayed unless the configured policy explicitly permits it AND required approval controls are exercised.

- **AC9 — Redaction enforced** — Redaction tests prove sensitive fields (credentials, tokens, declared-PII fields, secret-bearing stack frames) are not persisted or displayed in default failure views. Operator override path requires authz + audit.

- **AC10 — Per-executor migration** — Migration can be enabled for one executor / call site (e.g., trailing_gate) while others continue using compatibility mode. CI stays green throughout (per NFR9).

- **AC11 — Observability dashboards** — Observability surfaces expose terminal-state distribution, retry-storm detection, quarantine growth, and replay outcomes. Per-pool and per-error-class drill-down works.

- **AC12 — Rollback policy visible** — Rollback policy (partial-success-preservation / per-item / atomic-group) is visible in the pool result and per-item envelopes. Each mode has contract tests.

- **AC13 — Compatibility shim** — Compatibility adapters for ParallelExecutor, remediate_executor, batch_retry, process.py, and trailing_gate each emit both legacy status AND new envelope during the compatibility window. Tests verify dual-emission.

- **AC14 — Failure-store outage degraded mode** — A simulated failure-store outage triggers degraded mode (envelope in-memory or local spool); the pool itself does not cascade-fail.

## Risks

- **R1 — Hot-path overhead** — Envelope serialization on every success could exceed NFR1's success-path budget. Mitigation: rich serialization is failure-path only; success path records minimal status field.

- **R2 — Replay tooling duplicates side effects** — Replay can duplicate side effects if idempotency check and approval gates are incomplete or misused. Mitigation: FR7 + AC8 + AC9; non-idempotent work blocked from auto-replay by default.

- **R3 — Permanent compatibility mode** — Compatibility window may become permanent unless removal criteria + migration deadlines are explicit and tracked. Mitigation: FR12 requires named owner and removal deadline; tracking surfaces in observability per FR9.

- **R4 — Over-broad rollback** — Pool-level rollback policy could discard valid partial successes or hide mixed-outcome batches. Mitigation: FR8 makes rollback scope explicit and visible; `partial_success_preservation` is a first-class mode.

- **R5 — Secrets in persisted context** — Persisted error context may expose secrets without strict redaction. Mitigation: FR11 + AC9 enforce default redaction with audit-gated override.

- **R6 — Failure-store outage cascade** — Failure-store outage could cause secondary incidents if envelope persistence is synchronous and unbuffered. Mitigation: NFR2 + AC14 require batching, backpressure, and degraded-mode handling.

- **R7 — Envelope schema drift** — Envelope contract drift could break downstream consumers (CLI, pipeline gates, evaluators). Mitigation: NFR5 requires stable contract with deprecation cycle for breaking changes.

- **R8 — Adoption velocity** — Per-executor migration may stall mid-way, leaving the codebase in a permanent dual-state. Mitigation: FR12 named owner + removal deadline + NFR9 CI-green gate + observability dashboards (FR9) make migration progress publicly visible.

- **R9 — Retry storms** — Retry policy misconfiguration could create retry storms that amplify a dependency outage. Mitigation: NFR3 bounded retries + retry-budget per pool + FR9 retry-storm detection.

## Open Questions

- **OQ1** — Which worker pools require atomic-group rollback versus partial-success preservation? Default mode selection requires per-executor review.
- **OQ2** — What durable persistence backend should hold failure envelopes and replay audit records? Options: relational store (audit-friendly, structured query), append-only log store (high-throughput, replay-friendly), or hybrid. Deferred to /sc:design; this is the listed `unresolved_conflicts` entry.
- **OQ3** — What is the allowed compatibility window for legacy result shapes? Recommended bound: one release cycle per executor; needs operator buy-in.
- **OQ4** — Which work types are idempotent enough for automatic replay, and which require manual approval? Requires per-executor task-type audit.
- **OQ5** — What success-path overhead budget should be enforced per executor class? NFR1 requires a number; design phase to set it.
- **OQ6** — Who owns replay authorization and incident runbook approval in operational deployments? Roles and escalation paths need to be defined before broad rollout per NFR7.
- **OQ7** — What is the migration owner / cutover schedule for each of the five existing executors (trailing_gate, batch_retry, process, remediate_executor, parallel.py)?

## Provenance

- **FR1 (stable envelope)** — Architect proposal (opus): supplied envelope field list, work-item-identity requirement, and "raw exception is not a contract" framing. Refined by Security (sonnet) to add `redaction_marker` field. Anchor honored: `failure causality cannot be lost` (seed-brief must_preserve).
- **FR2 (typed taxonomy)** — Architect proposal + research-deep enrichment Pattern 1. Refined by QA (haiku) to add `rollback_failed` and `unknown` as first-class terminal states (failure-mode coverage). Anchor honored: terminal-taxonomy seed-brief context_anchor.
- **FR3 (mixed-outcome preservation)** — Architect proposal §pool-result contract. Anchor honored: `partial success must remain representable` (seed-brief must_preserve).
- **FR4 (compatibility adapters)** — DevOps proposal (sonnet): per-executor adapter list. Specifically anchored to all five existing executors per seed-brief context_anchors.
- **FR5 (bounded retries)** — Architect + Performance (sonnet) merged: max_attempts, backoff/jitter, retry budget, idempotency check, promotion rule. Research Pattern 2.
- **FR6 (quarantine)** — Architect + Security merged: quarantine preserves diagnostics, retention policy, default-redacted payloads.
- **FR7 (safe replay)** — DevOps + Security merged: rate limits, audit envelope, idempotency-awareness, dry-run, approval-gating. Research Pattern 4. Anchor honored: `non-idempotent work must not be auto-replayed` (seed-brief must_preserve).
- **FR8 (rollback scoping)** — Architect proposal §rollback modes; QA contributed `rollback_failed` as distinct terminal (cross-ref FR2). Anchor honored: `scoped rollback over global` (seed-brief).
- **FR9 (observability)** — DevOps + Performance merged: per-worker/pool/executor/error-class metrics, retry-storm detection, quarantine growth. Research Pattern 5.
- **FR10 (operator diagnostics)** — DevOps proposal §operator-facing surface; CLI consumer requirement from seed-brief Q5.
- **FR11 (redaction)** — Security proposal §default-redaction; operator override path. Refined by QA (test coverage).
- **FR12 (per-executor migration)** — DevOps proposal §rollout sequencing. Migration order rationale (trailing_gate first, parallel.py last) added during merge based on codebase-context.md richness gradient.
- **FR13 (shutdown contract)** — Architect proposal §shutdown semantics; seed-brief Q8 verbatim.
- **NFR1 (success-path overhead)** — Performance proposal §hot-path budget; Architect concurrence.
- **NFR2 (backpressure)** — Performance proposal §failure-store backpressure; tied to AC14.
- **NFR3 (bounded retries)** — Performance proposal §retry-storm prevention; reinforces FR5.
- **NFR4 (durable envelope)** — DevOps proposal §incident-review durability; QA concurrence.
- **NFR5 (stable contract)** — Architect proposal §downstream contract stability; seed-brief Q5.
- **NFR6 (incremental adoption)** — DevOps proposal §no-flag-day. Anchor honored: incremental-migration seed-brief context_anchor.
- **NFR7 (security pre-rollout)** — Security proposal §security-review-as-rollout-gate.
- **NFR8 (multi-dimensional metrics)** — DevOps + Performance merged.
- **NFR9 (CI green)** — Cross-domain merge discipline imported from the pytest→vitest migration patterns in this same codebase; DevOps proposal §CI gate.
- **AC1–AC14** — Synthesis of QA proposal (failure-mode coverage and gate enforcement) + cross-variant test coverage. QA was the primary author of contract-gate framing.
- **R1–R9** — Union of all five proposals' risk sections, deduplicated and merged. R1, R6 from Performance; R2, R5, R9 from Security; R3, R4, R8 from DevOps; R7 from Architect.
- **OQ1–OQ7** — Carried from seed-brief.md `## Open Questions` plus three additional questions surfaced by adversarial debate (OQ2 unresolved-conflict, OQ6 ownership, OQ7 cutover schedule).

### Dropped Anchors

None. All seed-brief `must_preserve` items appear in the merged output:

- "Worker pool not replaced" → FR-series scope language + out_of_scope explicit
- "Existing executors continue functioning during migration" → FR4 (compatibility adapters) + FR12 (per-executor migration) + NFR6
- "Failure causality cannot be lost" → FR1 (envelope field list)
- "Partial success must remain representable" → FR3 + AC2
- "Non-idempotent work must not be auto-replayed" → FR7 + AC8
- "Stable status contracts for downstream consumers" → NFR5
- "Requirements-only scope" → enforced by document scope; no implementation prescribed

### Out-of-Scope Promotions

None promoted to in-scope. All seed-brief `out_of_scope` items remained out-of-scope in the merged output:

- Worker runtime replacement → not addressed; explicitly excluded
- Full workflow engine → not addressed; explicitly excluded
- Implementation code → not produced; requirements-only output
- Persistence backend selection → OQ2 (deferred to /sc:design as unresolved_conflict)
- Architecture decisions → deferred to /sc:design

### Fit-to-Intent Issues

(none — all `pass` criteria met: intent_summary matches output scope, context_anchors honored, must_preserve fully reflected, out_of_scope respected, source_confidence high)

### Unresolved Conflicts Detail

- **OQ2 / durability backend** — The architect and devops proposals diverged on persistence backend selection (architect leaned relational for audit query; devops leaned append-only log for replay-throughput). Both are viable; selection depends on incident-replay volume and audit query patterns. Deferred to /sc:design with both options documented for evaluation.
