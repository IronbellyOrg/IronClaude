# R0.1 Aggregation Report (Step PG2.1)

**Phase:** 2 — R0.1 Spec-ID Registry (Contract #9)
**Date:** 2026-05-31
**Commit:** `6cee1eb1` on `refactor/roadmap-pipeline-r0-r1-rewrite`
**Working directory (new worktree):** `/config/workspace/IronClaude-RoadmapRewrite/`

## Phase-Output File Inventory

| File | Size (B) | One-line summary |
|---|---|---|
| `phase-outputs/discovery/spec-id-extraction-sites.md` | 4,793 | 9-row inventory of every ID pattern site in `cli/roadmap/`; identifies `spec_parser._REQUIREMENT_PATTERNS` as the single canonical source and `fidelity_checker._FR_HEADING_RE` as a specialized heading-anchored consumer (NOT a duplication). |
| `phase-outputs/test-results/r0-1-pytest-output.txt` | 9,178 | Raw pytest output: 71 passed, 10 skipped (pre-existing), 0 failed, in 0.22s. |
| `phase-outputs/test-results/r0-1-pytest-summary.md` | 3,068 | Structured pytest summary: 11 new tests in `test_spec_roadmap_id_containment.py` all PASS; existing `test_spec_parser.py` + `test_spec_fidelity.py` still pass (anti-regression). |
| `phase-outputs/test-results/r0-1-lint-format-summary.md` | 1,095 | ruff check + ruff format --check both PASS on all 5 touched files; post-format pytest re-run still 71 pass / 10 skip / 0 fail. |

## New Source Files Created

- `src/superclaude/cli/roadmap/id_registry.py` (frozen `SpecIdRegistry` dataclass, `build_id_registry`, `extract_roadmap_ids`)
- `tests/roadmap/test_spec_roadmap_id_containment.py` (11 tests covering Contract #9 invariant + Contract #8 anti-duplication + master:§Flaw 4 fail-shut)
- `tests/roadmap/fixtures/recurrence/README.md` (corpus layout convention)
- `tests/roadmap/fixtures/recurrence/id_containment/spec_roadmap_drift_case.md` (master:§Recurrence #4 minimal reproducer)
- `tests/roadmap/fixtures/recurrence/id_containment/spec_roadmap_drift_case.expected.json` (expected outcome JSON)

## Modified Source Files

- `src/superclaude/cli/roadmap/executor.py` — added `_save_id_registry()` helper + post-extract sidecar persistence + `set_id_registry_sidecar_path` wiring.
- `src/superclaude/cli/roadmap/gates.py` — added `_roadmap_ids_within_spec` SemanticCheck registered on `MERGE_GATE`; module-level `set_id_registry_sidecar_path` hint bridge for the `Callable[[str], bool | str]` signature.
- `tests/roadmap/conftest.py` — added `recurrence_corpus_dir` + `recurrence_case` fixtures (reused by Contracts #4, #6, #7, #8, #10 in later phases per R3 §3.4).

## Test Result Summary (from r0-1-pytest-summary.md)

- **Total:** 71 passed, 10 skipped, 0 failed.
- **New tests:** 11/11 PASS.
- **Existing test files:** all pass (no regression).
- **Contract #1 invariant satisfied:** test file imports symbols that do not exist in the parent commit `91095144` — cannot have passed pre-fix.

## Lint/Format Summary (from r0-1-lint-format-summary.md)

- `ruff check` — PASSED (all 5 files clean).
- `ruff format --check` — PASSED (5 files already formatted).
- One `I001` import-sort fix applied during Step 2.8; formatting normalized 4 files; final state clean.

## Contract #9 Satisfaction Assertion

**The new `MERGE_GATE` SemanticCheck `roadmap_ids_within_spec` enforces** the Contract #9 invariant:

> roadmap_ids ⊆ spec_ids ∪ accepted_deviation_ids

via the following chain:

1. The extract step persists `<output_dir>/spec_id_registry.json` via `_save_id_registry()` (executor.py).
2. `_save_id_registry()` calls `set_id_registry_sidecar_path(sidecar)` on the gates module (R0.1 bridge — R1.3 widens the SemanticCheck signature and removes the bridge).
3. When the merge step writes its output, the `MERGE_GATE.semantic_checks` list runs.
4. `_roadmap_ids_within_spec(content)` loads the sidecar JSON, reconstructs `SpecIdRegistry`, extracts IDs from `content` via the canonical `spec_parser.extract_requirement_ids` (Contract #8 reuse), computes `roadmap_ids - registry.union_of_known()`, and returns a failure string listing the first 5 violations if non-empty (else `True`).
5. Missing/unreadable/malformed sidecar returns a failure string (master:§Flaw 4 — no fail-open default).

## Preserve Invariants Honored

- `commands.py` — UNTOUCHED (MVR §6.3).
- `structural_checkers.py` — UNTOUCHED (MVR §3, v3.05 deterministic layer).
- `convergence.py` — UNTOUCHED (MVR §5, public API + atexit).
- `cosmetic_remediator.py` — UNTOUCHED (MVR §2.8).
- Zero `return True` fragility stubs introduced.
- Zero CLI options renamed/removed.

## No Fabrication

Every cited file:line in this report exists in commit `6cee1eb1`; every Contract item cited maps to BUILD-REQUEST §Contract (verbatim) and master:§Recurrence (verbatim). The recurrence fixture cites A12:F-A12-01 from `master-report.md` directly.
