# Phase 2 Output Summary Manifest (Step GA.1)

Phase 2 = FX3 (field-resolution AST test) + FX5 (gate-helper coverage collector).
All artifacts under the pr209-harden worktree.

## Code/test artifacts (the Gate-A review targets)

| Path | Bytes | Purpose |
|------|-------|---------|
| `tests/pr_submit/test_setup_questions_resolution.py` | 10035 | FX3 — AST-introspects questions.py; asserts every deriver literal ⊆ SetupAnswers/EvidenceBundle fields (4 tests, subset direction, dynamic field sets, Constant-arg guard). |
| `tests/pr_submit/test_gate_helper_differentials.py` | 24292 | FX5 — negative + differential (mutation-must-fail) pairs for all 11 enforced helpers (22 tests); defines `HELPER_TEST_MAP`. |
| `tests/pr_submit/test_gate_helper_coverage.py` | 1248 | FX5 — parametrized coverage test (`test_gate_helper_has_negative_and_differential`), one reported id per registered helper. |
| `tests/pr_submit/conftest.py` | 10198 | FX5 — appended `GATE_LOAD_BEARING_HELPERS` registry, `GATE_HELPER_DEF_PATTERN`, `pytest_generate_tests` hook, existence/coverage/drift-alarm assertions, `assert_gate_helper_coverage` fixture. Existing 5 fixtures preserved byte-for-byte. |

## Discovery inventories
- `phase-outputs/discovery/fx3-questions-inventory.md` — 8 `_answer_default` literals + 2 `_evidence_attr` pairs, 17 SetupAnswers fields, 13 EvidenceBundle attrs, F3 trap, subset-direction note.
- `phase-outputs/discovery/fx5-gate-helper-registry.md` — 11-helper enforced registry (9 drift-alarm-matched + 2 hand-registered), the invariant, the pattern reconciliation (resolution (ii)), F4 anchor chain, residual-risk non-goals.
- `phase-outputs/discovery/baseline-confirm.md` — audit base = HEAD = merge-base = 46a787da.

## Test-results
- `phase-outputs/test-results/fx3-summary.md` — FX3: 4/4 PASSED.
- `phase-outputs/test-results/fx3-fx5-summary.md` — full `tests/pr_submit/`: 311 passed, 6 pre-existing failures (missing untracked `offer-pr-review.sh` hook, unrelated to FX3/FX5); FX3 (4) + FX5 diff (22) + FX5 coverage (11) + 80 contract_setup all green.
- `phase-outputs/test-results/fx3-fx5-ruff.txt` — `ruff check` PASS + `ruff format --check` PASS (after scoped format of the 2 flagged files).

## Recorded verdicts
- **FX3 pytest:** PASSED (4/4).
- **FX5 pytest:** PASSED (22 differential + 11 per-helper coverage, each helper its own green id).
- **pr_submit regression:** none — all 80 pre-existing `test_contract_setup_*` green; the 6 failures are a pre-existing environmental gap (untracked hook script), not caused by the conftest additions.
- **ruff check + format-check:** both exit 0 (scoped to the 4 changed files).

Every file discovered is listed; recorded verdicts match the test-results summaries. No fabrication.
