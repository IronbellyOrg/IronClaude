# Base Selection — Option A vs Option B

## Combined scoring (0.0–1.0; higher = better fit for R1.3 NOW)

| Dimension | Weight | Option A | Option B (simplified, no-envelope) |
|-----------|--------|----------|-------------------------------------|
| Correctness (fixes DEV-001 real gap = semantic_checks run) | 0.25 | 1.00 | 1.00 |
| Regression-risk (installed-pkg + shared-executor) | 0.25 | 0.45 (A1 shared-executor risk; envelope-plumbing ripple) | 0.95 (local; no-envelope avoids INV-001) |
| Blast-radius / R1.3 scope fit | 0.20 | 0.40 | 0.95 |
| Spec-fidelity (§MVR §2 "wire as final step" + Contract #2 via CI) | 0.15 | 0.90 | 0.95 |
| Maintainability (no machinery certify doesn't need; helpers reused) | 0.15 | 0.60 (A2) / 0.40 (A1) | 0.80 |
| **Weighted total** | | **0.66** | **0.93** |

## Tiebreaker
Not needed — margin > 5%.

## Selected base: **Option B (simplified — no envelope passed)**

Rationale: B fixes the real DEV-001 correctness gap (certify semantic_checks now evaluate the produced report) with a local change, reuses existing helpers (`gate_passed`, `build_certify_metadata`, `check_certify_resume`), and — critically — by NOT passing envelope it correctly leaves the source-tree `assert_step_reachable` code_assertion as a CI-only check (INV-001), avoiding the pipx-install spurious-failure that firing it at runtime would cause. Option A's only edge (architectural purity) is overridden by the R1.3 "not a pipeline-executor refactor" scope and the installed-package safety constraint.

## Strengths from Option A to incorporate
- A's "certify gate-fail should be recorded in state" insight → B persists via `build_certify_metadata` + `write_state`.
- A's halt-semantics concern → B maps a certify gate-fail to `certified-with-caveats` (per `derive_pipeline_status`), not a hard `sys.exit`.

## Rejected (changes NOT being made)
- Plumbing envelope/repo_root into `execute_pipeline`'s `gate_passed` call — rejected for R1.3 (ripples to all gated steps + 4 consumer modules; explicitly R1.6 scope; and would wrongly fire source-tree assertions at runtime).
- Routing certify into the shared `execute_pipeline` step loop (A1) — rejected (changes shared-executor semantics; PRESERVE-adjacent risk).
