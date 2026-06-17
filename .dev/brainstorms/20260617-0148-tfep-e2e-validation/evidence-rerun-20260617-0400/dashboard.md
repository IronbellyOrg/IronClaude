# TFEP E2E Validation Dashboard — v2 (post-probe-fix)

Policy: `strict_12_of_12_green_plus_digest_identity` · Generated: 2026-06-17T04:00:00Z

| Test | Run1 | Run2 | Run3 | Digest-identical | Test-status |
|------|:----:|:----:|:----:|:----------------:|:-----------:|
| E1 — Residual-Integrity & Sync-Parity   | PASS | PASS | PASS | YES (443baab42cb2) | PASS |
| E2 — Adapter Contract Round-Trip        | PASS | PASS | PASS | YES (202f96f6aa6f) | PASS |
| E3 — Protocol-Chain Resolution          | PASS | PASS | PASS | YES (18f526d247a6) | PASS |
| E4 — Safety-Invariant Preservation      | PASS | PASS | PASS | YES (1c6bb52e67cd) | PASS |

Totals: 12/12 runs PASS · 4/4 tests with byte-identical per-test digests.

**GATE: GREEN**

## v1 → v2 delta

E3 and E4 moved DISAGREE → PASS after three probe/schema (instrumentation) fixes — E4-I4a regex, E4-I1b regex, and E3 branch_keys digest determinism — with NO migration change.
E1 and E2 carried over unchanged from the v1 GREEN run; the migration artifacts themselves were never touched, so the closed gate reflects corrected measurement, not altered behavior.

## Definition of done

MIGRATION_VALIDATED = true — established by 12/12 PASS verdicts plus 4×3/3 byte-identical `normalized_observation_digest` values (E1 443baab42cb2, E2 202f96f6aa6f, E3 18f526d247a6, E4 1c6bb52e67cd), satisfying the strict 12-of-12-green-plus-digest-identity gate.
