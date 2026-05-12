# Quality Validation Report

**Document:** `v3.7-task-unified-v2-release-spec.md`
**Validator:** rf-qa-qualitative (Claude Opus 4.6)
**Date:** 2026-04-02
**Phase:** doc-qualitative (release spec)
**Fix cycle:** N/A

---

## Overall Assessment

- **Rating:** NEEDS REVISION
- **Confidence:** 82%
- **Key strengths:** Thorough root cause analysis for checkpoint enforcement; well-structured three-layer defense model; excellent cross-domain dependency analysis with file-level conflict mapping; honest confidence assessments with the highest-risk task (T03.03) clearly flagged; comprehensive open questions catalog
- **Key concerns:** Scope is ambitious for a single release; task count discrepancy (14 vs stated 15); TUI v2 has no tasklist/task breakdown comparable to checkpoint enforcement; naming consolidation ordering creates a fragile window; several implicit dependencies are documented but not resolved

---

## Dimension Results

### 1. Logical Coherence
**Rating:** PASS (with minor notes)

**Findings:**

The three domains connect logically and serve a coherent narrative: the sprint pipeline had a reliability gap (checkpoint enforcement), a visibility gap (TUI), and a consistency gap (naming). The document correctly identifies that these are three independent problems with overlapping implementation surfaces.

**Cross-references are accurate:**
- Section 5 (Cross-Domain Dependencies) correctly identifies `executor.py` as the highest-conflict file (modified by both checkpoint and TUI domains)
- Section 7.4 conflict map is internally consistent with Section 5
- The rollout timeline in Section 8.1 respects the dependency ordering stated in Section 5: checkpoint first on shared files, then TUI, with naming interleaved at a low-conflict window
- Phase dependency chains within checkpoint enforcement are correct: Phase 2 depends on Phase 1 (T01.02 establishes the call site pattern), Phase 3 depends on Phase 2 (checkpoints.py exists), Phase 4 depends on Phases 1-3 (interim coverage)

**Implementation order makes sense given dependencies:**
- Checkpoint Wave 1 (Day 1) has no dependencies -- correct to start first
- Naming consolidation (Day 1-3) is placed after checkpoint Wave 1 but before Wave 2 -- this is correct because both modify `process.py:170` and the spec says they should not be concurrent
- TUI Wave 1 (Day 3-7) starts after naming to avoid conflicts on shared model files -- reasonable
- The spec correctly defers Wave 4 (tasklist normalization) to "next release" because it is a breaking change

**One logical subtlety handled well:** The document explains that T02.04 *replaces* T01.02's `_warn_missing_checkpoints()` with the full `_verify_checkpoints()` gate. This is a progressive refinement pattern where Wave 1 code is intentionally temporary. This is called out in both T02.04's steps and in CE-Q2 (cross-wave rollback concern).

---

### 2. Scope Appropriateness
**Rating:** WARN

**Findings:**

This is the primary concern. Three domains in a single release creates meaningful risk:

**Quantitative scope assessment:**
- Checkpoint enforcement: 15 tasks (actually 14 -- see Dimension 4), ~580 LOC, 7 files, 4 waves
- TUI v2: 10 features, 7 files (2 new), unquantified LOC (this is itself a gap -- see Dimension 5)
- Naming consolidation: 12 tasks, ~21 files, mechanical search-and-replace
- **Total unique files touched:** At least 18 distinct files across the three domains, with 3 files modified by multiple domains

**Scope concerns:**
1. **TUI v2 is enormous on its own.** F8 (Post-Phase Summary) alone introduces a new module, background threading, NDJSON parsing, Haiku subprocess calls, and tmux integration. F10 (Release Retrospective) is similarly complex. These two features have HIGH effort/risk ratings. Bundling them with checkpoint enforcement AND naming consolidation is aggressive.

2. **Domain boundaries are clean** -- the spec does a good job keeping the three domains conceptually separate. The cross-domain dependency section (Section 5) is thorough and the file conflict map (Section 7.4) provides clear resolution ordering. This mitigates the scope risk somewhat.

3. **The spec correctly defers Wave 4** (checkpoint normalization) to next release. It also defers 8 TUI features (--compact, cost tracking, etc.). These are good scope discipline decisions.

4. **Naming consolidation is low-risk but high-blast-radius.** Touching 21+ files for a rename is mechanical but any missed reference breaks the sprint pipeline silently. This should be its own atomic commit with full grep verification.

**Verdict:** The scope is feasible but aggressive. The clean domain boundaries and explicit conflict resolution ordering make it manageable, but the implementation plan should treat the three domains as independently shippable increments with their own merge points, not as one monolithic release.

---

### 3. Technical Feasibility
**Rating:** PASS (with notes)

**Findings:**

**LOC estimates are realistic for checkpoint enforcement:**
- Wave 1 at ~60 LOC (prompt string additions + a warning function) -- reasonable
- Wave 2 at ~120 LOC (new module + enum + logging method + integration) -- reasonable
- Wave 3 at ~200 LOC (manifest, recovery, CLI subcommand, executor wiring) -- reasonable
- Wave 4 at ~200 LOC (SKILL.md rule changes) -- reasonable for documentation/template changes

**TUI v2 has NO LOC estimate.** This is a gap. The analysis identifies effort as "High" for F8 and F10 but does not provide LOC estimates. Given the scope (two new modules, background threading, NDJSON parsing, Haiku subprocess, tmux changes, 8 new MonitorState fields, 3 new PhaseResult fields, 5 new SprintResult properties, comprehensive TUI layout rewrite), a rough estimate of 800-1200 LOC for TUI v2 is likely. This makes the release total closer to 1400-1800 LOC, not 580.

**Risk assessments are accurate:**
- T03.03 (auto-recovery) at 75% confidence is correctly identified as highest-risk. The evidence file format consistency assumption is real.
- F8 and F10 marked as High effort/risk is correct -- subprocess management + threading + NDJSON parsing is genuinely complex.
- TUI-4 (tmux pane index migration) is a real concern -- hardcoded pane indices are fragile.

**No hidden complexity cliffs detected** beyond what the spec already acknowledges. The SummaryWorker threading model is described in sufficient detail (daemon threads, exception isolation, wait_all with timeout).

**One technical concern:** The Haiku narrative pipeline strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` from the environment before spawning the subprocess. This is necessary to prevent recursive Claude Code invocations. Good engineering, but the spec does not discuss what happens if other environment variables (API keys, proxy settings) are needed by the Haiku call. This is likely a non-issue in practice but should be acknowledged.

---

### 4. Contradiction Detection
**Rating:** WARN

**Findings:**

I performed a systematic contradiction check across all sections.

**Verified consistency:**
- File counts: "7 files (1 new, 6 modified)" for checkpoint enforcement -- verified against Section 7.1 file inventory: process.py, executor.py, checkpoints.py (NEW), models.py, logging_.py, commands.py, SKILL.md = 7 files, 1 new. Consistent.
- "10 features across 7 files (5 modified, 2 new)" for TUI -- verified against Section 7.2: models.py, monitor.py, tui.py, executor.py, tmux.py (5 modified) + summarizer.py, retrospective.py (2 new) = 7 files. Consistent.
- LOC: "~580 LOC across all 4 waves" -- verified against per-wave estimates: ~60 + ~120 + ~200 + ~200 = ~580. Consistent.
- Checkpoint write rate: "86% (6/7 phases)" used consistently in Sections 2.1, 10.1, and the domain analysis.
- TUI F2 removes Tasks column and adds Turns/Output -- consistently stated across Sections 2.2, 3.2, and 4.2.

**Contradiction found:**

**IMPORTANT -- Task count discrepancy.** The spec states "15 tasks total" for checkpoint enforcement in Section 1 ("15 tasks across 4 phases"), Section 4.1 overview ("4 phases (waves), 15 tasks total"), and the domain analysis. However, enumerating the actual tasks: T01.01-T01.02 (2) + T02.01-T02.04 (4) + T03.01-T03.05 (5) + T04.01-T04.03 (3) = **14 tasks**, not 15. One task is either missing from the enumeration or the count is wrong.

**Checkpoint report paths reference OntRAG directory.** The checkpoint report paths in Phases 1-4 reference `.dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/CP-CE-P0N-END.md`. This is the path structure from the OntRAG sprint, not from v3.7-task-unified-v2. These paths appear to be copy-pasted from the original checkpoint enforcement tasklist without updating for the v3.7 release context. While these are template paths that would be parameterized at runtime, having them reference a different release's directory structure is misleading.

---

### 5. Completeness of Actionability
**Rating:** WARN

**Findings:**

**Checkpoint enforcement: HIGHLY ACTIONABLE.** Each of the 14 tasks has target file, steps (with PLANNING/EXECUTION/VERIFICATION labels), acceptance criteria, rollback commands, confidence percentages, dependency lists, and risk drivers. An implementer could start building from Section 4.1 today.

**TUI v2: MODERATELY ACTIONABLE.** The spec provides feature descriptions, data model changes, and a wave ordering, but:
1. **No task-level breakdown.** Checkpoint enforcement has T01.01-T04.03 with full metadata. TUI v2 has features (F1-F10) with descriptions but no comparable task breakdown with steps, acceptance criteria, or verification methods. An implementer would need to decompose features into tasks before starting.
2. **No LOC estimates.** The checkpoint domain has per-wave LOC estimates. TUI has none.
3. **Several open questions are blockers.** TUI-Q1 (prompt_preview location), TUI-Q4 (monitor reset interface change), and TUI-Q10 (config.py not in file list) would force an implementer to stop and make design decisions before proceeding. These should be resolved in the spec, not left as open questions.

**Naming consolidation: HIGHLY ACTIONABLE.** Section 4.3 provides a complete task table with targets, changes, risk levels, and dependency ordering. The mechanical nature of the work (search-and-replace) means the task descriptions are sufficient.

**Gaps that would force an implementer to stop:**
1. TUI-Q1: Where does `prompt_preview` go? This affects F5 implementation.
2. TUI-Q4: How does `reset()` get the phase file path? This affects F3 implementation.
3. TUI-Q10: `config.py` not in modified files list but needs task pre-scan integration.
4. CE-Q1: No test file creation tasks in the checkpoint enforcement plan. The file inventory lists no `tests/` files.
5. The TUI section does not specify whether the `SummaryWorker` class lives in `executor.py` or `summarizer.py`. Section 3.2 says "SummaryWorker class (in executor.py)" and the file inventory says "(SummaryWorker in executor)". This is stated but inconsistent with the heading "summarizer.py -- Three components" which lists SummaryWorker as component 3.

---

### 6. Risk Assessment
**Rating:** PASS

**Findings:**

The risk register (Section 9) is comprehensive with 17 risks across three domains. Each risk has severity, likelihood, and mitigation.

**Risks appropriately identified:**
- CE-2 (path resolution false positives) is correctly rated Medium severity/Medium likelihood and mitigated by shadow mode.
- TUI-2 (thread safety) is correctly flagged with honest but weak mitigation.
- NC-1 (missing reference) is the most likely naming risk and is correctly mitigated by comprehensive grep.

**Unacknowledged risks:**

1. **Integration testing gap.** The spec describes per-task verification methods but no end-to-end integration test plan. Given three domains modifying shared files, an integration test sprint should be explicitly planned as a gated milestone.

2. **Haiku API cost.** Each sprint execution will make N+1 Haiku API calls (one per phase + one for retrospective). For a 7-phase sprint, that is 8 API calls. The spec does not acknowledge cost or provide a way to disable narrative generation independently of summary generation.

3. **Rollback interdependency.** CE-Q2 identifies this but the spec does not provide a concrete Wave 2 rollback procedure that restores Wave 1 state.

---

### 7. Architecture Quality
**Rating:** PASS

**Findings:**

**Three-layer checkpoint defense: NOT overengineered.** The minimum viable set (Solution 1 + Solution 3) is explicitly identified. Each layer addresses a different root cause. The adversarial analysis demonstrates complementary rather than redundant coverage.

**TUI scope: Reasonable but front-loaded.** The wave ordering is sound: data model first, rendering second, new modules third, tmux last. The highest-risk features (F8, F10) are correctly placed in Wave 3.

**Haiku narrative generation: Justified.** Graceful degradation (summary without narrative on failure) means the feature adds value without fragility. The `claude --print` approach avoids adding an API dependency.

**One concern:** The spec uses `--dangerously-skip-permissions` for the Haiku subprocess. In context this is acceptable (read-only `--print` with `--max-turns 1`), but the rationale should be documented explicitly.

---

### 8. Naming/Migration Safety
**Rating:** WARN

**Findings:**

**The naming consolidation plan is safe in isolation** but creates risk when executed alongside the other two domains.

**Safety strengths:**
- Correct dependency ordering (N1 -> N2 -> N3 -> N4 -> N5+N6 -> N7-N10 -> N11)
- Three-tier file classification correctly prioritizes highest-impact files
- Plan includes `make sync-dev` as final step

**Safety concerns:**

1. **Timing window overlap.** The rollout timeline places naming at "Day 1-3" overlapping with Checkpoint Wave 1 (Day 1) and Wave 2 (Day 2-5). The resolution order is documented but must be enforced by commit ordering.

2. **Classification header decision unresolved (NC-Q3).** The header `SC:TASK-UNIFIED:CLASSIFICATION` is used for telemetry. The spec leaves this as an open question. This should be decided before implementation.

3. **No end-to-end verification task after rename.** The naming tasks do not include "Run sprint execution and verify the renamed command resolves correctly." Given unresolved NC-Q4 (subprocess resolution mechanism), this is critical.

4. **Historical artifacts correctly deferred.** `.dev/releases/complete/` not updated is acceptable and explicitly noted.

---

## Contradictions Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Sections 1, 4.1 | Task count stated as "15 tasks" but actual enumeration yields 14 (2+4+5+3). Either a task is missing from the spec or the count is wrong. | Recount and correct. If the count should be 14, update all references. If a task is missing, add it. |
| 2 | MINOR | Section 4.1 checkpoint report paths | All four phase checkpoint paths reference `.dev/releases/current/feature-Ont-RAG/feature-OntRAG_r0-r1/checkpoints/` which is the OntRAG sprint directory, not the v3.7 release directory. These are copy-pasted from the source tasklist. | Update to use parameterized paths or paths appropriate for the v3.7 release context, or add a note that these are illustrative paths from the original incident. |

---

## Recommended Revisions

**Priority 1 (Must fix before sprint planning):**

1. **Fix task count discrepancy.** Verify whether checkpoint enforcement has 14 or 15 tasks and correct all references (Sections 1, 4.1).

2. **Resolve TUI-Q1, TUI-Q4, TUI-Q10 before implementation.** These open questions are implementation blockers, not "nice to resolve later" items:
   - TUI-Q1: Decide where `prompt_preview` field goes (recommend: `Phase` dataclass, populated by executor before passing to monitor)
   - TUI-Q4: Decide how `reset()` receives phase file path (recommend: add `phase_file` parameter to `reset()`)
   - TUI-Q10: Add `config.py` to the TUI modified files list

3. **Resolve NC-Q3 (classification header).** Decide whether `SC:TASK-UNIFIED:CLASSIFICATION` changes to `SC:TASK:CLASSIFICATION` or is retained. Document the decision and its implications.

4. **Add end-to-end verification task for naming consolidation.** After N11 (sync), add N12: "Run `superclaude sprint run` on a test tasklist and verify `/sc:task` resolves correctly through the full subprocess chain."

**Priority 2 (Should fix before sprint planning):**

5. **Add LOC estimates for TUI v2.** Even rough estimates (per-wave or per-feature) help with timeline planning. Current spec gives the impression that v3.7 is "~580 LOC" when the real total is likely 1400-1800 LOC.

6. **Create task-level breakdown for TUI v2.** The checkpoint enforcement domain has full MDTM tasks. The TUI domain has only feature descriptions. For sprint execution, TUI features need to be decomposed into tasks with acceptance criteria and verification methods. This could be a separate tasklist document.

7. **Add integration test milestone.** After all three domains are implemented, add a gated milestone: "Run a full sprint execution (3+ phases) and verify: checkpoint gate fires correctly in shadow mode, TUI renders all new fields, naming resolves through subprocess chain, no regressions in existing tests."

8. **Address test strategy for checkpoint enforcement (CE-Q1).** Add `tests/sprint/test_checkpoints.py` to the file inventory and add a test creation task to the checkpoint implementation plan.

**Priority 3 (Nice to have):**

9. **Clarify SummaryWorker location.** Section 3.2 and the file inventory both say it lives in `executor.py`, but the "summarizer.py -- Three components" description lists it as component 3 of summarizer.py. Clarify that summarizer.py has 2 components and executor.py has SummaryWorker.

10. **Document `--dangerously-skip-permissions` rationale.** Add a one-line comment in the Haiku pipeline section explaining why this flag is necessary.

11. **Add Haiku disable mechanism.** Consider adding a config option to disable narrative generation (for environments without API access or cost-sensitive deployments).

---

## Red Flags

| # | Severity | Description |
|---|----------|-------------|
| 1 | WARN | **No TUI tasklist.** Checkpoint enforcement has 14 detailed tasks; TUI v2 has zero. The TUI domain cannot be sprint-executed without first generating a tasklist. This is the single biggest gap in the spec. |
| 2 | WARN | **Naming + Checkpoint timing overlap on process.py.** Day 1-3 naming consolidation overlaps Day 1 checkpoint Wave 1 on the same file. The spec documents this but relies on discipline, not automation, to enforce ordering. |
| 3 | LOW | **NC-Q4 unresolved.** Whether Claude Code resolves commands by filename or frontmatter `name` field is still unknown. The entire naming consolidation plan assumes filename-based resolution (renaming `task-unified.md` to `task.md`). If resolution is frontmatter-based, the current state already works and the file rename is unnecessary but harmless. If resolution is filename-based, the rename is critical. This needs testing before the naming work begins. |
| 4 | LOW | **No rollback plan for cross-domain failures.** If checkpoint Wave 2 is deployed and breaks, rolling back requires restoring Wave 1 state. If naming + checkpoint are both partially deployed, rollback complexity increases. The spec has per-task rollback commands but no cross-domain rollback strategy. |

---

## Summary

| Dimension | Rating |
|-----------|--------|
| 1. Logical Coherence | PASS |
| 2. Scope Appropriateness | WARN |
| 3. Technical Feasibility | PASS |
| 4. Contradiction Detection | WARN |
| 5. Completeness of Actionability | WARN |
| 6. Risk Assessment | PASS |
| 7. Architecture Quality | PASS |
| 8. Naming/Migration Safety | WARN |

**Dimensions passed:** 4 of 8
**Dimensions warned:** 4 of 8
**Dimensions failed:** 0

The spec is well-structured, thoroughly researched, and architecturally sound. The three-layer checkpoint defense is the strongest section. The primary gaps are: (1) the TUI domain lacks the task-level detail that checkpoint enforcement provides, (2) several open questions are actually implementation blockers that should be resolved in the spec, (3) the task count discrepancy needs correction, and (4) the cross-domain timing on shared files needs stricter enforcement than documentation alone provides.

**Verdict: NEEDS REVISION before sprint planning, but no fundamental rework required.** The Priority 1 items (task count fix, blocker question resolution, naming verification task) can be addressed in 1-2 hours. The Priority 2 items (TUI tasklist generation, LOC estimates, integration milestone) require more effort but are essential for sprint execution.

---

*End of quality validation report.*
