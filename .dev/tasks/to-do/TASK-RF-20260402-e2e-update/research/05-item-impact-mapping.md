# Research: Existing Task Item Impact Mapping

| Field | Value |
|-------|-------|
| Topic type | Doc Cross-Validator |
| Status | Complete |
| Date | 2026-04-02 |
| Source | `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` |
| Items assessed | 63 items across 11 phases |

## Methodology

Each of the 63 task items is assessed against the known changes from:
1. Auto-detection overhaul (TASK-RF-20260402-auto-detection)
2. QA fixes (28 findings)
3. New EXTRACT_TDD_GATE
4. Prompt and tasklist fidelity changes

Impact values:
- **NO_CHANGE** -- item text is still accurate as-is
- **UPDATE_NEEDED** -- item text references outdated behavior or misses new behavior
- **OBSOLETE** -- item should be removed

---

## Phase 1: Preparation and CLI Verification (6 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 1.1 | Read task, update status | NO_CHANGE | -- |
| 1.2 | Create output directories | NO_CHANGE | -- |
| 1.3 | Verify --prd-file and --tdd-file in help output | UPDATE_NEEDED | CLI changed: `spec_file` is now `input_files` (nargs=-1, accepts 1-3 files). Help text will show positional `input_files` not `spec_file`. Also verify `--input-type` includes "prd" option. The item should check for the new multi-file positional arg format and `--input-type` flag with "prd" value. |
| 1.4 | Run unit test suite | NO_CHANGE | -- |
| 1.5 | Verify skill layer sync | NO_CHANGE | -- |
| 1.6 | Verify existing fixtures exist | NO_CHANGE | -- |

## Phase 2: Create PRD Test Fixture (3 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 2.1 | Create PRD fixture (test-prd-user-auth.md) with detailed content specs | NO_CHANGE | Fixture creation specs are content-driven (personas, sections, etc.) and not affected by code changes. The fixture is authored manually. |
| 2.2 | Sentinel checks on PRD fixture (grep for type, personas, etc.) | NO_CHANGE | These are content checks on the fixture file itself. Not affected by code changes. |
| 2.3 | Verify PRD fixture does NOT trigger TDD auto-detection via dry-run | UPDATE_NEEDED | **Major change**: (1) detect_input_type() now returns "prd" as a third type. A well-formed PRD fixture with 5+ PRD signals (PRD-specific frontmatter, persona sections, user stories, success metrics, product language) will now detect as "prd", NOT "spec". The item says "The PRD should be detected as 'spec' (it is a non-TDD document)" -- this is now WRONG. It should detect as "prd". (2) The stderr message format changed from `"Auto-detected input type: X"` to `"[roadmap] Input type: X (spec=N, tdd=N, prd=N)"`. The grep pattern needs updating. (3) The CLI invocation changed: `superclaude roadmap run FILE` now takes positional `input_files` not `spec_file`, though single-file invocation still works the same way syntactically. |

## Phase 3: Dry-Run Verification with PRD Flag (5 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 3.1 | TDD+PRD dry-run; verify --prd-file accepted, auto-detects "tdd" | UPDATE_NEEDED | The auto-detection check says to verify primary input is "tdd". This is still correct. However: (1) stderr format changed -- look for `"[roadmap] Input type: tdd (spec=N, tdd=N, prd=N)"` not `"Auto-detected input type: tdd"`. (2) With `_route_input_files()`, the PRD file passed via --prd-file may be classified separately. Item should note the new routing behavior. |
| 3.2 | Spec+PRD dry-run; verify auto-detects "spec" | UPDATE_NEEDED | Same stderr format change as 3.1. Also: the spec fixture should still detect as "spec" (no PRD signals in the spec fixture). But item should reference new format. |
| 3.3 | Test --tdd-file flag on roadmap run (spec primary + TDD supplementary) | NO_CHANGE | The --tdd-file flag behavior is unchanged by the auto-detection overhaul. |
| 3.4 | Test redundancy guard (TDD primary + --tdd-file same file) | UPDATE_NEEDED | The redundancy guard was moved to `execute_roadmap` (C-111 fix). Also a same-file guard was added (C-20 fix) for --tdd-file and --prd-file. The warning text and location may differ from what the item expects. Item should verify the guard fires from `execute_roadmap`, and should also test the same-file guard (--tdd-file pointing to same path as primary). |
| 3.5 | Review Phase 3 results, go/no-go decision | NO_CHANGE | -- |

## Phase 4: Test 1 -- Full TDD+PRD Pipeline Run (14 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 4.1 | Run full TDD+PRD pipeline | UPDATE_NEEDED | The item references `detect_input_type()` and `_build_steps()` behavior. With the auto-detection overhaul, `_build_steps()` now uses EXTRACT_TDD_GATE (19 fields) when input_type=="tdd", else EXTRACT_GATE. The pipeline step order may reflect this. Also, dead auto-detection was removed from `_build_steps` (C-84). The item should note EXTRACT_TDD_GATE usage for TDD primary. |
| 4.2 | Verify TDD+PRD extraction frontmatter (13 standard + 6 TDD fields) | UPDATE_NEEDED | EXTRACT_TDD_GATE now requires 19 fields total (13 standard + 6 TDD-specific). The item already lists these correctly, but should reference EXTRACT_TDD_GATE as the gate that enforces this. The gate name should be mentioned for clarity. |
| 4.3 | Verify TDD+PRD extraction body sections, PRD enrichment check | UPDATE_NEEDED | The generate prompt now has standard body section descriptions (C-04 fix) and TDD supplementary blocks added to all 4 remaining prompt builders (C-05). The extraction body structure may differ slightly from prior expectations. The PRD enrichment check is still valid. |
| 4.4 | Verify roadmap variant files | NO_CHANGE | The roadmap variant checks are content-based and not directly affected by the code changes. |
| 4.5a | Verify diff analysis artifact | NO_CHANGE | diff builder does not have TDD/PRD awareness changes. |
| 4.5b | Verify debate transcript artifact | NO_CHANGE | debate builder does not have TDD/PRD awareness changes. |
| 4.5c | Verify base selection (score prompt with PRD dimensions) | NO_CHANGE | The score prompt PRD dimensions are unchanged. |
| 4.6 | Verify merged roadmap | UPDATE_NEEDED | Merge prompt now has TDD/PRD awareness (C-06 fix). The merged roadmap may now contain explicit TDD/PRD-influenced content that was not present before. Item should check for merge prompt TDD/PRD awareness markers. |
| 4.7 | Verify anti-instinct audit | NO_CHANGE | Anti-instinct gate is unchanged by these fixes. |
| 4.8 | Verify test strategy output | NO_CHANGE | Test strategy builder already had PRD enrichment. |
| 4.9 | Verify spec-fidelity output | UPDATE_NEEDED | Spec-fidelity dims 7-11 are now conditional on tdd_file (C-03 fix). For TDD+PRD path, tdd_file is null (TDD is primary input, not supplementary). But wait -- C-08 simplified: no supplementary tdd_file when primary is TDD. So dims 7-11 should NOT appear in TDD primary path. This is a behavioral change from what the item may expect. Item should clarify that TDD-specific fidelity dimensions only appear when tdd_file is explicitly provided as supplementary, not when TDD is the primary input. |
| 4.9a | Verify wiring-verification output | NO_CHANGE | -- |
| 4.9b | Verify state file (tdd_file, prd_file, input_type) | UPDATE_NEEDED | C-62 fix: input_type "auto" is no longer written to state file. C-91 fix: input_type restoration on resume works. The item should verify input_type is "tdd" (not "auto"). Also should verify the state file format matches the new schema. The item already expects input_type="tdd" which is correct post-fix. Minor: add check that input_type is never "auto". |
| 4.10 | Phase 4 summary | NO_CHANGE | -- |

## Phase 5: Test 2 -- Full Spec+PRD Pipeline Run (9 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 5.1 | Run full spec+PRD pipeline | NO_CHANGE | Single-file spec invocation still works. The spec path uses EXTRACT_GATE (not EXTRACT_TDD_GATE). No behavioral change for this invocation. |
| 5.2 | Verify spec+PRD extraction frontmatter (13 standard only, no TDD fields) | NO_CHANGE | Spec path still produces 13 standard fields. EXTRACT_GATE is used (not EXTRACT_TDD_GATE). Correct as-is. |
| 5.3 | Verify spec+PRD extraction body (8 standard sections, no TDD sections, PRD enrichment check) | NO_CHANGE | The spec extraction path is unchanged. PRD enrichment check is still valid. |
| 5.4 | Verify spec+PRD merged roadmap (PRD enrichment check, TDD leak check) | UPDATE_NEEDED | Merge prompt now has TDD/PRD awareness (C-06 fix). The TDD leak check should be updated to account for merge prompt changes -- the merge prompt may now explicitly reference that no TDD was provided, which could affect content. |
| 5.5 | Verify spec+PRD anti-instinct audit | NO_CHANGE | -- |
| 5.6 | Verify spec+PRD spec-fidelity output | UPDATE_NEEDED | C-03 fix: spec-fidelity dims 7-11 are now conditional on tdd_file. For spec+PRD path (no --tdd-file), dims 7-11 should be ABSENT. The item already expects TDD-specific dimensions to be "absent or empty" which aligns, but should be made explicit: dims 7-11 are now conditionally excluded by code, not just expected to be empty. Also: new PRD check 4 (priority ordering from tasklist fidelity) may affect what's checked here. |
| 5.7 | Verify spec+PRD state file | UPDATE_NEEDED | Same as 4.9b: verify input_type is "spec" (not "auto"). C-62 fix ensures "auto" is never written. Item already expects "spec" which is correct. Minor: add explicit check that input_type != "auto". |
| 5.8 | Verify all gates passed for spec+PRD pipeline | NO_CHANGE | -- |
| 5.9 | Phase 5 summary | NO_CHANGE | -- |

## Phase 6: Auto-Wire from .roadmap-state.json (6 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 6.1 | Run tasklist validate with auto-wire (no explicit flags) | UPDATE_NEEDED | C-27 fix: --prd-file CLI now overrides state-restored prd_file on resume. C-91 fix: input_type restoration on resume. The auto-wire behavior should work, but the item should also verify that input_type is correctly restored from state. Also: _restore_from_state behavior changed (C-08 fix, then simplified). |
| 6.2 | Verify auto-wired fidelity output includes PRD validation | UPDATE_NEEDED | New tasklist fidelity checks: TDD checks 4-5 (data models, API endpoints) and PRD check 4 (priority ordering). The item lists only 3 PRD checks (persona S7, metrics S19, scenarios S12/S22). Should add PRD check 4 (priority ordering). Also should note TDD checks 4-5 if tdd_file is auto-wired. |
| 6.3 | Test explicit flag precedence over auto-wire | UPDATE_NEEDED | C-27 fix explicitly addresses this: --prd-file CLI overrides state-restored prd_file. The item should reference this as verified behavior, not just tested behavior. The test is still valid but the expected behavior is now explicitly documented in the codebase. |
| 6.4 | Test graceful degradation (auto-wired path doesn't exist on disk) | NO_CHANGE | -- |
| 6.5 | Test auto-wire with no .roadmap-state.json present | NO_CHANGE | -- |
| 6.6 | Phase 6 summary | NO_CHANGE | -- |

## Phase 7: Tasklist Validation Enrichment Testing (6 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 7.1 | Run tasklist validate with explicit TDD+PRD flags | NO_CHANGE | -- |
| 7.2 | Run tasklist validate baseline (no supplementary flags) | NO_CHANGE | -- |
| 7.3 | Compare enriched vs baseline fidelity reports | UPDATE_NEEDED | The item lists 3 TDD checks (test cases S15, rollback S19, components S10) and 3 PRD checks (persona S7, metrics S19, scenarios S12/S22). New checks were added: TDD checks 4-5 (data models, API endpoints) and PRD check 4 (priority ordering). The comparison table should include these new checks. |
| 7.4 | Run tasklist validate on spec+PRD output (PRD-only enrichment) | NO_CHANGE | -- |
| 7.5 | Verify build_tasklist_generate_prompt function directly | UPDATE_NEEDED | The function signature or behavior may have changed. The inline Python test checks for specific strings ("Supplementary", "TDD", "PRD", "PRD context informs", "When both TDD and PRD"). If authority language changed from "advisory" to "authoritative for business context", the string checks may need updating. Check: `'PRD context informs'` may now be `'PRD context is authoritative for business context'` or similar. |
| 7.6 | Phase 7 summary | NO_CHANGE | -- |

## Phase 8: TDD+PRD vs TDD-Only Comparison (5 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 8.1 | Compare Test 1 extraction: TDD+PRD vs TDD-only | UPDATE_NEEDED | The item says "both should have 19 TDD fields" in frontmatter. With EXTRACT_TDD_GATE, this is now enforced by the gate (19 required fields). The comparison should note that the gate enforcement is new. Also, the generate prompt changes (C-04: standard body section descriptions) may cause structural differences in extraction output between old and new runs. |
| 8.2 | Compare Test 1 roadmap: TDD+PRD vs TDD-only | NO_CHANGE | Content comparison is still valid. |
| 8.3 | Compare Test 2 extraction: spec+PRD vs spec-only | NO_CHANGE | Both should have 13 fields. The comparison logic is unchanged. |
| 8.4 | Compare Test 2 roadmap: spec+PRD vs spec-only | NO_CHANGE | Content comparison is still valid. |
| 8.5 | Phase 8 summary | NO_CHANGE | -- |

## Phase 9: Cross-Pipeline Comparison and Anti-Instinct Analysis (4 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 9.1 | Compare anti-instinct results across 4 runs | NO_CHANGE | Anti-instinct is unchanged. |
| 9.2 | Compare pipeline completion status across 4 runs | UPDATE_NEEDED | New runs use EXTRACT_TDD_GATE (for TDD primary) and updated _build_steps routing (C-117). The step plan may differ from prior runs. The comparison should account for potentially different step names or gate labels in the new runs. |
| 9.3 | Compare fidelity results between TDD+PRD and spec+PRD | UPDATE_NEEDED | C-03 fix (dims 7-11 conditional on tdd_file) means fidelity output structure may differ between TDD+PRD and spec+PRD more explicitly than before. The comparison should note this conditional behavior. |
| 9.4 | Phase 9 summary | NO_CHANGE | -- |

## Phase 10: Final Verification Report (3 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 10.1 | Compile final verification report | UPDATE_NEEDED | The success criteria checklist should add new criteria: (1) EXTRACT_TDD_GATE used for TDD primary (yes/no), (2) PRD auto-detection returns "prd" for PRD fixture (yes/no), (3) input_type never "auto" in state file (yes/no), (4) new fidelity checks present (TDD 4-5, PRD 4) (yes/no), (5) borderline warning for scores 3-6 (yes/no if tested). |
| 10.2 | Compare new vs prior verification report | NO_CHANGE | -- |
| 10.3 | Write consolidated follow-up action items | NO_CHANGE | -- |

## Phase 11: Completion (2 items)

| Item | Current Description Summary | Impact | Change Needed |
|------|---------------------------|--------|---------------|
| 11.1 | Verify all deliverables exist | NO_CHANGE | -- |
| 11.2 | Update status to done | NO_CHANGE | -- |

---

## Frontmatter and Preamble Updates

| Section | Impact | Change Needed |
|---------|--------|---------------|
| Task Overview | UPDATE_NEEDED | References "auto-detection identifies as 'tdd'" and "'spec'" -- should note "prd" is now a third detection type. Also: `spec_file` parameter is now `input_files` (nargs=-1). |
| Key Objectives | UPDATE_NEEDED | Add objective: "Verify PRD auto-detection returns 'prd' for PRD fixtures". Add: "Verify EXTRACT_TDD_GATE is used for TDD primary input". Remove or update: "Verify redundancy guard fires when --tdd-file is passed with a TDD primary input" -- guard moved to execute_roadmap. |
| Prerequisites - CLI prerequisites | UPDATE_NEEDED | `--input-type` flag now includes "prd" option. Help output format may differ due to `input_files` nargs=-1. |
| Prerequisites - Pipeline Code | UPDATE_NEEDED | `executor.py` description should mention EXTRACT_TDD_GATE, _route_input_files(), and note that dead auto-detection was removed from _build_steps. `prompts.py` description: generate prompt now has standard body sections (C-04), TDD supplementary blocks on all remaining builders (C-05), merge has TDD/PRD awareness (C-06). `commands.py`: spec_file is now input_files. |
| Known Issues | UPDATE_NEEDED | (1) "detect_input_type() threshold fixed to >= 5 with revised signal weights. PRD documents should detect as 'spec'" -- this is NOW WRONG. PRD documents detect as "prd". Remove/update. (2) "Click stderr auto-detection messages swallowed in dry-run output" -- the stderr format changed to "[roadmap] Input type: X (spec=N, tdd=N, prd=N)". (3) Add: borderline warning for scores 3-6 is new behavior. (4) Add: effective_input_type alias was removed (C-113). |
| Known Limitation - Tasklist Generation | NO_CHANGE | Still accurate. |
| Open Questions | UPDATE_NEEDED | AW-1 about tdd_file storage: C-08 simplified this -- no supplementary tdd_file when primary is TDD. Should be marked RESOLVED with the C-08 fix. RG-1 about redundancy guard stderr: redundancy guard moved to execute_roadmap (C-111). Should note location change. |
| Deferred Work | UPDATE_NEEDED | "PRD auto-detection path" says "PRD documents currently detect as 'spec'. Future: dedicated PRD detection type." -- this is NOW DONE. PRD detection is implemented. Remove or mark as COMPLETED. |

---

## New Items Needed

Items that do not exist yet but should, based on the known changes:

| Phase | Suggested Item # | Description | Rationale |
|-------|-----------------|-------------|-----------|
| 2 | 2.3a | Verify PRD fixture triggers "prd" auto-detection (not "spec") by running dry-run and checking for `"[roadmap] Input type: prd (spec=N, tdd=N, prd=N)"` in stderr. Verify prd score >= 5. | detect_input_type() now returns "prd" for PRD documents. The existing 2.3 expects "spec" detection which is now wrong. This item replaces the detection check in 2.3. |
| 3 | 3.1a | Verify new stderr auto-detection format shows score breakdown: `"[roadmap] Input type: tdd (spec=N, tdd=N, prd=N)"`. Check that all three scores are present in the output. | New stderr format includes all three scores. Existing items don't verify the score breakdown. |
| 3 | 3.4a | Test same-file guard: run `uv run superclaude roadmap run FILE --tdd-file FILE --dry-run` where FILE is the same path for primary and --tdd-file. Verify the same-file guard (C-20 fix) produces a warning or error. Similarly test with --prd-file pointing to the same file as primary. | C-20 fix added same-file guard. No existing item tests this. |
| 3 | 3.4b | Test borderline warning: create or use a fixture with auto-detection scores in range 3-6 and verify that a borderline warning is emitted (C-103 fix). | Borderline warning for scores 3-6 is new behavior with no test coverage. |
| 1 or 3 | 1.3a | Verify `--input-type` flag accepts "prd" value: run `uv run superclaude roadmap run --help` and verify "prd" appears as an option for --input-type. Then run `uv run superclaude roadmap run FILE --input-type prd --dry-run` and verify it works without error. | --input-type now includes "prd" as a valid choice. No existing item tests this. |
| 3 | 3.1b | Verify multi-file CLI invocation: run `uv run superclaude roadmap run SPEC TDD --dry-run` (two positional files) and verify _route_input_files() classifies and routes them correctly. Check stderr for routing decisions. | CLI now accepts nargs=-1 (1-3 files). No existing item tests multi-file positional invocation. |
| 3 | 3.1c | Verify multi-file CLI with all three types: run `uv run superclaude roadmap run SPEC TDD PRD --dry-run` (three positional files) and verify routing. | Three-file invocation is a new capability. |
| 4 | 4.2a | Verify EXTRACT_TDD_GATE is used for TDD primary input: check pipeline log for EXTRACT_TDD_GATE reference (19 required fields). Verify all 19 fields are present in extraction frontmatter. | EXTRACT_TDD_GATE is new. No existing item explicitly verifies which gate was used. |
| 6 | 6.1a | Verify input_type is correctly restored from .roadmap-state.json on resume (C-91 fix). Run a pipeline that resumes from state and verify input_type is not lost. | C-91 fix for input_type restoration on resume. No existing item tests resume behavior explicitly. |
| 7 | 7.3a | Verify new tasklist fidelity checks: TDD checks 4-5 (data models from TDD, API endpoints from TDD) and PRD check 4 (priority ordering matches PRD). | New fidelity checks added. Existing items only reference the original 3+3 checks. |

---

## Known Issues Updates

| Section | Current Content | Recommended Change |
|---------|---------------|--------------------|
| Known Issues bullet 4 | "detect_input_type() threshold fixed to >= 5 with revised signal weights. PRD documents should detect as 'spec' (not 'tdd') unless PRD has its own detection path." | **REPLACE WITH**: "detect_input_type() now returns 'prd', 'tdd', or 'spec'. PRD scoring uses 5 weighted signals with threshold >= 5. PRD is checked BEFORE TDD in the detection order. Borderline scores (3-6) produce a warning." |
| Known Issues bullet 3 | "Click stderr auto-detection messages swallowed in dry-run output (display bug, detection still works)." | **UPDATE**: Note new stderr format: `"[roadmap] Input type: X (spec=N, tdd=N, prd=N)"`. The display bug may still apply. |
| Open Questions AI-1 | Anti-instinct gate question | NO_CHANGE (still open) |
| Open Questions TG-1 | Tasklist generation limitation | NO_CHANGE (still valid) |
| Open Questions AW-1 | "does the implementation save tdd_file as null when TDD is the primary input?" | **MARK RESOLVED**: C-08 simplified -- no supplementary tdd_file when primary is TDD. tdd_file will be null in state when TDD is primary. |
| Open Questions RG-1 | "Redundancy guard warning may be swallowed by Click stderr in dry-run" | **UPDATE**: Redundancy guard moved to execute_roadmap (C-111). Warning location changed. Still may be affected by stderr display bug. |
| Deferred Work row 2 | "PRD auto-detection path -- PRD documents currently detect as 'spec'. Future: dedicated PRD detection type." | **REMOVE or MARK COMPLETED**: PRD auto-detection is now implemented (TASK-RF-20260402-auto-detection, status=done). |

---

## Summary Statistics

- Items with NO_CHANGE: **37**
- Items needing UPDATE: **21**
- Items OBSOLETE: **0**
- New items suggested: **11**
- Preamble/section updates needed: **8**

### Breakdown of UPDATE_NEEDED items by change driver:

| Change Driver | Items Affected |
|--------------|----------------|
| Auto-detection overhaul (detect_input_type returns "prd", new stderr format, _route_input_files) | 2.3, 3.1, 3.2, 3.4, 9.2, frontmatter sections |
| EXTRACT_TDD_GATE (19 fields, routing in _build_steps) | 4.1, 4.2, 8.1 |
| QA fixes (C-03 fidelity conditional dims, C-06 merge awareness, C-08 tdd_file simplification, C-27 CLI override, C-62 no "auto" in state, C-91 input_type restore, C-111 redundancy guard moved) | 4.6, 4.9, 4.9b, 5.4, 5.6, 5.7, 6.1, 6.2, 6.3, 9.3 |
| New fidelity checks (TDD 4-5, PRD 4) | 6.2, 7.3 |
| Prompt language changes (authority language, generate prompt body sections) | 4.3, 7.5 |
| Known Issues / Open Questions / Deferred Work sections | 5 section-level updates |

### Highest-priority updates (will cause test FAILURES if not addressed):

1. **Item 2.3** -- expects PRD detected as "spec", but it now detects as "prd". Test will FAIL.
2. **Item 3.1, 3.2** -- grep for old stderr format will find nothing. Tests will appear to fail.
3. **Item 7.5** -- inline Python string checks may fail if authority language changed.
4. **Known Issues bullet 4** -- tells executor that PRD detects as "spec", causing incorrect expectations throughout.
5. **Deferred Work row 2** -- tells executor PRD detection is future work, when it's already done.

