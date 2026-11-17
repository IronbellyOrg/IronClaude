# Merge Log

Base: variant-3-original.md. Merge date: 2026-11-17. Plan: refactor-plan.md. Output: merged-output.md.

## Changes

| # | Status | Target | Before | After | Provenance |
|---|---|---|---|---|---|
| 1 | Applied | F2 | F2 ended at "fix: point the fixture at @classic." | Appended "tests/review/test_review_cli.py:52-62 and :76 also pin the 4-slot ids and a t1b-1 re-review." | Base (original, modified); Variant 1 F2, C-002 85% |
| 2 | Applied | new F10, placed after F3 | no @default finding | F10 MAJOR non-blocking: deletion removes @default and template_id default; citations panel.py:447-455, test_review_telemetry.py:29 from V1 F3 | Variant 1 F3 per Change #2 |
| 3 | Applied | new F11 | no plugin-mirror finding | F11 MINOR non-blocking: test_review_brief_placement.py:129-134 byte-identity with plugins/ rules file | Variant 1 F5 / V3 advocate per Change #3, C-007 80% |
| 4 | Applied | F4 | F4 MINOR | F4 MAJOR blocking, adds Task 4 line 63 vs Task 5 line 77 contract conflict, unpassable acceptance check | Base (original, modified); Variant 2 F4, X-002 |
| 5 | Applied | new F12 | no tier5a finding | F12 MINOR non-blocking, Necessary deviation: tier5a two models vs source.md:5 | Variant 2 F3 / X-003 per Change #5, C-003 75% |
| 6 | Applied | new F13, F14 | none | F13: --strict-distinct shrinks wonsol (panel.py:647-656); F14: frozen packaged default template option | Advocate A-001 / A-003 per Change #6 |

## Judgment calls (plan gave no value)

- Severity labels for F10 (MAJOR, taken from V1 F3), F11 (MINOR, from V1 F5), F12, F13, F14 (MINOR) were chosen by me because the plan gave only "non-blocking". V2 F3 was MAJOR in its source; I labelled F12 MINOR because the plan adjudicated it non-blocking. Orchestrator may adjust.
- Change 6 has two notes, so it produced two findings (F13, F14).
- F10 sits physically after F3 (plan instruction), so ids are not in file order.
- Citations for F12 (TASK file :29-33) come from V2 F3; F13 and F14 cite only what the plan gave.

## Not made (per plan)

V2 F3 as blocking; V2 F5; V1 F1 golden-values claim; V1 F2 range :91-100.

## Post-merge checks

- Heading structure: PASS. One H1 card heading, no level skips; header lines (persona, model_class, reviewer) kept.
- Internal references: PASS. F2 refers to @classic, F10 to F3 context only; F1..F9 ids intact, F10..F14 unique and sequential; no finding refers to an id that does not exist.
- Citations: PASS. Base citations unchanged; inserted ones copied from source cards or the plan.
- Contradictions: none new. F14 (keep frozen default template) is an alternative to F1's "unless a frozen copy is kept", consistent with it. F10 "keep an alias" is consistent with F14. F4 blocking and F12 non-blocking concern different tasks. F2 "fixture at @classic" is consistent with F10.
