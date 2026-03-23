---
high_severity_count: 0
medium_severity_count: 5
low_severity_count: 3
total_deviations: 8
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: MEDIUM
- **Deviation**: Roadmap Phase 3 Gate C covers SC-4 (≥70% structural), but SC-4 validation is listed under Phase 4 exit criteria ("≥70% of findings have severity determined by structural rules (SC-4)") and Phase 6. The spec ties SC-4 to the structural/semantic split which spans FR-1 through FR-4 — assigning Gate C to SC-4 is premature since the semantic layer (Phase 4) hasn't been built yet at Phase 3 exit.
- **Spec Quote**: "SC-4: ≥70% findings from structural rules" (Success Criteria table)
- **Roadmap Quote**: "Gate C — Registry Certified" (Phase 3 header) and "SC-4: ≥70% findings from structural rules" listed under Phase 4 exit criteria with Gate C, then again under Phase 6 with Gate E/F
- **Impact**: Gate C assignment for SC-4 is inconsistent — the structural/semantic ratio can only be measured after Phase 4 delivers the semantic layer. Phase 4 exit criteria correctly note this but assign Gate C which closes at Phase 3.
- **Recommended Correction**: Assign SC-4 validation to Gate D (Phase 5) or Gate F (Phase 6) only. Remove SC-4 from Gate C scope.

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Spec defines `_DIFF_SIZE_THRESHOLD_PCT` change from 50 to 30 as a specific delta item, but roadmap does not explicitly call out modifying this constant — it only mentions the new per-patch 30% threshold behavior.
- **Spec Quote**: "`MODIFY _DIFF_SIZE_THRESHOLD_PCT: 50 → 30` | ISS-004, BF-5" and "`_DIFF_SIZE_THRESHOLD_PCT = 50` | line 45 | Exists — MUST change to 30 (ISS-004/BF-5)"
- **Roadmap Quote**: "Per-patch diff-size guard: reject if `changed_lines / patch_original_lines > 30%` (NFR-5)" and "`_check_diff_size()` retired; replaced by per-patch evaluation"
- **Impact**: The roadmap implies the old constant is retired along with `_check_diff_size()`, but doesn't explicitly state modification of `_DIFF_SIZE_THRESHOLD_PCT`. An implementer could create a new constant rather than modifying the existing one, or miss the ISS-004/BF-5 traceability.
- **Recommended Correction**: Add explicit task in Milestone 6.1: "Modify `_DIFF_SIZE_THRESHOLD_PCT` from 50 to 30 (ISS-004/BF-5) or replace with new per-patch constant."

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Spec defines `deviation_registry.py` removal from manifest (`REMOVE_FROM_MANIFEST` action in frontmatter). Roadmap does not mention this cleanup action.
- **Spec Quote**: "file: src/superclaude/cli/roadmap/deviation_registry.py / action: REMOVE_FROM_MANIFEST / note: 'Class exists inside convergence.py:50-225, no separate file'"
- **Roadmap Quote**: [MISSING]
- **Impact**: Minor manifest/documentation hygiene issue. If `deviation_registry.py` is referenced in any manifest or import list, it would remain as a stale reference.
- **Recommended Correction**: Add task to Milestone 6.4 (Dead Code Removal): "Remove `deviation_registry.py` from any manifest files (class lives in convergence.py)."

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Spec defines an open question numbering that includes OQ-5b ("FR-4.1 threshold calibration basis"), but roadmap lists only OQ-1 through OQ-5 and subsumes OQ-5b into OQ-1.
- **Spec Quote**: N/A — OQ-5b is implicit from the debate rubric calibration risk note in FR-4.1
- **Roadmap Quote**: "OQ-1 | FR-4.1 rubric threshold (0.15) calibration against real corpus" and Milestone 6.6 lists "Document FR-4.1 threshold calibration basis (OQ-5b)" separately
- **Impact**: Milestone 6.6 references OQ-5b but the Open Question Risks table does not define it. An implementer may be confused about whether OQ-5b is a separate question or part of OQ-1.
- **Recommended Correction**: Either add OQ-5b to the Open Question Risks table or merge the Milestone 6.6 reference into OQ-1 explicitly.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Spec's `RunMetadata` dataclass is specified to be typed (not raw dicts), but roadmap does not explicitly mention the typed `RunMetadata` requirement in Phase 3 Milestone 3.1 where run metadata is implemented.
- **Spec Quote**: "Run metadata uses a typed dataclass (`RunMetadata`) — not raw dicts — to ensure field presence and type safety at construction time" (FR-6 acceptance criteria)
- **Roadmap Quote**: "Add run metadata: `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`, `structural_high_count`, `semantic_high_count`, `total_high_count`" (Milestone 3.1)
- **Impact**: The `RunMetadata` dataclass is defined in Phase 1 Milestone 1.3, but the Milestone 3.1 task wording doesn't explicitly require using it (could be implemented as raw dicts). Phase 1 defines it, Phase 3 should consume it.
- **Recommended Correction**: Add to Milestone 3.1: "Run metadata stored as `RunMetadata` dataclass instances (defined in Phase 1) — not raw dicts."

### DEV-006
- **ID**: DEV-006
- **Severity**: LOW
- **Deviation**: Spec references `budget_snapshot: dict | None = None` as an optional `RunMetadata` field (FR-10), but roadmap only mentions "ledger snapshot in convergence mode" without specifying the field name or type.
- **Spec Quote**: "Optional `RunMetadata` field: `budget_snapshot: dict | None = None` containing `budget_consumed`, `budget_reimbursed`, and `budget_available` integer values."
- **Roadmap Quote**: "Run metadata includes ledger snapshot in convergence mode" (Milestone 3.2)
- **Impact**: Minor detail omission — the field name and type are defined in Phase 1's data model extension (Milestone 1.3 covers `RunMetadata`), so implementers would find it there. No functional gap.
- **Recommended Correction**: No action required — Phase 1 data model definition covers this. Optionally add field name to Milestone 3.2 for clarity.

### DEV-007
- **ID**: DEV-007
- **Severity**: LOW
- **Deviation**: Roadmap uses "OQ-3" for "Agent failure definition" but also references "OQ-3" for "ParseWarning handling" in the Open Question Risks table and Milestone 6.6, creating an ID collision.
- **Spec Quote**: N/A (open questions are roadmap-defined)
- **Roadmap Quote**: "OQ-2 | ParseWarning severity policy" and "OQ-3 | Agent failure definition in FR-8" in the table, but Milestone 6.6 lists "Document ParseWarning handling decision: log-and-continue vs. block (OQ-3)"
- **Impact**: Milestone 6.6 assigns OQ-3 to ParseWarning handling, but the Open Question Risks table assigns OQ-3 to agent failure definition and OQ-2 to ParseWarning. Internal inconsistency within the roadmap.
- **Recommended Correction**: Fix Milestone 6.6 to reference OQ-2 for ParseWarning handling.

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: Spec lists `spec_patch.py` as a preserved coexisting module, but roadmap does not mention it at all.
- **Spec Quote**: "Preserved and coexisting: `spec_patch.py` (the accepted-deviation workflow) operates in both legacy and convergence modes."
- **Roadmap Quote**: [MISSING]
- **Impact**: No functional impact — the spec explicitly states v3.05 does not modify `spec_patch.py`. Its absence from the roadmap is consistent with "no work needed," but a brief mention would confirm the coexistence was considered.
- **Recommended Correction**: Optionally add a note in Phase 5 or Phase 6 confirming `spec_patch.py` coexistence is verified (no modifications needed).

---

## Summary

**Severity distribution**: 0 HIGH, 5 MEDIUM, 3 LOW (8 total)

The roadmap is a faithful and comprehensive translation of the specification. No functional requirements are omitted, no architectural constraints are violated, and no signatures or data models are contradicted. The five MEDIUM deviations are:

1. **Gate assignment inconsistency** (SC-4 assigned to Gate C before semantic layer exists)
2. **Missing explicit constant modification** (`_DIFF_SIZE_THRESHOLD_PCT` change not called out)
3. **Missing manifest cleanup** (`deviation_registry.py` REMOVE_FROM_MANIFEST action)
4. **Open question numbering gap** (OQ-5b referenced but not defined in table)
5. **Typed dataclass requirement not restated** at consumption point (RunMetadata)

All are addressable with minor roadmap edits. The roadmap is **tasklist-ready** — none of these deviations risk incorrect implementation if the spec is used as the authoritative reference alongside the roadmap.
