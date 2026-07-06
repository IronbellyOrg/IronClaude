# Adversarial Debate Transcript

## Metadata

- Depth: deep
- Advocate count: 3
- Convergence threshold: 0.75
- Final convergence: 0.92
- Status: CONVERGED

## Round 1: Advocate Statements

### Variant 1 — Architect

The live problem is not just one stale version string; it is lack of a single source of truth. The installer should remain local stdio for this change, but the command-builder should be testable and transport-aware so future HTTP support does not require risky inline mutation.

### Variant 2 — Refactorer

The smallest safe fix is a local-stdio package update, deletion or neutralization of dead Tavily configs, and Tavily-scoped stale-install reconciliation. Remote HTTP/OAuth should not be bundled into this patch.

### Variant 3 — QA

The target should be observable: dry-run must show `tavily-mcp@latest`, stale 0.1.x installs must be detected, docs must agree with installer policy, and the map/crawl tool surface must be verified or documented as an integration smoke.

## Round 2: Rebuttals

### Version Policy

Architect/refactorer argued for a fixed `0.2.20` pin for reproducibility. QA argued that the user request and current docs target `@latest`, and multiple existing MCP package entries already use floating latest-style package specs. The merged decision accepts QA's `@latest` target while preserving reproducibility at the policy layer: one centralized package constant, tests forbidding 0.1.x, and docs-installer parity.

### Transport Policy

All variants agree that remote HTTP/OAuth is vendor-preferred but should not become the default in this upgrade. The current installer models stdio command tails; HTTP needs a positional URL and separate auth choices. Merged decision: keep `tavily` local stdio default and record remote HTTP as a future or optional `tavily-remote` path only if explicitly implemented with tests.

### Config Source of Truth

All variants agree that dormant Tavily JSON config files are misleading. Merged decision: delete or otherwise retire them; preferred acceptance criterion is deletion because repository search found no active Python loader for the config directory.

## Round 2.5: Invariant Probe Summary

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | guard_conditions | Dry-run must not mutate installed MCP state even when stale install is detected | ADDRESSED | HIGH | Tests require no remove/add subprocess calls in dry-run |
| INV-002 | interaction_effects | Stale migration must not affect AIRIS gateway or non-Tavily servers | ADDRESSED | HIGH | Requirements scope stale detection to exact server name `tavily` |
| INV-003 | guard_conditions | API key values must not appear in generated dry-run/log strings | ADDRESSED | MEDIUM | Redaction requirement and test matrix included |
| INV-004 | sufficiency_challenge | Version string update alone is insufficient because existing stale installs would still skip | ADDRESSED | HIGH | Migration/back-compat requirements explicitly added |

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---:|---|
| S-001 | Merged | 90% | SoT + minimal transform + tests all retained |
| S-002 | Merged | 95% | All variants agree remote HTTP default is deferred |
| C-001 | Variant 3 with controls | 78% | Explicit user request and docs favor `@latest`; controls address drift concerns |
| C-002 | Variant 2/3 | 91% | Deletion is simplest and testable |
| C-003 | All | 96% | All variants require stale-install reconciliation |
| C-004 | Variant 3 | 94% | Most complete test matrix |
| X-001 | Variant 3 with architect/refactorer safeguards | 78% | Centralized `@latest` token resolves target while retaining parity tests |
| A-001 | All | 99% | Shared agreement |
| A-002 | All | 99% | Shared agreement |
| A-003 | All | 96% | Shared agreement |
| A-004 | All | 96% | Shared agreement |

## Convergence Assessment

- Points resolved: 11 of 12
- Alignment: 0.92
- Threshold: 0.75
- Status: CONVERGED
- Unresolved tensions: whether a future remote HTTP mode should use OAuth-only or API-key query/header support remains out of scope for this merged spec.
