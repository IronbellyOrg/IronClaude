# §8.2 Integration-Test Coverage Map (resolves reflect G-1 silent-omission)

**Date:** 2026-06-03
**Step:** Phase 6, Step 6.13
**Source:** spec §8.2 (7 integration tests) + reflect report `.dev/reflect/pre-rv3-med-tasklist-20260602-172834/REPORT.md` finding G-1.

Every one of the 7 spec §8.2 integration tests has exactly ONE disposition below, so the layer is provably
not silently omitted. Dispositions: `ENCODED-NEW` (a new dedicated eval case), `ABSORBED` (covered by a per-FR
case's variants or a static gate), `RUNNER-DEFERRED` (encoded + explicitly deferred behind an absent runner).

| # | §8.2 test | Disposition | Where |
|---|-----------|-------------|-------|
| 1 | Serena-disabled + read-only full run (NFR-1/NFR-5) | **ABSORBED** | per-case skip variants in `serena-execute-verify` (--no-verify/read-only), `serena-onboarding` (context-excluded), `serena-handoff` (both-fail), `serena-type-hierarchy` (lsp-disabled) + the §14 fail-rows |
| 2 | Verification-triangle regression promotion-block (FR-4 + §14.5.2) | **ABSORBED** | `serena-execute-verify` (id 27, Step 6.2) — pytest exit-1 → regression_present → gate_evaluation_failures |
| 3 | Telemetry-completeness sweep (NFR-2) | **ENCODED-NEW** | `serena-telemetry-completeness` (id 35, Step 6.12) — holistic both-paths sweep |
| 4 | Contract-version bump regression (§5) | **ABSORBED** | static grep assertions in Steps 2.16 / 5.9 (no stale 1.1.0; contract_version == 1.2.0 at all canonical sites incl. report-template.md fixed in PG-5) |
| 5 | Token-budget delta measurement (NFR-3) | **RUNNER-DEFERRED** (encoded) | `serena-token-budget` (id 34, Step 6.11) — skeleton-pending-runner + explicit deferral record `nfr3-token-budget.md` (token-ledger runner absent) |
| 6 | Citation-freshness audit (NFR-4) | **ENCODED-NEW** | `serena-citation-freshness` (id 36, Step 6.12) — holistic re-Read-within-5-calls sweep |
| 7 | Verification-liveness (NFR-6) | **ABSORBED** | `serena-execute-verify` (id 27) timeout→124 variant (`verify_timeout_hit`, exit 124, run completes) |

## Cross-references
- ENCODED-NEW rows (3, 6) → eval-case dirs `cases/serena-telemetry-completeness/`, `cases/serena-citation-freshness/` (ids 35, 36).
- RUNNER-DEFERRED row (5) → `cases/serena-token-budget/` (id 34) + `phase-outputs/plans/nfr3-token-budget.md`.
- ABSORBED rows (1, 2, 4, 7) → the per-FR cases (ids 27, 31, 32, 33) + static greps in the verify steps.

## Result
All 7 §8.2 rows have an explicit disposition. The integration-test layer is no longer silently omitted (reflect G-1 resolved); the holistic NFR-2/NFR-4 cases resolve reflect G-2.
