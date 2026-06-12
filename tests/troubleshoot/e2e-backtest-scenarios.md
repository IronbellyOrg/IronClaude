# E2E Backtest Scenarios

Documented executable-intent backtests for the Pipeline Hardening Closure mode, derived
verbatim from RELEASE-SPEC v1.1.0 §8.3. These are **documented** scenarios (not
pytest-collected); the NFR-1 replay suite that executes them is deferred to milestone M5.
Each scenario maps 1:1 to a pipeline escape (E1–E5) or the cross-cutting no-re-greening
invariant. The 13 unit + 5 integration tests in this directory are the executable Phase 7
validation; these scenarios document the end-to-end replays that M5 will automate.

## E1 backtest

- **Scenario:** Replay a headless PRD `--spec` invocation with a local-path `--file` against H1 (Runtime-Entrypoint Verification).
- **Steps:** Replay headless PRD `--spec` with a local-path `--file` against H1.
- **Expected outcome:** H1 FAIL pre-fix (negative witness), PASS post-fix.
- **Mapped escape / FR coverage:** E1; FR-3 (runtime-entrypoint verification) + FR-4 (negative witness).

## E2 backtest

- **Scenario:** Replay a full generated artifact containing `complete` and near-miss `incomplete` phase text against the H3 classifier.
- **Steps:** Replay the full generated artifact containing `complete` and near-miss `incomplete` phase text against the H3 classifier.
- **Expected outcome:** The intended executable violation still HALTs; the near-miss sibling negative does not hard-fail.
- **Mapped escape / FR coverage:** E2; FR-7 (whole-artifact classifier) + FR-8 (word-boundary / near-miss negatives).

## E3 backtest

- **Scenario:** Replay a Task-Log/Findings sibling-heading artifact against the H3 unmask/sweep card.
- **Steps:** Replay the Task-Log/Findings sibling-heading artifact against the H3 unmask/sweep card.
- **Expected outcome:** H3 FAILs until `K_swept == K_true` and non-executable headings WARN/CONTINUE rather than HALT.
- **Mapped escape / FR coverage:** E3; FR-7 + FR-8 + FR-9 (unmask-and-sweep regression).

## E4 backtest

- **Scenario:** Run an `advisory` semantic check through PRD `_evaluate_gate` with the H2 ledger.
- **Steps:** Run an advisory check through PRD `_evaluate_gate` with the H2 ledger.
- **Expected outcome:** H2 FAIL until both `gate_passed` and `_evaluate_gate` consumers are classified.
- **Mapped escape / FR coverage:** E4; FR-3 + FR-5 (contract-enumeration ledger) + FR-12 (no-re-greening). The `advisory` semantic-check token is preserved (advisory invariant).

## E5 backtest

- **Scenario:** POST-reflect with dirty `/task` work plus a foreign commit in range, against H4.
- **Steps:** POST-reflect with dirty `/task` work plus a foreign commit in range.
- **Expected outcome:** H4 FAIL closed (wrong surface) until the selector is proven correct — i.e. until `E ∩ true_runtime_surface` is proven correct.
- **Mapped escape / FR coverage:** E5; FR-10 (effective-input proof) + FR-11 (off-path reviewer) + FR-12 (no-re-greening).

## Waiver re-green attempt backtest

- **Scenario:** Waive H1, then run a downstream reflect/adversarial stage and attempt to re-green the verdict.
- **Steps:** Waive H1, then run the downstream reflect/adversarial stage.
- **Expected outcome:** The verdict stays `blocked`/`advisory`; it never upgrades to `pass`. Both `blocked` AND `advisory` are valid non-upgraded states (advisory invariant preserved).
- **Mapped escape / FR coverage:** NFR-4 (no-re-greening durability) / FR-12 (one-way waiver / no-re-greening latch).
