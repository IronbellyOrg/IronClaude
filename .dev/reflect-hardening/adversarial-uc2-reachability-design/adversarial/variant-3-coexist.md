# Variant 3 — Position: One 1.6.0 contract hosts BOTH field families (coexist now)

<!-- Source: design position synthesizing the user's question 2; EXISTING_MATRIX M-028 -->

## Thesis

`contract_version: "1.6.0"` is defined as `1.5.0` **+** B's `runtime_surface_*` fields **+** C's `reachability_*` R7 fields — all additive, all optional. Both designs ship together now; UC-1 may omit the reachability block, un-annotated surfaces may omit runtime_surface, and the single minor bump carries both.

## Feasibility

- **Field names do not collide** (`runtime_surface_*` vs `reachability_*`), so a union schema is mechanically valid.
- **Deviation taxonomy can host both** in principle: B's `UNREACHED` is a finding *modifier* (no new class) and C's mapping adds no fifth class — both preserve the 4-category invariant.

## Costs / risks (why this is the weakest position)

1. **Violates C-040 as written** — C's `no-fr-rsr-semantic-leakage` QA lens asserts the *absence* of `runtime_surface_*`/UNREACHED. Co-locating B's fields in the same SKILL.md/contract makes C's own acceptance gate FAIL unless C-040 is rewritten.
2. **Forces simultaneous landing** of two large edits to the *same* SKILL.md sections + `deviation-taxonomy.md` + `evals.json` → maximal merge conflict and a 3-way single-fix-agent serialization problem (matrix M-016/M-047).
3. **Unsafe without a precedence invariant** (see invariant-probe INV-001): B's degrade-only/fail-open posture could mask C's real-boot Regression for the same root cause.
4. **Couples two independent features' release cadence** and doubles operator cognitive load (two reachability verdicts, two ledgers).
