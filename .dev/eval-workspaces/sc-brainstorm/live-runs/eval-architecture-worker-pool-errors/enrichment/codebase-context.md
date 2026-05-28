---
source: codebase
quality_tier: primary
topic: "redesign error handling across worker pool"
---

# Codebase Context: Worker-Pool Error Handling

## Relevant Existing Code

- `src/superclaude/execution/parallel.py` defines a `ParallelExecutor` that executes task groups through `ThreadPoolExecutor`, catches task exceptions, marks task state failed, stores the exception on the task, and returns `None` for the task result. This is a key integration point because result maps currently encode failure ambiguously.
- `src/superclaude/execution/__init__.py` wraps intelligent execution and detects `None` results as failures. It feeds failure information into self-correction, but does not preserve a typed error envelope per task.
- `src/superclaude/cli/roadmap/remediate_executor.py` has richer failure semantics: snapshots, timeout/retry wrappers, per-file rollback, cross-file coherence checks, and success/failure status propagation. It demonstrates the need for scoped rollback and partial rejection rather than one global error shape.
- `src/superclaude/cli/audit/batch_retry.py` keeps retry records, attempt counts, terminal status, and final failure reason. This is a useful precedent for a generalized attempt ledger.
- `src/superclaude/cli/prd/process.py` distinguishes transient launch failures from non-transient failures and reports exhausted retries with causal detail.
- `src/superclaude/cli/pipeline/trailing_gate.py` models remediation retry states such as budget exhaustion, first/second-attempt pass, and persistent failure.

## Architecture & Patterns

- Current patterns are distributed by subsystem; there is no single worker failure contract.
- Existing code already values explicit status propagation and retry accounting, but each subsystem uses its own representation.
- Some flows prioritize safe rollback; others preserve partial results. The new requirements must support both via explicit policy.
- CLI-facing workflows need stable contracts rather than raw exceptions because downstream gates and evaluators consume status fields.

## Integration Points

- Parallel task execution result collection and terminal status mapping.
- Remediation executor failure/rollback handling.
- Audit retry ledger and batch terminal status recording.
- Pipeline retry/gate result contracts.
- Self-correction/reflexion failure ingestion.

## Constraints Identified

- Existing callers may depend on `None` result behavior, so migration should allow compatibility shims.
- Worker pools may execute heterogeneous tasks; one pool-level error cannot represent all task outcomes.
- Exception objects are not durable or stable contracts; structured envelopes are required.
- Some work is non-idempotent and cannot be replayed automatically.
