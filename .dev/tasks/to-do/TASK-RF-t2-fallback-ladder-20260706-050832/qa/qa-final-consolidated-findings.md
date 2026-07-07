# QA — Phase 6 Final Aggregate Gate: Consolidated Findings (Step 6.G9)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Inputs:** 7 report-only adversarial lens agents (Steps 6.G2–6.G8)

## Aggregate verdict

**PASS with a bounded fix cycle.** Zero CRITICAL. Zero runtime-correctness defects. Every lens independently confirmed the implementation logic is correct (F1 slot-NAME binding, F4 wall-clock, F6 first-match precedence, additive-only contract, no proxy-cred leak, verdict-honesty structural guarantee). The two FAIL verdicts are both **non-correctness**:

- actionability FAIL → driven by **I1** (one runtime seam proven only at the pure-planner layer — a *coverage-depth* gap, not a wrong test).
- structural-consistency FAIL → driven by **I2** (a stale docstring/comment making a false integration claim — *documentation accuracy*, no behavior change).

Both are closable with additive test + docstring edits. No implementation logic changes.

## Per-lens roll-up

| Step | Lens | Verdict | Findings |
|------|------|---------|----------|
| 6.G2 | structural-conformance | PASS | M1 (orphan fixture); INFO count-nuance |
| 6.G3 | structural-consistency | FAIL | **I2** (false builder-integration docstring); M5 (task import-allowlist enumeration gap) |
| 6.G4 | structural-additive | PASS | 0 issues |
| 6.G5 | content-actionability | FAIL | **I1** (F4 controller wall-clock untested); M1 (orphan fixture); M3 (httpx leak) |
| 6.G6 | content-enums | PASS | M1 (orphan fixture / G1); M2 (enum ValueError guard untested / G2) |
| 6.G7 | content-crossref | PASS | **I1** (F4 controller wall-clock untested — corroborates 6.G5); M4 (recipe-literal drift F2); INFO F3 |
| 6.G8 | domain-honesty | PASS | O1/O2/O3 LOW/INFO — none affects honesty |

## Deduplicated actionable items (final fix cycle — all additive)

| ID | Sev | Source lenses | Location | Fix | Kind |
|----|-----|---------------|----------|-----|------|
| **I1** | IMPORTANT | 6.G5 #1 + 6.G7 F1 (2 lenses concur) | `test_ensemble_fallback_stub.py` (all `run_fallback_ladder` calls pass `deadline_monotonic=None`) | Add a controller-level test injecting an exhausted/near-zero `deadline_monotonic` into `run_fallback_ladder` (§8 incident shape, spy `dispatch`): assert dispatch spy NEVER called AND `terminal_reason == "fallback_wall_clock_exhausted"` AND `fallback_attempt_count == 0`; plus one asserting the `min(config.timeout_seconds, remaining)` clamp on a mid-range remaining. | TEST |
| **I2** | IMPORTANT | 6.G3 #1 | `swarm/commands.py` `_resolve_run_transport_factory` docstring (~L666) + comment (~L698) | Correct the docstring/comment: the reflect T1 fallback resolver does NOT read its pool through this builder — `ensemble.resolve_t1_fallback_factory` calls `read_env_for_pool` + `make_fallback_slot_factory` directly (required for slot-NAME binding; the builder returns a positional factory). Describe the direct-read design; drop the false "SAME builder" claim. Keep the 4 defaulted kwargs (harmless, backward-compat). | DOCSTRING (no behavior) |
| **M1** | MINOR | 6.G2 #1 + 6.G5 #2 + 6.G6 G1 (3 lenses) | `tests/cli/reflect/fixtures/pass_with_t2_fallback.yaml` (orphan) | Wire into a `test_verdict_mapping.py` case: load the fixture, assert `derive_verdict(...).verdict is Verdict.PASS` (verdict-unchanged with fallback metadata present). Closes the additive-only proof symmetrically and removes the dead artifact. | TEST |
| **M2** | MINOR | 6.G6 G2 | `fallback.py` `build_fallback_metadata` enum guard; `test_contract_fallback_metadata.py` | Add two `pytest.raises(ValueError)` cases (`terminal_reason="not_a_real_reason"`, `certification_basis="bogus"`), asserting the message names the offending token. | TEST |
| **M3** | MINOR | 6.G5 #3 | `tests/swarm/test_openai_compat.py` `test_resolve_factory_t1_branch_binds_per_slot_models`, `..._pool_too_small_raises` | Close the constructed `OpenAICompatTransport`s in `try/finally` (they each open an `httpx.Client`), matching the reflect-side `_closing_factory` hygiene. | TEST |
| **M4** | MINOR | 6.G7 F2 | `fallback.py` `_REFLECT_REVIEW_RECIPE` vs `ensemble.py` `REFLECT_REVIEW_RECIPE` (duplicated to break the import cycle) | Add a guard test asserting `fallback._REFLECT_REVIEW_RECIPE == ensemble.REFLECT_REVIEW_RECIPE` so AC #8's "same normalization contract" can't silently drift. | TEST |
| **M5** | MINOR | 6.G3 #2 | Task file Key Objective 1 import-allowlist enumeration | Add `swarm.preflight` and `swarm.transports.openai_compat` to the enumerated fallback.py allowlist (both verified leaf modules, no reflect back-import → invariant holds; enumeration was just inaccurate). | TASK FILE |

## Explicitly cleared (no action)

- **"Augmented set" vs "smallest contributing set"** — design.md §4 authoritatively specifies the *smallest* satisfying set; implementation is faithful. "Augmented" is loose intro wording in both task + design, not a defect. (6.G3 notes)
- **F3 AC-#2 wording** — next-unattempted-slot logic reaches T1Model02 only after T1Model01; intentional, documented in design §4.2. (6.G7 F3)
- **domain-honesty O1/O2/O3** — enabled-path reviewer_count telemetry delta; try/except catching only 2 exception types (other faults → honest fail-loud BLOCKED); unreachable `allow_single_vendor`-agnostic slug. None can produce a false PASS. (6.G8)
- **`_T1_PROXY_BINDING is None` dead defensive arm** — harmless given the CONFIRMED non-None binding.
- **conformance INFO count-nuance** — 8 vs 6 reflect test files = documented authorized over-delivery.

## Fix-cycle scope

ONE serialized fix agent (Step 6.G10), `fix_authorization: true`. Six code/test edits (I1, M1–M4, plus I2 docstring) + one task-file edit (M5). No implementation-logic change; `contract.py`/`swarm/models.py` remain 0-diff. Verify with `pytest -k "reflect or swarm"` + scoped ruff (6.G11).
