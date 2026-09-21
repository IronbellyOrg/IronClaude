# Tests-gate input manifest (item 8.5)

WT=`/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/`

## Harness modules (2)

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/_assertions.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/_procedures.py`

## New test files (21)

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_validator_assertions.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_calibrator_assertions.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_producers_enumeration.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_primitivegrep_targeting.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_locus_card.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_verdict_source.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_discriminator_form.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_threshold_bracket.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_cosmetic_counter.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_counter_key.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_hardstop_verdicts.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_headline_threshold.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_timestamp_tolerance.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_inline_fallback_parity.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_calibrator_eval_cases.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_regression_sysbox.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_primitive_differential.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_discriminator_rows.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_behaviour_definition_row.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_menu_equality.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_hc_rename_guard.py`

## Edited existing tests (2)

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_hardening_h1.py`
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/tests/troubleshoot/test_hardening_verdict.py`

## Fixture tree

`find tests/troubleshoot/fixtures -type f` = **125** (not 129).

Delta vs harness §4.1 `88 + 31 + 9 + 1 = 129`:

- assertion fixtures: **88** (matches)
- procedure/counter: **27** landed (producers 2, primitivegrep 2, locus 5, verdict-source 3, discriminator 2, rows 4, differential 1, behaviour 3, tasklist 4, counters 1). Harness §4.1 said 31; the extra 4 were never specified as named files in §4.4.
- regression: **9** + MANIFEST **1** = 10

88 + 27 + 9 + 1 = 125.

## Test totals (item 8.1)

245 passed, 1 known-red (e4), new reds: 0. New cases: 175.
