# pytest tests/troubleshoot/ (item 8.1)

Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize`
Date: 2026-09-20

## Overall

- Result: **PASS** (known-red only)
- Collected/total: 246
- Passed: 245
- Failed: 1
- Skipped: 0

## Pytest summary line

```
1 failed, 245 passed in 15.10s
```

## Failing tests

| Node id | Error type | Brief message |
|---|---|---|
| `tests/troubleshoot/backtest/test_backtest_e4.py::test_backtest_e4_new_gate_catches_via_contract_enumeration_ref` | AssertionError | H2 ref must require BOTH `gate_passed` AND `_evaluate_gate` consumers be classified |

## Per-file pass counts (21 new files)

| File | Passed |
|---|---|
| test_validator_assertions.py | 47 |
| test_calibrator_assertions.py | 46 |
| test_producers_enumeration.py | 2 |
| test_primitivegrep_targeting.py | 1 |
| test_locus_card.py | 6 |
| test_verdict_source.py | 3 |
| test_discriminator_form.py | 2 |
| test_threshold_bracket.py | 3 |
| test_cosmetic_counter.py | 1 |
| test_counter_key.py | 1 |
| test_hardstop_verdicts.py | 4 |
| test_headline_threshold.py | 2 |
| test_timestamp_tolerance.py | 3 |
| test_inline_fallback_parity.py | 3 |
| test_calibrator_eval_cases.py | 35 |
| test_regression_sysbox.py | 3 |
| test_primitive_differential.py | 3 |
| test_discriminator_rows.py | 4 |
| test_behaviour_definition_row.py | 3 |
| test_menu_equality.py | 2 |
| test_hc_rename_guard.py | 1 |
| **new total** | **175** |

known-red: 1 (test_backtest_e4), new reds: 0
