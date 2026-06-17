# Golden-Capture Verdict (Step 4.2)

**Status: Complete**
**Verdict: PASS**
**Date:** 2026-06-16

## Criteria (all met)

All 3 scenario directories exist under
`tests/swarm/fixtures/bare_review_v1/golden/`, each containing the expected
per-reviewer `.md` bodies plus a non-zero `return-contract.yaml`:

| scenario | per-reviewer `.md` | contract | bodies expected | bytes (min) |
|----------|--------------------|----------|------------------|-------------|
| `all-success` | 01, 02, 03 | ✅ 954 B | 3 (M==N==3) | 568 |
| `partial-with-timeout` | 01, 02 | ✅ 882 B | 2 (slot 3 timed out → no body) | 568 |
| `salvage-promoted` | 01, 02, 03 | ✅ 954 B | 3 (slot 3 parse_error promoted) | 568 |

Every body and contract is non-zero (smallest body 568 B, smallest contract
882 B). Supporting files present: `_review_target.py` (frozen target),
`README.md` (regen discipline + normalization scheme).

Per-scenario body counts match the SCENARIOS plans exactly (the timeout slot in
`partial-with-timeout` correctly produces no body, per legacy hard-failure
semantics).

## Provenance

Generated from the **real** legacy `t2_normalize.py` via the env-gated regen
helper `tests/swarm/test_bare_review_golden_regen.py` (`SWARM_REGEN_GOLDEN=1`),
with CLI-aligned args. Byte-matchability against a fixture-fed live CLI run was
proven for the all-success scenario (sorted multiset equality) — see Phase 4
Findings and `phase-outputs/discovery/ws-b-golden-design.md`.

## Gate effect

The frozen golden exists and is well-formed → WS-C deletion may proceed **only
after** the WS-B parity gate (Step 4.5 / PG4) is GREEN. The golden is the
permanent reference that survives `t2_normalize.py` deletion.

Raw inventory: `phase-outputs/test-results/golden-inventory.txt`.
