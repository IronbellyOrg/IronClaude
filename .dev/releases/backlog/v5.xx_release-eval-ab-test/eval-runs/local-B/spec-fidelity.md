---
high_severity_count: 3
medium_severity_count: 5
low_severity_count: 4
total_deviations: 12
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap references `StepResult` in `cli/pipeline/models.py` but spec states dependency is `src/superclaude/cli/roadmap/models.py`
- **Spec Quote**: "Dependencies: `src/superclaude/cli/roadmap/executor.py` (`execute_pipeline` callback), `src/superclaude/cli/roadmap/models.py` (`StepResult`)" (FR-EVAL-001.1)
- **Roadmap Quote**: "`StepResult` lives in `cli/pipeline/models.py`, not `cli/roadmap/models.py` — the extraction document's dependency table is misleading on this point."
- **Impact**: The roadmap contradicts the spec's stated dependency location. If the roadmap is correct about the actual codebase, the spec itself is wrong — but the roadmap's job is to implement what the spec says, not editorialize. This creates ambiguity about which module to import from and whether `models.py` needs modification.
- **Recommended Correction**: Verify actual `StepResult` location in codebase. If it truly lives in `cli/pipeline/models.py`, update the spec's FR-EVAL-001.1 dependencies before proceeding. The roadmap should explicitly note this as a spec erratum requiring resolution in Phase 0, not assert a correction unilaterally.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap claims "17 requirements (12 functional, 5 non-functional)" but spec defines 6 functional requirements (FR-EVAL-001.1 through FR-EVAL-001.6) and 3 non-functional requirements (NFR-EVAL-001.1 through NFR-EVAL-001.3)
- **Spec Quote**: Sections 3 and 6 define FR-EVAL-001.1 through FR-EVAL-001.6 (6 FRs) and NFR-EVAL-001.1 through NFR-EVAL-001.3 (3 NFRs)
- **Roadmap Quote**: "17 requirements (12 functional, 5 non-functional) across 4 domains"
- **Impact**: The roadmap inflates the requirement count, suggesting it is tracking phantom requirements not present in the spec. This miscount undermines traceability — tasks reference FR-001 through FR-012 and NFR-001 through NFR-005, which do not exist in the spec's numbering scheme.
- **Recommended Correction**: Re-map all roadmap requirement references (FR-001 through FR-012, NFR-001 through NFR-005, SC-001 through SC-009) to the spec's actual IDs (FR-EVAL-001.1 through FR-EVAL-001.6, NFR-EVAL-001.1 through NFR-EVAL-001.3). Remove or consolidate phantom requirements.

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: Roadmap introduces `--resume` behavior (OQ-004) as a blocking open question, but the spec explicitly states overwrite behavior and never mentions `--resume` for progress files
- **Spec Quote**: "If progress file already exists, it is overwritten (not appended to)" (FR-EVAL-001.2 acceptance criteria)
- **Roadmap Quote**: "OQ-004: resume-vs-overwrite semantics — confirm `--resume` appends, fresh run overwrites, or defer `--resume` from scope"
- **Impact**: The spec is unambiguous — overwrite, not append. The roadmap treats this as an open question that blocks Phase 1, adding unnecessary delay. The integration test `test_resume_preserves_progress` from the spec (Section 8.2) does reference resume behavior, creating an internal spec tension, but the FR is clear.
- **Recommended Correction**: Accept the spec's FR-EVAL-001.2 overwrite requirement as settled. Note the tension with test plan item `test_resume_preserves_progress` as a spec-internal inconsistency to flag, but do not block implementation on it.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds a `to_json()` / `from_json()` API on `PipelineProgress` not specified in the data model
- **Spec Quote**: Section 4.5 defines `PipelineProgress` with fields `spec_file`, `started_at`, `steps`, `completed` — no methods specified
- **Roadmap Quote**: "Define `PipelineProgress` dataclass wrapping `list[StepProgress]` with `to_json()` / `from_json()`" (Task 1.2)
- **Impact**: Minor scope expansion. These methods are reasonable implementation details but are not in the spec's data model contract. Could introduce deserialization assumptions not validated by the spec.
- **Recommended Correction**: Implement serialization as needed but note these methods are implementation details, not spec requirements. Do not add acceptance criteria for them.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap references `ALL_GATES` constant and claims "all 13 gates" but spec does not define the number of gates
- **Spec Quote**: "Dry-run output includes a Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks" and "All steps including conditional ones (remediate, certify) are listed" (FR-EVAL-001.3)
- **Roadmap Quote**: "verify table has all 13 gates" (Task 3.5), "Dry-run output includes complete gate table with all 13 gates" (Phase 3 milestone)
- **Impact**: The spec says "all steps" without specifying a count. The roadmap asserts 13 as the expected count. If the actual gate count differs, tests will fail for the wrong reason. The number 13 is an implementation detail that should be derived from the codebase, not hardcoded in the roadmap.
- **Recommended Correction**: Replace hardcoded "13" with a dynamic assertion (e.g., assert row count equals `len(ALL_GATES)`). The spec requirement is "all steps" not "13 steps."

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Spec test plan includes `test_gate_summary_all_steps` in unit tests (Section 8.1) but roadmap places equivalent test in Phase 3 as an integration test
- **Spec Quote**: "test_gate_summary_all_steps | tests/roadmap/test_progress.py | Gate summary includes all 13 gate definitions" (Section 8.1 Unit Tests)
- **Roadmap Quote**: "Write tests: verify table has all 13 gates, conditional marking, column completeness" (Task 3.5, Phase 3)
- **Impact**: The spec categorizes this as a unit test but the roadmap's Phase 3 approach treats it as part of integration testing with actual CLI output. This is actually an improvement (per project preference for real evals over unit tests), but it's a deviation from spec's test classification.
- **Recommended Correction**: Acceptable deviation given project conventions favoring eval-style tests. Document the reclassification.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds Phase 0 (Specification Closure) with 0.5 day duration not present in spec's implementation order
- **Spec Quote**: Section 4.6 lists 5 implementation steps starting with "Create progress.py with StepProgress/PipelineProgress models"
- **Roadmap Quote**: "Phase 0 — Specification Closure (0.5 day) ... Resolve OQ-001 ... Resolve OQ-002 ... Resolve OQ-004 ... Freeze progress JSON shape"
- **Impact**: The spec's implementation order (Section 4.6) has no specification closure phase. The roadmap inserts one that blocks all subsequent work. While prudent for the seeded ambiguities, this reorders the spec's prescribed implementation sequence and adds scope.
- **Recommended Correction**: Phase 0 is reasonable given acknowledged spec gaps (GAP-002, GAP-003), but should be explicitly marked as roadmap-added scope not derived from the spec.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Spec's implementation order has dry-run enrichment (step 4) depending on step 2 (CLI surface), but roadmap has Phase 3 (dry-run) running parallel with Phase 2 (CLI integration)
- **Spec Quote**: "4. Enrich --dry-run output with gate summary table -- depends on 2" (Section 4.6)
- **Roadmap Quote**: "Phase 3 can run in parallel with Phase 2 — they share no code dependencies. Both depend only on Phase 1 outputs."
- **Impact**: The spec explicitly states step 4 (dry-run enrichment) depends on step 2 (CLI surface). The roadmap asserts they can parallelize. If dry-run enrichment requires the `--progress-file` Click option from step 2, the roadmap's parallelization claim is incorrect.
- **Recommended Correction**: Verify whether the dry-run gate table actually depends on the `--progress-file` option. If the gate summary is independent of progress file writing (likely), document why the spec's dependency is overstated. If dependent, restore sequential ordering.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: Roadmap uses internal requirement IDs (FR-001 through FR-012, NFR-001 through NFR-005, SC-001 through SC-009) instead of spec's IDs (FR-EVAL-001.x, NFR-EVAL-001.x)
- **Spec Quote**: Requirements are identified as FR-EVAL-001.1 through FR-EVAL-001.6, NFR-EVAL-001.1 through NFR-EVAL-001.3
- **Roadmap Quote**: References throughout use FR-001, FR-002, ..., FR-012, NFR-001 through NFR-005, SC-001 through SC-009
- **Impact**: Traceability loss. A reader cannot map roadmap task requirements back to spec sections without a lookup table. The roadmap never provides this mapping.
- **Recommended Correction**: Add a requirement mapping table or use spec IDs directly.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap notes OQ-005 about missing Section 4.3 in the spec
- **Spec Quote**: Sections jump from 4.2 to 4.4 (no Section 4.3 exists)
- **Roadmap Quote**: "OQ-005: Missing Section 4.3 | Non-blocking | Likely editorial gap — no action needed | Ignore"
- **Impact**: Purely editorial. No content is missing — the section numbering has a gap. The roadmap correctly identifies this as non-blocking.
- **Recommended Correction**: No action required. Roadmap correctly handles this.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: Roadmap introduces OQ-006 about metadata field keys not addressed in spec
- **Spec Quote**: Section 4.5 defines `metadata: dict = field(default_factory=dict)` with no further specification of expected keys
- **Roadmap Quote**: "OQ-006: Metadata field keys | Non-blocking | Treat as extension point; no mandated keys | Defer"
- **Impact**: Minimal. The spec intentionally leaves metadata as a generic dict. The roadmap correctly defers this.
- **Recommended Correction**: No action required.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Deviation**: Spec Section 10 specifies "5 implementation tasks" and "3 test tasks" for tasklist generation, but roadmap's phased plan has ~25 tasks across 7 phases
- **Spec Quote**: "5 implementation tasks mapping to implementation order (Section 4.6), 3 test tasks mapping to unit + integration tests, 1 documentation task for CLI help text updates" (Section 10)
- **Roadmap Quote**: Phases 0-6 contain approximately 25 tasks total
- **Impact**: The spec's downstream input for tasklist generation suggests 9 total tasks. The roadmap's granularity is much finer. This is not necessarily wrong — roadmap tasks and tasklist tasks are different abstractions — but the disconnect could cause confusion when generating the tasklist.
- **Recommended Correction**: When generating the tasklist from this roadmap, consolidate back to the spec's suggested 5+3+1 task structure, or document why finer granularity is appropriate.

## Summary

**Severity Distribution**: 3 HIGH, 5 MEDIUM, 4 LOW

The three HIGH findings are:

1. **DEV-001**: `StepResult` import path contradiction — roadmap asserts the spec's dependency table is wrong without formal resolution
2. **DEV-002**: Phantom requirement inflation — roadmap claims 12 FRs and 5 NFRs when spec defines 6 FRs and 3 NFRs, breaking traceability
3. **DEV-003**: `--resume` scope creep — roadmap treats overwrite-vs-append as an open question when the spec explicitly requires overwrite

The MEDIUM findings center on scope additions (Phase 0, serialization methods, gate count hardcoding) and a dependency ordering change (parallel Phase 2/3 vs spec's sequential steps 2→4).

The roadmap is generally well-structured and demonstrates strong understanding of the feature. The primary corrections needed are: (1) align requirement IDs and counts with the spec, (2) accept the spec's overwrite requirement rather than reopening it, and (3) resolve the `StepResult` location through codebase verification rather than unilateral assertion.
