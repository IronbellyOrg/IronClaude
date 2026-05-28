# Diff Analysis: Worker-Pool Error Handling Requirements

## Metadata

- Variants compared: 5
- Total differences found: 10
- Categories: structural (2), content (4), contradictions (1), unique (3), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Variant 4 | Variant 5 | Severity |
|---|------|-----------|-----------|-----------|-----------|-----------|----------|
| S-001 | Primary organizing principle | Envelope/classifier | Operations/replay | Contract testing | Security controls | Performance/backpressure | Medium |
| S-002 | Migration emphasis | Adapter-first | Flag/runbook-first | Gate-first | Approval-first | Overhead-first | Medium |

## Content Differences

| # | Topic | Variant Positions | Severity |
|---|-------|-------------------|----------|
| C-001 | Terminal state taxonomy | All variants agree on explicit states; architect is most complete | High |
| C-002 | Replay controls | DevOps and security require rate limits and audit; performance adds backpressure | High |
| C-003 | Test gates | QA requires contract matrix; others imply but do not enumerate | Medium |
| C-004 | Success-path overhead | Performance makes overhead a gate; architect treats it as constraint | Medium |

## Contradictions

| # | Conflict | Positions | Impact |
|---|----------|-----------|--------|
| X-001 | Atomic rollback vs partial success | Architect allows configurable policy; QA insists every mixed batch be representable; no irreconcilable conflict if policy is explicit | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | QA | Formal failure-mode contract gate | High |
| U-002 | Security | Redaction before persistence/display | High |
| U-003 | Performance | Backpressure and batching during failure storms | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Existing call sites can migrate incrementally without a flag day | All variants depend on compatibility migration | High | UNSTATED |
| A-002 | Worker tasks can expose stable work item identities | Envelope, replay, audit, and tests all require identity | High | UNSTATED |

## Summary

- Highest-severity items: C-001, C-002, U-001, U-002, U-003, A-001, A-002
- Debate should resolve envelope shape, terminal status taxonomy, replay authorization, testing gates, and performance budgets.
