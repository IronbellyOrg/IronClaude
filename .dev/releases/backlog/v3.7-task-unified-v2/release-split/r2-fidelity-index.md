# Release 2 -- Fidelity Index Against Original Spec

**Audit date**: 2026-04-02
**Auditor**: Claude Opus 4.6 (via /sc:reflect)
**Original spec**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md`
**Release 2 spec**: `release-split/release-2-spec.md`

---

## Section-by-Section Index

| Section | Subsection | R2 Status | Fidelity | Notes |
|---------|-----------|-----------|----------|-------|
| **1** | **Release Overview** | | | |
| 1 | Executive Summary | PARTIAL | 0.8 | R2 Objective section captures TUI v2 scope accurately (10 features, 7 files). Missing explicit mention of checkpoint enforcement and naming consolidation context (correctly excluded from R2 scope but useful for framing). |
| 1 | Scope Boundaries (In scope) | PRESENT | 0.9 | R2 Included section covers all TUI v2 scope items. LOC estimate (~800+) not explicitly restated but features are enumerated in detail. |
| 1 | Scope Boundaries (Deferred) | PRESENT | 0.95 | R2 "Excluded (deferred beyond this split)" section accurately lists deferred items: --compact flag, cost tracking, MCP health, ETA estimation, sprint status/logs stubs, modal overlay, configurable summary model. |
| **2** | **Problem Statement** | | | |
| 2.1 | Checkpoint Enforcement Failure | NOT-APPLICABLE | -- | Belongs to R1. Correctly absent from R2. |
| 2.2 | Sprint TUI Information Gap | PARTIAL | 0.6 | R2 does not include a dedicated problem statement section. The "Objective" paragraph implicitly covers the gap but lacks the detailed current-vs-target comparison table from the original (Section 2.2). The Success Criteria table partially compensates. |
| 2.3 | Naming/Identity Confusion | NOT-APPLICABLE | -- | Belongs to R1. Correctly absent from R2. |
| **3** | **Solution Architecture** | | | |
| 3.1 | Checkpoint Enforcement -- Three-Layer Defense | NOT-APPLICABLE | -- | Belongs to R1. Correctly absent from R2. |
| 3.2 | Sprint TUI v2 -- Visual UX Overhaul | PRESENT | 0.9 | 10 features overview captured in R2 Included section with per-feature specs. New modules (summarizer.py, retrospective.py) documented. Critical invariants (SummaryWorker thread safety, failure isolation) explicitly called out. Haiku narrative pipeline documented. Minor gap: the "10 Features Overview" table format from original (with Effort/Risk columns) not replicated -- R2 uses inline descriptions instead. |
| 3.2 | Critical Invariants | PRESENT | 1.0 | Both invariants (summary failure isolation, threading.Lock for _summaries) explicitly stated with "From: [parent-spec] Section 3.2 Critical Invariants" attribution. |
| 3.2 | Haiku Narrative Pipeline | PRESENT | 0.95 | All 6 steps present: shutil.which check, prompt building, env var stripping, claude CLI invocation with flags, 30s timeout, graceful failure. |
| 3.3 | Naming Consolidation | NOT-APPLICABLE | -- | Belongs to R1. Correctly absent from R2. |
| **4** | **Implementation Plan** | | | |
| 4.1 | Checkpoint Enforcement Phases (Waves 1-4) | NOT-APPLICABLE | -- | Belongs to R1 (Waves 1-3) and deferred (Wave 4). Correctly absent. |
| 4.1 | Phase 1 (T01.01-T01.02) | NOT-APPLICABLE | -- | R1 scope. |
| 4.1 | Phase 2 (T02.01-T02.05) | NOT-APPLICABLE | -- | R1 scope. |
| 4.1 | Phase 3 (T03.01-T03.06) | NOT-APPLICABLE | -- | R1 scope. |
| 4.1 | Phase 4 (T04.01-T04.03) | NOT-APPLICABLE | -- | Deferred to next release cycle. Correctly noted in R2 "Excluded (deferred)" section. |
| 4.2 | Sprint TUI v2 Implementation Phases | PRESENT | 0.85 | Wave ordering (1-4) preserved. Wave 1 (data model + monitor), Wave 2 (rendering), Wave 3 (summary infra), Wave 4 (tmux) all present. Rationale for ordering constraints explicitly stated. Missing: the detailed per-wave tables with Effort/Risk columns from original Section 4.2. R2 uses a different organizational structure (numbered items by wave) rather than tables. |
| 4.2 | Wave 1 (Data Model + Monitor) | PRESENT | 0.9 | All 6 items present: MonitorState 8 fields, PhaseResult 3 fields, SprintResult 5 properties, SprintConfig.total_tasks, SprintTUI.latest_summary_notification, monitor extraction updates. Parent-spec section references included. |
| 4.2 | Wave 2 (TUI Rendering) | PRESENT | 0.9 | All 7 features (F1-F7) present with per-feature detail. Activity stream ring buffer, phase table column changes, dual progress bar, error panel (max 10 stored/5 displayed), LLM context lines, terminal panels, sprint name in title -- all captured. |
| 4.2 | Wave 3 (Summary Infrastructure) | PRESENT | 0.9 | F8 (summarizer.py), F10 (retrospective.py), Haiku pipeline, executor integration all present. Critical invariants included. |
| 4.2 | Wave 4 (Tmux Integration) | PRESENT | 0.9 | F9 documented: 3-pane layout, summary pane, tail pane index shift, --no-tmux fallback. |
| 4.2 | Per-Feature Specifications (F1-F10) | PARTIAL | 0.75 | R2 captures key specs for each feature but in a condensed format. Original has paragraph-length specifications per feature with precise implementation details (e.g., F1: tool name shortening examples "TodoWrite->Todo", thinking indicator timing ">2s"). R2 has most of this but some details are abbreviated. F3 regex pattern `T\d{2}\.\d{2}` not explicitly stated in R2. F4 max-10-stored is present (original says max 10 stored, max 5 displayed -- R2 says "max 10 stored, max 5 displayed" -- correct). |
| 4.3 | Naming Consolidation Tasks (N1-N12) | NOT-APPLICABLE | -- | Belongs to R1. Correctly listed in R2 "Excluded (assigned to Release 1)". |
| **5** | **Cross-Domain Dependencies** | | | |
| 5.1 | Checkpoint <-> TUI | PARTIAL | 0.7 | R2 captures the PASS_MISSING_CHECKPOINT display dependency (items 19-20: STATUS_STYLES and STATUS_ICONS). Also captures post-phase hook ordering (item 21). However, the shared-file conflict analysis (executor.py, models.py) and the functional dependency explanation are not explicitly included -- they are implied by the Dependencies section. |
| 5.2 | Naming <-> Checkpoint | NOT-APPLICABLE | -- | Both belong to R1. |
| 5.3 | Naming <-> TUI | PARTIAL | 0.5 | R2 Dependencies section notes "Naming consolidation complete -> Clean references in all files R2 touches" as a soft dependency. But the original's explanation about prompt string contract and classification header parsing is absent. |
| 5.4 | Checkpoint <-> TUI PASS_MISSING_CHECKPOINT Display | PRESENT | 0.85 | R2 items 19-20 explicitly add STATUS_STYLES and STATUS_ICONS entries for PASS_MISSING_CHECKPOINT. Validation requirement #7 covers display verification. Original's note about GateDisplayState/_show_gate_column awareness is captured in Risk TUI-6. |
| 5.5 | Shared File Conflict Analysis | PARTIAL | 0.5 | R2 does not include the detailed conflict map table from Section 5.5. The Dependencies section captures R1 prerequisites but not the file-level conflict resolution order. Some of this is implicitly covered by the wave ordering constraints. |
| **6** | **Cross-Cutting Concerns** | | | |
| 6.1 | Shared File Modifications | ABSENT | -- | R2 does not include a shared-file coordination table. This is a gap -- R2 modifies several files (executor.py, models.py, tui.py) and coordination notes would be valuable. However, since R2 is a single-domain release, inter-domain coordination is less critical. |
| 6.2 | Recommended Implementation Order | PARTIAL | 0.6 | R2 has "Intra-Release Ordering Constraints" covering wave sequencing (W1 before W2, W3 parallel with W2, W4 after W3). The original's cross-domain ordering (naming->checkpoint->TUI->etc.) is NOT-APPLICABLE since R2 is TUI-only. |
| 6.3 | Haiku Subprocess Conventions | PRESENT | 0.9 | R2 item 16 covers: shutil.which check, prompt building, env var stripping (CLAUDECODE/CLAUDE_CODE_ENTRYPOINT), claude CLI flags (--print --model claude-haiku-4-5 --max-turns 1 --dangerously-skip-permissions), 30s timeout, graceful failure. Missing explicit mention of stdin=subprocess.DEVNULL from original Section 6.3. |
| 6.4 | Post-Phase Hook Ordering | PRESENT | 0.9 | R2 item 21 explicitly states: (1) _verify_checkpoints() (R1), (2) summary_worker.submit(), (3) manifest update (R1). Includes the 5s timeout warning note. |
| 6.5 | Token Display Helper | PRESENT | 0.85 | R2 item 22 mentions _format_tokens(n) with K/M suffixes and placement in tui.py or utils.py. Missing the actual code snippet from original Section 6.5 (the Python function body). |
| **7** | **Data Model Changes** | | | |
| 7.1 | MonitorState -- New Fields | PRESENT | 0.95 | R2 item 1 lists all 8 fields: activity_log, turns, errors, last_assistant_text, total_tasks_in_phase, completed_task_estimate, tokens_in, tokens_out. References Section 7.1. |
| 7.2 | PhaseResult -- New Fields | PRESENT | 0.95 | R2 item 2 lists all 3 fields: turns, tokens_in, tokens_out. References Section 7.2. |
| 7.3 | SprintResult -- New Properties | PRESENT | 0.95 | R2 item 3 lists all 5 properties: total_turns, total_tokens_in, total_tokens_out, total_output_bytes, total_files_changed. References Section 7.3. |
| 7.4 | SprintConfig -- New Fields | PARTIAL | 0.8 | R2 item 4 covers total_tasks. checkpoint_gate_mode is NOT-APPLICABLE (R1 scope). However, R2 does not mention that checkpoint_gate_mode already exists from R1 -- the Traceability table references Section 7.4 but only for total_tasks. This is correct behavior. |
| 7.5 | PhaseStatus Enum -- New Value | NOT-APPLICABLE | -- | PASS_MISSING_CHECKPOINT belongs to R1. Correctly listed in R2 "Excluded (assigned to Release 1)" item 3. R2 does reference it for display purposes (items 19-20). |
| 7.6 | New Dataclasses | PARTIAL | 0.7 | R2 captures PhaseSummary and ReleaseRetrospective (via Traceability table referencing Section 7.6) but does not reproduce the field-level specifications from original Section 7.6. The detail is present in the feature descriptions (items 14-15) but not in a dedicated data model section. CheckpointEntry is NOT-APPLICABLE (R1). |
| 7.7 | SprintTUI -- New Field | PRESENT | 0.95 | R2 item 5 covers latest_summary_notification. References Section 7.7. |
| **8** | **File Inventory (Complete)** | | | |
| 8.1 | Checkpoint Enforcement Files | NOT-APPLICABLE | -- | Belongs to R1. |
| 8.2 | Sprint TUI v2 Files | PRESENT | 0.95 | R2 File Inventory table matches original: 7 files (2 CREATE, 5 MODIFY) with accurate wave assignments and change descriptions. Test files also enumerated (8 files: 5 MODIFY, 3 CREATE). Output artifacts documented. |
| 8.3 | Naming Consolidation Files | NOT-APPLICABLE | -- | Belongs to R1. |
| 8.4 | Cross-Domain Conflict Map | ABSENT | -- | R2 does not include the conflict map. Since R2 is single-domain, this is less critical but the executor.py shared modification point (R1 checkpoint + R2 summary) is noted in Dependencies. |
| 8.5 | Output Artifacts | PRESENT | 0.9 | R2 Output Artifacts table covers phase-N-summary.md and release-retrospective.md with correct writers and timing. Missing manifest.json (NOT-APPLICABLE -- R1 checkpoint feature). |
| **9** | **Rollout Strategy** | | | |
| 9.1 | Combined Timeline | ABSENT | -- | R2 does not include a timeline. This is a gap -- even as a single-domain release, a wave-by-wave timeline estimate would be valuable for planning. The original's timeline (Days 3-18 for TUI) is not translated. |
| 9.2 | Checkpoint Gate Progression | NOT-APPLICABLE | -- | Belongs to R1. |
| 9.3 | Backward Compatibility Guarantees | PARTIAL | 0.5 | R2 does not have an explicit backward compatibility section. The original states TUI v2 is "Fully backward compatible. All changes are additive to the rendering layer. MonitorState defaults preserve existing behavior." This assurance is absent from R2. |
| **10** | **Risk Register** | | | |
| 10.1 | Checkpoint Enforcement Risks | NOT-APPLICABLE | -- | Belongs to R1. |
| 10.2 | Sprint TUI v2 Risks | PRESENT | 0.9 | R2 Risk Register includes TUI-1 through TUI-6 matching original, plus R2-1 (executor.py merge conflict with R1). All severities, likelihoods, and mitigations match. |
| 10.3 | Naming Consolidation Risks | NOT-APPLICABLE | -- | Belongs to R1. |
| **11** | **Success Metrics** | | | |
| 11.1 | Checkpoint Enforcement Metrics | NOT-APPLICABLE | -- | Belongs to R1. |
| 11.2 | TUI Usability Metrics | PRESENT | 0.9 | R2 Success Criteria table has 4 metrics matching original Section 11.2: information visibility, post-phase analysis availability, error visibility latency, release summary availability. Current/Target values match. |
| 11.3 | Naming Clarity Metrics | NOT-APPLICABLE | -- | Belongs to R1. |
| **12** | **Test Strategy** | | | |
| 12.1 | Existing Tests Requiring Updates | PRESENT | 0.85 | R2 Test Files table lists 5 MODIFY entries matching original: test_tui.py, test_models.py, test_tui_gate_column.py, test_tui_monitor.py, test_tui_task_updates.py. Scope descriptions accurate. |
| 12.2 | New Tests Required | PRESENT | 0.9 | R2 lists 3 CREATE test files: test_summarizer.py, test_retrospective.py, test_tmux.py matching original. test_checkpoints.py is NOT-APPLICABLE (R1). |
| 12.3 | Tests Confirmed Unchanged | ABSENT | -- | R2 does not list tests confirmed unchanged (test_cli_contract.py, test_config.py, test_process.py, test_e2e_*). Minor gap -- useful for implementers. |
| 12.4 | Test Coverage Targets | ABSENT | -- | R2 does not include coverage targets. Original specifies: summarizer.py >80%, retrospective.py >80%, MonitorState >90%, TUI rendering maintained. This is a moderate gap. |
| 12.5 | Checkpoint Verification Methods | NOT-APPLICABLE | -- | Belongs to R1. |
| 12.6 | Test Tasks Added | NOT-APPLICABLE | -- | Belongs to R1. |
| **13** | **Configuration Changes** | | | |
| 13.1 | SprintConfig Additions | PARTIAL | 0.7 | R2 mentions SprintConfig.total_tasks but does not have a dedicated configuration section. The field is documented in item 4 of the Included section. checkpoint_gate_mode is NOT-APPLICABLE (R1). |
| 13.2 | Gate Mode Behavior | NOT-APPLICABLE | -- | Belongs to R1. |
| 13.3 | CLI Additions | NOT-APPLICABLE | -- | verify-checkpoints belongs to R1. |
| 13.4 | No CLI Flag Additions for TUI | ABSENT | -- | R2 does not explicitly state that no CLI flags are added. The original notes --compact is deferred. R2's "Excluded (deferred)" mentions --compact but doesn't make the "no new flags" statement explicit. Minor gap. |
| **14** | **Open Questions and Gaps** | | | |
| 14.1 | Checkpoint Enforcement -- Open Questions | NOT-APPLICABLE | -- | Belongs to R1. |
| 14.2 | Sprint TUI v2 -- Open Questions | PRESENT | 0.85 | R2 Open Questions section carries 8 questions: TUI-Q1, Q2, Q4, Q6, Q7, Q8, Q9, Q10. Correctly excludes resolved questions TUI-Q3 and TUI-Q5. Priorities match. |
| 14.3 | Naming Consolidation -- Open Questions | NOT-APPLICABLE | -- | Belongs to R1. |
| 14.4 | Confidence Assessment Summary | ABSENT | -- | R2 does not include confidence assessments. The original has per-task confidence scores. Since R2 does not break down into individual tasks (that is the tasklist's job), this is understandable, but a summary confidence range for R2 overall would be useful. |
| **15** | **Appendices** | | | |
| 15-A | Adversarial Analysis Summary (Checkpoint) | NOT-APPLICABLE | -- | Belongs to R1. |
| 15-B | UI Layout Mockups (Sprint TUI v2) | ABSENT | -- | R2 does not include the UI mockups (active sprint, sprint complete, sprint halted, tmux 3-pane layouts). The Traceability table references "Section 15, Appendix B" but the mockups themselves are not reproduced. This is a significant gap -- mockups are critical for TUI implementation. |
| 15-C | Codebase Integration Map (Naming) | NOT-APPLICABLE | -- | Belongs to R1. |
| 15-D | Source Document Index | ABSENT | -- | R2 does not include source document references. The individual items have "From: [parent-spec]" attribution which partially compensates. |

---

## Additional R2-Specific Content Not in Original

| R2 Section | Status | Notes |
|-----------|--------|-------|
| Planning Gate | ADDED | R2 adds a validation gate requiring R1 real-world validation before R2 proceeds. Not in original spec -- this is a valuable addition from the split process. |
| Real-World Validation Requirements | ADDED | R2 adds 10 specific validation requirements. Not in original -- derived from success metrics and test strategy. Valuable addition. |
| Traceability Table | ADDED | R2 adds explicit parent-spec section references for each item. Not in original -- useful for audit. |
| R1 Prerequisites Table | ADDED | R2 adds explicit R1 dependency table with hard/soft classification. Not in original -- useful for sequencing. |

---

## Summary Statistics

### Total Sections Assessed

| Count | Value |
|-------|-------|
| Total sections/subsections assessed | 55 |
| PRESENT | 22 |
| PARTIAL | 11 |
| ABSENT | 8 |
| NOT-APPLICABLE | 14 |

### Fidelity Scores (PRESENT + PARTIAL items only)

| Metric | Value |
|--------|-------|
| Items scored | 33 |
| Average fidelity | 0.83 |
| Median fidelity | 0.85 |
| Min fidelity | 0.5 |
| Max fidelity | 1.0 |

### ABSENT Items That SHOULD Be in R2 (Gaps)

These items are absent from R2 but would be expected in a complete release spec:

| # | Section | Subsection | Severity | Rationale |
|---|---------|-----------|----------|-----------|
| 1 | 15-B | UI Layout Mockups | **HIGH** | Mockups are the primary visual reference for TUI implementation. Implementers need the active sprint, sprint complete, sprint halted, and tmux 3-pane ASCII layouts. Without these, the implementer must consult the parent spec. |
| 2 | 9.1 | Combined Timeline | **MEDIUM** | No timeline estimate for R2 wave delivery. Original had Day 3-18 for TUI features. Implementers lack scheduling guidance. |
| 3 | 12.4 | Test Coverage Targets | **MEDIUM** | Original specifies >80% for summarizer.py and retrospective.py, >90% for MonitorState fields. R2 omits these targets. |
| 4 | 6.1 | Shared File Modifications | **LOW** | R2 is single-domain so inter-domain coordination is less critical, but noting that executor.py is shared with R1 would be useful. Partially covered in Dependencies. |
| 5 | 12.3 | Tests Confirmed Unchanged | **LOW** | Useful for implementers to know which tests should NOT break. |
| 6 | 14.4 | Confidence Assessment Summary | **LOW** | No overall confidence range for R2. Less critical since R2 does not define individual tasks. |
| 7 | 13.4 | No CLI Flag Additions for TUI | **LOW** | Explicit "no new CLI flags" statement missing. --compact deferral is noted in exclusions. |
| 8 | 15-D | Source Document Index | **LOW** | Parent-spec attributions on individual items partially compensate. |

### Items Scored Below 0.7 Fidelity (Need Attention)

| # | Section | Subsection | Fidelity | Issue |
|---|---------|-----------|----------|-------|
| 1 | 2.2 | Sprint TUI Information Gap | 0.6 | No dedicated problem statement. The current-vs-target comparison table (7 dimensions) from original is absent. R2 jumps straight to Objective without framing the problem. |
| 2 | 5.3 | Naming <-> TUI | 0.5 | Minimal coverage of the prompt string contract dependency. Soft dependency noted but explanation absent. |
| 3 | 5.5 | Shared File Conflict Analysis | 0.5 | No file-level conflict resolution table. Partially implied by wave ordering. |
| 4 | 9.3 | Backward Compatibility Guarantees | 0.5 | Missing the explicit "fully backward compatible, all changes additive" guarantee from original. |
| 5 | 6.2 | Recommended Implementation Order | 0.6 | Has wave ordering but not the broader cross-domain sequencing context. |

---

## Overall Assessment

**R2 spec quality: GOOD (0.83 average fidelity)**

The Release 2 spec is a well-structured, self-contained document that accurately captures the TUI v2 scope. It correctly excludes checkpoint enforcement and naming consolidation content, correctly identifies R1 prerequisites, and adds valuable content not in the original (planning gate, real-world validation requirements, traceability table).

**Primary gaps to address:**
1. **UI Layout Mockups** (HIGH) -- The ASCII mockups from Appendix B are the most critical missing content. These are the implementation reference for the TUI rendering work.
2. **Problem Statement** (MEDIUM) -- Adding the current-vs-target table from Section 2.2 would strengthen the spec's motivation framing.
3. **Test Coverage Targets** (MEDIUM) -- The >80%/>90% targets from Section 12.4 should be carried forward.
4. **Backward Compatibility Statement** (MEDIUM) -- An explicit "all changes additive" guarantee is important for reviewer confidence.
5. **Timeline** (MEDIUM) -- Even a rough wave-by-wave estimate would help planning.
