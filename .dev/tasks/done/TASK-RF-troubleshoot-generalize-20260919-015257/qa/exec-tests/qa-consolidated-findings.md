# Tests-gate consolidated findings (item 9.9)

**Date:** 2026-09-20
**cycle:** 1
**Consolidated verdict:** FAIL
**|F_1| = 2** (in-scope only)
**PASS_1:** [internal-consistency, evidence-quality, hc-guard-lint]

10 lens reports present.

## In-scope findings (fix here)

| id | Severity | Location | Issue | Required fix | Lenses |
|---|---|---|---|---|---|
| F-T1 | IMPORTANT | test_regression_sysbox.py:31 | parametrize missing `ids=` | add ids=["GLM-RUN2","Fable-D3","Astra-A3"] | template-conformance, completeness |
| F-T2 | MINOR | test_menu_equality.py | no `FIX` Path idiom | `FIX = Path(__file__).parent / "fixtures"` | template-conformance |

## Out-of-scope / authorized (Follow-Up, do not fix)

- Astra EXPECTED_IDS {A1,A10} vs harness §5.2 {A10} — task item 7.48 F-C1 authorized.
- E501 in _assertions.py — project ruff ignores E501.
- Extra A6 numeric/quoted-path twins — fixtures are harness-verbatim; inventing bodies is forbidden.
- Overdetermined pos/neg twins — harness fixture design.
- Cosmetic [5,14,19] vs SKILL 5/10/15 — harness §4.4 pins the test vector.
- Predicate vs expanded agent-assertions trigger prose — T13 compares trigger text; predicates are harness §1.2 proxies.
- T4/T8/T12 R-item docstring labels — cosmetic; tests cover the T-table rows.
- `_HEADLINE_SECTIONS` unused helper — not required for evaluators.
- 125 vs 129 fixture files — 4 phantom procedure files never named in §4.4.

## Applied in cycle 1 (executor, item 9.10)

F-T1 and F-T2 applied in worktree.
