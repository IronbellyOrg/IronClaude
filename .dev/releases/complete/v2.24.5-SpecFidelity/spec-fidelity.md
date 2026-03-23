---
high_severity_count: 1
medium_severity_count: 5
low_severity_count: 4
total_deviations: 10
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap places test file for FR-ATL.3 and FR-ATL.4 in wrong location
- **Spec Quote**: `tests/roadmap/test_file_passing.py:105-136` (Section 4.2) and test table lists file as `tests/roadmap/test_file_passing.py` (Section 8.1)
- **Roadmap Quote**: `tests/roadmap/test_executor.py (or equivalent)` (Phase 2, Files touched)
- **Impact**: An implementer following the roadmap would create tests in the wrong file or create a new file instead of modifying the existing one. The spec is explicit about `test_file_passing.py` as the target for both the rename (FR-ATL.3) and new composed-string test (FR-ATL.4). The roadmap's `(or equivalent)` qualifier introduces ambiguity where the spec has none.
- **Recommended Correction**: Replace `tests/roadmap/test_executor.py (or equivalent)` with `tests/roadmap/test_file_passing.py` in the Phase 2 Files touched and the Resource Requirements table.

---

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Roadmap Phase 2 test steps do not include the at-limit boundary assertion specified in FR-ATL.2
- **Spec Quote**: `When len(composed.encode('utf-8')) == _EMBED_SIZE_LIMIT exactly (at-limit), inline embedding fires (not fallback) — confirming <= is the intended operator` (FR-ATL.2, acceptance criteria)
- **Roadmap Quote**: `2.6 | Add at-limit boundary test: input exactly _EMBED_SIZE_LIMIT bytes → inline embedding (not fallback)` (Phase 2)
- **Impact**: The roadmap does include step 2.6 for this, so the action is present. However, the Success Criteria table maps SC-10 to Phase 2 but no specific test name is given for the boundary test — it is unnamed, unlike every other test in Phase 2. This creates a gap in traceability: an implementer might fold it into another test rather than creating a distinct, named assertion. Minor concern since the step exists.
- **Recommended Correction**: Assign an explicit test name (e.g., `test_at_limit_exact_boundary_inline`) to step 2.6 for traceability to SC-10.

---

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Spec's Implementation Order places FR-001.3 tests in Phase 1.4 (parallel with other Phase 1 work), but roadmap defers all tests to Phase 2
- **Spec Quote**: `1.4 Edit tests/pipeline/test_process.py: add new test, update two existing (must follow 1.1)` (Section 4.6, Phase 1)
- **Roadmap Quote**: `Phase 2 — Test Coverage ... 2.1 Add test_tools_default_in_command ... 2.2 Update test_required_flags ... 2.3 Update test_stream_json_matches_sprint_flags` (Phase 2)
- **Impact**: The roadmap consolidates all test work into Phase 2, whereas the spec parallelizes FR-001.3 test updates with Phase 1 constant work. This means the roadmap runs Phase 1.1 production code changes without immediate test validation, whereas the spec intended test updates to follow closely. The roadmap's approach is valid but changes the verification timing — a test failure from the flag insertion would be caught later.
- **Recommended Correction**: Either move steps 2.1–2.3 into Phase 1.1 (after step 1.1.4) to match spec ordering, or document the deliberate resequencing with rationale.

---

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap introduces success criteria SC-1 through SC-10 not defined in the spec
- **Spec Quote**: The spec defines no `SC-NNN` success criteria section. It defines acceptance criteria per FR and NFR.
- **Roadmap Quote**: `SC-1 | --tools default in all subprocess commands | test_tools_default_in_command + test_required_flags` (Success Criteria Validation Matrix)
- **Impact**: The roadmap synthesizes 10 success criteria that map to spec FRs and NFRs, which is useful for validation tracking. However, these are roadmap-originated artifacts not traceable to spec identifiers. An implementer might treat these as authoritative and miss acceptance criteria in the spec that don't map cleanly to an SC-N. For example, FR-ATL.1's acceptance criterion about `No import resource line` maps to SC-8 (zero new imports) only loosely — SC-8 is about new imports generally, while FR-ATL.1 specifically calls out removing a dead `import resource` line.
- **Recommended Correction**: Add a mapping table from each SC-N to the specific FR/NFR acceptance criteria it covers, or reference the spec's own acceptance criteria directly.

---

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits the spec's explicit Phase 0 CLI-failure retry semantics
- **Spec Quote**: `→ CLI FAILURE: exit non-zero for any reason. Resolve CLI issue and re-run Task 0.1. Do not record WORKING or BROKEN until exit code is 0.` (Section 4.6, Phase 0)
- **Roadmap Quote**: `0.1 | Verify CLI prerequisite: claude --print -p "hello" --max-turns 1 exits 0` (Phase 0 table)
- **Impact**: The roadmap separates the prerequisite check (step 0.1) from the sentinel test (step 0.2) but does not specify what happens if step 0.2 returns a non-zero exit code that is distinct from WORKING/BROKEN. The spec defines a third outcome (CLI FAILURE) with explicit retry instructions. An implementer following only the roadmap might record BROKEN for a transient CLI error.
- **Recommended Correction**: Add the CLI FAILURE outcome to step 0.3's recording criteria, with retry instruction matching the spec's three-outcome model.

---

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Roadmap introduces OQ-6 not present in the spec
- **Spec Quote**: Section 11 defines OQ-1 through OQ-4 only.
- **Roadmap Quote**: `OQ-6: Completeness of executor inventory — codebase search for subprocess invocation patterns recommended before v2.26` (Open Questions for Post-Release)
- **Impact**: The roadmap adds a new open question that expands scope awareness beyond the spec. While this is a reasonable observation, it introduces a tracking item that the spec author did not identify. If the roadmap is treated as the implementation plan, this could trigger out-of-scope investigation. Low risk since it's marked post-release.
- **Recommended Correction**: Either add OQ-6 to the spec's Section 11 for consistency, or note it explicitly as a roadmap-originated observation distinct from spec open items.

---

### DEV-007
- **ID**: DEV-007
- **Severity**: LOW
- **Deviation**: Roadmap omits OQ-3 from the spec's open items
- **Spec Quote**: `OQ-3 | Is remediate_executor.py:177 actively producing incorrect results due to broken --file? | If yes, all prior remediations may have been context-free | Phase 0 determines; Phase 1.5 fixes` (Section 11)
- **Roadmap Quote**: Open Questions lists OQ-2, OQ-4, OQ-6 only. '[MISSING]' for OQ-3.
- **Impact**: OQ-3 is implicitly addressed by Phase 0 + Phase 1.5 in the roadmap, but the explicit tracking item and its implication ("all prior remediations may have been context-free") is not surfaced. This is informational — the roadmap handles the resolution path but drops the diagnostic question.
- **Recommended Correction**: Add OQ-3 to the roadmap's open questions section, or note that Phase 0 implicitly resolves it.

---

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: Roadmap omits OQ-1 from open questions (resolved by Phase 0)
- **Spec Quote**: `OQ-1 | Does claude --print --file /bare/path deliver file content? | Determines if fallback works or needs replacement | Phase 0 (15 min test — blocking gate)` (Section 11)
- **Roadmap Quote**: '[MISSING]' from Open Questions section.
- **Impact**: OQ-1 is fully addressed by Phase 0 execution, so omitting it from the post-release open questions is arguably correct (it's resolved in-release). However, the spec's cross-reference from FR-ATL.5 (`Cross-reference: Phase 0 result resolves OQ-1`) assumes OQ-1 is tracked.
- **Recommended Correction**: Note OQ-1 as resolved by Phase 0 in the roadmap rather than omitting it entirely.

---

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: Spec title says "v2.24.5" but frontmatter `title` field references "v2.24.5" while spec filename is `v2.25.1-release-spec.md`
- **Spec Quote**: Filename: `v2.25.1-release-spec.md`, frontmatter: `title: "v2.24.5: Fix Tool Schema Discovery..."`
- **Roadmap Quote**: `spec_source: v2.25.1-release-spec.md`
- **Impact**: The filename/version mismatch in the spec is a source document issue, not a roadmap deviation. The roadmap correctly references the filename. No implementation impact.
- **Recommended Correction**: None required for the roadmap; spec filename should be corrected upstream.

---

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap adds timeline estimates and resource requirements sections not present in the spec
- **Spec Quote**: No timeline or resource allocation section exists in the spec.
- **Roadmap Quote**: `Timeline Estimates ... Implementation Effort (WORKING path): ~2–3 hours ... Delivery elapsed (WORKING path): 1–2 days` (Timeline section)
- **Impact**: These are additive roadmap artifacts that do not contradict the spec. They provide useful planning context. No correctness concern.
- **Recommended Correction**: None required — additive content is appropriate for a roadmap.

---

## Summary

**Severity Distribution**: 1 HIGH, 5 MEDIUM, 4 LOW

The single HIGH severity deviation (DEV-001) is the roadmap directing test work to the wrong file (`test_executor.py` instead of `test_file_passing.py`). This would cause an implementer to either create tests in the wrong location or create unnecessary new files, contradicting the spec's explicit file paths in both the architecture table and test plan.

The five MEDIUM deviations cluster around: test phase sequencing (DEV-003), missing CLI-failure retry semantics in Phase 0 (DEV-005), the unnamed boundary test (DEV-002), untraced success criteria (DEV-004), and a roadmap-originated open question (DEV-006). None of these would cause incorrect code, but they reduce implementation precision and traceability.

The four LOW deviations are informational: dropped open question tracking items (DEV-007, DEV-008), a pre-existing filename mismatch (DEV-009), and additive roadmap content (DEV-010).

**Recommendation**: Resolve DEV-001 (wrong test file) before generating a tasklist. The MEDIUM items should be addressed for implementation clarity but do not block tasklist generation if DEV-001 is fixed.
