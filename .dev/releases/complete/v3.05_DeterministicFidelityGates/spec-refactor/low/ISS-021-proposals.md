# ISS-021: RunMetadata dataclass is dead within convergence.py

## Status Check
- Superseded by upstream? **NO.** ISS-001 (CRITICAL) reclassifies convergence.py from CREATE to MODIFY and scopes the extension to `execute_fidelity_with_convergence()` and `handle_regression()`. It does not address the RunMetadata dataclass or `begin_run()` internals. ISS-021 remains independent.

## Analysis

The `RunMetadata` dataclass (convergence.py:36-44) defines typed fields that exactly mirror the run metadata fields required by FR-6:
- `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`
- `structural_high_count`, `semantic_high_count`, `total_high_count`

However, `begin_run()` (convergence.py:84-94) constructs run records as raw dicts, ignoring the dataclass entirely. The spec's FR-6 acceptance criteria (line 325) requires these fields but does not prescribe typed vs dict representation.

The spec already describes **Run Metadata** in FR-6 (lines 314-317) as a conceptual requirement. The gap is that the spec doesn't mandate typed run records, so the existing code "complies" with raw dicts while leaving dead code behind.

---

## Proposal A: Add typed run metadata note to FR-6 acceptance criteria

Lightweight: add one acceptance criterion to FR-6 requiring run metadata to use the `RunMetadata` dataclass, which wires the existing dead code into `begin_run()`.

**Before** (FR-6 acceptance criteria, spec line 325):
> - [ ] Registry includes run metadata: run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count

**After**:
> - [ ] Registry includes run metadata: run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count
> - [ ] Run metadata uses a typed dataclass (`RunMetadata`) — not raw dicts — to ensure field presence and type safety at construction time

---

## Proposal B: Remove RunMetadata from spec scope (delete dead code, no spec change)

Since the spec never references `RunMetadata` by name, the fix is purely a code cleanup: delete the dataclass from convergence.py. No spec text changes needed. This can be tracked as an implementation-time cleanup note rather than a spec amendment.

**Before** (spec): No text references RunMetadata.

**After** (spec): No change. Implementation note added to the tasklist or ISS-001 resolution scope: "Delete unused `RunMetadata` dataclass at convergence.py:35-44 during the CREATE-to-MODIFY reclassification."

---

## Recommendation

**Proposal A** is preferred. The `RunMetadata` dataclass already has exactly the right fields for FR-6's run metadata requirements, including the split HIGH counts added by BF-3. Wiring it into `begin_run()` costs one line of spec text and eliminates both the dead-code smell and the type-safety gap in run records. It also aligns with the spec's existing emphasis on typed, structured data (FR-1 findings, FR-6 registry). Deleting useful infrastructure (Proposal B) would just recreate the same need later.
