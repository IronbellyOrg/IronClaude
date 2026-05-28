---
schema_version: "1.0"
topic: "Brainstorm redesigning error handling across the worker pool"
domain: architecture
strategy: enterprise
depth: deep
proposals_target: 5
handoff_target: none
intent_summary: "Redesign error-handling requirements across the worker pool so that every task reaches a single, classifiable terminal state with a stable error envelope, bounded retries, safe replay, scoped rollback, and observable failure semantics — without breaking existing executors via incremental migration."
context_anchors:
  - type: component
    value: "worker pool"
    source: topic
    confidence: high
  - type: concept
    value: "error handling"
    source: topic
    confidence: high
  - type: concept
    value: "redesign"
    source: topic
    confidence: high
  - type: component
    value: "src/superclaude/execution/parallel.py (ParallelExecutor — None-on-failure pattern)"
    source: codebase-enrichment
    confidence: high
  - type: component
    value: "src/superclaude/cli/roadmap/remediate_executor.py (snapshot + rollback + cross-file coherence)"
    source: codebase-enrichment
    confidence: high
  - type: component
    value: "src/superclaude/cli/audit/batch_retry.py (retry ledger + terminal status precedent)"
    source: codebase-enrichment
    confidence: high
  - type: component
    value: "src/superclaude/cli/prd/process.py (transient vs non-transient launch classification)"
    source: codebase-enrichment
    confidence: high
  - type: component
    value: "src/superclaude/cli/pipeline/trailing_gate.py (remediation retry state machine)"
    source: codebase-enrichment
    confidence: high
  - type: concept
    value: "terminal taxonomy (succeeded/failed/cancelled/quarantined/skipped/unknown)"
    source: research-enrichment
    confidence: high
  - type: concept
    value: "stable failure envelope / dead-letter contract"
    source: research-enrichment
    confidence: high
  - type: concept
    value: "bounded retries with idempotency-aware promotion"
    source: research-enrichment
    confidence: high
  - type: concept
    value: "incremental migration (compatibility window, no flag day)"
    source: research-enrichment
    confidence: high
must_preserve:
  - "Worker pool (the execution layer being redesigned — not replaced)"
  - "Existing executors must continue functioning during incremental migration (no repo-wide flag day)"
  - "Failure causality, task identity, retry attempt history, and rollback decisions cannot be lost"
  - "Partial success must remain representable — a pool failure must not erase successful tasks"
  - "Non-idempotent work must not be auto-replayed without explicit policy authorization"
  - "CLI/pipeline/eval consumers depend on stable status contracts — raw exceptions are not a contract"
  - "Requirements-level output only — no implementation code, no DB/API schema beyond envelope field-level requirements"
out_of_scope:
  - "Replacing the worker runtime itself (e.g., swapping ThreadPoolExecutor for a different concurrency primitive)"
  - "Introducing a full workflow engine (Temporal, Airflow, etc.)"
  - "Writing implementation code or migrating call sites in this brainstorm"
  - "Specifying concrete database schemas or persistence backends beyond envelope field requirements"
  - "Architecture-level design decisions (deferred to /sc:design after merged requirements)"
source_confidence: high
created: 2026-05-27T00:00:00Z
---

# Seed Brief: architecture-worker-pool-errors

## Intent Summary

The user wants a deep, enterprise-strategy brainstorm that produces unified requirements for worker-pool error handling. The current state has fragmented failure semantics: ParallelExecutor collapses task exceptions to `None` results, remediate_executor.py implements rich rollback + retry, batch_retry.py keeps an attempt ledger, prd/process.py distinguishes transient vs non-transient launch failures, and pipeline/trailing_gate.py models its own retry state machine. The redesign must produce a single error-handling contract that preserves throughput, makes failures classifiable, supports bounded retries, enables safe replay, scopes rollback explicitly, and allows incremental per-executor migration. Output is requirements-only — implementation, schema design, and architecture decisions are explicitly deferred to downstream commands.

## Context Anchors

- component — worker pool (topic/high)
- concept — error handling (topic/high)
- concept — redesign (topic/high)
- component — src/superclaude/execution/parallel.py / ParallelExecutor (codebase/high)
- component — src/superclaude/cli/roadmap/remediate_executor.py (codebase/high)
- component — src/superclaude/cli/audit/batch_retry.py (codebase/high)
- component — src/superclaude/cli/prd/process.py (codebase/high)
- component — src/superclaude/cli/pipeline/trailing_gate.py (codebase/high)
- concept — terminal taxonomy (research/high)
- concept — failure envelope / dead-letter contract (research/high)
- concept — bounded retries + promotion (research/high)
- concept — incremental migration / compatibility window (research/high)

## Must Preserve

- The worker pool is the redesign target, not the replacement target — the execution layer stays
- Existing executors (ParallelExecutor, remediate_executor, batch_retry, process, trailing_gate) must continue functioning during migration
- Failure causality (which task, which worker, what error class, attempt history, rollback decision) must survive any contract change
- Partial success representation — a mixed-outcome batch must not be flattened to a single status
- Non-idempotent work safety — automatic replay is blocked unless policy explicitly authorizes
- Stable status contracts for downstream consumers (CLI, pipeline gates, evaluators)
- Requirements-only scope — no implementation, no schema design, no architecture decisions

## Out of Scope

- Worker runtime replacement (concurrency primitive swaps)
- Full workflow engine introduction (Temporal/Airflow class systems)
- Implementation code or call-site migration in this brainstorm
- Concrete persistence backend / database schema selection
- Architecture-level design (deferred to /sc:design)

## Problem Statement

The worker execution layer has inconsistent failure semantics across parallel task execution, remediation executors, audit batching, and process/pipeline retries. Some paths return `None` on task failure, some persist retry records, some rollback broadly, and some surface raw exceptions. Downstream consumers (CLI gates, pipeline orchestrators, evaluators) cannot reliably distinguish success, failure, cancellation, partial success, or poison inputs. The goal is to define enterprise-grade requirements for a unified worker-pool error-handling model that preserves throughput while making failures classifiable, observable, retryable where safe, recoverable where needed, and migratable per-executor without a flag day.

## Socratic Discovery

**Q1. What is being redesigned?**
A: The error-handling contract across the worker pool layer — terminal status taxonomy, failure envelope shape, retry policy semantics, replay controls, rollback scoping, observability, and migration approach. Not the worker runtime itself.

**Q2. What failure classes must the system distinguish?**
A: Retryable/transient (deps, rate limits, timeouts), non-retryable/deterministic (invalid input, invariant violations, authz), poison/unclassifiable (repeated crashes in classification), cancellation, timeout, partial success, and orchestration/transport failures.

**Q3. What information cannot be lost?**
A: Work item identity, worker/pool id, terminal status, error class, cause chain, attempt count, retry policy applied, idempotency key, replay eligibility, rollback decision, timestamps, and operator action history.

**Q4. Where is compatibility required?**
A: All existing executors must keep working during migration. Compatibility mode must emit both legacy status and the new envelope during the migration window. Migration must be per-call-site enableable.

**Q5. Who consumes the results?**
A: CLI workflows, pipeline gates, remediation orchestrators, test/eval graders, self-correction/reflexion ingestion, and incident-response operators.

**Q6. What is the recovery posture?**
A: Bounded retries with explicit promotion rules; quarantine over infinite retry; partial success preservation when safe; explicit rollback only where atomicity is required.

**Q7. What observability is required?**
A: Per-worker and per-task metrics for terminal state distribution, error class breakdown, retry exhaustion rate, quarantine growth, replay outcomes, cancellation/timeout counts, rollback success/failure, and unknown-status incidence.

**Q8. What should happen on worker-pool shutdown?**
A: In-flight tasks receive cancellation context, queued work remains durable or resumable, and the final pool contract reports completed/failed/cancelled/unknown counts as separate fields — never collapsed.

**Q9. How should operators intervene?**
A: Filtered replay/quarantine controls, rate limits on replay, justification + audit logging for manual replay, dry-run path before high-risk replay, and explicit approval gating for non-idempotent work.

**Q10. What is enterprise about this strategy?**
A: Deep-tier coverage of security (redaction, replay authz, audit), operational rollout (per-call-site flags, compatibility windows, rollback rehearsal), QA contract gates (terminal-state, retry-exhaustion, replay-denial, rollback-failure, partial-success contract tests), and performance budgets (hot-path overhead, failure-store backpressure, retry-storm prevention).

## Known Context

- ParallelExecutor in `src/superclaude/execution/parallel.py` catches task exceptions, marks task state failed, stores the exception on the task, and returns `None` for the task result — failure is encoded ambiguously in the result map.
- `src/superclaude/execution/__init__.py` detects `None` results as failures and feeds them into self-correction without preserving a typed envelope per task.
- `src/superclaude/cli/roadmap/remediate_executor.py` has richer failure semantics: snapshots, timeout/retry wrappers, per-file rollback, cross-file coherence checks, success/failure status propagation — demonstrates scoped rollback and partial rejection.
- `src/superclaude/cli/audit/batch_retry.py` keeps retry records, attempt counts, terminal status, and final failure reason — useful precedent for a generalized attempt ledger.
- `src/superclaude/cli/prd/process.py` distinguishes transient launch failures from non-transient and reports exhausted retries with causal detail.
- `src/superclaude/cli/pipeline/trailing_gate.py` models remediation retry states including budget exhaustion, first/second-attempt pass, and persistent failure.
- Research patterns recommend: typed error taxonomies, bounded retries with promotion, structured failure envelopes, idempotency-aware replay, observable terminal states, and incremental migration via compatibility windows.

## Constraints

- Requirements-only output — do not change source code or specify implementation in this phase
- Failure contracts must not collapse distinct outcomes into a single `None`, generic exception string, or boolean
- Retry policy must be bounded, typed, idempotency-aware, and have explicit promotion rules
- Partial success must be representable — pool-level failure must not erase per-task outcomes
- Rollback semantics must be explicit and scoped (per-item, configured atomic group, or pool-level — chosen by policy)
- Operator replay must be rate-limited, auditable, idempotency-aware, dry-run capable, and approval-gated for non-idempotent work
- Migration must be per-call-site enableable with a compatibility window — no flag day
- Sensitive payloads and credentials must be redacted before persisted or displayed
- Enterprise depth must address security (redaction, authz, audit), ops (rollout, replay, runbooks), QA (contract gates), and performance (overhead, backpressure)

## Success Criteria

- A stable worker error envelope is defined for all worker-pool implementations
- Every task reaches exactly one terminal status: succeeded, failed, cancelled, quarantined, skipped, or unknown
- Retryable failures are bounded and promoted to terminal failure or quarantine after policy exhaustion
- Non-retryable and poison failures are not retried blindly
- Metrics, logs, and return contracts let consumers identify which tasks failed and why
- Existing workflows can migrate one executor / call site at a time without breaking peers
- Replay is rate-limited, auditable, idempotency-aware, and approval-gated for non-idempotent work
- Sensitive context is redacted before persistence or display by default
- Requirements are ready for /sc:design without making implementation or schema decisions here

## Open Questions

- Which worker pools require atomic group rollback versus partial success preservation?
- Which task types are idempotent enough for automatic replay, and which require manual approval?
- What durability layer should hold failure envelopes and replay audit records in production?
- What compatibility window is acceptable for legacy result shapes during migration?
- What hot-path overhead budget should be enforced per executor class for envelope serialization?
- Who owns replay authorization and incident runbook approval in operational deployments?

## Enrichment Context

Codebase enrichment (primary tier) surveyed five existing executors and confirmed fragmented failure patterns: None-on-failure encoding in ParallelExecutor, snapshot+rollback semantics in remediate_executor, retry ledger persistence in batch_retry, transient/non-transient classification in process, and a remediation retry state machine in trailing_gate. Research enrichment (primary tier, deep) confirmed industry patterns: typed taxonomies with retryable/non-retryable/poison/cancellation/timeout classes, bounded retries with idempotency-aware promotion, stable dead-letter envelopes with redaction markers, safe replay controls (rate-limited, audited, dry-run capable), terminal-state observability, and incremental migration via compatibility windows. Five proposals were generated across architect (envelope/classifier), devops (rollout/replay), qa (contract gates), security (redaction/authz/audit), and performance (overhead/backpressure) personas.

## Defaults Applied (Non-Interactive Run)

- depth: deep (from flag)
- proposals_target: 5 (from flag)
- strategy: enterprise (from flag) — also implies depth deep (Wave 0 step 10; already explicit)
- domain: architecture (auto-classified — topic is a system-wide redesign of error semantics across multiple executors)
- handoff_target: none (not specified by user)
- personas: enterprise-default set per Wave 2B step 1 — architect, devops, qa, security, performance (5 to match proposals_target)
- model rotation: opus for architect (deep + heavy-lift), sonnet for devops/security/performance, haiku for qa (per Wave 2B step 2 deep-tier rule preferring opus for analyzer/architect personas)
- enrichment: both codebase (architecture domain) and research-deep (enterprise + novel-cross-cutting topic) auto-invoked
- source_confidence: high (topic + flags fully specified; codebase + research enrichment both primary tier)
