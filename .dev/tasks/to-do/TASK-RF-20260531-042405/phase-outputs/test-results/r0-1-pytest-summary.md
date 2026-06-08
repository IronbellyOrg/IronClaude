# R0.1 Pytest Summary (Step 2.7)

**Date:** 2026-05-31
**Command:** `cd /config/workspace/IronClaude-RoadmapRewrite && uv run pytest tests/roadmap/test_spec_roadmap_id_containment.py tests/roadmap/test_spec_parser.py tests/roadmap/test_spec_fidelity.py -v`
**Raw output:** `r0-1-pytest-output.txt`

## Overall Result

**PASSED** — 71 passed, 10 skipped, 0 failed in 0.22s.

| Metric | Value |
|---|---|
| Total collected | 81 |
| Passed | 71 |
| Skipped | 10 (pre-existing skips, not introduced by R0.1) |
| Failed | 0 |
| Errors | 0 |
| Wall time | 0.22s |

## New Tests (Contract #9 invariant)

All 11 tests in the new `tests/roadmap/test_spec_roadmap_id_containment.py` PASSED.
The Contract #1 invariant (MUST FAIL pre-fix, MUST PASS post-fix) is satisfied:
the new tests reference `superclaude.cli.roadmap.id_registry` and
`gates._roadmap_ids_within_spec`, neither of which exists in the parent
commit (`91095144`), so they cannot collect (let alone pass) without the
R0.1 implementation.

| Test | Result |
|---|---|
| `test_phantom_id_rejected[recurrence_case0]` | PASS — Contract #9 master:§Recurrence #4 case caught |
| `test_registry_contains_method[recurrence_case0]` | PASS — `contains()` API correct |
| `test_spec_ids_contained_when_roadmap_matches_spec` | PASS — anti-regression for clean roadmap |
| `test_accepted_deviation_allows_otherwise_phantom_id` | PASS — accepted deviations widen known set |
| `test_fail_shut_when_sidecar_missing` | PASS — master:§Flaw 4 fail-shut invariant |
| `test_fail_shut_when_sidecar_unreadable` | PASS — fail-shut on OSError |
| `test_extract_roadmap_ids_reuses_canonical_extractor` | PASS — Contract #8 anti-duplication |
| `test_registry_is_immutable_and_hashable` | PASS — frozen dataclass invariant (R1.2 envelope absorption prereq) |
| `test_registry_sidecar_schema_stable` | PASS — sidecar JSON schema contract |
| `test_build_id_registry_picks_up_d_lenient_family` | PASS — documents A12:F-A12-01 asymmetry |
| `test_sidecar_schema_round_trip` | PASS — JSON round-trip lossless |

## Existing Tests (anti-regression)

- `test_spec_parser.py` — all pre-existing tests PASS (no regression introduced by importing into id_registry).
- `test_spec_fidelity.py` — all pre-existing tests PASS (MERGE_GATE additions did not regress).

## Failed Tests

None.

## Contract Assertions Satisfied

- **Contract #1** (MUST FAIL pre-fix / MUST PASS post-fix): new test file imports symbols that do not exist pre-R0.1 — verified.
- **Contract #8** (no duplicate regex literals): `extract_roadmap_ids` and `build_id_registry` BOTH delegate to `spec_parser.extract_requirement_ids`; test `test_extract_roadmap_ids_reuses_canonical_extractor` enforces.
- **Contract #9** (`roadmap_ids ⊆ spec_ids ∪ accepted_deviations`): MERGE_GATE registered `roadmap_ids_within_spec` SemanticCheck; tested with phantom-ID fixture and clean-roadmap anti-regression case.
- **master:§Flaw 4** (no fail-open defaults): `test_fail_shut_when_sidecar_missing` and `test_fail_shut_when_sidecar_unreadable` enforce.
