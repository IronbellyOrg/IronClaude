# Area E Aggregation Report — Step PG6.1

**Aggregated:** 2026-06-03 21:06 · Branch `integration`

## Discovered files (4)

| File | One-line summary |
|------|------------------|
| `phase-outputs/plans/area-e1-registry-removal-PENDING.md` | e1 HALT: registry-writer removal blocked on cutover (0/3) AND the live JSON-file reader; Contract #9 reader-repoint prereq documented. |
| `phase-outputs/plans/area-e2-remediate-parser-PENDING.md` | e2 HALT/DEFERRED: `remediation` step 0/3; parser has 0 prod callers but 3 test callers + cutover-deferred. |
| `phase-outputs/test-results/area-e3-mdfamily-verify.txt` | e3 raw output: 187 passed, 1 skipped; `test_all_schemas_accept_md_family` present (4 params). |
| `phase-outputs/test-results/area-e3-mdfamily-summary.md` | e3 summary: MD-family guard green, no residual drift, shims preserved. |

## Four mandated assertions

**(i) e1 registry-writer removal HALTED with Contract #9 reader-repoint prerequisite documented — YES.** The e1 marker records HALT on two grounds: (a) cutover NOT-MET (all 13 steps 0/3); (b) the live MERGE_GATE reader `gates.py:_roadmap_ids_within_spec` STILL reads the `spec_id_registry.json` sidecar FILE (`_id_registry_sidecar_path.read_text()`, ~L1021) and fails closed — the `envelope.spec_ids` repoint never landed. Prerequisite documented: repoint the reader to `envelope.spec_ids` using `verify_implementation.py:assert_all_frs_resolved` (`envelope.spec_ids.fr_ids` accessor) as the template, THEN earn ≥3 parity cycles, THEN the writer may be removed.

**(ii) e2 `remediate_parser.py` deletion HALTED/DEFERRED — YES.** The e2 marker records `remediation` at 0/3 (`cutover_eligible: false`); `remediate_parser.py` has ZERO production callers in `src/` (the two `remediate.py` mentions are docstring/comment only, not imports/calls) but is cutover-deferred and 3 test files still call it (`test_remediate_parser.py`, `test_pipeline_integration.py`, `test_phase7_hardening.py`). Deletion requires retargeting those 3 + meeting the ≥3-cycle precondition. HALTED.

**(iii) e3 MD-family guard tests pass with no residual drift; back-compat shims NOT removed — YES.** `test_all_schemas_accept_md_family` (params extract/extract_tdd/generate/merge) passed; 6-file MD-family suite → 187 passed, 1 skipped, 0 failed → no residual drift. The `.get(..., ())` back-compat shims in `envelope.py`/`gates.py` were explicitly DEFERRED and NOT removed.

**(iv) NO production code deleted or modified in this phase — YES.**
- `gates.py` (reader): `git diff HEAD --stat` → empty (untouched).
- `executor.py` (writer `_save_id_registry`): not modified by Area E (only the prior Area B+C hunks exist); the writer is intact.
- `remediate_parser.py`: still **EXISTS** on disk; `git diff` → empty (untouched).
- The 3 calling test files were not deleted/retargeted; the back-compat shims were not removed.

All statements backed by the marker/summary files + `git diff` + filesystem evidence with no fabrication.
