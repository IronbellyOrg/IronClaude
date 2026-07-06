# Diff Analysis: Tavily MCP Upgrade Proposal Comparison

## Metadata

- Variants compared: 3
- Categories: structural, content, contradictions, unique contributions, shared assumptions

## Structural Differences

| ID | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Scope framing | SoT + transport abstraction | Minimal-risk version/config convergence | Test-first observable upgrade | Medium |
| S-002 | Future HTTP handling | Defines as separate transport abstraction | Explicitly defers | Explicitly defers and asks for separate tests | Low |

## Content Differences

| ID | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Version strategy | Centralized token, leaning latest-known pin | Centralized token, leaning pin | Centralized `@latest` token | High |
| C-002 | Config cleanup | Delete or neutralize dormant configs | Prefer deletion | Assert deletion via tests | Medium |
| C-003 | Migration behavior | Reconcile stale install rather than skip | Tavily-scoped stale detector | Remove/re-add under mocks and dry-run | Low |
| C-004 | Test surface | Parity, grammar, redaction, migration | Regression and docs/config convergence | Detailed unit and optional integration matrix | Low |

## Contradictions

| ID | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Whether installer should use `@latest` or latest-known pin | Prefer fixed `0.2.20` constant | Prefer fixed `0.2.20` constant | Prefer `tavily-mcp@latest` | Must be resolved because user asked for version strategy |

## Unique Contributions

| ID | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | Variant 1 | Pure command-builder seam and future HTTP grammar notes | High |
| U-002 | Variant 2 | Explicitly excludes AIRIS gateway Tavily env references from this change | Medium |
| U-003 | Variant 3 | Detailed mocked unit-test matrix and optional live tool-surface smoke | High |

## Shared Assumptions

| ID | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Default transport should remain local stdio for this upgrade | All variants | Avoids coupling version bump to remote/OAuth migration | Promoted |
| A-002 | Existing name-only installed check is insufficient for stale Tavily upgrades | All variants | Required for back-compat success | Promoted |
| A-003 | Dead Tavily JSON configs must not remain as contradictory apparent sources of truth | All variants | Required to prevent future drift | Promoted |
| A-004 | Tests should mock Claude CLI for unit coverage and isolate live tool checks as optional integration | All variants | Keeps CI deterministic | Promoted |

## Summary

The only high-severity disagreement is version policy. The merged decision resolves it in favor of `tavily-mcp@latest` because the driving request explicitly targets `@latest` and existing docs already document it. Reproducibility concerns are addressed by centralizing the package token, documenting the decision, and adding regression tests that forbid 0.1.x and docs/installer drift.
