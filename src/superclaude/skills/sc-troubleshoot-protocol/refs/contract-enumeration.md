# Contract Enumeration (H2)

H2 builds a producer/transformer/consumer **ledger** for the changed contract (a field, flag, parser rule, semantic check, selector, status, or predicate) and sweeps sibling pipelines and duplicate evaluators. It closes **E4** (the shared `SemanticCheck.advisory` honored by the generic gate but not the PRD `_evaluate_gate`) and supports **E1** (PRD identified as the sibling-contract outlier vs the roadmap/tasklist/validate file-delivery consumers). The H2 status feeds the §5.4 aggregation in [`hardening-output-contract.md`](hardening-output-contract.md).

## H2 Contract Ledger Row schema (§5.6)

| Field | Required | Meaning |
|-------|----------|---------|
| `contract_token` | yes | Field / flag / parser rule / semantic check / status / predicate under change |
| `role` | yes | `producer`, `transformer`, `consumer`, `evaluator`, or `dead/legacy` |
| `component_path` | yes | Source / ref / test path or generated-artifact path |
| `discovery_method` | yes | Symbol/reference search, exact grep, semantic retrieval, sibling scan, fixture scan, or manual evidence |
| `classification` | yes | `classified`, `unclassified`, or `dead/legacy_with_proof` |
| `unreachability_proof` | required for `dead/legacy` | Why runtime cannot reach the component |

> **OI-2 deferral (PENDING human decision).** Which tokens are *first-class* ledger entries (flags, phase-IDs, gate-names, verdicts, step-IDs, statuses) is an open item (OI-2). The `contract_token` field is therefore an **OPEN / extensible** enumeration: the classes just listed are **examples**, not a closed set. Do not finalize a closed first-class vocabulary here — that decision is deferred to OI-2. See `phase-outputs/plans/OI-2-PENDING.md`.

## FAIL rules (FR-5)

H2 **FAILs** if any of the following hold:

- **Empty / zero-row ledger.** An empty ledger does **not** vacuously pass — a zero-row ledger cannot satisfy "no unclassified consumer" (fixes adversarial F-N3).
- **Unclassified live consumer.** Any live consumer left `unclassified`.
- **Generic/shared proof without product-path proof.** Generic or shared proof is used for a product path without proving the product path actually reaches that implementation.

The ledger MUST enumerate **≥ the consumer count** discovered by symbol/reference search plus semantic search. A `dead/legacy` role requires an **unreachability proof**, not an assertion.

## Sibling / duplicate-evaluator sweep (FR-6)

When a concept is shared, H2 **FAILs** if sibling pipelines or duplicate evaluators are not swept. The sweep must inventory every implementation that consumes the changed contract — e.g. a generic gate, a product-specific evaluator, a trailing gate, and a remediation-dispatch path — before closure.
