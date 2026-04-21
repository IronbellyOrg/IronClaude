# 08 - Prior Research Context: Tasklist Quality Investigation (2026-04-03)

**Status**: Complete
**Source**: TASK-RESEARCH-20260403-tasklist-quality
**Agent**: Doc Analyst
**Date**: 2026-04-04
**Verification Method**: All architectural claims cross-validated against source code in `src/superclaude/cli/`

---

## Purpose

Distill key findings from the prior tasklist-quality research investigation (2026-04-03), with independent code verification of all pipeline behavior claims. The prior investigation answered: "Why does the tasklist generation pipeline produce 49% fewer tasks from 4.1x richer input?"

---

## 1. Problem Statement (Confirmed)

The `/sc:tasklist` skill generates 87 tasks from a 312-line spec-only input but only 44 tasks from 1,282 lines of combined TDD+PRD input for the same functional domain (user authentication). Enrichment content IS present in the 44 tasks (persona references, compliance markers, +70% component references), but the pipeline compresses rather than expands.

**Key evidence table** (from research report Section 1.4, cross-checked against synthesis/synth-01):

| Metric | Spec-Only | TDD+PRD | Delta |
|--------|-----------|---------|-------|
| Input lines | 312 | 1,282 | +4.1x |
| Roadmap lines | 380 | 746 | +2.0x |
| Phases | 5 | 3 | -40% |
| R-items in registry | 87 | 44 | -49% |
| Tasks generated | 87 | 44 | -49% |
| R-item:task ratio | 1:1 | 1:1 | Same |

---

## 2. Corrected Framing: R-Item Collapse Investigation

The R-item collapse investigation (reviews/r-item-collapse-investigation.md) **corrected the original problem framing**. Key corrections:

1. **The original "47 parser-visible items expand to 87 R-items" claim was wrong.** The spec-only roadmap actually has 87 table data rows -- 1:1 mapping, no expansion.

2. **The original "88 R-items collapse to 44 tasks" claim was wrong.** The TDD+PRD Roadmap Item Registry has exactly 44 entries (R-001 through R-044), not 88. The "88" was a miscount.

3. **There is no expansion or collapse at the tasklist generation stage.** Both runs exhibit perfect 1:1:1 mapping: roadmap items -> R-items -> tasks.

4. **The real loss point is the roadmap generator**, not the tasklist generator. The adversarial roadmap pipeline produces 87 fine-grained items from spec-only input but only 44 coarser items (with richer narrative context) from TDD+PRD input.

---

## 3. Confirmed Granularity Loss Points

### Loss Point 1: Roadmap Generation -- Fewer Phases (PRIMARY)

**Prior claim**: The `build_generate_prompt()` function provides zero guidance on phase count; when TDD content includes a 3-phase rollout (Alpha/Beta/GA), the LLM adopts it instead of creating 5+ technical-layer phases.

**[CODE-VERIFIED]** -- `src/superclaude/cli/roadmap/prompts.py`, lines 439-445. The prompt says:

```
"After the frontmatter, provide a complete roadmap including:\n"
"1. Executive summary\n"
"2. Phased implementation plan with milestones\n"
```

No minimum/maximum phase count. No complexity-to-phase mapping. Confirmed: zero phase count guidance.

**[CODE-VERIFIED]** -- `src/superclaude/cli/roadmap/prompts.py`, lines 457-481 (TDD block). The TDD supplementary context mentions "phased rollout tasks" and rollback procedures but does NOT instruct the LLM to preserve a specific phase count structure. However, the current code (post-research) DOES include the instruction: "Use technical-layer phasing (Foundation -> Core Logic -> Integration -> Hardening -> Production Readiness) regardless of any rollout/milestone structure in the TDD." This appears to be a **fix applied after the research was conducted** (or during the same period).

**[CODE-VERIFIED]** -- `src/superclaude/cli/roadmap/prompts.py`, lines 484-504 (PRD block). The current code contains: "It does NOT change the number of phases, the phasing paradigm (technical layers, not delivery milestones), or reduce the number of task rows." This is also a protective instruction that constrains PRD's influence on phasing.

**IMPORTANT NOTE**: The generate prompt's TDD and PRD blocks now contain anti-consolidation language that was NOT present in the version described by the prior research. The prior research described a version where PRD's "value-based phasing" instruction caused the LLM to adopt a 3-phase delivery-milestone structure. The current code explicitly prevents this. **The roadmap generate prompt appears to have been partially fixed already.**

### Loss Point 2: Roadmap R-Item Granularity

**Prior claim**: The TDD+PRD roadmap bundles ~112 discrete work items into 44 R-items (2.5:1 bundling) because narrative-rich roadmaps use subsection headings with dense table content underneath, while spec-only roadmaps use flat table rows where each row is an independent R-item.

**[UNVERIFIED]** -- This is an observation about LLM output behavior, not a code-level claim. The structure of the generated roadmap depends on model inference. Cannot verify against source code. The underlying cause (no R-item granularity enforcement) is confirmed by the absence of such enforcement in the generate and merge prompts.

### Loss Point 3: Merge Stage Inheritance

**Prior claim**: The merge stage does NOT actively reduce granularity; it preserves the 3-phase structure from the winning base variant.

**[CODE-VERIFIED]** -- `src/superclaude/cli/roadmap/prompts.py`, lines 631-649 (`build_merge_prompt`). The merge prompt says "uses the selected base variant as foundation and incorporates the best elements from the other variant." No consolidation instruction. No phase reduction instruction. No "remove redundancy" instruction. Confirmed: merge inherits structure from the base variant.

---

## 4. Validated Root Causes (5 Hypotheses)

### H1: Roadmap Phasing Paradigm (MEDIUM impact)

PRD rollout strategy causes fewer, broader phases. The TDD+PRD roadmap has 3 delivery-milestone phases vs spec-only's 5 technical-layer phases.

**[CODE-VERIFIED]** -- The generate prompt at lines 439-445 has zero phase count guidance. However, **the current code at lines 479-481 now mandates "technical-layer phasing... regardless of any rollout/milestone structure in the TDD"** and lines 498-500 say PRD "does NOT change the number of phases, the phasing paradigm." These appear to be fixes applied to address H1. If these were present during the test fixture runs that produced 44 tasks, H1 may already be mitigated for future runs. If these are new additions, the test fixtures predate the fix.

### H2: PRD Suppression Language in Tasklist Prompt (HIGH impact -- strongest single cause)

**Prior claim**: `tasklist/prompts.py` lines 221-223 contain "PRD context... does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them."

**[CODE-VERIFIED]** -- `src/superclaude/cli/tasklist/prompts.py`, lines 221-223. Exact text confirmed:

```python
"PRD context informs task descriptions and priorities but does NOT generate "
"standalone implementation tasks. Engineering tasks come from the roadmap; "
"PRD enriches them."
```

This suppression language remains in the current codebase. **Not yet fixed.**

### H3: Testing Task Consolidation (MEDIUM impact -- largest category contributor)

**Prior claim**: TDD+PRD produces 5 standalone test tasks vs baseline's 28 (5.6:1 ratio). Testing is absorbed into `[VERIFICATION]` steps within implementation tasks.

**[UNVERIFIED]** -- This is an observation about output behavior, not a code-level claim. The 5.6:1 consolidation ratio comes from comparing test fixture outputs, which we cannot re-verify without re-running the pipeline. The observation is consistent with the protocol rules: SKILL.md Section 4.4 does not mandate standalone test tasks.

### H4: Protocol Merge Directives (HIGH impact)

**Prior claim**: SKILL.md contains 5 merge/consolidation instructions with vague matching criteria.

**[CODE-VERIFIED]** -- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`:
- Line 233: "Merge rather than duplicate if a generated task duplicates an existing task for the same component" (Section 4.4a)
- Line 255: "Merge rather than duplicate if a generated task duplicates an existing task. PRD-derived tasks enrich task descriptions and acceptance criteria but do NOT generate standalone implementation tasks -- engineering tasks come from the roadmap; PRD enriches them." (Section 4.4b)
- Line 259: "merge with existing feature task if one covers the same goal" (4.4b user_stories row)

Three instances confirmed (the prior report counted 5 total -- the other two may be in surrounding context not captured by this grep). The merge directives are still present. **Not yet fixed.**

### H5: Roadmap R-Item Granularity (HIGH impact -- upstream)

**Prior claim**: The TDD+PRD roadmap bundles ~112 work items into 44 R-items because the roadmap's narrative structure uses deeper heading nesting with tables underneath.

**[UNVERIFIED]** -- This is an observation about generated output structure, not code. The absence of R-item granularity enforcement in the roadmap prompts is confirmed (no "minimum items per subsection" or "1:1 work-item-to-table-row" instruction exists in `build_generate_prompt` or `build_merge_prompt`).

---

## 5. Gap Registry (12 Gaps Identified)

The prior research identified 12 gaps across 3 severity levels:

| Severity | Gaps | Status |
|----------|------|--------|
| HIGH (5) | G1 (PRD suppression in tasklist prompt), G2 (protocol merge directives), G3 (no task count floor), G5 (R-item granularity), G9 (no anti-consolidation guard) | G1: [CODE-VERIFIED] still present. G2: [CODE-VERIFIED] still present. G3: [CODE-VERIFIED] absent. G5: [UNVERIFIED]. G9: [CODE-VERIFIED] absent. |
| MEDIUM (5) | G4 (no phase count guidance), G6 (testing absorption), G7 (scope boundary suppression), G10 (interaction block amplifies suppression), G12 (subjective merge criteria) | G4: [CODE-VERIFIED] -- partially addressed by new phasing instructions in roadmap prompts. G7/G10: [CODE-VERIFIED] still present. G12: [CODE-VERIFIED] still present. |
| LOW (2) | G8 (Section 3.x framing), G11 (output token ceiling) | G8: [UNVERIFIED]. G11: model constraint, not code-fixable. |

---

## 6. Prior Recommendation

The prior research recommended **Option C: Fix Both Prompt + Protocol + Roadmap Phase Count Guidance** (10/12 gaps addressed). The implementation plan had 11 steps across 3 files:

1. `src/superclaude/cli/tasklist/prompts.py` -- Remove PRD suppression, add anti-consolidation guard
2. `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` -- Tighten merge criteria, add task count floor, add testing minimums
3. `src/superclaude/cli/roadmap/prompts.py` -- Add phase count guidance, merge phase floor

### Implementation Status Assessment

Based on code verification:

| Component | Fix Status |
|-----------|-----------|
| Tasklist `prompts.py` PRD suppression (G1) | **NOT FIXED** -- suppression language at lines 221-223 unchanged |
| Tasklist `prompts.py` anti-consolidation guard (G9) | **NOT FIXED** -- no guard present |
| Tasklist `prompts.py` interaction block (G10) | **NOT FIXED** -- "shapes task descriptions" framing unchanged |
| SKILL.md merge directives (G2, G12) | **NOT FIXED** -- merge language at lines 233, 255, 259 unchanged |
| SKILL.md task count floor (G3) | **NOT FIXED** -- no Section 4.4c or task count assertion exists |
| Roadmap `prompts.py` phase count (G4) | **PARTIALLY FIXED** -- TDD block now mandates technical-layer phasing; PRD block now prevents phase count reduction. No explicit phase count range heuristic added. |
| Roadmap `prompts.py` generate prompt TDD granularity | **PARTIALLY FIXED** -- lines 463-475 now contain explicit per-item decomposition instructions ("create a SEPARATE task table row for EACH independently implementable item") |

---

## 7. Pipeline Trace Summary

The pipeline trace investigation (reviews/pipeline-trace-investigation.md) traced the data through all 4 stages:

| Stage | Behavior | Collapse? |
|-------|----------|-----------|
| Stage 1: Extraction | TDD extraction has 14 sections, ~85 entities vs spec's 8 sections, ~49 entities. Granularity preserved. | No |
| Stage 2: Generation | TDD+PRD variants adopt 3-phase delivery structure vs spec's 5-phase technical layers. Content per phase is denser but fewer buckets. | **Yes -- structural** |
| Stage 3: Merge | Merge preserves 3-phase structure from winning base variant. No active reduction. | No (inherited) |
| Stage 4: Tasklist | Perfect 1:1 R-item-to-task mapping in both cases. Tasklist generator is deterministic. | No |

**Key finding**: The collapse occurs at Stage 2 (roadmap generation) and is inherited downstream. The tasklist generator is functioning correctly -- the problem is its input.

---

## 8. Stale Documentation Found

1. **Pipeline trace "88 R-items" claim**: The pipeline trace investigation (lines 23-24) states "R-items parsed: 88" for TDD+PRD. The R-item collapse investigation later corrected this to 44. The pipeline trace document was NOT updated to reflect this correction.

2. **Research report line references to `prompts.py`**: The research report references specific line numbers (e.g., "lines 221-223", "lines 229-234") in `tasklist/prompts.py`. These line numbers are **still accurate** as of the current codebase. However, line references to `roadmap/prompts.py` may be stale -- the file has been modified since the research (the TDD and PRD blocks now contain anti-consolidation language not described in the research).

3. **Research report's characterization of `build_generate_prompt` TDD block**: The report describes the TDD supplementary context as saying "Include phased rollout tasks with feature flags, rollback procedures." The current code (lines 457-481) has been substantially rewritten to instead say "Use technical-layer phasing... regardless of any rollout/milestone structure in the TDD." This is a significant behavioral change that the research report does not reflect.

4. **Research report's characterization of `build_generate_prompt` PRD block**: The report describes the PRD block as introducing "value-based prioritization" that pushes toward delivery-milestone phasing. The current code (lines 484-504) now explicitly says PRD "does NOT change the number of phases, the phasing paradigm (technical layers, not delivery milestones), or reduce the number of task rows." This contradicts the research report's description.

---

## 9. Gaps and Questions

### UNVERIFIED Claims Requiring Re-Investigation

1. **H5 (R-item granularity bundling)**: The claim that ~112 work items get bundled into 44 R-items cannot be verified against code -- it depends on LLM output behavior. With the new TDD block instructions mandating per-item decomposition, this bundling may be reduced in future runs.

2. **H3 (5.6:1 testing absorption)**: Output-level observation. Cannot verify whether the ratio persists under the current (partially fixed) prompts without re-running the pipeline.

3. **Section 3.x framing (G8)**: Whether the SKILL.md enrichment framing primes consolidation behavior is LLM-behavioral, not code-structural.

### CODE-CONTRADICTED Claims

4. **The roadmap generate prompt's TDD block**: The prior research describes this as passively allowing TDD rollout plans to become the organizing structure. The current code actively prevents this with "Use technical-layer phasing... regardless of any rollout/milestone structure in the TDD." **This is a material change not reflected in the research report.**

5. **The roadmap generate prompt's PRD block**: The prior research describes PRD as introducing "value-based prioritization" that causes fewer phases. The current code explicitly prevents PRD from changing phase count or paradigm. **This is a material change not reflected in the research report.**

### Outstanding Questions

6. **When were the roadmap prompt fixes applied?** If before the test fixture runs, the 3-phase collapse should not have occurred. If after, the fixes address H1 but have not been validated with a new test run.

7. **Are the partial fixes sufficient?** The roadmap generate prompt now has anti-consolidation language, but the tasklist prompt (G1, G9, G10) and SKILL.md protocol (G2, G3, G12) remain unfixed. The pipeline may still produce fewer tasks than expected if the roadmap itself is now granular but the tasklist generator's merge directives over-consolidate.

8. **Test fixture staleness**: The test fixtures in `.dev/test-fixtures/results/` may predate the roadmap prompt fixes. New test runs are needed to determine whether the partial fixes change the outcome.

---

## 10. Summary

The prior tasklist-quality research (2026-04-03) identified a multi-layered granularity loss problem where 4.1x richer input produced 49% fewer tasks. The investigation was thorough and its core conclusions hold, with these key takeaways for the current overhaul:

**Still valid and unfixed:**
- Tasklist `prompts.py` PRD suppression language (H2/G1) -- the single strongest root cause
- SKILL.md protocol merge directives (H4/G2) -- 3+ merge instructions with vague criteria
- No task count floor anywhere in the pipeline (G3)
- No anti-consolidation guard in tasklist prompts (G9)
- Testing task absorption pattern (H3/G6) -- no standalone test task minimum

**Partially addressed since research:**
- Roadmap generate prompt now mandates technical-layer phasing (H1/G4 partial fix)
- Roadmap generate prompt TDD block now requests per-item decomposition (G5 partial fix)
- Roadmap generate prompt PRD block now prevents phase count reduction

**Not fixable via code:**
- Output token ceiling redistribution (G11) -- model constraint
- LLM behavioral tendencies toward consolidation -- can only be mitigated, not eliminated

**Recommended action**: The prior research's Option C implementation plan remains largely applicable, but Steps 10 (phase count guidance in roadmap prompt) and parts of the TDD/PRD block changes may already be addressed. Focus implementation effort on the **unfixed** items: tasklist prompt suppression removal (Steps 1-2, 9), SKILL.md protocol tightening (Steps 3-8), and run new test fixtures to validate the partial roadmap fixes already in place.
