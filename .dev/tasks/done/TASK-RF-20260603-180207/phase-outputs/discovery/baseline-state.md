# Baseline State — Step 1.4

**Captured:** 2026-06-03 19:40 · Branch: `integration` @ `e4daaa9e`

## (a) Whole-suite collection baseline

Command: `uv run pytest --collect-only -q 2>&1 | tail -8`

Verbatim tail:

```
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/integration/test_wiring_pipeline.py:28: in <module>
    from superclaude.cli.roadmap.gates import ALL_GATES, WIRING_GATE
E   ImportError: cannot import name 'WIRING_GATE' from 'superclaude.cli.roadmap.gates' (/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/gates.py)
=========================== short test summary info ============================
ERROR tests/integration/test_wiring_pipeline.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
==================== 7909 tests collected, 1 error in 1.53s ====================
```

- **Collected count:** 7909 tests
- **Error count:** 1
- **Area A collection error present?** YES — `ERROR tests/integration/test_wiring_pipeline.py` (the sole collection error). Root cause: `from superclaude.cli.roadmap.gates import ALL_GATES, WIRING_GATE` — `WIRING_GATE` no longer lives in `cli/roadmap/gates.py` (it moved to `cli/audit/wiring_gate.py`).
- Matches research file `07-test-verification.md` §0 expected baseline ("7909 tests collected, 1 error", single error = `test_wiring_pipeline.py`). ✓

## (b) Cutover SoT state — all 13 steps

Source: `.dev/migrations/r1-4-cutover-counters.yaml` (`cutover_at_count_default: 3`)

| Step | release_marker_count | cutover_at_count | cutover_eligible |
|------|----------------------|------------------|------------------|
| extract | 0 | 3 | false |
| extract_tdd | 0 | 3 | false |
| generate | 0 | 3 | false |
| diff | 0 | 3 | false |
| debate | 0 | 3 | false |
| score | 0 | 3 | false |
| merge | 0 | 3 | false |
| spec_fidelity | 0 | 3 | false |
| wiring_verification | 0 | 3 | false |
| test_strategy | 0 | 3 | false |
| certify | 0 | 3 | false |
| validate_reflect | 0 | 3 | false |
| remediation | 0 | 3 | false |

- **Any step cutover_eligible?** NO — all 13 steps are at `release_marker_count: 0` / `cutover_eligible: false` (0/3). Cutover precondition is **NOT-MET** for every step.
- Matches research file `05-area-de-dualwrite-vectorA-registry.md` Finding 1 (all steps 0/3, cutover_eligible false). ✓

## Implications for this task

- **Area A (Phase 2):** the collection error IS present → re-home + delete will clear it.
- **Areas D & E (Phases 5–6):** cutover precondition NOT-MET for all steps → those phases MUST HALT (write PENDING markers, delete no production code).

All counts and the cutover table are copied verbatim from the actual command output and YAML — no fabrication.
