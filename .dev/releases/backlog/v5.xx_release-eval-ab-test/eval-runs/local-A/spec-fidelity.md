---
high_severity_count: 3
medium_severity_count: 5
low_severity_count: 3
total_deviations: 11
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap references FR-001 through FR-010, NFR-001 through NFR-005, and SC-001 through SC-007, but the spec defines only FR-EVAL-001.1 through FR-EVAL-001.6, NFR-EVAL-001.1 through NFR-EVAL-001.3, and no explicit SC-NNN identifiers at all. The roadmap's requirement numbering scheme is fabricated.
- **Spec Quote**: "FR-EVAL-001.1: Progress File Writer", "FR-EVAL-001.2: CLI Option for Progress File", ..., "FR-EVAL-001.6: Wiring Verification Integration"; "NFR-EVAL-001.1", "NFR-EVAL-001.2", "NFR-EVAL-001.3"
- **Roadmap Quote**: "establishes traceability for FR-001 through FR-010, NFR-001 through NFR-005, SC-001 through SC-007" (Phase 1); "SC-001 through SC-007" (Phase 4, Success Criteria Validation Matrix)
- **Impact**: Traceability is broken. The roadmap claims to cover 10 FRs when the spec defines 6. It claims 5 NFRs when the spec defines 3. It references SC-001 through SC-007 which do not exist in the spec. An implementer following the roadmap's requirement IDs cannot map back to spec requirements.
- **Recommended Correction**: Renumber all roadmap requirement references to match the spec's actual IDs (FR-EVAL-001.1 through FR-EVAL-001.6, NFR-EVAL-001.1 through NFR-EVAL-001.3). Remove phantom FR-007 through FR-010, NFR-004 through NFR-005. Define success criteria explicitly or reference spec acceptance criteria by their FR/NFR IDs.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap references OQ-001, OQ-002, OQ-004, OQ-005 as "open questions" to resolve in Phase 1, but the spec contains no OQ-NNN identifiers. The spec has a single resolved open item (OI-001) and three acknowledged gaps (GAP-001, GAP-002, GAP-003). The roadmap fabricates open questions that don't exist in the spec.
- **Spec Quote**: "~~OI-001~~ ... **Resolved**: wrapped JSON with atomic rewrite" (Section 11); "GAP-002 | Deviation sub-entry schema undefined (intentional for eval) | Medium"; "GAP-003 | 'Significant findings' threshold undefined (intentional for eval) | Medium" (Section 12)
- **Roadmap Quote**: "Resolve **OQ-001**: Define the JSON schema for deviation sub-entries"; "Resolve **OQ-004**: Reconcile overwrite vs. resume contradiction"; "Resolve **OQ-002**: Define 'significant findings' threshold"
- **Impact**: Phase 1 is structured around resolving fabricated OQs. While the underlying issues (GAP-002, GAP-003) are real, OQ-004 (overwrite vs. resume) and OQ-005 (metadata key conventions) have no spec basis. An implementer would search the spec for these IDs and find nothing.
- **Recommended Correction**: Replace OQ-001 with GAP-002, OQ-002 with GAP-003. Remove OQ-004 and OQ-005 as they address concerns not raised in the spec. If overwrite/resume behavior needs clarification, cite the actual spec text (FR-EVAL-001.2 acceptance criterion: "If progress file already exists, it is overwritten").

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: The roadmap introduces a resume/append behavior for `--resume` mode (OQ-004 resolution) that directly contradicts the spec. The spec explicitly states overwrite-only semantics, and the spec's integration test `test_resume_preserves_progress` is the only reference to resume behavior — but this is a test plan item, not a functional requirement. The roadmap elevates this to a first-class behavioral mode.
- **Spec Quote**: FR-EVAL-001.2 Acceptance Criteria: "If progress file already exists, it is overwritten (not appended to)"
- **Roadmap Quote**: "Resolve **OQ-004**: Reconcile overwrite vs. resume contradiction. Recommended: treat as two distinct modes — fresh run overwrites, `--resume` appends."
- **Impact**: Implementing the roadmap's dual-mode behavior would violate the spec's explicit overwrite-only acceptance criterion. The spec's test plan does mention `test_resume_preserves_progress` which suggests resume appending, but the FR is unambiguous about overwrite semantics.
- **Recommended Correction**: Follow the spec's FR-EVAL-001.2 acceptance criterion (overwrite). If the spec's test plan item `test_resume_preserves_progress` is desired, it should be flagged as a spec inconsistency for the spec author to resolve, not silently adopted.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap does not reproduce the spec's data model signatures. The spec defines exact `StepProgress` and `PipelineProgress` dataclass definitions with specific field names and types. The roadmap mentions these classes but only partially lists fields in prose.
- **Spec Quote**: Section 4.5: `@dataclass class StepProgress: step_id: str; status: str; duration_ms: int; gate_verdict: Optional[str]; output_file: Optional[str]; metadata: dict = field(default_factory=dict)`; `@dataclass class PipelineProgress: spec_file: str; started_at: str; steps: list[StepProgress] = field(default_factory=list); completed: bool = False`
- **Roadmap Quote**: Phase 2, Key Action 1: "`StepProgress` dataclass: `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`, `metadata` (dict)" and "`PipelineProgress` container with `list[StepProgress]` and `to_json()` serialization"
- **Impact**: The roadmap omits `PipelineProgress.spec_file`, `PipelineProgress.started_at`, and `PipelineProgress.completed` from its Phase 2 description. An implementer following only the roadmap could miss these fields.
- **Recommended Correction**: Include the full dataclass signatures from spec Section 4.5 verbatim in the roadmap's Phase 2 data model task.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: The spec defines a 5-step implementation order (Section 4.6) while the roadmap reorganizes into 4 phases with different groupings and adds a Phase 1 that has no spec basis.
- **Spec Quote**: Section 4.6: "1. Create progress.py ... 2. Add --progress-file option ... Add summary() to gate constants ... 3. Wire progress callback into executor.py ... 4. Enrich --dry-run output ... 5. Add deviation sub-reporting in convergence loop"
- **Roadmap Quote**: "Phase 1 — Requirements Closure and Architectural Alignment" (no spec equivalent); Phase 2 combines spec steps 1-3; Phase 3 combines spec steps 2(partial), 4-5 plus wiring/remediation
- **Impact**: The roadmap's phasing differs from the spec's prescribed implementation order. Phase 1 is entirely additive (requirements closure). While this may be beneficial, it deviates from what the spec prescribes. The parallelism noted in spec step 2 is preserved but relocated.
- **Recommended Correction**: Either follow the spec's 5-step implementation order directly or explicitly justify the reordering. Phase 1 should be flagged as an additive roadmap concern, not a spec requirement.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: The spec's Section 4.4 module dependency graph shows `progress.py` depending on `models.py` and `gates.py`, with no dependency from `progress.py` to `convergence.py` or `wiring_gate.py`. The roadmap lists `convergence.py` and `wiring_gate.py` as "cross-module read points" in the executive summary, implying `progress.py` has a dependency on them.
- **Spec Quote**: Section 4.4: "commands.py ──> executor.py ──> progress.py (new) ... progress.py depends on models.py; executor.py depends on gates.py which depends on audit/wiring_gate.py"
- **Roadmap Quote**: "one new module (`progress.py`), three modified modules (`executor.py`, `commands.py`, `gates.py`), and two cross-module read points (`convergence.py`, `wiring_gate.py`)"
- **Impact**: If `progress.py` directly imports from `convergence.py` or `wiring_gate.py`, the dependency graph would violate the spec's architecture. The spec intends metadata to flow through `executor.py` callbacks, not through direct imports in `progress.py`.
- **Recommended Correction**: Clarify that `convergence.py` and `wiring_gate.py` are read points for `executor.py`, not for `progress.py`. The progress module should only depend on `models.py` and `gates.py` per the spec's dependency graph.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: The spec's Section 10 (Downstream Inputs) specifies "1 validation milestone per 2 work milestones" (interleave ratio 1:2) for MEDIUM complexity. The roadmap uses a 4-phase structure with 1 requirements phase, 2 work phases, and 1 validation phase — an effective 1:2:1 ratio, not 1:2.
- **Spec Quote**: Section 10: "Complexity MEDIUM maps to interleave ratio 1:2 (1 validation milestone per 2 work milestones)"
- **Roadmap Quote**: Phase structure: Phase 1 (requirements), Phase 2 (work), Phase 3 (work), Phase 4 (validation) — 1 validation per 2 work, but Phase 1 is neither work nor validation.
- **Impact**: Minor structural mismatch. The interleave ratio is approximately correct if Phase 1 is excluded from the count, but the spec's guidance implies a simpler milestone structure.
- **Recommended Correction**: Either restructure to match the spec's milestone guidance more closely or note the deviation as an intentional enrichment.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: The spec explicitly states the feature is "Single phase, can be implemented in one sprint" (Section 10), but the roadmap breaks it into 4 phases spanning 5-8.5 working days.
- **Spec Quote**: Section 10, For sc:roadmap: "Milestone: Single phase, can be implemented in one sprint"
- **Roadmap Quote**: "Total estimated duration: 5–8.5 working days" across 4 phases
- **Impact**: The roadmap's multi-phase structure contradicts the spec's single-phase guidance. While the roadmap's phasing may be more realistic, it represents a deviation from the spec author's intent regarding implementation scope.
- **Recommended Correction**: Either consolidate into a single sprint/phase as the spec directs, or explicitly acknowledge the deviation from the spec's single-phase guidance with justification.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: The spec defines the CLI option type as `click.Path` in Section 5.1. The roadmap also uses `click.Path` but does not mention whether `exists=False` or `dir_okay=False` constraints should be applied, while the spec's acceptance criteria imply parent directory validation.
- **Spec Quote**: Section 5.1: "`--progress-file` | `click.Path` | `{output_dir}/progress.json`"; FR-EVAL-001.2: "Option is validated before pipeline starts (parent directory must exist)"
- **Roadmap Quote**: Phase 2 Key Action 3: "Add `--progress-file` as `click.Path` option"; Key Action 4: "Add path validation: parent directory must exist; fail fast before pipeline starts"
- **Impact**: Minimal — the roadmap does capture the parent directory validation requirement but doesn't specify Click parameter constraints.
- **Recommended Correction**: No action needed; this is a level-of-detail difference.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: The spec's test plan (Section 8) defines specific test names and file locations. The roadmap's Phase 4 validation describes equivalent tests but uses different names (SC-001 through SC-007 labels rather than the spec's test names).
- **Spec Quote**: Section 8.1: "`test_step_progress_serialization`", "`test_pipeline_progress_append`", "`test_gate_summary_all_steps`"; Section 8.2: "`test_dry_run_includes_gate_table`", "`test_full_pipeline_produces_progress`", "`test_resume_preserves_progress`"
- **Roadmap Quote**: Phase 4: "SC-001: End-to-end CLI eval", "SC-002: Crash-safety eval", "SC-003: Dry-run eval", etc.
- **Impact**: Test naming mismatch is cosmetic but could cause confusion if someone tries to cross-reference.
- **Recommended Correction**: Reference the spec's test names alongside the roadmap's SC labels.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: The spec's Section 4.2 (Modified Files) lists exactly 3 files. The roadmap's executive summary mentions "two cross-module read points (`convergence.py`, `wiring_gate.py`)" implying modifications, but the spec lists these as dependency targets, not modified files.
- **Spec Quote**: Section 4.2: Modified Files table lists only `executor.py`, `commands.py`, `gates.py`
- **Roadmap Quote**: "two cross-module read points (`convergence.py`, `wiring_gate.py`)"
- **Impact**: If the roadmap implies modifying `convergence.py` or `wiring_gate.py`, that exceeds the spec's modification surface. The spec's FR-EVAL-001.4 dependency on `convergence.py` suggests reading from it, not modifying it.
- **Recommended Correction**: Clarify whether `convergence.py` and `wiring_gate.py` require modifications. If so, add them to the modified files list. If not, clarify "read points" means data is consumed, not that files are changed.

---

## Summary

**Severity Distribution**: 3 HIGH, 5 MEDIUM, 3 LOW (11 total)

The three HIGH-severity deviations are:
1. **Fabricated requirement IDs** — The roadmap uses FR-001 through FR-010, NFR-001 through NFR-005, and SC-001 through SC-007, none of which exist in the spec. Traceability is broken.
2. **Fabricated open questions** — The roadmap invents OQ-001 through OQ-005 when the spec only has OI-001 (resolved), GAP-002, and GAP-003.
3. **Resume/append contradiction** — The roadmap introduces dual-mode overwrite/append behavior that directly contradicts the spec's explicit overwrite-only acceptance criterion.

The MEDIUM deviations center on structural differences: incomplete data model reproduction, reordered implementation phases, ambiguous dependency boundaries, and a multi-phase structure contradicting the spec's single-sprint guidance.

**Verdict**: The roadmap is **not tasklist-ready** due to 3 HIGH-severity deviations. The fabricated ID schemes must be corrected to restore traceability, and the resume behavior contradiction must be resolved before implementation can proceed.
