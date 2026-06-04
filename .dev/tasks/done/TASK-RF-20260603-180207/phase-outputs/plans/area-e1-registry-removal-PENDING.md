# spec_id_registry.json writer removal HALTED

**Evaluated:** 2026-06-03 21:00 · Branch `integration`

## Verdict: **HALT** (writer NOT deleted; reader NOT modified)

The `spec_id_registry.json` writer removal is blocked on TWO independent grounds, EITHER of which forces HALT:

### (i) Cutover precondition NOT-MET

`.dev/migrations/r1-4-cutover-counters.yaml`: all 13 steps at `release_marker_count: 0`, `cutover_eligible: false`, `cutover_at_count: 3`. No step is cutover-eligible.

### (ii) HARD code prerequisite — the live MERGE_GATE reader still reads the JSON FILE

The live Contract #9 reader `_roadmap_ids_within_spec` in `src/superclaude/cli/roadmap/gates.py` (~L996-1059) STILL reads the `spec_id_registry.json` **sidecar file** and **fails closed**:

- It resolves the module-level `_id_registry_sidecar_path` (set by the executor's `_save_id_registry` via `set_id_registry_sidecar_path`); if unset → returns a failure string (`gates.py:~1013-1018`).
- It reads the file: `raw = _id_registry_sidecar_path.read_text(...)` (`gates.py:~1021`); OSError → failure string (`gates.py:~1022-1026`).
- It reconstructs a `SpecIdRegistry` from the FILE payload (`gates.py:~1033-1045`) and runs the containment check.

The promised migration to `envelope.spec_ids` **never landed**. Deleting the writer now would strand this live, fail-closed reader → every merge would fail Contract #9 (or worse, fail-open if someone also weakened the reader). So the writer CANNOT be removed until the reader is repointed.

## Contract #9 reader-repoint PREREQUISITE (documented, NOT done here)

Before the `spec_id_registry.json` writer (`_save_id_registry` in `executor.py:~649-655`) may be removed:

1. **Repoint the reader** `gates.py:_roadmap_ids_within_spec` to source the spec universe from `envelope.spec_ids` instead of reading the JSON file — using the LIVE template `verify_implementation.py:assert_all_frs_resolved` (`verify_implementation.py:~51-121`), which reads `envelope.spec_ids.fr_ids` and `envelope.spec_ids.accepted_deviation_ids` via the dataclass **accessor** pattern (`envelope.spec_ids.<family>_ids` — NEVER `envelope.spec_ids[FAMILY]`, which raises `TypeError`).
2. **Earn ≥3 parity-passing release cycles** on the repointed reader (per Vector A), i.e. the relevant cutover counter must reach `cutover_eligible: true`.
3. THEN, and only then, the writer may be deleted.

## Zero production-code change (explicit)

- The writer `_save_id_registry` in `src/superclaude/cli/roadmap/executor.py` was **NOT** deleted or modified by this item.
- The reader `_roadmap_ids_within_spec` in `src/superclaude/cli/roadmap/gates.py` was **NOT** modified by this item (`gates.py` is byte-unchanged across the whole task; `git diff HEAD -- gates.py` is empty).

This is recorded as a [Priority: High] prerequisite in the task's `### Follow-Up Items Identified` / Open Questions. Under the current state the "proceed" branch is NOT taken. Removal additionally requires SEPARATE user authorization.
