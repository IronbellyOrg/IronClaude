# Codebase Context: payment webhook delivery failures Q1

## Relevant Existing Code

- `src/superclaude/cli/audit/batch_retry.py` — batch retry handling with configurable retry count, failed status marking, and minimum viable report output on cascading failure. This is not payment-webhook code, but it is a relevant in-repo failure/retry policy pattern.
- `src/superclaude/cli/roadmap/remediate_executor.py` — parallel execution with retry-once behavior, rollback, and per-file failure isolation; relevant as a pattern for containment, retries, rollback, and partial-failure accounting.
- `src/superclaude/cli/pipeline/diagnostic_chain.py` — multi-stage diagnostic chain for persistent failures with graceful degradation; relevant to incident investigation and remediation sequencing.
- `.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-incident-payment-webhook-q1/old_skill/outputs/requirements.md` — prior monolithic brainstorm output for this exact incident scenario, including PIR context, retry tiers, DLQ pressure, compliance concerns, and acceptance criteria.
- `.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-incident-payment-webhook-q1/with_skill/outputs/merged-requirements.md` and `adversarial/proposal-1-analyzer-opus.md` — prior adversarial-v2 artifacts for this exact scenario, useful as historical context but not copied as the live-run result.

## Architecture & Patterns

- The repository is SuperClaude/IronClaude, not a payment system implementation. There is no production `payments-webhook-dispatcher` service in source.
- Existing code patterns emphasize bounded retries, explicit failed-state recording, rollback/isolation, graceful degradation, and diagnostic chains.
- The brainstorm protocol treats incident topics as requiring systematic requirements discovery, optional codebase enrichment, multi-persona proposal generation, adversarial merge, and a versioned return contract.

## Integration Points

- The live run should produce `seed-brief.md`, `merged-requirements.md`, `adversarial/` artifacts, `enrichment/codebase-context.md`, and `return-contract.yaml` under the requested evaluation output folder.
- Downstream consumers should use `merged-requirements.md`; no handoff was requested (`--handoff none`).

## Constraints Identified

- No repository code exists for an actual payment webhook dispatcher, so implementation-specific remediation must remain requirements-level.
- Requirements should preserve incident scope: Q1 delivery failures, three PIRs, Redis Streams delayed retry, PostgreSQL DLQ, merchant reconciliation gaps, SLO/PCI evidence-chain implications.
- Existing stale `live-run-error.md` should be removed only after the run succeeds.
