---
confirmed_high_count: 2
disputed_count: 0
medium_count: 8
noise_count: 4
total_unique_findings: 14
voter_count: 5
---

# Spec-Fidelity Consensus Report (5-Vote Statistical Aggregation)

## Methodology

Five independent spec-fidelity checks were run against the same roadmap and spec.
Each finding was matched across votes by deviation description (not DEV-NNN ID).
Consensus severity uses majority vote (3/5+); ties break toward LOWER severity.

## Aggregated Findings

| # | Finding | Vote Count | Severity Votes | Consensus | Confidence | Action |
|---|---------|-----------|----------------|-----------|------------|--------|
| F-01 | **Phantom FR-NNN requirement IDs** — roadmap references ~30 FR-009–FR-038 identifiers not defined anywhere in spec | 5/5 | HIGH(3), MEDIUM(2) | HIGH | 1.0 | **CONFIRMED HIGH — must fix** |
| F-02 | **Analysis functions in wrong file** — roadmap puts `analyze_unwired_callables`, `analyze_orphan_modules`, `analyze_unwired_registries` in `wiring_analyzer.py`; spec puts them in `wiring_gate.py` | 5/5 | HIGH(5) | HIGH | 1.0 | **CONFIRMED HIGH — must fix** |
| F-03 | **Phantom NFR-NNN requirement IDs** — roadmap references NFR-001–NFR-014 (except NFR-007) not defined in spec | 4/5 | HIGH(1), MEDIUM(2), merged-into-F-01(1), implicit(1) | MEDIUM | 0.8 | MEDIUM — document, don't block (most votes merge this with F-01) |
| F-04 | **Missing `_get_all_step_ids()` explicit task** — spec §5.7 Step 5 requires it; roadmap has it only in validation checkpoint, not as a task | 5/5 | HIGH(1), MEDIUM(3), LOW(1) | MEDIUM | 1.0 | MEDIUM — add to task 3a.2 |
| F-05 | **Performance target conflation** — roadmap Phase 1 uses `<2s` but spec SC-008 says `<5s`; `<2s` is sprint-specific (R4) | 4/5 | MEDIUM(4) | MEDIUM | 0.8 | MEDIUM — correct Phase 1 checkpoint |
| F-06 | **OQ-3 treats settled spec decision as open question** — whitelist strictness per rollout_mode is already decided in spec §5.2.1 | 2/5 | MEDIUM(2) | MEDIUM | 0.4 | NOISE — only 2/5 flagged |
| F-07 | **Risk R9 added without spec backing** — roadmap adds merge conflict risk R9; spec covers this in §15 but without risk ID | 4/5 | MEDIUM(3), LOW(1) | MEDIUM | 0.8 | MEDIUM — annotate as roadmap-originated |
| F-08 | **Test LOC estimate mismatch** — spec frontmatter says 370-480, §12 says 420-560; roadmap uses 420-560 | 4/5 | LOW(3), MEDIUM(1) | LOW | 0.8 | NOISE — spec internal inconsistency |
| F-09 | **`ast_analyze_file()` placed in Phase 1 vs spec's T06 (deferrable)** — roadmap Task 1.6 puts it in core Phase 1; spec assigns it to T06 with cut criteria | 2/5 | HIGH(1), MEDIUM(1) | MEDIUM | 0.4 | NOISE — only 2/5 flagged; roadmap's 1.6 is a shared AST utility, not the ToolOrchestrator plugin |
| F-10 | **Missing YAML injection prevention task** — spec §5.4 MUST use `yaml.safe_dump()`; no explicit roadmap task | 3/5 | MEDIUM(1), LOW(2) | LOW | 0.6 | MEDIUM — add acceptance criterion to Task 2.1 |
| F-11 | **Missing resume behavior validation** — spec §5.7.2 documents 3 conditions; no roadmap task/test | 3/5 | MEDIUM(1), LOW(2) | LOW | 0.6 | MEDIUM — add to Phase 3a integration tests |
| F-12 | **`wiring_whitelist.yaml` in roadmap New Files but not in spec §12 manifest** | 2/5 | MEDIUM(1), LOW(1) | LOW | 0.4 | NOISE — additive, reasonable |
| F-13 | **`build_wiring_verification_prompt()` signature not specified in roadmap task** | 2/5 | LOW(2) | LOW | 0.4 | NOISE — implementers reference spec |
| F-14 | **Spec internal inconsistency: §5.4 example shows `blocking_findings: 3` with `rollout_mode: shadow`** — should be 0 per §5.6 logic | 1/5 | LOW(1) | LOW | 0.2 | NOISE — spec defect, not roadmap deviation |

## Classification Summary

### CONFIRMED HIGH (must fix before tasklist generation)

**F-01: Phantom FR-NNN requirement IDs** (5/5 votes, confidence 1.0)
- Every vote flagged this. 3 votes rated HIGH, 2 rated MEDIUM.
- Consensus: HIGH — traceability is broken when implementers cannot map tasks to spec requirements.
- **Fix**: Replace all FR-NNN references with spec-native identifiers (G-NNN, SC-NNN, spec §section).

**F-02: Analysis functions in wrong file** (5/5 votes, confidence 1.0)
- Every vote flagged this as HIGH unanimously.
- Spec §4.2 and §12: `wiring_gate.py` = "Core analysis + gate + emitter" (280-320 LOC); `wiring_analyzer.py` = "AST analyzer for ToolOrchestrator" (140-180 LOC).
- **Fix**: Move Tasks 1.2, 1.3, 1.4 from `cli/audit/wiring_analyzer.py` to `cli/audit/wiring_gate.py`.

### DISPUTED (none)

No findings met the DISPUTED criteria (consensus HIGH + confidence < 0.6).

### MEDIUM (document, don't block)

- **F-03**: NFR-NNN phantom IDs (4/5, confidence 0.8) — often merged with F-01; fix alongside F-01.
- **F-04**: `_get_all_step_ids()` missing task (5/5, confidence 1.0) — add to task 3a.2.
- **F-05**: Performance target `<2s` vs `<5s` (4/5, confidence 0.8) — correct Phase 1 checkpoint.
- **F-07**: Risk R9 added without spec ID (4/5, confidence 0.8) — annotate as roadmap-originated.
- **F-10**: YAML injection prevention (3/5, confidence 0.6) — add acceptance criterion.
- **F-11**: Resume behavior validation (3/5, confidence 0.6) — add integration test assertion.

### NOISE (attention artifacts, 1-2/5 votes only)

- **F-06**: OQ-3 as open question (2/5) — valid concern but not consistently flagged.
- **F-08**: Test LOC mismatch (4/5 flagged but all rated LOW) — spec internal inconsistency.
- **F-09**: `ast_analyze_file()` phase placement (2/5) — roadmap's Task 1.6 is a shared AST utility, distinct from the ToolOrchestrator plugin.
- **F-12**: `wiring_whitelist.yaml` not in spec manifest (2/5) — additive file, reasonable.
- **F-13**: Prompt function signature omitted (2/5) — trivial detail.
- **F-14**: Spec example `blocking_findings` inconsistency (1/5) — spec defect, not roadmap issue.
